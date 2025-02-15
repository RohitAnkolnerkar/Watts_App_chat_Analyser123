import streamlit as st
import preprocess
import Helper
from  urlextract import URLExtract
import matplotlib .pyplot as plt
extractor=URLExtract()
st.sidebar.title('wattsapp chat analyser')
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    data=bytes_data.decode("utf-8")
    df=preprocess.preproocess1(data)

    #fetch unique users
    user_list=df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,"overall")
    selected_user=st.sidebar.selectbox("show analysis wrt",user_list)

    if st.sidebar.button("Show Analysis"):
        num_messages,words,num_media_messages,num_links=Helper.fetch_stats(selected_user,df)
        col1,col2,col3,col4=st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total words")
            st.title(words)
        with col3:
            st.header("Total media")
            st.title(num_media_messages)
        with col4:
            st.header("Total Links")
            st.title(num_links)
        # monthly_timeline
        time_line = Helper.time_helper(selected_user, df)
        st.title('Time Analysis')
        fig, ax = plt.subplots()
        ax.plot(time_line['time'], time_line['message'], color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # daily_timeline
        daily_timeline = Helper.daily_time_helper(selected_user, df)
        st.title('Daily Time Analysis')
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['date'], daily_timeline['message'])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
        # month_wise_activity
        monthly_timeline = Helper.month_activity(selected_user, df)
        st.title('Monthly Time Analysis')
        fig, ax = plt.subplots()
        ax.plot(monthly_timeline.index, monthly_timeline.values)
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
        # weekly activity
        st.title('weekly activity')
        day_wise_activity=Helper.day_activity(selected_user,df)
        fig, ax = plt.subplots()
        ax.bar(day_wise_activity['day_name'],day_wise_activity['count'])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
        # month_wise_activity


        # finding the busiest users in the group
        if selected_user =='overall':
            st.title('most busy user')
            x,new_df=Helper.busy_user(df)
            fig,ax=plt.subplots()

            col1,col2=st.columns(2)
            with col1:
                ax.bar(x.index,x.values)
                st.pyplot(fig)
            with col2:

                st.dataframe(new_df)
        st.title('WordCloud')
        df_wc=Helper.create_wordcloud(selected_user,df)
        fig,ax=plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)
        most_common_df=Helper.most_common_words(selected_user,df)
        st.title('most_common_words')
        fig1,ax1=plt.subplots()

        ax1.barh(most_common_df[0],most_common_df[1])
        plt.xticks(rotation='vertical')
        st.pyplot(fig1)

        emoji_df=Helper.emoji_helper(selected_user,df)
        st.dataframe(emoji_df)














