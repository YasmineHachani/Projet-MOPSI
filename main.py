import tardos_code_construction as tcc
import collusion_attack as ca
import matplotlib.pyplot as plt
from random import random
from scipy.stats import linregress
import numpy as np
import EM_algorithm as em
import MCMC as mc

# Constant variables
n_ = 100
m_ = 100
c_max_ = 8
t_ = 1 / (300 * c_max_)
size_c_ = 6
T_ = 20
K_ = 50
# Choice of the collusion
c_ = [ 56, 32, 0, 0 , 1, 17,3,99]

# Creation of the secret p and the secret fingerprints
secret_p_ = tcc.random_variable_p(m_)
secret_fingerprints_ = tcc.users_fingerprints(n_, m_, secret_p_)

# Attack of type I
sigma_list_ = np.linspace(0.0001, 0.5, 8)
fingerprints_merged_ = ca.attack_i_average2(c_, m_, secret_fingerprints_,0.1 )
epsilon_ = 10 ** (-2)
plt.subplot(211)
C = list()
for colluder in c_:
    if colluder > 0:
        C.append(secret_fingerprints_[colluder])
C = np.array(C)
plt.imshow(C)
plt.colorbar()
plt.title("Les 8 codes des pirates")
plt.ylabel("Pirates")
plt.subplot(212)
D = [fingerprints_merged_ for k in range(10)]
D = np.array(D)
plt.title("Code après collusion [Type I 'Average', bruit sigma=0.21]")
plt.imshow(D)
plt.colorbar()
plt.show()

mu_list1_, sigma_list1_, log_likelihood_list1_, iterator_list_ = em.EM1_list(fingerprints_merged_, secret_p_, epsilon_,c_max_, m_)

estim_c_=np.argmax(log_likelihood_list1_)+1
print("estim_c",estim_c_)
print(mu_list1_)
x = np.argmax(log_likelihood_list1_)
abs = np.array(range(1, c_max_ + 1))
plt.plot(abs, log_likelihood_list1_)
plt.axvline(x=x+1, color='r')
plt.title("Vraisemblance en fonction du nombre de pirates")
plt.xlabel("c de 1 à c_max")
plt.show()

plt.plot(np.array(range(len(mu_list1_[x]))), mu_list1_[x])
ord = 2 * np.array(range(len(mu_list1_[x]))) / x - 1
plt.plot(np.array(range(len(mu_list1_[x]))), ord, color='g')
plt.title("'Average' et mu calculé par algorithme EM")
plt.plot()
plt.show()
markov_tirages= mc.algo(fingerprints_merged_,secret_fingerprints_,c_max_,n_,mu_list1_,0.1,m_,estim_c_, T_,K_)

margins=mc.margins(markov_tirages,K_,n_)

plt.plot(range(1,n_+1),margins)
for c in c_:
    if c>0:
        plt.axvline(x=c,color='r',linewidth=0.6, linestyle='--')
plt.title("1 - 3 - 17 - 32 - 56 - 99")
plt.show()