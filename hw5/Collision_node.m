function flg = Collision_node(rob,obs)

global COUNT;
COUNT = COUNT + 1;

% initialize flg
flg = 0;
num_obs = numel(obs.area);

for j=1:num_obs 
    % check whether object point is located inside or not
    [in, on] = inpolygon(rob.p(:,1),rob.p(:,2),obs.area(j).coord(:,1),obs.area(j).coord(:,2));
    if any(in==1) || any(on==1)
        flg = 1;
        return;
    end
end

