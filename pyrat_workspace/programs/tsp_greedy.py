#####################################################################################################################################################
######################################################################## INFO #######################################################################
#####################################################################################################################################################

"""
    This program is an empty PyRat program file.
    It serves as a template for your own programs.
    Some [TODO] comments below are here to help you keep your code organized.
    Note that all PyRat programs must have a "turn" function.
    Functions "preprocessing" and "postprocessing" are optional.
    Please check the documentation of these functions for more info on their purpose.
    Also, the PyRat website gives more detailed explanation on how a PyRat game works.
    https://formations.imt-atlantique.fr/pyrat
"""

#####################################################################################################################################################
###################################################################### IMPORTS ######################################################################
#####################################################################################################################################################

# Import PyRat
from pyrat import *

# External imports 
import heapq

# Previously developed functions
from tutorial import get_neighbors, locations_to_action , get_vertices

#####################################################################################################################################################
############################################################### CONSTANTS & VARIABLES ###############################################################
#####################################################################################################################################################

# [TODO] It is good practice to keep all your constants and global variables in an easily identifiable section

#####################################################################################################################################################
##################################################################### FUNCTIONS #####################################################################
#####################################################################################################################################################

# [TODO] It is good practice to keep all developed functions in an easily identifiable section

#####################################################################################################################################################
##################################################### EXECUTED ONCE AT THE BEGINNING OF THE GAME ####################################################
#####################################################################################################################################################
def opposite(action):
    if action == "west" :
        return "east"
    elif action == "east":
        return "west"
    elif action == "south" :
        return "north"
    elif action == "north" :
        return "south"
def list_opposite(l):
    l.reverse()
    rep=[]
    for i in l:
        rep.append(opposite(i))
    rep.reverse()
    return rep

def traversal ( source:             int,
            graph:              Union[numpy.ndarray, Dict[int, Dict[int, int]]],
            create_structure:   Callable[[], Any],
            push_to_structure:  Callable[[Any, Tuple[int, int, int]], None],
            pop_from_structure: Callable[[Any], Tuple[int, int, int]],
            #vertice_list : List[int]
            ) ->                  Tuple[Dict[int, int], Dict[int, Union[None, int]]]:
    """
    Traversal function that explores a graph from a given vertex.
    This function is generic and can be used for most graph traversal.
    To adapt it to a specific traversal, you need to provide the adapted functions to create, push and pop elements from the structure.
    In:
        * source:             Vertex from which to start the traversal.
        * graph:              Graph on which to perform the traversal.
        * create_structure:   Function that creates an empty structure to use in the traversal.
        * push_to_structure:  Function that adds an element of type B to the structure of type A.
        * pop_from_structure: Function that returns and removes an element of type B from the structure of type A.
    Out:
        * distances_to_explored_vertices: Dictionary where keys are explored vertices and associated values are the lengths of the paths to reach them.
        * routing_table:                  Routing table to allow reconstructing the paths obtained by the traversal.
    """
    distances_to_explored_vertices={source:0}
    routing_table={source:None}
    visited=create_structure()
    push_to_structure(visited,(source,0))
    while len(visited)>0:
        pop, distance_to_source =pop_from_structure(visited)
        for vertice in get_neighbors(pop,graph):
            if vertice in distances_to_explored_vertices:
                if distances_to_explored_vertices[vertice] > distance_to_source+graph[vertice][pop] :
                    distances_to_explored_vertices[vertice]=distance_to_source+graph[vertice][pop]
                    push_to_structure(visited,(vertice,distances_to_explored_vertices[vertice]))
                    routing_table[vertice]=pop
                    """if pop in cheese_list:
                        if len(cheese_list)==1:
                            print("pop",pop,"vertice",vertice)
                            distances_to_explored_vertices[vertice]=distance_to_source+graph[vertice][pop]
                            routing_table[vertice]=pop
                            return distances_to_explored_vertices , routing_table
                        else :  
                            cheese_list.remove(pop)"""
            else :
                distances_to_explored_vertices[vertice]=distance_to_source+graph[vertice][pop]
                push_to_structure(visited,(vertice,distances_to_explored_vertices[vertice]))
                routing_table[vertice]=pop
                """if pop in cheese_list:
                        if len(cheese_list)==1:
                            print("pop",pop,"vertice",vertice)
                            distances_to_explored_vertices[vertice]=distance_to_source+graph[vertice][pop]
                            routing_table[vertice]=pop
                            return distances_to_explored_vertices , routing_table
                        else :  
                            cheese_list.remove(pop)"""
    return distances_to_explored_vertices , routing_table
