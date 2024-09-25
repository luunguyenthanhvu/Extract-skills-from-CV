from flask import Flask, request, jsonify
import requests
import pdfplumber
import io
import string
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from gensim import corpora
from gensim.models.ldamodel import LdaModel

app = Flask(__name__)

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

# Khởi tạo lemmatizer
lemmatizer = WordNetLemmatizer()

# Hàm xử lý văn bản
def preprocess(text):
    tokens = word_tokenize(text.lower())
    tokens = [word for word in tokens if word not in string.punctuation]
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
            if len(word) > 3 and word not in stop_words:
                keywords.add(word)

    return list(keywords)

# Đường dẫn đến các file mô hình
lda_model_path = "C:\\Users\\PC\\Desktop\\Models\\model_lda_100.model"
id2word_path = "C:\\Users\\PC\\Desktop\\Models\\model_lda_100.model.id2word"

# Tải mô hình và từ điển
lda_model = LdaModel.load(lda_model_path)
dictionary = corpora.Dictionary.load(id2word_path)

@app.route('/extract-skills', methods=['POST'])
def extract_skills():
    # Nhận URL từ yêu cầu JSON
    data = request.json
    pdf_url = data.get('url')

    if not pdf_url:
        return jsonify({"error": "URL không hợp lệ"}), 400

    try:
        # Gửi yêu cầu tải file PDF từ URL
        response = requests.get(pdf_url)

        if response.status_code != 200:
            return jsonify({"error": f"Không thể tải file PDF, mã lỗi: {response.status_code}"}), 400

        # Đọc nội dung từ PDF
        with pdfplumber.open(io.BytesIO(response.content)) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text() + "\n"

        # Trích xuất từ khóa
        keywords = extract_keywords(text, lda_model, dictionary)

        return jsonify({"skills": keywords})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
