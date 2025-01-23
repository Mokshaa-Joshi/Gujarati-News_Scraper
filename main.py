import requests
from bs4 import BeautifulSoup
import streamlit as st
from deep_translator import GoogleTranslator

def scrape_articles():
    base_url = "https://www.gujaratsamachar.com/"
    response = requests.get(base_url)
    
    if response.status_code != 200:
        st.error("Failed to retrieve the website. Please check the URL or your internet connection.")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')
    
    articles = []
    for article in soup.find_all('div', class_='news-box'):
        title = article.find('a', class_='theme-link news-title').text.strip()
        link = article.find('a', class_='theme-link')['href']
        summary = article.find('p').text.strip() if article.find('p') else ""
        
        content = scrape_article_content(link)
        
        articles.append({
            'title': title,
            'link': link,
            'summary': summary,
            'content': content
        })
    
    return articles

def scrape_article_content(link):
    try:
        if link.startswith('/'):
            base_url = "https://www.gujaratsamachar.com"
            link = base_url + link

        article_response = requests.get(link)
        if article_response.status_code != 200:
            return "Error loading article content."
        
        article_soup = BeautifulSoup(article_response.content, 'html.parser')
        
        content_div = article_soup.find('div')
        if not content_div:
            content_elements = article_soup.find_all(['p', 'h1', 'h2', 'h3', 'ul', 'ol'])
            content = ' '.join([element.get_text().strip() for element in content_elements])
        else:
            content = content_div.text.strip() if content_div else "Content not available."
        
        return content
    except Exception as e:
        return f"Error: {e}"

def translate_query(query, lang="gu"):
    if lang != "en":
        return GoogleTranslator(source='auto', target=lang).translate(query)
    return query

def search_articles(query, articles):
    return [article for article in articles if query.lower() in article['title'].lower() or query.lower() in article['summary'].lower()]

def main():
    st.title("Gujarat Samachar Article Search")
    st.write("Enter a keyword to search for relevant articles.")

    query = st.text_input("Search for articles", "")
    
    articles = scrape_articles()
    if not articles:
        st.warning("No articles found. Please try again later.")
        return
    
    if query:
        translated_query = translate_query(query, lang="gu")
        st.write(f"Searching for: {translated_query}")
        
        filtered_articles = search_articles(translated_query, articles)
        
        if filtered_articles:
            st.subheader(f"Search Results for '{translated_query}':")
            for article in filtered_articles:
                st.markdown(f"### [{article['title']}]({article['link']})")
                st.write(article['summary'])
                st.write(article['content'])
        else:
            st.warning(f"No articles found for '{translated_query}'.")
    else:
        st.info("Please enter a search term.")

if __name__ == "__main__":
    main()
