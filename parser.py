import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import time
import numpy as np
import csv

#НАО - 325
#CЗАО - 1
#CAO - 5
#CBAO - 6
#TAO - 326
#ЗАО - 11
#ЦАО - 4
#BAO - 7
#ЗелАО - 151
#ЮЗАО - 10
#ЮАО - 9
#ЮВАО - 8
okruga = [325, 1, 5, 6, 326, 11, 4, 7, 151, 10, 9, 8]
def fetch_price(span_list, substring):
    for item in span_list:
        if substring in item.text:
            raw_price = item.text.strip().replace(substring, '').replace(' ', '').replace('\xa0', '')
            return int(raw_price)
    return None

res = []

def main_parser(cian_page_n, okrug):
    page_mas_28 = []
    session = requests.Session()
    headers = {'User-Agent': UserAgent().chrome}

    main_page = f'https://www.cian.ru/cat.php?deal_type=sale&district%5B0%5D={okrug}&engine_version=2&offer_type=flat&p={cian_page_n}&room1=1&room2=1&room3=1&room4=1&room5=1&room9=1&sort=creation_date_desc'
    
    main_response = session.get(main_page, headers=headers)
    if main_response.status_code == 200:
        main_response.encoding = 'utf-8'
        main_tree = BeautifulSoup(main_response.text, 'html.parser')
        offers = main_tree.find_all('a', class_='_93444fe79c--media--9P6wN')
        links = [offer['href'] for offer in offers if 'href' in offer.attrs]
        
        for offer_link in links:
            offer_mas = []
            print(offer_link)
            price = None
            price_per_sqm = None
            max_attempts = 5
            attempts = 0
            while attempts < max_attempts and (price is None or price_per_sqm is None):
                attempts += 1
                try:
                    offer_response = session.get(offer_link, headers=headers)
                    if offer_response.status_code == 200:
                        offer_response.encoding = 'utf-8'
                        offer_tree = BeautifulSoup(offer_response.text, 'html.parser')

                        price_spans = offer_tree.find_all('span', class_='a10a3f92e9--color_black_100--Ephi7 a10a3f92e9--lineHeight_9u--limEs a10a3f92e9--fontWeight_bold--BbhnX a10a3f92e9--fontSize_28px--P1gR4 a10a3f92e9--display_block--KYb25 a10a3f92e9--text--e4SBY')
                        price_per_sqm_spans = offer_tree.find_all('span', class_='a10a3f92e9--color_black_100--Ephi7 a10a3f92e9--lineHeight_5u--e6Sug a10a3f92e9--fontWeight_normal--JEG_c a10a3f92e9--fontSize_14px--reQMB a10a3f92e9--display_block--KYb25 a10a3f92e9--text--e4SBY a10a3f92e9--text_letterSpacing__0--cQxU5 a10a3f92e9--text_whiteSpace__nowrap--hJYYl')
                        floor_spans = offer_tree.find_all('span', class_='a10a3f92e9--color_black_100--Ephi7 a10a3f92e9--lineHeight_6u--cedXD a10a3f92e9--fontWeight_bold--BbhnX a10a3f92e9--fontSize_16px--QNYmt a10a3f92e9--display_block--KYb25 a10a3f92e9--text--e4SBY')
                        loc = offer_tree.find_all('a', class_='a10a3f92e9--address--SMU25')
                        age = offer_tree.find_all('span', class_='a10a3f92e9--color_black_100--Ephi7 a10a3f92e9--lineHeight_6u--cedXD a10a3f92e9--fontWeight_bold--BbhnX a10a3f92e9--fontSize_16px--QNYmt a10a3f92e9--display_block--KYb25 a10a3f92e9--text--e4SBY')
                        transport = offer_tree.find('span', class_='a10a3f92e9--underground_time--YvrcI')
                        transport_times = []
                        try:
                            for item in transport:
                                transport_times.append(item)
                        except:
                            pass

                        for item in age:
                            if len(item.text) == 4 and item.text.isnumeric() == True:
                                building_age = item.text

                        loc_inf = []
                        for item in loc:
                            loc_inf.append(item.text.strip())


                        if price is None:
                            price = fetch_price(price_spans, '₽')
                        if price_per_sqm is None:
                            price_per_sqm = fetch_price(price_per_sqm_spans, '₽/м²')
                        for item in floor_spans:
                            if 'из' in item.text:
                                floor = item.text.strip().replace('из', '').split(' ')
                                offer_floor = floor[0]
                                try:
                                    overall_floor = floor[2]
                                except:
                                    pass
                                

                        title = offer_tree.find('h1', class_='a10a3f92e9--title--vlZwT').text.strip()
                        if title[10] != 'А' and title[10] != 'С':
                            try:
                                n_rooms = int(title[10])
                            except:
                                pass
                        else:
                            n_rooms = 0
                        tip = False
                        isapart = title[18:26]
                        sq = (title[title.find(',')+2:].replace(' м²', '').replace(',', '.'))
                        
                        if isapart != 'квартира':
                            tip = True
                       
                        offer_mas.append(offer_link) 
                        offer_mas.append(price) 
                        offer_mas.append(price_per_sqm)
                        offer_mas.append(sq)
                        offer_mas.append(offer_floor)
                        offer_mas.append(overall_floor)
                        offer_mas.append(n_rooms)
                        offer_mas.append(tip)
                        try:
                            offer_mas.append(building_age)
                        except:
                            pass
                        try:
                            offer_mas.append(transport_times[1].replace(' мин.', ''))
                        except:
                            pass
                        offer_mas.append(loc_inf[1])
                        offer_mas.append(loc_inf[2])
                    else:
                        print(f"Ошибка {offer_response.status_code}, попытка {attempts}...")
                except requests.RequestException as e:
                    print(f"Ошибка запроса: {e}, попытка {attempts}...")
                

            if price is None or price_per_sqm is None:
                print("Не удалось получить всю информацию после 5 попыток")
            page_mas_28.append(offer_mas)
        return(page_mas_28)
    else:
        print(main_response.status_code)
for okrug in okruga:
    for page in range(1,55):
        res.append(main_parser(page, okrug))

final_result = []
try:
    for sub_array in res:
        for sub_sub_array in sub_array:
            final_result.append(sub_sub_array)
except:
    pass
  
fields = ['Link', 'Price', 'Price per m2', 'Square', 'Floor', 'Floors', 'Rooms', 'Is Apartment?', 'Year', 'Time to metro', 'Okrug', 'District']
with open('cian_offers.csv', 'w', newline='') as csvfile:
    fieldnames = fields
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for i in range(len(final_result)):
        try:
            writer.writerow({fields[0]: final_result[i][0], fields[1]: final_result[i][1], fields[2]: final_result[i][2], fields[3]: final_result[i][3], fields[4]: final_result[i][4], fields[5]: final_result[i][5], fields[6]: final_result[i][6], fields[7]: final_result[i][7], fields[8]: final_result[i][8], fields[9]: final_result[i][9], fields[10]: final_result[i][10], fields[11]: final_result[i][11]})
        except:
            pass  
#resulting file - cian_offers.csv with approximately 7700 entries
