import json
import datetime
import boto3
from scrapy.crawler import CrawlerProcess

from algorithm import getJson, get_image_list, get_phone_list, get_ird, get_menu
import scrapy
import requests
from scrapy import cmdline
from restobot.restobot.spiders.endpoints import endpoint

first_next_counter = True
max_count = 0
hundred_adder = 0
page_counter = 0
all_data = []
choice = 0
all_data = []


def save_data():
    global all_data
    with open(f"{file_name}.json", "w") as f:
        f.write(json.dumps(all_data))
    f.close()


class RestoBot(scrapy.Spider):
    name = "restobot"
    print(f"""
        choose 1 for canada
        choose 2 for germany
        choose 3 for mexico
        """)
    choice = int(input("enter choice"))
    # check main,py for start urls for various countries
    # change filename to the name of the city
    global file_name
    if choice == 1:
        start_urls = endpoint[1]
        file_name = "canada"
    if choice == 2:
        start_urls = endpoint[2]
        file_name = "germany"
    if choice == 3:
        start_urls = endpoint[3]
        file_name = "mexico"

    else:
        print("*" * 20)

    def add_to_aws(self, file_name, save_store):
        # remember to change file name to the json you want

        s3 = boto3.resource('s3', aws_access_key_id="XXXXXXXXXX",
                            aws_secret_access_key="XXXXXXXX")
        s3object = s3.Object('tw-external-dumps1',
                             f"opentable/canada/{str(datetime.datetime.utcnow().isocalendar()[0]) + '-' + str(datetime.datetime.utcnow().isocalendar()[1])}/{file_name.split('/')[-1]}.json")
        s3object.put(
            Body=(bytes(json.dumps(save_store).encode('UTF-8'))))

    def get_details(self, response):
        rid = get_ird(response.css("head").get())
        menu_variants = getJson(response.text)
        # print(menu_variants)
        menus = get_menu(menu_variants)
        hotel_name = response.css("h1.a6481dc2._4a4e7a6a::text").get()
        other_offers = []
        if hotel_name is None or len(hotel_name.split()) == 0:
            tags = response.css("a.d302396e::text").extract()
            # page uses different css selectors probably when it does not have enough info or is not verified
            if hotel_name is not None:
                # resto is not verified and uses different tags
                hotel_name = response.css("h1.Ic5GaGP-VRdwdCHinbp2R._1E11-nyyWnndSSOElGuAVa::text").get()

                brief_description = response.css("p._33FNBS4DDcGGOaAeUsBAsR._3ZYgMThR77irVoyAamOJ3X span::text").get()
                other_offers = response.css("div.e7ff71b6.b2f6d1a4::text").extract()
                other_offers = other_offers[1:-2]
                website = response.css("a.v47bWSVhEfgDbPybArSqa::text").get()
                location = response.css("a.v47bWSVhEfgDbPybArSqa::text").extract()
                try:
                    location = list(location)[1]
                except:
                    location = "NA"

                reviews = response.css(
                    "p._33FNBS4DDcGGOaAeUsBAsR.IEnFAhBwfgkaFnkHj_Twl._3xyTZuwnXRvkj6X6tsZH_M::text").extract()
                reviewer_name = response.css("p.p40a8Csa04w1i7ep-x1HK.G1kfyull_V3y-AuTlAlGm::text").extract()
                stars = response.css("div._2s6ofZ_eiTKuvNHV3mVnaG::text").extract()

                review_list = []

                for review_ind, review in enumerate(reviews):
                    try:
                        review_list.append({
                            "author": reviewer_name[review_ind],
                            "text": review,
                            "rating": stars[review_ind]
                        })
                    except:
                        review_list.append({
                            "author": "NA",
                            "text": review,
                            "rating": stars[review_ind]
                        })

        else:
            tags = response.css("a.d302396e::text").extract()

            brief_description = response.css("div._3c23fa05 div::text ").get()

            reviews = response.css(".oc-reviews-8107696f p::text").extract()
            reviewer_name = response.css(".oc-reviews-954a6007 span::text").extract()
            website = response.css("._3ddfcf5c._5c8483c8::text").get()
            other_offers = response.css("div.e7ff71b6.b2f6d1a4::text").extract()
            other_offers = other_offers[1:-2]
            image = response.css("div._5fc02aaa").extract()
            image_list = get_image_list(image)
            phone_number = response.css("div.e7ff71b6.b2f6d1a4").extract()
            phone_list = get_phone_list(phone_number)
            location = response.css("a._3ddfcf5c._5c8483c8 span::text").get()
            p_title = response.css("h1.e2387a5e::text").extract()
            p_desc = response.css("p._7e61fae6::text").extract()
            stars = response.css("div.oc-reviews-7736a27d::attr(aria-label)").extract()

            twit_auth = response.css("span.TweetAuthor-name::text").extract()
            twith_auth_url = response.css("span.TweetAuthor-screenName::text").extract()
            twith_body = response.css("p.timeline-Tweet-text::text").extract()
            other_image = response.css("div.photo__10vsfGte img::attr(src)").extract()

            twit_list = []
            for auth_ind, auth in enumerate(twit_auth):
                try:
                    twit_list.append(
                        {
                            "tweet_author": auth,
                            "tweet": twith_body[auth_ind],
                            "author_url": "twitter " + twith_auth_url[auth_ind]
                        }
                    )
                except:
                    twit_list.append(
                        {
                            "tweet_author": auth,
                            "tweet": "NA",
                            "author_url": "NA"
                        }
                    )

            p_list = []

            for title_ind, title in enumerate(p_title):
                try:
                    p_list.append({
                        title: p_desc[title_ind]
                    })
                except:
                    p_list.append({
                        title: "NA"
                    })

            review_list = []

            for review_ind, review in enumerate(reviews):
                try:
                    review_list.append({
                        "author": reviewer_name[review_ind],
                        "text": review,
                        "rating": stars[review_ind].split()[0]
                    })
                except:
                    review_list.append({
                        "author": "NA",
                        "text": review,
                        "rating": "NA"
                    })

        mydata = {
            "hotel_name": hotel_name,
            "url": response.url,
            "tags": tags + other_offers,
            "rid": str(rid),
            "menu": menus,
            "popular_dishes": p_list,
            "phone_number": phone_list,
            "location": location,
            "website": website,
            "overview": brief_description,
            "reviews": review_list,
            "twitter_reviews": twit_list,
            "image": image_list + other_image
        }
        global all_data
        all_data.append(mydata)
        yield mydata

    def parse(self, response):
        hotel_names = response.css("a.rest-row-name::attr(href)").extract()
        global page_counter
        page_counter += 1
        for hotel in hotel_names:
            yield response.follow(hotel, callback=self.get_details)
            # break
        # self.add_to_aws(file_name, all_data)
        print("*saving " * 8)


if __name__ == '__main__':
    all_data = []
    process = CrawlerProcess()
    process.crawl(RestoBot)
    process.start()
    save_data()
    # cmdline.execute(f"scrapy crawl restobot -O {file_name}.json".split())