def dijkstra ( source: int,
                graph:  Union[numpy.ndarray, Dict[int, Dict[int, int]]],
                #vertice_list : List[int]
                ) ->      Tuple[Dict[int, int], Dict[int, Union[None, int]]]:
    """
        Dijkstra's algorithm is a particular traversal where vertices are explored in an order that is proportional to the distance to the source vertex.
        In:
            * source: Vertex from which to start the traversal.
            * graph:  Graph on which to perform the traversal.
        Out:
            * distances_to_explored_vertices: Dictionary where keys are explored vertices and associated values are the lengths of the paths to reach them.
            * routing_table:                  Routing table to allow reconstructing the paths obtained by the traversal.
    """
    
    # Function to create an empty priority queue
    def _create_structure ():
        return []
    # Function to add an element to the priority queue
    def _push_to_structure (structure, element):
        heapq.heappush(structure, element)
    # Function to extract an element from the priority queue
    def _pop_from_structure (structure):
        return heapq.heappop(structure)
    
    # Perform the traversal
    distances_to_explored_vertices, routing_table = traversal(source, graph, _create_structure, _push_to_structure, _pop_from_structure)
    return distances_to_explored_vertices, routing_table

def find_route ( routing_table: Dict[int, Union[None, int]],
                    source:        int,
                    target:        int
                ) ->             List[int]:
    """
        Function to return a sequence of locations using a provided routing table.
        In:
            * routing_table: Routing table as obtained by the traversal.
            * source:        Vertex from which we start the route (should be the one matching the routing table).
            * target:        Target to reach using the routing table.
        Out:
            * route: Sequence of locations to reach the target from the source, as perfomed in the traversal.
    """
    route=[target]
    vertice=target
    while routing_table[vertice]!= source :
        temp=routing_table[vertice]
        vertice=temp
        route.append(vertice)
    route.append(source)
    route.reverse()
    return route

