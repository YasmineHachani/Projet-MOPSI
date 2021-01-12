import math
import numpy as np
from scipy import stats
from random import random

""" Constant variables """
n_ = 20
m_ = 3000
c_max_ = 10
secret_fingerprints_ = list()

z_ = list()
p_ = list()
epsilon_ = 10**-3


""" Computation of the two log-likelihoods"""

# tableau de mu et sigma, on doit déterminer type d'attaque 1 ou 2 pour chaque attaque de taille 0 à cmax ( dépendant de s)


def log_likelihood1(z, p, size_c, mu, sigma):
    log_likelihood = 0
    size_c_fac = math.factorial(size_c)
    for i in range(m_):
        s = 0
        for k in range(size_c+1):
            p_k = (size_c_fac/(math.factorial(k)*math.factorial(size_c-k)))*(p[i]**k)*((1-p[i])**(size_c-k))
            s += p_k*stats.norm.pdf(z[i], loc=mu[k], scale=sigma)
        #print("s : ", s)
        log_likelihood += math.log(s)
    return log_likelihood


def log_likelihood2(z, p, size_c, theta, sigma):
    log_likelihood = 0
    size_c_fac = math.factorial(size_c)
    for i in range(m_):
        s = 0
        for k in range(size_c + 1):
            p_k = (size_c_fac/(math.factorial(k)*math.factorial(size_c-k)))*(p[i]**k)*((1-p[i])**(size_c-k))
            s += p_k*(theta[k]*stats.norm.pdf(z[i], loc=1, scale=sigma)+(1-theta[k])*stats.norm.pdf(z[i], loc=-1, scale=sigma))
        log_likelihood += math.log(s)
    return log_likelihood


"""EM Algorithm for type I attacks just for one size"""


def EM1(z, p, size_c, epsilon, mu_0, sigma_0):
    T = np.ones((size_c+1, m_))
    L1 = log_likelihood1(z, p, size_c, mu_0, sigma_0)
    L2 = L1 + 2*epsilon
    size_c_fac = math.factorial(size_c)
    while abs(L1-L2) > epsilon:

        # E step
        for k in range(size_c+1):
            for i in range(m_):
                s1 = 0
                for u in range(size_c+1):
                    p_u = (size_c_fac/(math.factorial(u)*math.factorial(size_c-u)))*(p[i]**u)*((1-p[i])**(size_c-u))
                    s1 += p_u*stats.norm.pdf(z[i], loc=mu_0[u], scale=sigma_0)
                p_k = (size_c_fac/(math.factorial(k)*math.factorial(size_c-k)))*(p[i]**k)*((1-p[i])**(size_c-k))
                T[k][i] = p_k*stats.norm.pdf(z[i], loc=mu_0[k], scale=sigma_0)/s1

        # M step

        for k in range(size_c+1):
            s2, s3 = 0, 0
            for i in range(m_):
                s2 += T[k][i]*z[i]
                s3 += T[k][i]
            if k < size_c:
                mu_0[k] = s2/s3
        s4 = 0
        for k in range(size_c+1):
            for i in range(m_):
                s4 += T[k][i]*(z[i]-mu_0[k])**2
        sigma_0 = math.sqrt(s4/m_)

        # Update
        # print(" sigma decode : ", sigma_0, " ; mu_0 :", mu_0)
        L1, L2 = log_likelihood1(z, p, size_c, mu_0, sigma_0), L1
    return L1, sigma_0


""" Generation of mu_0"""


def init_mu_0(size_c):
    mu_0 = [1]*(size_c+1)
    mu_0[0] = -1
    for i in range(1, size_c//2+1):
        mu_0[i] = 2*random()-1
        mu_0[size_c-i] = -mu_0[i]
    return mu_0


"""EM Algorithm for type I attacks returning a list"""


def EM1_list(z, p, epsilon):
    mu_list1 = list()
    sigma_list1 = list()
    log_likelihood_list1 = list()
    for size in range(1, c_max_+1):
        mu_0 = init_mu_0(size)
        sigma_0 = random()
        L1, sigma_0 = EM1(z, p, size, epsilon, mu_0, sigma_0)
        mu_list1.append(mu_0)
        sigma_list1.append(sigma_0)
        log_likelihood_list1.append(L1)
    return mu_list1, sigma_list1, log_likelihood_list1

# Listes des mu, sigma et log_likelihood pour chaque c dans [1,cmax_]


mu_list1_, sigma_list1_, log_likelihood_list1_ = EM1_list(z_, p_, epsilon_)
theta_list2_, sigma_list2_, log_likelihood_list2_ = list(), list(), list()


""" Size of a collusion """


def size_collusion(s):
    size = 0
    for colluder in s:
        if colluder > 0:
            size += 1
    return size


""" Computation of the posterior probabilities """


def post_proba1(z, s):
    p = 1
    size = size_collusion(s)
    if size > 0:
        for i in range(m_):
            ki = 0
            for colluder in s:
                if colluder > 0:
                    ki += secret_fingerprints_[colluder-1][i]
            p *= stats.norm.pdf(z[i], loc=mu_list1_[size-1][ki], scale=sigma_list1_[size-1])
    return p


def post_proba2(z, s):
    p = 1
    size = size_collusion(s)
    if size > 0:
        for i in range(m_):
            ki = 0
            for colluder in s:
                if colluder > 0:
                    ki += secret_fingerprints_[colluder-1][i]
            p *= (theta_list2_[ki] * stats.norm.pdf(z[i], loc=1, scale=sigma_list2_[size-1]) + (1 - theta_list2_[size-1][ki]) * stats.norm.pdf(z[i], loc=-1, scale=sigma_list2_[size-1]))
    return p


def post_proba(z, s):  # true --> I ; false --> II
    size = size_collusion(s)
    type_of_attack = log_likelihood_list2_[size-1] < log_likelihood_list1_[size-1]
    if type_of_attack:
        return post_proba1(z, s)
    else:
        return post_proba2(z, s)








