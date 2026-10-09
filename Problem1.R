# Problem 1
# (a)
y = dbinom(0:100, 100,0.5) # Creates binomial RV and computes P(X=x) for all x.
x = 20:70
plot(x,y[20:70],ylab = "P(X=x)", xlab = "x", type="h", main = "PMF of X over the range 20-70") # Plots PMF from range 20-70 as required.
# (b)
E1 = pbinom(40, 100,0.5) # Uses pbinom, which finds P(X<=x).
E2 = 1-pbinom(29, 100,0.5) # same idea, but since E2 = {X≥70}, reverse to get E2 = 1-{X<30}=1-{X≤29}.
E1_alt = pbinom(40, 100,2/3) # Biased coin
E2_alt = 1-pbinom(29, 100,2/3)
E1 # p = 0.02844397
E2 # p = 0.9999839
E1_alt # p = 4.324019e-08
E2_alt # p = 1 (approx)
# (c) 
dbinom(40,100,0.5) # p = 0.01084387
dbinom(40,100,2/3) # p = 2.932636e-08
dbinom(70,100,0.5) # p = 2.317069e-05
dbinom(70,100,2/3) # p = 0.06728415
# Notice the probability of X = 40 for the fair coin is much more likely than the skewed one, whereas X = 70 has a higher probability for the biased coin. This implies Coin 1 is most likely a fair coin, and Coin 2 is most likely a biased coin.
# (d i)
# Question is asking what is the probability X = 0,2,4,6,8,10
X = dbinom(seq(0,10,by=2), 10,0.5) # Finds probability of above statement
sum(X) # Outputs probability = 0.5
# (d ii)
Y = dbinom(seq(0,10,by=2), 10,2/3)
sum(Y) # p = 0.5000085
###
# Problem 2 
# (a)
index = c(1:6)
tens = 10^index
eq = (1-1/tens)^tens
eq # for n = tens, eq = 0.3486784 0.3660323 0.3676954 0.3678610 0.3678776 0.3678793 respectively.
# (b)
# 1/eq = 2.867972 2.731999 2.719642 2.718418 2.718295 2.718283 for respective n.
# Taking the reciprocal, we notice as n increases, it becomes the reciprocal of e! Awesome!
# 1/eq -> 1/exp(1), n -> infty.
# (c)
p_dice_six = 1/6
p_card_A_space = 1/52
p_win = p_dice_six*p_card_A_space # since both events are independent. p = 1/312
p_no_wins = (1-p_win)^312 # p = 0.3672891
# We see 1/p_win = n = 312, so our probability satisfies the limit of (1-1/n)^n -> 1/exp(1).
# (d i)
# Since each year is independent of one another, we can multiply the union of all the probabilities:
p_5_year = p_no_wins^5 # p = 0.006684058
# (d ii)
# p_no_wins^5=(1-p_win)^(312*5)=(1-p_win)^1560. We see the probability is constant, with fixed number of trials, implying it followsa binomial distribution.
Z = rbinom(20, 1560,1/312) # Let Z be the number of eggs awarded over the five years.
plot(1:20,Z, xlab = "Realisation of Card-Die experiment", ylab = "Frequency", main = "Samples of eggs awarded per 5-year Experiment", type = "hist")
