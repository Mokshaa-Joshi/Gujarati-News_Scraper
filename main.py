import requests
from bs4 import BeautifulSoup
import streamlit as st
from deep_translator import GoogleTranslator

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
    for article in soup.find_all('div', class_='news-box'):  # Adjust this selector as needed
        title = article.find('a', class_='theme-link news-title').text.strip()
        link = article.find('a', class_='theme-link')['href']
        summary = article.find('p').text.strip() if article.find('p') else ""
        
        articles.append({
            'title': title,
            'link': link,
            'summary': summary
        })
    
    print(f"Scraped Articles: {len(articles)}")  # Print the number of articles scraped
    return articles

# Translate query if it's in English
def translate_query(query, lang="gu"):
    if lang != "en":
        return GoogleTranslator(source='auto', target=lang).translate(query)
    return query

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
        translated_query = translate_query(query, lang="gu")  # Translate to Gujarati if needed
        st.write(f"Searching for: {translated_query}")
        
        filtered_articles = search_articles(translated_query, articles)
        print(f"Filtered Articles: {len(filtered_articles)}")  # Print the number of articles after filtering
        
        if filtered_articles:
            st.subheader(f"Search Results for '{translated_query}':")
            for article in filtered_articles:
                st.markdown(f"### [{article['title']}]({article['link']})")
                st.write(article['summary'])
        else:
            st.warning(f"No articles found for '{translated_query}'.")
    else:
        st.info("Please enter a search term.")

if __name__ == "__main__":
    main()
