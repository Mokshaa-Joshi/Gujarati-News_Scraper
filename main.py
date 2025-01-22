import requests
from bs4 import BeautifulSoup
import streamlit as st

# Function to scrape articles from BBC News
def fetch_articles():
    url = "https://www.bbc.com/news"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception("Failed to load page")
    soup = BeautifulSoup(response.content, "html.parser")

    articles = []
    for item in soup.find_all("div", class_="gs-c-promo"):
        headline = item.find("h3").text if item.find("h3") else None
        link = item.find("a", href=True)["href"] if item.find("a", href=True) else None
        summary = item.find("p").text if item.find("p") else None
        if headline and link:
            articles.append({
                "headline": headline,
                "link": "https://www.bbc.com" + link,
                "summary": summary
            })
    return articles

# Function to search articles based on a keyword
def search_articles(articles, keyword):
    return [
        article for article in articles
        if keyword.lower() in article["headline"].lower() or 
           (article["summary"] and keyword.lower() in article["summary"].lower())
    ]

# Streamlit app
def main():
    st.set_page_config(page_title="BBC News Article Search", page_icon="📰", layout="wide")

    # App title and description
    st.title("📰 BBC News Article Search")
    st.markdown(
        """
        Welcome to the **BBC News Article Search** app!  
        Enter a keyword below to find related news articles scraped directly from the BBC News website.
        """
    )

    # Search bar
    keyword = st.text_input("🔍 Enter a keyword to search for news articles:")

    # Search button
    if st.button("Search"):
        if not keyword.strip():
            st.warning("Please enter a keyword to search.")
        else:
            with st.spinner("Fetching articles..."):
                try:
                    articles = fetch_articles()
                    filtered_articles = search_articles(articles, keyword)

                    if filtered_articles:
                        st.success(f"Found {len(filtered_articles)} articles for '{keyword}'")
                        for article in filtered_articles:
                            st.markdown(f"### [{article['headline']}]({article['link']})")
                            st.write(article['summary'] if article['summary'] else "No summary available.")
                            st.markdown("---")
                    else:
                        st.warning(f"No articles found for '{keyword}'. Try a different keyword.")
                except Exception as e:
                    st.error(f"An error occurred: {e}")

    # Footer
    st.markdown(
        """
        ---
        Made with ❤️ using [Streamlit](https://streamlit.io) and [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/).
        """
    )

if __name__ == "__main__":
    main()
