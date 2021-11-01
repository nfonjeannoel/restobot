import scrapy
from pyasn1.compat.octets import null
from time import sleep


def small_sleep():
    sleep(0.1)


def get_image_list(myresult):
    img_list = []
    for test in myresult:
        build = False
        res = ""
        for char in test:
            if char == ")":
                img_list.append(res)
                break
            if build == True:
                res += char
            if char == "(":
                build = True
    return img_list


def get_phone_list(test):
    num_list = []
    for item in test:
        build = False
        res = ""
        for ind, char in enumerate(item):
            if build:
                if char == "<":
                    num_list.append(res)
                    break
                res += char
                continue
            if char == "(":
                if item[ind + 4] == ")":
                    res += char
                    build = True
    return num_list


first_next_counter = True
max_count = 0
hundred_adder = 0
page_counter = 0


class RestoBot(scrapy.Spider):
    name = "restobot"

    #check main,py for start urls for various countries

    start_urls = [
    "https://www.opentable.ca/rest_list.aspx?m=358",
    "https://www.opentable.ca/s/restaurantlist?metroid=3374",
    "https://www.opentable.ca/rest_list.aspx?m=310",
    "https://www.opentable.ca/los-cabos-mexico-restaurant-listings",
    "https://www.opentable.ca/rest_list.aspx?m=502",
    "https://www.opentable.ca/rest_list.aspx?m=346",
    "https://www.opentable.ca/s/restaurantlist?metroid=499",
    "https://www.opentable.ca/rest_list.aspx?m=334",
    "https://www.opentable.ca/rest_list.aspx?m=475",
    "https://www.opentable.ca/rest_list.aspx?m=3400",
    "https://www.opentable.ca/s/restaurantlist?metroid=490",
    "https://www.opentable.ca/rest_list.aspx?m=349",
    "https://www.opentable.ca/rest_list.aspx?m=442",
    "https://www.opentable.ca/s/restaurantlist?metroid=3385",
    "https://www.opentable.ca/mexico-city-mexico-restaurant-listings",
    "https://www.opentable.ca/s/restaurantlist?metroid=3383",
    "https://www.opentable.ca/rest_list.aspx?m=355",
    "https://www.opentable.ca/s/restaurantlist?metroid=3370",
    "https://www.opentable.ca/s/restaurantlist?metroid=3486",
    "https://www.opentable.ca/rest_list.aspx?m=478",
    "https://www.opentable.ca/rest_list.aspx?m=361",
    "https://www.opentable.ca/puerto-vallarta-mexico-restaurant-listings",
    "https://www.opentable.ca/rest_list.aspx?m=457",
    "https://www.opentable.ca/rest_list.aspx?m=460",
    "https://www.opentable.ca/s/restaurantlist?metroid=508",
    "https://www.opentable.ca/rest_list.aspx?m=352",
    "https://www.opentable.ca/rest_list.aspx?m=472",
    "https://www.opentable.ca/rest_list.aspx?m=3443",
    "https://www.opentable.ca/s/restaurantlist?metroid=3437",
    "https://www.opentable.ca/rest_list.aspx?m=364",
    "https://www.opentable.ca/s/restaurantlist?metroid=505",
    "https://www.opentable.ca/rest_list.aspx?m=493"
]

    def get_details(self, response):
        # global first_next_counter
        # if first_next_counter:
        #     global max_count
        #     max_count = 5
        #     first_next_counter = False
        other_offers = []
        p_list = []
        phone_list = []
        twit_list = []
        image_list = []
        other_image = []
        tags = []
        website = ""
        brief_description = ""
        menu_list = []
        review_list = []
        location = ""

        hotel_name = response.css("h1.a6481dc2._4a4e7a6a::text").get()
        if hotel_name is None or len(hotel_name.split()) == 0:
            # page uses different css selectors probably when it does not have enough info or is not verified
            if hotel_name is not None:
                # resto is not verified and uses different tags
                hotel_name = response.css("h1.Ic5GaGP-VRdwdCHinbp2R._1E11-nyyWnndSSOElGuAVa::text").get()

                brief_description = response.css("p._33FNBS4DDcGGOaAeUsBAsR._3ZYgMThR77irVoyAamOJ3X span::text").get()
                meal_names = response.css("h4.W9xFP5fLkpgG1TNINCYQQ span::text").extract()
                meal_description = response.css("p._3ENq-b1Q6nZK-iI1ZI5Vyk::text").extract()
                menu_name = response.css("h3._3LCWn88NzkJFiBtcOWtTZX.ZaqwCEmxQvIesKN8NRNfi::text").get()
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

                new_meals = []
                for meal in meal_names:
                    if "€" in meal:
                        last = new_meals[-1]
                        new_meals[-1] = last + " - " + meal
                meal_names = new_meals
                meal_list = []

                for meal_ind, meal in enumerate(meal_names):
                    price = "NA"
                    name = meal
                    if "€" in meal.split()[-1]:
                        price = meal.split()[-1]
                        name = " ".join(meal.split()[:-2])
                    try:
                        meal_list.append({
                            "name": name,
                            "price": price,
                            "description": meal_description[meal_ind]
                        })
                    except:
                        meal_list.append({
                            "name": name,
                            "price": price,
                            "description": "NA"
                        })
                menu_list = [
                    {"menu_name": menu_name}, {"items": meal_list}
                ]

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
        # self.no_use()

        else:
            tags = response.css("a.d302396e::text").extract()

            brief_description = response.css("div._3c23fa05 div::text ").get()
            meal_names = response.css("div.menu-item-header__3xwnFL-n div::text").extract()
            new_meals = []

            for meal in meal_names:
                if "$" in meal:
                    new_meals[-1] = new_meals[-1] + " - " + meal
                else:
                    new_meals.append(meal)

            meal_names = new_meals

            meal_description = response.css("p.menu-description__2HXkC4oE::text").extract()
            menu_name = response.css("h3.menu-section-title__22Q2IFWX::text").get()
            # prices = response.css("div.menu-item-header__3xwnFL-n div::text").extract()
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

            meal_list = []

            for meal_ind, meal in enumerate(meal_names):
                price = "NA"
                name = meal
                if "$" in meal.split()[-1]:
                    price = meal.split()[-1]
                    name = " ".join(meal.split()[:-2])
                try:
                    meal_list.append({
                        "name": name,
                        "price": price,
                        "description": meal_description[meal_ind]
                    })
                except:
                    meal_list.append({
                        "name": name,
                        "price": price,
                        "description": "NA"
                    })
            menu_list = [
                {"menu_name": menu_name}, {"items": meal_list}
            ]
        yield {
            "hotel_name": hotel_name,
            "url": response.url,
            "tags": tags + other_offers,
            "popular_dishes": p_list,
            "phone_number": phone_list,
            "location": location,
            "website": website,
            "overview": brief_description,
            "menu": menu_list,
            "reviews": review_list,
            "twitter_reviews": twit_list,
            "image": image_list + other_image
        }



    def parse(self, response):
        hotel_names = response.css("a.rest-row-name::attr(href)").extract()
        # counter = 0
        global page_counter
        page_counter += 1
        for hotel in hotel_names:
            # if len(hotel) > 8:
            # counter += 1
            small_sleep()
            yield response.follow(hotel, callback=self.get_details)
            # if counter >2:
            #     break
            # next_page = response.css("a.pagination-link.pagination-next::attr(href)").get()
            # if next_page is not None:
        # global max_count
        # if page_counter < max_count:
        #     base = "https://www.opentable.ca/nova-scotia-new-brunswick-restaurant-listings?covers=2&currentview=list&datetime=2021-11-01+19%3A00&latitude=45.9308&longitude=-63.67584&metroid=274&size=100&sort=Popularity&from="
        #     base += "100"
        #     yield scrapy.Request(base, callback=self.parse)

        # if counter >= 10:
        #     break
