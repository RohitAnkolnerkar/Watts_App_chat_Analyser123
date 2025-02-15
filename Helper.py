import pandas as pd
import emoji
from collections import Counter
import time
import streamlit as st

def fetch_stats(selected_user,df):
    if selected_user!='overall':
        df = df[df['user'] == selected_user]
    num_messages=df.shape[0]
    words = []
    for message in df['message']:
        words.extend(message.split())
    num_media_messages=df[df['message']=='<Media omitted>\n'].shape[0]

    links = []
    from urlextract import URLExtract
    extractor = URLExtract()

    for message in df['message']:
        links.extend(extractor.find_urls(message))
    return num_messages, len(words), num_media_messages,len(links)
def busy_user(df):
    x = df['user'].value_counts().head()
    df=round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={'index': 'name', 'count': 'percent'})

    return x,df
from wordcloud import WordCloud

def create_wordcloud(selected_user,df):
    if (selected_user!='overall'):
        df=df[df['user'] ==selected_user]
    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']
    f = open("stop_hinglish.txt", 'r')
    stop_words = f.read()
    def remove_stop_words(message):
        y=[]
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)
    temp['message']=temp['message'].apply(remove_stop_words)
    wc=WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    df_wc=wc.generate(temp['message'].str.cat(sep=" "))
    return df_wc
def most_common_words(selected_user,df):
    if (selected_user!='overall'):
        df=df[df['user'] ==selected_user]
    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']
    f = open("stop_hinglish.txt", 'r')
    stop_words = f.read()
    words = []
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)
    from collections import Counter
    x = Counter(words).most_common(20)
    most_common_words=pd.DataFrame(x)
    return most_common_words
def emoji_helper(selected_user,df):
    if (selected_user!='overall'):
        df=df[df['user'] ==selected_user]
    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])
    emoji_df=Counter(emojis).most_common(len(Counter(emojis)))
    return emoji_df

def time_helper(selected_user,df):
    if (selected_user!='overall'):
        df=df[df['user'] ==selected_user]

    time_line = df.groupby(['year', 'month_num', 'month_name']).count()['message'].reset_index()
    time = []
    for i in range(time_line.shape[0]):
        time.append(time_line['month_name'][i] + "-" + str(time_line['year'][i]))
    time_line['time'] = time
    return time_line
def daily_time_helper(selected_user,df):
    if (selected_user!='overall'):
        df=df[df['user'] ==selected_user]
    df['date'] = df['message_date'].dt.date
    daily_timeline = df.groupby(['date']).count()['message'].reset_index()
    return daily_timeline
def day_activity(selected_user,df):
    if (selected_user!='overall'):
        df=df[df['user'] ==selected_user]
    day_wise_activity=df['day_name'].value_counts().reset_index()
    return day_wise_activity
def month_activity(selected_user,df):
    if (selected_user!='overall'):
        df=df[df['user'] ==selected_user]

    return df['month_name'].value_counts()



