import requests 

with open ("spara_data.txt", "r")as file:
   lines = file.readlines()
   print(lines)

# klassen skickar API-förfrågan och hämtar väderdata. 
class ApiRequest: 
    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude
        self.url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m"
        
# Definierar en metod som hämtar väderdata från API
    def fetch_data(self):
        response = requests.get(self.url)
        print (response)
        if response.status_code in [200, 201, 202, 203]:
            return( response.json()) # returnar värdet om det får rätt "svarskod"
        else:
            print("Misslyckades att hämta väderdata från API.")
             
 
# Skapar en klass för att bearbeta väderdatan som hämtats från API
class Sort:
    def __init__(self, data):
        self.data = data

# Definierar en metod för att extrahera specifik väderinformation.
    def weather_info(self):
        hourly_data = self.data.get('hourly', {})
        temperature = hourly_data.get('temperature_2m', 'No data')
        humidity = hourly_data.get('relative_humidity_2m', 'No data')
        wind_speed = hourly_data.get('wind_speed_10m', 'No data')
        return temperature, humidity, wind_speed
    

latitude = input ("välj lat, ange i kordinater: \n")
longitude = input ("välj log, ange i kordinater: \n") 
stad = input ("Ge din plats ett namn: \n") 


# Skapa en instans av ApiRequest-klassen och hämta väderdata.
api_request = ApiRequest(latitude, longitude)
weather_data = api_request.fetch_data()


# bearbetar  och extraherar temperatur, luftfuktighet och vindhastighet för användning.
sorter = Sort(weather_data)
temperature, humidity, wind_speed = sorter.weather_info()

# printa ut värderna.
print(f"Temperature: {temperature[0]}")
print(f"Humidity: {humidity[0]}")
print(f"Wind Speed: {wind_speed[0]}")

# kordinater stockholm: 59.33 |  18.03

with open("spara_data.txt", "a") as file:
    file.write(f"temperature: {temperature[0]},humidity: {humidity[0]},wind_speed: {wind_speed[0]}\n")


# TODO: gör en meny. t ex 1. lägg till stad. 2. visa städer. 3. visa väder för stad.
#

# Visa menyn
print("Välj ett alternativ")
print("1. Lägg till stad")
print("2. Visa städer")
print("3. Visa väder för stad")

# Hämta användarens val
val = input("Ange ditt val (1-3): \n")

# Använd if-satser för att hantera olika val
if val == "1":
    stad = input("Vilken stad vill du lägga till?: ")
    # Lägg till funktionalitet för att spara staden
    print(f"Staden {stad} har lagts till!")
    
elif val == "2":
    # Lägg till funktionalitet för att visa städer
    print("Här är listan med städer...")
    
elif val == "3":
    stad = input("Vilken stad vill du visa väder för?: ")
    # Lägg till funktionalitet för att visa vädret för en stad
    print(f"Visar vädret för {stad}...")
    
else:
    print("Ogiltigt val, försök igen.")
