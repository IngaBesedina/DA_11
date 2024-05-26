#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
Вариант 2.
С использованием многопоточности для заданного значения x
найти сумму ряда S с точностью члена ряда по абсолютному значению e=10^-7
и произвести сравнение полученной суммы с контрольным значением функции
для двух бесконечных рядов. Необходимо реализовать вычисление значений
функций в отдельных процессах.
"""


from multiprocessing import Barrier, Manager, Process


def calc_sum1(x, eps, s, lock, br):
    sum1 = 0
    n = 0
    while True:
        el = x**n
        if abs(el) < eps:
            break
        sum1 += el
        n += 1
    with lock:
        s["s1"] = sum1
    br.wait()


def calc_sum2(x, eps, s, lock, br):
    sum2 = 0
    n = 0
    while True:
        t = n + 1
        el = (-1) ** n * x**n / 2**t
        if abs(el) < eps:
            break
        else:
            sum2 += el
            n += 1
    with lock:
        s["s2"] = sum2
    br.wait()


def res(s, y1, y2, br):
    br.wait()
    s1 = s["s1"]
    s2 = s["s2"]

    print(f"Вариант №2. Сумма ряда S: {s1}")
    print(f"Контрольное значение функции для бесконечного ряда: {y1}")

    print(f"Вариант №3. Сумма ряда S: {s2}")
    print(f"Контрольное значение функции для бесконечного ряда: {y2}")


def main(m):
    br = Barrier(3)
    lock = m.Lock()

    s = m.dict()
    e = 1e-7

    x1 = 0.7
    y1 = 1 / (1 - x1)

    x2 = 1.2
    y2 = 1 / (2 + x2)

    process1 = Process(target=calc_sum1, args=(x1, e, s, lock, br))
    process2 = Process(target=calc_sum2, args=(x2, e, s, lock, br))
    process3 = Process(target=res, args=(s, y1, y2, br))

    process1.start()
    process2.start()
    process3.start()

    process1.join()
    process2.join()
    process3.join()


if __name__ == "__main__":
    with Manager() as manager:
        main(manager)
