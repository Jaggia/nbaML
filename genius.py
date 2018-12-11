import json
import requests
import imp

def custom_method():
    artists = ['Logic',
               'A$AP ROCKY',
               'Kendrick Lamar',
               'Travis Scott',
               'J. Cole']

    #json.dumps([url])
    for a in artists:
        r = requests.get('https://api.genius.com/artists/16775/songs',
                         auth='')


# !/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import numpy as np
import sys
import re
import urllib.request, urllib.error, urllib.parse
import json
import csv
import codecs
import os
import socket
from bs4 import BeautifulSoup
from socket import AF_INET, SOCK_DGRAM


def load_credentials():
    lines = [line.rstrip('\n') for line in open('credentials.txt')]
    chars_to_strip = " \'\""
    for line in lines:
        if "client_id" in line:
            client_id = re.findall(r'[\"\']([^\"\']*)[\"\']', line)[0]
        if "client_secret" in line:
            client_secret = re.findall(r'[\"\']([^\"\']*)[\"\']', line)[0]
        # Currently only need access token to run, the other two perhaps for future implementation
        if "client_access_token" in line:
            client_access_token = re.findall(r'[\"\']([^\"\']*)[\"\']', line)[0]
    return client_id, client_secret, client_access_token


def setup(search_term):
    imp.reload(
        sys)  # dirty (but quick) way to deal with character encoding issues in Python2; if writing for Python3, should remove
    #sys.setdefaultencoding('utf8')
    if not os.path.exists("output/"):
        os.makedirs("output/")
    outputfilename = "output/output-" + re.sub(r"[^A-Za-z]+", '', search_term) + ".csv"
    with codecs.open(outputfilename, 'ab', encoding='utf8') as outputfile:
        outwriter = csv.writer(outputfile)
        if os.stat(outputfilename).st_size == 0:
            header = ["page", "id", "title", "url", "path", "header_image_url", "annotation_count", "pyongs_count",
                      "primaryartist_id", "primaryartist_name", "primaryartist_url", "primaryartist_imageurl"]
            outwriter.writerow(header)
            return outputfilename
        else:
            return outputfilename


def search(search_term, outputfilename, client_access_token):
    songids = []
    primaryID = -1
    with codecs.open(outputfilename, 'ab', encoding='utf8') as outputfile:
        outwriter = csv.writer(outputfile)
        # Unfortunately, looks like it maxes out at 50 pages (approximately 1,000 results), roughly the same number of results as displayed on web front end
        page = 1
        while page <= 2:
            querystring = "http://api.genius.com/search?q=" + urllib.parse.quote(search_term) + "&page=" + str(page)
            request = urllib.request.Request(querystring)
            request.add_header("Authorization", "Bearer " + client_access_token)
            request.add_header("User-Agent",
                               "curl/7.9.8 (i686-pc-linux-gnu) libcurl 7.9.8 (OpenSSL 0.9.6b) (ipv6 enabled)")  # Must include user agent of some sort, otherwise 403 returned
            while True:
                try:
                    response = urllib.request.urlopen(request,
                                               timeout=10)  # timeout set to 4 seconds; automatically retries if times out
                    raw = response.read()
                except socket.timeout:
                    print("Timeout raised and caught")
                    continue
                break
            json_obj = json.loads(raw)
            body = json_obj["response"]["hits"]

            num_hits = len(body)
            if num_hits == 0:
                if page == 1:
                    print(("No results for: " + search_term))
                break
            print(("page {0}; num hits {1}".format(page, num_hits)))

            for r, result in enumerate(body):
                result_id = result["result"]["id"]
                title = result["result"]["title"]
                url = result["result"]["url"]
                path = result["result"]["path"]
                header_image_url = result["result"]["header_image_url"]
                annotation_count = result["result"]["annotation_count"]
                pyongs_count = result["result"]["pyongs_count"]
                primaryartist_id = result["result"]["primary_artist"]["id"]
                primaryartist_name = result["result"]["primary_artist"]["name"]
                primaryartist_url = result["result"]["primary_artist"]["url"]
                primaryartist_imageurl = result["result"]["primary_artist"]["image_url"]
                row = [page, result_id, title, url, path, header_image_url, annotation_count, pyongs_count,
                       primaryartist_id, primaryartist_name, primaryartist_url, primaryartist_imageurl]
                outwriter.writerow(row)  # write as CSV
                if r == 1: # r == 1 is the first index of actual artist
                    primaryID = primaryartist_id
                if int(primaryartist_id) == primaryID:
                    songids = songids + [str(result_id)]
                    # if r == 1 and page == 1: # to look for a specific entry
                    #    print("*********here is the ID: {}".format(result_id))
                    #    songids = songids + [str(result_id)]
            page += 1
    return songids


