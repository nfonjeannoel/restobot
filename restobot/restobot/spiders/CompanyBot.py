import scrapy


def get_linkedin_url(company_linkedin_url):
    result = ""
    for link in company_linkedin_url:
        if "linkedin" in link:
            result = link
    return result


def get_contact_linkedin(urls_url):
    result = ""
    for link in urls_url:
        if "linkedin" in link:
            result = link
            break
    return result


def get_contact_name(name_list):
    for ind, link in enumerate(name_list):
        if "linkedin" in link:
            return ind


class CompanyBot(scrapy.Spider):
    name = "companybot"

    start_urls = ["https://gregslist.com/phoenix/"]

    def get_details(self, response):
        company_name = response.css("h1.entry-title::text").get()
        urls_url = response.css("div.et_pb_text_inner div.detail a::attr(href)").extract()
        company_linkedin_url = get_linkedin_url(urls_url)
        contact_linkedin = get_contact_linkedin(urls_url)
        name_list = response.css("div.et_pb_text_inner div.detail a::text").extract()
        contact_name = name_list[get_contact_name(urls_url)]

        yield {
            "Company": company_name,
            "Company_Linkedin_Url": company_linkedin_url,
            "contact_name": contact_name,
            "contact_linkedin_url": contact_linkedin
        }

    def parse(self, response):
        redirect_links = response.css("div.company-logo-column a::attr(href)").extract()
        counter = 0
        for company in redirect_links:
            counter += 1
            yield response.follow(company, callback=self.get_details)
            # if counter == 4:
            #     break


"""
company follow url = response.css("div.company-logo-column a::attr(href)").extract()
company name = response.css("h1.entry-title::text").get()
url = response.css("div.et_pb_text_inner div.detail a::attr(href)").extract()
result = ""
for link in url:
    if "linkedin" in link:
        result = link

 response.css("div.et_pb_text_inner div.detail a::attr(href)").extract()
first contact url
result = ""
for link in url:
    if "linkedin" in link:
        url = link
        break
        
print(url)
first contact name
name_ind = response.css("div.et_pb_text_inner div.detail a::text").extract()
new_ind = 0
for ind, link in enumerate(url):
    if "linkedin" in link:
        new_ind = ind
        print(name_ind[new_ind])
        break   
print(name_ind[new_ind])
"""
