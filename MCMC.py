import EM_algorithm as em
import math
from random import randint
from copy import deepcopy

""" Constant variables """
n_ = 20
fact_n_ = math.factorial(n_)
m_ = 3000
c_max_ = 10
T_ = 100
K_ = 500

""" It returns the list of P(s'|z) where s' is a neighbor of s. neighborhood_proba_list[k] = P(s'|z) if s[i] = k """


def neighborhood_proba_list(z, s, i): # proba à 0 pour l'indice correspondant exactement à s
    proba_list = [0]*(n_ + 1)
    size = em.size_collusion(s)
    for k in range(n_ + 1):
        s_copy = deepcopy(s)
        if k != s[i]:
            if s[i] == 0:
                s_size = size + 1
            elif k == 0:
                s_size = size - 1
            else:
                s_size = size
            s_copy[i] = k
            coeff = (c_max_*fact_n_/(math.factorial(s_size)*math.factorial(n_ - s_size)))**-1
            proba_list[k] += em.post_proba(z, s_copy)*coeff
    return proba_list


""" Markov chain process"""


def markov_chain(z, s0):
    collusions = list()

    for t in range(T_+K_):
        i = randint(1, c_max_)
        neighborhood_list = neighborhood_proba_list(z, s0, i)
        sum_proba = sum(neighborhood_list)

        # Choice of the best s(t+1)
        proba_opt, index_opt = 0, -1
        for k in range(len(neighborhood_list)):
           proba= neighborhood_list[k]/sum_proba
           if proba > proba_opt:
               proba_opt, index_opt = proba, k
        s0[i] = index_opt
        if t >= T_-1:
            collusions.append(s0)
    return collusions


""" Return whether or not the person number j is in the collusion s """


def in_collusion(s, j):
    for k in s:
        if k == j:
            return True
    return False


""" Return the approach marginals list compute thanks to a list of collusions """


def monte_carlo(collusions):
    marginals_list = [0]*n_
    for j in range(1, n_+1):
        frequency = 0
        for s in collusions:
            if in_collusion(s, j):
                frequency += 1
        marginals_list[j-1] = frequency/collusions.size()
    return marginals_list







