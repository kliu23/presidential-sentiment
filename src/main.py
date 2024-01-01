import json
import os


emotions = [
    "admiration", "amusement",
    "anger", "annoyance",
    "approval", "caring",
    "confusion", "curiosity",
    "desire", "disappointment",
    "disapproval", "disgust",
    "embarrassment", "excitement",
    "fear", "gratitude",
    "grief", "joy",
    "love", "nervousness",
    "optimism", "pride",
    "realization", "relief",
    "remorse", "sadness",
    "surprise", "neutral"
]

def shows_most_emotion():
    emotion_dic = []

    for president in os.listdir("presidents"):
        with open(f"presidents/{president}") as f:
            speeches = json.load(f)
        
        non_neutral = 0
        total = 0
        for speech in speeches:
            total += sum(speech["emotion"].values())
            non_neutral +=  sum(speech["emotion"].values()) - speech["emotion"]["neutral"]

        emotion_dic.append({
            "president": president[:-5],
            "ratio": round(non_neutral / total, 4)
        })

    emotion_dic = sorted(emotion_dic, key=lambda item: item["ratio"], reverse=True)

    with open(f"analysis/total_emotion_ratio.json", 'w') as f:
        json.dump(emotion_dic, f, indent=4)


def most_by_emotion():
    for emotion in emotions:
        emotion_dic = []

        for president in os.listdir("presidents"):
            with open(f"presidents/{president}") as f:
                speeches = json.load(f)
            
            emotion_num = 0
            total = 0
            for speech in speeches:
                total += sum(speech["emotion"].values())
                emotion_num += speech["emotion"][emotion] if emotion in speech["emotion"] else 0

            emotion_dic.append({
                "president": president[:-5],
                "ratio": round(emotion_num / total, 4)
            })

        emotion_dic = sorted(emotion_dic, key=lambda item: item["ratio"], reverse=True)

        with open(f"analysis/most-by-emotion/{emotion}.json", 'w') as f:
            json.dump(emotion_dic, f, indent=4)


if __name__ == "__main__":
    shows_most_emotion()
    # most_by_emotion()