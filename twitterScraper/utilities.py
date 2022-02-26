import re
import json
import numpy as np
import pandas as pd
from nltk.stem.porter import *
from textblob import TextBlob
from Scweet.scweet import scrape
from .models import *
from datetime import datetime, timedelta


def clean_text(text):
    pat1 = r'@[^ ]+'
    pat2 = r'https?://[A-Za-z0-9./]+'
    pat3 = r'\'s'
    pat4 = r'\#\w+'
    pat5 = r'&amp '
    pat6 = r'[^A-Za-z\s]'
    combined_pat = r'|'.join((pat1, pat2, pat3, pat4, pat5, pat6))
    text = re.sub(combined_pat, "", text).lower()
    return text.strip()



def remove_pattern(input_txt, pattern):
    r = re.findall(pattern, input_txt)
    for i in r:
        input_txt = re.sub(i, '', input_txt)

    return input_txt


def getData(body):
    response_json = json.dumps(body)
    data = json.loads(response_json)
    return data


def return_tweet_data(keyword):
    now = datetime.now()
    today=now.strftime("%y-%m-%d")
    week_ago = now - timedelta(days=7)
    previous=week_ago.strftime("%y-%m-%d")

    data = scrape(words=[keyword], since='2021-12-1', until='2021-12-8', from_account=None, interval=1, headless=True, display_type="Top", save_images=False, lang="en",
                  resume=False, filter_replies=False, proximity=False)

    # Cleaning data
    cleaned_df = pd.DataFrame()
    cleaned_df['text'] = np.vectorize(remove_pattern)(
        data['Embedded_text'], "@[\w]*")
    cleaned_df['text'] = cleaned_df['text'].str.replace("[^a-zA-Z#]", " ")
    cleaned_df['text'] = cleaned_df['text'].apply(
        lambda x: ' '.join([w for w in x.split() if len(w) > 3]))

    # tokenization
    tokenized_tweet = cleaned_df['text'].apply(lambda x: x.split())
    stemmer = PorterStemmer()
    # Stemming
    tokenized_tweet = tokenized_tweet.apply(
        lambda x: [stemmer.stem(i) for i in x])  # stemming

    for i in range(len(tokenized_tweet)):
        tokenized_tweet[i] = ' '.join(tokenized_tweet[i])

    cleaned_df['text'] = tokenized_tweet

    # Removing hash tags
    for i in range(0, len(cleaned_df)):
        cleaned_df['text'][i] = clean_text(cleaned_df['text'][i])

    # adding polarity and subtectivity

    analysis = []
    subjectivity = []
    for i in range(0, len(cleaned_df)):
        analysis.append(TextBlob(cleaned_df['text'][i]).polarity)
        subjectivity.append(TextBlob(cleaned_df['text'][i]).subjectivity)
    cleaned_df['polarity'] = analysis
    cleaned_df['subjectivity'] = subjectivity

    # add sentiments
    polarity_sentiment = []
    for polarity in analysis:
        if polarity > 0:
            polarity_sentiment.append('Positive')
        elif polarity < 0:
            polarity_sentiment.append('Negative')
        else:
            polarity_sentiment.append('Neutral')

    # adding date
    cleaned_df['date'] = pd.to_datetime(data["Timestamp"])
    cleaned_df = cleaned_df.sort_values("date").set_index("date")

    # adding rolling mean
    cleaned_df['mean'] = cleaned_df['polarity'].expanding().mean()
    cleaned_df['rolling'] = cleaned_df['polarity'].rolling("7d").mean()

    # converting to JSON object
    cleaned_df['sentiment'] = polarity_sentiment

    # appending date
    date = []
    for i in range(0, len(data)):
        date.append(data['Timestamp'][i][:10])

    cleaned_df['date'] = date

    # appending cumulative polarity and date
    tweet_date = []
    cumulative_polarity = []
    sum_polarity = 0
    cumulative_sentiments=[]
    negative=0
    positive=0
    neutral=0

    curr_date = cleaned_df['date'][0]
    sum_polarity = cleaned_df['polarity'][0]

    for i in range(1, len(cleaned_df)):
        if curr_date == cleaned_df['date'][i]:
            sum_polarity += cleaned_df['polarity'][i] * \
                (1-cleaned_df['subjectivity'][i])
            if cleaned_df['sentiment'][i] == 'Neutral':
                neutral+=1
            elif cleaned_df['sentiment'][i] == 'Positive':
                positive+=1
            else:
                negative+=1
        else:
            tweet_date.append(curr_date)
            cumulative_polarity.append(sum_polarity)
            cumulative_sentiments.append([negative, positive, neutral])
            curr_date = cleaned_df['date'][i]
            sum_polarity = 0
            negative=0
            positive=0
            neutral=0

    JSONobject = [{
        'cumulative_polarity': cumulative_polarity,
        'date': tweet_date,
        'cumulative_sentiments':cumulative_sentiments,
        'total_negative': len(np.where(cleaned_df['sentiment'] == 'Negative')[0]),
        'total_positive': len(np.where(cleaned_df['sentiment'] == 'Positive')[0]),
        'total_neutral' : len(np.where(cleaned_df['sentiment'] == 'Neutral')[0])

    }]

    new_tweet=tweet()
    new_tweet.keyword=keyword
    new_tweet.since='2021-12-1'
    new_tweet.until='2021-12-8'
    new_tweet.keyword_data=JSONobject
    new_tweet.save()


    



