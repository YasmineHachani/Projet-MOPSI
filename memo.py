import EM_algorithm as em
import tardos_code_construction as tcc
import collusion_attack as ca
import matplotlib.pyplot as plt
from random import random
from scipy.stats import linregress


# Constant variables
n_ = 20
m_ = 30
c_max_ = 10
t_ = 1 / (300 * c_max_)
size_c_ = 8

# Choice of the collusion
c_ = [6, 1, 3, 2, 0, 14, 0, 17, 9, 13]

# Creation of the secret p and the secret fingerprints
secret_p_ = tcc.random_variable_p(m_)
secret_fingerprints_ = tcc.users_fingerprints(n_, m_, secret_p_)

# Attack of type I

sigma_ = random()

fingerprints_merged_ = ca.attack_i_average(c_, secret_fingerprints_, sigma_)

# Estimation with the EM algorithm

mu_0 = em.init_mu_0(size_c_)
sigma_0 = random()
print("sigma 0 : ", sigma_0)

L1, sigma_0 = em.EM1(fingerprints_merged_, secret_p_, size_c_, 10**-5, mu_0, sigma_0)

fc = ca.attack_i_average(c_, secret_fingerprints_, sigma_)

print("sigma de l'attaque : ", sigma_, " ; sigma decode : ", sigma_0)
print("secret_fingerprints_", secret_fingerprints_)
print("fingerprints_merged_ :", fc)
print("mu_0 :", mu_0)


attack = list()
decoded_attack_with_noise = list()

for k in range(size_c_+1):
    attack.append(ca.attack_function_average(k, size_c_, sigma_))
    decoded_attack_with_noise.append(mu_0[k])

(a1, b1, rho1, _, _) = linregress(range(size_c_+1), attack)
(a2, b2, rho2, _, _) = linregress(range(size_c_+1), decoded_attack_with_noise)

linear_regression1 = list()
linear_regression2 = list()

for k in range(size_c_+1):
    linear_regression1.append(a1*k + b1)
    linear_regression2.append(a2*k+b2)

plt.plot(range(size_c_+1), attack, "o", color="red")
plt.plot(range(size_c_+1), linear_regression1, color="red")
plt.plot(range(size_c_+1), decoded_attack_with_noise, "+")
plt.plot(range(size_c_+1), linear_regression2, color="blue")

plt.show()
print("a1 : ", a1, " ; b1 : ", b1, " ; rho1 : ", rho1)
print("a2 : ", a2, " ; b2 : ", b2, " ; rho2 : ", rho2)





