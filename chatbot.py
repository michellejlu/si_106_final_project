print("Booting up. One moment please.")

import aiml
import os
import requests
import json
import time 

# kernel is responsible for responding to users
kernel = aiml.Kernel()

# load every aiml file in the 'standard' directory
dirname = 'aiml_data'
filenames = [os.path.join(dirname, f) for f in os.listdir(dirname)]
aiml_filenames = [f for f in filenames if os.path.splitext(f)[1]=='.aiml']


kernel = aiml.Kernel()
for filename in aiml_filenames:
    kernel.learn(filename)


CACHE_FNAME = 'cache.json'

######### API CREDENTIALS ###############

#Google Geocoding API credentials 
Google_base = "https://maps.googleapis.com/maps/api/geocode/json"
Google_key = "AIzaSyDx49ma1zQhxf6AzJL1a7-jQJzHn9Wv0Zw"

#DarkSky API credentials
DarkSky_base = "https://api.darksky.net/forecast/"
DarkSky_key = "84216042991f8ae5b54ca7b5e5095a57"

############## CACHING ##################

try:
	cache_file = open(CACHE_FNAME, 'r')
	cache_contents = cache_file.read()
	cache_file.close()
	CACHE_DICTION = json.loads(cache_contents)
except:
	CACHE_DICTION = {}

### cache function for google geocoding API ###
def getwithCaching(base_URL, params = {}):
	req = requests.Request(method = 'GET', url = base_URL, params = sorted(params.items()))
	prepped = req.prepare()
	fullURL = prepped.url

### Check if request already exists in cache and time limit check ###

	if fullURL in CACHE_DICTION:
		if time.time() - CACHE_DICTION[fullURL]['time'] < 300:
			return json.loads(CACHE_DICTION[fullURL]['data'])
		else:
			response = requests.Session().send(prepped)
			CACHE_DICTION[fullURL] = {'time': time.time(), 'data': response.text}

		## Updated cache file
			cache_file = open(CACHE_FNAME, 'w')
			cache_file.write(json.dumps(CACHE_DICTION))
			cache_file.close()

			return json.loads(CACHE_DICTION[fullURL]['data'])

	else:
			## make the request and store the response
		response = requests.Session().send(prepped)
		CACHE_DICTION[fullURL] = {'time': time.time(), 'data': response.text}

	## Updated cache file
		cache_file = open(CACHE_FNAME, 'w')
		cache_file.write(json.dumps(CACHE_DICTION))
		cache_file.close()

		return json.loads(CACHE_DICTION[fullURL]['data'])

############## GET RESPONSE FROM CACHE ######################

## CACHE FUNCTION FOR GOOGLE GEOCODE ##
def getLatLng(city):
	try:
		data = getwithCaching(Google_base, params = {
			'key': Google_key,
			'address': city
			})
		# new_data = json.loads(data)
		lat = data['results'][0]['geometry']['location']['lat']
		lng = data['results'][0]['geometry']['location']['lng']
		return lat, lng
	except:
		return False
 
 ## CACHE FUNCTION FOR DARK SKY ##
 # use Google API to get lat, lng, and then put those numbers in Dark Sky API to get weather data
def getWeather(city):
	try:
		if getLatLng(city) == False:
			return "geocode error"
		lat, lng = getLatLng(city)
		url = DarkSky_base + DarkSky_key + "/" + str(lat) + "," + str(lng)
		weather_data = getwithCaching(url)
		return weather_data
	except:
	 	return "Is {city} a city?".format(city = city)

# add a new response for when the user says "example * and *"
# note that the ARGUMENT NAMES (first and second) must match up with
# the names in kernel.addPattern
# def exampleResponse(first, second):
#     return 'first arg is {}, second arg is {}'.format(first, second)
# kernel.addPattern("example {first} and {second}", exampleResponse)


################## EXTRACTION FROM GOOGLE GEOCODING AND DARK SKY ########################

# def Google_Geocode(city):
# 	try:
# 		googleURL = Google_base + "address=" + city + "&key=" + Google_key
# 		response = requests.get(googleURL)
# 		jsonResultGoogle = json.loads(response.text)
# 		lat = jsonResultGoogle['results'][0]['geometry']['location']['lat'] 
# 		lng = jsonResultGoogle['results'][0]['geometry']['location']['lng'] 
# 		return (lat, lng)
# 	except:
# 		return "Is {city} a city?".format(city = city)
		

# def Dark_Sky(city):
# 	Dark_Sky_URL = 0
# 	try:
# 		lat,lng = Google_Geocode(city)
# 		Dark_Sky_URL = (DarkSky_base + DarkSky_key + "/" + str(lat) + "," + str(lng))
# 		response = requests.get(Dark_Sky_URL)
# 		jsonResultDarkSky = json.loads(response.text)
# 		#temp = jsonResultDarkSky['currently']['temperature']
# 		#weather = jsonResultDarkSky['currently']['summary']
# 		return jsonResultDarkSky
# 	except:
# 		return "Sorry, I don't know"


#################### RAIN PROBABILITY ##################

