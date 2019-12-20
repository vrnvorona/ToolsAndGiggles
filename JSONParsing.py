import json
import codecs
import openpyxl


data = json.load(codecs.open('/Users/voronin/ToolsAndGiggles/geo_new.json', 'r', 'utf-8-sig'))

# duplicates
temp = []
for_removal = []
for city in data:
  temp1 = [city["city"], city["region"]]
  if temp1 not in temp:
    temp.append(temp1)
  else:
    print(temp1)
    for_removal.append(data.index(city))

for removal in for_removal[::-1]:
  data.pop(removal)
  # symbols
  # if city["city"][-1:] in list('{}()[].,:;+-*/&|<>=~'):
  #   print("---SYMBOLS IN CITY---")
  #   print(city["city"])
  # if city["region"][-1:] in list('{}()[].,:;+-*/&|<>=~'):
  #   print("---SYMBOLS IN REGION---")
  #   print(city["region"])

# reading xsls file
# wb = openpyxl.load_workbook(filename="/Users/voronin/Downloads/geo.xlsx")
# sheet_ranges = wb['что необходимо удалить']
# for i in range(2, 250):
#   temp1 = [sheet_ranges[f'A{i}'].value, sheet_ranges[f'B{i}'].value]
#   temp.append(temp1)
#   print(sheet_ranges['A2'].value)

# marking deleting cities as false, change to true if needed to reverse
# for deletion in temp:
#   for item in data:
#     if item["city"] == deletion[0] and item ["region"] == deletion[1]:
#       item["isLoyaltyAvailable"] = "false"
#       item["isHealthyClubAvailable"] = "false"

# write data to new json
file = codecs.open('/Users/voronin/ToolsAndGiggles/geo_new.json', 'w', 'utf-8-sig')
json.dump(data, file, ensure_ascii=False)
file.close()