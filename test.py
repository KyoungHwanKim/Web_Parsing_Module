import requests
import sys


url = "https://httpd.apache.org/"

y = sys.platform
print(y)

x = requests.get(url)
print(x.headers)
for i in x.headers.keys():
    print(i, x.headers[i])