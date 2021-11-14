from bs4 import BeautifulSoup
import requests
import re
from concurrent.futures import ThreadPoolExecutor

def top_unis(province, maxLim):
    province = province.strip().lower().replace(' ', '')
    province = province.replace('-', '')
    maxListLimit = maxLim

    base_url = "https://www.4icu.org/ca"
    base_url_links = "https://www.4icu.org"

    def url(prov):
        switcher = {
            "alberta":"/alberta/",
            "britishcolumbia":"/british-columbia/",
            "manitoba":"/manitoba/",
            "newbrunswick":"/new-brunswick/",
            "newfoundlandandlabrador":"/newfoundland-and-labrador/",
            "novascotia": "/nova-scotia/",
            "ontario": "/ontario/",
            "quebec": "/quebec/",
            "saskatchewan": "/saskatchewan/"
        }
        return switcher.get(prov, "Invalid province")

    url = base_url + url(province)
    html_text = requests.get(url).text

    soup = BeautifulSoup(html_text, 'lxml')

    def getUniLink(string, base):
        str(string)
        print(string)
        bIndex = string.find('/')
        eIndex = string.find("m")
        output = base + string[bIndex:eIndex]
        return output


    university_tags = soup.find_all('a', href=re.compile("reviews"))
    university_tags = university_tags[1:-1]
    university_names = []
    university_links = []
    for university in university_tags:
        university_names.append(university.text)
        university_links.append(base_url_links + university.get('href'))

    tuition_dict = {}
        
    def calc_top_num(maxNum):
        if len(university_names) >= maxNum:
            topNum = maxNum
        else:
            topNum = len(university_names)
        
        return topNum

    def get_tuition_costs(int):
        html_text_2 = requests.get(university_links[int]).text
        soup_2 = BeautifulSoup(html_text_2, 'lxml')
        strong_tags = soup_2.find_all('strong')
        
        def fun(ls):
            for item in ls:
                return '$' in item.string

        costs = list(filter(fun, strong_tags))
        costs = [costs[x].text for x in [0, 2]]
        domestic_tuition = costs[0]
        international_tuition = costs[1]
        tuition_dict[university_names[int]] = [domestic_tuition, international_tuition]


    def multi_get_costs(num):
        with ThreadPoolExecutor(max_workers=num) as executor:
            [executor.submit(get_tuition_costs, i) for i in range(0, num)]

    def make_tuition_lists(dict, num):
        
        domestic_list = [0] * num
        international_list = [0] * num

        def check_key_exists(dict, key):
            return key in dict.keys()
            
        for i in range(num):
            if check_key_exists(dict, university_names[i]):
                domestic_list[i] = dict[university_names[i]][0]
                international_list[i] = dict[university_names[i]][1]
                #print(f'{i+1}. {university_names[i]}')
                #print(f'Domestic Tuition (1 year): {dict[university_names[i]][0]}')
                #print(f'International Tuition (1 year): {dict[university_names[i]][1]} \n')
                
            else:
                domestic_list[i] = "Not Reported"
                international_list[i] = "Not Reported"
                #print(f'{i+1}. {university_names[i]}')
                #print(f'Domestic Tuition (1 year): Not reported')
                #print(f'International Tuition (1 year): Not reported \n')

        return [university_names, domestic_list, international_list]   
    
   

    topNum = calc_top_num(maxListLimit)

    multi_get_costs(topNum)

    

    """
    def check_key_exists(dict, key):
        return key in dict.keys()
            
    def print_output(dict, num):
        for i in range(num):
            if check_key_exists(dict, university_names[i]):
                print(f'{i+1}. {university_names[i]}')
                print(f'Domestic Tuition (1 year): {dict[university_names[i]][0]}')
                print(f'International Tuition (1 year): {dict[university_names[i]][1]} \n')
                
            else:
                print(f'{i+1}. {university_names[i]}')
                print(f'Domestic Tuition (1 year): Not reported')
                print(f'International Tuition (1 year): Not reported \n')
                
    print_output(tuition_dict, topNum)
    """
    return make_tuition_lists(tuition_dict, topNum)

        