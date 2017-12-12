%% Colligion_node funcition
function flg = Collision_node(obj,obs)
% check node collisions
% input
%  obj: object structure
%  obs: obstacle structure
%
% output
%  flg: if points of objects are inside, 1
%       else, 0
%

global COUNT;
COUNT = COUNT + 1;

% initialize flg
flg = 0;

% compute number of obstacles
num_obs = numel(obs.area);

for j=1:num_obs 
    % check whether object point is located inside or not
    in = In_region(obj.p(:,1),obj.p(:,2),obs.area(j).coord(:,1),obs.area(j).coord(:,2));
    if any(in==1)
        flg = 1;
        return;
    end
end

