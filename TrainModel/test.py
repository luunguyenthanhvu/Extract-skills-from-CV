import unittest
import spacy
from spacy.matcher import PhraseMatcher

# Danh sách kỹ năng đã cập nhật
skills_list = ['oracle', 'sql', 'mysql', 'weblogic', 'jboss', 'tomcat', 'iis',
               'hadoop', 'java', 'python', 'docker']
spacy_nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner'])
matcher = PhraseMatcher(spacy_nlp.vocab)
patterns = [spacy_nlp(skill) for skill in skills_list]
matcher.add("SKILLS", patterns)


# Hàm để tìm kiếm kỹ năng trong văn bản
def find_skills(text):
  doc = spacy_nlp(text)
  matches = matcher(doc)
  found_skills = []

  for match_id, start, end in matches:
    span = doc[start:end]
    found_skills.append(span.text.lower())  # Chuyển thành chữ thường

  return found_skills


# Lớp test
class TestSkillMatcher(unittest.TestCase):

  def test_find_skills(self):
    text = "I have experience with Python, Java, and Docker."
    expected_skills = ["python", "java"]  # Chuyển thành chữ thường

    found_skills = find_skills(text)

    # Kiểm tra xem các kỹ năng tìm thấy có đúng như mong đợi không
    self.assertTrue(all(skill in found_skills for skill in expected_skills))
    self.assertEqual(len(found_skills),
                     3)  # Cập nhật số lượng kỹ năng đã tìm thấy

  def test_no_skills_found(self):
    text = "I am learning new technologies."
    found_skills = find_skills(text)

    # Kiểm tra xem không có kỹ năng nào được tìm thấy
    self.assertEqual(found_skills, [])


if __name__ == "__main__":
  unittest.main()
