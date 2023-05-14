import argparse

import pandas as pd


topics_dict = {
    "political discussion (POD)": "POD", 
    "public health (PUH)": "PUH",
    "personal health (PEH)": "PEH",
    "vaccine effectiveness (VAE)": "VAE",
    "human rights (HUR)": "HUR",
    "other (OTH)": "OTH"
}

topics_list = [ 
    "political discussion (POD)",
    "public health (PUH)",
    "personal health (PEH)",
    "vaccine effectiveness (VAE)",
    "human rights (HUR)",
    "other (OTH)"
]

topics_abb = [
    "POD",
    "PUH",
    "PEH",
    "VAE",
    "HUR",
    "OTH"
]

sentiment_dict = {
    "negative": "NEG",
    "positive": "POS",
    "neutral": "NEU"
}

sentiment_list = [
    "negative",
    "positive",
    "neutral"
]


sentiment_abb = [
    "NEG",
    "POS",
    "NEU"
]

def annotate(input_file, output_file, start, end):
    """
    Annotate a file with a column of annotations.

    Args:
        input_file (str): path to the input file.
        output_file (str): path to the output file.

    Returns:
        None
    """
    
    print("Annotating file...")
    
    # Read the input file
    df = pd.read_csv(input_file, encoding= 'unicode_escape')
    
    df = df.astype({'text': str, 'topics': str, 'sentiment': str})
    
    print(df.dtypes)
    
    # print(df['sentiment'].value_counts())

    i = start
    while(i < len(df)):
        if i >= end:
            break
        
        print(i, "tweet:\n\"" + df.iloc[i]['text'], "\"")
        print("\n")
              
        print("topics:", df.iloc[i]['topics'], "sentiment:", df.iloc[i]['sentiment'])
        
        
        # topics 
        
        print("topics choices:")
        
        j = 1
        for topic in topics_list:
            print(j,"-", topic)
            j+=1
            
        print("\n")
            
        print("Choose topic using number and then press enter (use '0' to go back, '-' to jump to another row and '=' to skip this row. Use 's' to save.):")
        
        topic_choice = input()
        
        if topic_choice == "=":
            continue
        elif topic_choice == "-":
            print("jump to row:")
            i = int(input())
            continue
        elif topic_choice == "0":
            i -= 1
            continue
        elif topic_choice.capitalize() in topics_abb:
            print('you chose topic:', topics_abb[topic_choice])
            df.at[i,'topics'] = topic_choice.capitalize()
        elif topic_choice == "s":
            df.to_csv(output_file, index=False)
            print("saved to", output_file, "and now restarting this current row.")
            continue
        else:
            
            while(True):
                try:
                    topic_choice = int(topic_choice)
                    
                    if topic_choice in range(1, len(topics_list)+1):
                        break
                    else:
                        print("invalid choice, try again:")
                        topic_choice = input()
                except:
                    print("invalid input, try again:")
                    topic_choice = input()
                    
            topic_choice -= 1
            print('you chose topic:', topics_abb[topic_choice])
            df.at[i,'topics'] = topics_abb[topic_choice]
            
            
        
        # sentiment
        
        print("\n")
        
        print("sentiment choices:")
        
        j = 1
        for sentiment in sentiment_list:
            print(j,"-", sentiment)
            j+=1
            
        print("\n")
            
        print("Choose sentiment using number and then press enter (use '0' to go back, '-' to jump to another row and '=' to skip this row. Use 's' to save.):")
        
        sentiment_choice = input()
        
        if sentiment_choice == "=":
            continue
        elif sentiment_choice == "-":
            print("jump to row:")
            i = int(input())
            continue
        elif sentiment_choice == "0":
            i -= 1
            continue
        elif sentiment_choice.capitalize() in sentiment_abb:
            print('you chose sentiment:', sentiment_abb[sentiment_choice])
            df.at[i, 'sentiment'] = sentiment_choice.capitalize()
        elif sentiment_choice == "s":
            df.to_csv(output_file, index=False)
            print("saved to", output_file, "and now restarting this current row.")
            continue
        else:
            
            while(True):
                try:
                    sentiment_choice = int(sentiment_choice)
                    
                    if sentiment_choice in range(1, len(sentiment_list)+1):
                        break
                    else:
                        print("invalid choice, try again:")
                        sentiment_choice = input()
                except:
                    print("invalid input, try again:")
                    sentiment_choice = input()
                
            sentiment_choice -= 1
            print(i, 'you chose sentiment:', sentiment_abb[sentiment_choice])
            df.at[i,'sentiment'] = sentiment_abb[sentiment_choice]
            
            
            print("\n")
            i+=1
        


    # Write the output file
    df.to_csv(output_file, index=False)
    
    
def main():
    """
    Main function.

    Returns:
        None
    """
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Annotate a file with a column of annotations.")
    parser.add_argument("-i", "--input", default="data/thousand_tweets.csv", help="path to the input file.")
    parser.add_argument("-o", "--output", default="out.csv", help="path to the output file.")
    parser.add_argument("-s", "--start", default=0, help="path to the output file.")
    parser.add_argument("-e", "--end", default=1001, help="path to the output file.")
    args = parser.parse_args()

    print("Input file:", args.input)
    
    # Annotate the file
    annotate(args.input, args.output, int(args.start), int(args.end))
    
    
if __name__ == "__main__":
    main()