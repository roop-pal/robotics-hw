%% In_region funcition
function in = In_region(x,y,x_obs,y_obs)
% check if test points in region
% input
%  x: x coordinates of test points
%  y: y coordinates of test points
%  x_obs: x coordinates of obstacles
%  y_obs: y coordinates of obstacles
%
% output
%  in: if 1, inside
%      else, outside
%

% the number of nodes for obstacles
n  = size(x_obs,1);

% compute the size of x
x_size = size(x);
m = x_size(1,1);

x = x';
y = y';

% obs vectors starting from the test points
x_obs = repmat(x_obs,1,m) - repmat(x,n,1);
y_obs = repmat(y_obs,1,m) - repmat(y,n,1);

ind = 1:n-1;

% cross product of adjacent vectors
cp = x_obs(ind,:) .* y_obs(ind+1,:) - x_obs(ind+1,:) .* y_obs(ind,:);

x_obs(x_obs<=0) = 0;
y_obs(y_obs<=0) = 0;

% compute the quadrant changes
diff_q = diff((~x_obs & y_obs) + 2*(~x_obs & ~y_obs) + 3*(x_obs & ~y_obs));
diff_q(find(diff_q==3)) = -1;
diff_q(find(diff_q==-3)) =  1;

% check if the points are inside the obstacles
sign_cp = sign(cp);
diff_q = diff_q + (2*sign_cp - diff_q ).*(abs(diff_q)==2);
diff_q(find(isnan(diff_q))) = 0;

in(sum(diff_q,1)==0) = 0;
in(sum(diff_q,1)~=0) = 1;

% reshape output
in = reshape(in,x_size);
