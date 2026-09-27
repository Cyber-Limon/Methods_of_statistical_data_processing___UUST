from MoSDP_data import *
from math import log, e



def minor(matrix, i, j):
    active_matrix = []
    for row in matrix:
        active_matrix.append(row.copy())


    active_matrix.pop(i)
    for row in active_matrix:
        row.pop(j)

    return active_matrix



def complement(matrix, i, j):
    return (-1) ** (i + j) * det(minor(matrix, i, j))



def det(matrix):
    determinant = 0

    if len(matrix) == 2:
        determinant += matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    else:
        for j in range(len(matrix)):
            determinant += complement(matrix, 0, j) * matrix[0][j]

    return determinant


"""
var      = [Y[14]] + X[14]
var_data = [[] for i in range(len(var))]

for k in range(len(var)):
    for n in range(len(data)):
        var_data[k].append(data[n][var[k] - 1])
"""


var_data = [[30, 20, 40, 35, 45, 25, 50, 30],
            [20, 30, 50, 70, 80, 20, 90, 25],
            [20, 25, 20, 15, 10, 30, 10, 20]]

k = len(var_data)
n = len(var_data[0])


# Ср. арифм
X_means = []
for x in var_data:
    X_means.append(sum(x) / len(x))
print("X:", X_means)



# Среднеквадрат.
S = []
for j in range(k):
    s = 0
    for i in var_data[j]:
        s += (i - X_means[j]) ** 2
    S.append((s / n) ** 0.5)
print("\nS:", S)



# Парные
R = [[[] for i in range(k)] for j in range(k)]
for l in range(len(R)):
    for j in range(l, len(R)):
        if j == l:
            R[l][j] = 1
        else:
            s = 0
            for i in range(n):
                s += (var_data[j][i] - X_means[j]) * (var_data[l][i] - X_means[l])

            R[l][j] = R[j][l] = (s / n) / (S[j] * S[l])

print("\nR:")
for r in R:
    print(r)



# Частные
r_partial = [[[] for i in range(k)] for j in range(k)]
for i in range(len(r_partial)):
    for j in range(i, len(r_partial)):
        if i == j:
            r_partial[i][j] = 1
        else:
            r_partial[i][j] = r_partial[j][i] = - (complement(R, i, j)) / ((complement(R, i, i) * complement(R, j, j)) ** 0.5)

print("\nr_partial:")
for r in r_partial:
    print(r)



# Значимость
r_critical = 0.754 #0.288 (По таблице 5 при: a = 0.05 и v = n - l - 2 = 53 - 4 - 2 = 47)

print("\nЗначимость:")
for i in range(1, len(r_partial)):
    for j in range(i):
        if abs(r_partial[i][j]) > r_critical:
            print(r_partial[i][j], 'H0 отвергается')
        else:
            print(r_partial[i][j], 'H0 не отвергается')



# Интервальные
print("\nИнтервальные:")
t = 1.96 # (По таблице 1: Ф(t) = 0.95)
l = k - 2

for i in range(1, len(r_partial)):
    for j in range(i):
        Z = 0.5 * (log(1 + r_partial[i][j]) - log(1 - r_partial[i][j])) #(По таблице 6)

        Z1 = Z - t * ((1 / (n - l - 3)) ** 0.5)
        Z2 = Z + t * ((1 / (n - l - 3)) ** 0.5)

        Z_min, Z_max = min(Z1, Z2), max(Z1, Z2)
        print(r_partial[i][j], ":", Z_min, Z_max)

        print('---')

        r_min = (e ** (2 * Z_min) - 1) / (e ** (2 * Z_min) + 1)
        r_max = (e ** (2 * Z_max) - 1) / (e ** (2 * Z_max) + 1)
        print(r_partial[i][j], ":", r_min, r_max)

        print("\n")



# Множественные
R_multiple = []

for i in range(k):
    R_multiple.append((1 - (det(R) / complement(R, i, i))) ** 0.5)

print("\nR_multiple:", R_multiple)

D = [i ** 2 for i in R_multiple]
print("\nD:", D)



# Значимость
F_critical = 5.79 #2.37 (По таблице 4 при: a = 0.05; v1 = k - 1 = 6 - 1 = 5 и v2 = n - k = 53 - 6 = 47)

print("\nЗначимость:")
for d in D:
    F = (d / (k - 1)) / ((1 - d) / (n - k))

    if F > F_critical:
        print(F, 'H0 отвергается')
    else:
        print(F, 'H0 не отвергается')
