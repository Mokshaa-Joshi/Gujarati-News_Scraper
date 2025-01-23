import requests
from bs4 import BeautifulSoup
import streamlit as st

# Function to scrape articles from Gujarat Samachar
def fetch_articles():
    url = "https://www.gujaratsamachar.com/"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception("Failed to load page")
    
    soup = BeautifulSoup(response.content, "html.parser")
    articles = []

    # Scraping article blocks (adjusting to Gujarat Samachar structure)
    for item in soup.find_all("div", class_="listing-text"):
        headline = item.find("h3")
        link = item.find("a", href=True)
        summary = item.find("p")

        if headline and link:
            articles.append({
                "headline": headline.text.strip(),
                "link": link["href"].strip(),
                "summary": summary.text.strip() if summary else "No summary available"
            })
    return articles

# Function to search articles based on a keyword
def search_articles(articles, keyword):
    keyword = keyword.lower()  # Case-insensitive search
    return [
        article for article in articles
        if keyword in article["headline"].lower() or keyword in article["summary"].lower()
    ]

# Streamlit app
def main():
    st.set_page_config(page_title="Gujarat Samachar News Search", page_icon="📰", layout="wide")

    # App title and description
    st.title("📰 Gujarat Samachar News Search")
    st.markdown(
        """
        Welcome to the **Gujarat Samachar News Search** app!  
        Enter a keyword below to find related news articles scraped directly from the Gujarat Samachar website.
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
