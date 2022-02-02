import requests
from bs4 import BeautifulSoup
import os


print("This is a web scraper app, it extracts articles from websites.")
print("The current default website is https://www.nature.com/")
print("Specify below the number of pages you want to search in, and the type of the article.")
types_of_articles = ["Article", "Author Correction", "Book Review", "Career Column", "Comment", "Correspondence",
                     "Editorial", "Futures", "Nature Briefing", "Nature Index", "Nature Podcast", "News",
                     "News & Views", "News Feature", "News Round-Up", "Outlook", "Publisher Correction",
                     "Research Highlight", "Where I Work", "World View"]
print(types_of_articles)
print()
num = int(input("Enter the number of pages to search is: "))
article_type = input("Enter the type of the article: ")
parent_dir = os.getcwd()

for i in range(1, num + 1):
    url = f"https://www.nature.com/nature/articles?searchType=journalSearch&sort=PubDate&year=2020&page={i}"
    print(url)
    r = requests.get(url)
    titles = []
    articles = []
    links = []

    if r.status_code in range(200, 400):
        soup = BeautifulSoup(r.content, 'html.parser')
        articles = soup.find_all('span', {'class': 'c-meta__type'}, text=f'{article_type}')
        os.chdir(parent_dir)
        if os.path.isdir(f"./Page_{i}") is False:
            os.mkdir(f"Page_{i}")
        os.chdir(f"./Page_{i}")
        for article in articles:
            # Articles title
            title = article.find_parent('article').find('a', {'data-track-action': 'view article'}).string
            if title is not None:
                title = title.split()
            try:
                title = "_".join(title)
            except TypeError:
                pass
            punc = "!()-[]{};:'`\,<>./?@$%^&*~"
            if title is not None:
                for char in title:
                    if char in punc:
                        title = title.replace(char, "")
            titles.append(title)
            # Articles link
            link = article.find_parent('article').find('a')
            link = link.get('href')
            links.append("https://www.nature.com" + link)
            # Article Body
            article_url = "https://www.nature.com" + str(link)
            content = requests.get(article_url).content
            soup2 = BeautifulSoup(content, 'html.parser')
            article_body = soup2.find('div', attrs={'class': "c-article-body"})
            if article_body is not None:
                article_body = article_body.text.strip()
            f = open(f"{title}.txt", 'w', encoding="UTF-8")
            if article_body is not None:
                f.write(article_body)
                f.close()
        print("Saved all articles.")

    else:
        print(f"The URL returned {r.status_code}!")
