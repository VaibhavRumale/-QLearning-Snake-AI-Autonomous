import pygame
from pygame.locals import *
from snake_agent import SnakeAgent
from board import BoardEnv
import helper
import time



class SnakeGame:


    def __init__(self, args):
        self.args = args
        self.env = BoardEnv(args.snake_head_x, args.snake_head_y, args.food_x, args.food_y)
        self.agent = SnakeAgent(self.env.get_actions(), args.Ne, args.LPC, args.gamma)
    

    def play(self):
        if self.args.NUM_TRAIN_ITER != 0:
            self.do_training()
        self.do_testing()
        self.show_games()


    def do_training(self):
        print("IN TRAINING PHASE: ")
        flag = 1
        self.agent.set_train()
        NUM_TO_STAT = self.args.NUM_TO_STAT
        self.points_results = []
        start = time.time()


        for game in range(1, self.args.NUM_TRAIN_ITER + 1):
            print("TRAINING NUMBER : " + str(game))
            
            state = self.env.get_state()
            dead = False
            a = self.agent.agent_action(state, 0, dead)
           
           
            while not dead:
                temp1 = self.env.step(a)
                state = temp1[0]
                points = temp1[1]
                dead = temp1[2]
                if flag == 1 and points == 1:
                    flag = 0
                    self.agent.save_model()
                a = self.agent.agent_action(state, points, dead)
            points = self.env.get_points()
            self.points_results.append(points)
            

            if game % self.args.NUM_TO_STAT == 0:
               print(
                   "Played games:", len(self.points_results) - NUM_TO_STAT, "-", len(self.points_results),
                   "Calculated points (Average:", sum(self.points_results[-NUM_TO_STAT:])/NUM_TO_STAT,
                   "Max points so far:", max(self.points_results[-NUM_TO_STAT:]),
                   "Min points so far:", min(self.points_results[-NUM_TO_STAT:]),")",
               )
            self.env.reset()
        print("Training takes", time.time() - start, "seconds")
        #   THIS LINE WILL SAVE THE MODEL TO THE FILE "model.npy"
        self.agent.save_model()


    def do_testing(self):
        print("Test Phase:")
        self.agent.set_eval()
        #   This line loads the model
        self.agent.load_model()
        points_results = []
        start = time.time()
        


        for game in range(1, self.args.NUM_TEST_ITER + 1):
            print("TESTING NUMBER: " + str(game))
            state = self.env.get_state()
            dead = False
            action = self.agent.agent_action(state, 0, dead)
            while not dead:
                state, points, dead = self.env.step(action)
                action = self.agent.agent_action(state, points, dead)
            points = self.env.get_points()
            points_results.append(points)
            self.env.reset()
            
        #UNCOMMENT THE CODE BELOW TO PRINT STATISTICS
        print("Testing takes", time.time() - start, "seconds")
        print("Number of Games:", len(points_results))
        print("Average Points:", sum(points_results)/len(points_results))
        print("Max Points:", max(points_results))
        print("Min Points:", min(points_results))




    def show_games(self):
        print("Display Games")
        self.env.display()
        pygame.event.pump()
        self.agent.set_eval()
        points_results = []
        end = False
        for game in range(1, self.args.NUM_DISP_ITER + 1):
            state = self.env.get_state()
            dead = False
            action = self.agent.agent_action(state, 0, dead)
            count = 0
            while not dead:
                count +=1
                pygame.event.pump()
                keys = pygame.key.get_pressed()
                if keys[K_ESCAPE] or self.check_quit():
                    end = True
                    break
                state, points, dead = self.env.step(action)
                action = self.agent.agent_action(state, points, dead)
            if end:
                break
            self.env.reset()
            points_results.append(points)
            print("Game:", str(game)+"/"+str(self.args.NUM_DISP_ITER), "Points:", points)
        if len(points_results) == 0:
            return
        print("Average Points:", sum(points_results)/len(points_results))

    def check_quit(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
        return False
                

if __name__ == "__main__":

    main_args = helper.make_args()
    print(main_args)
    game1 = SnakeGame(main_args)
    game1.play()
