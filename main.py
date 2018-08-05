from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt

OK_STATUS = 200
URL = 'https://en.wikipedia.org/wiki/List_of_countries_by_future_population_(United_Nations,_medium_fertility_variant)'


def parse_url(url):
    try:
        with closing(get(url, stream=True)) as response:
            content = response.headers['Content-Type'].lower()
            if (response.status_code == OK_STATUS) \
                    and (content is not None) and (content.find('html') > -1):
                return response.content
            else:
                return None
    except RequestException as re:
        print('Error during requests to {} : {}'.format(url, str(re)))


raw_html_doc = parse_url(URL)
soup = BeautifulSoup(raw_html_doc, 'html.parser')

print(soup.title.string)
print('__________________________________________________________________________________________')

table = soup.find_all('table', attrs={'class': 'wikitable'})
tbody = table[1].find('tbody')
rows = tbody.find_all('tr')

# convert a string representation of numbers (with commas) into numbers
def get_num(str):
    return int(str.replace(',', ''))


population_list = []

for row in rows:
    dummy_dict = {}

    first_td = row.find('td')
    if first_td is not None:
        col = first_td.find('a')
        dummy_dict['country'] = col.text

    tds = row.findAll('td')
    if len(tds) > 0:
        dummy_dict['2020'] = get_num(tds[1].text)
        dummy_dict['2030'] = get_num(tds[2].text)
        dummy_dict['2040'] = get_num(tds[3].text)
        dummy_dict['2050'] = get_num(tds[4].text)
        dummy_dict['2060'] = get_num(tds[5].text)
        dummy_dict['2070'] = get_num(tds[6].text)
        dummy_dict['2080'] = get_num(tds[7].text)
        dummy_dict['2090'] = get_num(tds[8].text)
        dummy_dict['2100'] = get_num(tds[9].text.split('\n')[0])
        population_list.append(dummy_dict)


# create dataframe
df = pd.DataFrame(population_list)

index1 = df.index[df.country == 'India']
index2 = df.index[df.country == 'United States']
index3 = df.index[df.country == 'United Kingdom']

r_index = index1.tolist()
r_index.extend(index2.tolist())
r_index.extend(index3.tolist())

ndf = df.iloc[r_index, :]
ndf.set_index('country', inplace=True)

X = ndf.columns.values
y_india = list(ndf.iloc[0, :])
y_usa = list(ndf.iloc[1, :])
y_uk = list(ndf.iloc[2, :])

# plot bar graphs to compare
plt.bar(X, y_india, width=0.2, color='r', align='center')
plt.bar(X, y_usa, width=0.4, color='g', align='center')
plt.bar(X, y_uk, width=0.8, color='b', align='center')
plt.xlabel('Years')
plt.ylabel('Population (in thousands)')
plt.title('List of countries by future population (United Nations)')
plt.legend()
plt.show()



