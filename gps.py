"""Create routes between cities on a map."""
import sys
import argparse

class City:
    
    """ Class that uses methods to crate citites that will be used on a created map
    Attributies: Name - Name of City
    Neighbors - Dictionary which key is neighbor of city and value are tuple
    
    Methods - add_neighboor - Adds Neighbor toCity
    """

    def __init__(self, name):
        
        """ INIT Method. 
        Functionality:Initliaze List and Set Name"""
        self.name = name
        self.neighbors = {}
        
    def __repr__(self) -> str:
        
        """ Represenation Method.
        Functionailty: Gives object a string representation. RETURNS STRING"""
        return self.name
    
    def add_neighbor(self, neighbor, distance, interstate):
        
        """Add Neighboor Method
        Arguments - Neighboor City, Distance, Interstate 
        NO RETURNS
        Functionailty :Adds on to the previous initialize dictionary by checking if its not in it already."""
        route = (distance, interstate)
        if neighbor not in self.neighbors:
            self.neighbors[neighbor] = route
            
        if self not in neighbor.neighbors:
            neighbor.neighbors[self] = route
            
class Map:
    
    """MAP CLASS:  Class that plots the created city on a graph.
    Atrribuites : Cities - Initalize list of cities
    Arguments: Relationhips - Dictionary of relationships to cites """
    
    def __init__(self, relationships):
        """InIT Method.
        Functionailty: Creates a graph(map) to plot cities based on its relationships to others. Creats City Object condtionally
        NO Returns """
        self.cities  = []
        for x,y in relationships.items():
            city_positions = None
            for i,city in enumerate(self.cities): 
                if city.name == x:
                    city_positions = i
                    break
            if city_positions is None:
                new_city = City(x)
                self.cities.append(new_city)
                city_positions = len(self.cities) - 1
            for a, b, c in y:
                neighbors_positions = None
                for i, city in enumerate(self.cities):
                    if city.name == a:
                        neighbors_positions = i
                        break
                if neighbors_positions is None:
                    new_neighbor = City(a)
                    self.cities.append(new_neighbor)
                    neighbors_positions = len(self.cities) - 1
                
                self.cities[city_positions].add_neighbor(self.cities[neighbors_positions], b, c)

    def __repr__(self) -> str:
        """Representtion. No Args.
        Functionailty: Creates string represetation of objecj
        Retunrs String"""
        return str(self.cities)


def bfs(graph, start, goal):
    """ Breadth First Search Algorithim 
    Args - Graph(Map Object) Start - Starting destination Goal - End destination
    Functionailty  - Finds shortest path bewtween two nodes on the graph
    Returns - new path - path to take. Also returns None if no route to cities"""
    explored = []
    queue = [[start]]
    while queue: 
        path = queue.pop(0)
        lnode = path[-1]
        if lnode not in explored:
            for city in graph.cities:
              if city.name == lnode:
                  place = (city)
                  break
            
            neighbors = place.neighbors
            for neighbor in neighbors.keys():
                new_path = list(path)
                new_path.append(neighbor.name)
                queue.append(new_path)
                if neighbor.name == goal:
                    return (new_path)
            explored.append(lnode)
    print("No Path after through nodes")
    return None
      
                    
               
            
    
    
    
def main(start, destination, graph):
    """ Main Function. 
    Args Start- Starting point entered at terminal. Destination - End point entered at terminal
    Graph - Collections of cities and neighboors
    Functionailty - Runs Program. Implements BFS algo on start and destination
    Trys to give instructions on how to reach city. If Error rasied, quits program.
    Returns OS - A string detailing the instructions"""
    map = Map(graph)
    instructions = bfs(map, start, destination)
    try:
        OS = ""
        for i, val in enumerate(instructions):
            if val == instructions[0]:
                print(f"Starting at {val}")
                OS += f"Starting at {val}"
            if val not in instructions[-1]:
                moving_on = instructions[i+1]
                for city in map.cities:
                    if city.name == val:
                        its_neighbors = city.neighbors
                        for places in its_neighbors:
                            a,b, = its_neighbors[places]
                            if str(places) == moving_on:
                                print(f"Drive {a} miles on {b} towards {moving_on}, then")
                                OS += f"Drive {a} miles on {b} towards {moving_on}, then"
            elif val == instructions[-1]:
                print("You will arrive at your destination")
                OS += f"You will arrive at your destination"
        return OS
    except ValueError:
        quit
        
        
        
        
    
        
    











def parse_args(args_list):
    """Takes a list of strings from the command prompt and passes them through as arguments
    
    Args:
        args_list (list) : the list of strings from the command prompt
    Returns:
        args (ArgumentParser)
    """

    parser = argparse.ArgumentParser()
    
    parser.add_argument('--starting_city', type = str, help = 'The starting city in a route.')
    parser.add_argument('--destination_city', type = str, help = 'The destination city in a route.')
    
    args = parser.parse_args(args_list)
    
    return args

