#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import print_function
from builtins import str
from downloader.universal import main as FileDownloader
import re
import sys
import cfscrape
import os
from bs4 import BeautifulSoup
import logging


def readcomic_Url_Check(input_url, current_directory, logger):
    if logger == "True":
        logging.basicConfig(format='%(levelname)s: %(message)s', filename="Error Log.log", level=logging.DEBUG)

    Issue_Regex = re.compile('https?://(?P<host>[^/]+)/Comic/(?P<comic>[\d\w-]+)(?:/Issue-)?(?P<issue>\d+)?')
    Annual_Regex = re.compile('https?://(?P<host>[^/]+)/Comic/(?P<comic>[\d\w-]+)(?:/Annual-)?(?P<issue>\d+)?')
    lines = input_url.split('\n')
    for line in lines:
        found = re.search(Issue_Regex, line)
        if found:
            match = found.groupdict()
            if match['issue']:
                Edited_Url = str(input_url) + '?&readType=1'
                url = str(Edited_Url)
                Single_Issue(url, current_directory, logger)

            else:
                url = str(input_url)
                Whole_Series(url, current_directory, logger)

        found = re.search(Annual_Regex, line)
        if found:
            match = found.groupdict()

            if match['issue']:
                Edited_Url = str(input_url) + '?&readType=1'
                url = str(Edited_Url)
                Single_Issue(url, current_directory, logger)
            else:
                print()
                'Uh, please check the link'

        if not found:
            print()
            'Please Check Your URL one again!'
            sys.exit()

def Single_Issue(url, current_directory, logger):

    scraper = cfscrape.create_scraper()
    connection = scraper.get(url).content

    Series_Name_Splitter = url.split('/')
    Series_Name = str(Series_Name_Splitter[4]).replace('-', ' ')
    Issue_Number_Splitter = str(Series_Name_Splitter[5])
    Issue_Or_Annual_Split = str(Issue_Number_Splitter).split("?")
    Issue_Or_Annual = str(Issue_Or_Annual_Split[0]).replace("-", " ").strip()
    reg = re.findall(r'[(\d)]+', Issue_Number_Splitter)

    Issue_Number = str(reg[0])

    Raw_File_Directory = str(Series_Name) + '/' + "Chapter " + str(Issue_Or_Annual)

    File_Directory = re.sub('[^A-Za-z0-9\-\.\'\#\/ ]+', '',
                            Raw_File_Directory)  # Fix for "Special Characters" in The series name

    Directory_path = os.path.normpath(File_Directory)

    print('\n')
    print('{:^80}'.format('=====================================================================\n'))
    print('{:^80}'.format('%s - %s') % (Series_Name, Issue_Or_Annual))
    print('{:^80}'.format('=====================================================================\n'))

    linksList = re.findall('lstImages.push\(\"(.*?)\"\)\;', str(connection))
    logging.debug("Image Links : %s" % linksList)

    for link in linksList:
        if not os.path.exists(File_Directory):
            os.makedirs(File_Directory)
        fileName = str(linksList.index(link)) + ".jpg"
        # logging.debug("Name of File : %s" % fileName)
        FileDownloader(fileName, Directory_path, link, logger)

def Whole_Series(url, current_directory, logger):

    scraper = cfscrape.create_scraper()
    connection = scraper.get(url).content

    soup = BeautifulSoup(connection, "html.parser")
    # logging.debug("Soup : %s" % soup)
    all_links = soup.findAll('table', {'class': 'listing'})
    # logging.debug("Issue Links : %s" % all_links)

    for link in all_links:
        # logging.debug("link : %s" % link)
        x = link.findAll('a')
        logging.debug("Actual Link : %s" % x)
        for a in x:
            url = "http://readcomiconline.to" + a['href']
            logging.debug("Final URL : %s" % url)
            Single_Issue(url, current_directory=current_directory, logger=logger)
    print("Finished Downloading")
