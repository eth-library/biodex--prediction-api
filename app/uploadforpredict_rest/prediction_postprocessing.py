from backend.settings import MEDIA_BASE_URL
import json
import csv
import os
import numpy as np
from pprint import pprint
from time import time


curdir = os.path.dirname(os.path.abspath(__file__))

strt_time = time()
# these path definitions are temporary, should be imported from settings 
BASE_DIR = os.path.join(curdir, '..')

MEDIA_ROOT = os.path.join(BASE_DIR, '..', 'uploaded_media')

ASSETS_DIR = os.path.join(BASE_DIR, 'backend/assets')
EXAMPLE_IMAGES_DIR = os.path.join(BASE_DIR, 'backend/assets','example_images')

HIER_ORDER = ['species', 'genus', 'subfamily', 'family']
prob_order = [x+'_prob' for x in HIER_ORDER]
prediction_keys = HIER_ORDER + prob_order
NUM_RESULTS = 5


def load_csv_as_array(fpath, datatype=np.int0, skip_header=True):
    """
    load a csv file and return as a numpy array
    faster than loading using pandas but all cols must be same datatype
    skips first row by default
    """
    with open(fpath,'r') as dest_f:
        data_reader = csv.reader(dest_f,
                                delimiter = ',',
                                quotechar = '"')
        if skip_header:
            next(data_reader) #skips the header/first line
    
        data = [data for data in data_reader]
    
    return np.asarray(data, datatype)


# def load_encoded_hierarchy(model_record):
    
#     # fpath = os.path.join(ASSETS_DIR, 'encoded_hierarchy.csv')
#     # hier_enco = load_csv_as_array(fpath, datatype=np.int0, skip_header=True)
    
#     hier_enco = model_record.encoded_hierarchy
#     # hier_enco = 
    
#     return hier_enco


def load_class_hierarchy_map(model_record):
    
    # old way was to load from file

    # fname = 'class_hierarchy_maps.json'
    # fpath = os.path.join(ASSETS_DIR, fname)
    # with open(fpath, 'r') as f:
    #     class_maps = json.load(f)
    
    # for k,v in class_maps.items():
    #     class_maps[k] = np.array(v)
    
    class_map_str = model_record.class_hierarchy_map
    class_hierarchy_map = json.loads(class_map_str)

    return class_hierarchy_map

def load_charfield_as_dict(char_field):

    lst = json.loads(char_field)
    array = np.from_list(lst)

    return array


def load_charfield_as_numpy(char_field):

    lst = json.loads(char_field)
    array = np.from_list(lst)

    return array



def load_example_img_dict():

    fname = 'example_images.json'
    fpath = os.path.join(ASSETS_DIR, fname)
    
    with open(fpath,'r') as f:
        example_img_dict = json.load(f)

    for k,img_lst in example_img_dict.items():
        example_img_dict[k] = [EXAMPLE_IMAGES_BASE_URL + os.path.basename(img) for img in img_lst]

    return example_img_dict


def softmax(x):

    """Compute softmax values for each sets of scores in x."""
    e_x = np.exp(x - np.max(x))
    return e_x / e_x.sum()


def calc_class_probas(model_response, class_hierarchy_map):
    """
    sum up the probabilites at each hierarchical level
    """

    probas = {}
    probas[HIER_ORDER[0]] = softmax(model_response)

    for i in range(1, len(HIER_ORDER)):
        
        parent_key = HIER_ORDER[i]
        child_key = HIER_ORDER[i-1]
        probas[parent_key] = np.bincount(class_hierarchy_map[parent_key], weights=probas[child_key])

    return probas


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


def query_example_images(species_key, num_results):
    
    qs = Image.objects.filter(imageclassification__species_key=1000)
    res = qs.values('image').distinct()[:num_results].values()

    return [MEDIA_BASE_URL + obj['image'] for obj in res]


def process_model_response(model_record, model_response):

    #Load reference files
    class_hierarchy_map = json.loads(model_record.class_hierarchy_map)
    hier_enco = load_charfield_as_numpy(model_record.encoded_hierarchy)
    model_key_map = load_charfield_as_numpy(model.record)

    # create sorted results
    all_class_probas = calc_class_probas(model_response, class_hierarchy_map)
    top_classes, top_probs = calc_top_results(all_class_probas, hier_enco)
    
    # subscript the hierarchy order to get the class names
    top_classes_str = [class_encodings[HIER_ORDER[i]][top_classes[:,i]] for i in range(len(HIER_ORDER))]
    top_classes_str = np.array()
    top_classes_str = top_classes_str.transpose()

    #join the rows of the array of classes names and the array of probabilities together
    classes_probs = np.hstack((top_classes_str, top_probs))
    classes_probs = classes_probs.tolist() 

    #loop over the classes_probs list to assemble the predictions part of the json response
    predictions = {}
    prediction_keys = HIER_ORDER + prob_order

    for i in range(len(classes_probs)):

        temp_dict = dict(zip(prediction_keys, classes_probs[i]))
        temp_dict['species_key'] = top_classes[i,0]
        temp_dict['example_images'] = query_example_images(species_key, num_results)
        # temp_dict['example_image_0'] = img_lst[0] # included for legacy reasons due to how mobile app consumes the reponse
        temp_dict['description'] = ""
        predictions[i] = temp_dict

    return predictions