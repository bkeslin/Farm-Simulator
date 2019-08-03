## Node class, UCT, and play_game functions from http://mcts.ai/code/python.html 

from math import log, sqrt
from random import choice
from enum  import Enum


class plant_options(Enum) :
    EMPTY = 0
    CORN = 1
    BEAN = 2


class Farm :
    def __init__ (self, size) :
        self._farm = [[plant_options.EMPTY.value for n in range(size)] for n in range(size)]
        self._size = size 
        self._plays = []        


    def clone(self) :
        farm = Farm(self._size)
        farm._farm = [[self._farm[row][column] for row in range(self._size)] for column in range(self._size)]
        return farm


    def execute_play(self, move) :
        row, column, crop = move
        if self._farm[row][column] == plant_options.EMPTY.value :
            self._farm[row][column] = crop
            return "Success"
        return "Failure"


    def get_plays(self) : 
        plays = []
        for row in range (self._size) :
            for column in range(self._size) :
                if self._farm[row][column] == plant_options.EMPTY.value :
                    plays.append((row, column, plant_options.CORN.value))
                    plays.append((row, column, plant_options.BEAN.value))

        return plays


    def get_result(self) :
        score = 0
        for row in range(self._size) :
            for column in range(self._size) :
                if self._farm[row][column] == plant_options.CORN.value :
                    corn_score = 10
                    if row + 1 < self._size and column + 1 < self._size and self._farm[row + 1][column + 1] == plant_options.BEAN.value :
                        corn_score += 1
                    if row + 1 < self._size and self._farm[row + 1][column] == plant_options.BEAN.value :
                        corn_score += 1
                    if row + 1 < self._size and column >= 1 and self._farm[row + 1][column - 1] == plant_options.BEAN.value :
                        corn_score += 1
                    if column + 1 < self._size and self._farm[row][column + 1] == plant_options.BEAN.value :
                        corn_score += 1
                    if column >= 1 and self._farm[row][column - 1] == plant_options.BEAN.value :
                        corn_score += 1
                    if row >= 1 and column + 1 < self._size and self._farm[row - 1][column + 1] == plant_options.BEAN.value :
                        corn_score += 1
                    if row >= 1 and self._farm[row - 1][column] == plant_options.BEAN.value :
                        corn_score += 1
                    if row >= 1 and column >= 1 and self._farm[row - 1][column - 1] == plant_options.BEAN.value :
                        corn_score += 1
                    
                    score += corn_score

                if self._farm[row][column] == plant_options.BEAN.value :
                    bean_score = 10
                    if row + 1 < self._size and column + 1 < self._size and self._farm[row + 1][column + 1] == plant_options.CORN.value :
                        bean_score += 5
                    elif row + 1 < self._size and self._farm[row + 1][column] == plant_options.CORN.value :
                        bean_score += 5
                    elif row + 1 < self._size and column >= 1 and self._farm[row + 1][column - 1] == plant_options.CORN.value :
                        bean_score += 5
                    elif column + 1 < self._size and self._farm[row][column + 1] == plant_options.CORN.value :
                        bean_score += 5
                    elif column >= 1 and self._farm[row][column - 1] == plant_options.CORN.value :
                        bean_score += 5
                    elif row >= 1 and column + 1 < self._size and self._farm[row - 1][column + 1] == plant_options.CORN.value :
                        bean_score += 5
                    elif row >= 1 and self._farm[row - 1][column] == plant_options.CORN.value :
                        bean_score += 5
                    elif row >= 1 and column >= 1 and self._farm[row - 1][column - 1] == plant_options.CORN.value :
                        bean_score += 5

                    score += bean_score

        return score


    def move_to_string(self, move) :
        row, column, crop = move
        plant_str = "bean" if (crop == plant_options.BEAN.value) else "corn"
        string = "Location = (" + str(row) + ", " + str(column) + "), Crop = " + plant_str
        return string

class Node :
    def __init__ (self, move = None, parent = None, farm = None) :
        self.move = move 
        self.parent_node = parent
        self.child_nodes = []
        self.score = 0
        self.visits = 0
        self.unexplored_moves = farm.get_plays()


    def uct_select_child (self) :
        s = sorted(self.child_nodes, key = lambda c: c.score/c.visits + sqrt(2*log(self.visits)/c.visits))[-1]
        return s


    def add_child (self, mv, st) :
        n = Node(move = mv, parent = self, farm = st)
        self.child_nodes.append(n)
        self.unexplored_moves.remove(mv)
        return n


    def update (self, result) :
        self.visits += 1
        self.score += result


def UCT (root_farm, marow_iter) :
    root_node = Node(farm = root_farm)
    for i in range (marow_iter) :
        node = root_node
        farm = root_farm.clone()

        while node.unexplored_moves == [] and node.child_nodes != [] :
            node = node.uct_select_child()
            farm.execute_play(node.move)

        if node.unexplored_moves != [] :
            m = choice(node.unexplored_moves)
            farm.execute_play(m)
            node = node.add_child(m, farm)

        while farm.get_plays() != [] :
            farm.execute_play(choice(farm.get_plays()))
            
        while node != None :
            node.update(farm.get_result())
            node = node.parent_node

    return sorted(root_node.child_nodes, key = lambda c: c.visits)[-1].move

def play_game (size) :
    farm = Farm(size) 
    optimal_move_list = []
    while (farm.get_plays() != []):
        m = UCT(root_farm = farm, marow_iter = 1000)
        #print ("Best Move: " + farm.move_to_string(m))
        optimal_move_list.append(farm.move_to_string(m))
        farm.execute_play(m)

    print ("Best score found " + str(farm.get_result()))
    return optimal_move_list


if __name__ == "__main__" :
    size = 6
    move_list = play_game(size)
    print (move_list)