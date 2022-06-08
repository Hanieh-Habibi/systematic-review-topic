

import requests
from bs4 import BeautifulSoup

import BackEnd.functions.PDF_download as pdf 
from BackEnd.functions.filter_article import split_search_term

import datetime
from DataBase.models import *
from BackEnd.functions.Remove_references import *
from threading import Thread

def get_search_term(search):
    """we translate the search to a readable string search for the api"""
    split,_ = split_search_term(search)
    search_term = ''
    for c in split:
        search_term += c
        search_term += "+"
    
    return search_term

def get_max_article(search,begin,end):

    year_begin = str(begin.year)
    month_begin = str(begin.month)
    day_begin = str(begin.day)

    year_end = str(end.year)
    month_end = str(end.month)
    day_end = str(end.day)

    search_term = get_search_term(search)
    api_query = 'https://www.medrxiv.org/search/'
    query_base = api_query + search_term + f"+limit_from:{year_begin}-{month_begin}-{day_begin}+limit_to:{year_end}-{month_end}-{day_end}+"
    
    first_page_query = query_base
    text = requests.get(first_page_query).text
    soup = BeautifulSoup(text, 'html.parser')
    last_str = soup.select_one('li.pager-last.last.odd a').string    
    num_pages = int(last_str)

    article_by_page=10
    return article_by_page * num_pages

def extract_id(search_term,begin,end):

    year_begin = str(begin.year)
    month_begin = str(begin.month)
    day_begin = str(begin.day)

    year_end = str(end.year)
    month_end = str(end.month)
    day_end = str(end.day)

    api_query = 'https://www.medrxiv.org/search/'
    query_base = api_query + search_term  + f"+limit_from:{year_begin}-{month_begin}-{day_begin}+limit_to:{year_end}-{month_end}-{day_end}+"
    
    id = []
    metadata ={}
    
    first_page_query = query_base
    try:
        text = requests.get(first_page_query).text
    except:
        return [],{}
    
    soup = BeautifulSoup(text, 'html.parser')
    last_str = soup.select_one('li.pager-last.last.odd a').string
    num_pages = int(last_str)

    for i in range(num_pages):

        query = query_base if i == 0 else query_base + '?page=' + str(i)
        try:
            text = requests.get(query).text
        except:
            continue

        soup = BeautifulSoup(text, 'html.parser')
        entries = soup.select('div.highwire-article-citation')

        for entry in entries:
            entry_id = entry['data-pisa']
            id.append(entry_id)
            metadata[entry_id] = entry

    return id,metadata


def extract_article(entry_id_list,entry,research):
    """ input: a list of entry_id, the dictionnary with all entry and the research.
        For each id, we write the article and all data in our database"""
    
    for entry_id in entry_id_list:

        doi_url = str(entry[entry_id].select_one(".highwire-cite-metadata-doi").contents[1]).strip()
        doi = doi_url.replace("https://doi.org/", "")

        #we check if article exists already
        a = Article.objects.filter(doi = doi)
        if a.exists():
            Research_Article.objects.create(research=research,article=a[0])
            continue

        authors_list = []
        for author_html in entry[entry_id].select(".highwire-citation-author"):
            
            try:
                first_name = author_html.select_one(".nlm-given-names").string
                last_name = author_html.select_one(".nlm-surname").string
                authors_list.append((last_name,first_name))
            except:
                continue

        date_str = entry[entry_id].select_one(".highwire-cite-metadata-pages").string[0:10]
        publication = ''
        try:
            publication = datetime.datetime.strptime(date_str,"%Y.%m.%d").date()
        except:
            publication = datetime.date(1900,1,1)

        title_sel = entry[entry_id].select_one('.highwire-cite-linked-title')
        title = title_sel.text
        abstract_url = "https://www.medrxiv.org" + title_sel["href"]
        url = abstract_url + ".full.pdf"

        abstract = ''
        try:
            abstract_page = requests.get(abstract_url).text
            soup = BeautifulSoup(abstract_page, 'html.parser')
            sel = soup.select_one('div#abstract-1 p').text
            abstract =  sel
        except:
            abstract = ''
            
        #we write the article
        article = Article.objects.filter(doi = doi)
        is_file_get = False
        if article.exists():
            article = article[0]
        else:
            article = Article.objects.create(title=title,doi=doi,abstract=abstract,full_text=full_text,publication=publication,url_file=url)
            try:
                name = "article_{id}_{title}"
                if len(article.title) <= 30:
                    name = name.format(id=str(article.id),title=article.title[0:].replace(" ","_"))
                else:
                    name = name.format(id=str(article.id),title=article.title[0:30].replace(" ","_"))
                full_text = pdf.extract_full_text(url,"research_"+str(research.id) + "_id_" + str(entry_id))
                full_text = remove_references(full_text)
                is_file_get = True
            except:
                full_text = ""
            article.full_text = full_text.replace("\x00", "\uFFFD")
            article.is_file_get = is_file_get
            article.save()

        # we bond the article to the research
        Research_Article.objects.create(research=research,article=article)

        # we write the authors and bind to the article
        for author in authors_list:
            
            a = Author.objects.filter(last_name = author[0],first_name = author[1])
            if a.exists():
                author = a[0]
            else:
                author = Author.objects.create(last_name=author[0],first_name=author[1])
            Article_Author.objects.create(article=article,author=author)


def get_article( search, research,begin,end, number_thread=1):
    """ we get the article and write them in database. The process is parallelized"""

    search_term = get_search_term(search)
    id, entry = extract_id(search_term,begin,end)
    total = str(len(id))

    #we distribute the job to each thread
    list_job = []
    for i in range(number_thread):
        list_job.append([])
    
    for i in range(len(id)):
        current_thread = i % number_thread
        list_job[current_thread].append(id[i])
    
    #we create the threads
    list_thread = []
    for i in range(number_thread):
        list_thread.append(Thread(target=extract_article,args=(list_job[i],entry,research)))
    
    # we start the threads and wait they finish
    for thread in list_thread:
        thread.start()
    for thread in list_thread:
        thread.join()