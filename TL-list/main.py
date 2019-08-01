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
        list_of_params = [self.count]
        append = list_of_params.append
        list_2_arr = []

        next_node = self.head
        while next_node:
            list_2_arr.append(next_node)
            next_node = next_node.next

        memory_addr_2_list_position = {item: num for num, item in enumerate(list_2_arr)}

        for item in list_2_arr:
            str_node = item.string
            # str_len = len(str_node)
            rnd_node = memory_addr_2_list_position[item.rand]

            # append(str_len)
            append(str_node)
            append(rnd_node)

        list_of_params = map(str, list_of_params)
        list_of_params = '\n'.join(list_of_params)

        # file.write(bytes(list_of_params, 'utf-8'))
        file.write(list_of_params)

    @staticmethod
    def deserialize(file):
        """Десериализация"""
        split_arr = file.read().split('\n')

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
    def create_list():
        """Создание двусвязного списка из набора отдельных блоков"""
        # Создание независимых блоков
        list_of_independent_nodes = [ListNode(
            next_el=None,
            prev_el=None,
            rand_el=None,
            new_string=str(x)
        ) for x in range(25)]

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


if __name__ == '__main__':
    test_list = MakeTest.create_list()

    with open('ListRand.sbr', mode='w') as op_file:
        test_list.serialize(op_file)

    with open('ListRand.sbr', mode='r') as op_file:
        restore_list = test_list.deserialize(op_file)

