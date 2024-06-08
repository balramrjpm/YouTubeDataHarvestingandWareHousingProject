import pandas as pd
from googleapiclient.discovery import build
import streamlit as st
import datetime
import plotly.express as px
import mysql.connector

# Api connection details
# Api_Key = "AIzaSyByIzpRaLxymR44tohB9XsiYkCd_66Foa0"
Api_Key = "AIzaSyA8sFEUjjDAsWzxlJfOCko47e-TWkQMPXU"
Api_Name = "youtube"
Api_Version = "v3"

def Api_connect():
    youtube = build(Api_Name, Api_Version, developerKey=Api_Key)
    return youtube

# Function to get the channel details
def get_channel_info(youtube, channel_id):
    request = youtube.channels().list(
        part="snippet,statistics,contentDetails",
        id=channel_id
    )
    response = request.execute()

    data = []
    for i in response["items"]:
        data.append({
            "Channel_Name": i["snippet"]["title"],
            "Channel_Id": i["id"],
            "Subscribers": i["statistics"]["subscriberCount"],
            "Views": i["statistics"]["viewCount"],
            "Total_videos": i["statistics"]["videoCount"],
            "Channel_description": i["snippet"]["description"],
            "Playlist_Id": i["contentDetails"]["relatedPlaylists"]["uploads"]
        })
    return data


#Function to get the video ids
def get_video_ids(youtube, channel_id):
    video_ids = []
    response = youtube.channels().list(
        id=channel_id,
        part='contentDetails'
    ).execute()
    playlist_id = response['items'][0]['contentDetails']['relatedPlaylists']['uploads']

    next_page_token = None

    while True:
        response = youtube.playlistItems().list(
            part='snippet',
            playlistId=playlist_id,
            maxResults=50,
            pageToken=next_page_token
        ).execute()

        for item in response['items']:
            video_ids.append(item['snippet']['resourceId']['videoId'])

        next_page_token = response.get('nextPageToken')

        if not next_page_token:
            break

    return video_ids

#Function to get the Video Details
import datetime
def get_Video_Details(youtube, video_ids):
    Video_data = []

    for video_id in video_ids:
        request = youtube.videos().list(
            part="snippet,contentDetails,statistics",
            id=video_id
        )
        response = request.execute()

        for item in response["items"]:
            publish_date_str = item['snippet']['publishedAt']
            publish_date = datetime.datetime.strptime(publish_date_str, '%Y-%m-%dT%H:%M:%SZ')
            formatted_publish_date = publish_date.strftime('%Y-%m-%d %H:%M:%S')


            data = {
                'Channel_Name': item['snippet']['channelTitle'],
                'channel_Id': item['snippet']['channelId'],
                'Video_Id': item['id'],
                'Title': item['snippet']['title'],
                'Tags': item['snippet'].get('tags'),
                'Thumbnail': item['snippet']['thumbnails']['default']['url'],
                'Description': item['snippet'].get('description'),
                'Publishdate': formatted_publish_date,
                'Duration': item['contentDetails']['duration'],
                'Views': item['statistics'].get('viewCount'),
                'Likes': item['statistics'].get('likeCount'),
                'Comments': item['statistics'].get('commentCount'),
                'Favorite_count': item['statistics'].get('favoriteCount'),
                'Definition': item['contentDetails']['definition'],
                'Caption_Status': item['contentDetails']['caption']
            }
            Video_data.append(data)
    return Video_data

def get_comment_Details(youtube, video_ids):
    Comment_data = []
    try:
        for video_id in video_ids:
            request = youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                maxResults=50
            )
            response = request.execute()

            for item in response['items']:
                publish_date_str = item['snippet']['topLevelComment']['snippet']['publishedAt']
                publish_date = datetime.datetime.strptime(publish_date_str, '%Y-%m-%dT%H:%M:%SZ')
                formatted_publish_date = publish_date.strftime('%Y-%m-%d %H:%M:%S')
                data = {
                    'Comment_id': item['snippet']['topLevelComment']['id'],
                    'Video_id': item['snippet']['topLevelComment']['snippet']['videoId'],
                    'Comment_text': item['snippet']['topLevelComment']['snippet']['textDisplay'],
                    'Comment_Author': item['snippet']['topLevelComment']['snippet']['authorDisplayName'],
                    'Comment_Published':  formatted_publish_date
                }
                Comment_data.append(data)
    except Exception as e:
        print("Error retrieving comments:", e)
    return Comment_data

