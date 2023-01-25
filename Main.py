import time
import os
import pandas as pd
from sentiment_analysis import ArticleSentimentAnalysis
from extract_content import content_to_text_file, get_content_text_file_name

# import all urls as df
url_df=pd.read_excel("archive/Input.xlsx")

# extract contents and store as .txt files
for url in url_df.URL:  
    content_to_text_file(url)

# create output df
output_df = pd.DataFrame(columns=["URL_ID",	"URL",	"POSITIVE SCORE", "NEGATIVE SCORE",	"POLARITY SCORE",
        	                    "SUBJECTIVITY SCORE",	"AVG SENTENCE LENGTH",	"PERCENTAGE OF COMPLEX WORDS",	"FOG INDEX",
                                "AVG NUMBER OF WORDS PER SENTENCE",	"COMPLEX WORD COUNT",	"WORD COUNT",	"SYLLABLE PER WORD",
                                "PERSONAL PRONOUNS",	"AVG WORD LENGTH"])

print("Preparing output dataframe...")
for id, url in zip(url_df.URL_ID, url_df.URL):

    file_name = get_content_text_file_name(url)
    file_path = os.path.join("extracted_articles", file_name)
    sentiment = ArticleSentimentAnalysis(articles_text_file_path=file_path)
    
    output_row = [id, url, sentiment.positive_score(), sentiment.negative_score(), sentiment.polarity_score(), sentiment.subjectivity_score(),
                sentiment.avg_sentence_len(), sentiment.percentage_of_complex_words(), sentiment.fog_index(), sentiment.avg_no_of_words_per_sentence(),
                sentiment.count_complex_words(), sentiment.word_count(), sentiment.syllable_per_word(), sentiment.personal_pronouns(),sentiment.avg_word_length()]

    output_df.loc[len(output_df.index)] = output_row

print("Saving sentimant Analysis result as .csv file")
output_df.to_csv("sentiment_analysis_output.csv")
print('\n',"Mission Accomplished")

# -------------------'''END OF CODE'''--------------------------------