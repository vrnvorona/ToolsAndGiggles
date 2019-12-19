import json
import codecs

temp = []

data = json.load(codecs.open('/Users/voronin/PycharmProjects/TaskParser/codebeautify.json', 'r', 'utf-8-sig'))
for city in data:
  temp1 = [city["city"], city["region"]]
  if temp1 not in temp:
    temp.append(temp1)
  else:
    print(city["city"])
  if city["city"][-1:] in list('{}()[].,:;+-*/&|<>=~'):
    print(city["city"])
  if city["region"][-1:] in list('{}()[].,:;+-*/&|<>=~'):
    print(city["region"])

