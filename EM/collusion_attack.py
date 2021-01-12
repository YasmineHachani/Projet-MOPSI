import tardos_code_construction as tcc
from random import gauss, random

""" Constant variables """
n_ = 20
m_ = 3000
c_max_ = 10
t_ = 1 / (300 * c_max_)

""" Choice of the collusion """
c_ = [6, 0, 3, 2, 0]

""" Creation of the secret p and the secret fingerprints"""
secret_p_ = tcc.random_variable_p(m_)
secret_fingerprints_ = tcc.users_fingerprints(n_, m_, secret_p_)

"""ATTACK OF TYPE 1: AVERAGE AND AVERAGE2"""


def attack_function_average_without_noise(k, size_c):
    return 2 * k / size_c - 1


def attack_function_average(k, size_c, sigma):
    n = gauss(0, sigma ** 2)
    return 2 * k / size_c - 1 + n


def attack_function_average2(k, size_c, sigma):
    n = gauss(0, sigma ** 2)
    if k == size_c:
        return 1 + n
    if k == 0:
        return -1 + n
    return n


def fusion_chunks(c, secret_fingerprints):
    fingerprints_merged = [0 for i in range(m_)]
    len_of_collusion = 0
    for i in range(m_):
        for index_c in c:
            if index_c > 0:
                if i == 0:
                    len_of_collusion += 1
                """ We only make the collusion on the actual colluders whose index are > 1"""
                fingerprints_merged[i] += secret_fingerprints[index_c - 1][i]

    return fingerprints_merged, len_of_collusion


def attack_i_average(c, secret_fingerprints, sigma):
    fingerprints_merged, len_of_collusion = fusion_chunks(c, secret_fingerprints)
    for i in range(m_):
        fingerprints_merged[i] = attack_function_average(fingerprints_merged[i], len_of_collusion, sigma)
    return fingerprints_merged


def attack_i_average2(c, secret_fingerprints, sigma):
    fingerprints_merged, len_of_collusion = fusion_chunks(c, secret_fingerprints)
    for i in range(m_):
        fingerprints_merged[i] = attack_function_average2(fingerprints_merged[i], len_of_collusion, sigma)
    return fingerprints_merged


"""ATTACK OF TYPE 2: UNIFORM AND MAJORITY"""


def attack_function_uniform(k, size_c):
    return k/size_c


def attack_function_majority(k, size_c):
    if k > size_c/2:
        return 1
    else:
        return 0


def attack_ii_uniform(c, secret_fingerprints, sigma):
    fingerprints_merged, len_of_collusion = fusion_chunks(c, secret_fingerprints)
    for i in range(m_):
        if random() <= attack_function_uniform(fingerprints_merged[i], len_of_collusion):
            fingerprints_merged[i] = gauss(1, sigma ** 2)
        else:
            fingerprints_merged[i] = gauss(-1, sigma ** 2)
    return fingerprints_merged







