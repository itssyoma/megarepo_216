#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import json
from jsonschema import validate
from jsonschema.exceptions import ValidationError


def validation(instance):
    schema = {
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "group": {"type": "string"},
                "grade": {"type": "number"},
                },
            },
            "required": ["name", "group", "grade"],
        }

    try:
        validate(instance, schema=schema)
        return True
    except ValidationError as err:
        print(err.message)
        return False


def command_add(students):
     # Запросить данные о студенте.
    name = input("Фамилия и инициалы? ")
    group = input("Номер группы? ")
    grade = list(map(int, input("Успеваемость студента? (Пять оценок через пробел) ").split()))
    while True:
        if len(grade) < 5:
            print("Введное количество оценок меньше 5, введите оценки еще раз: ", file=sys.stderr)
            grade = list(map(int, input("Успеваемость студента? (Пять оценок через пробел) ").split()))
        else:
            break

    # Создать словарь.
    if sum(grade)/len(grade) >= 4.0:
        student = {
            'name': name,
            'group': group,
            'grade': sum(grade)/len(grade),
        }
        # Добавить словарь в список.
        students.append(student)
    
    # Отсортировать список в случае необходимости.
    if len(students) > 1:
        students.sort(key=lambda item: item.get('name', ''))
    
    return students


def command_list(students):
    if students:
                print("Список студентов с успеваемостью больше 4.0")
                # Заголовок таблицы.
                line = '+-{}-+-{}-+-{}-+'.format(
                    '-' * 4,
                    '-' * 30,
                    '-' * 20
                )
                print(line)
                print(
                    '| {:^4} | {:^30} | {:^20} |'.format(
                        "No",
                        "Ф.И.О.",
                        "Группа"
                    )
                )
                print(line)

                # Вывести данные о всех сотрудниках.
                for idx, student in enumerate(students, 1):
                    print(
                        '| {:>4} | {:<30} | {:<20} |'.format(
                            idx,
                            student.get('name', ''),
                            student.get('group', '')
                        ) 
                    )

                print(line)
    
    else:
                print("Студентов с успеваемостью выше 4.0 нет")


def save_students(file_name, staff):
    # Сохранить всех студентов в файл JSON
    # Открыть файл с заданным именем для записи.
    with open(file_name, "w", encoding="utf-8") as fout:
        # Выполнить сериализацию данных в формат JSON.
        # Для поддержки кирилицы установим ensure_ascii=False
        json.dump(staff, fout, ensure_ascii=False, indent=4)


def load_students(file_name):
    # Загрузить всех студентов из файла JSON.
    # Открыть файл с заданным именем для чтения.
    with open(file_name, "r", encoding="utf-8") as fin:
        data = json.load(fin)
    
    if validation(data):
         return data


if __name__ == '__main__':

    students = []

    # Организовать бесконечный цикл запроса команд.
    while True:
        # Запросить команду из терминала.
        command = input(">>> ").lower()

        # Выполнить действие в соответствие с командой.
        if command == 'exit':
            break
        elif command == 'add':
            students = command_add(students)
        elif command == 'list':
            command_list(students)
        elif command.startswith('save'):
             # Разбить команду на части для выделения имени файла.
            parts = command.split(maxsplit=1)
            # Получить имя файла.
            file_name = parts[1]
            # Сохранить данные в файл с заданным именем.
            save_students(file_name, students)
        elif command.startswith('load'):
             # Разбить команду на части для выделения имени файла.
            parts = command.split(maxsplit=1)
            # Получить имя файла.
            file_name = parts[1]
            # Сохранить данные в файл с заданным именем.
            students = load_students(file_name)
        
        else:
            print(f"Неизвестная команда {command}", file=sys.stderr)
