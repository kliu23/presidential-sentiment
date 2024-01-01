from transformers import pipeline
import json


emotion_classifier = pipeline("text-classification", model="SamLowe/roberta-base-go_emotions")
# emotion_classifier = pipeline("text-classification",model='bhadresh-savani/distilbert-xbase-uncased-emotion', return_all_scores=True)


def split_sentences(text: str) -> list:
    sentences = []
    sentence = ""
    for char in text:
        sentence += char
        if char in [".", "!", "?", ";"]:
            sentences.append(sentence)
            sentence = ""

        if len(sentence) >= 512:
            last_space = sentence.rfind(" ")
            sentences.append(sentence[:last_space])
            sentence = sentence[last_space:]
    

    return sentences


def get_emotion_result(speech: str) -> dict:
    sentences = split_sentences(speech)
    emotion_result = emotion_classifier(sentences)

    return emotion_result


def get_sorted_emotions(speech: str) -> dict:
    emotion_result = get_emotion_result(speech)
    labels = [result["label"] for result in emotion_result]

    emotion_count = dict(
        sorted(
            {label: labels.count(label) for label in labels}.items(), 
            key=lambda item: item[1], 
            reverse=True
        )
    )
    
    return emotion_count



def get_overall_emotion():
    with open('webscrape-results/speech_text_by_president.json') as f:
        speeches_by_president = json.load(f)

    for president in speeches_by_president:
        new_li = []
        print(f"Processing {president}")
        for speech in speeches_by_president[president]:
            emotions = get_sorted_emotions(speech["transcript"])
            speech["emotion"] = emotions
            new_li.append(speech)

            print(f"Finished {speech['title']}. Average emotion of {emotions}")
        
        with open(f"presidents/{president}.json", 'w') as f:
            json.dump(new_li, f, indent=4)
        
        print(f"Finished {president}\n")


if __name__ == "__main__":
    get_overall_emotion()

