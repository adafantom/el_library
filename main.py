import json
import requests
from geopy import distance
import folium
from flask import Flask
import os


API_KEY = os.environ['API_KEY']


def fetch_coordinates(API_KEY, address):
    base_url = "https://geocode-maps.yandex.ru/1.x"
    response = requests.get(base_url, params={
        "geocode": address,
        "apikey": API_KEY,
        "format": "json",
    })
    response.raise_for_status()
    found_places = response.json()['response']['GeoObjectCollection']['featureMember']

    if not found_places:
        return None

    most_relevant = found_places[0]
    lon, lat = most_relevant['GeoObject']['Point']['pos'].split(" ")
    return lon, lat


def get_user_coords():
    user_geo_point = input('Где вы находитесь? Ваш местоположение: ')
    user_coords = fetch_coordinates(API_KEY, user_geo_point)
    return user_geo_point, user_coords


def get_distance(coffee_house):
    return coffee_house['distance']


def get_coords(user_coords):
    with open("coffee.json", "r", encoding="CP1251") as my_file:
        file_contents = my_file.read()

    file_contents = json.loads(file_contents)  
  
    coffee_list = []
    
    for file_element in file_contents:
        coffee_house  = dict()
        coffee_house['Name'] = file_element['Name']
        coffee_house['longitude'], coffee_house['latitude'] = file_element['geoData']['coordinates']
        coffee_house['distance'] = distance.distance((user_coords[1], user_coords[0]), (coffee_house['latitude'],coffee_house['longitude'])).km
        coffee_list.append(coffee_house)

    return sorted(coffee_list, key=get_distance)[:5]


def save_html(near_coffee, user_coords):
    m = folium.Map(location=[user_coords[1], user_coords[0]],  zoom_start=13)
    folium.Marker(
        ([user_coords[1], user_coords[0]]), popup='<i>{}</i>'.format(user_geo_point), tooltip=user_geo_point
    ).add_to(m)
    
    for coffee in near_coffee:
        folium.Marker(
          (coffee['latitude'], coffee['longitude']), popup='<i>{}</i>'.format(coffee['Name']), tooltip=coffee['Name']
        ).add_to(m)
    
    return m.save("index.html")


def hello_world():
     with open('index.html') as file:
      return file.read()


if __name__ == '__main__':
    user_geo_point, user_coords = get_user_coords()
    near_coffee = get_coords(user_coords)
    save_html(near_coffee, user_coords)
    app = Flask(__name__)
    app.add_url_rule('/', 'hello', hello_world)
    app.run('0.0.0.0')