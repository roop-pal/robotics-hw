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
        
        if mod(itr,2)==0
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
        flg_r1 = 1;
        p_a = [p_a; p];
        pc_a = repmat(p,size(p_a,1),1);
    end
    
    %% the tree from goal
    
    if flg_r2==0
        % create random point
        len = param.dist;
        theta2 = rand(1,1)*2*pi();
        px2 = len * cos(theta2);
        py2 = len * sin(theta2);
        
        % select node
        for i=1:length(rrt2)
            p2 = zeros(1,2);
            p2(1,1) = rrt2{i}.p(1,1) + px2;
            p2(1,2) = rrt2{i}.p(1,2) + py2;
            dist2 = norm(p2 - start);
            if (i==1) || (dist2 < mindist)
                mindist = dist2;
                min_i = i;
            end
        end
        
        p2 = zeros(1,2);
        p2(1,1) = rrt2{min_i}.p(1,1) + px2;
        p2(1,2) = rrt2{min_i}.p(1,2) + py2;
        
        if mod(itr,2)==0
            len_rrt2 = length(rrt2);
            rn = randi([1 len_rrt2]);
            p2 = zeros(1,2);
            p2(1,1) = rrt2{rn}.p(1,1) + px2;
            p2(1,2) = rrt2{rn}.p(1,2) + py2;
            min_i = rn;
        end
        
        % set object coordinate
        obj.p = p2;
        
        % check a point in the image range
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
        flg = Collision_edge(obj,obs,p2,rrt2{min_i}.p);
        
        if flg == 1
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
            flg_m = 0;
            flg_b = 1;
        else
            dist = dist_min_c;
            ind = find(dist_min_c==dist);
            pp = p;
            pp2 = p2_a(ind,:);
            flg_m = 1;
            flg_b = 0;
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
        
        if flg_m==1
            plot([p2(1,1),p(1,1)],[p2(1,2),p(1,2)],'m','LineWidth',3);
        else
            plot([p2(1,1),p(1,1)],[p2(1,2),p(1,2)],'b','LineWidth',3);
        end
              
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