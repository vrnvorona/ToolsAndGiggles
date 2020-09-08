import numpy as np
import re

'''
Дана прямоугольная матрица размерности MxN и заданное значение.
Создать одномерный массив, в который занести элементы данной матрицы,
меньше чзаданного значения.
Реализовать ввод с клавиатуры или файла, массив из целых или вещественных чисел.
'''


def read_from_file(path):
    with open(path, 'r') as file:
        temp = []
        for line in file.readlines():
            row = [float(j) for j in re.split(',\s*|\s+', line.rstrip())]
            temp.append(row)
        try:
            return np.array(temp, np.float64)
        except ValueError as e:
            print('Не получилось считать матрицу из файла, скорее всего размер строк не совпадает')
            raise e


def read_from_input():
    m = int(input('Введите количество строк матрицы: '))
    n = int(input('Введите количество столбцов матрицы: '))
    print(f'Матрица {m}x{n}')
    temp = [get_input_row(n) for _ in range(m)]

    return np.concatenate(temp, axis=0)


def get_input_row(length):
    input_list = [float(j) for j in re.split(',\s*|\s+', input('Введите строку матрицы: '))]
    row = np.array([input_list])
    if row.shape[1] != length:
        print(f'Длина строки матрицы должна быть {length}')
        return get_input_row(length)
    else:
        return row


def main():
    array = read_from_file('matrix')
    # array = read_from_input()
    threshold = float(input('Введите заданное число: '))
    print(f'Матрица: \n{array}')
    print(f'Элементы меньше числа: \n{np.array2string(array[array < threshold], separator=", ")}')
    print(f'Визуальная репрезентация сравнения: \n{np.array2string(array < threshold, separator=", ")}')
    print(f'Индексы элементов которые меньше числа: \n{np.array2string(np.transpose(np.nonzero(array < threshold)), separator=", ")}')


if __name__ == '__main__':
    main()