
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

import util


class Node:
    def __init__(self, state, path, cost):
        self.state = state
        self.path = path
        self.cost = cost


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
    return [s, s, w, s, w, w, s, w]


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
    # variables init:
    start_state = problem.getStartState()
    start_node = Node(start_state, [], 0)
    frontier = util.Stack()
    frontier.push(start_node)
    closed_list = set()
    while not frontier.isEmpty():
        current_node = frontier.pop()
        if problem.isGoalState(current_node.state):
            return current_node.path
        closed_list.add(current_node.state)
        for children_state, children_path, children_cost in problem.getSuccessors(current_node.state):
            if problem.isGoalState(children_state):
                return current_node.path + [children_path]
            child_node = Node(children_state, [children_path], children_cost)
            if child_node.state not in closed_list and child_node.state not in (node.state for node in frontier.list):
                child_node.cost += current_node.cost
                child_node.path = current_node.path + child_node.path
                frontier.push(child_node)
    return False



def breadthFirstSearch(problem):
    start_state = problem.getStartState()
    start_node = Node(start_state, [], 0)
    frontier = util.Queue()
    frontier.push(start_node)
    closed_list = []
    while not frontier.isEmpty():
        current_node = frontier.pop()
        if problem.isGoalState(current_node.state):
            return current_node.path
        closed_list.append(current_node.state)
        for children_state, children_path, children_cost in problem.getSuccessors(current_node.state):
            if problem.isGoalState(children_state):
                return current_node.path + [children_path]
            child_node = Node(children_state, [children_path], children_cost)
            if child_node.state not in closed_list and child_node.state not in (node.state for node in frontier.list):
                child_node.cost += current_node.cost
                child_node.path = current_node.path + child_node.path
                frontier.push(child_node)
    return False


def uniformCostSearch(problem):

    start_state = problem.getStartState()
    start_node = Node(start_state, [], 0)
    frontier = util.PriorityQueue()
    frontier.push(start_node, 0)
    closed_list = set()
    while not frontier.isEmpty():
        current_node = frontier.pop()
        if problem.isGoalState(current_node.state):
            return current_node.path
        if current_node.state not in closed_list:
            for children_state, children_path, children_cost in problem.getSuccessors(current_node.state):
                if problem.isGoalState(children_state):
                    return current_node.path + [children_path]
                child_node = Node(children_state, [children_path], children_cost)
                if child_node.state not in closed_list:
                    child_node.cost += current_node.cost
                    child_node.path = current_node.path + child_node.path
                    frontier.push(child_node, child_node.cost)
            closed_list.add(current_node.state)
    return False


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    frontier = util.PriorityQueue()
    frontier.push(Node(problem.getStartState(), [], 0), 0)
    closed_list = []
    while not frontier.isEmpty():
        current_node = frontier.pop()
        if problem.isGoalState(current_node.state):
            return current_node.path  # here is a deep first algorithm in a sense
        if current_node.state not in closed_list:
            closed_list.append(current_node.state)

            for child_state, child_path, child_cost in problem.getSuccessors(current_node.state):
                if problem.isGoalState(child_state):
                    return current_node.path + [child_path]
                frontier.push(Node(child_state, current_node.path + [child_path], current_node.cost + child_cost),
                              current_node.cost + child_cost + heuristic(child_state, problem))
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
