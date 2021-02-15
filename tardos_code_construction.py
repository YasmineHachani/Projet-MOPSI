import numpy as np
from random import random

""" Constant variables """
n = 100
m = 120
c_max = 10
t = 1 / (300 * c_max)


def tardos_distribution(p):
    """ distribution according to which (pi) are independent and identically drawn"""
    if t <= p <= 1 - t:
        indicator = 1
    else:
        indicator = 0
    kappa_t = 1 / (2 * (np.arcsin(np.sqrt(1 - t)) - np.arcsin(np.sqrt(t))))
    return indicator * kappa_t / (np.sqrt(p * (1 - p)))


def random_variable_p(number_bits):
    """ use inversion of the repartition function """
    p = list()
    kappa_t = 1 / (2 * (np.arcsin(np.sqrt(1 - t)) - np.arcsin(np.sqrt(t))))
    for i in range(number_bits):
        p.append(np.sin(random() / (2 * kappa_t) + np.arcsin(np.sqrt(t))) ** 2)
    return p


def users_fingerprints(number_users, number_bits, p_list):
    """ creates n fingerprints of m bits according to the auxiliary sequence p"""
    fingerprints = list()
    for i in range(number_users):
        x_user = list()
        for j in range(number_bits):
            p_test = random()
            if p_test <= p_list[j]:
                x_user.append(1)
            else:
                x_user.append(0)
        fingerprints.append(x_user)
    return fingerprints




