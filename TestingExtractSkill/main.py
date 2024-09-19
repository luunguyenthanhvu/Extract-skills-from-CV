import pandas as pd
import gensim

df = pd.read_json('https://raw.githubusercontent.com/selva86/datasets/master/newsgroups.json')

# Preprocessing

data = list(df['content'])

def sent_to_words(sentences):
  for sentence in sentences:
    yield(gensim.utils.simple_preprocess(str(sentence), deacc=True))

data_words = list(sent_to_words(data))
print(data_words[:2])