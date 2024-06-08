import pandas as pd
from googleapiclient.discovery import build
import streamlit as st
import datetime
import plotly.express as px
import mysql.connector

# db = mysqlcon.connect(host="localhost", user="root", password="Admin@123", database="youtubedata")
# MySQL connection configuration
mysql_host = "localhost"
mysql_user = "root"
mysql_password = "Admin@123"
mysql_database = "youtubedata"
mysql_port = "3306"

# Function to connect to MySQL database
def connect_to_mysql():
    try:
        conn = mysql.connector.connect(
            host=mysql_host,
            user=mysql_user,
            password=mysql_password,
            database=mysql_database,
            port=mysql_port
        )
        print("Connected to MySQL database successfully")
        return conn
    except mysql.connector.Error as e:
        print("Error connecting to MySQL database:", e)
        return None


def execute_query(query):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Admin@123",
        database="youtubedata",
        port="3306"
    )
    cursor = mydb.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    mydb.close()
    return data

st.title(":orange[Queries and their Result]")
question = st.selectbox("Select Your Question To Display The Query",
                        ("What are the names of all the videos and their corresponding channels?",
                        "Which channels have the most number of videos, and how many videos do they have?",
                        "What are the top 10 most viewed videos and their respective channels?",
                        "How many comments were made on each video, and what are their corresponding video names?",
                        "Which videos have the highest number of likes, and what are their corresponding channel names?",
                        "What is the total number of likes for each video, and what are their corresponding video names?",
                        "What is the total number of views for each channel, and what are their corresponding channel names?",
                        "What are the names of all the channels that have published videos in the year 2022?",
                        "What is the average duration of all videos in each channel, and what are their corresponding channel names?",
                        "Which videos have the highest number of comments, and what are their corresponding channel names?"),
                        )

if question == "What are the names of all the videos and their corresponding channels?":
     query = """
        SELECT c.Channel_Name, v.Title 
        FROM channel_data AS c 
        JOIN video_data AS v 
        ON c.Channel_Id = v.Channel_Id;
    """
     result = execute_query(query)
     df = pd.DataFrame(result, columns=["Channel_Name","Title"])
     st.dataframe(df,hide_index=True)

elif question == "Which channels have the most number of videos, and how many videos do they have?":
        query = """
            SELECT Channel_Name, Total_videos 
            FROM channel_data
            ORDER BY Total_videos DESC;
        """
        result = execute_query(query)
        df1 = pd.DataFrame(result, columns=["Channel_Name", "Total_videos"])
        st.dataframe(df1,hide_index=True)
        # st.write(df1)

        fig = px.bar(df1, x='Channel_Name', y='Total_videos', title='Channels with Most Videos',
                 labels={'Total_videos': 'Number of Videos', 'Channel_Name': 'Channel'})

    # Update layout
        fig.update_layout(xaxis_title='Channel', yaxis_title='Number of Videos')

        # Display the chart using Streamlit
        st.title(":blue[Visualization:]")
        st.plotly_chart(fig)

elif question == "What are the top 10 most viewed videos and their respective channels?":
        query = """
                select Channel_Name,Title,Views from video_data
                order by Views desc limit 10;
                """
        result = execute_query(query)
        df2 = pd.DataFrame(result, columns=["Channel_Name", "Title","Views"])
        st.dataframe(df2,hide_index=True)
        # st.write(df2)

        fig = px.bar(df2, x='Channel_Name', y='Views', text='Title', title='Top 10 Most Viewed Videos by Channel')
        fig.update_traces(textposition='outside')
        fig.update_layout(xaxis_title='Channel Name', yaxis_title='Views')
        # st.write("Visualization:")
        st.title(":blue[Visualization:]")
        st.plotly_chart(fig)

elif question == "How many comments were made on each video, and what are their corresponding video names?" :
        query = """
                Select c.Channel_Name, v.comments,v.Title from channel_data as c join video_data as v on c.Channel_ID=v.Channel_ID;
                """
        result = execute_query(query)
        df3 = pd.DataFrame(result, columns=["Channel_Name", "Comments","Title"])
        # st.write(df3)
        st.dataframe(df3,hide_index=True)

        fig = px.bar(df3, x='Title', y='Comments', color='Channel_Name', title='Number of Comments on Each Video')
        fig.update_layout(xaxis_title='Video Title', yaxis_title='Number of Comments', legend_title='Channel Name')
        st.title(":blue[Visualization:]")
        st.plotly_chart(fig)

