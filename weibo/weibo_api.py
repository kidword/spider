# coding:utf-8

import webbrowser
import weibo

APP_KEY = '3046161119'
MY_APP_SECRET = 'ccf12aad12515498132abc3487f5fa03'
REDIRECT_URL = 'https://api.weibo.com/oauth2/default.html'


client = weibo.APIClient(APP_KEY, MY_APP_SECRET)
authorize_url = client.get_authorize_url(REDIRECT_URL)
webbrowser.open(authorize_url)
code = raw_input("input the code: ").strip()

request = client.request_access_token(code, REDIRECT_URL)


access_token = request.access_token
expires_in = request.expires_in
uid = request.uid

client.set_access_token(access_token, expires_in)
get_results = client.statuses__friends_timeline()

