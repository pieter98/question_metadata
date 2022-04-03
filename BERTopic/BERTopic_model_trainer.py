import os
import numpy
from tqdm import tqdm
from pathlib import Path
from bertopic import BERTopic
from sklearn.datasets import fetch_20newsgroups

'''
docs = fetch_20newsgroups(subset='all',  remove=('headers', 'footers', 'quotes'))['data']
print(type(docs))
print(type(docs[0]))
print(len(docs[0]))
'''

main_dir = os.getcwd()
print(main_dir)

target_folder = "nl"
iteration = 3

target_folder_path = os.path.join(main_dir, target_folder)
print("===== Initialization =====\n")
print("Target folder path: " + target_folder_path)

print("\t Data files in target folder: " + str(len(os.listdir(target_folder_path))))


documents = []

word_threshold = 500

print("\nTransform text files to list of strings, filter out text files who don't have atleast " + str(word_threshold) + " words:")

for file in tqdm(os.listdir(target_folder_path)):
    text = " ".join(Path(os.path.join(target_folder_path, file)).read_text(encoding="utf8").split('\n')[1:]).strip()
    if len(text) > word_threshold:
        documents.append(text)


print("\tTotal text files that furfill the requirements: " + str(len(documents)) + "\n\n")



print("===== Initiate Bert =====")
print("\tStart")
topic_model = BERTopic(language="Dutch")
print("\tDone\n")
print("===== Fit transform =====")
topics, probabilities = topic_model.fit_transform(documents)


print("Topics information:")
print(topic_model.get_topic_info())

topic_model.visualize_topics()

topic_model.save("BERTopic-language-dutch-" + str(iteration))

a = numpy.asarray(probabilities)
numpy.savetxt("probabilities-nl-" + str(iteration) +".csv", a, delimiter=",")
