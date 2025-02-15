import re
import pandas as pd
def preproocess1(data):
    pattern = '\d{1,2}/\d{1,2}/\d{2},\s\d{1,2}:\d{1,2}\s[AP]M'
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)
    df = pd.DataFrame({"user_messages": messages, 'message_data': dates})
    df['message_date'] = pd.to_datetime(df['message_data'])
    df['time'] = df['message_date'].dt.strftime("%I:%M:%S %p")
    df['message_date'] = df['message_date'].dt.date
    df.drop(columns=['message_data'], inplace=True)
    df['message_date'] = pd.to_datetime(df['message_date'])
    user = []
    messages = []
    for message in df['user_messages']:

        entry = re.split('([\w\w]+?):\s', message)
        if entry[1:]:

            user.append(entry[1])
            messages.append(entry[2])
        else:

            user.append('group_notification')
            messages.append(entry[0])
    df['user'] = user
    df['message'] = messages
    df.drop(columns=['user_messages'], inplace=True)
    df['year'] = df['message_date'].dt.year
    df['month_name'] = df['message_date'].dt.month_name()
    df['month_num'] = df['message_date'].dt.month
    df['day_name'] = df['message_date'].dt.day_name()
    return df

