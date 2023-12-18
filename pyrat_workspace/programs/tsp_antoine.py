#####################################################################################################################################################
######################################################################## INFO #######################################################################
#####################################################################################################################################################

"""
    Metagraph
    https://formations.imt-atlantique.fr/pyrat
"""

#####################################################################################################################################################
###################################################################### IMPORTS ######################################################################
#####################################################################################################################################################

# Import PyRat
from pyrat import *

# External imports 
import heapq as h

# Previously developed functions
from tutorial import get_neighbors, locations_to_action, get_vertices, get_weight
from dijkstra_A import dijkstra

#####################################################################################################################################################
############################################################### CONSTANTS & VARIABLES ###############################################################
#####################################################################################################################################################

# [TODO] It is good practice to keep all your constants and global variables in an easily identifiable section

#####################################################################################################################################################
##################################################################### FUNCTIONS #####################################################################
#####################################################################################################################################################

def held_karp(start_vertex,maze,cheese,maze_width):
    
  n=len(cheese)+1

  def combinaisons(n, k):
    def aux(element, combinaison_actuelle):
        if len(combinaison_actuelle)==k:
            combinaisons.append(tuple(combinaison_actuelle))
            return
        for i in range(element, n+1):
            combinaison_actuelle.append(i)
            aux(i+1,combinaison_actuelle)
            combinaison_actuelle.pop()
    combinaisons=[]
    aux(1,[])
    return combinaisons

  assert n>=2

  if n==2 :
    return dijkstra(start_vertex,maze,cheese,maze_width)
    
  else :
    villes=[start_vertex]+cheese
    distance_matrix=[[dijkstra(ville1,maze,[ville2],maze_width) for ville2 in villes] for ville1 in villes]
    g={((k,),k):(dijkstra(start_vertex,maze,[villes[k]],maze_width)[0],[0]) for k in range(1,n)}
    for s in range(2,n):
      for S in combinaisons(n-1,s):
        for k in range(s):
          mini,ordre=float("inf"),None
          n_S=S[:k]+S[k+1:]
          for m in n_S:
            if mini>g[n_S,m][0]+distance_matrix[m][S[k]][0]:
              mini=g[n_S,m][0]+distance_matrix[m][S[k]][0]
              ordre=g[n_S,m][1]+[m]
          g[(S,S[k])]=mini,ordre
    mini,ordre=float("inf"),None
    for k in range(1,n):
      if mini>g[tuple(range(1,n)),k][0]:
        mini=g[tuple(range(1,n)),k][0]
        ordre=g[tuple(range(1,n)),k][1]+[k]
    directions=[]
    for k in range(n-1):
      directions+=distance_matrix[ordre[k]][ordre[k+1]][1]
    print(distance_matrix)
    return directions
            
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
    global routing_table
    routing_table=held_karp(player_locations[name],maze,cheese,maze_width)
    
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

    return routing_table.pop(0)

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
    players = [{"name": "TSP", "preprocessing_function": preprocessing, "turn_function": turn, "postprocessing_function": postprocessing}]

    # Customize the game elements
    config = {"maze_width": 31,
              "maze_height": 29,
              'cell_percentage': 80.0,
              "wall_percentage": 60.0,
              "mud_percentage": 20.0,
              "nb_cheese": 16}

    # Start the game
    game = PyRat(players, **config)
    stats = game.start()

    # Show statistics
    print(stats)

#####################################################################################################################################################
#####################################################################################################################################################