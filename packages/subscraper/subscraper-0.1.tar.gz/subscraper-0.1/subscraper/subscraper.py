import requests
import pycurl
import tempfile
from zipfile import ZipFile
from urllib import urlencode
from bs4 import BeautifulSoup
from shutil import copyfile
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import sys

class SubScraper:
    directory = None
    name = None
    cookie = {'LanguageFilter': '13'}
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    subsceneUrl = 'https://subscene.com'
    searchUrl = '/subtitles/release?'
    searchPhrase = None
    selectedSubtitle = None
    results = []

    def __init__(self, path):
        self.path = path
        self.parsePath()
        self.parseName()
        self.showInterface()

    def parsePath(self):
        self.directory, self.name = self.path.rsplit('/', 1)

    def parseName(self):
        words = self.name.split('.')
        words.pop();
        self.searchPhrase = ' '.join(words)

    def crawl(self, url):
        return BeautifulSoup(requests.get(url, cookies=self.cookie, headers=self.headers).text, 'lxml')
    
    def emptyResults(self):
        self.results = []

    def search(self):
        url = self.subsceneUrl + self.searchUrl + urlencode({'q' : self.searchPhrase})
        soup = self.crawl(url)
        for a in soup.select('td.a1 > a'):
            url = self.subsceneUrl + a.get('href')
            name = a.findAll('span')[1].text.strip()
            self.results.append({'name': name, 'url': url})

    def download(self, obj):
        soup = self.crawl(obj['url'])
        url = self.subsceneUrl + soup.select('div.download > a')[0].get('href')
        tmpZip = tempfile.mkstemp('scraper')

        fp = open(tmpZip[1], "wb")
        curl = pycurl.Curl()
        curl.setopt(pycurl.URL, url)
        curl.setopt(pycurl.WRITEDATA, fp)
        curl.setopt(pycurl.USERAGENT, self.headers['User-Agent'])
        curl.perform()
        curl.close()
        fp.close()
        
        zip = ZipFile(tmpZip[1])
        subExt = zip.namelist()[0].rsplit('.', 1)[1];
        filename = self.path.rsplit('.', 1)[0]
        destination = filename + '.' + subExt

        data = zip.read(zip.namelist()[0])
        fp = open(destination, "wb")
        fp.write(data);
        fp.close()

    def showInterface(self):
        # App
        app = QApplication(sys.argv)

        # Layout
        self.layout = QVBoxLayout()

        # Create textbox
        self.textbox = QLineEdit()
        self.textbox.setText(self.searchPhrase)
        self.textbox.textChanged.connect(self.onSearchChange)
        self.textbox.returnPressed.connect(self.onSearchPressed)
        self.layout.addWidget(self.textbox)
        
        # Search Button Widget
        self.searchButton = QPushButton("Search")
        self.searchButton.clicked.connect(self.onSearchPressed)
        # Add it to layout
        self.layout.addWidget(self.searchButton);

        # List Widget
        self.list = QListWidget()
        self.list.itemClicked.connect(self.onListItemSelected)
        # Add it to layout
        self.layout.addWidget(self.list);

        # Download Button Widget
        self.downloadButton = QPushButton("Download")
        self.downloadButton.clicked.connect(self.onDownloadPressed)
        # Add it to layout
        self.layout.addWidget(self.downloadButton);
        
        # QWidget
        self.widget = QWidget()
        self.widget.resize(600,600)
        self.widget.setWindowTitle('Scraper')
        self.widget.setLayout(self.layout)
        self.widget.show()

        sys.exit(app.exec_())

    def onListItemSelected(self, item):
        self.selectedSubtitle = self.results[item.data(Qt.UserRole).toInt()[0]]

    def onDownloadPressed(self):
        self.widget.hide()
        self.widget.close()
        self.download(self.selectedSubtitle)
        sys.exit()

    def onSearchPressed(self):
        self.list.clear()
        self.emptyResults()
        self.search()
        count = 0
        for item in self.results:
            listItem = QListWidgetItem()
            listItem.setData(Qt.UserRole, count)
            listItem.setText(item['name'])
            self.list.addItem(listItem)
            count = count + 1
        # Set first result as selected
        if self.results and self.list.count():
            self.selectedSubtitle = self.results[0]
            self.list.setCurrentRow(0)

    def onSearchChange(self):
        self.searchPhrase = self.textbox.text()