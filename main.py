import requests
from bs4 import BeautifulSoup
import sqlite3

connection = sqlite3.connect("news.base")
cursor = connection.cursor()
cursor.executescript('''
    drop table if exists news;
    create table if not exists news(
        id integer primary key autoincrement,
        category text,
        title text,
        post_date text

    );
''')
connection.commit()

url = "https://podrobno.uz/"
html = requests.get(url).text
soup = BeautifulSoup(html, "html.parser")
wrapper = soup.find('div', class_='col-md-8')
articles = wrapper.find_all('div', class_='inhype-post-details')

for article in articles:
    category = article.find('div', class_='post-categories').get_text(strip=True)
    title = article.find('h3', class_='post-title entry-title').get_text(strip=True)
    post_date = article.find('div', class_='post-date').get_text(strip=True)

    cursor.execute('''
        insert into news(category, title, post_date) values(?,?,?)
    ''', (category, title, post_date))
    connection.commit()
