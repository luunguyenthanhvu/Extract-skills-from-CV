# Tất cả các import được đặt ở đầu file
import nltk
from nltk.corpus import stopwords
from gensim.utils import simple_preprocess
from gensim.models import Phrases
from gensim.models.phrases import Phraser
import gensim
import pandas as pd
import spacy
import gensim.corpora as corpora
from gensim.models.ldamodel import LdaModel
from gensim.models.coherencemodel import CoherenceModel
import re
import matplotlib.pyplot as plt
import pyLDAvis.gensim_models
import pyLDAvis

# Các lệnh tải xuống cần thiết
nltk.download('stopwords')
nltk.download('punkt')

# Load mô hình spaCy một lần
spacy_nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner'])

# Định nghĩa stop words
stop_words = set(stopwords.words('english'))
stop_words.update(['from', 'years', 'least', 'work', 'ability', 'good', 'university',
                   'job', 'position', 'excellent', 'strong', 'capable', 'skill', 'degree',
                   'graduate', 'year', 'responsive', 'software', 'understanding',
                   'experience', 'process', 'information', 'tool', 'equivalent',
                   'knowledge', 'monitor', 'age', 'level'
                   ])



# Hàm xử lý văn bản
def preprocess(text):

  tokens = simple_preprocess(text.lower(), deacc=True)
  tokens = [word for word in tokens if word not in stop_words]
  return tokens


# Hàm để trích xuất chủ đề và từ khóa
def extract_topic(text, lda_model, dictionary, num_keywords=10):
  tokens = preprocess(text)
  bow = dictionary.doc2bow(tokens)
  topics = lda_model.get_document_topics(bow)

  if not topics:
    return "No topics found for the given text."

  dominant_topic, prob = max(topics, key=lambda x: x[1])
  topic_keywords = lda_model.show_topic(dominant_topic, topn=num_keywords)
  topic_description = f"Topic {dominant_topic}: " + " + ".join(
      [f"{round(weight, 3)}*\"{word}\"" for word, weight in topic_keywords])

  return topic_description


# Đọc dữ liệu từ file CSV
df = pd.read_csv("data.csv")

# Chuyển đổi các câu thành danh sách từ
data = df['description'].tolist()


def sent_to_words(sentences):
  for sentence in sentences:
    yield simple_preprocess(str(sentence), deacc=True)


# Chuyển đổi dữ liệu thành dạng từ
data_words = list(sent_to_words(data))

# Xây dựng bigram và trigram models
bigram = Phrases(data_words, min_count=5, threshold=100)
bigram_mod = Phraser(bigram)
trigram = Phrases(bigram[data_words], threshold=100)
trigram_mod = Phraser(trigram)


# Function để loại bỏ stopwords
def remove_stopwords(texts):
  return [[word for word in gensim.utils.simple_preprocess(str(doc)) if
           word not in stop_words] for doc in texts]


def make_bigrams(texts):
  return [bigram_mod[doc] for doc in texts]


def make_trigrams(texts):
  return [trigram_mod[bigram_mod[doc]] for doc in texts]


# Lemmatization
def lemmatization(texts, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV']):
  texts_out = []
  for sent in texts:
    doc = spacy_nlp(" ".join(sent))
    texts_out.append(
        [token.lemma_ for token in doc if token.pos_ in allowed_postags])
  return texts_out


# Remove Stop Words
data_words_nostops = remove_stopwords(data_words)

# Form Bigrams
data_words_bigrams = make_bigrams(data_words_nostops)

# Do lemmatization
data_lemmatized = lemmatization(data_words_bigrams,
                                allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV'])

# Create Dictionary and Corpus
id2word = corpora.Dictionary(data_lemmatized)
texts = data_lemmatized

# Term Document Frequency
corpus = [id2word.doc2bow(text) for text in texts]

# Build LDA model (num_topics=100 là ví dụ, bạn có thể thay đổi sau khi tìm số lượng tối ưu)
num_topics = 100
lda_model = LdaModel(
    corpus=corpus,
    id2word=id2word,
    num_topics=num_topics,
    random_state=100,
    update_every=1,
    chunksize=100,
    passes=5,
    alpha='auto',
    per_word_topics=True
)

# Lưu mô hình và từ điển
lda_model.save("C:\\Users\\PC\\Desktop\\Models\\model_lda_100.model")
id2word.save("C:\\Users\\PC\\Desktop\\Models\\model_lda_100.model.id2word")
corpora.MmCorpus.serialize(
  "C:\\Users\\PC\\Desktop\\Models\\model_lda_100.model.corpus", corpus)


# Hàm format_topics_sentences
# Hàm format_topics_sentences
def format_topics_sentences(ldamodel, corpus, texts):
    sent_topics = []

    for i, row in enumerate(ldamodel[corpus]):
        row = sorted(row[0], key=lambda x: (x[1]), reverse=True)
        for j, (topic_num, prop_topic) in enumerate(row):
            if j == 0:  # Dominant topic
                wp = ldamodel.show_topic(topic_num)
                topic_keywords = ", ".join([word for word, prop in wp])
                sent_topics.append([int(topic_num), round(prop_topic, 4), topic_keywords])
            else:
                break

    # Chuyển danh sách thành DataFrame
    sent_topics_df = pd.DataFrame(sent_topics, columns=['Dominant_Topic', 'Perc_Contribution', 'Topic_Keywords'])

    # Thêm văn bản gốc vào DataFrame
    contents = pd.Series(texts)
    sent_topics_df['Text'] = contents

    return sent_topics_df




# Gọi hàm format_topics_sentences
df_topic_sents_keywords = format_topics_sentences(ldamodel=lda_model,
                                                  corpus=corpus, texts=data)

# Format DataFrame
df_dominant_topic = df_topic_sents_keywords.reset_index()

# Hiển thị kết quả
print(df_dominant_topic.head(10))
