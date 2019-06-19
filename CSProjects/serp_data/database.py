"""queries and links tables"""
from link import Link
from query import Query
from extraction import *
import importlib
import sqlite3



conn = sqlite3.connect('serp_data.db')

c = conn.cursor()
#conn.commit()
#---------create tables---------------
#no date datatype avaliable, thus stored date as text  "YYYY-MM-DD HH:MM:SS.SSS"

#c.execute("""CREATE TABLE queries(
#    start_date text, 
#    end_date text,
#   num_of_obs int,
#    category text,
#    query_text text
#)""")
#c.execute("DROP TABLE links")
#no boolean type available, stored as 0/1
#c.execute("""CREATE TABLE links(
#    query text,
#   date text,
#    time text,
#    link_name text,
#    domain_name text,
#    position int,
#    movement int,
#    is_news int,
#    page int,
#    title text
#)""")
#conn.commit()

#----------define functions to update table------------------

#Insert a new query to queries table
def insert_query(q): 
    with conn:
        c.execute("""INSERT INTO queries VALUES(:start_date, :end_date, :num_of_obs, :category, :query_text)""",
        {'start_date':q.start_date, 'end_date':q.end_date,'num_of_obs':q.num_of_obs,'category':q.category,'query_text':q.query_text})


#Insert a new link to links table
def insert_link(l): 
    with conn:
        c.execute("""INSERT INTO links VALUES(:query, :date, :time, :link_name, :domain_name, :position, :movement, :is_news, :page,:title)""",
        {'query':l.query, 'date':l.date,'time':l.time,'link_name':l.link_name,'domain_name':l.domain_name,'position':l.position,'movement':l.movement,'is_news':l.is_news,'page':l.page,'title':l.title})


#update the number of observations given the query and 
def update_obs(q, num):
    with conn:
        c.execute("UPDATE queries SET num_of_obs= :num_of_obs WHERE id=:id",{'num_of_obs':num, 'id':q.id})


def get_query_by_text(query_text):
        c.execute("SELECT * FROM queries WHERE query_text=:query_text",{'query_text':query_text})
        return c.fetchall()

def get_link_by_query_date(date):
        c.execute("SELECT title FROM links WHERE date=:date",{'date':date})
        return c.fetchall()

def remove_query_by_text(query_text):
    with conn:
        c.execute("DELETE FROM queries WHERE query_text= :query_text",{'query_text':query_text})
      
#----test code-----
#q_1 = Query('2019-02-22','2019-04-25',47,'Caribbean',"Bahamas")
#insert_query(q_1)
#update_obs(q_1, 6)
#print(get_query_by_id(q_1.id))
#remove_query_by_text('Bahamas')

"""add queries in a batch with a text file containing a list of queries,
manually input start and end date, number of observations, and category"""
def batch_add_queries(query_list, start_date, end_date, obs, category):
        q_list = []
        for query_text in query_list:
                curr_query = Query(start_date,end_date,obs,category,query_text)
                insert_query(curr_query)
        
print(get_link_by_query_date('20-06-2018'))
#batch_add_queries(query_list,'19-06-2018','16-12-2018',174,'manually added queries 2018')
