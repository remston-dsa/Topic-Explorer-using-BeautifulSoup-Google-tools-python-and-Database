from explorer import *
from seo import *

# get query from user
main_query=input("Enter your Query: \n")

# get links for main query
links, search_query=fetch_links(main_query,num_of_links=50)
links=links[:20]
# print(links)


#get top related queries
query_top_ls=related_queries(main_query, query_type='top', num_queries=5)
print(query_top_ls)
print(len(query_top_ls))


#get rising related queries
query_rise_ls=related_queries(main_query, query_type='rising', num_queries=5)
print(query_rise_ls)
print(len(query_rise_ls))


# combine two list
related_queries=list(set(query_top_ls+query_rise_ls))
print(related_queries)

related_queries_links={}
for query in related_queries:
    related_queries_links[query],_=fetch_links(query,5)
    
print(related_queries_links)

