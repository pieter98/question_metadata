# basic imports
import os
import re
import json
from unicodedata import name

# language detection imports
import spacy
from spacy.language import Language
from spacy_langdetect import LanguageDetector
from langdetect import detect
from googletrans import Translator
import fasttext as ft

# utility imports
from tqdm import tqdm
from bs4 import BeautifulSoup


ft_model = ft.load_model("./fasttext_pretrained/lid.176.bin")

'''
===================================================================================================================
METHOD: (get_lang_detector)
helper method for initiating spacy langdetect
===================================================================================================================
'''
def get_lang_detector(nlp, name):
    return LanguageDetector()


'''
===================================================================================================================
METHOD: (fasttext_language_predict)
helper method for fasttext language predictions

PARAMS:
text:   the text for which to predict the language
model:  the fasttext model that needs to be used
===================================================================================================================
'''
def fasttext_language_predict(text, model = ft_model):
    text = text.replace('\n', ' ')
    prediction = model.predict([text])
    return prediction

'''
===================================================================================================================
METHOD: (extract_language)
as the name suggests this method derrives the language from the textual data in the assessmentQ question

PARAMS:
dir_path:   path to directory containing the questions you want to process
debug:      indicates if debug logging is needed
===================================================================================================================
'''

def extract_language(dir_path, debug = False):

    spacy_detector = spacy.load('en_core_web_sm')
    Language.factory("language_detector", func=get_lang_detector)
    spacy_detector.add_pipe('language_detector', last=True)

    google_translator = Translator()


    if os.path.isdir(dir_path):

        # go over all files in the directory
        for file_name in tqdm(os.listdir(dir_path)):
            file_path = os.path.join(dir_path, file_name)
            file = open(file_path)
            json_file = json.load(file)
            
            voting_dict = {}
            
            if debug:
                print(json_file["Textual_data"])
            
            if json_file["Textual_data"] != "":
                try:
                    pred1 = detect(json_file["Textual_data"])
                except:
                    pred1 = ""
                pred2 = spacy_detector(json_file["Textual_data"])._.language['language']
                # Errors can occur in the goole_Translator detect, catch these errors
                try:
                    pred3 = google_translator.detect(json_file["Textual_data"]).lang
                except:
                    pred3 = ""
                pred4 = fasttext_language_predict(json_file["Textual_data"])[0][0][0].replace("__label__", "")

                if pred1 != "":
                    voting_dict[pred1] = 1

                if pred2 in voting_dict.keys():
                    voting_dict[pred2] += 1
                else:
                    voting_dict[pred2] = 1
                    
                if pred3 in voting_dict.keys() and pred3 != "":
                    if pred3 == 'nl':
                        voting_dict[pred3] += 2
                    else:
                        voting_dict[pred3] += 1
                else:
                    # google_translator gets a higher weighted vote for dutch ("nl") 
                    if pred3 == 'nl':
                        voting_dict[pred3] = 2
                    else:
                        voting_dict[pred3] = 1

                if pred4 in voting_dict.keys():
                    voting_dict[pred4] += 1
                else:
                    voting_dict[pred4] = 1
                    
                # json_file["Metadata"]["Language"] = max(voting_dict, key=voting_dict.get)
                if(debug):
                    print(json_file["Metadata"]["Language"])
                    print(voting_dict)
                    print(pred1 + " " + pred2 + " " + pred3 + " " + pred4)
                    print(max(voting_dict, key=voting_dict.get))
                
                json_file["Metadata"]["Language"] = max(voting_dict, key=voting_dict.get)

                with open(file_path,"w") as file:
                    json.dump(json_file, file)


# Example usage
path = os.path.join(os.getcwd(), "Questions")
dir_path = os.path.join(path, "Fill Gaps Questions")
extract_language(dir_path)
# dirs = os.listdir(path)

'''
for dir in dirs[1:]:
    dir_path = os.path.join(path, dir)
    extract(dir_path)'''