#description _1397f114
"""
scrapy crawl restobot -O output1.json

canada start urls
["https://www.opentable.ca/nova-scotia-new-brunswick-restaurant-listings",
                  "https://www.opentable.ca/calgary-alberta-restaurant-listings",
                  "https://www.opentable.ca/edmonton-alberta-restaurant-listings",
                  "https://www.opentable.ca/manitoba-saskatchewan-restaurant-listings",
                  "https://www.opentable.ca/montreal-quebec-restaurant-listings",
                  "https://www.opentable.ca/rest_list.aspx?m=406",
                  "https://www.opentable.ca/rest_list.aspx?m=451",
                  "https://www.opentable.ca/toronto-ontario-restaurant-listings",
                  "https://www.opentable.ca/vancouver-british-columbia-restaurant-listings",
                  "https://www.opentable.ca/rest_list.aspx?m=3369"
                  ]

germany start urls
start_urls = [
        "https://www.opentable.ca/rest_list.aspx?m=3287",
        "https://www.opentable.ca/berlin-restaurant-listings",
        "https://www.opentable.ca/rest_list.aspx?m=3236",
        "https://www.opentable.ca/rest_list.aspx?m=3296",
        "https://www.opentable.ca/rest_list.aspx?m=3269",
        "https://www.opentable.ca/rest_list.aspx?m=236",
        "https://www.opentable.ca/rest_list.aspx?m=3293",
        "https://www.opentable.ca/rest_list.aspx?m=230",
        "https://www.opentable.ca/rest_list.aspx?m=233",
        "https://www.opentable.ca/rest_list.aspx?m=296",
        "https://www.opentable.ca/rest_list.aspx?m=3233",
        "https://www.opentable.ca/rest_list.aspx?m=3251",
        "https://www.opentable.ca/rest_list.aspx?m=293",
        "https://www.opentable.ca/rest_list.aspx?m=287",
        "https://www.opentable.ca/rest_list.aspx?m=3272",
        "https://www.opentable.ca/munich-restaurant-listings",
        "https://www.opentable.ca/rest_list.aspx?m=3275",
        "https://www.opentable.ca/rest_list.aspx?m=3239",
        "https://www.opentable.ca/rest_list.aspx?m=290",
        "https://www.opentable.ca/rest_list.aspx?m=3278",
        "https://www.opentable.ca/rest_list.aspx?m=3242",
        "https://www.opentable.ca/rest_list.aspx?m=3245",
        "https://www.opentable.ca/rest_list.aspx?m=3284",
        "https://www.opentable.ca/rest_list.aspx?m=3248",
        "https://www.opentable.ca/rest_list.aspx?m=242",
        "https://www.opentable.ca/rest_list.aspx?m=3260"
    ]

heading response.css("h1.a6481dc2._4a4e7a6a::text").get()
all heading from homepage
response.css("a.rest-row-name::attr(href)").extract()

next page total response.css("span.js-pagination-page.pagination-link span::text").extract()
get the last element and loop last_element * 100 times
each time, update the link of the next page and fetch it
https://www.opentable.ca/nova-scotia-new-brunswick-restaurant-listings
https://www.opentable.ca/nova-scotia-new-brunswick-restaurant-listings?
covers=2&currentview=list&datetime=2021-10-28+19%3A00&latitude=45.
9308&longitude=-63.67584&metroid=274&size=100&sort=Popularity&from=100

https://www.opentable.ca/nova-scotia-new-brunswick-restaurant-listings?
covers=2&currentview=list&datetime=2021-10-28+19%3A00&latitude=45.
9308&longitude=-63.67584&metroid=27

tags response.css("a.d302396e::text").extract()

brief description response.css("div._3c23fa05 div::text ").get()

review
response.css(".oc-reviews-8107696f p::text").extract()

reviewer name  response.css(".oc-reviews-954a6007 span::text").extract()

website response.css("._3ddfcf5c._5c8483c8::text").get()

menu name response.css("div.menu-item-header__3xwnFL-n div::text").get()



location  response.css("a._3ddfcf5c._5c8483c8 span::text").get()

meal title response.css("h1.e2387a5e::text").extract()

meal description response.css("p._7e61fae6::text").extract()


backgrounf image response.css("div._5fc02aaa").get()


img_list = []
for test in myresult:
    build = False
    res = ""
    for char in test:
        if char == ")":
            img_list.append(res)
            break
        if build == True:
            res+= char
        if char == "(":
            build = True

phone number
response.css("div.e7ff71b6.b2f6d1a4").extract()

num_list = []
for item in test:
    build = False
    res = ""
    for ind, char in enumerate(item):
        if build:
            if char == "<":
                num_list.append(res)
                break
            res+= char
            continue
        if char == "(":
            if item[ind + 4] == ")":
                res += char
                build = True


pagination
base = https://www.opentable.ca/nova-scotia-new-brunswick-restaurant-listings?covers=2&currentview=list&datetime=2021-11-01+19%3A00&latitude=45.9308&longitude=-63.67584&metroid=274&size=100&sort=Popularity&from=
base += 100

response.css("span.pagination-link span::text").extract()
get the [-1] element and cenvert to int
last = [-1]
for i in range(last):


number of stars response.css("div.oc-reviews-7736a27d::attr(aria-label)").extract()

twitter author name response.css("span.TweetAuthor-name::text").extract()
url response.css("span.TweetAuthor-screenName::text").extract()
twit body response.css("p.timeline-Tweet-text::text").extract()




for case 2
hotel name response.css("h1.Ic5GaGP-VRdwdCHinbp2R._1E11-nyyWnndSSOElGuAVa::text").get()
"""

#mexico
start = [
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


















