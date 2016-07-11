__author__ = 'saba.teserra'


from math import log, exp
import re
import editdistance as distance




#data source, pulled from snowplow
file_name = "../data/job_search_cookies-10000-31.txt" #parameters cookies (file_name, 3,0,2)
#file_name = "../data/job_search-6411_part_00.txt" #parameters cookies (file_name, 3,1,2)

#output files
search_stream = open("../data/searches_by_id.txt", 'w')
volume_stream = open("../data/search_volume_per_id", 'w')


""" 1. compiles searches made by a given id (ip, session, or cookies or a combination of them) and stores them in a file
    2. compiles how many times a query term has been used overall and stores it in a file

    This is a batch process. The output files will be used to make a decision on what the suggested query terms are for a given query.
    A batch process since we do not want to generate the files whenever we want to get suggested search terms for each new search """

#parameters, one can use different columns as id depending on the data obtained from the data source beginning from 0
#you may also define how many records of the file to use, trade of on how big of data - for maximizing precision or speed. I used 200k here
def get_search(file_name, num_columns, id_index, search_term_index):
    search_by_id ={}
    search_volume ={}
    with open(file_name) as f:
        counter = 0
        for line in f.readlines():
            counter += 1
            arr = line.lower().split('|')
            if len(arr) ==num_columns and arr[search_term_index].strip()!='':
                key_word = re.sub('title:\(|\)|\(|\"','', arr[search_term_index].strip()).strip()
                id = arr[id_index]
                if id not in search_by_id:
                    search_by_id[id] =[key_word]
                    search_volume[id] = 1
                else:
                    search_volume[id] += 1
                    lis = search_by_id[id]
                    if key_word not in lis:
                        lis.append(key_word)
                        search_by_id[id] = lis
                if counter > 200000:
                    break
    for key, value in search_by_id.iteritems():
        search_stream.write(key +'|' + str[value] +'\n')

    for key, value in search_volume.iteritems():
        volume_stream.write(key +'|' + str[value] + '\n')

    search_stream.close()
    volume_stream.close()
    return search_by_id, search_volume


searches, volume = get_search(file_name, 3,0,2) # used cookies here

