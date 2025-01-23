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
        link = article.find('a', class_='theme-link')['href']
        summary = article.find('p').text.strip() if article.find('p') else ""
        
        # Ensure the link is absolute (complete URL)
        if link.startswith('/'):
            link = base_url + link
        
        # Scrape full content of the article
        content = scrape_article_content(link)
        
        # Check if we have the content
        if title and link and content:
            articles.append({
                'title': title,
                'link': link,
                'summary': summary,
                'content': content  # Add content here
            })
    
    # Debugging: Check how many articles are scraped
    print(f"Scraped {len(articles)} articles.")
    return articles

# Scrape the full article content from the article page
def scrape_article_content(link):
    try:
        # Send request to the article page
        article_response = requests.get(link)
        if article_response.status_code != 200:
            return "Error loading article content."
        
        article_soup = BeautifulSoup(article_response.content, 'html.parser')
        
        # Try finding the article body in different ways if no class is available
        content_div = article_soup.find('div')  # Try targeting the first div
        if not content_div:
            # If no div found, look for paragraphs or other text-containing elements
            content_elements = article_soup.find_all(['p', 'h1', 'h2', 'h3', 'ul', 'ol'])
            content = ' '.join([element.get_text().strip() for element in content_elements])
        else:
            # If a div is found, extract its content
            content = content_div.text.strip() if content_div else "Content not available."
        
        return content
    except Exception as e:
        return f"Error: {e}"

# Search articles based on the query
def search_articles(query, articles):
    # Debugging: Check articles being filtered
    print(f"Filtering articles based on query: {query}")
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
    
    # Debugging: Check how many articles we have before filtering
    print(f"Total articles before filtering: {len(articles)}")
    
    if query:
        filtered_articles = search_articles(query, articles)
        if filtered_articles:
            st.subheader(f"Search Results for '{query}':")
            for article in filtered_articles:
                # Display the article title as a clickable link
                st.markdown(f"### <a href='{article['link']}' target='_blank'>{article['title']}</a>", unsafe_allow_html=True)
                st.write(article['summary'])
                st.write(article['content'])  # Display the full article content
        else:
            st.warning(f"No articles found for '{query}'.")
    else:
        st.info("Please enter a search term.")

if __name__ == "__main__":
    main()
