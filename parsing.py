import requests
import re
from queue import Queue
from bs4 import BeautifulSoup

import PyQt5
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import uic

from multiprocessing import Pool


class Parsing(QObject):
    Signal_Data = pyqtSignal(int, str)

    def __init__(self, URL):
        super().__init__()

        self.URL = URL

        self.Internal_Links = set()
        self.External_Links = set()
        self.JavaScripts = set()
        self.Images = set()

        self.Server = None
        self.BS = None
        self.URL_Queue = None


    def GetData(self):
        self.URL_Queue = Queue()

        self.Internal_Links.add(self.URL)
        self.URL_Queue.put(self.URL)

        self.Signal_Data.emit(1, self.URL)

        while not self.URL_Queue.empty():
            Next_URL = self.URL_Queue.get()

            site_depth = str(len(Next_URL.split('/')) - len(self.URL.split('/')))
            print(Next_URL, "로 접근, SITE depth :", site_depth)

            req = requests.get(Next_URL)

            if self.Server is None:
                self.Server = req.headers['server']

            html = req.text
            self.BS = BeautifulSoup(html, 'html.parser')

            self.GetLink()
            self.GetJavaScript()
            self.GetResources()

        return self.Internal_Links


    def GetLink(self):
        if self.BS is None:
            return

        for links in self.BS.findAll('a'):
            if 'href' not in links.attrs:  # href 속성이 없으면 넘김.
                continue

            link = links.attrs['href']
            if len(link) == 0:
                continue

            cmd = self.Check_URL(link)

            if cmd == 0:
                continue

            link = self.LinkPreProcessing(link)

            if cmd == 1:  # External Link
                if link not in self.External_Links:
                    self.External_Links.add(link)
                    self.Signal_Data.emit(2, link)
            elif cmd == 2:  # Internal Link
                if self.URL not in link:
                    link = self.URL + link
                if link not in self.Internal_Links:
                    self.Internal_Links.add(link)
                    self.URL_Queue.put(link)
                    self.Signal_Data.emit(1, link)


    def GetJavaScript(self):
        if self.BS is None:
            return

        for script in self.BS.findAll('script'):
            if 'src' not in script.attrs:
                continue
            script_uri = script.attrs['src']
            script_uri = self.LinkPreProcessing(script_uri)
            if script_uri not in self.JavaScripts:
                self.JavaScripts.add(script_uri)
                self.Signal_Data.emit(3, script_uri)


    def GetResources(self):
        if self.BS is None:
            return

        for img in self.BS.findAll('img'):  # get Image URI
            if 'src' not in img.attrs:
                continue
            img_uri = img.attrs['src']
            img_uri = self.LinkPreProcessing(img_uri)
            if img_uri not in self.Images:
                self.Images.add(img_uri)
                self.Signal_Data.emit(4, img_uri)


    def Check_URL(self, url):  # 1 = External Link, 2 = Internal Link
        if url[0] == '/':  # Internal Link
            return 2
        else:
            if self.URL in url:  # Internal Link
                return 2
            if 'http://' in url or 'https://' in url:  # External Link
                return 1
            return 0


    def LinkPreProcessing(self, link):
        if '?' in link:
            link = link[:link.index('?')]
        if '#' in link:
            link = link[:link.index('#')]
        if link[-1] == '/':
            link = link[:-1]
        return link


'''
if __name__ == "__main__":
    #module = Parsing("http://218.146.55.65")
    module = Parsing("https://kyounghwankim.github.io")
    #module = Parsing("https://naver.com")
    print(module.GetData())
    print(module.External_Links)
    print(module.Images)
    print(module.JavaScripts)
    print(len(module.Internal_Links))
    print(len(module.External_Links))
    print(len(module.Images))
    print(len(module.JavaScripts))
    print(module.Server)
'''