import numpy as np
import json


data={"Q_Learn":None,"Path":None,"Training_Summary":None,"Path_Summary":None}
Epochs={}


# R matrix
R=np.matrix([[-1, -1, -1, -1, 0, -1],
                          [-1, -1, -1, 0, -1, 100],
                          [-1, -1, -1, 0, -1, -1],
                          [-1, 0, 0, -1, 0, -1],
                          [-1, 0, 0, -1, -1, 100],
                          [-1, 0, -1, -1, 0, 100]])
Q = np.matrix(np.zeros([6, 6]))

# This function returns all availbe actions in the state given as argument
def available_actions(state):
    current_state_row = R[state,]
    av_act = np.where(current_state_row >=0)[1]
    return av_act

#This function chooses at random which action to be performed within the range of all the available actions
def sample_next_action(available_actions_range):
    next_action = int(np.random.choice(available_actions_range, 1))
    return next_action

#This function updates the Q matrix according to the path selected and the Q learning algorithm
def update(current_state, action, gamma,epo):
    max_index = np.where(Q[action,] == np.max(Q[action,]))[1]
    
    if max_index.shape[0] > 1:
        max_index = int(np.random.choice(max_index, size=1))
    else:
        max_index = int(max_index)
    max_value = Q[action, max_index]
    
    #Q learning formula
    Q[current_state, action] = R[current_state, action] + gamma * max_value
    v_m=str(current_state)+str(action)
    Epochs[epo]=dict({v_m: Q[current_state, action]})
    return epo+1

class Q_Learn:
    def __init__(self,gamma=0.8,initial_state=1):
        #Gamma (learning parameter).
        self.gamma = gamma
        #Initial state. (Usually to be choosen at random)
        self.initial_state=initial_state

    def train(self,n,epo):
        #Training
        print("\n   Agent Training starts: ")
        for i in range(n):
            current_state = np.random.randint(0, int(Q.shape[0]))
            available_act = available_actions(current_state)
            action = sample_next_action(available_act)
            epo=update(current_state, action, self.gamma,epo)
        #Normalize the trained Q matrix
        print("\n Trained Q matrix: ")
        print(Q / np.max(Q) * 100)
        print("\n Wow..!! Agent is trained.")

    def find_path(self,current_state=2,final_state=5):
        print("\n ............ Finding the path: ")
        steps = [current_state]
        while current_state != final_state:
            
            next_step_index = np.where(Q[current_state,] == np.max(Q[current_state,]))[1]
            
            if next_step_index.shape[0] > 1:
                next_step_index = int(np.random.choice(next_step_index, size=1))
            else:
                next_step_index = int(next_step_index)
                
            steps.append(next_step_index)
            current_state = next_step_index
        return steps
        print("\n  Path found.")        
        

def access_algorithm():
    print("\n   Available  states: 0,1,2,3,4,5 ")
    initial_state=int(input("\n   Enter initial state for training: "))
    gamma=float(input("\n Enter learning parameter: (between 0 and 1) :"))
    n=int(input("\n Enter number of epochs for training: "))
    # Get available actions in the current state
    available_act = available_actions(initial_state)

    # Sample next action to be performed
    action = sample_next_action(available_act)

    #Upadte Q matrix
    epo=0
    epo=update(initial_state, action, gamma,epo)
    #Print selected sequence of path

    obj=Q_Learn(gamma,initial_state)
    obj.train(n,epo)
    print("\n  Enter the nodes to get path between nodes:")
    start_node=int(input("\n  Enter Start Node: "))
    final_node=int(input("\n  Enter Final Destination Node: "))
    steps=obj.find_path(start_node,final_node)
    print("\n Selected path: ")
    print(steps)
    if len(steps)==0:
        print("No Path")
    data['Q_Learn']=Epochs
    data['Path']=steps
    model_summary=" Learning Parameter:"+ str(gamma)+ " Training Epochs: " + str(n)+ " Initial State  For Training: "+ str(initial_state)
    path_summary=" Start Node: "+ str(start_node)+ " Final Destination Node:" + str(final_node)
    
    data['Training_Summary']=model_summary
    data['Path_Summary']=path_summary
    with open('model_history.json', 'w') as json_file:
      json.dump(data, json_file)
    
    
if __name__=="__main__":
    access_algorithm()
