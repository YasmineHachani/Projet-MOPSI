from main import *
import numpy as np
A = np.array(secret_fingerprints_)

plt.imshow(A, cmap=plt.cm.get_cmap('Blues', 2))
plt.colorbar(ticks=range(2), label='bits value')
plt.show()



plt.subplot(511)
C=list()
for colluder in c_:
    if colluder>0:
        C.append(secret_fingerprints_[colluder])
C=np.array(C)
plt.imshow(C)
plt.colorbar()
plt.title("Les 8 codes des pirates")
plt.ylabel("Pirates")
plt.subplot(512)
B=list()
for i in sigma_list_:

    f=ca.attack_i_average(c_, m_, secret_fingerprints_, i)
    B.append(f)
B=np.array(B)
plt.imshow(B)
plt.colorbar()
plt.title("Type I: 'Average'")
plt.ylabel("Bruit croissant")
plt.subplot(513)
B=list()
for i in sigma_list_:

    f=ca.attack_i_average2(c_, m_, secret_fingerprints_, i)
    B.append(f)
B=np.array(B)
plt.imshow(B)

plt.colorbar()
plt.title("Type I: 'Average2'")
plt.ylabel("Bruit croissant")
plt.subplot(514)
B=list()
for i in sigma_list_:

    f=ca.attack_ii_uniform(c_, m_, secret_fingerprints_, i)
    B.append(f)
B=np.array(B)
plt.imshow(B)

plt.colorbar()

plt.title("Type II: 'Uniform'")
plt.ylabel("Bruit croissant")
plt.subplot(515)
B=list()
for i in sigma_list_:
    f=ca.attack_ii_majority(c_, m_, secret_fingerprints_, i)
    B.append(f)
B=np.array(B)
plt.imshow(B)
plt.colorbar()

plt.title("Type II: 'Majority'")
plt.ylabel("Bruit croissant")

plt.show()

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
plt.plot(abs, sigma_list1_)
plt.axhline(y=sigma_list_[3], color='g')
plt.title("Sigma vrai et sigma calculé par algorithme EM en fonction de c")
plt.show()
plt.axvline(x=x+1, color='r')
print(iterator_list_)


print("ok")