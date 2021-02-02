# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import os
import requests
from urllihat b.parse import urljoin
from bs4 import BeautifulSoup
class getDocuments:
    def __init__(self, url):
        # Get the html code
        page = requests.get(url)
        contents = page.content

        # Put the code in more reader friendly format
        soup = BeautifulSoup(page.text, 'html.parser')
        soup.find_all('a')

        #
        folder_location = r'/Users/peterargo/Documents/webScraper'
        if not os.path.exists(folder_location): os.mkdir(folder_location)

        for link in soup.select("a[href$='.pdf']"):
            # Name the pdf files using the last portion of each link which are unique in this case
            filename = os.path.join(folder_location, link['href'].split('/')[-1])
            with open(filename, 'wb') as f:
                f.write(requests.get(urljoin(url, link['href'])).content)

        # Print some stuff
        print(soup)
        print(f'we got data from, {url}')


def main(url):
    getDocuments(url)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main('http://www.gatsby.ucl.ac.uk/teaching/courses/ml1-2016.html')
