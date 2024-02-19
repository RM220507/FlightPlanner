# Don't write or change any code in this file. You can call the methods from your main.py file

class Waypoint: 
    def __init__(self, name, lat, lon): 
        self.name = name 
        self.lat = lat
        self.lon = lon

class Aircraft:
    def __init__(self, name, capacity, burn, reserve, cruiseSpeed): 
        self.name = name 
        self.capacity = capacity
        self.reserve = reserve
        self.burn = burn

        # Convert knots to m/s
        self.cruiseSpeed = (cruiseSpeed/1.944)

        # Calculate capacity with reserve fuel removed
        adjustedCapacity = capacity * (1-(reserve/100))
        self.adjustedCapacity = adjustedCapacity

        # Calculate maximum flight time in seconds
        maxFlightTime = (adjustedCapacity/burn)*3600  

        # Calculate aircraft range in meters
        # ∆𝑠 = ∆t ⋅ 𝑣 
        maxRange = maxFlightTime*(cruiseSpeed/1.944)
        # Convert to kilometers
        self.maxRange = maxRange/1000

def fetchWaypoints():

    waypoints = []

    # Generate waypoints
    waypoints.append(Waypoint("Waypoint 1", -38.84646, 145.5433))
    waypoints.append(Waypoint("Waypoint 2", -32.84646, 90.72480))
    waypoints.append(Waypoint("Waypoint 3", -1.94289, -114.30181))
    waypoints.append(Waypoint("Waypoint 4", 61.99259, -21.22569))
    waypoints.append(Waypoint("Waypoint 5", 33.38230, -68.63856))
    waypoints.append(Waypoint("Waypoint 6", 28.33409, 0.22041))
    waypoints.append(Waypoint("Waypoint 7", -0.62933, -148.48595))
    waypoints.append(Waypoint("Waypoint 8", 23.14100, -158.66447))
    waypoints.append(Waypoint("Waypoint 9", -27.75061, -53.36579))
    waypoints.append(Waypoint("Waypoint 10", 17.83333, -126.81735))

    return waypoints

def fetchAircraft():

    aircraft = []

        # Generate aircraft
    aircraft.append(Aircraft("Extra 300", 159, 72, 5, 178))
    aircraft.append(Aircraft("Cessna 182", 333, 59, 10, 140))
    aircraft.append(Aircraft("BAES Hawk", 1360, 374, 10, 430))
    aircraft.append(Aircraft("Learjet", 1870, 645, 10, 503))
    aircraft.append(Aircraft("Boeing 737-8", 20726, 2657, 10, 453))

    return aircraft