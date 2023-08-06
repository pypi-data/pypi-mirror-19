import requests
from bs4 import BeautifulSoup


BASE_WEBSITE_URL = "http://www.merriam-webster.com/dictionary/"
ALPHABETS        = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n',
                    'o','p','q','r','s','t','u','v','w','x','y','z']


def find_meaning(query):
    url      = BASE_WEBSITE_URL + query
    res_flag = False
    page     = requests.get(url)
    src      = page.text
    ob       = BeautifulSoup(src, 'lxml')
    results  = []

    for info in ob.findAll('p',{'class':'definition-inner-item'}):
        word = info.text

        if word[0].isdigit():
            res_flag    = True
            sliced_data = word.split(':')

            if len(sliced_data)>1:
                if (sliced_data[1].strip()[-2]==' ') and (sliced_data[1].strip()[-1] in ALPHABETS):
                    results.append(sliced_data[1][:-2].encode('ascii','ignore').strip()) 
                else:
                    results.append(sliced_data[1].encode('ascii','ignore').strip())
        else:
            break

    if res_flag==False:
        results.append("No result found")

    return results