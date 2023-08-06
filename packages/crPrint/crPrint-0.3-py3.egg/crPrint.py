#-*- coding: utf-8 -*-
""" 
    Exemplo:
    --------

        >>> from crPrint import cprint
        >>>  cprint('OLA MUNDO','Green')
        OLA MUNDO

   © Copyright 2017 João Mário

"""

__author__ = 'João Mário'
__mail__ = 'joaok63@outlook.com'

__copyright__ = '© 2017 João Mário'
__license__ = 'GPL'


def cprint(texto='',cor=''):

    if cor == 'Red':
        print(('\033[91m%s\033[0m')% (texto))

    elif cor == 'Yellow':
        print(('\033[93m%s\033[0m')% (texto))

    elif cor == 'Green':
        print(('\033[92m%s\033[0m')% (texto))

    elif cor == 'Pink':
        print(('\033[95m%s\033[0m')% (texto))

    elif cor == 'Blue':
        print(('\033[94m%s\033[0m')% (texto))

    elif cor == 'Cyan':
        print(('\033[96m%s\033[0m')% (texto))

    else:
        print(texto)

if __name__ == '__main__':
  exit() 
