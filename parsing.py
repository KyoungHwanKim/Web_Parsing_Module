import requests
import re
from queue import Queue
from bs4 import BeautifulSoup


class Parsing():

    def __init__(self, URL):
        self.URL = URL

        self.Internal_Links = set()
        self.External_Links = set()

        self.JavaScripts = set()
        self.Images = set()

        self.Server = None


    def Get_Resources(self):
        self.Internal_Links.clear()

        URL_Queue = Queue()
        self.Internal_Links.add(self.URL)
        URL_Queue.put([self.URL, 0])

        while not URL_Queue.empty():
            Next_URL = URL_Queue.get()

            site_depth = str(len(Next_URL[0].split('/')) - len(self.URL.split('/')))
            print(Next_URL[0], "로 접근, SITE depth :", site_depth, "BFS depth :", str(Next_URL[1]))

            req = requests.get(Next_URL[0])

            if self.Server is None:
                self.Server = req.headers['server']

            html = req.text
            soup = BeautifulSoup(html, 'html.parser')

            for img in soup.findAll('img'):  # get Image URI
                if 'src' not in img.attrs:
                    continue
                img_uri = img.attrs['src']
                self.Images.add(img_uri)

            for script in soup.findAll('script'):
                if 'src' not in script.attrs:
                    continue
                script_uri = script.attrs['src']
                self.JavaScripts.add(script_uri)

            for links in soup.findAll('a'):
                if 'href' not in links.attrs:  # href 속성이 없으면 넘김.
                    continue

                link = links.attrs['href']
                if len(link) == 0:  # Link가 없으면 넘김.
                    continue

                cmd = self.Check_URL(link)

                if cmd == 1:  # External Link
                    self.External_Links.add(link)
                elif cmd == 2:  # Internal Link
                    if self.URL not in link:
                        link = self.URL + link
                    if link not in self.Internal_Links:
                        self.Internal_Links.add(link)
                        URL_Queue.put([link, Next_URL[1] + 1])

        return self.Internal_Links


    def Check_URL(self, url):  # 1 = External Link, 2 = Internal Link
        if url[0] == '/':  # Internal Link
            return 2
        else:
            if self.URL in url:  # Internal Link
                return 2
            if 'http://' in url or 'https://' in url:  # External Link
                return 1
            return 0


if __name__ == "__main__":
    #module = Parsing("http://218.146.55.65/wordpress")
    #module = Parsing("https://kyounghwankim.github.io")
    module = Parsing("https://naver.com")
    print(module.Get_Resources())
    print(module.External_Links)
    print(module.Images)
    print(module.JavaScripts)
    print(len(module.Internal_Links))
    print(len(module.External_Links))
    print(len(module.Images))
    print(len(module.JavaScripts))
    print(module.Server)
