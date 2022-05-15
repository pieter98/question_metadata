from transformers import pipeline

classifier = pipeline("zero-shot-classification")

sequence = "Who are you voting for in 2020?"
candidate_labels = ["politics", "public health", "economics"]

hypothesis_template="The topic of this text is {}"

print(classifier(sequence, candidate_labels, hypothesis_template))
print(classifier(sequence, candidate_labels))
