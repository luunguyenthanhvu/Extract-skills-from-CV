import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from job_scraper.items import JobScraperItem
import os
from csv import writer

class JobScraper(CrawlSpider):
    name = 'jobscraper'
    start_urls = ["https://itviec.com"]
    rules = (
        Rule(LinkExtractor(
                restrict_css=".menu-content.bg-it-black.small-text.position-absolute > .row.g-1 > .flex-column > a"),
                follow=True),
        Rule(LinkExtractor(
            restrict_css=".col-md-5.card-jobs-list.ips-0.ipe-0.ipe-md-6 > .job-card > h3 > a"),
            callback='parse_job')
    )


    def parse_job(self, response):
        job = JobScraperItem()

        # Extract job title
        job['title'] = response.css(".job-header-info > h1::text").get()

        # Extract required skills
        job['required_skills'] = response.css(
            ".imy-5.paragraph:nth-of-type(2) > ul > li::text").getall()

        # Save to file
        self.save_to_file(job['title'], job['required_skills'])
        return job

    def save_to_file(self, title, required_skills):
        # Convert list of skills to a comma-separated string
        required_skills_str = ', '.join(required_skills)

        # Check if the file exists and write data
        file_exists = os.path.isfile("data.csv")

        if os.path.isfile("data.csv"):
            with open('data.csv', 'a') as f_object:
                writer_object = writer(f_object)

                # Pass the list as an argument into
                # the writerow()
                writer_object.writerow([self.title, required_skills_str])
                # Close the file object
                f_object.close()
        else:
            with open('data.csv', 'w') as f_object:
                writer_object = writer(f_object)

                # Pass the list as an argument into
                # the writerow()
                writer_object.writerow([self.title, required_skills_str])
                # Close the file object
                f_object.close()