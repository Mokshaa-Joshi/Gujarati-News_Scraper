import requests
from bs4 import BeautifulSoup
import streamlit as st
from datetime import datetime
import pandas as pd

# Function to scrape articles from BBC News
def fetch_articles(keyword=None):
    # BBC News URL
    url = 'https://www.bbc.com/news'
    headers = {'User-agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception("Failed to fetch BBC News page.")
    
    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')
    news_list = []

    # Extract articles
    for news in soup.find_all('div', class_='gs-c-promo'):
        headline = news.find('h3', class_='gs-c-promo-heading__title')
        date = news.find('time', class_='qa-status-date')

        if headline and date:
            news_title = headline.get_text().strip()
            news_date = date.get_text().strip()

            # Filter out irrelevant entries
            if 'bbc' not in news_title.lower():
                news_list.append({'headline': news_title, 'date': news_date})

    # Convert to DataFrame
    news_df = pd.DataFrame(news_list)

    # Filter articles based on the keyword
    if keyword:
        keyword = keyword.lower()
        news_df = news_df[news_df['headline'].str.contains(keyword, case=False, na=False)]

    return news_df

# Streamlit App
def main():
    # Set Streamlit page config
    st.set_page_config(page_title="BBC News Article Search", page_icon="📰", layout="wide")

    # App title and description
    st.title("📰 BBC News Article Search")
    st.markdown(
        """
        Welcome to the **BBC News Article Search** app!  
        Scrape the latest news headlines from BBC News and search for specific topics of interest.
        """
    )

    # Current date and time
    st.write(f"**Source:** [BBC News](https://www.bbc.com/news)  \n**Date & Time:** {datetime.now().strftime('%b %d, %Y | %I:%M %p')}")

    # Search input
    keyword = st.text_input("🔍 Enter a keyword to search for news articles:")

    # Search button
    if st.button("Search"):
        st.write("Fetching news articles...")

        try:
            # Fetch and filter articles
            articles = fetch_articles(keyword)

            if not articles.empty:
                st.success(f"Found {len(articles)} articles for '{keyword}'")
                # Display articles in Streamlit
                for _, row in articles.iterrows():
                    st.markdown(f"### {row['headline']}")
                    st.write(f"🕒 {row['date']}")
                    st.markdown("---")
            else:
                st.warning(f"No articles found for '{keyword}'. Try a different keyword.")
        except Exception as e:
            st.error(f"An error occurred: {e}")

    # Footer
    st.markdown(
        """
        ---
        Made with [Streamlit](https://streamlit.io) and [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/).
        """
    )

if __name__ == "__main__":
    main()
