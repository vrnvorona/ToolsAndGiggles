import json
import codecs
import openpyxl

filename = "2020-02-06-geo"
# filename = "no_dupes"
data = json.load(codecs.open(f'/Users/voronin/ToolsAndGiggles/{filename}.json', 'r', 'utf-8-sig'))

def deletion():
  for_removal = []
  while True:
    temp = []
    temp2 = []
    for city in data:
      temp1 = [city["city"], city["region"]]
      if temp1 not in temp:
        temp.append(temp1)
      else:
        print(temp1)
        temp2.append(city)
        data.pop(data.index(city))
        break
    if not temp2:
      break

  file = codecs.open(f'/Users/voronin/ToolsAndGiggles/{filename}_no_dupes.json', 'w', 'utf-8-sig')
  json.dump(data, file, ensure_ascii=False)
  file.close()

def cities_parse():
  temp = []
  i = 0
  for city in data:
    temp1 = [city["city"], city["region"]]
    if temp1 not in temp:
      temp.append(temp1)
    else:
      print(temp1)
      i+=1
  print(i)


def coord_parse(zeroes = 0):
  temp = []
  used = []
  i = 0
  for city in data:
    temp2 = [city["city"], city["region"]]
    temp3 =  [city["lat"], city["lon"]]
    if temp3 == ['0.0', '0.0']:
      # print(temp2)
      # print(temp3)
      # i+=1
      pass
    elif temp3 not in temp:
      temp.append(temp3)
    else:
      if zeroes == 0:
        if temp3 not in used:
          print("---------------")
          print(temp3)
          for city1 in data:
            temp31 = [city1["lat"], city1["lon"]]
            temp32 = [city1["city"], city1["region"]]
            if temp31 == temp3:
              print(temp32)
          used.append(temp3)
        i+=1
  print("---------------")
  print(i)
  # symbols
  # for i in range(1, 30):
  #   try:
  #     if city["city"][-i] in list('{}()[].,:;+-*/&|<>=~'):
  #       # print("---SYMBOLS IN CITY---")
  #       print(city["city"])
  #     if city["region"][-i] in list('{}()[].,:;+-*/&|<>=~'):
  #       # print("---SYMBOLS IN REGION---")
  #       print(city["region"])
  #   except IndexError:
  #     pass
#
# for removal in for_removal[::-1]:
#   data.pop(removal)


# reading xsls file
def xlsx_reader(file):
  temp = []
  wb = openpyxl.load_workbook(filename=f"/Users/voronin/Downloads/{file}.xlsx")
  sheet_ranges = wb['все']
  for i in range(1, 600000):
    if sheet_ranges[f'A{i}'].value is None:
      break
    temp1 = [sheet_ranges[f'A{i}'].value, sheet_ranges[f'B{i}'].value, sheet_ranges[f'C{i}'].value]
    temp.append(temp1)
  return temp


def ratio_checker(xlsx):
  for city in data:
    if city["isIncreasedRatio"]:
      temp1 = [city["city"], city["region"]]
      if temp1 not in xlsx:
        print (temp1)

def xlsx_diff(file1, file2):
  first = xlsx_reader(file1)
  second = xlsx_reader(file2)
  added = []
  removed = []
  # added
  for item1 in second:
    if item1 not in first:
      added.append(item1)
  # removed
  for item2 in first:
    if item2 not in second:
      removed.append(item2)

  print("------REMOVED------")
  for removee in removed:
    print(removee)
  print("-------ADDED-------")
  for add in added:
    print(add)
  print("-------------------")


def json_diff(json1, json2):
  json11 = json.load(codecs.open(f'/Users/voronin/Downloads/{json1}.json', 'r', 'utf-8-sig'))
  json21 = json.load(codecs.open(f'/Users/voronin/Downloads/{json2}.json', 'r', 'utf-8-sig'))
  added = []
  removed = []
  # added
  for item1 in json21:
    if item1 not in json11:
      added.append(item1)
  # removed
  for item2 in json11:
    if item2 not in json21:
      removed.append(item2)
  print("------REMOVED------")
  for removee in removed:
    print(removee)
  print("-------ADDED-------")
  for add in added:
    print(add)
  print("-------------------")