if __name__ == "__main__":
    
    connections = {  
        "Baltimore": [("Washington", 39, "95"), ("Philadelphia", 106, "95")],
        "Washington": [("Baltimore", 39, "95"), ("Fredericksburg", 53, "95"), ("Bedford", 137, "70")], 
        "Fredericksburg": [("Washington", 53, "95"), ("Richmond", 60, "95")],
        "Richmond": [("Charlottesville", 71, "64"), ("Williamsburg", 51, "64"), ("Durham", 151, "85")],
        "Durham": [("Richmond", 151, "85"), ("Raleigh", 29, "40"), ("Greensboro", 54, "40")],
        "Raleigh": [("Durham", 29, "40"), ("Wilmington", 129, "40"), ("Richmond", 171, "95")],
        "Greensboro": [("Charlotte", 92, "85"), ("Durham", 54, "40"), ("Ashville", 173, "40")],
        "Ashville": [("Greensboro", 173, "40"), ("Charlotte", 130, "40"), ("Knoxville", 116, "40"), ("Atlanta", 208, "85")],
        "Charlotte": [("Atlanta", 245, "85"), ("Ashville", 130, "40"), ("Greensboro", 92, "85")],
        "Jacksonville": [("Atlanta", 346, "75"), ("Tallahassee", 164, "10"), ("Daytona Beach", 86, "95")],
        "Daytona Beach": [("Orlando", 56, "4"), ("Miami", 95, "268")],
        "Orlando": [("Tampa", 94, "4"), ("Daytona Beach", 56, "4")],
        "Tampa": [("Miami", 281, "75"), ("Orlando", 94, "4"), ("Atlanta", 456, "75"), ("Tallahassee", 243, "98")],
        "Atlanta": [("Charlotte", 245, "85"), ("Ashville", 208, "85"), ("Chattanooga", 118, "75"), ("Macon", 83, "75"), ("Tampa", 456, "75"), ("Jacksonville", 346, "75"), ("Tallahassee", 273, "27") ],
        "Chattanooga": [("Atlanta", 118, "75"), ("Knoxville", 112, "75"), ("Nashville", 134, "24"), ("Birmingham", 148, "59")],
        "Knoxville": [("Chattanooga", 112,"75"), ("Lexington", 172, "75"), ("Nashville", 180, "40"), ("Ashville", 116, "40")],
        "Nashville": [("Knoxville", 180, "40"), ("Chattanooga", 134, "24"), ("Birmingam", 191, "65"), ("Memphis", 212, "40"), ("Louisville", 176, "65")],
        "Louisville": [("Nashville", 176, "65"), ("Cincinnati", 100, "71"), ("Indianapolis", 114, "65"), ("St. Louis", 260, "64"), ("Lexington", 78, "64") ],
        "Cincinnati": [("Louisville", 100, "71"), ("Indianapolis,", 112, "74"), ("Columbus", 107, "71"), ("Lexington", 83, "75"), ("Detroit", 263, "75")],
        "Columbus": [("Cincinnati", 107, "71"), ("Indianapolis", 176, "70"), ("Cleveland", 143, "71"), ("Pittsburgh", 185, "70")],
        "Detroit": [("Cincinnati", 263, "75"), ("Chicago", 283, "94"), ("Mississauga", 218, "401")],
        "Cleveland":[("Chicago", 344, "80"), ("Columbus", 143, "71"), ("Youngstown", 75, "80"), ("Buffalo", 194, "90")],
        "Youngstown":[("Pittsburgh", 67, "76")],
        "Indianapolis": [("Columbus", 175, "70"), ("Cincinnati", 112, "74"), ("St. Louis", 242, "70"), ("Chicago", 183, "65"), ("Louisville", 114, "65"), ("Mississauga", 498, "401")],
        "Pittsburg": [("Columbus", 185, "70"), ("Youngstown", 67, "76"), ("Philadelphia", 304, "76"), ("New York", 391, "76"), ("Bedford", 107, "76")],
        "Bedford": [("Pittsburg", 107, "76")], #COMEBACK
        "Chicago": [("Indianapolis", 182, "65"), ("St. Louis", 297, "55"), ("Milwaukee", 92, "94"), ("Detroit", 282, "94"), ("Cleveland", 344, "90")],
        "New York": [("Philadelphia", 95, "95"), ("Albany", 156, "87"), ("Scranton", 121, "80"), ("Providence,", 95, "181"), ("Pittsburgh", 389, "76")],
        "Scranton": [("Syracuse", 130, "81")],
        "Philadelphia": [("Washington", 139, "95"), ("Pittsburgh", 305, "76"), ("Baltimore", 101, "95"), ("New York", 95, "95")]
    }
    
    args = parse_args(sys.argv[1:])
    main(args.starting_city, args.destination_city, connections)