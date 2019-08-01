import random as rnd


class ListNode:
    """Элемент двусвязного списка"""
    def __init__(self, prev_el, next_el, rand_el, new_string):
        """Создание нового элемента"""
        self.prev = prev_el
        self.next = next_el
        self.rand = rand_el
        self.string: str = new_string


class ListRand:
    """Список элементов"""
    def __init__(self, head, tail, count):
        """Инициализация списка"""
        self.head = head
        self.tail = tail
        self.count = count

    def serialize(self, file):
        """Сериализация"""
        # Создание контейнеров для хранения собираемой строки и списка всех нодов.
        list_of_params = [self.count]
        list_2_arr = []
        # Так как Python обрабатывает каждое обращение к методу индивидуально, для ускорения работы циклов
        #   добавление элементов в созданные контейнеры перенесено в специальные переменные
        append_param = list_of_params.append
        append_arr = list_2_arr.append

        # Сохранение всех элементов списка в контейнер, последовательно друг за другом
        next_node = self.head
        while next_node:
            append_arr(next_node)
            next_node = next_node.next

        # Для удовлетврения условия на алгоритмическую сложность придумал решение в виде хэширования позиции нода
        #   с ключом из экземпляра этого нода (или иначе - его адреса)
        memory_addr_2_list_position = {item: num for num, item in enumerate(list_2_arr)}

        # Сериализация элементов
        for item in list_2_arr:
            # Получение строки
            str_node = item.string
            # Получение позиции нода по его экземпляру
            rnd_node = memory_addr_2_list_position[item.rand]

            # Добавление в список
            append_param(str_node)
            append_param(rnd_node)

        # Пробегаем по списку приводя тип к строковому
        list_of_params = map(str, list_of_params)
        # Конкатенация в единую строку с разделителем в виде переноса коретки
        list_of_params = '\n'.join(list_of_params)

        # Запись в поток
        file.write(list_of_params)

    @staticmethod
    def deserialize(file):
        """Десериализация"""
        # Чтение из потока и разделение на список подстрок
        split_arr = file.read().split('\n')

        # Путём получения срезов с различным шагом подстроки сортируются по категориям
        count = int(split_arr[0])
        data = split_arr[1:]
        strings_arr = data[::2]
        rnd_arr = list(map(int, data[1::2]))

        # Создание независимых блоков
        list_of_independent_nodes = [ListNode(
            next_el=None,
            prev_el=None,
            rand_el=None,
            new_string=strings_arr[x]
        ) for x in range(count)]

        # Расстановка зависимостей
        for num in range(1, len(list_of_independent_nodes)):
            # Связка предыдущего блока с текущим
            list_of_independent_nodes[num - 1].next = list_of_independent_nodes[num]
            list_of_independent_nodes[num].prev = list_of_independent_nodes[num - 1]

        for num in range(len(list_of_independent_nodes)):
            # Подстановка случайного блока
            list_of_independent_nodes[num].rand = list_of_independent_nodes[rnd_arr[num]]

        # Включение блоков в структуру
        new_list = ListRand(head=list_of_independent_nodes[0],
                            tail=list_of_independent_nodes[-1],
                            count=len(list_of_independent_nodes))

        return new_list


class MakeTest:
    """Набор инструкций для тестирования"""
    @staticmethod
    def create_list(num):
        """Создание двусвязного списка из набора отдельных блоков"""
        # Создание независимых блоков
        list_of_independent_nodes = [ListNode(
            next_el=None,
            prev_el=None,
            rand_el=None,
            new_string=str(x)
        ) for x in range(num)]

        # Расстановка зависимостей
        for num in range(1, len(list_of_independent_nodes)):
            # Связка предыдущего блока с текущим
            list_of_independent_nodes[num - 1].next = list_of_independent_nodes[num]
            list_of_independent_nodes[num].prev = list_of_independent_nodes[num - 1]

        for num in range(len(list_of_independent_nodes)):
            # Подстановка случайного блока
            rnd_elem_number = rnd.choice(range(len(list_of_independent_nodes)))
            list_of_independent_nodes[num].rand = list_of_independent_nodes[rnd_elem_number]

        # Включение блоков в структуру
        new_list = ListRand(head=list_of_independent_nodes[0],
                            tail=list_of_independent_nodes[-1],
                            count=len(list_of_independent_nodes))

        return new_list

    @staticmethod
    def identity_test(first_struct, second_struct):
        """Тест на правильность восстановления зависимостей"""
        def node_check(first_node, second_node):
            """Сравнение элементов"""
            strings_eq = first_node.string == second_node.string
            rand_eq = first_node.rand.string == second_node.rand.string

            if first_node.next:
                next_eq = first_node.next.string == second_node.next.string
            else:
                next_eq = first_node.next == second_node.next

            if first_node.prev:
                prev_eq = first_node.prev.string == second_node.prev.string
            else:
                prev_eq = first_node.prev == second_node.prev

            assert all([strings_eq, rand_eq, next_eq, prev_eq]), 'Элементы не совпадают!'

        assert first_struct.count == second_struct.count, 'Число элементов не совпадает!'

        first_next = first_struct.head
        second_next = second_struct.head
        while first_next:
            node_check(first_next, second_next)
            first_next = first_next.next
            second_next = second_next.next

        print('Структуры идентичны!')


if __name__ == '__main__':
    # Создание списка
    test_list = MakeTest.create_list(25)

    # Сериализация
    with open('ListRand.sbr', mode='w') as op_file:
        test_list.serialize(op_file)

    # Десериализация
    with open('ListRand.sbr', mode='r') as op_file:
        restore_list = test_list.deserialize(op_file)

    # Тест на идентичность
    MakeTest.identity_test(test_list, restore_list)

