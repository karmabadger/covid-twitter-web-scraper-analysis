import sys
import json
import math
from collections import Counter
import pandas as pd


def remove_punctuations(text):
    punctuations = ["(", ")", "[", "]", ",", "-", ".", "?", "!", ":", ";", "#", "&"]
    new_text = ""
    for char in text:
        if char in punctuations:
            new_text += " "
        else:
            new_text += char
    return new_text


def remove_non_alphanumeric(words_list):
    new_list = []
    for word in words_list:
        if word.isalpha():
            new_list.append(word)
    return new_list


def get_stopwords(filename):
    file = open(filename, 'r')
    lines = file.readlines()
    file.close()
    stopwords = set()
    for line in lines:
        if "#" in line:
            continue
        else:
            word = line.replace("\n", "")
            stopwords.add(word)
    return stopwords


def remove_stopwords(words_list, stopwords_list):
    new_list = []
    for word in words_list:
        if word in stopwords_list:
            continue
        else:
            new_list.append(word)
    return new_list


def get_topics_count(csv_file, stopwords_file):

    stopwords = get_stopwords(stopwords_file)
    df = pd.read_csv(csv_file, encoding='unicode_escape')
    df = df.dropna()
    df = df[['text', 'topics']]
    df['text'] = df['text'].str.lower()

    topics_dict = {}
    new_topics_dict = {}
    total_words = {}
    for text, coding in df.values.tolist():
        removed_pun_text = remove_punctuations(text)
        words_list = removed_pun_text.split()
        removed_non_alpha_list = remove_non_alphanumeric(words_list)
        removed_stopwords_list = remove_stopwords(removed_non_alpha_list, stopwords)

        if coding not in topics_dict:
            topics_dict[coding] = {}
        word_count_dict = topics_dict[coding]

        for word in removed_stopwords_list:
            if word in word_count_dict:
                word_count_dict[word] += 1
            else:
                word_count_dict[word] = 1

            if word in total_words:
                total_words[word] += 1
            else:
                total_words[word] = 1

    for topic in topics_dict.keys():
        for key, value in topics_dict[topic].items():
            if total_words[key] >= 5:
                if topic not in new_topics_dict:
                    new_topics_dict[topic] = {}
                new_topics_dict[topic][key] = value

    return new_topics_dict


def get_word_count(word, topic, topics_dict):
    topic_dict = topics_dict[topic]
    word_count = topic_dict[word]
    return word_count


def get_topics_total(topics_dict):
    return len(topics_dict)


def get_topics_word_count(word, topics_dict):
    total_count = 0
    for topic_dict in topics_dict.values():
        if word in topic_dict:
            total_count += 1
    return total_count


def tfidf_scorer(word, topic, topics_dict):
    tf = get_word_count(word, topic, topics_dict)
    idf = math.log10(get_topics_total(topics_dict) / get_topics_word_count(word, topics_dict))
    tfidf = tf * idf
    return tfidf


def get_topics_score(topics_dict, num_words):
    new_dict = {}
    for topic, count_dict in topics_dict.items():
        new_dict[topic] = {}
        for word in count_dict.keys():
            score = tfidf_scorer(word, topic, topics_dict)
            new_dict[topic][word] = score

    sorted_dict = {}
    for topic, count_dict in new_dict.items():
        sorted_list = Counter(count_dict).most_common(num_words)
        sorted_words = []
        for tp in sorted_list:
            word = tp[0]
            sorted_words.append(word)
        sorted_dict[topic] = sorted_words

    return sorted_dict


def main():

    csv_file = sys.argv[1]
    num_words = sys.argv[2]

    topics_count = get_topics_count(csv_file, '../data/stopwords.txt')
    count_dict = get_topics_score(topics_count, int(num_words))
    print(json.dumps(count_dict, indent=1))


if __name__ == "__main__":
    main()