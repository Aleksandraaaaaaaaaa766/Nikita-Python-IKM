"""
Задача о контейнерах:
На складе хранятся контейнеры с товарами N различных видов.
Все контейнеры составлены в N стопок. Автопогрузчик может перемещать
верхние контейнеры между стопками. Необходимо расставить все контейнеры
с товаром вида i в i-ю стопку.
"""

MAX_STACKS = 500
MAX_CONTAINERS = 500


class Stack:
    """Класс для работы со стопками контейнеров."""

    def __init__(self, name):
        self.items = []
        self.name = name

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if not self.is_empty():
            return self.items.pop()
        raise IndexError("Попытка взять контейнер из пустой стопки")

    def peek(self):
        if not self.is_empty():
            return self.items[-1]
        return None

    def is_empty(self):
        return len(self.items) == 0

    def size(self):
        return len(self.items)

    def __str__(self):
        return f"{self.name}: {self.items}"


def print_stacks(main_stacks, temp_stacks):
    """Выводит текущее состояние стопок."""
    print("\nТекущее расположение контейнеров:")
    for stack in main_stacks + temp_stacks:
        if not stack.is_empty():
            print(f"{stack.name}: {stack.items}")
    print("------")


def validate_input(parts, stack_num, num_stacks):
    """Проверяет корректность введенных данных."""
    if not parts:
        raise ValueError(f"Пустой ввод для стопки {stack_num}")

    try:
        ki = int(parts[0])
    except ValueError:
        raise ValueError(f"Некорректное количество контейнеров в стопке {stack_num}")

    if ki < 0:
        raise ValueError(f"Отрицательное количество контейнеров в стопке {stack_num}")

    if len(parts) - 1 != ki:
        raise ValueError(
            f"Несоответствие количества контейнеров в стопке {stack_num}. "
            f"Ожидалось {ki}, получено {len(parts) - 1}"
        )

    for elem in parts[1:]:
        try:
            elem_int = int(elem)
        except ValueError:
            raise ValueError(f"Некорректный тип контейнера в стопке {stack_num}")

        if elem_int < 1 or elem_int > num_stacks:
            raise ValueError(
                f"Недопустимый тип контейнера {elem} в стопке {stack_num}. "
                f"Допустимы значения от 1 до {num_stacks}"
            )


def solve_containers():
    """Основная функция решения задачи."""
    print("=== Программа для расстановки контейнеров ===")
    print("Условие: нужно расставить контейнеры так, чтобы в i-й стопке")
    print("находились только контейнеры типа i\n")

    try:
        num_stacks = int(input("Введите количество стопок (1-500): "))
        if num_stacks < 1 or num_stacks > MAX_STACKS:
            raise ValueError(f"Количество стопок должно быть от 1 до {MAX_STACKS}")
    except ValueError as e:
        print(f"Ошибка: {e}")
        return

    main_stacks = [Stack(f"Стопка-{i + 1}") for i in range(num_stacks)]
    temp_stacks = [Stack(f"Временная-{num_stacks + i + 1}") for i in range(num_stacks)]

    print("\nВведите данные для каждой стопки:")
    print("Формат: <количество> <типы контейнеров снизу вверх>")
    print("Пример: 3 1 2 1 - стопка с 3 контейнерами: 1 (низ), 2, 1 (верх)")

    for i in range(num_stacks):
        while True:
            try:
                input_str = input(f"Стопка-{i + 1}: ").strip()
                parts = list(map(str, input_str.split())) if input_str else ['0']

                validate_input(parts, i + 1, num_stacks)

                ki = int(parts[0])
                for elem in parts[1:]:
                    main_stacks[i].push(int(elem))
                break

            except ValueError as e:
                print(f"Ошибка: {e}. Пожалуйста, введите данные снова.")
            except Exception as e:
                print(f"Ошибка: {e}. Пожалуйста, введите данные снова.")

    print("\nНачальное расположение контейнеров:")
    print_stacks(main_stacks, temp_stacks)

    def is_correct():
        """Проверяет правильность расположения контейнеров."""
        for i in range(num_stacks):
            for elem in main_stacks[i].items:
                if elem != i + 1:
                    return False
        return True

    if is_correct():
        print("Контейнеры уже правильно расположены!")
        return

    operations = []

    try:
        # Фаза 1: Распределение по временным стопкам
        for i in range(num_stacks):
            while not main_stacks[i].is_empty():
                elem = main_stacks[i].pop()
                if elem < 1 or elem > num_stacks:
                    raise ValueError(f"Недопустимый тип контейнера {elem}")

                target_stack = elem - 1
                temp_stacks[target_stack].push(elem)
                op = f"Переместить из {main_stacks[i].name} в {temp_stacks[target_stack].name}"
                operations.append(op)
                print(f"Операция {len(operations)}: {op}")
                print_stacks(main_stacks, temp_stacks)

        # Фаза 2: Перемещение в основные стопки
        for i in range(num_stacks):
            while not temp_stacks[i].is_empty():
                elem = temp_stacks[i].pop()
                main_stacks[i].push(elem)
                op = f"Переместить из {temp_stacks[i].name} в {main_stacks[i].name}"
                operations.append(op)
                print(f"Операция {len(operations)}: {op}")
                print_stacks(main_stacks, temp_stacks)

        if not is_correct():
            print("\nРезультат: задача не имеет решения")
            return

        print("\nВсе операции перемещения:")
        for i, op in enumerate(operations, 1):
            print(f"{i}. {op}")

        print("\nФинальное расположение контейнеров:")
        print_stacks(main_stacks, temp_stacks)
        print("=== Задача успешно решена! ===")

    except IndexError as e:
        print(f"\nОшибка: {e}")
    except Exception as e:
        print(f"\nОшибка: {e}")


if __name__ == "__main__":
    solve_containers()