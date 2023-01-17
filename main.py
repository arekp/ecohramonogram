import requests
import json
from rich import print
import configparser
import csv
from model import Schedules,ScheduleDescriptions
config = configparser.ConfigParser()
config.sections()
config.read('config.ini')

proxies = {
'http': config['PROXY']['http'],
'https': config['PROXY']['http']
}

# url = "https://pluginssl.ecoharmonogram.pl/api/v1/plugin/v1/schedules?number=18&streetId=11022197"
url = config['ECOHARMONOGRAM']['UriHarmonogram']+config['ECOHARMONOGRAM']['StreetId']

payload={}
headers={}
response=requests.request("POST",url,headers=headers,data=payload,proxies=proxies)
response.encoding='utf-8-sig'

data =response.json()

typysmieci = ScheduleDescriptions(data["scheduleDescription"])
harmonogram = Schedules(data["schedulePeriod"]["startDate"],data["schedulePeriod"]["endDate"],data["schedulePeriod"]["changeDate"],data["schedules"],typysmieci)


def zapisdocsv(dane):

    # header=['Subject','Start Date','Start Time','End Date','End Time','All Day Event','Description','Location']
    header=['Subject','Start Date','Start Time','All Day Event','Description']

    with open('smieci.csv', 'w', encoding='UTF8',newline='') as f:
        writer = csv.writer(f)

        # write the header
        writer.writerow(header)
        for kal in dane:
            print(kal.getcvs())    
            if kal.getcvs() != None:
                writer.writerow(kal.getcvs())

zapisdocsv(harmonogram.harmonogram)