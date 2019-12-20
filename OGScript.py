import xlrd
import openpyxl
from collections import OrderedDict
import simplejson as json
import requests
import sys
import time
from xml.etree import ElementTree
import argparse
from argparse import RawTextHelpFormatter

#command-line arguments handler
parser = argparse.ArgumentParser(description='.xlsx to .json parser.\nFormat of .xlsx should be:\n\nРегион | Населённый пункт | Субъект РФ | Loyalty | Healthy Club\n  str  |       str        |     str    |  bool   |     bool\n\nFormat of master .json should be:\n\n\n\n\n[\n    {\n        "region": "str",\n        "city": "str",\n        "isLoyaltyAvailable": bool,\n        "lat": "str",\n        "lon": "str",\n        "isHealthyClubAvailable": bool\n    },\n\n    ...\n\n    {\n        ...\n    }\n]', formatter_class=RawTextHelpFormatter)
parser.add_argument("-x", "--xlsx", nargs=1, help="name of xlsx file to be parsed", action='store', type=argparse.FileType('r'))
parser.add_argument("-j", "--json", nargs="+", help="names of master json and 'donor' json; can be used simultaniuosly with -x to create donor from .xlsx(only master .json name required)", action='store',  type=argparse.FileType('r'))
parser.add_argument("-m", "--mode", nargs=1, help="mode for -j (default is merge):\nl - update loyalty\nh - update heathclub\nn - add new cities\nm - full merge", action='store', type=str, default='m')
args = parser.parse_args()

#List of junk in city names
removal_list = [" ж/д_ст", " г", " пгт", " ст-ца", " сл"," ст", " рп", " п", " им", " c/c", "с/с ", "с/о", " сл", " т", " дп", "д. ", " д", " мкр", "аул", " х", " с", " т-ца", " кв-л", " нп", " тер", " кп", " м"]

#Get coordinates
def locate(region, city):
    key = '55661af4-6e41-410b-bc0a-266aad439920'
    location = '{} {}'.format(region, city)
    api_request = 'https://geocode-maps.yandex.ru/1.x/?apikey={}&geocode={}'.format(key, location)
    time.sleep(0.5)
    responce = requests.get(api_request)
    root = ElementTree.fromstring(responce.content)
    for child in root.iter('*'):
        if child.tag == '{http://www.opengis.net/gml}pos':
            return child.text
    return '0.0 0.0'

#Update loyalty in master .json
def json_update_loyatly(master, donor):
    for i in master:
        for j in donor:
            if i['region'] == j['region'] and i['city'] == j['city']:
                print('Updating loyalty {} {}'.format(i['region'], i['city']))
                i['isLoyaltyAvailable'] = j['isLoyaltyAvailable']
                break

#Update heathyclub in master .json
def json_update_heath(master, donor):
    for i in master:
        for j in donor:
            if i['region'] == j['region'] and i['city'] == j['city']:
                print('Updating HealthClub {} {} '.format(i['region'], i['city']))
                i['isHealthyClubAvailable'] = j['isHealthyClubAvailable']
                break

#Full merge master and donor .json, donor .json values will replace master .json corresponding values
def json_merge(master, donor):
    for i in donor:
        for j in master:
            if i['region'] == j['region'] and i['city'] == j['city']:
                print('Updating {} {}'.format(i['region'], i['city']))
                j.update(i)
                break
        else:
            print('Adding {} {}'.format(i['region'], i['city']))
            master.append(i)

#Add new cities in master .json
def json_add_new(master, donor):
    for i in donor:
        for j in master:
            if i['region'] == j['region'] and i['city'] == j['city']:
                break
        else:
            print('Adding {} {}'.format(i['region'], i['city']))
            master.append(i)

#Parse .xlsx to .json, format of .xlsx should be:
#Регион | Населённый пункт | Субъект РФ | Loyalty | HealthyClub
#  str  |       str        |     str    |  bool   |     bool
def xlsx_parser(xlsx_file):
    # Open the workbook and select the first worksheet
    try:
        wb = openpyxl.load_workbook(xlsx_file)
    except Exception as e:
        print("File doesn't exist")
        sys.exit(0)
    #Start parsing
    for sheetname in wb.sheetnames:
        data_list = []
        sheet = wb[sheetname]
        for row in sheet:
            if row[0].value == 'Регион':
                continue
            else:
                try:
                    data = OrderedDict()
                    data['region'] = row[2].value
                    city =  row[1].value
                    data['isLoyaltyAvailable'] = bool(row[3].value)
                    print('Parsing {} {}'.format(row[2].value, city))
                    coord = locate(row[2].value, row[1].value)
                    for word in removal_list:
                        city = city.replace(word, "")
                    data['city'] = city
                    data['lat'] = coord.split()[1]
                    data ['lon'] = coord.split()[0]
                    data['isHealthyClubAvailable'] = bool(row[4].value)
                    data_list.append(data)
                except Exception as e:
                    print(e)
                    pass
        # Serialize the list of dicts to JSON
        j = json.dumps(data_list, ensure_ascii=False)
    # Write to file
    with open('{}json'.format(xlsx_file.replace('xlsx', '')), 'w', encoding='utf8') as outfile:
        outfile.write(j)

#Edit master .json
def json_editor(master_file, donor_file):
    if (master_file and donor_file):
        with open(master_file, 'r', encoding='utf8') as masterjson:
            master = json.load(masterjson)
            masterjson.close()
        with open(donor_file, 'r', encoding='utf8') as donorjson:
            donor = json.load(donorjson)
            donorjson.close()
        if args.mode[0] == 'n':
            json_add_new(master, donor)
        elif args.mode[0] == 'm':
            json_merge(master, donor)
        elif args.mode[0] == 'l':
            json_update_loyatly(master, donor)
        elif args.mode[0] == 'h':
            json_update_heath(master, donor)
        j = json.dumps(master, ensure_ascii=False)
        with open('{}_{}'.format(time.strftime("%d%m%Y"), master_file), 'w', encoding='utf8') as outfile:
            outfile.write(j)

if (args.xlsx == None and args.json == None): #no args
    parser.print_usage()
    sys.exit(0)
elif(args.xlsx != None and args.json == None): #only .xlsx
    xlsx_parser(args.xlsx[0].name)
    sys.exit(0)
elif(args.xlsx == None and args.json != None): #only .json
    try:
        json_editor(args.json[0].name, args.json[1].name)
        sys.exit(0)
    except Exception as e:
        if e.args[0] == 'list index out of range':
            print('Donor .json is missing!')
        sys.exit(0)
elif(args.xlsx != None and args.json != None): #.xlsx to json
    xlsx_parser(args.xlsx[0].name)
    json_editor(args.json[0].name, args.xlsx[0].name.replace('xlsx', 'json'))
    sys.exit(0)