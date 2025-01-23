import requests
from bs4 import BeautifulSoup
import streamlit as st

# Function to scrape articles from Gujarat Samachar website
def scrape_articles(base_url, keyword):
    try:
        # Fetch the HTML content of the page
        response = requests.get(base_url)
        response.raise_for_status()  # Raise an error if the request failed
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Find all articles on the page (modify based on the website's structure)
        articles = []
        for article in soup.find_all("div", class_="article-class"):  # Adjust class name
            title = article.find("h2").get_text(strip=True)  # Extract title
            link = article.find("a")["href"]  # Extract URL
            summary = article.find("p").get_text(strip=True)  # Extract summary

            # Check if the keyword is in the title or summary
            if keyword.lower() in title.lower() or keyword.lower() in summary.lower():
                articles.append({
                    "title": title,
                    "link": base_url + link,
                    "summary": summary,
                })
        return articles
    except Exception as e:
        st.error(f"Error occurred while scraping: {e}")
        return []

# Streamlit interface
def main():
    st.title("Gujarat Samachar Article Search")
    
    # User inputs
    base_url = st.text_input("Enter the Base URL of Gujarat Samachar website:", 
                             value="https://www.gujaratsamachar.com/")
    keyword = st.text_input("Enter a keyword to search for articles:")

    if st.button("Search"):
        if base_url and keyword:
            # Scrape articles based on the keyword
            articles = scrape_articles(base_url, keyword)
            
            if articles:
                st.write(f"Found {len(articles)} articles containing the keyword '{keyword}':")
                for article in articles:
                    st.write(f"**{article['title']}**")
                    st.write(f"{article['summary']}")
                    st.write(f"[Read more]({article['link']})")
                    st.write("---")
            else:
                st.write(f"No articles found containing the keyword '{keyword}'.")
        else:
            st.warning("Please enter both the Base URL and a keyword.")

if __name__ == "__main__":
    main()
