import EM_algorithm as em
import tardos_code_construction as tcc
import collusion_attack as ca
import matplotlib.pyplot as plt
from random import random
from scipy.stats import linregress


# Constant variables
n_ = 20
m_ = 3000
c_max_ = 10
t_ = 1 / (300 * c_max_)
size_c_ = 2

# Choice of the collusion
c_ = [6, 0, 0, 0, 0, 0, 0, 17, 0, 0]

# Creation of the secret p and the secret fingerprints
secret_p_ = tcc.random_variable_p(m_)
secret_fingerprints_ = tcc.users_fingerprints(n_, m_, secret_p_)

# Attack of type I

sigma_ = random()

fingerprints_merged_ = ca.attack_i_average(c_, secret_fingerprints_, sigma_)



print(sigma_)

for size_c in range(1, c_max_+1):
    sigma_0 = random()
    mu_0 = em.init_mu_0(size_c)
    L = em.EM1(fingerprints_merged_, secret_p_, size_c, 10**-3, mu_0, sigma_0)
    print("Taille : ", size_c, " ; Vraisemblance", L)





