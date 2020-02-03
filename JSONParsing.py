import json
import codecs
import openpyxl


data = json.load(codecs.open('/Users/voronin/ToolsAndGiggles/geo.json-20-01-29-ratio.json', 'r', 'utf-8-sig'))


# for_removal = []
# while True:
#   temp = []
#   temp2 = []
#   for city in data:
#     temp1 = [city["city"], city["region"]]
#     if temp1 not in temp:
#       temp.append(temp1)
#     else:
#       print(temp1)
#       temp2.append(city)
#       data.pop(data.index(city))
#       break
#   if not temp2:
#     break
#
# file = codecs.open('/Users/voronin/ToolsAndGiggles/no_dupes.json', 'w', 'utf-8-sig')
# json.dump(data, file, ensure_ascii=False)
# file.close()

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
def xlsx_reader():
  temp = []
  wb = openpyxl.load_workbook(filename="/Users/voronin/Downloads/2.xlsx")
  sheet_ranges = wb['Лист1']
  for i in range(1, 105):
    temp1 = [sheet_ranges[f'B{i}'].value, sheet_ranges[f'A{i}'].value]
    temp.append(temp1)
  return temp


def ratio_checker(xlsx):
  for city in data:
    if city["isIncreasedRatio"]:
      temp1 = [city["city"], city["region"]]
      if temp1 not in xlsx:
        print (temp1)