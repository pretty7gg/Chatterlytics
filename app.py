import streamlit as st
import preprocessor,helper
import matplotlib.pyplot as plt
import seaborn as sns


st.sidebar.title("Whatsapp Chat and Sentiment Analyzer")
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data=uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df=preprocessor.preprocess(data)
    # st.dataframe(df)
    user_list=df['user'].unique().tolist()
    # user_list.remove("group_notification")
    user_list.sort()
    user_list.insert(0,"Overall")
    
    selected_user = st.sidebar.selectbox("show analysis wrt",user_list)
    if st.sidebar.button("Show analysis"):
        st.markdown("<h1 style='text-align: center;'>TOP STATISTICS</h1>", unsafe_allow_html=True)
        num_messages,words,media,num_links = helper.fetch_stats(selected_user,df)
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("Total Media")
            st.title(media)
        with col4:
            st.header("Total links")
            st.title(num_links)
        
        # Daily timeline
        st.markdown("<h1 style='text-align: center;'>Daily Timeline</h1>", unsafe_allow_html=True)
        daily = helper.dailyTimeline(selected_user,df)
        fig, ax = plt.subplots()
        ax.plot(daily['only_date'],daily['message'])
        plt.xlabel("all dates")
        plt.ylabel("message per day")
        plt.xticks(rotation="vertical")
        st.pyplot(fig)
        
        # Monthly timeline
        st.markdown("<h1 style='text-align: center;'>Monthly Timeline</h1>", unsafe_allow_html=True)
        timeline = helper.monthlyTimeline(selected_user,df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'],timeline['message'])
        plt.xlabel("Month-Year")
        plt.ylabel("Message count")
        plt.xticks(rotation="vertical")
        st.pyplot(fig)
        
        # activity map
        st.markdown("<h1 style='text-align: center;'>Activity Map</h1>", unsafe_allow_html=True)
        col1,col2 = st.columns(2)
        with col1:
            st.header("Most Busy Day")
            busyDay = helper.week_activity_map(selected_user,df)
            fig, ax = plt.subplots()
            ax.bar(busyDay.index,busyDay.values)
            plt.xlabel("Days")
            plt.ylabel("Message count")
            plt.xticks(rotation="vertical")
            st.pyplot(fig)
        with col2:
            st.header("Most Busy Month")
            busyMonth = helper.month_activity_map(selected_user,df)
            fig, ax = plt.subplots()
            ax.bar(busyMonth.index,busyMonth.values)
            plt.xlabel("Month")
            plt.ylabel("Message count")
            plt.xticks(rotation="vertical")
            st.pyplot(fig)
        
        # heat map is used to tell at what time the user is most active in the whole weak
        st.markdown("<h1 style='text-align: center;'>Weekly Activity Map</h1>", unsafe_allow_html=True)
        pivot = helper.activity_heatmap(selected_user,df)
        fig, ax = plt.subplots()
        sns.heatmap(pivot)
        plt.yticks(rotation="horizontal")
        st.pyplot(fig)
        
        
        # finding the busiest user in the group(Group Level)
        if selected_user == 'Overall':
            # st.title('Most Busy Users')
            st.markdown("<h1 style='text-align: center;'>Most Busy Users</h1>", unsafe_allow_html=True)
            x , new_df = helper.most_busy_user(df)
            fig,ax = plt.subplots()
            col1,col2,col3 = st.columns(3)
            with col1:
                ax.bar(x.index,x.values,color='green')
                plt.xticks(rotation="vertical")
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)
            with col3:
                fig, ax = plt.subplots()
                ax.pie(new_df['count'], labels=new_df['percent'])
                ax.set_title('Most Busy Users')
                ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
                st.pyplot(fig)
        # wordcloud
        st.markdown("<h1 style='text-align: center;'>Word Cloud</h1>", unsafe_allow_html=True)
        df_wc = helper.create_wordcloud(selected_user,df)   
        fig,ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)
        
        # most common words
        st.markdown("<h1 style='text-align: center;'>Most Common Words</h1>", unsafe_allow_html=True)
        most_common_df = helper.most_common_words(selected_user,df)
        fig,ax=plt.subplots()
        col1,col2 = st.columns(2)
        with col1:
            st.dataframe(most_common_df)
        with col2:
            ax.bar(most_common_df['words'],most_common_df['frequency'])
            plt.xticks(rotation="vertical")
            st.pyplot(fig)
        
        #emoji
        st.markdown("<h1 style='text-align: center;'>Emoji Analysis</h1>", unsafe_allow_html=True)
        emoji_df = helper.emoji_helper(selected_user,df)
        fig,ax=plt.subplots()
        col1,col2= st.columns(2)
        with col1:
            st.dataframe(emoji_df)
        with col2:
            ax.pie(emoji_df['frequency'].head(),labels=emoji_df['emojis'].head(),autopct="%0.2f")
            st.pyplot(fig)
        
        
        