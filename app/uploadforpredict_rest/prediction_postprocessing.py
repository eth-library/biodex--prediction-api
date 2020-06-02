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
MEDIA_URL = '/media/2017_03_10R/'
ASSETS_DIR = os.path.join(BASE_DIR, 'backend/assets')
EXAMPLE_IMAGES_DIR = os.path.join(BASE_DIR, 'backend/assets','example_images')
EXAMPLE_IMAGES_BASE_URL = 'http://0.0.0.0:8000' + MEDIA_URL

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


def load_encoded_hierarchy():
    
    fpath = os.path.join(ASSETS_DIR, 'encoded_hierarchy.csv')
    hier_enco = load_csv_as_array(fpath, datatype=np.int0, skip_header=True)
    
    return hier_enco


def load_class_maps():
    
    fname = 'class_hierarchy_maps.json'
    fpath = os.path.join(ASSETS_DIR, fname)
    with open(fpath, 'r') as f:
        class_maps = json.load(f)
    
    for k,v in class_maps.items():
        class_maps[k] = np.array(v)
    
    return class_maps


def load_class_codings():

    fname = 'class_encodings.json'
    fpath = os.path.join(ASSETS_DIR, fname)
    
    with open(fpath,'r') as f:
        class_encodings = json.load(f)
    
    for k,v in class_encodings.items():
        class_encodings[k] = np.array(v)

    return class_encodings


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


def calc_class_probas(model_response, class_maps):
    """
    sum up the probabilites at each hierarchical level
    """

    probas = {}
    probas[HIER_ORDER[0]] = softmax(model_response)

    for i in range(1, len(HIER_ORDER)):
        
        parent_key = HIER_ORDER[i]
        child_key = HIER_ORDER[i-1]
        probas[parent_key] = np.bincount(class_maps[parent_key], probas[child_key])

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


def process_model_response(model_response):

    #Load reference files
    class_maps = load_class_maps()
    hier_enco = load_encoded_hierarchy()
    class_encodings = load_class_codings()
    example_img_dict = load_example_img_dict()

    # create sorted results
    all_class_probas = calc_class_probas(model_response, class_maps)
    top_classes, top_probs = calc_top_results(all_class_probas, hier_enco)
    
    top_classes_str = np.array([class_encodings[HIER_ORDER[i]][top_classes[:,i]] for i in range(len(HIER_ORDER))])
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
        img_lst = example_img_dict[str(temp_dict['species_key'])]
        temp_dict['example_images'] = img_lst
        temp_dict['example_image_0'] = img_lst[0] # included for legacy reasons due to how mobile app consumes the reponse
        temp_dict['description'] = ""
        predictions[i] = temp_dict

    return predictions


####!!! Move below functions into views.py ? ####

# #Load reference files
# class_maps = load_class_maps()
# hier_enco = load_encoded_hierarchy()
# class_encodings = load_class_codings()
# example_img_dict = load_example_img_dict()

# predictions = make_predictions_response(model_response, 
#                             class_maps, 
#                             hier_enco, 
#                             class_encodings, 
#                             example_img_dict)


#run main predictions functions
# predictions = make_predictions_response(model_response, 
#                             class_maps, 
#                             hier_enco, 
#                             class_encodings, 
#                             example_img_dict)

# predictions = process_model_response(model_response)

# total_time = time() - strt_time
# print('execution time: {}'.format(total_time))

