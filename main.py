from bs4 import BeautifulSoup
import requests
from requests import get
import json
import re

transaction = []
location = []
url1 = []
type_t = []
data_t = []
location_id = [500, 600, 1000]
url = 'https://nekretninecrikvenica.net'
json_loc = []
page = requests.get(url)
soup = BeautifulSoup(page.text, "html.parser")
all_type = soup.select('div.ct-u-marginBottom20 > div.ct-u-displayTableCell > div.ct-form--item > select#id_transaction option')
for g in all_type:
    transaction.append(g.attrs["value"])
#print(transaction)

loc_html = str(soup.select('script:contains(ignore_diacritics)'))
pattern_json = r'data\:\[(.+)\]'
pattern_loc = r'name\"\:\"(.+)\"'
json_loc = str(re.findall(pattern_json, loc_html))
jsds = json_loc.split('},{')
#print(jsds)

for l in jsds:
    loca = str(re.findall(pattern_loc, l))
    loca = loca.replace("['", "")
    loca = loca.replace("']", "")
    loca = loca.replace(',', '%2C')
    loca = loca.replace(' ', '+')
    loca = loca.replace("\\\\\\", '')
    location.append(loca)
#print(location)

for i in transaction:
    for j in location:
        url1 = ('https://nekretninecrikvenica.net/listings/results?id_transaction=' + str(i) + '&location=' + str(j))
        if str(i) == '1':
            type_t= ('sale_strict')
        else:
            type_t= ('rent_strict')
        data = {
            "url": url1,
            "meta":
                {
                    "type": type_t,
                    "location_id": location_id
                }
        }
        data_t.append(data)

dats = {
"source":
    {
    "urls":data_t
    }
        }
#for h in data_t:
    #print(h)

def gen_js(name, source):
    with open(name, 'w') as json_file:
        json.dump(source, json_file, indent=4)

gen_js('links1.json', data_t)
gen_js('links2.json', dats)
