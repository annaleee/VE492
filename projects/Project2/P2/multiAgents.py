from util import manhattanDistance
from game import Directions
import random, util

from game import Agent


class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """

    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices)  # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"

        return successorGameState.getScore()


def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()


class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
        self.index = 0  # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)


class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"

        def max_value(state, depth, index):
            if state.isWin() or state.isLose() or depth == 0:
                return self.evaluationFunction(state)
            v = -float("inf")
            for each in state.getLegalActions(index):
                v = max(v, min_value(state.generateSuccessor(index, each), depth, index + 1))
            return v

        def min_value(state, depth, index):
            if state.isWin() or state.isLose() or depth == 0:
                return self.evaluationFunction(state)
            v = float("inf")
            for each in state.getLegalActions(index):
                if index == gameState.getNumAgents() - 1:
                    v = min(v, max_value(state.generateSuccessor(index, each), depth - 1, 0))
                else:
                    v = min(v, min_value(state.generateSuccessor(index, each), depth, index + 1))
            return v

        actions = gameState.getLegalActions(0)
        value = [min_value(gameState.generateSuccessor(0, each), self.depth, 1) for each in actions]
        return actions[value.index(max(value))]


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"

        def max_value(state, depth, index, alpha, beta):
            if state.isWin() or state.isLose() or depth == 0:
                return self.evaluationFunction(state)
            v = -float("inf")
            for each in state.getLegalActions(index):
                v = max(v, min_value(state.generateSuccessor(index, each), depth, index + 1, alpha, beta))
                if v > beta:
                    return v
                alpha = max(alpha, v)
            return v

        def min_value(state, depth, index, alpha, beta):
            if state.isWin() or state.isLose() or depth == 0:
                return self.evaluationFunction(state)
            v = float("inf")
            for each in state.getLegalActions(index):
                if index == gameState.getNumAgents() - 1:
                    v = min(v, max_value(state.generateSuccessor(index, each), depth - 1, 0, alpha, beta))
                else:
                    v = min(v, min_value(state.generateSuccessor(index, each), depth, index + 1, alpha, beta))
                if v < alpha:
                    return v
                beta = min(beta, v)
            return v

        actions = gameState.getLegalActions(0)
        alpha = -float("inf")
        beta = float("inf")
        values = []
        for each in actions:
            values.append(min_value(gameState.generateSuccessor(0, each), self.depth, 1, alpha, beta))
            alpha = max(alpha, values[values.index(max(values))])
        return actions[values.index(max(values))]


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"

        def Expectiminimax_value(state, depth, index):
            if state.isWin() or state.isLose() or depth == 0:
                return self.evaluationFunction(state)
            actions = state.getLegalActions(index)
            if index == state.getNumAgents() - 1:
                value = [Expectiminimax_value(state.generateSuccessor(index, each), depth - 1, 0) for each in
                         actions]
            else:
                value = [Expectiminimax_value(state.generateSuccessor(index, each), depth, index + 1) for each in
                         actions]
            if index == 0:
                return max(value)
            return sum(value) / len(value)

        actions = gameState.getLegalActions(0)
        value = [Expectiminimax_value(gameState.generateSuccessor(0, each), self.depth, 1) for each in actions]
        return actions[value.index(max(value))]


def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()


# Abbreviation
better = betterEvaluationFunction
