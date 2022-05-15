import os
import json
import random
from transformers import pipeline
from tqdm import tqdm

classifier = pipeline("zero-shot-classification", model="roberta-large-mnli")
# classifier = pipeline("zero-shot-classification", model="pdelobelle/robbert-v2-dutch-base")

d = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
secondary_education_data = os.path.join(os.path.join(d, "English Sector Separated"), "Secondary Education")

print(secondary_education_data)
files = os.listdir(secondary_education_data)
selection = files
# subjects = ["Economics", "Statistics", "Computers", "Programming", "Security", "Religion", "Mathematics", "Sciences", "History", "Geography", "Physical education", "Information Technology"]
# subjects = ["Government", "K12", "Higher education", "Healthcare", "Educational publishers", "Exam centers", "Corporate"]
subjects = ["Chemistry", "History", "Physicis", "Biology", "Algebra", "Number Theory", "Geometry", "Arithmetic", "Programming", "Computers", "Geography", "Physical Education"]

result_file_path = os.path.join(d, "subjects-3.txt")


with open(result_file_path, "a+") as result_file:
    
    result_file.write("============================\n      USED SUBJECT LABELS      \n============================\n")
    for subject in subjects:
        result_file.write(subject + "\n") 
    
    result_file.write("============================\n            RESULTS            \n============================\n")
    
    count = 0
    for file in tqdm(selection):
        file_path = os.path.join(secondary_education_data, file)
        with open(file_path) as file:
            json_file = json.load(file)
            text = json_file["Textual_data"].split('\n',1)[1]
            if(len(text) > 100):
                result_file.write("\n")
                result_file.write("***** ITEM " + str(count) + " *****\n")
                classification = classifier(text, subjects)
                result_file.write("\nINPUT:\n")
                result_file.write(classification['sequence'] + "\n")
                result_file.write("\nPROBABILITIES:\n")
                for i in range(0, len(subjects)):
                    result_file.write('\t' + classification['labels'][i] + ": " + str(classification['scores'][i]) + '\n')
                result_file.write("\n")
                count = count + 1