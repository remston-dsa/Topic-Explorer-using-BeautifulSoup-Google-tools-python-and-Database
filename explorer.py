import requests
from bs4 import BeautifulSoup
from re import search
import unicodedata
import pandas as pd
from multiprocessing import Pool
from seo import *


# ...




i=0






def get_head(link):   
    
    Topics = {}
    h1_new = []
    h2_new = []
    h3_new = []
    
    Topics = {}
    
    

    
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    request = requests.get(link, headers=headers)
    
    Soup = BeautifulSoup(request.text, 'lxml')


    a = []
    b = []
    c = []


    h1_tags = ["h1"]

    for tags in Soup.find_all(h1_tags):
        a.append(tags.text.strip())

    h2_tags = ["h2"]

    for tags in Soup.find_all(h2_tags):
        b.append(tags.text.strip())

    h3_tags = ["h3"]

    for tags in Soup.find_all(h3_tags):
        c.append(tags.text.strip())

    h1 = []
    [h1.append(x) for x in a if x not in h1]

    h2 = []
    [h2.append(x) for x in b if x not in h2]

    h3 = []
    [h3.append(x) for x in c if x not in h3]


    if len(h1) ==0:
        message = ""
        h1_new.append(message)
    else:
        for sub in h1:
            string_encode = unicodedata.normalize("NFKD", sub)
            h1_new.append(string_encode)

    if len(h2) ==0:
        message = ""
        h2_new.append(message)
    else:
        for sub in h2:
            string_encode = unicodedata.normalize("NFKD", sub)
            h2_new.append(string_encode)

    if len(h3) ==0:
        message = ""
        h3_new.append(message)
    else:
        for sub in h3:
            string_encode = unicodedata.normalize("NFKD", sub)
            h3_new.append(string_encode)

    L = [['Heading 1', h1_new], ['Heading 2', h2_new], ['Heading 3',h3_new]]    
    Topics[link] = L
        
    return Topics
        
def excel_maker(main_dict, search_query, links):

    H1_Headings = []
    H2_Headings = []
    H3_Headings = []

    Mega_list1 = []
    Mega_list2 = []
    Mega_list3 = []

    r_l=related_queries(search_query)
    t_l=related_topics(search_query)
    
    for keys, values in main_dict.items():
        H1_Headings.append(values[0][1])
        H2_Headings.append(values[1][1])
        H3_Headings.append(values[2][1])
    
    


    for keys, values in main_dict.items():
        H1_Headings.append(values[0][1])
        H2_Headings.append(values[1][1])
        H3_Headings.append(values[2][1])


                
    for i in H1_Headings:
        for j in i:
            Mega_list1.append(j)  
            
    for i in H2_Headings:
        for j in i:
            Mega_list2.append(j)   

    for i in H3_Headings:
        for j in i:
            Mega_list3.append(j)    
            
    res1 = []
    res2 = []
    res3 = []

    for i in Mega_list1:
        if i not in res1:
            res1.append(i)

    for i in Mega_list2:
        if i not in res2:
            res2.append(i)
            
    for i in Mega_list3:
        if i not in res3:
            res3.append(i)        

            
    if len(res1) >= len(res2) and len(res1) >= len(res3):
        for i in range(len(res1)-len(res2)):
            res2.append('[]')
        for i in range(len(res1)-len(res3)):
            res3.append('[]')
            
    if len(res2) >= len(res1) and len(res2) >= len(res3):
        for i in range(len(res2)-len(res1)):
            res1.append('[]')
        for i in range(len(res2)-len(res3)):
            res3.append('[]')

    if len(res3) >= len(res1) and len(res3) >= len(res2):
        for i in range(len(res3)-len(res1)):
            res1.append('[]')
        for i in range(len(res3)-len(res2)):
            res2.append('[]')     
            
    res1 = list(filter(None, res1))
    res2 = list(filter(None, res2))
    res3 = list(filter(None, res3))
    
    
    ls = []
    for i in links:
        ls.append(search_query)
    data_tuples = list(zip(ls,links,H1_Headings,H2_Headings,H3_Headings))
    df1 = pd.DataFrame(data_tuples, columns=['Search_query','URL','H1_Headings','H2_Headings','H3_Headings'])
    df1
    
    import people_also_ask
    list1 = []
    for question in people_also_ask.get_related_questions(search_query):
        list1.append(question)  
    data_tuples = list(zip(ls,list1))
    df2 = pd.DataFrame(data_tuples, columns=['Search_query','People_also_asked'])
    df2
    
    list_final = []
    for i in res1:
        list_final.append(search_query)
    data_tuples = list(zip(list_final,res1,res2,res3))
    df3 = pd.DataFrame(data_tuples, columns=['Search_query','Unique H1_Headings','Unique H2_Headings','Unique H3_Headings'])
    df3
    
    filename = "%s.xlsx" % search_query
    
    with pd.ExcelWriter(filename, engine='xlsxwriter') as writer:
        df1.to_excel(writer, sheet_name='Headings Tab', index=False)
        df2.to_excel(writer, sheet_name='People_also_asked Tab', index=False) 
        df3.to_excel(writer, sheet_name='Unique Topics Tab', index=False)
        
    return H1_Headings,H2_Headings,H3_Headings,list1


