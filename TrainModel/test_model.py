import gensim
from gensim import corpora
from gensim.models.ldamodel import LdaModel
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string

# Danh sách các từ cần loại bỏ
unwanted_phrases = [
    'years', 'work', 'experience', 'good', 'ability',
    'advantage', 'goal', 'university', 'minimum',
    'solid', 'level', 'high'
]
stop_words = set(stopwords.words('english'))
stop_words.update(['from', 'years', 'least', 'work', 'ability', 'good', 'university',
                   'job', 'position', 'excellent', 'strong', 'capable', 'skill', 'degree',
                   'graduate', 'year', 'responsive', 'software', 'understanding',
                   'experience', 'process', 'information', 'tool', 'equivalent',
                   'knowledge', 'monitor', 'age', 'level'
                   ])

# Hàm xử lý văn bản
def preprocess(text):
    tokens = word_tokenize(text.lower())
    tokens = [word for word in tokens if word not in string.punctuation]
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word not in stop_words]
    tokens = [word for word in tokens if word not in unwanted_phrases]  # Loại bỏ từ không mong muốn
    return tokens

# Hàm để trích xuất từ khóa
def extract_keywords(text, lda_model, dictionary, num_keywords=5):
    tokens = preprocess(text)
    bow = dictionary.doc2bow(tokens)
    topics = lda_model.get_document_topics(bow)

    keywords = set()  # Sử dụng set để loại bỏ trùng lặp
    for topic_id, topic_prob in sorted(topics, key=lambda x: -x[1])[:num_keywords]:
        top_words = lda_model.show_topic(topic_id, topn=num_keywords)
        for word, prob in top_words:
            if word not in unwanted_phrases:  # Lọc từ không mong muốn
                keywords.add(word)  # Thêm từ khóa vào set

    return list(keywords)

# Đường dẫn đến các file mô hình
lda_model_path = "C:\\Users\\PC\\Desktop\\Models\\model_lda_100.model"
id2word_path = "C:\\Users\\PC\\Desktop\\Models\\model_lda_100.model.id2word"

# Tải mô hình và từ điển
lda_model = LdaModel.load(lda_model_path)
dictionary = corpora.Dictionary.load(id2word_path)

# Đoạn văn bản cần trích xuất từ khóa
text = "- Graduated from university or higher in IT or equivalent degree.- Working experience: minimum 02 years in Database Oracle, Microsoft SQL, MySQL .- Having experience in installing and managing Hadop is an advantage.Middleware such as Weblogic, Jboss, Tomcat, IIS.- Understanding the operating model of web systems.Withstand work pressure, accept duty, monitor the system and handle incidents at any time.True according to the management process"

# Trích xuất từ khóa
keywords = extract_keywords(text, lda_model, dictionary)

print("Keywords extracted:", keywords)
