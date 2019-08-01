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
        pass

    def deserialize(self, file):
        """Десериализация"""
        pass


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

    pass

