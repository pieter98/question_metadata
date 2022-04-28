import os
import json
from tqdm import tqdm
from bs4 import BeautifulSoup

'''
===================================================================================================================
METHOD: (extract_textual_data)
as the name suggests this method extracts the textual data from the assessmentQ question data

PARAMS:
dir_path: path to directory containing the questions you want to process
===================================================================================================================
'''
def extract_textual_data(dir_path):
    if os.path.isdir(dir_path):

        # go over all files in the directory
        for file_name in tqdm(os.listdir(dir_path)):
            file_path = os.path.join(dir_path, file_name)
            file = open(file_path)
            json_file = json.load(file)

            # Extract textual data and group it in a new property "Textual_data"
            json_file["Textual_data"] = json_file["Metadata"]["Location"].replace('>',' ')
            json_file["Textual_data"] += "\n"
            json_file["Textual_data"] += BeautifulSoup(json_file['Instruction'], 'html.parser').text
            if 'Answers' in json_file:
                for i in json_file['Answers']:
                    if "Value" in i and i["Value"] is not None:
                        json_file["Textual_data"] += '\n' + BeautifulSoup(i['Value'], 'html.parser').text
                    if "Text" in i and i["Text"] is not None:
                        json_file["Textual_data"] += '\n' + BeautifulSoup(i['Text'], 'html.parser').text
            if 'keywords' in json_file:
                for i in json_file['keywords']:
                    if "Value" in i and i["Value"] is not None:
                        json_file["Textual_data"] += '\n' + BeautifulSoup(i['Value'], 'html.parser').text


            with open(file_path,"w") as file:
                json.dump(json_file, file)

# Example usage
path = os.path.join(os.getcwd(), "Questions")
dirs = os.listdir(path)
for dir in dirs:
    dir_path = os.path.join(path, dir)
    extract_textual_data(dir_path)
   




            



