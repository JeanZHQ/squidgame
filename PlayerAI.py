import numpy as np
import random
import time
import sys
import os
from BaseAI import BaseAI
from Grid import Grid

# TO BE IMPLEMENTED
#
from Utils import manhattan_distance

# The largest possible number of the Heuristic funcion
H_MAX = 8

# The max_depth when searching for next trap
TRAP_SEARCH_DEPTH = 5

class PlayerAI(BaseAI):
    
    def __init__(self) -> None:
        # You may choose to add attributes to your player - up to you!
        super().__init__()
        self.pos = None
        self.player_num = None
    
    def getPosition(self):
        return self.pos
    
    def setPosition(self, new_position):
        self.pos = new_position
    
    def getPlayerNum(self):
        return self.player_num
    
    def setPlayerNum(self, num):
        self.player_num = num
    
    def getMove(self, grid: Grid) -> tuple:
        """ 
        YOUR CODE GOES HERE

        The function should return a tuple of (x,y) coordinates to which the player moves.

        It should be the result of the ExpectiMinimax algorithm, maximizing over the Opponent's *Trap* actions, 
        taking into account the probabilities of them landing in the positions you believe they'd throw to.

        Note that you are not required to account for the probabilities of it landing in a different cell.

        You may adjust the input variables as you wish (though it is not necessary). Output has to be (x,y) coordinates.
        
        """
        
        # find all available moves
        available_moves = grid.get_neighbors(self.pos, only_available=True)
        
        # make random move
        new_pos = random.choice(available_moves) if available_moves else None
        
        return new_pos
    
    def throw(self, grid: Grid, intended_position: tuple) -> tuple:
        '''
        Description
        ----------
        Function returns the potential position a trap will land as well as the corresponding probability

        Parameters
        ----------

        player : the player throwing the trap

        grid : current game Grid

        intended position : the (x,y) coordinates to which the player intends to throw the trap to.

        Returns
        -------
        Position (x_0,y_0) in which the trap landed : tuple

        '''
        
        # find neighboring cells
        neighbors = grid.get_neighbors(intended_position)
        
        neighbors = [neighbor for neighbor in neighbors if grid.getCellValue(neighbor) <= 0]
        n = len(neighbors)
        
        probs = np.ones(1 + n)
        
        # compute probability of success, p
        p = 1 - 0.05 * (manhattan_distance(self.pos, intended_position) - 1)
        
        probs[0] = p
        
        probs[1:] = np.ones(len(neighbors)) * ((1 - p) / n)
        
        # add desired coordinates to neighbors
        neighbors.insert(0, intended_position)
        
        return probs, neighbors
    
    def H(self,grid):
        player_neighbors = grid.get_neighbors(self.pos, only_available= True)
        opponent = grid.find(3 - self.player_num)
        opponent_neighbors = grid.get_neighbors(opponent, only_available=True)
        return len(player_neighbors) - len(opponent_neighbors)
    
    def getMax(self, grid: Grid, depth: int):
        # find opponent
        opponent = grid.find(3 - self.player_num)
        
        # find all available cells surrounding Opponent
        available_cells = grid.get_neighbors(opponent, only_available=True)
        
        if len(available_cells) == 0:
            # no available neighbor, actually will never happen
            return opponent
        
        next_trap = available_cells[0]
        depth -=1
        max_U = self.getChance(grid, next_trap,depth)
        for cell in available_cells:
            cur_U = self.getChance(grid, cell,depth)
            if cur_U > max_U:
                next_trap = cell
                max_U = cur_U
        return next_trap, max_U
    
    def getMin(self, grid: Grid,depth : int):
        
        # find opponent
        opponent = grid.find(3 - self.player_num)
        neighbors = grid.get_neighbors(opponent, only_available=True)
        
        # if the number of available neighbor is 0, that means the opponent is trapped and the player wins the game.
        # Hence we return infinity at this point we return a really large number However we can't infinity here,
        # because we should compare the situation where the trap's neighbor will fully trap the opponent and the trap
        # itself will do so.
        if len(neighbors) == 0:
            return H_MAX
        min_U = float('inf')
        depth -=1
        for i in range(len(neighbors)):
            next_move = neighbors[i]
            grid_clone = grid.clone()
            grid_clone.move(next_move, player=3 - self.player_num)
            if depth == 0:
                cur_U = self.H(grid_clone)
            else:
                _, cur_U = self.getMax(grid_clone,depth)
            if cur_U >= min_U:
                continue
            min_U = cur_U
        return min_U
    
    def getChance(self, grid: Grid, intended_position: tuple,depth :int):
        probs, positions = self.throw(grid, intended_position)
        chance = 0
        for i in range(len(probs)):
            grid_copy = grid.clone()
            grid_copy.trap(positions[i])
            if depth == 0:
                chance = probs[i]*self.H(grid_copy)
            else:
                chance = probs[i] * self.getMin(grid_copy,depth)
        return chance

    def getTrap(self, grid: Grid) -> tuple:
        """ 
        YOUR CODE GOES HERE

        The function should return a tuple of (x,y) coordinates to which the player *WANTS* to throw the trap.
        
        It should be the result of the ExpectiMinimax algorithm, maximizing over the Opponent's *Move* actions, 
        taking into account the probabilities of it landing in the positions you want. 
        
        Note that you are not required to account for the probabilities of it landing in a different cell.

        You may adjust the input variables as you wish (though it is not necessary). Output has to be (x,y) coordinates.
        
        """
        
        next_trap, max_U = self.getMax(grid, TRAP_SEARCH_DEPTH)
        
        return next_trap


# class Status():
#     def __init__(self):
#         self.status = None
