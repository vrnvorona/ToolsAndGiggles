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
            row = [float(j) for j in re.split(',\s*|\s+', line.strip())]
            temp.append(row)
        try:
            return np.array(temp, np.float64)
        except ValueError as e:
            print('Не получилось считать матрицу из файла, скорее всего размер строк не совпадает')
            raise e # raise'ем потому что в отличии от консольного ввода поменять файл мы
                    # во время выполнения не можем и нужно остановить прогу


def read_from_input():
    m = get_int_string('Введите количество строк матрицы: ')
    n = get_int_string('Введите количество столбцов матрицы: ')
    print(f'Матрица {m}x{n}')
    temp = [get_input_row(n) for _ in range(m)]

    return np.array(temp, np.float64)


def get_input_row(length):
    input_list = [float(j) for j in re.split(',\s*|\s+', input('Введите строку матрицы: ').strip())]
    if len(input_list) != length:
        print(f'Длина строки матрицы должна быть {length}')
        return get_input_row(length)
    else:
        return input_list


def get_int_string(string):
    try:
        return int(input(string))
    except ValueError:
        print('Введенная строка не годится, попробуйте еще раз.')
        return get_int_string(string)


def get_threshold():
    try:
        return float(input('Введите заданное число: '))
    except ValueError:
        print('Введенная строка не годится, попробуйте еще раз.')
        return get_threshold()


def main():
    array = read_from_file('matrix')
    # array = read_from_input()
    threshold = get_threshold()
    print(f'Матрица: \n{np.array2string(array, separator=", ")}')
    print(f'Элементы меньше числа: \n{np.array2string(array[array < threshold], separator=", ")}')
    print(f'Визуальная репрезентация сравнения: \n{np.array2string(array < threshold, separator=", ")}')
    print(f'Индексы элементов которые меньше числа: \n{np.array2string(np.transpose(np.nonzero(array < threshold)), separator=", ")}')


if __name__ == '__main__':
    main()
