# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

from cmath import inf
from itertools import accumulate
from queue import PriorityQueue
import util


class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"

    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"

    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

# Please DO NOT change the following code, we will use it later
def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    myPQ = util.PriorityQueue()
    startState = problem.getStartState()
    startNode = (startState, '',0, [])
    myPQ.push(startNode,heuristic(startState,problem))
    visited = set()
    best_g = dict()
    while not myPQ.isEmpty():
        node = myPQ.pop()
        state, action, cost, path = node
        if (not state in visited) or cost < best_g.get(state):
            visited.add(state)
            best_g[state]=cost
            if problem.isGoalState(state):
                path = path + [(state, action)]
                actions = [action[1] for action in path]
                del actions[0]
                return actions
            for succ in problem.getSuccessors(state):
                succState, succAction, succCost = succ
                newNode = (succState, succAction, cost + succCost, path + [(state, action)])
                myPQ.push(newNode,heuristic(succState,problem)+cost+succCost)
    util.raiseNotDefined()


def enforcedHillClimbing(problem, heuristic=nullHeuristic):
    """
    Local search with heuristic function.
    You DO NOT need to implement any heuristic, but you DO have to call it.
    The heuristic function is "manhattanHeuristic" from searchAgent.py.
    It will be pass to this function as second argument (heuristic).
    """
    "*** YOUR CODE HERE FOR TASK 1 ***"
    
    #from game import Directions
    # put the below line at the end of your code or remove it
    #return [Directions.SOUTH,Directions.SOUTH]
    import time
    start=time.time()
    currentNode=(problem.getStartState(),[]) 
    
    while not problem.isGoalState(currentNode[0]):
        q=util.Queue()
        q.push(currentNode)
        visited=[]
        while not q.isEmpty():
            node=q.pop()
            
            if node[0] not in visited:
                visited.append(node[0])
    
            if heuristic(node[0], problem)<heuristic(currentNode[0], problem):

                currentNode = node
                break
            for suc in list(problem.getSuccessors(node[0])):
                if suc[0] not in visited:
                    #print(suc)
                    q.push((suc[0],node[1] + [suc[1]]))
    #print(currentNode[1])
    return currentNode[1]


    util.raiseNotDefined()
        