def preprocessing ( maze:             Union[numpy.ndarray, Dict[int, Dict[int, int]]],
                    maze_width:       int,
                    maze_height:      int,
                    name:             str,
                    teams:            Dict[str, List[str]],
                    player_locations: Dict[str, int],
                    cheese:           List[int],
                    possible_actions: List[str],
                    memory:           threading.local
                  ) ->                None:

    """
        This function is called once at the beginning of the game.
        It is typically given more time than the turn function, to perform complex computations.
        Store the results of these computations in the provided memory to reuse them later during turns.
        To do so, you can crete entries in the memory dictionary as memory.my_key = my_value.
        In:
            * maze:             Map of the maze, as data type described by PyRat's "maze_representation" option.
            * maze_width:       Width of the maze in number of cells.
            * maze_height:      Height of the maze in number of cells.
            * name:             Name of the player controlled by this function.
            * teams:            Recap of the teams of players.
            * player_locations: Locations for all players in the game.
            * cheese:           List of available pieces of cheese in the maze.
            * possible_actions: List of possible actions.
            * memory:           Local memory to share information between preprocessing, turn and postprocessing.
        Out:
            * None.
    """
    """
        vertice_list is a list with the list of cheese and the player location
    """
    vertice_list=[player_locations[name]]
    temp=cheese.copy()
    vertice_list=vertice_list+temp

    def locations_to_actions ( locations:  List[int],
                               maze_width: int
                             ) ->          List[str]: 
        """
            Function to transform a list of locations into a list of actions to reach vertex i+1 from vertex i.
            In:
                * locations:  List of locations to visit in order.
                * maze_width: Width of the maze in number of cells.
            Out:
                * actions: Sequence of actions to visit the list of locations.
        """
        
        # We iteratively transforms pairs of locations in the corresponding action
        actions = []
        for i in range(len(locations)-1):
             action = locations_to_action(locations[i], locations[i + 1], maze_width)
             actions.append(action)
        return actions
    

    def graph_to_metagraph ( graph:    Union[numpy.ndarray, Dict[int, Dict[int, int]]],
                            vertices: List[int]
                        ) ->        Tuple[numpy.ndarray, Dict[int, Dict[int, Union[None, int]]]]:
        #changer matrice en dictionaire de dictionaire pour stocker le numéro des sommets avec la longueur 
        """
            Function to build a complete graph out of locations of interest in a given graph.
            In:
                * graph:    Graph containing the vertices of interest.
                * vertices: Vertices to use in the complete graph.
                * vertices_list[0] is the player location
            Out:
                * complete_graph: Complete graph of the vertices of interest.
                * routing_tables: Dictionary of routing tables obtained by traversals used to build the complete graph.
        """
        #initilisation de meta_graph et route avec les valeurs des sommets des frommages 
        meta_graph={i:{} for i in vertice_list}
        route={i:{} for i in vertice_list}
        for source in range(len(vertice_list)) :
            distances_to_explored_vertices, routing_table=dijkstra(vertice_list[source],maze)
            for cheesei in range(source+1,len(vertice_list)):
                meta_graph[vertice_list[source]][vertice_list[cheesei]]=distances_to_explored_vertices[vertice_list[cheesei]]
                route[vertice_list[source]][vertice_list[cheesei]]=locations_to_actions(find_route(routing_table,vertice_list[source],vertice_list[cheesei]),maze_width)
        #symétrisation du meta_graph , route
        for i in meta_graph:
            for j in meta_graph[i]:
                meta_graph[j][i]=meta_graph[i][j]
        for i in route:
            for j in route[i]:
                if route[i][j] == None:
                    continue
                else:
                    temp=route[i][j]
                    route[j][i]=list_opposite(temp)
        return meta_graph,route
        
    
    def tsp ( complete_graph: numpy.ndarray,
            source:         int
        ) ->              Tuple[List[int], int]:
        """
            Function to solve the TSP using an exhaustive search.
            In:
                * complete_graph: Complete graph of the vertices of interest.
                * source:         Vertex used to start the search.
            Out:
                * path : the shortest path to perform the meta_graph
        """
        visited=[source]
        path=[source]
        current_vertex=source
        while len(path) != len(complete_graph) :
            # If there are still vertices to visit, we explore unexplored neighbors
            min=1e9 #consideré comme infini
            min_neighbor=None
            for neighbor in complete_graph[current_vertex] :
                if neighbor not in visited :
                    if min>complete_graph[current_vertex][neighbor]:
                        min_neighbor=neighbor
                        print("min voisin",min_neighbor,)
            visited.append(min_neighbor)
            current_vertex=min_neighbor
            path.append(min_neighbor)                    
        return path
    #list of action
    def meta_graph_to_action(path,route):
        """
            Function to find the path .
            In:
                * path: list of vertices of meta_graph .
                * route: list of action to travel across different vertices in the meta_graph
        """
        actions=[]
        for i in range(len(path)-1):
            actions=actions+route[path[i]][path[i+1]]
        memory.actions=actions
    meta_graph , route = graph_to_metagraph(maze,vertice_list)
    meta_graph_to_action(tsp(meta_graph,vertice_list[0]),route)
    print("vertice_list",vertice_list)
    print("tsp",tsp(meta_graph,vertice_list[0]))
    pass
    
