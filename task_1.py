"""Создать телефонный справочник с
возможностью импорта и экспорта данных в
формате .txt. Фамилия, имя, отчество, номер
телефона - данные, которые должны находиться
в файле.
1. Программа должна выводить данные
2. Программа должна сохранять данные в
текстовом файле
3. Пользователь может ввести одну из
характеристик для поиска определенной
записи(Например имя или фамилию
человека)
4. Использование функций. Ваша программа
не должна быть линейной
"""
from os import listdir
from string import digits, punctuation
from csv import DictReader, DictWriter
from os.path import exists


class NameError(Exception):
    def __init__(self, txt):
        self.txt = txt


filename = "phonebook.csv"


def fmt_by_mask(fmt, in_str):
    res = ""
    i = 0
    for c in fmt:
        if c == '#':
            res += in_str[i:i + 1]
            i += 1
        else:
            res += c
    return res


def filter_str(in_str, allowed):
    out_str = ''
    for c in in_str:
        if c in allowed:
            out_str += c
    return out_str


def validate_string(in_str):
    for c in in_str:
        if c in digits or c in punctuation:
            return False
    return True


def import_text():
    flag = False
    while not flag:
        list_dir = [f for f in listdir() if f.endswith('.txt')]
        for i in range(len(list_dir)):
            print(f"{i + 1}: {list_dir[i]}")
        input_str = input("Выберите файл для загрузки: ")
        for item in input_str:
            if item not in digits:
                print("Неверный формат данных. Введите число")
                continue
        if int(input_str) > len(list_dir):
            print("Файл не существует!")
            continue
        flag = True
        file_name = list_dir[int(input_str) - 1]
        import_fb = []
        with open(file_name, encoding='utf-8') as import_file:
            for row in import_file:
                record = row.split()
                phone = reformat_phone(record[2])
                import_fb.append({'surname': record[0], 'name': record[1], 'phone': phone})
        for item in import_fb:
            add_sub(item, False)
        print(f"Записи ({len(import_fb)} шт.)  успешно добавлены.")
        y_n_continue()


def export_to_text():
    file_name = input("Введите имя файла для сохранения: ")
    f_b = read_phonebook()
    with open(f"{file_name}.txt", 'w', encoding='utf-8') as text_file:
        for item in f_b:
            text_file.write(f"{item['surname']} {item['name']} {item['phone']}\n")
    print(f"Файл: {file_name}.txt успешно сохранен!")
    y_n_continue()


def read_phonebook():
    f_book = []
    with open(filename, encoding='utf-8', newline='') as f_b:
        f_b_reader = DictReader(f_b)
        for row in f_b_reader:
            f_book.append(row)
    return f_book


def input_sub():
    flag = False
    while not flag:
        try:
            surname = input('Введите фамилию: ')
            if len(surname) < 3:
                raise NameError('Слишком короткая фамилия')
            if not validate_string(surname):
                raise NameError('Имя не должно содержать цифр и знаков пунктуации')
            name = input('Введите имя: ')
            if len(name) < 2:
                raise NameError('Слишком короткое имя')
            if not validate_string(name):
                raise NameError('Фамилия не должна содержать цифр и знаков пунктуации')
            phone = reformat_phone(input('Введите номер телефона: '))
            if len(phone) < 16:
                raise NameError('Слишком короткий номер телефона')
        except NameError as err:
            print(err)
        else:
            flag = True
    return {'surname': surname, 'name': name, 'phone': phone}


def add_sub(sub, menu_flag=True):
    fieldnames = ['surname', 'name', 'phone']
    with open(filename, 'a', encoding='utf-8', newline='') as f_b:
        f_b_writer = DictWriter(f_b, fieldnames=fieldnames)
        if len(read_phonebook()) == 0:
            f_b_writer.writeheader()
        f_b_writer.writerow(sub)
    print(f"Абонент {sub['surname']} {sub['name']} добавлен в справочник")
    if menu_flag:
        y_n_continue()


def reformat_phone(data):
    return fmt_by_mask('+#(###)###-##-##', filter_str(data.lower(), digits))