from math import inf as INF   
def bidirectionalAStarEnhanced(problem, heuristic=nullHeuristic, backwardsHeuristic=nullHeuristic):
    
    """
    Bidirectional global search with heuristic function.
    You DO NOT need to implement any heuristic, but you DO have to call them.
    The heuristic functions are "manhattanHeuristic" and "backwardsManhattanHeuristic" from searchAgent.py.
    It will be pass to this function as second and third arguments.
    You can call it by using: heuristic(state,problem) or backwardsHeuristic(state,problem)
    """
    "*** YOUR CODE HERE FOR TASK 2 ***"
    # The problem passed in going to be BidirectionalPositionSearchProblem  
    #print(problem.get)
    #problem.goal=tuple([1,1] + [1]*len(problem.foodLocation))
    
    goals=problem.getGoalStates()
    
    #print("Goal: Before | After",problem.goal," | ",goal)
    start=problem.getStartState()
    #print("Start: Before | After",problem.start,start)
    
    #goals_achieved+=1
    open={}
    closed={}
    open['f']=util.PriorityQueue()
    open['b']=util.PriorityQueue()
    closed['f']=[]#save states
    closed['b']=[]
    
    
    for goal in goals:
        startNode={}
        startNode['g_f']=0
        startNode['g_b']=0
        startNode['pth_f']=[]
        startNode['pth_b']=[]
        startNode['state']=start
        
        startNode['action']=""
        
        goalNode={}
        goalNode['g_f']=0
        goalNode['g_b']=0
        goalNode['pth_f']=[]
        goalNode['pth_b']=[]
        #print("Goal: ",problem.getGoal())
        goalNode['state']=goal#problem.getGoalStates()[1]
        goalNode['action']=""
        
        
        
        f_start =startNode['g_f'] + heuristic(startNode['state'],problem)
        d_start =startNode['g_f'] - backwardsHeuristic(goalNode['state'],problem)
        
        #print("bx at the begining: ",f_start+d_start)
        
        open['f'].push(startNode,f_start+d_start)
        #print(startNode)
        f_goal = goalNode['g_b'] + backwardsHeuristic(startNode['state'],problem)
        d_goal = goalNode['g_b'] - heuristic(goalNode['state'],problem)
        
        #print("bx_N(n) at the begining: ",f_goal+d_goal)
        
        open['b'].push(goalNode,f_goal+d_goal)
    
    #print(goalNode)
    l=0
    u=INF
    pi=[]
    x='b'
    
    expandedNodes=0
    
    while not open['f'].isEmpty() and not open['b'].isEmpty():
        
        bminf=open['f'].getMinimumPriority()
        bminb=open['b'].getMinimumPriority()
        l=(bminf+bminb)/2
        n=open[x].pop()
        expandedNodes+=1
        closed[x].append(n['state'])
        x_n='f' if x=='b' else 'b'     
        
        #print("\ncurrent node: ",n['state']," in direction: ",x," with priority: ",bminf if x=='f' else bminb)
 
        
        for open_node in open[x_n].heap:
            
            open_node=open_node[2]#dicitionary is in position 2
            if open_node['state'] == n['state']:

                g_x=n['g_'+x]
                g_x_n=open_node['g_'+x_n]
                n_x_n=open_node

                if g_x+g_x_n<u:
                    
                    u=g_x+g_x_n
                    #print('new u: ', u)
                    pi=n['pth_f']+open_node['pth_b'][::-1] if x=='f' else open_node['pth_f']+n['pth_b'][::-1]

        #print("L: ",l,"U: ",u)
        if l>=u: 
          #if goals_achieved==len(problem.getGoalStates()):
              #print("Nodes expanded: ",expandedNodes)
              #print("Plan: ", pi)
              return pi
          #else: 
          #    pi_acum=pi_acum+pi
          #    break
      
        succ_strategy=problem.getSuccessors(n['state']) if x=='f' else problem.getBackwardsSuccessors(n['state'])        
        
        
        if x=='f': succ_strategy.reverse()
        #print("Successors in direction: ",x)
        for succ in succ_strategy:
            
            succState, succAction, succCost = succ
            
            stateSeen=False
            for seen_state in closed[x]:
                if succState == seen_state:
                    stateSeen = True
            
            if not stateSeen:

                futNode={}
                if x=='f':
                    futNode['g_f']= n['g_f'] + succCost
                    futNode['g_b']=0
                    futNode['pth_f']=n['pth_f']+[succAction] 
                    futNode['pth_b']=[]
                    futNode['state']=succState
                    futNode['action']=succAction
                else:
                    futNode['g_f']= 0
                    futNode['g_b']=n['g_b'] + succCost
                    futNode['pth_f']=[]
                    futNode['pth_b']=n['pth_b']+[succAction]
                    futNode['state']=succState
                    futNode['action']=succAction
                
                
                
                f = futNode['g_'+x] + ( heuristic(futNode['state'],problem) if x=='f' else backwardsHeuristic(futNode['state'],problem))
                d = futNode['g_'+x] - ( backwardsHeuristic(futNode['state'],problem)) if x=='f' else heuristic(futNode['state'],problem)
                #print("Succesor ",succState," with priority ",f+d)
                open[x].push(futNode,f+d)
        #print("Frontier in direction: ",x, ": ",[nd[2]["state"] for nd in open[x].heap] )        
        
        x=x_n
            
        
        #if goals_achieved==len(problem.getGoalStates()):
        #    return pi_acum
        #else: pi_acum+pi
        
    
    # put the below line at the end of your code or remove it
    util.raiseNotDefined()

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch


ehc = enforcedHillClimbing
bae = bidirectionalAStarEnhanced


