# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util, time

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
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        #print "Info:"
        #time.sleep(1)
        #print gameState
        #print gameState.getFood()
        #print gameState.getPacmanPosition()
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = bestIndices[0] # Pick randomly among the best

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
        for move in successorGameState.getLegalActions():
          successorGameState2 = successorGameState.generatePacmanSuccessor(move)
          newPos2 = successorGameState2.getPacmanPosition()
          if successorGameState2.isLose():
            return successorGameState.getScore()-9999         


        #print "Food:"
        actPos = currentGameState.getPacmanPosition()
        foodPos=(0,0)
        x=0
        y=0
        for foodRows in newFood:
          x=x+1
          y=0
          for food in foodRows:
            y=y+1
            if food:
              foodPos=(x,y)
        #print "posicions"
        #print foodPos
        #print newPos
        #print actPos
        if( abs(foodPos[0]-newPos[0])<abs(foodPos[0]-actPos[0]) or abs(foodPos[1]-newPos[1])<abs(foodPos[1]-actPos[1])):
          return successorGameState.getScore()+5  
        else:
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

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
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
        """
        "*** YOUR CODE HERE ***"
        
        #print gameState
        legalMoves = gameState.getLegalActions(0)
        #print legalMoves
        scores = [self.minValue(gameState.generateSuccessor(0,action),0) for action in legalMoves]
        #print scores
        bestScore = max(scores)
        #print bestScore
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        #print bestIndices
        chosenIndex = random.choice(bestIndices)
        #chosenIndex = bestIndices[0]
        #print chosenIndex
        action = legalMoves[chosenIndex]
        return action
      
    def minValue(self, successorGameState, level):
      #print self.depth
      #print level
      if successorGameState.isWin() or successorGameState.isLose() or level==self.depth:
        return self.evaluationFunction(successorGameState)
        
      ghostIndices = [index for index in range(successorGameState.getNumAgents()) if index>0]
      gameStates = []
      for index in ghostIndices:
        if index==1:
          for action in successorGameState.getLegalActions(index):
            gameStates.append(successorGameState.generateSuccessor(index,action))
        else:
          gameStatesAux = []
          for game in gameStates:
            for action in game.getLegalActions(index):
              gameStatesAux.append(game.generateSuccessor(index,action))
          gameStates = gameStatesAux

      
      inf = float("inf")
      values=[inf]
      for game in gameStates:
        values.append(self.maxValue(game,level+1))
        
      return min(values)
      
    def maxValue(self, successorGameState, level):
      if successorGameState.isWin() or successorGameState.isLose() or level==self.depth:
        return self.evaluationFunction(successorGameState)
        
      legalMoves = successorGameState.getLegalActions(0)
      scores = [self.minValue(successorGameState.generateSuccessor(0,action),level) for action in legalMoves]
      
      inf = float("inf")
      scores.append(-inf)
      
      return max(scores)
      

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

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
        util.raiseNotDefined()

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
