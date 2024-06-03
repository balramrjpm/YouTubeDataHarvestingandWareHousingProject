import streamlit as st
import pandas as pd
from googleapiclient.discovery import build

def main():
    st.title(":blue[YOUTUBE HARVESTING AND WAREHOUSING]")
    st.write("The YouTube Data Harvesting and Warehousing project aims to empower users by allowing them to access and analyze data from various YouTube channels. The project utilizes SQL and Streamlit to develop a user-friendly application that enables users to retrieve, save, and query YouTube channel and video data")

    st.header(":green[Channel Data Collection]:information_desk_person:")
    st.write("Using this page YouTube channel details can be fetched and insert into datatable.")
    st.header(":green[Queries and their Result]:information_desk_person:")
    st.write("This Data collection zone can collect data by using channel id  and gives all the channel details,playlist details,comment details and video details")

if __name__ == "__main__":
    main()
