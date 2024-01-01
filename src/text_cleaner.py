import json
import re


def clean_text() -> dict:
    uni = re.compile(r"\\u[0-9a-fA-F]{4}")

    with open('webscrape-results/speech_text_by_president.json') as f:
        speeches_by_president = json.load(f)
    
    new_dic = {

    }
    for president, speeches in speeches_by_president.items():
        new_dic[president] = []
        for speech in speeches:
            speech["title"] = speech["title"].replace(" | Miller Center", "")
            speech["title"] = ": ".join(speech["title"].split(": ")[1:]) if ":" in speech["title"] else speech["title"]

            speech_ = speech["transcript"]
            speech_ = uni.sub(lambda x: chr(int(x.group(1), 16)), speech_)
            speech_ = speech_.replace("\n", " ").replace("View Transcript", "").replace("Transcript", "")
            speech_ = re.sub(' +', ' ', speech_)

            speech["transcript"] = speech_

            new_dic[president].append(speech)
    
    return new_dic


if __name__ == "__main__":
    dic = clean_text()
    
    with open('webscrape-results/speech_text_by_president.json', 'w') as f:
        json.dump(dic, f, indent=4)
