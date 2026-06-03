import requests
import smtplib
import os

API_KEY = os.environ.get("OWM_API_KEY")
LAT = 13.756331
LON = 100.501762

my_email = os.environ.get("EMAIL")
password = os.environ.get("PASSWORD")

OWM_Endpoint = "https://api.openweathermap.org/data/2.5/forecast"

weather_params = {
    "lat": LAT,
    "lon": LON,
    "appid": API_KEY,
    "cnt": 4,
}

response = requests.get(OWM_Endpoint, params=weather_params)
response.raise_for_status()
weather_data = response.json()

# for i in range(len(weather_data["list"])):
#     for j in range(len(weather_data["list"][i]["weather"])):
#         condition_code = weather_data["list"][i]["weather"][j]["id"]

will_rain = False
for hour_data in weather_data["list"]:
    condition_code = hour_data["weather"][0]["id"]
    if int(condition_code) < 700:
        will_rain = True

if will_rain:
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=my_email, password=password)
        connection.sendmail(
            from_addr=my_email,
            to_addrs=my_email,
            msg= "Subject:It is going to rain tomorrow\n\nRemember to bring your umbrella!!",
        )
        print("mail sent!")

