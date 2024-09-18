import scrapy
from bleach import clean
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.exceptions import CloseSpider
from crawl_job_data.items import CrawlJobDataItem

import os
import re
from bs4 import BeautifulSoup
from csv import writer


class JobScraper(CrawlSpider):
  name = 'jobs_topcv'
  start_urls = [f"https://www.topcv.vn/viec-lam-it?page={i}" for i in range(30,64)]


  rules = (
        # Rule để theo dõi các liên kết dẫn tới trang chi tiết công việc
        Rule(LinkExtractor(
            restrict_css=".job-list-2 > .job-item-2 > .box-header > .body > .title-block > h3 > a"),  # Chọn liên kết bằng CSS selector
            callback='parse_job',  # Callback khi vào trang chi tiết công việc
            follow=True),  # Tiếp tục theo dõi các liên kết
    )

  def remove_all_html_tags(self, html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    return soup.get_text()

  # def parse(self, response):
  #   # Trích xuất liên kết đến các trang chi tiết công việc từ trang danh sách
  #   links = response.css(
  #     '.job-list-2 > .job-item-2 > .box-header > .body > .title-block > h3 > a::attr(href)').getall()
  #   links_str = ', '.join(links)
  #
  #   print("Các link: " + links_str)
  #   for link in links:
  #     yield response.follow(url=link, callback=self.parse_job)

  def parse_job(self, response):
    print("Bắt đầu ghi lại job")
    job = CrawlJobDataItem()

    # Extract job title
    job['title'] = (response.css(
      ".job-detail__info--title").get())

    # Extract required skills
    # Lấy tất cả các div con của section > #JobDescription
    divs = response.css(".job-detail__information-detail--content > .job-description > div:has(h3)")
    for div in divs:
      # Lấy văn bản của phần tử <h2> bên trong <div>
      h2_text = div.css('h3::text').get()

      # Kiểm tra xem văn bản có phải là 'Your skills & qualifications' không
      if h2_text and (
          'Yêu cầu ứng viên' in h2_text or 'Kỹ năng & Chuyên môn' in h2_text):
        job['required_skills'] = div.css(".job-description__item--content").getall()
        break
    else:
      # Nếu không tìm thấy phần tử <h2> với văn bản mong muốn
      job['required_skills'] = 'N/A'

    if not job['title'] and job['required_skills'] == 'N/A':
      print("Stopping crawl: title and required skills are both missing.")
      return

    print("JOB DATA Nè" + str(job['title']) + str(job['required_skills']))

    # Save to file
    self.save_to_file(job['title'], job['required_skills'])
    return job

  def format_text(self,text):
    # Xóa tất cả khoảng trắng ở đầu và cuối từng dòng
    lines = [line.strip() for line in text.splitlines()]
    # Loại bỏ các dòng trống
    lines = [line for line in lines if line]
    # Gộp các dòng thành một dòng duy nhất
    one_line_text = ' '.join(lines)
    return one_line_text

  def save_to_file(self, title, required_skills):
    # Chuyển danh sách kỹ năng thành chuỗi ngăn cách bởi dấu phẩy
    required_skills_str = ', '.join(required_skills)

    # Xóa các thẻ <li> và nội dung của chúng trước khi lưu
    cleaned_required_skills = self.remove_all_html_tags(required_skills_str)
    clean_title = self.remove_all_html_tags(title)
    cleaned_title = self.format_text(clean_title)
    cleaned_required_skills2 = self.format_text(cleaned_required_skills)
    # Kiểm tra xem file đã tồn tại hay chưa
    if os.path.isfile("data_topcv.csv"):

      # Mở file ở chế độ 'a' (append) để ghi tiếp nội dung, sử dụng mã hóa UTF-8
      with open('data_topcv.csv', 'a', encoding='utf-8', newline='') as f_object:
        writer_object = writer(f_object)

        # Ghi tiêu đề công việc và các kỹ năng vào file
        writer_object.writerow([cleaned_title, cleaned_required_skills2])
    else:
      # Nếu file chưa tồn tại, tạo mới file và ghi dữ liệu, sử dụng mã hóa UTF-8
      with open('data_topcv.csv', 'w', encoding='utf-8', newline='') as f_object:
        writer_object = writer(f_object)

        # Ghi tiêu đề công việc và các kỹ năng vào file
        writer_object.writerow([cleaned_title, cleaned_required_skills2])