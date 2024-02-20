import re
from multimethod import multimethod

import DataService as data

class Route:
    def __init__(self):
        self.__waypoints = []
    
    @multimethod (object, object)
    def add_waypoint(self, waypoint_obj):
        self.__waypoints.append(waypoint_obj)

    @multimethod (object, str, float, float)
    def add_waypoint(self, name, lat, lon):
        self.__waypoints.append(data.Waypoint(name, lat, lon))

    @property
    def waypoint_count(self):
        return len(self.__waypoints)

print("Flight Planner - Ryan Mitcham - 2023")
print("-------------------------------------------")

def validate_float(input_val : str) -> bool:
    return re.match(r'^-?\d+(?:\.\d+)?$', element) is None        

def input_float(prompt : str, min_val=float("-inf") : float, max_val=float("inf") : float) -> float:
    input_val = ""
    valid = False
    while not valid:
        input_val = input(prompt)
        
        if validate_float(input_val) and min_val <= float(input_val) <= max_val:
            valid = True
        else:
            print("Not a valid input. Try again.")
            
    return float(input_val)

def input_bool(prompt : str, condition_val : str) -> bool:
    input_val = input(prompt)

    return input_val.strip().upper() == condition_val.upper()

def get_lat_lon() -> float | float:
    lat_input = input_float("Latitiude: ", -90, 90)
    lon_input = input_float("Longitude: ", -180, 180)

    return lat_input, lon_input

def build_route(route : Route) -> None:
    done_adding = False
    while not done_adding:
        lat, lon = get_lat_lon()
        name = input("Name of waypoint (leave blank to use default): ")
        if name == "":
            name = f"Route Waypoint{route.waypoint_count + 1}"

        route.add_waypoint(name, lat, lon)

        done_adding = input_bool("Add more waypoints? (Enter DONE to exit): ", "DONE")
        
def main():
    route = Route()
    build_route(route)

input("Press ENTER to Start")
build_route()
