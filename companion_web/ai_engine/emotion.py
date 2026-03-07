from transformers import pipeline
emotion_classifier=pipeline(
    "text-classification",
    model="j-hartmann/emotion-english-distilroberta-base"
)


def detect_emotion(text):
    result=emotion_classifier(text)[0]
    return result["label"].lower()