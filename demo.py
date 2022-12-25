import requests
url = 'https://www.sogou.com/'
resp = requests.get(url)
print(resp.text)
