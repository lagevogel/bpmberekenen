import requests
import json
from datetime import date
from datetime import datetime

idLine = '<div id="li-'
endLine = '<span class="cldf-summary-seller-contact-zip-city">'

priceLine = '<span class="cldt-price sc-font-xl sc-font-bold" data-item-name="price">'
dataLine = '<ul data-item-name="vehicle-details">'
transmissionLine = '<li data-type="transmission-type">'
emissionLine = "CO2/km"

carList = []

afschrijfTabel = {}

class Audi:
    '''
    Initialize class with the data given
    '''
    def __init__(self, nr, guid, price, distance, transmission, horsepower, date, emission):
        self.nr = nr
        self.guid = guid
        self.price = price.split(" ")[1][:-2].replace(".", "")
        self.distance = distance.split(" ")[0].replace(".", "")
        self.transmission = transmission
        self.horsepower = horsepower.split(" ")[2][1:]
        self.date = date
        self.emission = emission.split(" ")[0]
        self.bpm = self.calculateBPM(self.date, self.emission)

    def __str__(self):
        return (f"Car #{self.nr} with id {self.guid} has a price of {self.price} with {self.distance} kilometers run\n This car is from {self.date}, has {self.horsepower} HP and is an {self.transmission} with {self.emission} g CO2/km")

    def to_dict(self):
        return {"nr": self.nr,
                "id": self.guid,
                "price": self.price,
                "distance": self.distance,
                "transmission": self.transmission,
                "horsepower": self.horsepower,
                "date": self.date,
                "emission": self.emission,
                "BPM": self.bpm}

    def calculateBPM(self, date, emission):
        try:
            dateMonth = date.split("/")[0]
            dateYear = date.split("/")[1]
            
            bpmList = []
            totalMonths = diff_month(datetime.now(), datetime(int(dateYear), int(dateMonth), 1))

            emission = int(emission.strip())

            if int(dateYear) <= 2014:
                if 0 <= emission <= 88:
                    bpmList.append(calculateBPMmoney(0, 0, emission, 0))
                elif 89 <= emission <= 124:
                    bpmList.append(calculateBPMmoney(0, 89, emission, 105))
                elif 125 <= emission <= 182:
                    bpmList.append(calculateBPMmoney(3780, 125, emission, 126))
                elif 183 <= emission <= 203:
                    bpmList.append(calculateBPMmoney(11088, 183, emission, 237))
                elif 204 <= emission <= 999:
                    bpmList.append(calculateBPMmoney(16065, 204, emission, 474))

            if int(dateYear) <= 2015:
                if 0 <= emission <= 82:
                    bpmList.append(calculateBPMmoney(175, 0, emission, 6))
                elif 83 <= emission <= 110:
                    bpmList.append(calculateBPMmoney(667, 83, emission, 69))
                elif 111 <= emission <= 160:
                    bpmList.append(calculateBPMmoney(2599, 111, emission, 112))
                elif 161 <= emission <= 180:
                    bpmList.append(calculateBPMmoney(8199, 161, emission, 217))
                elif 181 <= emission <= 999:
                    bpmList.append(calculateBPMmoney(12539, 181, emission, 434))

            if int(dateYear) <= 2016:
                if 0 <= emission <= 79:
                    bpmList.append(calculateBPMmoney(175, 0, emission, 6))
                elif 80 <= emission <= 106:
                    bpmList.append(calculateBPMmoney(649, 80, emission, 69))
                elif 107 <= emission <= 155:
                    bpmList.append(calculateBPMmoney(2512, 107, emission, 124))
                elif 156 <= emission <= 174:
                    bpmList.append(calculateBPMmoney(8588, 156, emission, 239))
                elif 175 <= emission <= 999:
                    bpmList.append(calculateBPMmoney(13129, 175, emission, 478))

            if int(dateYear) <= 2017:
                if 0 <= emission <= 76:
                    bpmList.append(calculateBPMmoney(353, 0, emission, 2))
                elif 77 <= emission <= 102:
                    bpmList.append(calculateBPMmoney(505, 77, emission, 66))
                elif 103 <= emission <= 150:
                    bpmList.append(calculateBPMmoney(2221, 103, emission, 145))
                elif 151 <= emission <= 168:
                    bpmList.append(calculateBPMmoney(9181, 151, emission, 238))
                elif 169 <= emission <= 999:
                    bpmList.append(calculateBPMmoney(13465, 169, emission, 475))

            if int(dateYear) <= 2018:
                if 0 <= emission <= 73:
                    bpmList.append(calculateBPMmoney(356, 0, emission, 2))
                elif 74 <= emission <= 98:
                    bpmList.append(calculateBPMmoney(502, 74, emission, 63))
                elif 99 <= emission <= 144:
                    bpmList.append(calculateBPMmoney(2077, 99, emission, 139))
                elif 145 <= emission <= 162:
                    bpmList.append(calculateBPMmoney(8471, 145, emission, 229))
                elif 163 <= emission <= 999:
                    bpmList.append(calculateBPMmoney(12593, 163, emission, 458))

            if int(dateYear) <= 2019:
                if 0 <= emission <= 71:
                    bpmList.append(calculateBPMmoney(360, 0, emission, 2))
                elif 72 <= emission <= 95:
                    bpmList.append(calculateBPMmoney(502, 72, emission, 60))
                elif 96 <= emission <= 139:
                    bpmList.append(calculateBPMmoney(1942, 96, emission, 131))
                elif 140 <= emission <= 156:
                    bpmList.append(calculateBPMmoney(7706, 140, emission, 215))
                elif 157 <= emission <= 999:
                    bpmList.append(calculateBPMmoney(11361, 157, emission, 429))


            discount = float(afschrijfTabel[totalMonths])


            return min(bpmList) * (discount/100)

        except Exception as e:
            print(str(e))
            return "-"


