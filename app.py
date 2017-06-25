import sqlite3
import itertools
import urllib
import requests
import tinder
import threading
import pymysql
import pymysql.cursors

from flask import Flask, render_template,request

app = Flask(__name__)

conn = pymysql.connect(host="172.17.0.2", user="root", password="qazwsx", database="test", cursorclass=pymysql.cursors.DictCursor)

drop = "DROP TABLE IF EXISTS images; DROP TABLE IF EXISTS users"
create_query = "CREATE TABLE users(user_id int primary key auto_increment, name varchar(256) UNIQUE)"
create_img_table_query = "CREATE TABLE images(img_id int primary key auto_increment, user_id int, img_url varchar(256), happy DOUBLE, neutral DOUBLE, sad DOUBLE, FOREIGN KEY(user_id) REFERENCES users(user_id))"
with conn.cursor() as cursor:
    cursor.execute(drop)
    cursor.execute(create_query)
    cursor.execute(create_img_table_query)


params = {
    "redirect_uri" : "http://localhost:5000/login/100006055697656",
    "state" : '{"challenge":"q1WMwhvSfbWHvd8xz5PT6lk6eoA%3D","0_auth_logger_id":"54783C22-558A-4E54-A1EE-BB9E357CC11F","com.facebook.sdk_client_state":true,"3_method":"sfvc_auth"}',
    "scope" : "user_birthday,user_photos,user_education_history,email,user_relationship_details,user_friends,user_work_history,user_likes",
    "response_type" : "token,signed_request",
    "default_audience" : "friends",
    "return_scopes" : "true",
    "auth_type" : "rerequest",
    "client_id" : "464891386855067",
    "ret" : "login",
    "sdk" : "ios", 
    "logger_id" : "54783C22-558A-4E54-A1EE-BB9E357CC11F"
}
url = "www.facebook.com/v2.6/dialog/oauth?"

fb_login_url = url + urllib.urlencode(params)
print(fb_login_url)
# exit()

@app.route("/login/<int:profile_id>")
def login(profile_id):
    print(request.args)
    token = request.args.get("access_token")
    print(token)
    if token:
        t = threading.Thread(target=tinder.scrape, args=(conn, profile_id, token))
        t.start()

    return "authorized!"

@app.route("/")
@app.route("/<int:page>")
def template_test(page=0):
    cursor = conn.cursor()
    print (((page * 12) - 12, page * 12))

    x = cursor.execute("""
        select u.name, i.img_url, i.happy, i.neutral, i.sad from images i 
        JOIN users u ON i.user_id = u.user_id limit 12 OFFSET %s
        """, (page * 12,))
    l = cursor.fetchall()
    for item in l:
        item['happy'] = round(item['happy'], 4)
        item['neutral'] = round(item['neutral'], 4)
        item['sad'] = round(item['sad'], 4)
    return render_template('templates.html', my_string="Tinder Surprise", my_list=l)


if __name__ == '__main__':
    app.run(debug=True)
