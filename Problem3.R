set.seed(2305)
add_circle=function(radius)
{
  xcoord=(radius/50)*c(-50:50)
  ycoord_pos=sqrt(radius^2-xcoord^2)
  ycoord_neg=-sqrt(radius^2-xcoord^2)
  points(xcoord,ycoord_pos,type='l',col='red')
  points(xcoord,ycoord_neg,type='l',col='red')
}

pdf_f=function(x)
{
  fx= (1/pi)*(1/sqrt(30^2-x^2)) +
    (1/(30*pi))*log(30+sqrt(30^2-x^2)) +
    (-1/(30*pi))*log(abs(x)) +
    (-1/(30*pi)) +
    (-x^2/(30*pi))*(1/(30+sqrt(30^2-x^2)))*
    (1/sqrt(30^2-x^2))
  fx
}
# Problem #
# (a)
theta_f = runif(500,min = 0,max = 2*pi) # Defines the RV theta_f ~ Unif(0,2pi), generating 500 samples within this RV.
r_f = runif(500,min = 0,max = 30) # Defines the RV R_f ~ Unif(0,2pi)

x_f = r_f * cos(theta_f)
y_f = r_f * sin(theta_f)
# Code above converts polar to cartesian coordinates
plot(x_f,y_f,xlim = c(-30,30),ylim= c(-30,30),main = "Flopsy's position on field") # Plots cartesian coordinates
add_circle(30)
# (b)
x_m = rep(0,500)
y_m = rep(0,500)
# Code above generates 500 empty elements to be filled in via the code below:
for(i in 1:500)
{
  repeat # Repeats below code until the equation x_cand^2+y_cand^2 <= 30^2 is satisfied
  {
    x_cand = runif(1,-30,30) # Generates a RV distributed uniformly between [-30,30]
    y_cand = runif(1,-30,30)
    if(x_cand^2+y_cand^2 <= 30^2)
    {
      x_m[i] = x_cand # Assigns x value to the above x_m
      y_m[i] = y_cand
      break # Breaks repeat once the 500 elements have been filled in.
    }
  }
}
plot(x_m,y_m,xlim = c(-30,30),ylim=c(-30,30), main = "Mopsy's position on field")
add_circle(30)
# (c)
# For Flopsy's position, after running the code several times I notice her positions are much denser in the central region of the circular field, whereas Mopsy's position is much more evenly spread out. Since Flopsy's position is uniform in polar coordinates, we imagine dividing the circle into rings of equal width. We know from r_f, each ring is equally likely since r_f is uniform. However, rings further from the centre have a larger area than ones closer. Since each ring has the same probability, the points seem to be more crowded in the smaller-area rings. For Mopsy, each unit of area simply has the same probability containing her.
# (d)
options(max.print=1000000)
theta_f_new = runif(10000,min = 0,max = 2*pi)
r_f_new = runif(10000,min = 0,max = 30)
x_f_new = r_f_new * cos(theta_f_new)
hist(x_f_new,xlim = c(-30,30), prob = TRUE,col = "lightgreen",main = "Distribution of Flopsy's x-coordinate") # Plots histogram of X_F
curve(pdf_f, add = TRUE,col ="darkgreen") # Superimposes pdf_f from Cottontail onto the distribution.
pdf_f(0) # Inf
# From above, as x tends to 0, the PDF tends to infinity.


# (e)
# Reusing code from (b):
X_M = rep(0,10000)
Y_M = rep(0,10000)
D = rep(0,10000)
for(i in 1:10000)
{
  R_F = runif(1,0,2*pi)
  THETA_F = runif(1,0,30)
  X_F = R_F * cos(THETA_F)
  Y_F = R_F * sin(THETA_F)
  repeat 
  {
    x_cand_new = runif(1,-30,30) 
    y_cand_new = runif(1,-30,30)
    if(x_cand_new^2+y_cand_new^2 <= 30^2)
    {
      X_M[i] = x_cand_new
      Y_M[i] = y_cand_new
      break 
    }
  }
  dist = sqrt((X_F-X_M)^2+(Y_F-Y_M)^2) # Uses Pythagoras' Theorem
  D[i] = dist
}
hist(D,xlab="Distance (m)",breaks = 30, prob = TRUE, main = "Distribution of distances between Flopsy and Mopsy",col="cyan")
expected_distance = mean(D)
expected_distance # For this seed, = 11.29314
# (f)
# (i)
Z = rep(0,10000)
for(i in 1:10000) # This loop basically defines Z as the indicator variable: if it is below 15, Z = 1, 0 otherwise.
{
  if(D[i]<15)
  {
    Z[i]=1
  } else
  {
    Z[i]=0
  }
}
# (ii)
prob_E = sum(Z)/10000 # Since the sum of Z simply means the sum of all times Flopsy and Mopsy are less than 15 m away from each other, we can use this and divide by the entire sample space, whihc is 10000 in this case.
prob_E # = 0.9101 for this seed.
# (iii)
sdphat = function(n,p)
{
  sd_phat = sqrt(p*(1-p)/n) 
  return(sd_phat)
}
sdphat(10000, prob_E) # This works since each simulation would be a Bernoulli trial, where success is if Flopsy and Mopsy are within 15m of each other. For this seed, = 0.002860384
# (iv)
# using our prob_E from (ii), we can obtain n from the equation sd(p)=sqrt(p(1-p)/n), where sd(p)=0.001. Rearranging, we get n = p(1-p)/(0.001)^2:
n = prob_E*(1-prob_E)/(0.001)^2
n # = 81817.99, or 81818 trials. 
sdphat(81818, prob_E) # Checking, and we get approx. 0.001!