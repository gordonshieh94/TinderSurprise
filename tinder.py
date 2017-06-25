import requests
import pynder
import json
import itertools
import os

login = "https://www.facebook.com/v2.6/dialog/oauth?redirect_uri=fb464891386855067%3A%2F%2Fauthorize%2F&state=%7B%22challenge%22%3A%22q1WMwhvSfbWHvd8xz5PT6lk6eoA%253D%22%2C%220_auth_logger_id%22%3A%2254783C22-558A-4E54-A1EE-BB9E357CC11F%22%2C%22com.facebook.sdk_client_state%22%3Atrue%2C%223_method%22%3A%22sfvc_auth%22%7D&scope=user_birthday%2Cuser_photos%2Cuser_education_history%2Cemail%2Cuser_relationship_details%2Cuser_friends%2Cuser_work_history%2Cuser_likes&response_type=token%2Csigned_request&default_audience=friends&return_scopes=true&auth_type=rerequest&client_id=464891386855067&ret=login&sdk=ios&logger_id=54783C22-558A-4E54-A1EE-BB9E357CC11F#_=_"
# Female (Tinas) Account
# facebook_id = "100006055697656"
# token = "EAAGm0PX4ZCpsBAPzV5Krz8VTbA8SqrS71WbND98yySwdHBx2WzesNw4X58nVk01ZBN84osVZAZCM9TxiZBwUzgziePn0aNtVR4bZAfr3QiUYV0ecTdSCDVpIZBgiHHXrEFIJTo2Vb3edEYZBdXTNB8lWbd71w2iUu1kimp7L4S75Qvv6yqxtvv0WY7QbZCcpp8DhNriiv1QFR0pInjZBu8c3JJIm9OzGIYNvVJTUIQMmwRuTbrqUFKqXJxcgHKU64kodjZB3ZAi5BTBN60IgR7dJ6NWR"


endpoint = "https://westus.api.cognitive.microsoft.com/emotion/v1.0/recognize"
sub_key = "8b6fa03beb9f4d58a384dbcbe1e48d77"

def emotion(link):
    req = requests.post(url=endpoint, json={"url": link },
                   headers={'Content-Type': 'application/json',
                   'Ocp-Apim-Subscription-Key': sub_key})

    return req.json()[0]



def scrape(conn, facebook_id, token):
    msession = pynder.Session(facebook_id=facebook_id, facebook_token=token)
    msession.update_location("49.282271699999995", "-123.11903769999999")
    cursor = conn.cursor()
    for item in msession.nearby_users():
        # msession.update_location(60.615699768066, -2.344497680661191781)
        print(item.name)
        try:
            cursor.execute("insert into users(name) values(%s)", (item.name,))
            for img_url in item.get_photos(width="640"):
                print(img_url)
                scores = emotion(img_url)["scores"]
                happy = scores["surprise"] + scores["happiness"]
                neutral = scores["neutral"]
                sad = scores["sadness"]
                cursor.execute("insert into images(user_id, img_url, happy, neutral, sad) values ((select max(user_id) from users), %s, %s, %s, %s)", (str(img_url), happy, neutral, sad,))
                conn.commit()

                break; # feeling lazy
        except:
            pass

     
# x = cursor.execute("SELECT distinct u.name as name, i.img_url as img_url, distinct i.emotions as emotions FROM images i join users u")   
# l = [dict(itertools.izip(row.keys(), row)) for row in x.fetchall()]

# print(l[0])
