import requests
import matplotlib.pyplot as plt

api_key = input("Enter your API key: ")
cities = input("Enter cities (comma separated): ").split(",")

cities = [c.strip() for c in cities if c.strip() != ""]

if len(cities) < 2:
    print("Please enter at least 2 cities.")
    exit()

temps = []
humidity = []
valid_cities = []

for city in cities:
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    try:
        response = requests.get(url)
        data = response.json()

        if str(data.get("cod")) == "200":
            temps.append(data["main"]["temp"])
            humidity.append(data["main"]["humidity"])
            valid_cities.append(city)
        else:
            print(f"Skipping {city} (Not Found)")

    except requests.exceptions.RequestException:
        print(f"Error fetching data for {city}")

if not temps:
    print("No valid cities found.")
    exit()
max_temp = max(temps)
hottest_city = valid_cities[temps.index(max_temp)]
colors = ["red" if t == max_temp else "skyblue" for t in temps]
plt.figure(figsize=(10, 4))
plt.subplot(1, 2, 1)
bars = plt.bar(valid_cities, temps, color=colors, width=0.5)
plt.title("Temperature Comparison")
plt.ylabel("Temperature (°C)")
plt.ylim(0, max_temp + 5)
for bar in bars:
    y = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2,
             y + 0.5,
             f"{y:.1f}",
             ha='center',
             fontsize=8)
plt.subplot(1, 2, 2)
bars2 = plt.bar(valid_cities, humidity, width=0.5)
plt.title("Humidity Comparison")
plt.ylabel("Humidity (%)")
for bar in bars2:
    y = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2,
             y + 0.5,
             f"{y:.0f}",
             ha='center',
             fontsize=8)

plt.tight_layout()
plt.show()
print(f"\nHottest City: {hottest_city} ({max_temp}°C)")
