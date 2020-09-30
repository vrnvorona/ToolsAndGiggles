import requests
import time
import re

counter = 0
counter1 = 0
counter2 = 0
items1 = []
items2 = []
for i in range(49, 164):
    time.sleep(5)
    r = requests.get(f'https://upstage.rivegauche.ru/rg/v1/newRG/products/search?currentPage={i}&pageSize=100')

    r_json = r.json()

    results = r_json['results']
    # found = False
    for item in results:
        temp = requests.get(f'https://upstage.rivegauche.ru/rg/v1/newRG/products/{item["code"]}')
        temp_json = temp.json()

        try:
            code = temp_json['code']
        except KeyError:
            print(f'Wtf {temp_json["code"]}')
            break




        try:
            price = temp_json['price']
            price_card = price['priceGroupCode']
        except KeyError:
            price_card = None

        try:
            prices = temp_json['prices']
            cards = [x['priceGroupCode'] for x in prices]
        except KeyError:
            cards = []

        # if price_card in cards:
        #     print(f'{item["code"]} with price {price_card} and prices {cards}')

        if price_card == 'yellowPriceGroup' and 'yellowPriceGroup' not in cards:
            print(f'{item["code"].ljust(11, " ")} with yellowPriceGroup in price but not in {cards}')
            counter1 += 1
            items1.append([item["code"], price_card, cards])

        elif price_card != 'yellowPriceGroup' and 'yellowPriceGroup' in cards:
            print(f'{item["code"].ljust(11, " ")} without yellowPriceGroup in price but in {cards}')
            counter2 += 1
            items2.append([item["code"], price_card, cards])
        counter += 1
        # try:
        #     variants = temp_json['variantOptions']
        # except KeyError:
        #     variants = None
        # try:
        #     type_of_variant = temp_json['variantAttributeType']
        #     print(f'{item["code"]} with attr "{type_of_variant}"')
        #     if item['prices']:
        #         print(f'{item["code"]} with {item["prices"]}')
        #     # if type_of_variant not in ['color', 'volume', 'Volume ', 'Volume', 'volume ']:
        #     #     found = True
        #     #     print(f'WTF {type_of_variant} is this')
        #     #     break
        # except KeyError:
        #     pass
    # if found:
    #     break
    print(f'{i}/163')
