import requests
from bs4 import BeautifulSoup
import tweepy
import json
from random import random
from math import floor
import os

client = tweepy.Client(
    bearer_token="AAAAAAAAAAAAAAAAAAAAAKjtZAEAAAAAvFP7RLogOw2qFR80Kbvdvyble4w%3D8bz4Vvvv0nA5zAJKEnawannBXpG5e4Ip3k2SmIiAAbQYFVcOQZ",
    consumer_key="F40GQQQTHsGzJ9EQqvqLUHKWa",
    consumer_secret="BsFPJsQoDv1GVH3I5esihFBaguZzBSUgB9dLRqNrx1mzxZyJNY",
    access_token="1493235989220888582-QqlEtdu7k2NS0rDtFy3AsEIbsVdXgx",
    access_token_secret="FD4ny3DFrn0TQEsLqFBx555cwawFDqKqZ0Lu1513ltuQV"
)

reviews_list = []
with open("reviews.json") as json_file:
    reviews_list = json.load(json_file)

page = requests.get("https://letterboxd.com/menkoala/films/reviews/page/1/")

soup = BeautifulSoup(page.content, "html.parser")


latest_review = soup.find_all("div", class_="film-detail-content")[0]
latest_movie_title = latest_review.find_all("h2", class_="headline-2")[0].text
if latest_movie_title.strip() != reviews_list[0]["title"]:
    reviews_list = []
    number_pages = soup.find_all("li", class_="paginate-page")[-1].text
    for i in range(int(number_pages)):
        page = requests.get("https://letterboxd.com/menkoala/films/reviews/page/"+str(i+1)+"/")

        soup = BeautifulSoup(page.content, "html.parser")

        reviews = soup.find_all("div", class_="film-detail-content")

        for review in reviews:
            movie_title = review.find_all("h2", class_="headline-2")[0].text
            rating = review.find_all("span", class_="rating")[0].text
            review_text = review.find_all("div", class_="body-text")[0].text
            reviews_list.append({"title": movie_title.strip(), "rating": rating.strip(), "review": review_text.strip()})
    os.remove("reviews.json")
    f = open("reviews.json", "w")

    json.dump(reviews_list,f)

    f.close()

    print(len(reviews_list[0]["review"]))

print(floor(random()*len(reviews_list)))
posted_successfully = False
while not posted_successfully:
    try:
        index = floor(random()*len(reviews_list))
        tweet_text = reviews_list[index]["title"]+"\nRating: "+reviews_list[index]["rating"].replace("★","⭐")+"\n"+reviews_list[index]["review"]
        print(tweet_text)
        in_reply_to_tweet_id = ""
        while len(tweet_text) != 0:
            next_tweet = ""
            if len(tweet_text)>280:
                next_tweet = tweet_text[273:]
                tweet_text = tweet_text[:273]+"..."
            if len(in_reply_to_tweet_id) == 0:
                data = client.create_tweet(text=tweet_text)
            else:
                data = client.create_tweet(text=tweet_text,in_reply_to_tweet_id=in_reply_to_tweet_id)
            in_reply_to_tweet_id = data.data["id"]
            print(in_reply_to_tweet_id)
            tweet_text = next_tweet
            posted_successfully = True
    except tweepy.errors.Forbidden:
        print("Already posted")

#client.create_tweet(text=tweet_text,in_reply_to_tweet_id=in_reply_to_tweet_id)




# twitter_auth_keys = {
#     "consumer_key"        : "F40GQQQTHsGzJ9EQqvqLUHKWa",
#     "consumer_secret"     : "BsFPJsQoDv1GVH3I5esihFBaguZzBSUgB9dLRqNrx1mzxZyJNY",
#     "access_token"        : "1493235989220888582-QqlEtdu7k2NS0rDtFy3AsEIbsVdXgx",
#     "access_token_secret" : "FD4ny3DFrn0TQEsLqFBx555cwawFDqKqZ0Lu1513ltuQV"
# }

# auth = tweepy.OAuthHandler(
#         twitter_auth_keys['consumer_key'],
#         twitter_auth_keys['consumer_secret']
#         )
# auth.set_access_token(
#         twitter_auth_keys['access_token'],
#         twitter_auth_keys['access_token_secret']
#         )
# api = tweepy.API(auth)

# # Upload image
# media = api.media_upload("koala.jpg")

# # Post tweet with image
# tweet = "Koala"
# post_result = api.update_status(status=tweet, media_ids=[media.media_id])