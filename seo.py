from googlesearch import search as gs
import people_also_ask
import pandas as pd
from pytrends.request import TrendReq
import multiprocessing
import time
import re

def isValidURL(str):
    regex = ("((http|https)://)(www.)?" +
             "[a-zA-Z0-9@:%._\\+~#?&//=]" +
             "{2,256}\\.[a-z]" +
             "{2,6}\\b([-a-zA-Z0-9@:%" +
             "._\\+~#?&//=]*)")

    p = re.compile(regex)
    if (str == None):
        return False

    if(re.search(p, str)):
        return True
    else:
        return False

# fetch 20 links for each keyword
def fetch_links(search_query,num_of_links=20):
    links=[]
    for link in gs(search_query,lang='en', num_results=num_of_links+20):
        if isValidURL(link) and link not in links:
          links.append(link)

    return links,search_query

def people_also_ask_google(search_query):
    questions=[]
    for question in people_also_ask.get_related_questions(search_query):
        questions.append(question)
    return questions, search_query

def suggest_topics(search_query):
    topics=[]
    pytrend = TrendReq()
    suggestions_dict = pytrend.suggestions(keyword=search_query)

    for topic in suggestions_dict:
        if topic['type']=='Topic':
            topics.append(topic['title'])

    return topics

def related_topics(search_query, query_type='top', num_topics=10):
    print('\n\nSome Related Topic Are...\n')
    pytrend = TrendReq()
    pytrend.build_payload([search_query], timeframe='today 5-y')
    related_topics_dict = {}
    topic_ls = pytrend.related_topics()[search_query][query_type]['topic_title'].to_list()

    for topic in topic_ls:
        related_topics_dict[topic]=people_also_ask_google(topic)
    
    return related_topics_dict

def related_queries(search_query, query_type='top', num_queries=10):
    pytrend = TrendReq()
    pytrend.build_payload([search_query], timeframe='today 5-y')
    related_queries_dict = {}
    query_ls = pytrend.related_queries()[search_query][query_type]['query'].to_list()

    return query_ls[:num_queries]

def time_it(function): 
    start = time.time()
    function
    end=time.time()
    return (end-start)
