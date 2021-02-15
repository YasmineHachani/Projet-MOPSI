import math
import numpy as np
from scipy import stats
from random import random




""" Computation of the two log-likelihoods"""

# tableau de mu et sigma, on doit déterminer type d'attaque 1 ou 2 pour chaque attaque de taille 0 à cmax ( dépendant de s)


def log_likelihood1(z, p,  m, size_c, mu, sigma):
    log_likelihood = 0
    size_c_fac = math.factorial(size_c)
    for i in range(m):
        sum = 0
        for k in range(size_c+1):
            p_k = (size_c_fac/(math.factorial(k)*math.factorial(size_c-k)))*(p[i]**k)*((1-p[i])**(size_c-k))
            sum += p_k*stats.norm.pdf(z[i], loc=mu[k], scale=sigma)
        if sum>0:
            log_likelihood += math.log(sum)
        else:
            print("PROBLEME")
    return log_likelihood


def log_likelihood2(z, p,m, size_c, theta, sigma):
    log_likelihood = 0
    size_c_fac = math.factorial(size_c)
    for i in range(m):
        s = 0
        for k in range(0,size_c + 1):
            p_k = ((size_c_fac/(math.factorial(k)*math.factorial(size_c-k)))*(p[i]**k)*((1-p[i])**(size_c-k)))
            #print("s",size_c, k, s, p_k,theta[k],z[i], sigma, stats.norm.pdf(z[i], loc=-1, scale=sigma))
            s += p_k*(theta[k]*stats.norm.pdf(z[i], loc=1, scale=sigma)+(1-theta[k])*stats.norm.pdf(z[i], loc=-1, scale=sigma))

        if s>0:
            log_likelihood += math.log(s)
        else:
            print("PROBLEME", size_c, k, theta, sigma)

    return log_likelihood


"""EM Algorithm for type I attacks just for one size"""


def proba_sachant(k,p, size_c):
    return (math.factorial(size_c) / (math.factorial(k) * math.factorial(size_c - k))) * (p ** k) * ((1 - p) ** (size_c - k))


def EM2(z, p, size_c, epsilon, theta_0, sigma_0,m ):

    print("size_c", size_c, sigma_0)
    U = np.ones((2*size_c+1, m))
    L1 = log_likelihood2(z, p, m, size_c, theta_0, sigma_0)
    L2 = L1 + 100*epsilon
    print("L1/L2", L1,L2)
    iterator=0
    size_c_fac = math.factorial(size_c)
    while abs(L1-L2) > epsilon:

        # E step
        for i in range(m):
            for k in range(-size_c,size_c+1):
                if k>=0:
                    U[k][i] = theta_0[k] * proba_sachant(k,p[i],size_c)* stats.norm.pdf(z[i], loc=1, scale=sigma_0)
                    print("size", size_c, i,k,theta_0[k], proba_sachant(k,p[i],size_c), stats.norm.pdf(z[i], loc=1, scale=sigma_0), sigma_0)
                else:
                    U[k][i] = (1-theta_0[k]) * proba_sachant(abs(k), p[i], size_c) * stats.norm.pdf(z[i], loc=-1, scale=sigma_0)
            div=sum(U[:,i])
            U[:,i] = U[:,i] /div

        # M step



        for k in range(1,size_c):

            result=sum(U[k])/sum(U[k]+U[-k])
            print("res", result)

            theta_0.append(result)


        theta_0[0] = 0
        theta_0[size_c] = 1
        s=0
        for i in range(m):
            for k in range(-size_c, size_c + 1):
                print("size2", size_c, U[k][i], z[i] , (z[i] - 2 * int(k>0) +1))
                s += U[k][i] * (z[i] - 2 * int(k>0) +1)**2
        sigma_0 = (1/m) * s
        print("sigma0", sigma_0)
        L1, L2 = log_likelihood2(z, p, m, size_c, theta_0, sigma_0), L1
        iterator += 1
    return L1, iterator, sigma_0, theta_0

