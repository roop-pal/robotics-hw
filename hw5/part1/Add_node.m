function rrt = Add_node(rrt,cur,prev)

% input cur to node
node.p = cur;

% input prev to node
node.iPrev = prev;

% input node to rrt
rrt{end+1} = node;