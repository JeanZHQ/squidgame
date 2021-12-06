import unittest
from Grid import Grid
from Game import Game
from test_players.EasyAI import EasyAI
from Displayer import Displayer
from PlayerAI import PlayerAI
import time

def one_turn(turn, game):
    game.prevTime = time.process_time()
    grid_copy = game.grid.clone()
    
    move = None
    
    if turn == 1:
        
        print("Player's Turn: ")
        
        # find best move; should return two coordinates - new position and bombed tile.
        move = game.playerAI.getMove(grid_copy)
        
        # if move is valid, perform it
        if game.is_valid_move(game.grid, game.playerAI, move):
            game.grid.move(move, turn)
            game.playerAI.setPosition(move)
            print(f"Moving to {move}")
        else:
            game.over = True
            print(f"Tried to move to : {move}")
            print("invalid Player AI move!")
        
        intended_trap = game.playerAI.getTrap(game.grid.clone())
        
        if game.is_valid_trap(game.grid, intended_trap):
            trap = game.throw(game.playerAI, game.grid, intended_trap)
            game.grid.trap(trap)
            print(f"Throwing a trap to: {intended_trap}. Trap landed in {trap}")
        
        else:
            game.over = True
            print(f"Tried to put trap in {intended_trap}")
            print("Invalid trap!")
    
    else:
        
        print("Opponent's Turn : ")
        
        # make move
        move = game.computerAI.getMove(grid_copy)
        
        # check if move is valid; perform if it is.
        if game.is_valid_move(game.grid, game.computerAI, move):
            game.grid.move(move, turn)
            game.computerAI.setPosition(move)
            print(f"Moving to {move}")
        
        else:
            game.over = True
            print("invalid Computer AI Move")
        
        intended_trap = game.computerAI.getTrap(game.grid.clone())
        
        if game.is_valid_trap(game.grid, intended_trap):
            trap = game.throw(game.computerAI, game.grid, intended_trap)
            game.grid.trap(trap)
            print(f"Throwing a trap to: {intended_trap}. Trap landed in {trap}")
        else:
            game.over = True
            print(f"Tried to put trap in {intended_trap}")
            print("Invalid trap!")
    
    if game.is_over(turn):
        game.over = True
    game.updateAlarm(time.process_time())
    game.displayer.display(game.grid)
    
class MyTestCase(unittest.TestCase):
    def test_grid(self):
        grid = Grid(7)
    
    def test_game(self):
        playerAI = EasyAI()
        computerAI = EasyAI()  # change this to a more sophisticated player you've coded
        displayer = Displayer()
        game = Game(playerAI=playerAI, computerAI=computerAI, N=7, displayer=displayer)
        game.initialize_game()
        displayer.display(game.grid)
        one_turn(1,game)

    # test Player
    def player_throw(self):
        playerAI = PlayerAI()
        computerAI = EasyAI()  # change this to a more sophisticated player you've coded
        displayer = Displayer()
        game = Game(playerAI=playerAI, computerAI=computerAI, N=7, displayer=displayer)
        game.initialize_game()
        displayer.display(game.grid)
        playerAI.throw(game.grid,(1,3))
        
if __name__ == '__main__':
    unittest.main()
