from bertopic import BERTopic
import csv

bert = BERTopic.load("BERTopic-language-dutch-2")

print(bert.get_topic_info())
for topic in bert.get_topics():
    if topic <= 20:
        print(topic)
        print(bert.get_topic(topic))


with open("dutch-topics-model-1.csv" , "w", newline="") as csv_export:
    csv_writer = csv.writer(csv_export)
    csv_writer.writerow(['Group Number', 'Frequency', 'Keywords'])
    for topic in bert.get_topics():
        csv_writer.writerow([str(topic), bert.get_topic_freq(topic), ] + [i[0] for i in bert.get_topic(topic)])
