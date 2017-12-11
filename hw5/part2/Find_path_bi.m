%% Find_path_bi funcition
function [path, path2] = Find_path_bi(obj,obs,param,start,goal)
% find a path from start to goal using bi-directional approach
% input
%  obj: object structure
%  obs: obstacle structure
%  param: parameter structure
%  start: start position
%  goal: goal position
%
% output
%  path: a path from start
%  path2: a path from goal
%

global ITERATION

% initialize parameters
% rrt from the start
rrt = {};
rrt = Add_node(rrt,start,0);
flg_r1 = 0;
p_a = [];

% rrt from the goal
rrt2 = {};
rrt2 = Add_node(rrt2,goal,0);
flg_r2 = 0;
p2_a = [];

% path from the start
path = [];
% path from tne goal
path2 = [];
itr = 1;

while itr <= param.max_itr
    %% the tree from start
    
    if flg_r1==0
        % create random point
        p = rand(1,2);
        p(1,1) = p(1,1)*600;
        p(1,2) = p(1,2)*600;
        
        % set object coordinate
        obj.p = p;
        flg = Collision_node(obj,obs);
        
        % skip to next itr
        if flg == 1
            itr = itr + 1;
            continue
        end
        
        % if coordinate is valid
        for i=1:length(rrt)
            dist1 = norm(rrt{i}.p - p);
            if (i==1) || (dist1 < mindist)
                mindist = dist1;
                min_i = i;
                l = rrt{i}.p;
            end
        end
        
        %check if edge is valid
        flg = Collision_edge(obj,obs,p,l);
        
        if flg == 1 || (dist1 > param.dist)
            % if edge is not valid, skip to next itr
            itr = itr + 1;
            continue
        end
        
        % add p to rrt
        rrt = Add_node(rrt,p,min_i);
        
        plot([p(1,1),rrt{min_i}.p(1,1)],[p(1,2),rrt{min_i}.p(1,2)],'m','LineWidth',3);
        flg_r1 = 1;
        p_a = [p_a; p];
        pc_a = repmat(p,size(p_a,1),1);
    end
    
    %% the tree from goal
    
    if flg_r2==0
        % create random point
        p2 = rand(1,2);
        p2(1,1) = p2(1,1)*600;
        p2(1,2) = p2(1,2)*600;
        
        % set object coordinate
        obj.p2 = p2;
        flg = Collision_node(obj,obs);
        
        % skip to next itr
        if flg == 1
            itr = itr + 1;
            continue
        end
        
        % if coordinate is valid
        for i=1:length(rrt2)
            dist2 = norm(rrt2{i}.p - p2);
            if (i==1) || (dist2 < mindist)
                mindist = dist2;
                min_i = i;
                l = rrt2{i}.p;
            end
        end
        
        %check if edge is valid
        flg = Collision_edge(obj,obs,p2,l);
        
        if flg == 1 || (dist2 > param.dist)
            % if edge is not valid, skip to next itr
            itr = itr + 1;
            continue
        end
        
        % add p to rrt
        rrt2 = Add_node(rrt2,p2,min_i);
        
        p2_a = [p2_a; p2];
        pc2_a = repmat(p2,size(p2_a,1),1);
        
        % distance between the rrt1 and rrt2
        diff = p_a - pc2_a;
        dist_c2 = (diff.*diff).^(1/2);
        dist_min_c2 = min(dist_c2(:));
        
        diff = p2_a - pc_a;
        dist_c = (diff.*diff).^2;
        dist_min_c = min(dist_c(:));
        
        % find the minimum distance
        if dist_min_c2 < dist_min_c
            dist = dist_min_c2;
            ind = find(dist_min_c2==dist);
            pp = p_a(ind,:);
            pp2 = p2;
        else
            dist = dist_min_c;
            ind = find(dist_min_c==dist);
            pp = p;
            pp2 = p2_a(ind,:);
        end

        fprintf('Nodes:   %d, Distance: %.1f, Iterations: %d\n',length(rrt),dist,itr)
        
        plot([p2(1,1),rrt2{min_i}.p(1,1)],[p2(1,2),rrt2{min_i}.p(1,2)],'b','LineWidth',3);
        flg_r2 = 1;
    end
    
    %% merge the trees when they meet
    if (dist < param.thresh)
        %check if edge is valid
        flg = Collision_edge(obj,obs,p,p2);
        
        % if edge is not valid, skip to next itr
        if flg == 1
            itr = itr + 1;
            flg_r1 = 0;
            flg_r2 = 0;
            continue
        end
        ITERATION = itr
        % add p2 to rrt and p to rrt2, respectively
        rrt = Add_node(rrt,p2,length(rrt));
        rrt2 = Add_node(rrt2,p,length(rrt2));
        
        % construct the shortest path fromt the start
        i = length(rrt);
        path = rrt{i}.p;
        while 1
            i = rrt{i}.iPrev;
            if i == 0
                break
            end
            path = [rrt{i}.p; path];
        end
        
        % construct the shortest path from the goal and exit with success
        i = length(rrt2);
        path2 = rrt2{i}.p;
        while 1
            i = rrt2{i}.iPrev;
            if i == 0
                return
            end
            path2 = [rrt2{i}.p; path2];
        end
    end
    
    itr = itr + 1;
    flg_r1 = 0;
    flg_r2 = 0;
end