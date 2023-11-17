# import libaries
from bs4 import BeautifulSoup
from nltk import FreqDist
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from tkinter import filedialog as fd
import pysrt
import pandas as pd
import os

# extract the movie name from the file path
movie_list = []
srt_file_paths = fd.askopenfilenames(title='Open files',initialdir='~/Documents/CSS6625/training_data/')
for file_path in srt_file_paths:
    print(file_path)
    file_name = os.path.basename(file_path)
    movie_name = os.path.splitext(file_name)[0]
    movie_list.append(movie_name)
    #print(movie_name)
print(movie_list)
# Preprocessing
# open file explorer to select multiple srt files.
word_bank = ['god','help','kill','please','dead','love','sorry','beautiful','baby','father','bomb']
movie_data = []
movie_row = []
common_words = []
movie_counter = 0
cell_counter = 0


if(len(srt_file_paths) > 0):
    # Iterate over the tuple of file paths
    for file_path in srt_file_paths:
        #print(file_path)
        srt_file = pysrt.open(file_path)
        subs = srt_file
        # extract only the html tags and content from the raw srt file and print to screen.
        html_text_list = []
        html_tags_with_text = ""
        counter = 0
        srt_total_line_numebers = len(subs)
        while counter < srt_total_line_numebers:
            html_tags_with_text += subs[counter].text
            html_text_list.append(subs[counter].text)
            counter +=1
        # Put a space between each element to create a string 
        corpus_with_tags = ''.join(html_text_list)
        #print(corpus_with_tags)
        # Parse the text from in between the html tags in to memoryy
        soup = BeautifulSoup(corpus_with_tags, 'html.parser')
        corpus = soup.get_text().lower()
        #print(corpus)
        # Tokenizing the sentence into indvidual words.
        tokenize_words =  word_tokenize(corpus)
        #print(tokenize_words)
        
        #frequency_distribution = FreqDist(tokenize_words)
        # Filter out the stop words and place the filtered words into a seperate list.  
        filtered_list = []
        stop_words = set(stopwords.words("english"))
        for word in tokenize_words:
            if word.casefold() not in stop_words:
                filtered_list.append(word)
                if (word == ' kill' or word ==" Kill"):
                    print("found word {0}".format(word))
        #print(filtered_list)
        # Display the most frequent word that is contain in the list.
        frequency_distribution = FreqDist(filtered_list)
        # add movie name in the first element
        movie_row.append(movie_list[movie_counter])
        common_words = frequency_distribution.most_common(300)
        #len(common_words)
        print(len(common_words))
        missing_common_word_counter = 0
        for word in word_bank:
            #print("the common word is {0}".format(common_words))
            #for word in word_bank:
            for common_word in common_words:
                #print("the word bank is {0} and the common word is {1}".format(word,common_words))
                if (word == common_word[0]):
                    #print("found match#{0}".format(word)) 
                    cell_counter += 1
                    movie_row.append(common_word[1])
                    missing_common_word_counter = 0
                else:
                    missing_common_word_counter += 1
                    if(missing_common_word_counter == len(common_words)):
                        movie_row.append(0)
            missing_common_word_counter = 0

        print(movie_row)
        movie_data.append(movie_row)
        movie_row = []
        print(movie_counter)
        movie_counter += 1
        cell_counter = 0
        # iterate over the words to create training data 
elif(len(srt_file_paths) == 0):
   print("select a file")
movie_counter = 0
print(movie_data)

# Create Dataframe with movie_data from previous steps
df = pd.DataFrame(movie_data, columns= ['movie_name','god','help','kill','please','dead','love','sorry','beautiful','baby','father','bomb'] )
df["genre"]= ""
print(df)

# Display graphs of explatory data 

# Export dataframe to csv to for labeleing the data
#df.to_csv('/home/emalone/Documents/CSS6625/training_data/movie_training_data1.csv')

# Go through data and label the data Bold text 

# import training data
train_data = pd.read_csv('/home/emalone/Documents/CSS6625/training_data/movie_training_data.csv')
print(train_data.head)
# split the data 

# train the model 


