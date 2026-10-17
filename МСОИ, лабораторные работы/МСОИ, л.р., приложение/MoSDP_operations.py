from math import log10



### Лабораторная работа 1 ###

def copy(matrix):
    """Копирование матрицы"""

    new_matrix = []
    for row in matrix:
            new_matrix.append(row.copy())

    return new_matrix



def minor(matrix, i, j):
    """Минор"""

    active_matrix = copy(matrix)

    active_matrix.pop(i)
    for row in active_matrix:
        row.pop(j)

    return active_matrix



def complement(matrix, i, j):
    """Алгебраическое дополнение"""

    return (-1) ** (i + j) * det(minor(matrix, i, j))



def det(matrix):
    """Определитель"""

    determinant = 0

    if len(matrix) == 1:
        return matrix[0][0]
    elif len(matrix) == 2:
        determinant += matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    else:
        for j in range(len(matrix)):
            determinant += complement(matrix, 0, j) * matrix[0][j]

    return determinant



def matrix_output(matrix, length=25):
    """Вывод матрицы в консоль"""

    for m in matrix:
        print(f"[{"| ".join(f"{i:<{length}}" for i in m)}]")





### Лабораторная работа 2 ###

def transpose(matrix):
    """Транспонирование матрицы"""

    transposed_matrix = [[] for _ in range(len(matrix[0]))]

    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            transposed_matrix[j].append(matrix[i][j])

    return transposed_matrix



def matrix_by_a_number(matrix, k):
    """Умножение матрицы на число"""

    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            matrix[i][j] *= k

    return matrix



def matrix_multiplication(matrix1, matrix2):
    """Умножение матриц"""

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
    """Обратная матрица"""

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



def arithmetic_mean_deviations(sample):
    """Средние арифметические отклонения"""

    X_means = []
    for x in sample:
        X_means.append(sum(x) / len(x))

    return X_means



def root_mean_square_deviations(sample):
    """Среднеквадратические отклонения"""

    X_means = arithmetic_mean_deviations(sample)

    k = len(sample)
    n = len(sample[0])

    S = []
    for j in range(k):
        s = 0
        for i in sample[j]:
            s += (i - X_means[j]) ** 2
        S.append((s / n) ** 0.5)

    return S



def pairwise_correlation_coefficients(sample):
    """Матрица парных коэффициентов корреляции"""

    X_means = arithmetic_mean_deviations(sample)
    S       = root_mean_square_deviations(sample)

    k = len(sample)
    n = len(sample[0])

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

    matrix_output(R)

    return R





### Лабораторная работа 3 ###

def tr(matrix):
    """След матрицы"""

    s = 0
    for i in range(len(matrix)):
        s += matrix[i][i]

    return s



def bisection_method(f, a, b, eps = 1e-12):
    """Метод бисекций"""

    while b - a > eps:
        c = (a + b) / 2

        if eval(f.replace("lambda", "c")) == 0:
            return c
        elif eval(f.replace("lambda", "a")) * eval(f.replace("lambda", "c")) > 0:
            a = c
        else:
            b = c

    return (a + b) / 2



# Распределение Стьюдента (t-распределение) - по "таблице 2": a = 0.05 и v = n - k - 1
t_table = {(0.05, 40): 2.021, (0.1, 40): 1.684, (0.2, 40): 1.303, (0.3, 40): 1.050, (0.4, 40): 0.851}

# Распределение Фишера-Снедекора (F-распределение) - по "таблице 4": a = 0.05; v1 = k + 1 и v2 = n - k - 1
F_table = {(0.05, 6, 47): 2.25, (0.05, 5, 48): 2.37, (0.05, 4, 49): 2.52, (0.05, 3, 50): 2.76, (0.05, 2, 51): 3.15}



def estimate(Y, X, form):
    """Коэффициенты уравнения регрессии"""

    xTx = matrix_multiplication(transpose(X), X)
    xTy = matrix_multiplication(transpose(X), Y)
    b = matrix_multiplication(inverse_matrix(xTx), xTy)

    if form == "pow":
        b[0][0] = 10 ** b[0][0]

    return b



def draw(b, numbers, form):
    """Вывод уравнения регрессии в консоль"""

    equation = f"y = {b[0][0]}"

    for i in range(1, len(b)):
        if form == "linear":
            if b[i][0] > 0:
                equation += f" + {b[i][0]}"
            else:
                equation += f" - {abs(b[i][0])}"
            equation += f" * x{numbers[i]}"
        else:
            equation += f" * x{numbers[i]}^({b[i][0]})"

    print(equation)