def get_playlist_details(youtube, channel_id):
    next_page_token = None
    All_data = []
    while True:
        request = youtube.playlists().list(
            part='snippet,contentDetails',
            channelId=channel_id,
            maxResults=50,
            pageToken=next_page_token
        )
        response = request.execute()

        for item in response['items']:
            data = {
                'Playlist_Id': item['id'],
                'Title': item['snippet']['title'],
                'Channel_Id': item['snippet']['channelId'],
                'Channel_Name': item['snippet']['channelTitle'],
                'PublishedAt': item['snippet']['publishedAt'],
                'Video_count': item['contentDetails']['itemCount']
            }
            All_data.append(data)

        next_page_token = response.get('nextPageToken')
        if not next_page_token:
            break

    return All_data

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

# Function to create tables in MySQL
def create_tables(conn):
    cursor = conn.cursor()

    # Table creation queries
    channel_table_query = """
    CREATE TABLE IF NOT EXISTS channel_data (
        Channel_Name VARCHAR(255),
        Channel_Id VARCHAR(255) NOT NULL,
        Subscribers INT,
        Views INT,
        Total_videos INT,
        Channel_description TEXT,
        Playlist_Id VARCHAR(255),
        PRIMARY KEY(Channel_Id)
    )
    """
    video_table_query = """
    CREATE TABLE IF NOT EXISTS video_data (
        Channel_Name VARCHAR(255),
        Channel_Id VARCHAR(255),
        Video_Id VARCHAR(255),
        Title VARCHAR(255),
        Tags TEXT,
        Thumbnail TEXT,
        Description TEXT,
        Publishdate DATETIME,
        Duration VARCHAR(255),
        Views INT,
        Likes INT,
        Comments INT,
        Favorite_count INT,
        Definition VARCHAR(255),
        Caption_Status VARCHAR(255),
        PRIMARY KEY(Video_Id)
    )
    """
    comment_table_query = """
    CREATE TABLE IF NOT EXISTS comment_data (
        Comment_id VARCHAR(255),
        Video_id VARCHAR(255),
        Comment_text TEXT,
        Comment_Author VARCHAR(255),
        Comment_Published DATETIME,
        PRIMARY KEY (Comment_id)
    )
    """
    playlist_table_query = """
    CREATE TABLE IF NOT EXISTS playlist_data (
        Playlist_Id VARCHAR(255),
        Title VARCHAR(255),
        Channel_Id VARCHAR(255),
        Channel_Name VARCHAR(255),
        PublishedAt DATETIME,
        Video_count INT
    )
    """

    try:
        # Execute table creation queries
        cursor.execute(channel_table_query)
        cursor.execute(video_table_query)
        cursor.execute(comment_table_query)
        cursor.execute(playlist_table_query)

        conn.commit()
        print("Tables created successfully in MySQL")
    except mysql.connector.Error as e:
        print("Error creating tables in MySQL:", e)
        conn.rollback()
    finally:
        cursor.close()

# Test the functions
conn = connect_to_mysql()
if conn is not None:
    create_tables(conn)
    conn.close()

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Admin@123",
    database="youtubedata",
    port="3306"
)


# Function to insert channel details into MySQL database
def insert_channel_info_to_mysql(conn, channel_info):
    cursor = conn.cursor()
    try:
        for info in channel_info:
            
            insert_query = """
            INSERT INTO channel_data (Channel_Name, Channel_Id, Subscribers, Views, Total_videos, Channel_description, Playlist_Id) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            # Execute the query with data from the channel_info list
            cursor.execute(insert_query, (info["Channel_Name"], info["Channel_Id"], info["Subscribers"], info["Views"], info["Total_videos"], info["Channel_description"], info["Playlist_Id"]))
        
        conn.commit()
        return "Success"
    except mysql.connector.Error as e:
        return "Duplicate"
        conn.rollback()
    finally:
        cursor.close()


# Function to insert video data into MySQL database
def insert_video_data_to_mysql(conn, video_data):
    cursor = conn.cursor()
    try:
        for data in video_data:
            tags = data.get('Tags', [])
            if not isinstance(tags, list):
                tags = [tags]  
            tags = [tag for tag in tags if tag is not None]
            insert_query = """
            INSERT INTO Video_data (Channel_Name, Channel_Id, Video_Id, Title, Tags, Thumbnail, Description, Publishdate, Duration, Views, Likes, Comments, Favorite_count, Definition, Caption_Status) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            # Execute the query with data from the video_data list
            cursor.execute(insert_query, (
                data['Channel_Name'],
                data['channel_Id'],
                data['Video_Id'],
                data['Title'],
                ",".join(tags),  
                data['Thumbnail'],
                data.get('Description', ''),
                data['Publishdate'],
                data['Duration'],
                data['Views'],
                data.get('Likes', 0),  
                data.get('Comments', 0),  
                data.get('Favorite_count', 0),  
                data['Definition'],
                data['Caption_Status']
            ))
        
        # Commit the changes to the database
        conn.commit()
        print("Video data inserted into MySQL successfully!")
    except mysql.connector.Error as e:
        print("Error inserting video data into MySQL:", e)
        conn.rollback()
    finally:
        cursor.close()


