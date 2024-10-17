import requests 

# TODO: rensa onödiga kommentarer.
# TODO: få till en deletefunktion i menyn som rensar textfilen.

class ApiRequest:  # hämtar väderdata från API.
    def __init__(self, latitude, longitude):   # Konstruktor som tar dessa två argument.
        self.latitude = latitude
        self.longitude = longitude
        # Skapar URL med variablerna ovan för att hämta väderdata från API.
        self.url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true"


    def hämta_data(self):  # hämtar datan från API. 
        response = requests.get(self.url)  # skickar förfrågan om data och får svarskod.
        if response.status_code in [200, 201, 202, 203]:  
            return response.json() 
        else: 
            print("Misslyckades att hämta väderdata från API.")  


class Väder: # bearbetar väderdata.
    def __init__(self, data):  # Konstruktor som tar emot väderdata
        self.data = data  # Sparar väderdatan

    def väder_info(self):  
        current_data = self.data.get('current_weather', {})  # hämta värdet nyckeln 'current_weather i urlen.
        temperature = current_data.get('temperature', 'No data')  # Hämtar temperaturen. eller "No data" vid fel.
        wind_speed = current_data.get('windspeed', 'No data')  # Hämtar vindhastighet. eller "No data" vid fel.
        return temperature, wind_speed  


def menyval():
    while True:  # loppar tills break.
        print("\nVälj ett alternativ")  
        print("1. Lägg till stad") 
        print("2. Visa städer")  
        print("3. Visa väder för stad")  
        print("4. Rensa textfilen") 
        print("5. Avsluta") 
        
        val = input("Ange ditt val (1-4): \n")  

        if val == "1": 
            stad = input("Vilken stad vill du lägga till?: ")  
            latitude = input("Ange latitud för staden: ")  
            longitude = input("Ange longitud för staden: ")  

            with open("spara_data.txt", "a") as file:  
                file.write(f"{stad},{latitude},{longitude}\n")  
            print(f"Staden {stad} har lagts till!")  


        elif val == "2": 
            with open("spara_data.txt", "r") as file:  
                städer = file.readlines() 
                if städer:  
                    print("Sparade städer:")  
                    for stad in städer: 
                        print(stad)  
                else: 
                    print("Inga städer sparade.")  


        elif val == "3": 
            stad = input("Vilken stad vill du visa väder för?: ")  
            with open("spara_data.txt", "r") as file: 
                städer = file.readlines()  


            found = False  # Variabel för att hålla koll på om staden hittas
            for line in städer: 
                data = line.strip().split(',')  # delar upp på (,) i olika indexeringar för att få ut rätt del data.
                if data[0].lower() == stad.lower():  
                    latitude = data[1] 
                    longitude = data[2]  
                    found = True  # Markera att staden har hittats
                    break  # Avbryt loopen när staden hittats

            if found:  # Om staden hittats
                api_request = ApiRequest(latitude, longitude)  # Skapa ett ApiRequest-objekt med stadens koordinater.
                väder_data = api_request.hämta_data()  # Hämta väderdata från API.

                if väder_data:  # Om väderdata hämtats
                    väder = Väder(väder_data)  # Skapa ett Väder-objekt för att bearbeta datan
                    temperature, wind_speed = väder.väder_info()  # Hämta temperatur och vindhastighet för nedan.
                    print(f"Temperature: {temperature}")
                    print(f"Wind Speed: {wind_speed}")
            else: 
                print(f"Staden {stad} hittades inte.") 


        elif val == "4":
            with open("spara_data.txt", 'w') as file:
                pass  
            print("Filen har rensats.")


        elif val == "5":
            print("Programmet avslutas.")
            break 
        else: 
            print("Ogiltigt val, försök igen.")

if __name__ == "__main__":
    menyval()