def find_sub_by(criterion):
    if criterion == 'phone':
        print("Поиск по номеру телефона:")
        search_str = reformat_phone(input(f"Введите строку поиска: "))
    elif criterion == 'surname':
        print("Поиск по фамилии:")
        search_str = input(f"Введите строку поиска: ").lower()
    elif criterion == 'name':
        print("Поиск по имени:")
        search_str = input(f"Введите строку поиска: ").lower()
    f_book = read_phonebook()
    result = "Результаты поиска:\n"
    for item in f_book:
        if search_str in item[criterion].lower():
            result += (f"\nФамилия: {item['surname']} \nИмя: {item['name']}\nТелефон: {item['phone']}\n")
    if result == "Результаты поиска:\n":
        return "Поиск не дал результатов"
    else:
        return result


def find_sub():
    while True:
        print(
            "Выберите критерий поиска: \n1. Поиск по имени\n2. Поиск по фамилии\n3. Поиск по номеру телефона\nДля выхода наберите q\nДля выхода в основное меню наберите *")
        menu_item = input("Введите номер пункта меню: ")
        if menu_item == '1':
            print(find_sub_by('name'))
            y_n_continue()
            break
        elif menu_item == '2':
            print(find_sub_by('surname'))
            y_n_continue()
            break
        elif menu_item == '3':
            print(find_sub_by('phone'))
            y_n_continue()
            break
        elif menu_item == '*':
            main_menu()
            break
        elif menu_item == 'q':
            quit()


def list_all_phonebook():
    f_b = read_phonebook()
    for item in f_b:
        print(f"{item['surname']} {item['name']}, телефон: {item['phone']}")
    y_n_continue()


def delete_phone():
    flag = False
    while not flag:
        f_b = read_phonebook()
        with_num = [[i + 1, f_b[i]] for i in range(len(f_b))]
        for item in with_num:
            print(f"{item[0]}. {item[1]['surname']} {item[1]['name']}, телефон: {item[1]['phone']}")
        delete_num = input("Введите номер записи для удаления (для отмены введите q): ").lower()
        if delete_num == 'q':
            y_n_continue()
            break
        else:
            for item in delete_num:
                if item not in digits:
                    print("Неверный формат данных. Введите число")
                    continue
            delete_num = int(delete_num)
            if delete_num > len(with_num):
                print("Записи не существует!")
                continue
            f_b.pop(delete_num - 1)
            fieldnames = ['surname', 'name', 'phone']
            with open(filename, 'w', encoding='utf-8', newline='') as file_f_b:
                f_b_writer = DictWriter(file_f_b, fieldnames=fieldnames)
                f_b_writer.writeheader()
                f_b_writer.writerows(f_b)
            print('Запись удалена!')
        if input("Удалить еще? (y/n): ") == 'y':
            continue
        else:
            y_n_continue()


def y_n_continue():
    while True:
        print("Продолжить работу с программой? (y/n)")
        input_str = input().lower()
        if input_str == 'n':
            quit()
        elif input_str == 'y':
            break
    main_menu()


def main_menu():
    while True:
        print(
            "Телефонный справочник\n1. Добавить запись\n2. Поиск\n3. Просмотр\n4. Удаление записи\n5. Экспорт\n6. Импорт из json\nДля выхода наберите q")
        menu_item = input("Введите номер пункта меню: ")
        if menu_item == '1':
            add_sub(input_sub())
            break
        elif menu_item == '2':
            if not exists(filename):
                print(
                    f'Файл "{filename}" не существует. Добавьте хотя бы одну запись или импортируйте записи, файл создасться автоматически.')
                continue
            find_sub()
            break
        elif menu_item == '3':
            if not exists(filename):
                print(
                    f'Файл "{filename}" не существует. Добавьте хотя бы одну запись или импортируйте записи, файл создасться автоматически.')
                continue
            list_all_phonebook()
            break
        elif menu_item == '4':
            if not exists(filename):
                print(
                    f'Файл "{filename}" не существует. Добавьте хотя бы одну запись или импортируйте записи, файл создасться автоматически.')
                continue
            delete_phone()
            break
        elif menu_item == '5':
            if not exists(filename):
                print(
                    f'Файл "{filename}" не существует. Добавьте хотя бы одну запись или импортируйте записи, файл создасться автоматически.')
                continue
            export_to_text()
            break
        elif menu_item == '6':
            import_text()
            break
        elif menu_item == 'q':
            quit()


main_menu()
