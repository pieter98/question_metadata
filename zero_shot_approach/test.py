from transformers import pipeline

classifier = pipeline("zero-shot-classification")

sequence = "Who are you voting for in 2020?"
candidate_labels = ["politics", "public health", "economics"]

print(classifier(sequence, candidate_labels))
