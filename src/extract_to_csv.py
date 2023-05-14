import json
import random
import sys
import csv


def sample_json(filename, num_posts):
    file = open(filename, 'r', encoding='utf-8')
    json_list = file.readlines()
    sample_list = random.sample(json_list, int(num_posts))

    extract_list = []
    for post in sample_list:

        post_list = []
        post_dict = json.loads(post)

        posts_info = ['id', 'created_at', 'text']
        for info in posts_info:
            post_list.append(post_dict[info])

        public_metrics = ['retweet_count', 'reply_count', 'like_count', 'quote_count']
        for metric in public_metrics:
            post_list.append(post_dict['public_metrics'][metric])

        post_list.insert(2, '')
        post_list.insert(3, '')
        extract_list.append(post_list)

    file.close()
    return extract_list


def write_csv(filename, extract_list):
    header = ['id', 'created_at', 'topics', 'sentiment', 'text', 'retweet_count', 'reply_count', 'like_count', 'quote_count']
    file = open(filename, 'w', encoding='utf-8', newline='')
    writer = csv.writer(file)
    writer.writerow(header)
    writer.writerows(extract_list)


def main():

    json_file = sys.argv[1]
    output_filename = sys.argv[2]
    num_posts = sys.argv[3]

    write_csv(output_filename, sample_json(json_file, num_posts))


if __name__ == "__main__":
    main()