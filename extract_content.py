from bs4 import BeautifulSoup
import requests
import pandas as pd
import os

def get_content_text_file_name(url):
    url_str = str(url)
    url_str=url_str.replace(":", "_").replace("/", "").replace(".", "_")
    file_name = url_str+".txt"
    return file_name

def content_to_text_file(url):
    try:
        print("Extracting content from -> ", url)
        resp = requests.get(url, headers={"User-Agent": "XY"})

        soup = BeautifulSoup(resp.content, 'html.parser')
        title = soup.find("h1", {"class":"entry-title"})
        contents = soup.find_all("div", {"class":"td-post-content"})

        # create new folder
        dir = os.path.join("extracted_articles")
        os.makedirs(dir, exist_ok=True)
        
        file_name = get_content_text_file_name(url)
        file_path = os.path.join(dir, file_name)
        
        with open(file_path, "w") as file:

            file.writelines(title.text)

            for line in contents:
                file.writelines(line.text)
            file.close()
        print("Successfully extracted all tests", '\n')
    except Exception as e:
        print("Failed to extract as no content was found.", '\n')

