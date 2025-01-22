import streamlit as st
from bs4 import BeautifulSoup
import requests

st.set_page_config(
    page_title="News Scraper",
    page_icon="🌐"
)

st.markdown(
    """
<h1 style='text-align:center'>News Scraper</h1>
""",
    unsafe_allow_html=True,
)
st.write("##")

#st.image("news_img.png", use_column_width="auto")
st.write("##")

st.write("## Select the Date: ")
st.write("##")

year, month, day = st.columns(3)
year_select = year.selectbox("Select year:", options=["2025", "2024", "2023", "2022"])
month_select = month.selectbox(
    "Select month:",
    options=[
        "january",
        "february",
        "march",
        "april",
        "may",
        "june",
        "july",
        "august",
        "september",
        "october",
        "november",
        "december",
    ],
)
day_select = day.selectbox("Select day: ", options=[str(i).zfill(2) for i in range(1, 32)])
st.write("##")
toggle_btn = st.toggle("Hindi")
st.write("##")

Scrap_btn = st.button("Scrap")

st.write("##")
str_date = str(day_select)
if str_date[-1] == "1" and str_date != "11":
    st.write(f"### News for the date {day_select}st {month_select}, {year_select}")
elif str_date[-1] == "2" and str_date != "12":
    st.write(f"### News for the date {day_select}nd {month_select}, {year_select}")
elif str_date[-1] == "3" and str_date != "13":
    st.write(f"### News for the date {day_select}rd {month_select}, {year_select}")
else:
    st.write(f"### News for the date {day_select}th {month_select}, {year_select}")

box_style = """
    <style>
        .custom-box {
            padding: 10px;
            border: 2px solid white;
            border-radius: 10px;
            background-color: black;
            color: white;
            margin-bottom: 10px;
        }
        .custom-box a {
            color: #00FFFF !important;
            text-decoration: none !important;
            font-weight: bold !important;
        }
    </style>
"""

count = 1
if Scrap_btn:
    base_url = "https://www.gujaratsamachar.com/"
    req = requests.get(base_url)
    if req.status_code == 200:
        soup = BeautifulSoup(req.text, "html.parser")
        # Find news articles
        news_list = soup.find_all("div", class_="big-news-box")
        for news_item in news_list:
            a_tag = news_item.find("a")
            if a_tag:
                news_title = a_tag.get_text(strip=True)
                href_link = base_url + a_tag["href"]
                st.markdown(box_style, unsafe_allow_html=True)
                st.markdown(
                    f"""<div class="custom-box">{count}- <a href="{href_link}" target="_blank">{news_title}</a></div>""",
                    unsafe_allow_html=True,
                )
                count += 1
    else:
        st.error("Unable to fetch data. Please try again later.")
