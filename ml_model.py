from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import pickle

# 🧠 SAMPLE TRAINING DATA (SIMPLIFIED FOR CAPSTONE)
texts = [
    "small fire kitchen",
    "electric spark minor smoke",
    "burning trash low fire",
    "warehouse full fire spreading fast",
    "building engulfed flames",
    "gas explosion fire large",
    "vehicle fire road",
    "small electrical fire outlet"
]

labels = [
    "Low",
    "Low",
    "Low",
    "High",
    "High",
    "High",
    "Medium",
    "Low"
]

# 🔤 TEXT TO NUMBERS
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(texts)

# 🤖 TRAIN MODEL
model = MultinomialNB()
model.fit(X, labels)

# 💾 SAVE MODEL
pickle.dump(model, open("fire_model.pkl", "wb"))
pickle.dump(vectorizer, open("vectorizer.pkl", "wb"))

print("Model trained successfully!")