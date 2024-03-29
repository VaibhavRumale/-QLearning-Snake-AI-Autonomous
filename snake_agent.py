import numpy as np
import helper
import random


class SnakeAgent:

 
    def __init__(self, actions, Ne, LPC, gamma):
        self.actions = actions
        self.Ne = Ne
        self.LPC = LPC
        self.gamma = gamma
        self.reset()

        # Create the Q and N Table to work with
        self.Q = helper.initialize_q_as_zeros()
        self.N = helper.initialize_q_as_zeros()


    #   This function sets if the program is in training mode or testing mode.
    def set_train(self):
        self._train = True

     #   This function sets if the program is in training mode or testing mode.       
    def set_eval(self):
        self._train = False

    #   Calls the helper function to save the q-table after training
    def save_model(self):
        helper.save(self.Q)

    #   Calls the helper function to load the q-table when testing
    def load_model(self):
        self.Q = helper.load()

    #   resets the game state
    def reset(self):
        self.points = 0
        self.s = None
        self.a = None

.
    def helper_func(self, state):
        print("IN helper_func")
     
        head = [state[0],state[1]]
        food = [state[3], state[4]]
        body_list = []
        body = state[2]
        h_x = head[0]
        h_y = head[1]
        f_x = food[0]
        f_y = food[1]
        wall_hit = [0,0]
        direction_of_food = [0,0]
        snake_body = []
        body_list = [[i, j] for i, j in body]
   
        if h_x == 40:
            wall_hit[0] = 1
        elif h_x == 480:
            wall_hit[0] = 2
        else:
            wall_hit[0] = 0
        if h_y == 40:
            wall_hit[1] = 1
        elif h_y == 480:
            wall_hit[1] = 2
        else:
            wall_hit[1] = 0

        if (f_x - h_x) > 0:
            direction_of_food[0] = 2
        elif (f_x - h_x) < 0:
            direction_of_food[0] = 1
        else:
            direction_of_food[0] = 0
        if (f_y - h_y) > 0:
            direction_of_food[1] = 2
        elif (f_y - h_y) < 0:
            direction_of_food[1] = 1
        else:
            direction_of_food[1] = 0
            
        for x, y in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            if [h_x+x, h_y+y] in body_list:
                snake_body.append(1)
            else:
                snake_body.append(0)
#      print("HEREEE!!!")
        empty_cells = 0
        if [h_x, h_y-1] not in body_list:
            empty_cells += 1
        if [h_x, h_y+1] not in body_list:
            empty_cells += 1
        if [h_x-1, h_y] not in body_list:
            empty_cells += 1
        if [h_x+1, h_y] not in body_list:
            empty_cells += 1
            
        return [wall_hit[0],wall_hit[1],direction_of_food[0],direction_of_food[1],snake_body[0],snake_body[1],snake_body[2],snake_body[3], empty_cells]
       
    
    def compute_reward(self, points, dead):
        if dead:
            return -1
        elif points > self.points:
            return 1
        else:
            return -0.1

  
    def agent_action(self, state, points, dead):
        print("IN AGENT_ACTION")

        def change(state,dead,points,prev_s,prev_a):
            # Get the previous state and action in the form of Q-table indices
            prev_m = self.helper_func(prev_s)
            r = self.compute_reward(points, dead)           #Calculate the reward obtained for the previous action
            pres_s = self.helper_func(state)                #Get the current state in the form of Q-table indices

            # Get the Q-values for all possible actions in the current state
            left = self.Q[pres_s[0]][pres_s[1]][pres_s[2]][pres_s[3]][pres_s[4]][pres_s[5]][pres_s[6]][pres_s[7]][2]

            right = self.Q[pres_s[0]][pres_s[1]][pres_s[2]][pres_s[3]][pres_s[4]][pres_s[5]][pres_s[6]][pres_s[7]][3]

            upper = self.Q[pres_s[0]][pres_s[1]][pres_s[2]][pres_s[3]][pres_s[4]][pres_s[5]][pres_s[6]][pres_s[7]][0]

            bottom = self.Q[pres_s[0]][pres_s[1]][pres_s[2]][pres_s[3]][pres_s[4]][pres_s[5]][pres_s[6]][pres_s[7]][1]

            action = max(upper, bottom, left, right)  #For maximum Q-value
        
            q = self.Q[prev_m[0]][prev_m[1]][prev_m[2]][prev_m[3]][prev_m[4]][prev_m[5]][prev_m[6]][prev_m[7]][prev_a]
            temp=(self.LPC + self.N[prev_m[0]][prev_m[1]][prev_m[2]][prev_m[3]] [prev_m[4]][prev_m[5]][prev_m[6]][prev_m[7]][prev_a])
            alpha = self.LPC / temp
            change = q + alpha * (r + self.gamma * action - q)
            
            
            return change

        Qvalues = [0, 0, 0, 0]  #INITIALIZATION
#        if self.a == 0:        #I was trying to fix the cases where the snake heads in opposite direction dying instantly
#            Qvalues[1] = -100
#        elif self.a == 1:
#            Qvalues[0] = -100
#        elif self.a == 2:
#            Qvalues[3] = -100
#        elif self.a == 3:
#            Qvalues[2] = -100

        

        if dead:                    # Check if the agent has died in the previous turn
            prev_s = self.helper_func(self.s)            # Updating state-action pair and reseting the agent's state for previous values
            self.Q[prev_s[0]][prev_s[1]][prev_s[2]][prev_s[3]][prev_s[4]][prev_s[5]][prev_s[6]][prev_s[7]][self.a] = change(state, dead, points, self.s, self.a)
            self.reset()
            return
        pres_s = self.helper_func(state)      # Convert the current state into Q-table indices
       
        if self._train and self.s != None and self.a != None:
            prev_s = self.helper_func(self.s)
            new_q = change(state, dead, points, self.s, self.a)
            self.Q[prev_s[0]][prev_s[1]][prev_s[2]][prev_s[3]][prev_s[4]][prev_s[5]][prev_s[6]][prev_s[7]][self.a] = new_q
       
        for i in range(helper.NUM_ACTIONS):
            n = self.N[pres_s[0]][pres_s[1]][pres_s[2]][pres_s[3]][pres_s[4]][pres_s[5]][pres_s[6]][pres_s[7]][i]
            q = self.Q[pres_s[0]][pres_s[1]][pres_s[2]][pres_s[3]][pres_s[4]][pres_s[5]][pres_s[6]][pres_s[7]][i]
            if n < self.Ne:
                Qvalues[i] = 1
            else:
                Qvalues[i] = q
        action = np.argmax(Qvalues)
        max_action = max(Qvalues)
        if self.a == 0 and action == 1:                           #Still trying to fix the same issue! Keeps on taking a turn in opposite direction
                action = np.argmax(Qvalues[:-1])                  #Score could be much better if I was able to fix this issue
        elif self.a == 1 and action == 0:
                action = np.argmax(Qvalues[1:])
        elif self.a == 2 and action == 3:
                action = np.argmax(Qvalues[:3])
        elif self.a == 3 and action == 2:
                action = np.argmax(Qvalues[3:])

        
        
        for i in range(len(Qvalues)-1, -1, -1):
            if Qvalues[i] == max_action:
                action = i
                break
       
        self.N[pres_s[0]][pres_s[1]][pres_s[2]][pres_s[3]][pres_s[4]][pres_s[5]][pres_s[6]][pres_s[7]][action] += 1
        self.s = state
        self.a = action
        self.points = points
        return action
