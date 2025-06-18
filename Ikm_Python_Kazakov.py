"""
Задача о контейнерах:
На складе хранятся контейнеры с товарами N различных видов.
Все контейнеры составлены в N стопок. Автопогрузчик может перемещать
верхние контейнеры между стопками. Необходимо расставить все контейнеры
с товаром вида i в i-ю стопку.
"""

class Node:
    """Узел односвязного списка для стека"""
    def __init__(self, data):
        self.data = data
        self.next = None

class Stack:
    """Реализация стека через односвязный список"""
    def __init__(self, name):
        self.top = None
        self.name = name
        self.size = 0

    def push(self, item):
        """Добавление элемента на вершину стека"""
        new_node = Node(item)
        new_node.next = self.top
        self.top = new_node
        self.size += 1

    def pop(self):
        """Извлечение элемента с вершины стека"""
        if self.is_empty():
            raise IndexError("Попытка взять контейнер из пустой стопки")
        item = self.top.data
        self.top = self.top.next
        self.size -= 1
        return item

    def peek(self):
        """Просмотр верхнего элемента без извлечения"""
        return self.top.data if not self.is_empty() else None

    def is_empty(self):
        """Проверка на пустоту"""
        return self.top is None

    def __str__(self):
        """Визуализация стека"""
        items = []
        current = self.top
        while current:
            items.append(str(current.data))
            current = current.next
        return f"{self.name}: [{', '.join(reversed(items))}]" if items else f"{self.name}: []"

def get_valid_num_stacks():
    """Функция для получения корректного количества стопок"""
    while True:
        try:
            num = int(input("Введите количество стопок (1-500): "))
            if 1 <= num <= 500:
                return num
            print("Ошибка: количество стопок должно быть от 1 до 500")
        except ValueError:
            print("Ошибка: введите целое число")

def solve_containers():
    """Основная логика программы"""
    print("=== Программа для расстановки контейнеров ===")
    print("Условие: нужно расставить контейнеры так, чтобы в i-й стопке")
    print("находились только контейнеры типа i\n")

    # Получаем корректное количество стопок
    num_stacks = get_valid_num_stacks()

    stacks = [Stack(f"Стопка-{i+1}") for i in range(num_stacks)]
    temp_stacks = [Stack(f"Временная-{num_stacks+i+1}") for i in range(num_stacks)]

    # Ввод данных
    print("\nВведите для каждой стопки: количество контейнеров и их типы (снизу вверх)")
    print("Например:")
    print("2")
    print("3 2 1 2")
    print("1 1")
    for i in range(num_stacks):
        while True:
            try:
                parts = input(f"Стопка-{i+1}: ").split()
                if not parts:
                    parts = ['0']

                ki = int(parts[0])
                if ki < 0:
                    raise ValueError("Количество не может быть отрицательным")
                if len(parts) - 1 != ki:
                    raise ValueError(f"Ожидалось {ki} контейнеров, получено {len(parts)-1}")

                for elem in parts[1:]:
                    container_type = int(elem)
                    if not 1 <= container_type <= num_stacks:
                        raise ValueError(f"Тип контейнера должен быть от 1 до {num_stacks}")
                    stacks[i].push(container_type)
                break
            except ValueError as e:
                print(f"Ошибка: {e}. Должно быть число (кол-во контейнеров в стопке) и типы контейнеров (от 1 до N). Повторите ввод.")

    # Проверка начального состояния
    if all(stack.peek() == i+1 for i, stack in enumerate(stacks) if not stack.is_empty()):
        print("Контейнеры уже правильно расположены!")
        return

    operations = []

    # Фаза 1: Распределение по временным стопкам
    for i in range(num_stacks):
        while not stacks[i].is_empty():
            container = stacks[i].pop()
            target = container - 1
            temp_stacks[target].push(container)
            operations.append(f"{stacks[i].name} -> {temp_stacks[target].name}")

    # Фаза 2: Сборка в целевые стопки
    for i in range(num_stacks):
        while not temp_stacks[i].is_empty():
            container = temp_stacks[i].pop()
            stacks[i].push(container)
            operations.append(f"{temp_stacks[i].name} -> {stacks[i].name}")

    # Проверка результата
    if all(stack.peek() == i+1 for i, stack in enumerate(stacks) if not stack.is_empty()):
        print("\nПоследовательность перемещений:")
        for i, op in enumerate(operations, 1):
            print(f"{i}. {op}")
        print("\nЗадача решена!")
    else:
        print("Задача не имеет решения")

if __name__ == "__main__":
    solve_containers()
