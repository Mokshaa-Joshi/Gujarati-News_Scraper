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
        
        if link.startswith('/'):
            link = base_url + link
        
        content, date, day = scrape_article_content(link)
        
        if title and link and content:
            articles.append({
                'title': title,
                'link': link,
                'summary': summary,
                'content': content,
                'date': date,
                'day': day
            })
    
    return articles

def scrape_article_content(link):
    try:
        article_response = requests.get(link)
        if article_response.status_code != 200:
            return "Error loading article content.", "", ""
        
        article_soup = BeautifulSoup(article_response.content, 'html.parser')
        
        content_div = article_soup.find('div')
        content = ""
        if content_div:
            content = content_div.text.strip()
        
        date_div = article_soup.find('span', class_='date') 
        date = date_div.text.strip() if date_div else ""
        
        day_div = article_soup.find('span', class_='day')
        day = day_div.text.strip() if day_div else ""
        
        return content, date, day
    except Exception as e:
        return f"Error: {e}", "", ""

def translate_to_gujarati(query):
    try:
        translated_query = GoogleTranslator(source='en', target='gu').translate(query)
        return translated_query
    except Exception as e:
        return f"Translation Error: {e}"

def search_articles(query, articles):
    return [article for article in articles if query.lower() in article['title'].lower() or query.lower() in article['summary'].lower()]

def main():
    st.title("Gujarat Samachar Article Search")
    st.write("Enter a keyword to search for relevant articles.")

    query = st.text_input("Search for articles", "")
    
    if query:
        translated_query = translate_to_gujarati(query)
        st.write(f"Translated query (Gujarati): {translated_query}")
    else:
        translated_query = ""

    articles = scrape_articles()
    if not articles:
        st.warning("No articles found. Please try again later.")
        return
    
    if translated_query:
        filtered_articles = search_articles(translated_query, articles)
        if filtered_articles:
            st.subheader(f"Search Results for '{query}':")
            for article in filtered_articles:
                st.markdown(f"### <a href='{article['link']}' target='_blank'>{article['title']}</a>", unsafe_allow_html=True)
                st.write(article['summary'])
                st.write(f"Date: {article['date']}")
                st.write(f"Day: {article['day']}")
                st.write(article['content'])
        else:
            st.warning(f"No articles found for '{query}'.")
    else:
        st.info("Please enter a search term.")

if __name__ == "__main__":
    main()
