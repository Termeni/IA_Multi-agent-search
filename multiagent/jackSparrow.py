from pacman import GameState
from layout import *
from multiAgents import *

x = GameState()

layoutText = """
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%                                 %
% % % %%% % %%%%   %%%% % %%% % % %
% % %     % %  %% %%  % %     % % %
% % %   % % %         % % %   % % %
% % %%% % % % %%% %%% % % % %%% % %
%       % % %         % % %       %
% %%% % %   % %%   %% %   % % %%% %
%       % % %   % %   % % %       %
% %%%%    % % %     % % %    %%%% %
% %       %     % %     %       % %
%   %%%%  % %%%%% %%%%% %  %%%%   %
% %%%     %             %     %%% %
%     %%%    %%%   %%%    %%%     %
%   %    %               %    %   %
% %%% %% %%%%%%%% %%%%%%%% %% %%% %
%                                 %
% %% % % %%%% %%% %%% %%%% % % %% %
%    % %    % %  G  % %    % %    %
% %% % % %    %     %    % % % %% %
%      % % %% %     % %% % %      %
%  %%%%% % %  %%%%%%%  % % %%%%%  %
%          %     P     %          %
%  %%%% %  %  %%% %%%  %  % %%%%  %
% %     %% %           % %%     % %
% % %%        % % % %        %% % %
%       % %%% % % % % %%% %       %
% % %%%       % % % %       %%% % %
% %     %     %     %     %     % %
% % %%  %%% % %     % % %%%  %% % %
%         %             %         %
%  %%%%%  %%%%%%% %%%%%%%  %%%%%  %
% %%   % %      % %      % %   %% %
%                                 %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
"""

numGhosts = layoutText.count('G')

layoutText = layoutText.split('\n')
layoutText = filter(None,layoutText)

layout = Layout(layoutText)

x.initialize(layout,numGhosts);
agent = MinimaxAgent()
agent.index=1

randomAgent = RandomAgent()
randomAgent.index = 1

reflexAgent = ReflexAgent()
reflexAgent.index = 1

minimaxAgent = MinimaxAgent()
minimaxAgent.depth = 2
minimaxAgent.index = 1


alphabetaAgent = AlphaBetaAgent()
alphabetaAgent.depth = 4
alphabetaAgent.index = 1

print minimaxAgent.getAction(x)

#print reflexAgent.getAction(x)

#print randomAgent.getAction(x)

#print x.getLegalActions(0)
#print x.getLegalActions(1)

#print agent.getAction(x)

#print x

#print max([(1,"Salma hayek"),(2,"cerveza"),(3,"corazon"),(0,"Marimorena")])