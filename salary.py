from bs4 import BeautifulSoup
import math
import urllib.request

#change to input
def salary_and_qol(province, occupation):

    qol = {
        "Calgary, Alberta" : "180.88 (Very High)",
        "Vancouver, British Columbia": "174.45 (Very High)",
        "Winnipeg, Manitoba": "147.11 (High)",
        "Saint John, New Brunswick": "134.32 (Moderate)",
        "St.John's, Newfoundland and Labrador": "154.13 (High)",
        "Halifax, Nova Scotia": "168.99 (Very High)",
        "Toronto, Ontario": "154.83 (High)",
        "Montreal, Quebec": "158.82 (High)",
        "Regina, Saskatchewan": "150.16 (High)"
    }

    url = f'https://ca.indeed.com/career/{occupation}/salaries/{province}'

    #html_text = requests.get(url).text
    html_text = urllib.request.urlopen(url)
    print('done')
    soup = BeautifulSoup(html_text, 'lxml')

    salary = soup.find('span', class_="sal-agg-nonbase__average-salary-value")
    #print(salary.string)replace('-', ' ')
    occupation = occupation.capitalize()
    def normalize_names(string):
        string = string.replace('-', ' ')
        string = string.title()
        return string


    if math.floor(float(salary.string[1:].replace(',', ''))) > 10000:
        salary_value = f'{salary.string[1:]} CAD per year'
    else:
        salary_value = f'{salary.string[1:]} CAD per hour'

    
    province_ = normalize_names(province)
    
    #print(f'Average salary: {salary_value}')
    qol_province_list = qol.keys()
    

    for q in qol_province_list:
        province__ = province_.lower()
        if province__.lower() in q.lower():
            #print(f'\nQuality of life rating in {q}: {qol[q]}')
            qol_value = qol[q]
    
    
    return [salary_value, qol_value]