#####################################################################################################################################################
######################################################### EXECUTED AT EACH TURN OF THE GAME #########################################################
#####################################################################################################################################################

def turn ( maze:             Union[numpy.ndarray, Dict[int, Dict[int, int]]],
           maze_width:       int,
           maze_height:      int,
           name:             str,
           teams:            Dict[str, List[str]],
           player_locations: Dict[str, int],
           player_scores:    Dict[str, float],
           player_muds:      Dict[str, Dict[str, Union[None, int]]],
           cheese:           List[int],
           possible_actions: List[str],
           memory:           threading.local
         ) ->                str:

    """
        This function is called at every turn of the game and should return an action within the set of possible actions.
        You can access the memory you stored during the preprocessing function by doing memory.my_key.
        You can also update the existing memory with new information, or create new entries as memory.my_key = my_value.
        In:
            * maze:             Map of the maze, as data type described by PyRat's "maze_representation" option.
            * maze_width:       Width of the maze in number of cells.
            * maze_height:      Height of the maze in number of cells.
            * name:             Name of the player controlled by this function.
            * teams:            Recap of the teams of players.
            * player_locations: Locations for all players in the game.
            * player_scores:    Scores for all players in the game.
            * player_muds:      Indicates which player is currently crossing mud.
            * cheese:           List of available pieces of cheese in the maze.
            * possible_actions: List of possible actions.
            * memory:           Local memory to share information between preprocessing, turn and postprocessing.
        Out:
            * action: One of the possible actions, as given in possible_actions.
    """

    # [TODO] Write your turn code here and do not forget to return a possible action
    action = memory.actions.pop(0)
    return action

#####################################################################################################################################################
######################################################## EXECUTED ONCE AT THE END OF THE GAME #######################################################
#####################################################################################################################################################

def postprocessing ( maze:             Union[numpy.ndarray, Dict[int, Dict[int, int]]],
                     maze_width:       int,
                     maze_height:      int,
                     name:             str,
                     teams:            Dict[str, List[str]],
                     player_locations: Dict[str, int],
                     player_scores:    Dict[str, float],
                     player_muds:      Dict[str, Dict[str, Union[None, int]]],
                     cheese:           List[int],
                     possible_actions: List[str],
                     memory:           threading.local,
                     stats:            Dict[str, Any],
                   ) ->                None:

    """
        This function is called once at the end of the game.
        It is not timed, and can be used to make some cleanup, analyses of the completed game, model training, etc.
        In:
            * maze:             Map of the maze, as data type described by PyRat's "maze_representation" option.
            * maze_width:       Width of the maze in number of cells.
            * maze_height:      Height of the maze in number of cells.
            * name:             Name of the player controlled by this function.
            * teams:            Recap of the teams of players.
            * player_locations: Locations for all players in the game.
            * player_scores:    Scores for all players in the game.
            * player_muds:      Indicates which player is currently crossing mud.
            * cheese:           List of available pieces of cheese in the maze.
            * possible_actions: List of possible actions.
            * memory:           Local memory to share information between preprocessing, turn and postprocessing.
        Out:
            * None.
    """

    # [TODO] Write your postprocessing code here
    pass
    
#####################################################################################################################################################
######################################################################## GO! ########################################################################
#####################################################################################################################################################

if __name__ == "__main__":

    # Map the functions to the character
    players = [{"name": "tsp", "preprocessing_function": preprocessing, "turn_function": turn, "postprocessing_function": postprocessing}]

    # Customize the game elements
    config = {"maze_width": 12,
            "maze_height": 10,
            "mud_percentage": 40.0,
            "nb_cheese": 7,
            "trace_length": 1000}
        

    # Start the game
    game = PyRat(players, **config)
    stats = game.start()

    # Show statistics
    print(stats)

#####################################################################################################################################################
#####################################################################################################################################################