def copy(matrix):
    new_matrix = []
    for row in matrix:
        new_matrix.append(row.copy())

    return new_matrix



def minor(matrix, i, j):
    active_matrix = copy(matrix)

    active_matrix.pop(i)
    for row in active_matrix:
        row.pop(j)

    return active_matrix



def complement(matrix, i, j):
    return (-1) ** (i + j) * det(minor(matrix, i, j))



def det(matrix):
    determinant = 0

    if len(matrix) == 1:
        return matrix[0][0]
    elif len(matrix) == 2:
        determinant += matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    else:
        for j in range(len(matrix)):
            determinant += complement(matrix, 0, j) * matrix[0][j]

    return determinant



def transpose(matrix):
    transposed_matrix = [[] for _ in range(len(matrix[0]))]

    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            transposed_matrix[j].append(matrix[i][j])

    return transposed_matrix



def matrix_by_a_number(matrix, k):
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            matrix[i][j] *= k

    return matrix



def matrix_multiplication(matrix1, matrix2):
    if len(matrix1[0]) != len(matrix2):
        raise Exception("ОШИБКА: Матрицы нельзя перемножить")

    new_matrix = [[] for _ in range(len(matrix1))]

    for i1 in range(len(matrix1)):
        for i2 in range(len(matrix2[0])):
            element = 0
            for j in range(len(matrix1[0])):
                element += matrix1[i1][j] * matrix2[j][i2]

            new_matrix[i1].append(element)

    return new_matrix



def inverse_matrix(matrix):
    determinant = det(matrix)

    if determinant == 0:
        raise Exception("ОШИБКА: Нельзя найти обратную матрицу")

    new_matrix = [[] for _ in range(len(matrix))]
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            new_matrix[i].append(det(minor(matrix, i, j)) * (-1) ** (i + j))

    new_matrix = transpose(new_matrix)
    new_matrix = matrix_by_a_number(new_matrix, 1 / determinant)

    return new_matrix



def pairwise_correlation_coefficients(sample):
    k = len(sample)
    n = len(sample[0])

    X_means = []
    for x in sample:
        X_means.append(sum(x) / len(x))

    S = []
    for j in range(k):
        s = 0
        for i in sample[j]:
            s += (i - X_means[j]) ** 2
        S.append((s / n) ** 0.5)

    R = [[[] for _ in range(k)] for _ in range(k)]
    for l in range(len(R)):
        for j in range(l, len(R)):
            if j == l:
                R[l][j] = 1
            else:
                s = 0
                for i in range(n):
                    s += (sample[j][i] - X_means[j]) * (sample[l][i] - X_means[l])
                R[l][j] = R[j][l] = (s / n) / (S[j] * S[l])

    for r in R:
        print(f"[{"| ".join(f"{i:<{25}}" for i in r)}]")

    return R
