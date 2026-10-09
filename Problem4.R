# (a)
# Read in data values 

nfsold=
  c(  68.9, 142.3, 144.9,  89.1, 153.4,  96.2, 182.9,  94.0, 100.9,  49.1,
      128.5, 181.4, 119.2, 126.0, 165.4,  92.9, 132.2, 100.2, 125.3, 123.0,
      59.7, 125.6, 125.5, 163.8, 185.9, 361.1, 229.0,  58.7, 214.2,  74.5,
      202.1, 100.1,  78.7,  72.5,  98.6, 162.0, 133.9,  84.8,  76.8, 237.9,
      162.4, 297.8, 123.2, 125.4, 101.1,  71.7, 120.7, 143.6, 125.4, 101.9,
      142.9, 134.0, 135.5,  88.5,  89.4, 337.9, 132.5, 135.4,  88.0, 115.9,
      102.0, 156.0, 104.5, 133.3,  99.0, 139.0, 232.5, 184.1, 100.0, 288.3,
      196.6, 179.0, 160.3, 144.7, 128.8, 167.0, 160.2, 112.4, 134.1,  81.8,
      217.2, 154.6, 186.4,  45.5,  72.8, 103.6, 173.2,  67.5,  86.1, 123.6,
      90.8, 258.8, 168.2, 241.1, 129.3,  93.6, 133.6, 184.8, 138.8,  70.3,
      36.8, 106.3, 173.8, 125.9, 131.1, 104.6, 210.4, 161.2, 119.3, 178.7,
      113.6, 140.1, 153.4, 144.2, 105.7, 117.6,  82.7, 167.2, 151.5, 112.9,
      82.9, 182.2, 189.7,  76.4, 115.4, 211.3, 196.3,  83.4, 108.5, 113.2,
      127.3, 107.9, 149.2,  51.0,  72.3, 224.0, 160.0, 167.1, 132.9, 102.6,
      148.0, 178.4, 253.1, 195.1,  99.4,  66.2,  98.0,  67.7, 152.4, 267.3)
# In order to use the method of moments, we require the expectation of a given distribution.
# In this case, for the gamma(lambda,k) distribution, E(x) = k/lambda. Since we have two variables, we require two equations, so we could use E(X^2) = (k+1)k/lambda^2.
# Based on a sample of observed values x_1, ... , x_n, we use the fact that the mean (expectation) is (x_1+...+x_n)/n, and E(X^2) = (x_1^2+...+x_n^2)/n to find solutions for k and lambda.
# In this case, k/lambda = (x_1+...+x_n)/n, rearranging for k we get k = lambda*(x_1+...+x_n)/n. We can then substitute this into the following equation: (k+1)k/lambda^2 = (x_1^2+...+x_n^2)/n
# Now we get (using x_bar := (x_1+...+x_n)/n):
# lambda*x_bar(lambda*x_bar+1)/lambda^2 = (x_1^2+...+x_n^2)/n
# Rearranging we get lambda*(x_bar^2-(x_1^2+...+x_n^2)/n)=-x_bar
# Or lambda_hat = x_bar/((x_1^2+...+x_n^2)/n-x_bar^2)
# We can then use the original equation to find k_hat = lambda_hat*x_bar
nfsold_squared = nfsold^2
lambda_hat = mean(nfsold)/(mean(nfsold_squared)-mean(nfsold)^2)
k_hat = lambda_hat*mean(nfsold)
hist(nfsold,prob=TRUE,breaks=20,col="aquamarine",main = "Histogram of Daily Fish Sales with Fitted Gamma PDF",xlab = "Fish sold (kg)")
curve(dgamma(x,k_hat,lambda_hat),add=TRUE) # Superimposing PDF of fitted gamma distibution
# Comparing the curve to the histogram, it seems like the gamma distribution follows the histogram well. It captures the overall spread of the data, with minimal outliers.
# (b)
pp = c(1:length(nfsold))/151 # In order for Q-Q plots to work, we need to plot x_(k) against F_X^(-1)(k/(n+1)), so we are creating this vector to satisfy the latter part.
qq = qgamma(pp,shape=k_hat,rate=lambda_hat)
plot(qq,sort(nfsold),main="Q-Q plot with fitted Gamma distribution",xlab="Quantiles of gamma distribution",ylab="Ordered data")
curve(x*1,col="red",add=TRUE)
# Looking at the Q-Q plot, the points lie fairly close to the slope y=x, meaning the gamma distribution follows the data quite well. There are, however, data quite above the line near the end.
# (c)
# (i)
cost = function(n)
{
  if(n<=150)
  {
    return(n*5)
  }
  else
  {
    return(750+(n-150)*2.8) # 150*5=750, and if the weight is more than 150kg, the amount over 150 is multiplied by 2.8
  }
}

# (ii)
income = function(n,d)
{
  return(min(n,d)*9+max((n-d),0)*1) # Whatever is left over from demand is multiplied by 1.
}
# Note how I used min(n,d), since Rachel cannot sell more than she has stock. Similar case for max(n-d,0), since if d>n, there would absolutely be no more leftover.
# (iii)
avg.profit = function(n,k,lambda,nreps)
{
  profits = numeric(nreps)
  demand = rgamma(nreps,k,lambda)
  for(i in 1:nreps)
  {
    profits[i] = income(n,demand[i]) - cost(n)
  }

  return(mean(profits))
}
# Testing
cost(50) # Less than 150, return 50*5=250 which is what we wanted.
cost(150) # Boundary, equal to 150, returns 150*5=750, correct.
cost(200) # Returns 890=150*5+50*2.8, correct again.
income(200,150) # demand < purchase, returning 1400=150*9+50*1, correct.
income(200,200) # demand = purchase, returning 1800=200*9, correct.
income(200,250) # demand > purchase, returning 1800=200*9. Note that despite there being more demand, rachel cannot sell more than she physically has.
avg.profit(200,k_hat,lambda_hat,100) # Using k and lambda from part (a), we get 371.4208.
avg.profit(200,k_hat,lambda_hat,1000) # Returns 368.933.
avg.profit(200,k_hat,lambda_hat,10^7) # Returns 365.7574. Takes a while though!
avg.profit(400,k_hat,lambda_hat,1000) # Returns 55.70122. Expected since higher cost, and demand does not depend on n.

