from bs4 import BeautifulSoup
from textblob import TextBlob
from tqdm import tqdm
import json
import os

# preprocessing for multiple choice questions

main_dir = os.path.dirname(__file__)
data_path = os.path.join(
    main_dir, '20220124 - Question & Answer data (Fill Gaps, Multiple Choice & Open Question)')
questions_data_path = os.path.join(
    data_path, 'Multiple Choice Questions & Answers/Multiple Choice Questions')
file_path = os.path.join(
    questions_data_path, '000089A8-74F6-4BC4-8320-FA720DA56EF0.mcq.json')

languages = ['c:\\Users\\piete\\Documents\\1) Topic modelling\\af', 'c:\\Users\\piete\\Documents\\1) Topic modelling\\ar', 'c:\\Users\\piete\\Documents\\1) Topic modelling\\ca', 'c:\\Users\\piete\\Documents\\1) Topic modelling\\co', 'c:\\Users\\piete\\Documents\\1) Topic modelling\\cs', 'c:\\Users\\piete\\Documents\\1) Topic modelling\\da', 'c:\\Users\\piete\\Documents\\1) Topic modelling\\de', 'c:\\Users\\piete\\Documents\\1) Topic modelling\\en', 'c:\\Users\\piete\\Documents\\1) Topic modelling\\es', 'c:\\Users\\piete\\Documents\\1) Topic modelling\\et', 'c:\\Users\\piete\\Documents\\1) Topic modelling\\fi', 'c:\\Users\\piete\\Documents\\1) Topic modelling\\fr', 'c:\\Users\\piete\\Documents\\1) Topic modelling\\fy', 'c:\\Users\\piete\\Documents\\1) Topic modelling\\gu', 'c:\\Users\\piete\\Documents\\1) Topic modelling\\hi', 'c:\\Users\\piete\\Documents\\1) Topic modelling\\hu', 'c:\\Users\\piete\\Documents\\1) Topic modelling\\id', 'c:\\Users\\piete\\Documents\\1) Topic modelling\\it', 'c:\\Users\\piete\\Documents\\1) Topic modelling\\ja', 'c:\\Users\\piete\\Documents\\1) Topic modelling\\jw',
             'c:\\Users\\piete\\Documents\\1) Topic modelling\\kn', 'c:\\Users\\piete\\Documents\\1) Topic modelling\\la', 'c:\\Users\\piete\\Documents\\1) Topic modelling\\lb', 'c:\\Users\\piete\\Documents\\1) Topic modelling\\lv', 'c:\\Users\\piete\\Documents\\1) Topic modelling\\mg', 'c:\\Users\\piete\\Documents\\1) Topic modelling\\nl', 'c:\\Users\\piete\\Documents\\1) Topic modelling\\no', 'c:\\Users\\piete\\Documents\\1) Topic modelling\\ny', 'c:\\Users\\piete\\Documents\\1) Topic modelling\\pl', 'c:\\Users\\piete\\Documents\\1) Topic modelling\\pt', 'c:\\Users\\piete\\Documents\\1) Topic modelling\\ro', 'c:\\Users\\piete\\Documents\\1) Topic modelling\\ru', 'c:\\Users\\piete\\Documents\\1) Topic modelling\\sk', 'c:\\Users\\piete\\Documents\\1) Topic modelling\\sl', 'c:\\Users\\piete\\Documents\\1) Topic modelling\\sm', 'c:\\Users\\piete\\Documents\\1) Topic modelling\\sn', 'c:\\Users\\piete\\Documents\\1) Topic modelling\\sv', 'c:\\Users\\piete\\Documents\\1) Topic modelling\\te', 'c:\\Users\\piete\\Documents\\1) Topic modelling\\vi', 'c:\\Users\\piete\\Documents\\1) Topic modelling\\zu']


for filename in tqdm(os.listdir(questions_data_path)[57000:]):

    try:
        # open file + load the json
        with open(os.path.join(questions_data_path, filename), encoding="utf8") as f:

            data = json.load(f)
            # create text file by combining
            #   1) location in assessmentq as "title" (may contain extra info about topic)
            #   2) the instruction text
            #   3) the possible question answers
            multiple_choice_text = BeautifulSoup(
                data['Metadata']['Location'], 'html.parser').text
            multiple_choice_text += '\n' + \
                BeautifulSoup(data['Instruction'], 'html.parser').text
            for i in data['Answers']:
                multiple_choice_text += '\n' + \
                    BeautifulSoup(i['Value'], 'html.parser').text

            # detect language using Textblob
            # TextBlob invokes the google API, therefor while loop in case connection issue -> retry until success
            while True:
                try:
                    dir = TextBlob(multiple_choice_text).detect_language()
                except Exception:
                    continue
                else:
                    break

            # use id as textfile name
            text_file_name = data['Id'] + '.txt'

            target_dir = os.path.join(main_dir, dir)
            if not os.path.isdir(target_dir):
                os.mkdir(target_dir)

            with open(os.path.join(target_dir, text_file_name), "w", encoding="utf8") as new_f:
                new_f.write(multiple_choice_text)

    except:
        continue
