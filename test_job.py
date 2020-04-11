#!/usr/bin/python
# -*- coding: utf-8 -*-
import os


def main():
    ar = ['ar1', 'ar2']  #заполняем список
    print(f'len arr = {len(ar)}')  #используем функцию format
    if ar:  #проверка на существование без сравнения
        print(ar)
    for inx, row in enumerate(ar):  #добыча индекса родным методом
        print(f'index ar = {inx}')

    for root, dirs, files in os.walk("c:/tmp/"): #зачем страдать,если walk разложит все в переменные
        for file in files:
            print(root,file)

def main2():
    ar = []
    ar.append('ar1')
    ar.append('ar2')
    count = 0
    for r in ar:
        count += 1
    print('len arr = ' + str(count))
    if ar != []:
        print(ar)
    inx = 0
    for i in ar:
        print('index ar = ' + str(inx))
        inx = inx + 1

    dir_name = "c:/tmp/"
    names = os.listdir(dir_name)
    for name in names:
        fn = os.path.join(dir_name, name)
        if os.path.isfile(fn):
            print (fn)

if __name__ == '__main__':
    main()
    main2()