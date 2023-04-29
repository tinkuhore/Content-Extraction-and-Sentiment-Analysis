# Content-Extraction-and-Sentiment-Analysis

This project aims to automatically extract text from 100+ web pages and perform sentiment analysis on the extracted content. It uses the BeautifulSoup library for web scraping and the TextBlob library for sentiment analysis.


It generates a csv file that contain all the URLs along with the test result of sentiment analysis.



# Instructions

## 1. Package must contain following directories:
- archive (contains all required .xlsx files)
- MasterDictionary 
- StopWords


## 2. Create a new environment for the project

Using anaconda
```
conda create -p venv python==3.7 -y
```

If conda not installed
```
python3 -m venv .venv
```
To acivate the environment
```
source .venv/bin/activate
```

## 3. Install required libraries
```
pip install -r requirements.txt
```

## 4. To execute the script
```
python3 Main.py
```
