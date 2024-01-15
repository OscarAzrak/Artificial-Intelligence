#!/usr/bin/env python3
import random
import math
import time
from fishing_game_core.game_tree import Node
from fishing_game_core.player_utils import PlayerController
from fishing_game_core.shared import ACTION_TO_STR


class PlayerControllerHuman(PlayerController):
    def player_loop(self):
        """
        Function that generates the loop of the game. In each iteration
        the human plays through the keyboard and send
        this to the game through the sender. Then it receives an
        update of the game through receiver, with this it computes the
        next movement.
        :return:
        """

        while True:
            # send message to game that you are ready
            msg = self.receiver()
            if msg["game_over"]:
                return


class PlayerControllerMinimax(PlayerController):

    def __init__(self):
        super(PlayerControllerMinimax, self).__init__()

    def player_loop(self):
        """
        Main loop for the minimax next move search.
        :return:
        """

        # Generate first message (Do not remove this line!)
        first_msg = self.receiver()

        while True:
            msg = self.receiver()

            # Create the root node of the game tree
            node = Node(message=msg, player=0)

            # Possible next moves: "stay", "left", "right", "up", "down"
            best_move = self.search_best_next_move(initial_tree_node=node)

            # Execute next action
            self.sender({"action": best_move, "search_time": None})

    def search_best_next_move(self, initial_tree_node):
        """
        Use minimax (and extensions) to find best possible next move for player 0 (green boat)
        :param initial_tree_node: Initial game tree node
        :type initial_tree_node: game_tree.Node
            (see the Node class in game_tree.py for more information!)
        :return: either "stay", "left", "right", "up" or "down"
        :rtype: str
        """

        # EDIT THIS METHOD TO RETURN BEST NEXT POSSIBLE MODE USING MINIMAX ###

        # NOTE: Don't forget to initialize the children of the current node
        #       with its compute_and_get_children() method!

        # NOTE: You can use the get_value() method of the Node class to get
        #       the value of the current node. This value is computed by the
        #       game engine and is the sum of the values of the fish in the

        #       current state of the game.
        initial_time = time.time()
        node = initial_tree_node
        children = node.compute_and_get_children()
        moves = []

        for child in children:
            moves.append(self.minimax(node=child, player=0, depth=2, alpha=-math.inf, beta=math.inf, initial_time=initial_time))
        best_move = moves.index(max(moves))

        return ACTION_TO_STR[best_move]

    def heuristic(self, node):
        score0, score1 = node.state.get_player_scores()
        d1 = self.distance(node, 0)
        d2 = self.distance(node, 1)
        return (d1 - d2) + 30*(score0 - score1)

    def distance(self, node, player):
        distance = 0
        fish_positions = node.state.get_fish_positions()
        for fish in fish_positions.keys():
            if(fish not in [node.state.get_caught()[1 - player]]): #if fish is not caught by opponent
                fish_score = node.state.get_fish_scores()[fish] #fish score
                player_position = node.state.get_hook_positions()[player] #player position
                opponent_position = node.state.get_hook_positions()[1 - player] #opponent position
                fish_position = node.state.get_fish_positions()[fish] #fish position
                dist = self.hook_fish_distance(player_position, opponent_position, fish_position) #distance
                if(dist != 0): #if distance is not 0
                    dist = fish_score/dist #score to distance ratio
                else:
                    dist = 30*fish_score #if distance is 0, fish is on the same line as player
                if(dist > distance): #if score to distance ratio is greater than current max
                    distance = dist #set new max
        return distance

    def hook_fish_distance(self, player_position, opponent_position, fish_position):
        pt1_x, pt1_y = player_position #player position
        pt2_x, pt2_y = opponent_position #opponent position
        if pt2_x > min(pt1_x, fish_position[0]) and max(pt1_x, fish_position[0]) > pt2_x: #if opponent is on the same line as player and fish
            deltax = 20 - abs(fish_position[0] - pt1_x) #distance between player and fish
        else: #if opponent is not on the same line as player and fish
            deltax = fish_position[0] - pt1_x #distance between player and fish
        return math.sqrt(deltax**2 + (fish_position[1] - pt1_y)**2) + (20 - fish_position[1]) #return distance between player and fish


    def minimax(self, node, player, depth, alpha, beta, initial_time): #send in game state, maximize for user, minimize for opponent
        children = node.compute_and_get_children()
        if (depth == 0) or (len(children) == 0) or time.time() - initial_time > 0.05:
            v = self.heuristic(node=node)

        elif player == 0:
            v = -math.inf
            for child in node.compute_and_get_children():
                v = max(v, self.minimax(node=child, player=1, depth=depth-1, alpha=alpha, beta=beta, initial_time=initial_time))
                alpha = max(alpha, v)
                if(beta <= alpha):
                    break

        else:
            v = math.inf
            for child in node.compute_and_get_children():
                v = min(v, self.minimax(node=child, player=0, depth=depth-1, alpha=alpha, beta=beta, initial_time=initial_time))
                beta = min(beta, v)
                if(beta <= alpha):
                    break

        return v

