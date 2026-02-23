import json, pickle
from preprocessing import preprocess
from api_fallback import get_ai_response

# Load trained model
model = pickle.load(open("model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

# Load intents
with open("intents.json") as f:
    intents = json.load(f)

def get_dataset_response(tag):
    for intent in intents["intents"]:
        if intent["tag"] == tag:
            return intent["responses"][0]

def get_response(user_input):
    processed = preprocess(user_input)
    X = vectorizer.transform([processed])

    # Predict intent & confidence
    intent = model.predict(X)[0]
    confidence = max(model.predict_proba(X)[0])

    print("Intent:", intent, "Confidence:", confidence)  # debug

    # ✅ If model confident → use dataset
    if confidence >= 0.65:
        return "📚 " + get_dataset_response(intent)

    # ❌ If not confident → use Gemini
    else:
        ai_response = get_ai_response(user_input)
        return "🤖 " + (ai_response if ai_response else "Sorry, I couldn't generate a response.")