
import os
import string
import requests
from bs4 import BeautifulSoup

intab = " "
outtab = "_"
trantab = str.maketrans(intab, outtab)
saved_articles = []
page_no = int(input('Enter page number: '))
requested_type = input('Enter article type: ')

# Capture the current working directory and create the new directory

for i in range(1,page_no+1):
    original_dir = os.getcwd()
    new_dir = 'Page_' + str(i)
    try:
        os.mkdir(new_dir)
    except FileExistsError:
        pass

# Get the data
    page_data = requests.get('https://www.nature.com/nature/articles?searchType=journalSearch&sort=PubDate&page=' + str(i))

# Load data into BS4
    page_soup = BeautifulSoup(page_data.text, 'html.parser')

    articles = page_soup.find_all('article')

# Iterate through the section to find only the requested articles
# Grab their title and URL, and make a filename for each article
# Grab their titles, create a filename, and save the content
    for article in articles:
        article_type = article.find('span', {'class': "c-meta__type"}).text.strip()

        if article_type == requested_type:
            title = article.find('a', {'data-track-action': "view article"}).text.strip()
            article_title = ""
            for a in title:
                if a not in string.punctuation:
                    article_title += a
                else:
                    article_title += ""

            filename = article_title.translate(trantab) + ".txt"
            link = article.find('a')
            article_url = 'https://www.nature.com' + link.get('href')

            # Look up the article and grab the contents
            article_data = requests.get(article_url)
            article_soup = BeautifulSoup(article_data.text, 'html.parser')

            # Grab the content and save it to a new text file.  If none exists, save the title to the text file


            content = article_soup.select_one(".article__body")

            if content is None:
                content = article_soup.select_one(".article-item__body")


            with open(os.path.join(new_dir, filename), 'w', encoding="UTF-8") as f:
                f.write(str(content.text.strip()))
            f.close()

            saved_articles.append(filename)

print("The following articles were saved:")
print(saved_articles)