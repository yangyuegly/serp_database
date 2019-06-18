"""queries and links tables"""
from link import Link
from query import Query

import sqlite3

conn = sqlite3.connect('serp_data.db')

c = conn.cursor()
c.execute("ALTER TABLE queries ADD id int")

#---------create tables---------------
#no date datatype avaliable, thus stored date as text  "YYYY-MM-DD HH:MM:SS.SSS"

#c.execute("""CREATE TABLE queries(
#    start_date text, 
#    end_date text,
#    num_of_obs int,
#    category text
#)""")

#no boolean type available, stored as 0/1
#c.execute("""CREATE TABLE links(
#    query text,
#    date text,
#    time text,
#    link_name text,
#    domain_name text,
#    position int,
#    movement int,
#    is_news int
#)""")

#----------define functions to update table------------------

#Insert a new query to queries table
def insert_query(q): 
    with conn:
        c.execute("""INSERT INTO queries VALUES(:id, :start_date, :end_date, :num_of_obs, :category)""",
        {'id': q.id,'start_date':q.start_date, 'end_date':q.end_date,'num_of_obs':q.num_of_obs,'category':q.category})


#Insert a new link to links table
def insert_link(l): 
    with conn:
        c.execute("""INSERT INTO links VALUES(:query, :date, :time, :link_name, :domain_name, :position, :movement, :is_news)""",
        {'query':l.query, 'date':l.date,'time':l.time,'link_name':l.link_name,'domain_name':l.domain_name,'position':l.position,'movement':l.movement,'is_news':l.is_news})


#update the number of observations given the query and 
def update_obs(q, num):
    with conn:
        c.execute("UPDATE queries SET num_of_obs= :num_of_obs WHERE id=:id",{'num_of_obs':num, 'id':q.id})


conn.close()