#
# SPDX-FileCopyrightText: © 2024 Alenka Kavčič <alenka.kavcic@fri.uni-lj.si>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#


# This script performs topic modelling with BERTopic (using sentence transformer model) on corpus Kranjska. The results are list of topics with keywords and topic analysis over time (years).
#
# Input: json files prepared by prepare_data_speeches.py and extract_lemmas.py
# Output: topics and visualisation files


from bertopic import BERTopic
from sentence_transformers import SentenceTransformer
from umap import UMAP
import json


INPUT_FILE = "../data/bert_docs_time_stamps.json" # the name of the input data file (list of document-time_stamp pairs)
INPUT_FILE_LEMMAS = "../data/word_lemmas.json" # the name of the input data file with lemmas (list of pairs (word, lemma))
OUTPUT_DIR = "../model_vis/" # the name of the directory for writing visualisation files


# read input data
with open(INPUT_FILE, 'r') as f: # list of pairs (time_stamp, speech)
     corpus = json.load(f)

with open(INPUT_FILE_LEMMAS, 'r') as f: # list of pairs (word, lemma)
     word_lemmas = json.load(f)
     keys = [w for (w,x) in word_lemmas]
     word_dict = dict(zip(keys, word_lemmas))

# prepare the data
timestamps = [x[0][:4] for x in corpus] # list of time-stamps; time-stamp is the year of the document
documents = [x[1] for x in corpus] # list of documents

# use BERTopic to extract topics (umap for dimensionality reduction with preset seed to enable repetition of results)
seed = 5194
umap_model = UMAP(n_neighbors=15, n_components=5, min_dist=0.1, metric='cosine', random_state=seed)
bert_model = BERTopic(language="multilingual", top_n_words=100, umap_model=umap_model) # embedding model: paraphrase-multilingual-MiniLM-L12-v2
topics, probs = bert_model.fit_transform(documents)

# print out the results
print("-- TOPIC INFO - TOP 50 ---------------------------------------------")
print(bert_model.get_topic_info().head(50))

print("-- TOPIC FREQ - TOP 50 ---------------------------------------------")
print(bert_model.get_topic_freq().head(50))

print("-- TOP 100 TOPICS --------------------------------------------------")
for t in range(100):
    topic = bert_model.get_topic(t)
    if topic:
        keywords_list = [x for (x,y) in topic]
        print(f"TOPIC # {t} :: {keywords_list}")
    print("--------------------------------------------------------------------")
    # postprocess a list of topic keywords - keep only lemmas of words that are in dict (with certain upos and not stopwords)
    kw_list = [word_dict[x][1] for x in keywords_list if x in word_dict.keys()]
    print(f"TOPIC # {t} - postprocessed keywords :: {kw_list}")
    print("--------------------------------------------------------------------")
    print()


# Topics over time
# the number of timestamps should be below 50 (prepare timestamps accordingly, by year)
topics_over_time = bert_model.topics_over_time(documents, timestamps)

# visualizations of top 20 topics by year
fig = bert_model.visualize_topics_over_time(topics_over_time, top_n_topics=20)
fig.write_html(OUTPUT_DIR + "over_time_by_year.html")

# visualizations of top 20 topics
fig = bert_model.visualize_barchart(top_n_topics=20)
fig.write_html(OUTPUT_DIR + "barchart.html")
fig = bert_model.visualize_topics(top_n_topics=20)
fig.write_html(OUTPUT_DIR + "topics.html")
fig = bert_model.visualize_heatmap(top_n_topics=20)
fig.write_html(OUTPUT_DIR + "heatmap.html")
