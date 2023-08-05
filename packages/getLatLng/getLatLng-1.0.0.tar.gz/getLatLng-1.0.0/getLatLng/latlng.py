
import requests
import csv
from time import sleep


def getLatLngList(listOfCity):

	cities = listOfCity
	cities = [cities[i:i+2] for i in range(0,len(cities),2)]
	out = []
	citiesNotFound = []
	# print cities

	for city in cities:
		
		for c in city:
			result = []


			response = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address='+c)

			resp_json_payload = response.json()

			try:
				output = resp_json_payload['results'][0]['geometry']['location']
				result.append(c)
				result.append(output['lat'])
				result.append(output['lng'])
				out.append(result)
				
			except Exception, e:
				print "city",city
				citiesNotFound.append(c)
				# print str(e)

		sleep(1)

	return out


def getLatLngDict(listOfCity):

	cities = listOfCity
	cities = [cities[i:i+2] for i in range(0,len(cities),2)]
	out = []
	# print cities
	for city in cities:
		
		for c in city:
			result = {}


			response = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address='+c)

			resp_json_payload = response.json()

			try:
				output = resp_json_payload['results'][0]['geometry']['location']
				result['City']= c
				result['latitude'] = output['lat']
				result['longitude']= output['lng']
				out.append(result)
				
			except Exception, e:
				print "city",city
				citiesNotFound.append(c)				
				# print str(e)

		sleep(1)

	return out


# 	print state
# 	sleep(1)



# with open('worked.csv', "wb") as f:
#     writer = csv.writer(f, delimiter=',')
#     for line in data:
#     	writer.writerow(line)
