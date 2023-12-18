#####################################################################################################################################################
######################################################################## INFO #######################################################################
#####################################################################################################################################################

"""
    Greedy
    https://formations.imt-atlantique.fr/pyrat
"""

#####################################################################################################################################################
###################################################################### IMPORTS ######################################################################
#####################################################################################################################################################

# Import PyRat
from pyrat import *

# External imports 
import heapq as h
import dijkstra as opponent

# Previously developed functions
from tutorial import get_neighbors,get_vertices,get_weight,locations_to_action

#####################################################################################################################################################
############################################################### CONSTANTS & VARIABLES ###############################################################
#####################################################################################################################################################

# [TODO] It is good practice to keep all your constants and global variables in an easily identifiable section

#####################################################################################################################################################
##################################################################### FUNCTIONS #####################################################################
#####################################################################################################################################################

def dijkstra(start_vertex:int,maze:Union[numpy.ndarray, Dict[int, Dict[int, int]]],cheese:list[int],maze_width:int):
  """
  Renvoie la liste des directions à parcourir entre la position initiale et le fromage le plus proche dans un graphe avec des poids non négatifs.
  """
  assert cheese!=[]
  tas=[]
  h.heappush(tas,(0,start_vertex))
  table={vertex:(float("inf"),[]) for vertex in get_vertices(maze)}
  while tas!=[]:
    current_distance,current_vertex=h.heappop(tas)
    if current_vertex in cheese:
      tas=[]
    else :
      for nb in get_neighbors(current_vertex,maze):
        distance=current_distance+get_weight(current_vertex,nb,maze)
        if distance<table[nb][0]:
            chemin=table[current_vertex][1]+[locations_to_action(current_vertex,nb,maze_width)]
            h.heappush(tas,(distance,nb))
            table[nb]=(distance,chemin)
  return table[current_vertex],current_vertex


def ciblage(my_location:int,opp_location:int,maze:Union[numpy.ndarray, Dict[int, Dict[int, int]]],cheese:list[int],maze_width:int):
    """
    Renvoie la liste des directions à suivre pour atteindre le prochain fromage accessible, en respectant le principe suivant :
    tant que le joueur n'a pas atteint le fromage suivant, il doit connaitre parfaitement les actions de l'adversaire si celui-ci fait un greedy algorithm.
    """
    cibles=cheese.copy()
    (my_dist,my_routing_table),my_target=dijkstra(my_location,maze,cibles,maze_width)
    (opp_dist,opp_routing_table),opp_target=dijkstra(opp_location,maze,cibles,maze_width)
    while opp_dist<=my_dist and len(cibles)>1:
        cibles.remove(opp_target)
        if my_target==opp_target:
            (my_dist,my_routing_table),my_target=dijkstra(my_location,maze,cibles,maze_width)
            (dist,opp_routing_table),opp_target=dijkstra(opp_target,maze,cibles,maze_width)
            opp_dist+=dist
        else : 
            (dist,opp_routing_table),opp_target=dijkstra(opp_target,maze,cibles,maze_width)
            opp_dist+=dist
    return my_routing_table,my_target

#####################################################################################################################################################
##################################################### EXECUTED ONCE AT THE BEGINNING OF THE GAME ####################################################
#####################################################################################################################################################

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
    memory.greedy1=(len(teams)==1 or player_locations[name]==player_locations[teams['Opponent'][0]])
    if memory.greedy1:
        memory.my_routing_table=dijkstra(player_locations[name],maze,cheese,maze_width)[0][1]
    else :
        memory.my_routing_table=ciblage(player_locations[name],player_locations[teams['Opponent'][0]],maze,cheese,maze_width)[0]
    
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
    if memory.my_routing_table==[]:
        if memory.greedy1:
            memory.my_routing_table=dijkstra(player_locations[name],maze,memory.cheese,maze_width)[0][1]
        else :
            memory.my_routing_table=ciblage(player_locations[name],player_locations[teams['Opponent'][0]],maze,cheese,maze_width)[0]
    return memory.my_routing_table.pop(0)

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
    players = [{"name": "Greedy", "preprocessing_function": preprocessing, "turn_function": turn, "postprocessing_function": postprocessing,"location":"random"},
               {"name": "Adversaire", "team": "Opponent", "skin": "python", "preprocessing_function": opponent.preprocessing if "preprocessing" in dir(opponent) else None, "turn_function": opponent.turn, "postprocessing_function": postprocessing if "postprocessing" in dir(opponent) else None,"location":"random"}]

    # Customize the game elements
    config = {"maze_width": 31,
              "maze_height": 29,
              "mud_percentage": 20,
              "nb_cheese": 41}

    # Start the game
    game = PyRat(players, **config)
    stats = game.start()

    # Show statistics
    print(stats)

#####################################################################################################################################################
#####################################################################################################################################################