# Function to insert comment data into MySQL database
def insert_comment_data_to_mysql(conn, comment_data):
    cursor = conn.cursor()
    try:
        for data in comment_data:
            insert_query = """
            INSERT INTO comment_data (Comment_id, Video_id, Comment_text, Comment_Author, Comment_Published) 
            VALUES (%s, %s, %s, %s, %s)
            """
            # Execute the query with data from the comment_data list
            cursor.execute(insert_query, (
                data['Comment_id'],
                data['Video_id'],
                data['Comment_text'],
                data['Comment_Author'],
                data['Comment_Published']
            ))
        
        # Commit the changes to the database
        conn.commit()
        print("Comment data inserted into MySQL successfully!")
    except mysql.connector.Error as e:
        print("Error inserting comment data into MySQL:", e)
        conn.rollback()
    finally:
        cursor.close()

# Function to insert playlist data into MySQL database
def insert_playlist_data_to_mysql(conn, playlist_data):
    cursor = conn.cursor()
    try:
        for data in playlist_data:
            insert_query = """
            INSERT INTO playlist_data (Playlist_Id, Title, Channel_Id, Channel_Name, PublishedAt, Video_count) 
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            print(data['PublishedAt'].replace("T", " ").replace("Z", " "))
            # Execute the query with data from the playlist_data list
            cursor.execute(insert_query, (
                data['Playlist_Id'],
                data['Title'],
                data['Channel_Id'],
                data['Channel_Name'],
                data['PublishedAt'].replace("T", " ").replace("Z", " "),
                # format(data['PublishedAt'],"yyyy-mm-dd-hh-mm"),
                data['Video_count']
            ))
        
        # Commit the changes to the database
        conn.commit()
        print("Playlist data inserted into MySQL successfully!")
    except mysql.connector.Error as e:
        print("Error inserting playlist data into MySQL:", e)
        conn.rollback()
    finally:
        cursor.close()

st.title(":blue[Channel Data Collection]")
st.write("This Data collection zone can collect data by using channel id  and gives all the channel details,playlist details,comment details and video details")
                    
youtube = Api_connect()

channel_id_input_placeholder = 'channel_id_input'
channel_id = st.text_input('Enter the Channel ID', key=channel_id_input_placeholder)

if len(channel_id)>0:
    
    if st.button("Upload Data"):
        # Retrieving data from YouTube API
        playlist_data = get_playlist_details(youtube, channel_id)
        Video_data = get_video_ids(youtube,channel_id)
        comment_data = get_comment_Details(youtube, Video_data)
        video2 = get_Video_Details(youtube,Video_data)
        channel_data = get_channel_info(youtube, channel_id)
        
        # get_channel_info

        # '''
        # "Channel_Name": i["snippet"]["title"],
        # "Channel_Id": i["id"],
        # "Subscribers": i["statistics"]["subscriberCount"],
        # "Views": i["statistics"]["viewCount"],
        # "Total_videos": i["statistics"]["videoCount"],
        # "Channel_description": i["snippet"]["description"],
        # "Playlist_Id": i["contentDetails"]["relatedPlaylists"]["uploads"]
        # '''
        # Establishing connection to MySQL database
        conn = connect_to_mysql()

        # Creating tables if they don't exist
        if conn is not None:
            create_tables(conn)

            # Inserting data into MySQL tables
            result = insert_channel_info_to_mysql(conn, channel_data)
            if result == "Success":
                insert_video_data_to_mysql(conn, video2)
                insert_comment_data_to_mysql(conn, comment_data)
                insert_playlist_data_to_mysql(conn, playlist_data)
                st.write("Data migrated to MySQL successfully!")
            else:
                st.write("Duplicate Data")

            # Closing the MySQL connection
            conn.close()

            # Displaying success message
            

# def execute_query(query):
#     mydb = mysql.connector.connect(
#         host="localhost",
#         user="root",
#         password="Admin@123",
#         database="youtubedata",
#         port="3306"
#     )

# def duplicate_Channel(channel_id):
#     conn = execute_query("SELECT * FROM channel_data WHERE Channel_Id = %s", channel_id)


