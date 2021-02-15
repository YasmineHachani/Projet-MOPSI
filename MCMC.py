import EM_algorithm as em
import math
import random
from copy import deepcopy
import numpy as np
from copy import deepcopy
from scipy import stats

def step_zero(estim_c,c_max,n):
    s=np.zeros(c_max)
    for i in range(estim_c):
        s[i]=random.randint(1,n)
    random.shuffle(s)
    return s

def neighboorhood(s,i,n):
    Neighbor=list()
    if s[i]==0:
        Neighbor.append(s)
        for j in range(1,n+1):
            if j not in s:
                s2= deepcopy(s)
                s2[i]=j
                Neighbor.append(s2)
    else:
        Neighbor.append(s)
        s2 = deepcopy(s)
        s2[i] = 0
        Neighbor.append(s2)
        for j in range(1, n + 1):
            if j not in s:
                s3 = deepcopy(s)
                s3[i] = j
                Neighbor.append(s3)
    return Neighbor

def size_collusion(s):
    size = 0
    for colluder in s:
        if colluder > 0:
            size += 1
    return size

def proba_s(c_max,size_s,n):
    n_fac=math.factorial(n)
    return (1/c_max) *n_fac/(math.factorial(size_s)*math.factorial(n-size_s))

def post_proba1(z,secret_fingerprint,s, m, mu_list, sigma):
    p = 1
    size_s=size_collusion(s)
    for i in range(m):
        ki = 0
        for colluder in s:
            if colluder > 0:
                ki += secret_fingerprint[int(colluder)-1][i]
        p *= stats.norm.pdf(z[i], loc=mu_list[size_s-1][ki], scale=sigma)
    return p

def distrib(p):
    cumul_p=[p[0]]
    for i in range(1,len(p)):
        cumul_p.append(p[i]+cumul_p[i-1])
    r=random.random()
    index_tirage=0
    while(r>cumul_p[index_tirage]):
        index_tirage+=1
    print("index", index_tirage)
    return index_tirage

def gibbs_sampler(z,secret_fingerprint,c_max,s,n,mu_list,sigma,m):
    i=random.randint(1,c_max-1)
    Neighbors=neighboorhood(s,i,n)
    p=list()
    for s_tilde in Neighbors:
        proba_s(c_max,size_collusion(s_tilde),n)
        p.append(proba_s(c_max,size_collusion(s_tilde),n)*post_proba1(z,secret_fingerprint,s_tilde,m,mu_list,sigma))
    p_norm=sum(p)
    p=np.array(p)/p_norm
    print(len(p))

    tirage=Neighbors[distrib(p)]
    return tirage


def algo(z,secret_fingerprint,c_max,n,mu_list,sigma,m,estim_c, T,K):
    s0=step_zero(estim_c,c_max,n)
    tirage = gibbs_sampler(z,secret_fingerprint,c_max,s0,n,mu_list,sigma,m)
    for t in range(T):
        tirage=gibbs_sampler(z,secret_fingerprint,c_max,tirage,n,mu_list,sigma,m)
        print("t",t,"tirage",tirage)
    markov_tirages=list()
    for t in range(K):
        tirage=gibbs_sampler(z,secret_fingerprint,c_max,tirage,n,mu_list,sigma,m)
        markov_tirages.append(tirage)
        print("t", t, "tirage", tirage)
    return markov_tirages


def margins(tirages,K,n):
    margin=list()
    for j in range(1,n+1):
        sum=0
        for k in range(K):
            if j in tirages[k]:
                sum+=1
        margin.append(sum/K)
    return margin




