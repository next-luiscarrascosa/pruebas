"""
Clase python de prueba para probar el pylint
"""


def func():
    '''
    Script de prueba
    '''
    first = 1
    second = 2
    print(first)
    print(second)


# func()


def func1(param):
    data = ["A", "B"]

    index = data.index(param)
    print(data[index-1])

func1("B")
func1("A")