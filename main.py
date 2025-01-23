# Import required libraries
import requests
from bs4 import BeautifulSoup
import streamlit as st

# Scrape articles from Gujarat Samachar website
def scrape_articles():
    base_url = "https://www.gujaratsamachar.com/"
    response = requests.get(base_url)
    
    if response.status_code != 200:
        st.error("Failed to retrieve the website. Please check the URL or your internet connection.")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Modify the selectors below to match the Gujarat Samachar website's structure
    articles = []
    for article in soup.find_all('div', class_='news-box'):  # Example: Update the class to match the actual site
        title = article.find('a', class_='theme-link news-title').text.strip()
        link = article.find('a')['href']
        summary = article.find('p').text.strip() if article.find('p') else ""
        
        articles.append({
            'title': title,
            'link': link,
            'summary': summary
        })
    
    return articles

# Search articles based on the query
def search_articles(query, articles):
    return [article for article in articles if query.lower() in article['title'].lower() or query.lower() in article['summary'].lower()]

# Streamlit interface
def main():
    st.title("Gujarat Samachar Article Search")
    st.write("Enter a keyword to search for relevant articles.")

    # Input field for the search query
    query = st.text_input("Search for articles", "")
    
    # Scrape articles and search
    articles = scrape_articles()
    if not articles:
        st.warning("No articles found. Please try again later.")
        return
    
    if query:
        filtered_articles = search_articles(query, articles)
        if filtered_articles:
            st.subheader(f"Search Results for '{query}':")
            for article in filtered_articles:
                st.markdown(f"### [{article['title']}]({article['link']})")
                st.write(article['summary'])
        else:
            st.warning(f"No articles found for '{query}'.")
    else:
        st.info("Please enter a search term.")

if __name__ == "__main__":
    main()
