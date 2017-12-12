%% Find_path_bi funcition
function path = Find_path(obj,obs,param,start,goal)
% find a path from start to goal
% input
%  obj: object structure
%  obs: obstacle structure
%  param: parameter structure
%  start: start position
%  goal: goal position
%
% output
%  path: a path from start to goal
%

global ITERATION

% initialize parameters
rrt = {};
rrt = Add_node(rrt,start,0);
path = [];
itr = 1;

while itr <= param.max_itr
    % create random point
    len = param.dist;
    theta = rand(1,1)*2*pi();    
    px = len * cos(theta);
    py = len * sin(theta);
   
    % select node
    for i=1:length(rrt)
        p = zeros(1,2);
        p(1,1) = rrt{i}.p(1,1) + px;
        p(1,2) = rrt{i}.p(1,2) + py;
        dist1 = norm(p - goal);
        if (i==1) || (dist1 < mindist)
            mindist = dist1;
            min_i = i;
        end
    end  
    
    p = zeros(1,2);
    p(1,1) = rrt{min_i}.p(1,1) + px;
    p(1,2) = rrt{min_i}.p(1,2) + py;
    
    if mod(itr,5)==0
        len_rrt = length(rrt);
        rn = randi([1 len_rrt]);
        p = zeros(1,2);
        p(1,1) = rrt{rn}.p(1,1) + px;
        p(1,2) = rrt{rn}.p(1,2) + py;
        min_i = rn;
    end
      
    % set object coordinate
    obj.p = p;
    
    % check a point in the image range
    img_x = [0; param.DX; param.DX; 0; 0];
    img_y = [0; 0; param.DY; param.DY; 0];
    obs_coord = [img_x, img_y];
    one.coord = obs_coord;
    img.area = one;
    flg = Collision_node(obj,img);
    
    % skip to next itr
    if flg == 0
        itr = itr + 1;
        continue
    end
    
    % check node collision
    flg = Collision_node(obj,obs);
    
    % skip to next itr
    if flg == 1
        itr = itr + 1;
        continue
    end
    
    %check if edge is valid
    flg = Collision_edge(obj,obs,p,rrt{min_i}.p);
    
    if flg == 1
        % if edge is not valid, skip to next itr
        itr = itr + 1;
        continue
    end
    
    % add p to rrt
    rrt = Add_node(rrt,p,min_i);
    
    % distance between the current node and the goal
    dist = norm(p - goal);
    fprintf('Nodes:   %d, Distance: %.1f, Iterations: %d\n',length(rrt),dist,itr)
    
    plot([p(1,1),rrt{min_i}.p(1,1)],[p(1,2),rrt{min_i}.p(1,2)],'m','LineWidth',3);
    if (dist < param.thresh)
        %check if edge is valid
        flg = Collision_edge(obj,obs,p,goal);
        
        % if edge is not valid, skip to next itr
        if flg == 1
            itr = itr + 1;
            continue
        end
        ITERATION = itr
        % add goal to rrt and exit with success
        rrt = Add_node(rrt,goal,length(rrt));
        
        % construct the shortest path
        i = length(rrt);
        path = rrt{i}.p;
        while 1
            i = rrt{i}.iPrev;
            if i == 0
                return
            end
            path = [rrt{i}.p; path];
        end
    end
    
    itr = itr + 1;
end