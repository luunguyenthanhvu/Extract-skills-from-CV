import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.exceptions import CloseSpider
from crawl_job_data.items import CrawlJobDataItem
import os
import re
from bs4 import BeautifulSoup
from csv import writer


class JobScraper(CrawlSpider):
  name = 'jobs_topdev'
  start_urls = ["https://topdev.vn"]

  rules = (
      Rule(LinkExtractor(
              restrict_css=".group.relative:first-child > ul > li:nth-of-type(4) > ul > ul > li > a"),
          follow=True),

      Rule(LinkExtractor(
          restrict_css="#tab-job > div > ul > li > a"),
          callback='parse_job')
  )

  # rules = (
  #       # Rule để theo dõi các liên kết dẫn tới trang chi tiết công việc
  #       Rule(LinkExtractor(
  #           restrict_css="#tab-job > div > ul > li > a"),  # Chọn liên kết bằng CSS selector
  #           callback='parse_job',  # Callback khi vào trang chi tiết công việc
  #           follow=True),  # Tiếp tục theo dõi các liên kết
  #   )

  def remove_all_html_tags(self, html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    return soup.get_text()


  def parse_job(self, response):
    job = CrawlJobDataItem()

    # Extract job title
    job['title'] = response.css(
      "#detailJobHeader > div > h1::text").get()

    # Extract required skills
    # Lấy tất cả các div con của section > #JobDescription
    divs = response.css("#JobDescription > div:has(h2)")
    for div in divs:
      # Lấy văn bản của phần tử <h2> bên trong <div>
      h2_text = div.css('h2::text').get()

      # Kiểm tra xem văn bản có phải là 'Your skills & qualifications' không
      if h2_text and (
          'Your skills & qualifications' in h2_text or 'Kỹ năng & Chuyên môn' in h2_text):
        job['required_skills'] = div.css("div > ul > li").getall()
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

  def save_to_file(self, title, required_skills):
    # Chuyển danh sách kỹ năng thành chuỗi ngăn cách bởi dấu phẩy
    required_skills_str = ', '.join(required_skills)

    # Xóa các thẻ <li> và nội dung của chúng trước khi lưu
    cleaned_required_skills = self.remove_all_html_tags(required_skills_str)

    # Kiểm tra xem file đã tồn tại hay chưa
    if os.path.isfile("data_topdev.csv"):

      # Mở file ở chế độ 'a' (append) để ghi tiếp nội dung, sử dụng mã hóa UTF-8
      with open('data_topdev.csv', 'a', encoding='utf-8', newline='') as f_object:
        writer_object = writer(f_object)

        # Ghi tiêu đề công việc và các kỹ năng vào file
        writer_object.writerow([title, cleaned_required_skills])
    else:
      # Nếu file chưa tồn tại, tạo mới file và ghi dữ liệu, sử dụng mã hóa UTF-8
      with open('data_topdev.csv', 'w', encoding='utf-8', newline='') as f_object:
        writer_object = writer(f_object)

        # Ghi tiêu đề công việc và các kỹ năng vào file
        writer_object.writerow([title, cleaned_required_skills])