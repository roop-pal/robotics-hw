%% RRT
% Yusuke Hayashi yh2886

% find a path using an RRT algorithm
%% initialization
clear ; close all; clc

%% input parameter
prompt = 'What is the distance that you will grow your tree at each iteration? ';
tree_dist = input(prompt)

%% start the code

% set start and goal locations
M = dlmread('start_goal.txt');
start = M(1,:);
goal = M(2,:);
obj.p = start;

% parameters
% max tree length
param.dist = tree_dist;
% threshold for goal to reach
param.thresh = 20;
% max iterations
param.max_itr = 100000;

% load obstacles
filename ='world_obstacles.txt';
rawdata = dlmread(filename);

% number of obstacles
num_obs = rawdata(1,1);

% initialize parameters to extract obstacles
num_vtx = rawdata(2,1);
st = 3;
obs = [];
st_m = 1;

figure;
hold on

% extract the obstacles and draw a map
for j=1:num_obs
    obs_coord = rawdata(st:(st+num_vtx(j))-1,:);
    obs_coord = [obs_coord; obs_coord(1,:)];
    
    plot([obs_coord(:,1)],[obs_coord(:,2)],'k','LineWidth',3);
    % reverse y axis
    ax = gca;
    ax.YDir = 'reverse';
    
    % structure for obstacles
    one.coord = obs_coord;
    one.num = num_vtx(j);
    obs.area(j) = one;
    
    st = st + num_vtx(j) + 1;
    if j~=num_obs
        num_vtx(j+1) = rawdata(st-1,1);
    end
end

% find the path
path = Find_path(obj,obs,param,start,goal);

% plot the path
for i=2:length(path)
    plot([path(i,1);path(i-1,1)],[path(i,2);path(i-1,2)],'g','LineWidth',1.5);
end

% draw start and end points
plot(obj.p(1,1),obj.p(1,2),'o', 'MarkerFaceColor', 'b', 'MarkerSize', 10);
plot(goal(1,1),goal(1,2),'o', 'MarkerFaceColor', 'r', 'MarkerSize', 10);

hold off