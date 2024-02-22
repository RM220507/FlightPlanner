import re
from multimethod import multimethod
import math

import DataService as data

class Route:
    def __init__(self):
        self.__waypoints = []
    
    @multimethod
    def add_waypoint(self, waypoint_obj : data.Waypoint) -> None:
        self.__waypoints.append(waypoint_obj)

    @add_waypoint.register
    def _(self, name : str, lat : float, lon : float) -> None:
        print("Adding Waypoint")
        self.__waypoints.append(data.Waypoint(name, lat, lon))

    @property
    def waypoint_count(self) -> int:
        return len(self.__waypoints)
    
    def calculate_distance_pythag(self) -> float:
        total_distance = 0
        print("Calculating distance.")
        for i, waypoint in enumerate(self.__waypoints[:-1]):
            next_point = self.__waypoints[i + 1]
            
            enclosed_angle = math.cos((waypoint.lat + next_point.lat) / 2)
            x = (next_point.lon - waypoint.lon) * enclosed_angle
            y = next_point.lat - next_point.lon
            
            distance = math.sqrt((x ** 2) + (y ** 2)) * 6371
            print(f"Distance ({waypoint.name} -> {next_point.name}): {round(distance)}km.")
            total_distance += distance
            
        print(f"Total distance (between {self.waypoint_count} Waypoints): {round(total_distance)}km.")
        return total_distance

def validate_float(input_val : str) -> bool:
    return re.match(r'^-?\d*(\.\d+)?$', input_val) is not None        

def input_float(prompt : str, min_val : float=float("-inf"), max_val : float=float("inf")) -> float:
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
    lat_input = input_float("Latitiude (North is positive): ", -90, 90)
    lon_input = input_float("Longitude (East is positive): ", -180, 180)

    return lat_input, lon_input

def build_route(route : Route) -> None:
    print("Adding Waypoints.")
    done_adding = False
    while not done_adding:
        if route.waypoint_count == 20:
            print("20 Waypoints Added. No more allowed.")
            break
        
        lat, lon = get_lat_lon()
        
        default_name = f"Route Waypoint{route.waypoint_count + 1}"
        print(f"Default Waypoint name: {default_name}")
        name = input("Name of Waypoint (leave blank to use default): ")
        if name == "":
            name = default_name

        route.add_waypoint(name, math.radians(lat), math.radians(lon))
        print(f"Added Waypoint (Latitude: {lat}; Longitude: {lon}) as {name}")

        if route.waypoint_count != 1:
            done_adding = input_bool("Add more waypoints? (enter DONE to exit): ", "DONE")
        else:
            print("Only 1 Waypoint. More required to create route.")
        
    print("Waypoints Added.")
        
def main():
    route = Route()
    build_route(route)
    print(route.calculate_distance_pythag())
    
print("Flight Planner - Ryan Mitcham - 2023")
print("-------------------------------------------")
    
input("Press ENTER to Start")
main()
