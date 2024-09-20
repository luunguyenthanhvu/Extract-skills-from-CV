import pandas as pd
import gensim
import nltk
from gensim.utils import simple_preprocess

# download stop word
nltk.download('stopwords')

# Đọc dữ liệu từ file CSV
df = pd.read_csv("data.csv")

# Chuyển đổi các câu thành danh sách từ
data = df['description'].tolist()

def sent_to_words(sentences):
    for sentence in sentences:
        yield (gensim.utils.simple_preprocess(str(sentence), deacc=True))

# Chuyển đổi dữ liệu thành dạng từ
data_words = list(sent_to_words(data))

# Xây dựng bigram
bigram = gensim.models.Phrases(data_words, min_count=5, threshold=100)
bigram_mod = gensim.models.phrases.Phraser(bigram)  # Chuyển đổi thành Phraser

# Xây dựng trigram
trigram = gensim.models.Phrases(bigram[data_words], threshold=100)
trigram_mod = gensim.models.phrases.Phraser(trigram)  # Chuyển đổi thành Phraser

# Xem ví dụ trigram
# print(trigram_mod[bigram_mod[data_words[0]]])

# function for stopwords, bigrams, trigrams and lemmatization
def remove_stopwords(texts):
  return [[word for word in simple_preprocess(str)]]
