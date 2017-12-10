function flg = Collision_edge(rob,obs,p1,p2)

% initialize flg
flg = 0;

% calculate the slope and the y intersept for linear equation
a = (p1(1,2)-p2(1,2))/(p1(1,1)-p2(1,1));
b = p1(1,2) - a*(p1(1,1));

if abs(b) < 1000 || abs(a) < 10
    % set object coordinates
    n = norm([p1(1,1)-p2(1,1),0]);
    x = linspace(p1(1,1),p2(1,1),n);
    y = a*x + b;
else % if a or b is a large value
    % set object coordinates
    n = norm([0, p1(1,2)-p2(1,2)]);
    y = linspace(p1(1,2),p2(1,2),n);
    x = 1/a * (y - b);
end

p = [x', y'];
rob.p = p;

% check if an edge intersects objects
flg = Collision_node(rob,obs);

if flg == 1
    return;
end
