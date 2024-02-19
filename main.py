print("Flight Planner - Ryan Mitcham - 2024")
print("-------------------------------------------")

def get_coordinates():
    while True:
        proceed_input = input("Give more inputs: ")
        if proceed_input.strip().upper() != "DONE":
            break
        
        lat_input = input("Latitude: ")
        lon_input = input("Longitude: ")