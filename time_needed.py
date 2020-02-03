import datetime

def tn(time_string, h = 0, m = 0):
    temp = 0
    floats = [float(x) for x in time_string.split()]
    for item in floats:
        temp += 8 - item
    temp -= (h+m/60)
    result = datetime.timedelta(hours=abs(temp))
    if temp > 0:
        print(f"Underworked {result}")
    elif temp < 0:
        print(f"Overworked {result}")
    elif temp == 0:
        print("You worked as much as you needed")