def diff_month(d1, d2):
    return (d1.year - d2.year) * 12 + d1.month - d2.month

def calculateBPMmoney(startPrice, left, emission, price):
    return startPrice + (emission - left) * price

def getdatafrompage(text, carNumber):

    atLeastOnce = False
    counter = 0
    addCarData = False

    carNr = carNumber
    carId = "n/a"
    carPrice = "n/a"
    carDistance = "n/a"
    carTransmission = "n/a"
    carHorsePower = "n/a"
    carDate = "n/a"

    linesSplit = text.splitlines()

    for i in range(0, len(linesSplit)):
        line = linesSplit[i]
        if idLine in line:
            atLeastOnce = True
            carId = line.split('"')[1][3:]
            #print(f'{carId} on line {counter}')
        if priceLine in line:
            carPrice = linesSplit[i+1]
        if dataLine in line:
            carDistance = linesSplit[i+2]
            carDate = linesSplit[i+5]
            carHorsePower = linesSplit[i+8]
        if transmissionLine in line:
            carTransmission = linesSplit[i+1]
            if carTransmission == "Schaltgetriebe":
                carTransmission = "Manual"
            if carTransmission == "Automatik":
                carTransmission = "Automatic"
        if emissionLine in line:
            carEmission = line
            carNr += 1
            carList.append(Audi(carNr, carId, carPrice, carDistance, carTransmission, carHorsePower, carDate, carEmission))

        # if endLine in line:
        #     carList.append(Audi(carNr, carId, carPrice, carDistance, carTransmission, carHorsePower, carDate))
        #     carNr += 1
        counter += 1

    if atLeastOnce:
        return True
    else:
        return False


with open("afschrijftabel.txt","r") as f:
    for line in f.readlines():
        newLine = line.split(";")
        afschrijfTabel[int(newLine[0].strip())] = newLine[1]

price = 26000
for page in range(1, 100):
    link = f"https://www.autoscout24.de/lst/audi/tt?sort=standard&desc=0&ustate=N%2CU&size=20&page={page}&powerfrom=165&powertype=hp&cy=D&priceto={price}&kmto=150000&fregfrom=2014&atype=C&"
    #link = f"https://www.autoscout24.de/lst/ford/mustang?sort=standard&desc=0&ustate=N%2CU&size=20&page={page}&cy=D&fregfrom=2014&atype=C&"
    f = requests.get(link)

    text = f.text
    currentCarNr = (page-1) * 20
    if not getdatafrompage(text, currentCarNr):
        break

for car in carList:
    print(car)

results = [obj.to_dict() for obj in carList]
jsdata = json.dumps(results)

today = date.today()
fileName = today.strftime("%d-%m-%Y")
with open(f'jsondata_{fileName}.json', 'w') as outfile:
    json.dump(results, outfile)


#print(carList)