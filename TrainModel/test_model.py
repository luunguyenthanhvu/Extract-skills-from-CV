import gensim
from gensim import corpora
from gensim.models.ldamodel import LdaModel
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string
from nltk.stem import WordNetLemmatizer

# Danh sách các từ cần loại bỏ thêm
unwanted_phrases = {
    'years', 'work', 'experience', 'good', 'ability',
    'advantage', 'goal', 'university', 'minimum', 'solid', 'level', 'datum', 'use',
    'skill', 'well', 'requirement', 'english', 'application', 'technical', 'service',
    'computer_science', 'programming', 'write', 'thinking', 'basic', 'graduate', 'member',
    'eager', 'attitude', 'priority', 'issue', 'client', 'server', 'load_balance',
    'language', 'banking', 'office', 'know', 'group', 'teamwork', 'high', 'quality',
    'learn', 'candidate', 'familiar', 'function', 'development', 'project', 'problem_solve',
    'working', 'effective', 'team', 'responsibility', 'leadership', 'manage', 'writing',
    'product', 'manager', 'code', 'tool', 'infrastructure', 'build', 'include', 'cloud',
    'stakeholder', 'pattern', 'proficiency', 'independently', 'environment', 'relational',
    'digital', 'function', 'similar', 'system', 'framework', 'logical', 'container', 'database',
    'demonstrate', 'interpersonal', 'configuration', 'marketing', 'prototype', 'selenium',
    'orient', 'pressure', 'script', 'race', 'figma', 'javascript', 'error', 'candidate'
}

# Tạo tập hợp các stop words
stop_words = set(stopwords.words('english'))
stop_words.update(unwanted_phrases)

# In ra stop_words để kiểm tra các từ đã được thêm chưa
print("Stop words set:")
print(stop_words)

# Khởi tạo lemmatizer
lemmatizer = WordNetLemmatizer()

# Hàm xử lý văn bản đã cập nhật với lemmatization
def preprocess(text):
    tokens = word_tokenize(text.lower())
    tokens = [word for word in tokens if word not in string.punctuation]
    # Lọc từ stop words
    tokens = [lemmatizer.lemmatize(word) for word in tokens if word not in stop_words]
    return tokens

# Hàm để trích xuất từ khóa
def extract_keywords(text, lda_model, dictionary, num_keywords=10):
    tokens = preprocess(text)
    bow = dictionary.doc2bow(tokens)
    topics = lda_model.get_document_topics(bow)

    keywords = set()
    for topic_id, topic_prob in sorted(topics, key=lambda x: -x[1])[:num_keywords]:
        top_words = lda_model.show_topic(topic_id, topn=num_keywords)
        for word, prob in top_words:
            # Chỉ thêm từ nếu nó không thuộc stop_words và không thuộc unwanted_phrases
            if len(word) > 3 and word not in stop_words:
                keywords.add(word)

    return list(keywords)

# Đường dẫn đến các file mô hình
lda_model_path = "C:\\Users\\PC\\Desktop\\Models\\model_lda_100.model"
id2word_path = "C:\\Users\\PC\\Desktop\\Models\\model_lda_100.model.id2word"

# Tải mô hình và từ điển
lda_model = LdaModel.load(lda_model_path)
dictionary = corpora.Dictionary.load(id2word_path)

# Đoạn văn bản cần trích xuất từ khóa
text = ("Bachelor’s or master’s degree in computer science, Engineering, or a related field.Minimum of 5 years of professional backend development experience, with a demonstrated trajectory of increasing responsibility.Strong background in Golang and expert-level experience with SQL and database design (Postgres, SAP Hana).Proven leadership skills with the ability to manage, mentor, and grow a team of software engineers.Robust understanding of system design principles and a track record of delivering scalable, high-quality software.Effective communication skills, capable of liaising between technical teams and non-technical stakeholders.Experience with Kubernetes, Docker, and the implementation of CI/CD pipelines is essential.Fluency in English (4 skills), communicate directly with the foreign clientTech stack:Programming Language: GolangDatabases: PostgreSQL, SAP Hana, Containerization: Docker, KubernetesContinuous Integration/Continuous Deployment: Familiarity with CI/CD tools and pipelinesVersion Control: GitCloud Services: Experience with cloud service providers (e.g., AWS, GCP, Azure)API Design: RESTful API, GraphQL, GRPCReact and Node JS experience will be an added advantage.")

# Trích xuất từ khóa
keywords = extract_keywords(text, lda_model, dictionary)

print("Keywords extracted:")
for keyword in keywords:
    print(f"- {keyword}")