def EM1(z, p, size_c, epsilon, mu_0, sigma_0,m ):
    T = np.ones((size_c+1, m))
    L1 = log_likelihood1(z, p, m, size_c, mu_0, sigma_0)
    L2 = L1 + 2*epsilon
    iterator=0
    size_c_fac = math.factorial(size_c)
    while abs(L1-L2) > epsilon:

        # E step
        for k in range(size_c+1):
            for i in range(m):
                s1 = 0
                for u in range(size_c+1):
                    p_u = (size_c_fac/(math.factorial(k)*math.factorial(size_c-u)))*(p[i]**u)*((1-p[i])**(size_c-u))
                    s1 += p_u*stats.norm.pdf(z[i], loc=mu_0[u], scale=sigma_0)
                p_k = (size_c_fac/(math.factorial(k)*math.factorial(size_c-k)))*(p[i]**k)*((1-p[i])**(size_c-k))
                T[k][i] = p_k*stats.norm.pdf(z[i], loc=mu_0[k], scale=sigma_0)/s1

        # M step
        for k in range(size_c+1):
            s2, s3 = 0, 0
            for i in range(m):
                s2 += T[k][i]*z[i]
                s3 += T[k][i]
            if k < size_c:
                assert(s3>0)
                mu_0[k] = s2/s3
        s4 = 0
        for k in range(size_c+1):
            for i in range(m):
                s4 += T[k][i]*(z[i]-mu_0[k])**2
        sigma_0 = math.sqrt(s4/m)
        #print(sigma_0)
        L1, L2 = log_likelihood1(z, p, m, size_c, mu_0, sigma_0), L1
        iterator+=1
    return L1, iterator, sigma_0

""" Generation of mu_0"""


def init_mu_0(size_c):
    mu_0 = [1]*(size_c+1)
    mu_0[0] = -1
    for i in range(1, size_c//2+1):
        mu_0[i] = 2*random()-1
        mu_0[size_c-i] = -mu_0[i]
    return mu_0

def init_theta_0(size_c):
    theta_0 = [1]*(size_c+1)
    theta_0[0] = 0
    for i in range(1, size_c//2+1):
        theta_0[i] = random()
        theta_0[size_c-i] = 1-theta_0[i]
    return theta_0


"""EM Algorithm for type I attacks returning a list"""


def EM1_list(z, p, epsilon, c_max, m):
    mu_list1 = list()
    sigma_list1 = list()
    log_likelihood_list1 = list()
    iterator_list=list()
    for size in range(1, c_max+1):
        mu_0 = init_mu_0(size)
        sigma_0 = random()/2+0.01
        L1, iterator, sigma_0 = EM1(z, p, size, epsilon, mu_0, sigma_0, m)
        mu_list1.append(mu_0)
        print("EM1", sigma_0)
        sigma_list1.append(sigma_0)
        log_likelihood_list1.append(L1)
        iterator_list.append(iterator)
    return mu_list1, sigma_list1, log_likelihood_list1, iterator_list

def EM2_list(z, p, epsilon, c_max, m):
    theta_list2 = list()
    sigma_list2 = list()
    log_likelihood_list2 = list()
    iterator_list=list()
    for size in range(1, c_max+1):
        theta_0 = init_theta_0(size)
        sigma_0 = 0.01
        L1, iterator, sigma_0, theta_0 = EM2(z, p, size, epsilon, theta_0, sigma_0, m)
        print("theta_0", theta_0)
        theta_list2.append(theta_0)
        sigma_list2.append(sigma_0)
        log_likelihood_list2.append(L1)
        iterator_list.append(iterator)
    return theta_list2, sigma_list2, log_likelihood_list2, iterator_list

# Listes des mu, sigma et log_likelihood pour chaque c dans [1,cmax_]




""" Size of a collusion """


def size_collusion(s):
    size = 0
    for colluder in s:
        if colluder > 0:
            size += 1
    return size


""" Computation of the posterior probabilities """


def post_proba1(z, s, m, secret_fingerprints, mu_list1, sigma_list1):
    p = 1
    size = size_collusion(s)
    if size > 0:
        for i in range(m):
            ki = 0
            for colluder in s:
                if colluder > 0:
                    ki += secret_fingerprints[colluder-1][i]
            p *= stats.norm.pdf(z[i], loc=mu_list1[size-1][ki], scale=sigma_list1[size-1])
    return p


def post_proba2(z, s, m, secret_fingerprints, theta_list2, sigma_list2):
    p = 1
    size = size_collusion(s)
    if size > 0:
        for i in range(m):
            ki = 0
            for colluder in s:
                if colluder > 0:
                    ki += secret_fingerprints[colluder-1][i]
            p *= (theta_list2[ki] * stats.norm.pdf(z[i], loc=1, scale=sigma_list2[size-1]) + (1 - theta_list2[size-1][ki]) * stats.norm.pdf(z[i], loc=-1, scale=sigma_list2[size-1]))
    return p


def post_proba(z, s, log_likelihood_list2, log_likelihood_list1):  # true --> I ; false --> II
    size = size_collusion(s)
    type_of_attack = log_likelihood_list2[size-1] < log_likelihood_list1[size-1]
    if type_of_attack:
        return post_proba1(z, s)
    else:
        return post_proba2(z, s)








