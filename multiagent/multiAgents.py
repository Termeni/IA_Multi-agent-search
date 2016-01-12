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

INF = float("inf")

class RandomAgent(Agent):
    def getAction(self, gameState):
      legalMoves = gameState.getLegalActions(self.index)
      chosenMove = random.choice(legalMoves)
      return chosenMove

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
    #return manhattanDistance(currentGameState.getPacmanPosition(),currentGameState.getGhostPosition(1))
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
        return self.minimax(gameState, self.depth, 0)[1]
      
    def minimax(self, gameState, depth, agentIndex):
      if depth == 0 or gameState.isWin() or gameState.isLose():
         return (self.evaluationFunction(gameState), )

      childNodes = [(gameState.generateSuccessor(agentIndex,action),action) for action in gameState.getLegalActions(agentIndex)]

      if agentIndex==0:
        maximizingPlayer = True
      else:
        maximizingPlayer = False

      if agentIndex == gameState.getNumAgents()-1:
        depth = depth-1
        agentIndex = 0
      else:
        agentIndex = agentIndex +1

      if maximizingPlayer:
        values = [((self.minimax(child[0], depth, agentIndex)[0]),child[1]) for child in childNodes]
        return max(values)

      else:
        values = [((self.minimax(child[0], depth, agentIndex)[0]),child[1]) for child in childNodes]
        return min(values)
        

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        return self.alphaBeta(gameState, self.depth, 0, (-INF,), (INF,))[1]
        
    def alphaBeta(self, gameState, depth, agentIndex, alpha, beta):
      if depth == 0 or gameState.isWin() or gameState.isLose():
         return self.evaluationFunction(gameState)

      if agentIndex==0:
        maximizingPlayer = True
      else:
        maximizingPlayer = False

      if agentIndex == gameState.getNumAgents()-1:
        newDepth = depth-1
        newAgentIndex = 0
      else:
        newAgentIndex = agentIndex +1
        newDepth = depth

      

      if maximizingPlayer:
        for action in gameState.getLegalActions(agentIndex):
          successorGameState = gameState.generateSuccessor(agentIndex,action) 
          crida = (self.alphaBeta(successorGameState, newDepth, newAgentIndex, alpha, beta),action)
          if isinstance(crida[0],tuple):
            if crida[0] == beta:
              return beta
            if crida[0] == alpha:
              return alpha
            cridaTmp = crida[0][0],action
            crida = cridaTmp
          if crida[0] >= alpha[0]:
            alpha = crida
          if alpha > beta:
            return alpha
        return alpha

      else:
        for action in gameState.getLegalActions(agentIndex):
          successorGameState = gameState.generateSuccessor(agentIndex,action) 
          crida = (self.alphaBeta(successorGameState, newDepth, newAgentIndex, alpha, beta),action)
          if isinstance(crida[0],tuple):
            if crida[0] == alpha:
              return alpha
            if crida[0] == beta:
              return beta
            cridaTmp = crida[0][0],action
            crida = cridaTmp
          if crida[0] < beta[0]:
            beta = crida
          if beta < alpha:
            return beta
        return beta
        
    """
   Your minimax agent with alpha-beta pruning (question 3)
  def alphaBeta(self, gameState, depth, agentIndex=0, alpha=(-INF,), beta=(INF,)):
    
      Return the best choice (score, action) for the current agent.
      If agentIndex == 0 it is a max node, otherwise it is a min node.
    
    #: check if the game ends, or we reach the depth
    if gameState.isWin() or gameState.isLose() or depth == 0:
      #: return (current_score, )
      return ( self.evaluationFunction(gameState), )

    numAgents = gameState.getNumAgents()
    #: if current agent is the last agent in game, decrease the depth
    newDepth = depth if agentIndex != numAgents - 1 else depth - 1
    newAgentIndex = (agentIndex + 1) % numAgents

    if(agentIndex == 0):    #: max node
      v = (-INF, )
      for a in gameState.getLegalActions(agentIndex):
        nextState = gameState.generateSuccessor(agentIndex, a)
        v = max([v, (self.alphaBeta(nextState, newDepth, newAgentIndex, alpha, beta)[0], a)])
        if v > beta:
          return v
        alpha = max([alpha, v])
      return v

    else:                   #: min node
      v = (INF, )
      for a in gameState.getLegalActions(agentIndex):
        nextState = gameState.generateSuccessor(agentIndex, a)
        v = min([v, (self.alphaBeta(nextState, newDepth, newAgentIndex, alpha, beta)[0], a)])
        if alpha > v:
          return v
        beta = min([beta, v])
      return v

  def getAction(self, gameState):
    
      Returns the minimax action using self.depth and self.evaluationFunction
    
    "*** YOUR CODE HERE ***"
    s = self.alphaBeta(gameState, self.depth)
    print "SCORE", s[0]
    return s[1]
    """
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
