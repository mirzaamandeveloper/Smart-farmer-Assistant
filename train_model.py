import json, pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from preprocessing import preprocess

with open("intents.json") as f:
    data = json.load(f)

texts, labels = [], []

for intent in data["intents"]:
    for pattern in intent["patterns"]:
        texts.append(preprocess(pattern))
        labels.append(intent["tag"])

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(texts)

model = LogisticRegression()
model.fit(X, labels)

pickle.dump(model, open("model.pkl", "wb"))
pickle.dump(vectorizer, open("vectorizer.pkl", "wb"))