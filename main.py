# -*- coding: utf_8 -*-
from flask import Flask, render_template, request, send_from_directory, flash
import glob
import search
import csv 
import os
import datetime
import codecs
from urllib.error import HTTPError
import re

app = Flask(__name__)

# index page, sellect category to get info
@app.route("/", methods = ['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html', title = "select category")
    if request.method == 'POST':
        categories = request.form.getlist("category")
        return render_template('index.html', name = categories)

@app.route("/create", methods = ['POST'])
def create():
    try:
        category_urls = []
        category_names = []
        title = "creating files"
        if request.method == 'POST':
            category_values = request.form.getlist("category")
            for value in category_values:
                category_urls.append(value.split(",")[0])
                category_names.append(value.split(",")[1])
            searchAndWrite(category_urls, category_names)
            return render_template('index.html', title = title)
    except HTTPError as e:
        content = e.read()
        print(content)
        return content

def saveProcessingCategory(category_name):
    f = open("processing.txt", 'a')
    f.write(category_name + '\n')
    f.close()

def deleteProcessingCategory(category_name):
    f = open("processing.txt")
    lines = f.readlines()
    f.close()
    pat = re.compile(r'.*%s.*' % category_name)
    i = 0
    for line in lines:
        #fs.write("%s" % (re.sub(pat,"",line)))
        if pat.search(line):
            del lines[i]
        #fs.close()
    fs = open("processing.txt","w")
    for new_line in lines:
        fs.write(new_line)
    fs.close()

def saveWaitingCategory(category_names):
    f = open("waiting.txt", 'a')
    for line in category_names:
        f.write(line + '\n')
    f.close()

def deleteWaitingCategory(category_name):
    f = open("waiting.txt")
    lines = f.readlines()
    f.close()
    pat = re.compile(r'.*%s.*' % category_name)
    i = 0
    for line in lines:
        if pat.search(line):
            del lines[i]
    fs = open("waiting.txt","w")
    for new_line in lines:
        fs.write(new_line)
    fs.close()

def searchAndWrite(category_urls, category_names):
    i = 0
    try:
        #saveWaitingCategory(category_names[1:])
        for category_url in category_urls:
            now = datetime.datetime.now()
            csvname = now.strftime("%Y%m%d%H%M%S")
            csvpath = "csv/" + csvname + "_" + category_names[i] + ".csv"
            #saveProcessingCategory(category_names[i])
            #deleteWaitingCategory(category_names[i])
            page = 0
            while True:
                page = page + 1
                category_url_page = category_url + '&page=' + str(page)
                urls = search.getProductURLs(category_url_page)
                if len(urls) == 0:
                    break
                print(urls)
                for url in urls:
                    try:
                        f = codecs.open(csvpath, 'a', 'shift_jis')
                        base_info = search.search(url)
                        info = base_info[:2] + [url] + base_info[2:-1] + [category_names[i]]
                        print(info)
                        csvWriter = csv.writer(f)
                        csvWriter.writerow(info)
                        f.close()
                    except Exception as e:
                        print(e)
                        continue
            #deleteProcessingCategory(category_names[i])
            i = i + 1 # category_name number which is pair with the url
            os.chmod(csvpath, 0o777) #権限の変更
    except Exception as e:
        print(e)
        searchAndWrite(category_urls[i:], category_names[i:])

# show all created csv files
@app.route("/show")
def show():
    _files = glob.glob("csv/*")
    _tuples = []
    for x in _files:
        tuple = (x[4:17], x)
        _tuples.append(tuple)
    _tuples.sort(key = lambda x: int(x[0]), reverse = True)
    _filenames = [x[1][4:] for x in _tuples]
    #_files.sort(key=os.path.getmtime, reverse=True)

    #_filenames = []
    #for f in _files:
    #    _filenames.append(f[4:])
    return render_template('show.html', title = "show files", files = _filenames)

@app.route("/download/<path:filename>")
def download(filename):
    """donwload file"""
    return send_from_directory('.', filename)

if __name__ == "__main__":
    app.debug = True
    app.run(threaded=True)
