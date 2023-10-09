import os
from collections import defaultdict
from datetime import datetime
import logger

def get_len_files(path, file_name):
    """показывает количествосимволов в файле в указанной директории"""
    len = 0
    full_path = os.path.join(path, file_name)
    with open(full_path, 'r') as file:
        content = len(file.read())
    return content
def delete_small_len_files(path, min_size = 900):
    """Удаляет маленькие файлы в указанной директории"""
    all_files = 0
    files_deleted = 0
    for foldername, subfolders, filenames in os.walk(path):
        for filename in filenames:
            if filename.endswith('.txt'):
                all_files+=1
                full_path = os.path.join(foldername, filename)
                with open(full_path, 'r') as file:
                    content = file.read()
                if len(content) < min_size:
                    files_deleted+=1
                    os.remove(full_path)
    return all_files, files_deleted
def delete_earlier_files(path):
    """Удаляет более ранние файлы с одинаковыми именами в указанной директории"""
    files_dict = defaultdict(list)
    duplicate_deleted = 0
    all_files=0
    for foldername, subfolders, filenames in os.walk(path):
        for filename in filenames:
            all_files+=1
            _date_time = filename[-24:-4]
            _name = filename[:-24]
            date, time = _date_time.rsplit('__', 2)
            date_time = datetime.strptime(date + '__' + time, '%Y_%m_%d__%H_%M_%S')
            full_path = os.path.join(foldername, filename)
            files_dict[_name].append((str(date_time), full_path))
    for files in files_dict.values():
        files.sort()
        for date_time, full_path in files[:-1]:
            duplicate_deleted+=1
            os.remove(full_path)
    return all_files, duplicate_deleted
def search_fails_report_count(path):
    """Считает общее количество роутеров с ошибко"""
    all_files = 0
    count_fails = 0
    for foldername, subfolders, filenames in os.walk(path):
        for filename in filenames:
            if filename.endswith('.txt'):
                all_files+=1
                full_path = os.path.join(foldername, filename)
                with open(full_path, 'r') as read_obj:
                    text = read_obj.read()
                    if 'Fail' in text:
                        count_fails += 1

    return all_files, count_fails
def search_fails_count(path):
    """Считает общее количество роутеров с ошибко"""
    count_fails = 0
    for foldername, subfolders, filenames in os.walk(path):
        for filename in filenames:
            if filename.endswith('.txt'):
                full_path = os.path.join(foldername, filename)
                with open(full_path, 'r') as read_obj:
                    for line in read_obj:
                        if 'Fail' in line:
                            if not 'Router' in line and not 'TestEthernet' in line and not 'TestLeds' in line:
                                count_fails += 1

    return count_fails
def search_string_in_file(file_name, string_to_search):
    """Эта функция ищет строку в файле и возвращает список номеров строк, в которых эта строка найдена"""
    line_number = 0
    list_of_results = defaultdict(int)
    # Открываем файл в режиме чтения
    with open(file_name, 'r') as read_obj:
        for line in read_obj:
            line_number += 1
            if string_to_search in line:
                if not 'Router' in line and not 'TestEthernet' in line and not 'TestLeds' in line:
                    list_of_results[line.rstrip()] += 1
    return list_of_results
def search_statistic_in_files(path, lg:logger):
    """Проходит по всем файлам в директории и ищет строку в .txt файлах"""
    total_lines = 0
    total_files = 0
    all_results = defaultdict(int)
    for foldername, subfolders, filenames in os.walk(path):
        for filename in filenames:
            total_files+=1
            if filename.endswith('.txt'):
                full_path = os.path.join(foldername, filename)
                with open(full_path, 'r') as file:
                    lines = file.readlines()
                    total_lines += len(lines)
                file_results = search_string_in_file(full_path, 'Fail')
                for key, value in file_results.items():
                    all_results[key] += value
    count_fail = search_fails_count(path)
    lg.log(f'\nВсего ошибок: {count_fail}')
    lg.log('\nИз них: ')
    for key, value in all_results.items():
        proc= round( ((value / count_fail) * 100), 3)
        lg.log(f'\nСтрока: {key}, \t\t\tКоличество: {value}, Процент: {proc}%')

def search_string_spec(file_name, string_to_search):
    """Эта функция ищет строку в файле и возвращает список номеров строк, в которых эта строка найдена"""
    line_number = 0
    list_of_results = []
    # Открываем файл в режиме чтения
    with open(file_name, 'r') as read_obj:
        for line in read_obj:
            line_number += 1
            if string_to_search in line:
                if not 'Router' in line and not 'TestEthernet' in line and not 'TestLeds' in line:
                    list_of_results.append((line_number, line.rstrip()))
    return list_of_results
def write_fails(path, _lg:logger):
    """Проходит по всем файлам в директории и ищет строку в .txt файлах"""
    total_lines = 0
    error_lines = 0
    for foldername, subfolders, filenames in os.walk(path):
        for filename in filenames:
            if filename.endswith('.txt'):
                full_path = os.path.join(foldername, filename)
                with open(full_path, 'r') as file:
                    lines = file.readlines()
                    total_lines += len(lines)
                matched_lines = search_string_spec(full_path, 'Fail')
                error_lines += len(matched_lines)
                for elem in matched_lines:
                    _lg.log(f'У роутера {filename[8:-25]} ошибка по: {elem[1]}\n')
