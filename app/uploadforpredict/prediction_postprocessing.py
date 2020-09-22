from backend.settings import MEDIA_BASE_URL, DEBUG, MEDIA_ROOT
from django.core.files.storage import FileSystemStorage

import json
import csv
import os
import numpy as np
from pprint import pprint
from time import time

from taxonomy.models import Family, Subfamily, Genus, Species
from image.models import Image

strt_time = time()

HIER_ORDER = ['species', 'genus', 'subfamily', 'family']
prob_order = [x+'_prob' for x in HIER_ORDER]
prediction_keys = HIER_ORDER + prob_order
NUM_RESULTS = 5
NUM_EXAMPLE_IMAGES = 6

#Model class should not have to class Tensorflow Container?

# in hierarchy model subclass
def load_class_hierarchy_map(model_record):
    
    class_map_str = model_record.class_hierarchy_map
    class_hierarchy_map = json.loads(class_map_str)

    return class_hierarchy_map


#part of generic base model class
def softmax(x):

    """Compute softmax values for each sets of scores in x."""
    e_x = np.exp(x - np.max(x))
    return e_x / e_x.sum()

#in hierarchy model subclass
def calc_class_probas(model_raw_response, class_hierarchy_map):
    """
    sum up the probabilites at each hierarchical level
    """

    probas = {}
    probas[HIER_ORDER[0]] = softmax(model_raw_response)

    for i in range(1, len(HIER_ORDER)):
        
        parent_key = HIER_ORDER[i]
        child_key = HIER_ORDER[i-1]
        probas[parent_key] = np.bincount(class_hierarchy_map[parent_key], weights=probas[child_key])

    return probas


#in hierarchy model subclass
def calc_top_results(all_class_probas, hier_enco):

    # subscript(insert) the probabilities for each level in the hierarchy
    prob_levels = [all_class_probas[key][hier_enco[:,i]] for i, key in enumerate(HIER_ORDER)]
    arr_prob = np.array(prob_levels)
    arr_prob = arr_prob 

    # multi index sort, from last column in array to first 
    # (ie from coarsest to finest hierarchical level / top down) 
    sort_keys = np.lexsort(arr_prob)

    # take top n results
    top_sorted_keys = sort_keys[::-1][:NUM_RESULTS]
    top_probs = arr_prob.transpose()[top_sorted_keys,:]
    top_classes = hier_enco[top_sorted_keys,:]

    return top_classes, top_probs

#NOT in class
def query_db_to_make_dict_of_taxonomy_names(species_key):
    
    res_dict = {}

    s = Species.objects.get(id=species_key)
    g = Genus.objects.get(species=s.id)
    sf = Subfamily.objects.get(genus=g.id)
    f = Family.objects.get(subfamily=sf.id)

    res_dict['species'] = s.name
    res_dict['genus'] = g.name
    res_dict['subfamily'] = sf.name
    res_dict['family'] = f.name

    return res_dict


#NOT in class
def query_example_images(species_key, num_images):
    
    fs = FileSystemStorage()

    qs = Image.objects.filter(imageclassification__species_key=species_key)
    res = qs.values('image').distinct()[:num_images].values()
    
    return [fs.url(obj['image']) for obj in res]

#in class
def process_model_response(model_record, model_response):
    
    if DEBUG:
        print('model returned: ', model_response.status_code)
    
    model_response_dict = json.loads(model_response.text)
    model_raw_values = model_response_dict['predictions'][0]  #these model values are known as logits

    if DEBUG:
        print('model_raw_values: ', str(model_raw_values[:15])[:-1], ' ...')

    #Load reference files
    class_hierarchy_map = model_record.class_hierarchy_map
    hier_enco = np.array(model_record.encoded_hierarchy)
    model_key_map = model_record.species_key_map

    # create sorted results
    all_class_probas = calc_class_probas(model_raw_values, class_hierarchy_map)
    top_model_classes, top_probs = calc_top_results(all_class_probas, hier_enco)

    top_db_classes = [model_key_map[str(m_key[0])] for m_key in top_model_classes]

    if DEBUG:
        print('all_class_probas: ', all_class_probas)
        print('top_probs : ', top_probs)
        print('top_classes : ', top_model_classes)
        print('top_db_classes: ', top_db_classes)

    predictions = {}
    prob_order = ['species_prob', 'genus_prob', 'subfamily_prob', 'family_prob']

    #loop over the classes_probs list to assemble the predictions part of the json response
    
    for i, species_key in enumerate(top_db_classes):
        
        res_dict = query_db_to_make_dict_of_taxonomy_names(species_key)
        probs_dict = dict(zip(prob_order, top_probs[i,:].tolist()))
        res_dict.update(probs_dict)

        img_lst = query_example_images(species_key, NUM_EXAMPLE_IMAGES)
        res_dict['example_images'] = img_lst
        res_dict['example_image_0'] = img_lst[0] # included for legacy reasons due to how mobile app consumes the reponse
        res_dict['description'] = ""
        res_dict['index'] = species_key
        predictions[i] = res_dict

    return predictions