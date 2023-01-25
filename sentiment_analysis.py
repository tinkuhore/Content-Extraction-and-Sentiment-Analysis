from nltk.tokenize import word_tokenize, sent_tokenize
from textstat.textstat import textstatistics
from nltk.corpus import stopwords 
import nltk
import os
import re

nltk.download('stopwords')

class ArticleSentimentAnalysis:

    def __init__(self, articles_text_file_path:str) -> None:
        self.articles_text_file_path = articles_text_file_path
        self.stop_words_dir = os.path.join("StopWords")
        self.stop_words_file_list = os.listdir(self.stop_words_dir)
        self.master_dict_dir = os.path.join("MasterDictionary")
        self.master_dict_files_list = os.listdir(self.master_dict_dir)
        self.prepare_pos_neg_words_list()
        self.prepare_stop_words_list()
        self.prepare_article_body()
        


    def prepare_pos_neg_words_list(self):
        global pos_words_list, neg_words_list
        neg_words_list = []
        pos_words_list = []

        for txt_file in self.master_dict_files_list:
            txt_file_path = os.path.join(self.master_dict_dir,txt_file)
            
            f = open(txt_file_path,'r', encoding='utf-8', errors='replace')
            try:
                if "negative" in txt_file:
                    for i in f:
                        for x in i.replace(" | ", " ").split():
                            neg_words_list.append(x)
                else:
                    for i in f:
                        for x in i.replace(" | ", " ").split():
                            pos_words_list.append(x)
            except Exception as e:
                print(e)
        return None

    def prepare_stop_words_list(self):
        global stop_words_list
        stop_words_list = []
        for txt_file in self.stop_words_file_list:
            txt_file_path = os.path.join(self.stop_words_dir, txt_file)
            
            f = open(txt_file_path,'r', encoding='utf-8', errors='replace')
            try:
                for i in f:
                    for x in i.replace(" | ", " ").split():
                        stop_words_list.append(x)
            except Exception as e:
                print(e)
            f.close()
        return None

    def prepare_article_body(self)->str:
        global article_body
        article_body = ""
        f = open(file=self.articles_text_file_path, mode='r', encoding='utf-8', errors='replace')
        for i in f:
            article_body += i.strip()+" "
        return None
    
    def get_pos_words_list(self)->list:
        return pos_words_list

    def get_neg_words_list(self)->list:
        return neg_words_list

    def get_stop_words_list(self)->list:
        return stop_words_list

    def get_article_body(self)->str:
        return article_body

    def get_article_sentences(self)->list:
        return sent_tokenize(article_body)

    def get_article_words(self)->list:
        text = re.sub('[^a-zA-Z]', ' ', article_body)
        return word_tokenize(text)

    def remove_stop_words(self)->list:
        stop_words = set(stopwords.words('english')) 
        filtered_words_list = []
        for word in self.get_article_words():
            if word not in stop_words:
                if len(word) > 0:
                    filtered_words_list.append(word)
        return filtered_words_list

    def positive_score(self)->int:
        pos_score = 0

        for w in self.remove_stop_words():
            if w in pos_words_list:
                pos_score += 1
        return pos_score

    def negative_score(self)->int:
        neg_score = 0

        for w in self.remove_stop_words():
            if w in neg_words_list:
                neg_score += 1

        return neg_score

    def polarity_score(self)->float:
        polarity_score = round((self.positive_score()-self.negative_score())/((self.positive_score()+self.negative_score()) + 0.000001), 3)
        return polarity_score

    def subjectivity_score(self)->float:
        subjectivity_score = round((self.positive_score()+self.negative_score())/(len(self.remove_stop_words())+0.000001), 3)
        return subjectivity_score

    def get_complex_words_list(self)->list:
            complex_words_list=[]

            for word in self.get_article_words():
                if textstatistics().syllable_count(word) > 2:
                    complex_words_list.append(word)
            return complex_words_list

    def count_complex_words(self)->int:
        return len(self.get_complex_words_list())
    
    def avg_sentence_len(self)->float:
        if len(self.get_article_sentences()) == 0:
            return 0.0
        return round(len(self.get_article_words())/len(self.get_article_sentences()), 3)

    def percentage_of_complex_words(self)->float:
        if len(self.get_article_words()) == 0:
            return 0.0
        return round(self.count_complex_words()/len(self.get_article_words()), 3)

    def fog_index(self)->float:
        return round(0.4 * (self.avg_sentence_len() + self.percentage_of_complex_words()), 3)

    def avg_no_of_words_per_sentence(self)->float:
        if len(self.get_article_sentences()) == 0:
            return 0.0
        return round(len(self.get_article_words())/len(self.get_article_sentences()), 3)

    def word_count(self)->int:
        return len(self.remove_stop_words())

    def syllable_per_word(self)->int:
        if len(self.get_article_words()) == 0:
            return 0.0
        sylable_count = 0
        for word in self.get_article_words():
            sylable_count += textstatistics().syllable_count(word)

        return sylable_count/len(self.get_article_words())

    def personal_pronouns(self)->int:
        pronouns = ["I", "we", "my", "ours", "us", "We", "My", "Ours", "Us"]
        pp_count = 0

        for word in self.get_article_words():
            if word != "US":
                if word in pronouns:
                    pp_count += 1
        
        return pp_count

    def avg_word_length(self)->float:
        '''
        Formula:
        Sum of the total number of characters in each word/Total number of words
        '''
        if len(self.get_article_words()) == 0:
            return 0.0
        sum = 0
        for word in self.get_article_words():
            sum += len(word)
        
        return round(sum/ len(self.get_article_words()), 3)

