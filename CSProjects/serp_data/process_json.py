import os
import pandas 
import json
from link import Link
import datetime
from datetime import datetime as dt
import urllib
from database import insert_link, get_query_by_text, get_sites_by_query, update_title


#store = os.getcwd()

"""get the list of queries"""
def getQueryList(filepath):
    with open(filepath, 'r') as inputFile: # open the file
        queryList = [line.strip() for line in inputFile]
    return queryList


"""get all the dates of files in a given directory in a sorted order
    return a sorted list of datetimes
"""
def getDateListFromDir(directory):
    dateList = [each for each in os.listdir(directory) if not isHiddenFile(each)]
    # print dateList
    return sorted(dateList, key=lambda x: datetime.datetime.strptime(x, '%d-%m-%Y'))
    
    
"""detect hidden file"""
def isHiddenFile(path):
    base = os.path.basename(path)
    return (len(base) > 0
    and base[0] == '.'
    and base != '.'
    and base != '..')


"""append to the top N url dict a list of tuples [(date, rank)] for each
    date"""
def getPosition(dateList, topNList, query):
    if topNList != None:
        for item in topNList:
            url = item['url']
            item['trend'] = []
            for date in dateList:
                try:
                    with open(os.path.join(path, date, query + ".json"), 'r') as fr:
                        ranking = json.load(fr)
                    rankList = combinePages(ranking)
                    item['trend'].append((date, getRanking(url, rankList)))
                except:
                    item['trend'].append((date, ""))
                    print ("Does not have {} on {}".format(query, date))
    return topNList


"""given a list of dictionary(a specific page in the json file), find the ranking of a given url"""
def getRanking(url, dctList):
    counter = 0
    for item in dctList:
        counter += 1
        if item['url'] == url:
            break
    return counter


def batch_insert_links(datelist,query_list):
    curr_time = '00:00:00'
    for date in datelist:
        for query in query_list:
            try:
                with open(os.path.join(query_results_directory, date, query + ".json"), 'r',encoding='utf-8') as fr:
                    all_info = json.load(fr)
                    for page_num in page_list:
                        for i in range(len(all_info[page_num])):
                            #print(date)
                            curr_url = all_info[page_num][i]['url']
                            curr_page = int(page_num[5])+1 
                            curr_domain = urllib.parse.urlparse(curr_url).netloc
                            curr_position = i + 1 
                            curr_title = all_info[page_num][i]['title']
                            curr_title = curr_title.encode('utf-8')
                            curr_link =Link(query,date,curr_time,curr_url,curr_domain,curr_position,0,0,curr_page,str(curr_title,'utf-8'))
                            insert_link(curr_link) 
            except FileNotFoundError:
                print(query+date)
                continue 
            except Exception as e:
                print(e)
                exit(0)



def update_title_batch(datelist,query_list):
    for date in datelist:
        for query in query_list:
            try:
                with open(os.path.join(query_results_directory, date, query + ".json"), 'r',encoding='utf-8') as fr:
                    all_info = json.load(fr)
                    for page_num in page_list:
                        for i in range(len(all_info[page_num])):
                            curr_url = all_info[page_num][i]['url']
                            curr_title = all_info[page_num][i]['title']
                            #print(type(curr_title))
                            curr_title = curr_title.encode('utf-8')
                            #print(curr_title)
                            update_title(curr_url,curr_title) 
            except FileNotFoundError:
                print(query+date)
                continue 
            except Exception as e:
                print(e)
                exit(0)






query_results_directory = '/Users/yueyang/Desktop/CSProjects/serp_data/manually_added-results'
filepath = '/Users/yueyang/Desktop/CSProjects/serp_data/manually_added.txt'
datelist = getDateListFromDir(query_results_directory) #get available dates from directory 
query_list = getQueryList(filepath)
page_list = ['page_'+str(i) for i in range(5)] #list of page numbers used as key to json file
#update_title_batch(datelist[5:],query_list)
#print(get_sites_by_query('Trump good'))
#batch_insert_links(datelist[4:],query_list)
#print(datelist)