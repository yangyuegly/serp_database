# 01.06.2019
# extraction.py
# Code to extract elements from SERPs
# Author: Khonzoda Umarova

from bs4 import BeautifulSoup
import os
import json
import urllib.parse
from urllib.parse import urlparse
from bs4 import BeautifulSoup as BS


def find_rc(soup):
    """A function to find "rc" elements (i.e. ordinary search results)"""
    lst = soup.find_all('div', attrs={"class":"rc"})
    if len(lst)==0:
        return None

    sites = []
    for elt in lst:
        try:
            #class r is just url and title
            url = elt.find("h3", attrs={"class":"r"}).find("a").get("href")
            title = elt.find("h3", attrs={"class":"r"}).get_text()

        except:
            url = elt.find("div", attrs={"class":"r"}).find("a").get("href")
            title = elt.find("div", attrs={"class":"r"}).find("h3", attrs={"class":"LC20lb"}).get_text()


        snippet1 = elt.find("div", attrs={"class":"s"}) #text from page
        snippet2 = elt.find("div", attrs={"class":"P1usbc"}) #extra text

        #we're grabbing one or the other or showing missing message
        if snippet1 != None and snippet1.find("span", attrs={"class":"st"}) != None:
            snippet = snippet1.find("span", attrs={"class":"st"}).get_text()
        elif snippet2 != None:
            snippet = snippet2.get_text()
        else:
            snippet = ""
            print("------------")
            print("MISSING snippet -", url, title)
            print("------------")

        sites.append((urllib.parse.urlparse(url).netloc.lower(), title, snippet))

    return sites

def get_results_dct(directory):
    """
    Given a directory with htmls extracts results from each one
    and returns an output in the form of a dictionary:
    {source1: [result1, result2, result3, ...],
     source2: [...]
     ....
    }
    """
    os.chdir(directory)

    # We go one NID (class element) after another to maintain the order of elements on SERP
    serpDct = {}
    lst = [elt for elt in os.listdir(directory) if elt[0] != '.'] #why the hidden files??? creates a list of all html files
    count = 0
    for html in lst:
        #get the name of the news source
        source = html.split(".html")[0] #filename
 
        results = []

        with open(html) as f:
            html_doc = f.read()

        #load html into bs4
        soup = BeautifulSoup(html_doc, 'html.parser') #soupify the page
        basic_elts = soup.find_all("div", attrs={"class":"bkWMgd"}) #elements that give the basic layout of your page
        #includes panels with results related/similar to the search query

        other_elts = soup.find_all("div", attrs={"class":"sV2QOc"}) #other elements that are related to your search result

        for nid in basic_elts:
#             try:
                #extract needed information about nid element
                heading = nid.find("div", attrs={"class":"e2BEnf"}) #not sure what this does?
                text = nid.get_text()
                #Checks if this is a People also ask for box
                if "People also ask" in text:
                    results.append("People also ask")
                elif "Featured snippet from the web" in text:
                    results.append("Featured snippet")
                #check whether it is a panel that contains ordinary search results (which are links)
                elif find_rc(nid) != None:
                    links = find_rc(nid)
                    results += links
                elif heading != None:
                    title = heading.get_text()
                    if "Top stories" in title:
                        #Checks for Top stories panel
                        results.append("Top stories")
                    elif "Latest" in title:
                        #Checks for Latest stories panel
                        results.append("Latest stories")
                    elif "Images for" in title:
                        #Checks for Images panel
                        results.append("Images")
                    elif "Videos" in title:
                        #Checks for Videos panel
                        results.append("Videos")
                    elif "Twitter" in text:
                        #Checks for Twitter boxes
                        results.append("Twitter")
#                         print "found twitter", source
                    else:
                        print ("something else", source)
                elif nid.find("h2", attrs={"class":"bNg8Rb"}) != None\
                and "Twitter" in nid.find("h2", attrs={"class":"bNg8Rb"}).get_text():
                    #Checks for type 2 Twitter boxes
                    results.append("Twitter")
                elif nid.find("img", attrs={"id":"lu_map"}) != None:
                    #Checks for Maps
                    results.append("Maps")
                elif nid.find("div", attrs={"id":"sports-app"}) != None:
                    #Checks for Sports info boards
                    results.append("Sports app")
                elif nid.find("div", attrs={"id":"dictionary-modules"}) != None:
                    #Checks for Dictionary sections
                    results.append("Dictionary")
                elif nid.find("div", attrs={"class":"FGpTBd"}) != None:
                    #Check for Video Featured Snippet
                    section = nid.find("div", attrs={"class":"FGpTBd"})
                    site = urlparse(section.find("a").get("href")).netloc.lower()
                    results.append(("Video", site))
#                     print ("video snippet", site)
                elif nid.find("div", attrs={"class":"kp-blk"}) != None:
                    #Checks for Dictionary sections
                    results.append("Sport games")
#                     print ("sport games")
                else:
                    #some pages have empty "bkWMgd" divs
                    print ("Neither", source)

        for panel in other_elts:
            #Searches for other elements like
            results.append(panel.get_text())
#             except:
#                 print "ERROR:", source
        serpDct[source] = results
        count += 1
        if count%10 == 0:
            print(count)
    return serpDct

def extractKPInformation(html):
    """Finds the Knowledge Panel section in a SERP and extracts some fields
    of information from it, if they exist. Returns a dictionary with the results.
    """

    # initialize fields to empty, to have a value for all
    name, url, catName, descText, descUrl, more = "", "", "", "", "", {}

    # get the KP block
    kpBlk = html.find(class_='knowledge-panel')

    # if it exists, extract fields that we want
    if kpBlk:
        try:
            name = kpBlk.find(class_='kno-ecr-pt').find('span').text
        except:
            pass
        try:
            url = kpBlk.find(class_='B1uW2d')['href']
        except:
            pass
        try:
            catBlock = kpBlk.find(class_='wwUB2c')
            if catBlock == None:
                #special cases when category is missed
                catBlock = kpBlk.find_all(class_='YhemCb')[-1]
            catName = catBlock.text
        except:
            pass
        try:
            desc = kpBlk.find(class_='kno-rdesc')
            descText = desc.span.text
        except:
            pass

        try:
            descUrl = kpBlk.find(class_='kno-rdesc').find('a')['href']
        except:
            pass
        try:
            keys = kpBlk.findAll(class_='w8qArf')
            keys = [k.text for k in keys]
            values = kpBlk.findAll(class_='LrzXr')
            values = [v.text for v in values]
            # more = dict(zip(keys, values))
        except:
            pass
            
        return {'name': name, 'url': url, 'category': catName,
                'description': descText, 'descURL': descUrl, 'more': more}
    else:
        return {}


def getKPFromFolder(path):
    """Call 'extractKPInformation' for all files in a folder.
    """
    files = [f for f in os.listdir(path) if f.endswith('html')]
    dictKPs = {}

    for f in sorted(files):
        try:
            html = BS(open(os.path.join(path, f)), "html5lib")
        except:
            print("Couldn't open {}".format(f))

        #continue
        try:
            result = extractKPInformation(html)
            if result:
                dictKPs[f] = result
        except:
            print("coudln't extract from {}".format(f))

    print("total with KPs:", len(dictKPs))

    return dictKPs

if __name__ == "__main__":
   "bob.html".split(".html")[0]
