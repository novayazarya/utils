with open("source_data.txt") as fh: # открытие и чтение исходного файла
    # readlines() разбивает построчно содержимое файла
    # при помощи rstrip() избавляемся от символа переноса строки \n
    # в переменную name записывается ФИО, в id_ -- идентификатор
    name, id_ = [line.rstrip() for line in fh.readlines()]

num = int(int(id_) / len(name.replace(" ", ""))) # в num записывется результат деления id_ на количество символов в ФИО без пробелов

# в asc записывается логическое значение в зависимости от четности или нечетности num
# чётность проверяем значением остатка от деления на 2
asc = False if num % 2 else True

# при помощи последовательности функций map() и ord()
# получаем список unicode символов ФИО
ords  = list(map(ord, name.replace(" ", "")))

# алгоритм сортировки вставками https://en.wikipedia.org/wiki/Insertion_sort
def insertion_sort(arr, asc=True):
    for i in range(len(arr)): # цикл для перебора значений массива
        cursor = arr[i] # инициализация курсора на i-м элементе
        pos = i
        # в зависимости от параметра asc выбирается направление сортировки
        ascending = lambda asc: arr[pos - 1] > cursor if asc else arr[pos - 1] < cursor

        while pos > 0 and ascending(asc):
            # пока в позиции перед указателем
            # меньше / больше значения в позиции указателя
            # производим перестановку
            arr[pos] = arr[pos - 1]
            pos = pos - 1 # сдвигаем позицию к началу списка
        arr[pos] = cursor # перемещаем значение курсора в позицию финальной итерации
    return arr

# алгоритм сортировки пузырьком https://en.wikipedia.org/wiki/Bubble_sort
def bubble_sort(arr, asc=True):
    def swap(i, j):
        arr[i], arr[j] = arr[j], arr[i]

    n = len(arr)
    swapped = True
    x = -1
    ascending = lambda asc: arr[i - 1] > arr[i] if asc else arr[i - 1] < arr[i]

    while swapped:
        swapped = False
        x = x + 1
        for i in range(1, n - x):
            if ascending(asc):
                swap(i - 1, i)
                swapped = True
    return arr

""" Далее будет применяться алгоритм сортировки вставками
    1) он прост в реализации
    2) эффективен в работе с небольшими наборами данных или частично отсортированными
    3) сложность алгоритма O(n) = n^2
    4) выигрыша в производительности по сравнению с сортировкой пузырьком не будет, но
       сам алгоритм записывается короче
"""

# алгоритм расчёта среднего арифметического
def average(list):
    summa, counts = 0, 0
    for i in list:
        summa += i
        counts += 1
    return round(summa / counts, 3) # округление до трех знаков после запятой при помощи функции round()

# алгоритм расчёта среднего квадратического
def s_average(list):
    summa, counts = 0, 0
    for i in list:
        summa += i * i
        counts += 1
    return round((summa / counts) ** 0.5, 3)

"""
Форматированная строка для записи результатов
Требуется версия Python >= 3.6
Содержание переменных и результат работы функций
передаются в определенные участки многоуровневой строки
"""

result = f"""1. Исходные данные: {name}; ID: {id_}
2. {num}
3. Направление сортировки: по {'возрастанию' if asc else 'убыванию'}, так как число {num} – {'чётное' if asc else 'нечётное'}
4. Набор данных: {ords}
5. Отсортированный по {'возрастанию' if asc else 'убыванию'} набор данных {insertion_sort(ords, asc=asc)}
7. Среднее арифметическое значение: {average(ords)}
8. Среднее квадратическое значение: {s_average(ords)}
"""

def main():
    with open("result.txt", "w") as ph: # запись строки готовыми данными в файл
        ph.write(result)

if __name__ == '__main__':
    # проверяем нашу сортировку, сравнивая результат её работы с работой базовой функции sorted()
    # если сортировка выполнена правильно, результаты записываются в файл
    assert insertion_sort(ords, asc=asc) == sorted(ords, reverse=not(asc))
    assert bubble_sort(ords, asc=asc) == sorted(ords, reverse=not(asc))
    main()