def significance_equation(Y, X, b, form):
    """Значимость уравнения"""

    b_current = copy(b)

    if form == "pow":
        b_current[0][0] = log10(b_current[0][0])

    Y_reg = matrix_multiplication(X, b_current)

    Q = 0
    for i in range(len(Y)):
        Q += (Y[i][0] - Y_reg[i][0]) ** 2

    k   = len(X[0]) - 1
    n   = len(X)
    S_2 = Q / (n - k - 1)

    Q_r = matrix_multiplication(transpose(Y_reg), Y_reg)

    F_critical = F_table[(0.05, k + 1, n - k - 1)]
    F          = (Q_r[0][0] / (k + 1)) / S_2

    res = ('<=', 'не ')
    if F > F_critical:
        res = ('>', '')

    print(f"F_набл = {F} {res[0]} {F_critical}: {res[1]}значимое")

    return S_2



def significance_coefficients(X, b, S_2, t_critical):
    """Значимость коэффициентов регрессии"""

    xTx = inverse_matrix(matrix_multiplication(transpose(X), X))
    S   = matrix_by_a_number(xTx, S_2)

    t = []
    for i in range(1, len(S)):
        t.append(b[i][0] / (S[i][i] ** 0.5))

        res = (' <=', 'не')
        if abs(t[-1]) > t_critical:
            res = (' > ', '  ')

        print(f"- t_набл(b{i}) = |{t[-1]:{7}.3f}| {res[0]} {t_critical}: {res[1]} значимый")

        t[-1] = abs(t[-1])

    return t



def regression_analysis(Y, X, numbers, form):
    """Алгоритм пошагового регрессионного анализа"""

    for parameters in t_table:
        t_critical = t_table[parameters]

        print("=" * 97)
        print(f"При a = {parameters[0]}")
        print("=" * 97)

        new_X       = copy(X)
        new_numbers = numbers.copy()

        t = [0]

        step = 0
        while min(t) <= t_critical and len(t) > 1 or step == 0:
            if step != 0:
                print(f"{"-" * 45} Шаг {step} {"-" * 45}")

                j = t.index(min(t)) + 1
                print(f"\nМинимальный t: |t_набл(b{j})| <= {t_critical}")

                for x in new_X:
                    x.pop(j)

                new_numbers.pop(j)

            b = estimate(Y, new_X, form)
            print(f"\nНовая оценка b_{form}: {b}")

            draw(b, new_numbers, form)
            print()

            S_2 = significance_equation(Y, new_X, b, form)
            t   = significance_coefficients(new_X, b, S_2, t_critical)
            print()

            step += 1

        if min(t) > t_critical:
            print("=" * 97)
            print(f"Итоговая оценка b_{form}: {b}")
            print()
            draw(b, new_numbers, form)
            print("=" * 97)

            return new_X, b, new_numbers, S_2

    return None, None, None, None



def regression_equation(Y, X, form):
    """Уравнение регрессии"""

    new_Y = copy(Y)
    new_X = copy(X)

    for x in new_X:
        x.insert(0, 1)

    numbers = [i for i in range(len(new_X[0]))]

    if form == "linear":
        print(f"{"-" * 38} ЛИНЕЙНОЕ  УРАВНЕНИЕ {"-" * 38}\n")

    else:
        for i in range(len(new_X)):
            new_Y[i][0] = log10(new_Y[i][0])

            for j in range(1, len(X[0])):
                new_X[i][j] = log10(new_X[i][j])

        print(f"{"-" * 38} СТЕПЕННОЕ УРАВНЕНИЕ {"-" * 38}\n")

    regression_analysis(new_Y, new_X, numbers, form)





### Лабораторная работа 4 ###

def matrix_addition(matrix_1, matrix_2):
    """Сложение матриц"""
    new_matrix = copy(matrix_1)

    for i in range(len(matrix_1)):
        for j in range(len(matrix_1[0])):
            new_matrix[i][j] += matrix_2[i][j]

    return new_matrix



def matrix_difference(matrix_1, matrix_2):
    """Разность матриц"""
    new_matrix = copy(matrix_1)

    for i in range(len(matrix_1)):
        for j in range(len(matrix_1[0])):
            new_matrix[i][j] -= matrix_2[i][j]

    return new_matrix