def rainprob(city):
	prob = getWeather(city)['daily']['data'][0]['precipProbability']
	if prob <= 0.1:
		return "It almost definitely will not rain in " + city
	elif prob > 0.1 and prob < 0.5:
		return "It probably will not rain in " + city 
	elif prob > 0.5 and prob < 0.9:
		return "It probably will rain in " + city
	elif prob >= 0.9:
		return "It will almost definitely rain in " + city


def weekrainprob(city):
	subtract = 1.0
	weekprob = subtract - ((1.0 - (getWeather(city)['daily']['data'][0]['precipProbability']))*((1.0 - getWeather(city)['daily']['data'][1]['precipProbability']))*((1.0 - getWeather(city)['daily']['data'][2]['precipProbability']))*((1.0 - getWeather(city)['daily']['data'][3]['precipProbability']))*((1.0 - getWeather(city)['daily']['data'][4]['precipProbability']))*((1.0 - getWeather(city)['daily']['data'][5]['precipProbability']))*((1.0 - getWeather(city)['daily']['data'][6]['precipProbability'])))
	if weekprob < 0.1:
		return "It almost definitely will not rain in " + city
	elif weekprob > 0.1 and weekprob < 0.5:
		return "It probably will not rain in " + city 
	elif weekprob > 0.5 and weekprob < 0.9:
		return "It probably will rain in " + city
	elif weekprob >= 0.9:
		return "It will almost definitely rain in " + city

def week_hot_temp(city):
	web = getWeather(city)['daily']['data']
	result = [x['temperatureMax'] for x in web]
	return max(result)

def week_cold_temp(city):
	web = getWeather(city)['daily']['data']
	result = [x['temperatureMin'] for x in web]
	return min(result)
	

#################### PROMPTS ####################

### prompt 1. What's the weather like in {city}?
def prompt1(city):
	try:
		if 'geocode error' in getWeather(city):
			return "Is {city} a city?".format(city = city)
		return "{city}'s current temperature is {temp} and it is {weather}".format(city = city, temp = getWeather(city)['currently']['temperature'], weather = getWeather(city)['currently']['summary'])
	except:
		return "Sorry, I don't know."
kernel.addPattern("What's the weather like in {city}?", prompt1)

### prompt 2: Is it going to rain in {city} today?
def prompt2(city):
	try:
		if 'geocode error' in getWeather(city):
			return "Is {city} a city?".format(city = city)
		return "{prob}".format(prob = rainprob(city))
	except:
		return "Sorry, I don't know."
kernel.addPattern("Is it going to rain in {city} today?", prompt2)

### prompt 3: Is it going to rain in {city} this week?
def prompt3(city):
	try:
		if 'geocode error' in getWeather(city):
			return "Is {city} a city?".format(city = city)
		return "{weekprob}".format(weekprob = weekrainprob(city))
	except:
		return "Sorry, I don't know."
kernel.addPattern("Is it going to rain in {city} this week?", prompt3)

### prompt 4: How hot will it get in {city} today?
def prompt4(city):
	try:
		if 'geocode error' in getWeather(city):
			return "Is {city} a city?".format(city = city)
		return "The high in {city} today is {hot_temp}".format(city = city, hot_temp = getWeather(city)['daily']['data'][0]['temperatureMax'])
	except:
		return "Sorry, I don't know."
kernel.addPattern("How hot will it get in {city} today?", prompt4)

### prompt 5: How hot will it get in {city} this week?
def prompt5(city):
	try:
		if 'geocode error' in getWeather(city):
			return "Is {city} a city?".format(city = city)
		return "The high in {city} this week is {week_hot_temp}".format(city = city, week_hot_temp = week_hot_temp(city))
	except:
		return "Sorry, I don't know."	
kernel.addPattern("How hot will it get in {city} this week?", prompt5)

### prompt 6: How cold will it get in {city} today?
def prompt6(city):
	try:
		if 'geocode error' in getWeather(city):
			return "Is {city} a city?".format(city = city)
		return "The low in {city} today is {cold_temp}".format(city = city, cold_temp = getWeather(city)['daily']['data'][0]['temperatureMin'])
	except:
		return "Sorry, I don't know."
kernel.addPattern("How cold will it get in {city} today?", prompt6) 

### prompt 7: How cold will it get in {city} this week?
def prompt7(city):
	try:
		if 'geocode error' in getWeather(city):
			return "Is {city} a city?".format(city = city)
		return "The low in {city} this week is {week_cold_temp}".format(city = city, week_cold_temp = week_cold_temp(city))
	except:
		return "Sorry, I don't know."
kernel.addPattern("How cold will it get in {city} this week?", prompt7)


################# Provided example queries #################
# get a few example responses
# print('Example queries:\n')
# queries = ['hello', 'example SI and 106', "What's the weather like in Detroit?"]
# for q in queries:
#     print('> {}'.format(q))
#     print('...{}\n'.format(kernel.respond(q)))
#print (Google_Geocode("Austin"))
#print (Dark_Sky("Honolulu"))


##################### CHATBOT PROGRAM FUNCTION ###################
print("Hi there! Thanks for waiting. How can I help you today?")
while(True):
	user_input = input('> ')
	if user_input == 'exit':
		print ("Hope you got what you needed! Thank you and goodbye for now!")
		break
	else:
 		print(kernel.respond(user_input))