def searchSongs(songids, client_access_token):
    page = 0
    lyricsAll = []
    wordList = []
    wordMatrix = np.array([])
    numWords = 0
    prevWord = ''
    for n, songid in enumerate(songids):
        print('Done with song {} out of {}'.format(n, len(songids)))
        querystring = "http://api.genius.com/songs/" + songid
        request = urllib.request.Request(querystring)
        request.add_header("Authorization", "Bearer " + client_access_token)
        request.add_header("User-Agent",
                           "curl/7.9.8 (i686-pc-linux-gnu) libcurl 7.9.8 (OpenSSL 0.9.6b) (ipv6 enabled)")  # Must include user agent of some sort, otherwise 403 returned
        while True:
            try:
                response = urllib.request.urlopen(request,
                                                  timeout=10)  # timeout set to 4 seconds; automatically retries if times out
                raw = response.read()
            except socket.timeout:
                print("Timeout raised and caught")
                continue
            break
        json_obj = json.loads(raw)
        path = json_obj["response"]["song"]["path"]

        page_url = "http://genius.com" + path
        page = requests.get(page_url)
        htmlFile = BeautifulSoup(page.text, "html.parser")

        [h.extract() for h in htmlFile('script')]
        lyrics = htmlFile.find("div", "lyrics").get_text()
        #lyrics = htmlFile.find('div', classmethod='lyrics').get_text()
        #print(lyrics)
        lyricsAll = lyrics
        for word in lyrics.split():
            if word[0] is not '[': #if word a section header
                #print(word)
                if word not in wordList:
                    numWords += 1
                    wordList = wordList + [word]
                    if numWords == 1:
                        wordMatrix = np.zeros(shape=(1, 1))
                    else:
                        prevWordMatrix = wordMatrix
                        wordMatrix = np.zeros(shap1e=(numWords, numWords))
                        wordMatrix[:-1, :-1] = prevWordMatrix
                        wordMatrix[wordList.index(prevWord), -1] += 1
                else:
                    wordMatrix[wordList.index(prevWord), wordList.index(word)] += 1
                prevWord = word
                #input("next line?")

    return wordList, wordMatrix

def main():
    #arguments = sys.argv[1:]  # so you can input searches from command line if you want
    search_term = 'Travis Scott'
    outputfilename = setup(search_term)
    client_id, client_secret, client_access_token = load_credentials()
    songids = search(search_term, outputfilename, client_access_token)
    #print(songids)
    #print((len(songids)))
    wordList, wordMatrix = searchSongs(songids, client_access_token)
    #print(wordMatrix)
    numWords = len(wordList)
    numGenerate = 20
    while True:
        index = np.random.randint(0, numWords)
        generatedLyrics = [wordList[index]]
        for i in range(numGenerate):
            nextIndex = np.argmax(wordMatrix[index, :])
            generatedLyrics = generatedLyrics + [wordList[nextIndex]]
            index = nextIndex

        # print(generatedLyrics)
        counter = 0
        for word in generatedLyrics:
            sys.stdout.write(word + ' ')
            counter += 1
            if counter == 5:
                print() #newline
                counter = 0
        print()
        input('Generate next verse')


if __name__ == '__main__':
    main()