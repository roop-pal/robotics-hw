function path = Find_path(obj,obs,param,start,goal)

global ITERATION

% initialize parameters
rrt = {};
rrt = Add_node(rrt,start,0);
path = [];
itr = 1;

while itr <= param.max_itr
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
    
    % distance between the current node and the goal
    dist = norm(p-goal);
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