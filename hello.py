from flask import Flask, render_template, request, send_from_directory
import glob
import search
import csv
import os
import datetime
from urllib.error import HTTPError

app = Flask(__name__)

# index page, sellect category to get info
@app.route("/", methods = ['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html', title = "select category")
    if request.method == 'POST':
        categories = request.form.getlist("category")
        return render_template('index.html', name = categories)

# create csv files
'''
@app.route("/create", methods = ['POST'])
def create():
    try:
        now = datetime.datetime.now()
        csvname = now.strftime("%Y%m%d%H%M%S")
        title = "creating files"
        if request.method == 'POST':
            category_url = request.form.getlist("category")[0]
            urls = search.scrollAndGetURLs(category_url)
            print(urls)
            for url in urls:
                info = search.search(url) + [url] # [name, jcode, price, stock, points, url]
                print(info)
                f = open("csv/" + csvname + ".csv", 'a')
                csvWriter = csv.writer(f)
                csvWriter.writerow(info)
                f.close()
            return render_template('index.html', title = title)
    except HTTPError as e:
        content = e.read()
'''
@app.route("/create", methods = ['POST'])
def create():
    try:
        page = 0
        now = datetime.datetime.now()
        csvname = now.strftime("%Y%m%d%H%M%S")
        title = "creating files"
        if request.method == 'POST':
            category_url = request.form.getlist("category")[0] + '&page=' + str(page)
            while True:
                page = page + 1
                category_url = request.form.getlist("category")[0] + '&page=' + str(page)
                urls = search.getProductURLs(category_url)
                #if isinstance(urls, type(None)):
                if len(urls) == 0:
                    f.close()
                    break
                print(urls)
                for url in urls:
                    info = search.search(url) + [url] # [name, jcode, price, stock, points, url]
                    print(info)
                    f = open("csv/" + csvname + ".csv", 'a')
                    csvWriter = csv.writer(f)
                    csvWriter.writerow(info)
            return render_template('index.html', title = title)
    except HTTPError as e:
        content = e.read()

# show all created csv files
@app.route("/show")
def show():
    _files = glob.glob("csv/*")
    _files.sort(key=os.path.getmtime, reverse=True)

    _filenames = []
    for f in _files:
        _filenames.append(f[4:])
    return render_template('show.html', title = "show files", files = _filenames)

@app.route("/download/<path:filename>")
def download(filename):
    """donwload file"""
    return send_from_directory('.', filename)

if __name__ == "__main__":
    app.debug = True
    app.run()
