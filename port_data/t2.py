import requests
from user_agents import agents
import random
from lxml import etree

url = 'https://www.marinetraffic.com/en/reports?asset_type=vessels&columns=flag,shipname,photo,recognized_next_port,reported_eta,reported_destination,current_port,imo,ship_type,show_on_live_map,time_of_latest_position,lat_of_latest_position,lon_of_latest_position'
response = requests.get(url=url, headers={'User-Agent': random.choice(agents)},timeout=random.randrange(100,120))
html = response.text
print(html)
# select = etree.HTML(html)
# data = select.xpath('/html/body/main/div/div/div[1]/div[6]/div[1]/div[1]/div[1]/b/text()')
# country = select.xpath('/html/body/main/div/div/div[1]/div[5]/div/div/div[1]/div[2]/span/text()')
# gk = select.xpath("/html/body/main/div/div/div[1]/div[5]/div/div/div[1]/div[1]/h1/text()")
# print(gk,country,data)
# print(data)

'https://www.marinetraffic.com/en/data/' \
'?asset_type=ports&columns=flag,portname,unlocode,photo,vessels_in_port,vessels_departures,vessels_arrivals,' \
'vessels_expected_arrivals,local_time,anchorage,geographical_area_one,geographical_area_two,coverage'

'https://www.marinetraffic.com/en/data/' \
'?asset_type=ports&columns=flag,portname,unlocode,photo,vessels_in_port,vessels_departures,vessels_arrivals,' \
'vessels_expected_arrivals,local_time,anchorage,geographical_area_one,geographical_area_two,coverage'