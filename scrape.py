from bs4 import BeautifulSoup
import requests
import time

### Script to scrape reed.co.uk for jobs ###

def getPfp(url):
    page = ''
    while page == '':
        try:
            page = requests.get(url)
            soup = BeautifulSoup(page.content, 'html.parser')

            images = soup.find_all("img")
            for i in images:
                try:
                    if "https://resources.reed.co.uk/profileimages/" in i['data-src']:
                        image = i['data-src']
                        break
                except:
                    image = "https://dl.kalii.xyz/placeholder.png"
            return(image)
        except:
            print('[Ratelimit] Pausing for 5 secconds')
            time.sleep(5)
            continue

def getDescription(url):
    page = ''
    while page == '':
        try:
            page = requests.get(url)
            soup = BeautifulSoup(page.content, 'html.parser')
            job_elements = soup.find(class_="description")
            try:
                return(str(job_elements.text.strip()))
            except:
                return('Error: Description Unavailable.')
        except:
            print('[Ratelimit] Pausing for 5 secconds')
            time.sleep(5)
            continue
    