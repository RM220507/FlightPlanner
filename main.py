## TODO - Add comments

import re
from multimethod import multimethod
import math
import plotly.graph_objects as go

import DataService as data

DEBUG_ROUTE_CREATE = True
DEBUG_AIRCRAFT_SELECT = True

class Route:
    def __init__(self):
        self.__waypoints = []
    
    @multimethod
    def add_waypoint(self, waypoint_obj : data.Waypoint) -> None:
        """THis is where I'd put my docstring explaining how this method works"""
        self.add_waypoint(waypoint_obj.name, math.radians(waypoint_obj.lat), math.radians(waypoint_obj.lon))

    @add_waypoint.register
    def _(self, name : str, lat : float, lon : float) -> data.Waypoint:
        waypoint = data.Waypoint(name, lat, lon)
        self.__waypoints.append(waypoint)
        return waypoint

    @property
    def waypoint_count(self) -> int:
        return len(self.__waypoints)
    
    def calculate_distance(self, use_haversine : bool = True) -> float:
        total_distance = 0
        print("Calculating distance.")
        for i, waypoint in enumerate(self.__waypoints[:-1]):            
            next_point = self.__waypoints[i + 1]
            
            if use_haversine:
                distance = self.calculate_dist_haversine(waypoint, next_point)
            else:
                distance = self.calculate_dist_pythag(waypoint, next_point)
            
            print(f"Distance ({waypoint.name} -> {next_point.name}): {round(distance)}km.")
            total_distance += distance
            
        print(f"Total distance (between {self.waypoint_count} Waypoints): {round(total_distance)}km.")
        return round(total_distance)
    
    def calculate_dist_pythag(self, waypoint : data.Waypoint, next_point : data.Waypoint) -> float:
        enclosed_angle = math.cos((waypoint.lat + next_point.lat) / 2)
        x = (next_point.lon - waypoint.lon) * enclosed_angle
        y = next_point.lat - next_point.lat
            
        distance = math.sqrt((x ** 2) + (y ** 2)) * 6371
        return distance
    
    def calculate_dist_haversine(self, waypoint : data.Waypoint, next_point : data.Waypoint) -> float:
        haversine_lat = (math.sin((next_point.lat - waypoint.lat) / 2)) ** 2
        
        convex_combination = math.cos(waypoint.lat) * math.cos(next_point.lat)
        haversine_lon = (math.sin((next_point.lon - waypoint.lon) / 2)) ** 2
        term_2 = convex_combination * haversine_lon
        
        inside_arcsin = math.sqrt(haversine_lat + term_2)
        
        distance = 2 * 6371 * math.asin(inside_arcsin)
        return distance
    
    def plot(self):
        fig = go.Figure(
            go.Scattermapbox(
                mode = "markers+lines",
                lon = [math.degrees(waypoint.lon) for waypoint in self.__waypoints],
                lat = [math.degrees(waypoint.lat) for waypoint in self.__waypoints],
                marker = {"size" : 10}
            )
        )
        
        fig.update_layout(
            margin ={'l':0,'t':0,'b':0,'r':0},
            mapbox = {
                'center': {'lon': 0, 'lat': 0},
                'style': "open-street-map",
                'center': {'lon': 0, 'lat': 0},
                'zoom': 1
            }
        )
        
        fig.show()

def validate_float(input_val : str) -> bool:
    return re.match(r'^-?\d*(\.\d+)?$', input_val) is not None

def input_float(prompt : str, min_val : float=float("-inf"), max_val : float=float("inf")) -> float:
    """Force a user to keep inputting a float, until it has a valid structure between the bounds specified."""
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

def input_int(prompt : str, min_val : float = float("-inf"), max_val : float = float("inf")) -> int:
    input_val = ""
    valid = False
    while not valid:
        input_val = input(prompt)
        
        if input_val.isdigit() and min_val <= int(input_val) <= max_val:
            valid = True
        else:
            print("Not a valid input. Try again.")
            
    return int(input_val)

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
        
        if input_bool("Use [P]re-determined or [C]ustom Waypoint? ", "C"):
            lat, lon = get_lat_lon()
            
            default_name = f"Route Waypoint {route.waypoint_count + 1}"
            print(f"Default Waypoint name: {default_name}")
            name = input("Name of Waypoint (leave blank to use default): ")
            if name == "":
                name = default_name

            waypoint_to_add = route.add_waypoint(name, math.radians(lat), math.radians(lon))
        else:
            waypoint_to_add = get_waypoint()
            route.add_waypoint(waypoint_to_add)
        
        print(f"Added Waypoint (Latitude: {waypoint_to_add.lat}; Longitude: {waypoint_to_add.lon}) as {waypoint_to_add.name}")

        if route.waypoint_count != 1:
            done_adding = input_bool("Add more waypoints? (enter DONE to exit): ", "DONE")
        else:
            print("Only 1 Waypoint. More required to create route.")
        
    print("Waypoints Added.")
    
def select_aircraft_from_list() -> data.Aircraft:
    aircraft_list = data.fetchAircraft()
    
    print("Available Aircraft:")
    
    aircraft_names = []
    for aircraft in aircraft_list:
        print(aircraft.name)
        aircraft_names.append(aircraft.name.upper())
        
    valid = False
    while not valid:
        aircraft_name_input = input("Enter name of desired aircraft: ")
        if aircraft_name_input.upper() in aircraft_names:
            valid = True
        else:
            print(f"Aircraft '{aircraft_name_input}' is unknown. Please try again.")
            
    select_aircraft = aircraft_list[aircraft_names.index(aircraft_name_input.upper())]
    return select_aircraft

def calculate_flight_info(aircraft : data.Aircraft, distance : int) -> bool | float | float:
    print(f"Using Aircraft: {aircraft.name}")
    flight_possible = distance < aircraft.maxRange
    
    flight_time = ((distance * 1000) / aircraft.cruiseSpeed) / 3600
    
    fuel_required = aircraft.burn * flight_time
    
    return flight_possible, round(flight_time, 2), round(fuel_required)

def get_waypoint() -> data.Waypoint:
    waypoints = data.fetchWaypoints()
    for i, waypoint in enumerate(waypoints):
        print(f"{(i + 1):02} - {waypoint.name}")
        
    waypoint_id = input_int("Enter a waypoint index: ", min_val=0, max_val=len(waypoints) - 1)
    return waypoints[waypoint_id]
        
def main():
    route = Route()
    
    if not DEBUG_ROUTE_CREATE:
        build_route(route)
    else:
        route.add_waypoint(data.fetchWaypoints()[0])
        route.add_waypoint(data.fetchWaypoints()[1])
        route.add_waypoint(data.fetchWaypoints()[2])
    
    if input_bool("Use [P]ythagoras or [H]aversine for distance calculations? ", "P"):
        distance = route.calculate_distance(use_haversine=False)
    else:
        distance = route.calculate_distance()
    
    if not DEBUG_AIRCRAFT_SELECT:
        aircraft = select_aircraft_from_list()
    else:
        aircraft = data.fetchAircraft()[0]
    
    flight_possible, flight_time, fuel_required = calculate_flight_info(aircraft, distance)
    
    print(f"Flight Possible: {flight_possible}")
    print(f"Fuel Load: {fuel_required}/{aircraft.capacity}")
    print(f"Flight Time: {flight_time} hours")
    
    route.plot()
    input("Press ENTER to Exit")
    
print("Flight Planner - Ryan Mitcham - 2023")
print("-------------------------------------------")
    
input("Press ENTER to Start")
main()
