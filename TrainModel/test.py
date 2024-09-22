# Tải mô hình và từ điển đã lưu
from gensim import corpora
from gensim.models import LdaModel, CoherenceModel
import spacy

from main import data_words_bigrams

nlp = spacy.load('en_core_web_sm')
def lemmatization(texts, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV']):
  """https://spacy.io/api/annotation"""
  texts_out = []
  for sent in texts:
    doc = nlp(" ".join(sent))
    texts_out.append(
        [token.lemma_ for token in doc if token.pos_ in allowed_postags])
  return texts_out
data_lemmatized = lemmatization(data_words_bigrams, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV'])

lda_model = LdaModel.load("C:\\Users\\PC\\Desktop\\Models\\model_lda_100.model")
id2word = corpora.Dictionary.load("C:\\Users\\PC\\Desktop\\Models\\model_lda_100.model.id2word")
corpus = corpora.MmCorpus("C:\\Users\\PC\\Desktop\\Models\\model_lda_100.model.corpus")

# Xem các chủ đề đã học được
for idx, topic in lda_model.print_topics(-1):
    print(f"Topic {idx}: {topic}")

