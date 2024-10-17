import requests

# Klassen för att hämta väderdata
class ApiRequest:
    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude
        self.url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m"

    def fetch_data(self):
        response = requests.get(self.url)
        if response.status_code in [200, 201, 202, 203]:
            return response.json()
        else:
            print("Misslyckades att hämta väderdata från API.")
            

# Klass för att bearbeta väderdata
class Sort:
    def __init__(self, data):
        self.data = data

    def weather_info(self):
        hourly_data = self.data.get('hourly', {})
        temperature = hourly_data.get('temperature_2m', 'No data')
        humidity = hourly_data.get('relative_humidity_2m', 'No data')
        wind_speed = hourly_data.get('wind_speed_10m', 'No data')
        return temperature, humidity, wind_speed

# Funktion för att hantera menyval
def meny():
    while True:
        print("\nVälj ett alternativ")
        print("1. Lägg till stad")
        print("2. Visa städer")
        print("3. Visa väder för stad")
        print("4. Avsluta")
        
        val = input("Ange ditt val (1-4): \n")

        if val == "1":
            stad = input("Vilken stad vill du lägga till?: ")
            latitude = input("Ange latitud för staden: ")
            longitude = input("Ange longitud för staden: ")

            # Spara stad och koordinater i en fil
            with open("spara_data.txt", "a") as file:
                file.write(f"{stad},{latitude},{longitude}\n")
            print(f"Staden {stad} har lagts till!")

        elif val == "2":
            # Visa alla sparade städer
            with open("spara_data.txt", "r") as file:
                stader = file.readlines()
                if stader:
                    print("Sparade städer:")
                    for stad in stader:
                        print(stad)
                else:
                    print("Inga städer sparade.")

        elif val == "3":
            stad = input("Vilken stad vill du visa väder för?: ")
            with open("spara_data.txt", "r") as file:
                stader = file.readlines()

            # Hitta staden och dess koordinater
            found = False
            for line in stader:
                data = line.strip().split(',')
                if data[0].lower() == stad.lower():
                    latitude = data[1]
                    longitude = data[2]
                    found = True
                    break

            if found:
                # Hämta och visa väderdata för staden
                api_request = ApiRequest(latitude, longitude)
                weather_data = api_request.fetch_data()

                if weather_data:
                    sorter = Sort(weather_data)
                    temperature, humidity, wind_speed = sorter.weather_info()
                    print(f"Temperature: {temperature[0]}")
                    print(f"Humidity: {humidity[0]}")
                    print(f"Wind Speed: {wind_speed[0]}")
            else:
                print(f"Staden {stad} hittades inte.")
        
        elif val == "4":
            print("Programmet avslutas.")
            break
        else:
            print("Ogiltigt val, försök igen.")

if __name__ == "__main__":
    meny()
