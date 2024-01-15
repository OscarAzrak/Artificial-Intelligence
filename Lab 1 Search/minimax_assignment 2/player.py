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
        node = initial_tree_node
        children = node.compute_and_get_children()
        moves = []
        for child in children:
            moves.append(self.minimax(node=child, player=0, depth=2, alpha=-math.inf, beta=math.inf))

        best_move = moves.index(max(moves))



        return ACTION_TO_STR[best_move]

    def heuristic(self, node, player):
        score_p0, score_p1 = node.state.get_player_scores()
        heuristic = score_p0 - score_p1
        if player == 1:
            heuristic = -heuristic
        else:
            heuristic = heuristic - self.closest_fish_distance(node, player)
        return heuristic

    def minimax(self, node, player, depth, alpha, beta):
        # if no fishes --> terminal state
        if list(node.state.get_fish_positions().keys()) == [] or depth == 0:
            v = self.heuristic(node=node, player=0)

        else:
            if player == 0:
                v = -math.inf
                for child in node.compute_and_get_children():
                    v = max(v, self.minimax(node=child, player=1, depth=depth-1, alpha=alpha, beta=beta))
                    alpha = max(alpha, v)
                    if(beta <= alpha):
                        break

            else:
                v = math.inf
                for child in node.compute_and_get_children():
                    v = min(v, self.minimax(node=child, player=0, depth=depth-1, alpha=alpha, beta=beta))
                    beta = min(beta, v)
                    if(beta <= alpha):
                        break

        return v

    def closest_fish_distance(self, node, player):
        dist = []
        hooks = node.state.get_hook_positions()
        for fish in list(node.state.get_fish_positions().values()):
            print(fish)
            dist.append(self.fish_hook_distance(hooks[player], fish))
        if(dist == []):
            return 0
        return min(dist)

    def fish_hook_distance(self, hook, fish):
        return math.sqrt(math.pow(hook[0] - fish[0], 2) + math.pow(hook[1] - fish[1], 2))