elif question == "Which videos have the highest number of likes, and what are their corresponding channel names?" :
        query = """
                select c.Channel_Name,v.Title,v.Likes from channel_data as c join video_data as v on c.Channel_ID=v.Channel_ID
                order by v.Likes desc;
                """
        result = execute_query(query)
        df4 = pd.DataFrame(result, columns=["Channel_Name", "Title","Likes"])
        # st.write(df4)
        st.dataframe(df4,hide_index=True)

        fig = px.bar(df4, x='Title', y='Likes', color='Channel_Name', title='Number of Likes on Each Video')
        fig.update_layout(xaxis_title='Video Title', yaxis_title='Number of Likes', legend_title='Channel Name')
        st.title(":blue[Visualization:]")
        # st.write("Visualization:")
        st.plotly_chart(fig)

elif question == "What is the total number of likes for each video, and what are their corresponding video names?" :
        query = """
                SELECT Title, SUM(Likes) AS Total_Likes
                FROM video_data
                GROUP BY Title
                ORDER BY Total_Likes DESC;
                """
        result = execute_query(query)
        df5 = pd.DataFrame(result, columns=[ "Title","Likes"])
        # st.write(df5)
        st.dataframe(df5,hide_index=True)

        fig = px.bar(df5, x='Title', y='Likes', title='Total Number of Likes for Each Video')
        fig.update_layout(xaxis_title='Video Title', yaxis_title='Total Number of Likes')
        # st.write("Visualization:")
        st.title(":blue[Visualization:]")
        st.plotly_chart(fig)

elif question == "What is the total number of views for each channel, and what are their corresponding channel names?" :
        query = """
                select Channel_Name,views from channel_data order by views desc;
                """
        result = execute_query(query)
        df6 = pd.DataFrame(result, columns=[ "Channel_Name","views"])
        # st.write(df6)
        st.dataframe(df6,hide_index=True)

        fig = px.bar(df6, x='Channel_Name', y='views', title='Total Number of Views for Each Channel')
        fig.update_layout(xaxis_title='Channel Name', yaxis_title='Total Number of Views')
        # st.write("Visualization:")
        st.title(":blue[Visualization:]")
        st.plotly_chart(fig)

elif question == "What are the names of all the channels that have published videos in the year 2022?" :
        query = """
                select Channel_Name from video_data
                where EXTRACT(YEAR FROM Publishdate) = 2022;
                """
        result = execute_query(query)
        df7 = pd.DataFrame(result, columns=[ "Channel_Name"])
        # st.write(df7)
        st.dataframe(df7,hide_index=True)

        fig = px.histogram(df7, x='Channel_Name', title='Channels that Published Videos in 2022')
        fig.update_layout(xaxis_title='Channel Name', yaxis_title='Frequency')
        # st.write("Visualization:")
        st.title(":blue[Visualization:]")
        st.plotly_chart(fig)

elif question == "What is the average duration of all videos in each channel, and what are their corresponding channel names?" :
        query = """
                SELECT c.Channel_Name, AVG(v.Duration) AS Avg_Duration
                FROM channel_data c
                JOIN video_data v ON c.Channel_Id = v.Channel_Id
                GROUP BY c.Channel_Name;
                """
        result = execute_query(query)
        df8 = pd.DataFrame(result, columns=[ "Channel_Name","Avg_Duration"])
        # st.write(df8)
        st.dataframe(df8,hide_index=True)

        fig = px.bar(df8, x='Channel_Name', y='Avg_Duration', title='Average Duration of Videos in Each Channel')
        fig.update_layout(xaxis_title='Channel Name', yaxis_title='Average Duration')
        # st.write("Visualization:")
        st.title(":blue[Visualization:]")
        st.plotly_chart(fig)

elif question == "Which videos have the highest number of comments, and what are their corresponding channel names?" :
        query = """
                SELECT c.Channel_Name, v.Title, COUNT(co.Comment_Id) AS Num_Comments
                FROM channel_data c
                JOIN video_data v ON c.Channel_Id = v.Channel_Id
                LEFT JOIN comment_data co ON v.Video_Id = co.Video_Id
                GROUP BY c.Channel_Name, v.Title
                ORDER BY Num_Comments DESC
                LIMIT 10;
                """
        result = execute_query(query)
        df9 = pd.DataFrame(result, columns=[ "Channel_Name","Title","Num_Comments"])
        # st.write(df9)
        st.dataframe(df9,hide_index=True)

        fig = px.bar(df9, x='Title', y='Num_Comments', color='Channel_Name', title='Videos with the Highest Number of Comments')
        fig.update_layout(xaxis_title='Video Title', yaxis_title='Number of Comments', legend_title='Channel Name')
        # st.write("Visualization:")
        st.title(":blue[Visualization:]")
        st.plotly_chart(fig)