import csv
import argparse
from typing import List, Dict, Union, Callable, Any

from tabulate import tabulate


def read_csv(file_path: str):
    with open(file_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        return [row for row in reader]


def apply_filter(data: List[Dict[str, str]], condition: str):
    if not condition:
        return data
    
    column, operator, value = parse_condition(condition)
    
    filtered_data = []
    for row in data:
        if evaluate_condition(row[column], operator, value):
            filtered_data.append(row)
    
    return filtered_data


def parse_condition(condition: str):
    operators = ['>=', '<=', '!=', '>', '<', '=']
    for op in operators:
        if op in condition:
            column, value = condition.split(op)
            return column.strip(), op, value.strip()
    raise ValueError(f"Неправильный формат условия: {condition}")


def evaluate_condition(cell_value: str, operator: str, condition_value: str):
    try:
        cell_num = float(cell_value)
        cond_num = float(condition_value)
        return {
            '>': lambda: cell_num > cond_num,
            '<': lambda: cell_num < cond_num,
            '>=': lambda: cell_num >= cond_num,
            '<=': lambda: cell_num <= cond_num,
            '=': lambda: cell_num == cond_num,
            '!=': lambda: cell_num != cond_num,
        }[operator]()
    except ValueError:
        return {
            '>': lambda: cell_value > condition_value,
            '<': lambda: cell_value < condition_value,
            '>=': lambda: cell_value >= condition_value,
            '<=': lambda: cell_value <= condition_value,
            '=': lambda: cell_value == condition_value,
            '!=': lambda: cell_value != condition_value,
        }[operator]()


def apply_aggregation(data: List[Dict[str, str]], aggregation: str):
    if not aggregation:
        return {}
    
    column, func_name = aggregation.split('=')
    column = column.strip()
    func_name = func_name.strip().lower()
    
    try:
        values = [float(row[column]) for row in data]
    except ValueError:
        raise ValueError(f"Невозможно применить к нечисловым значениям: {column}")
    
    aggregators = {
        'avg': lambda vals: sum(vals) / len(vals) if vals else 0,
        'min': lambda vals: min(vals) if vals else 0,
        'max': lambda vals: max(vals) if vals else 0,
        'sum': lambda vals: sum(vals) if vals else 0,
        'count': lambda vals: len(vals)
    }
    
    if func_name not in aggregators:
        raise ValueError(f"Неизвестная функция агрегации: {func_name}")
    
    return {func_name: aggregators[func_name](values)}


def display_results(data: List[Dict[str, str]], aggregation_result: Dict[str, Union[float, str]]):
    if aggregation_result:
        func_name, value = next(iter(aggregation_result.items()))
        print(tabulate([[value]], headers=[func_name], tablefmt="grid"))
    else:
        if not data:
            print("No data matching the criteria")
            return
        
        table_data = [[row[col] for col in row] for row in data]
        headers = list(data[0].keys()) if data else []
        print(tabulate(table_data, headers=headers, tablefmt="grid"))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', help='Путь к CSV файлу', required=True)
    parser.add_argument('--where', help='Условие фильтрации. Например "rating>4.5"')
    parser.add_argument('--aggregate', help='Агрегация по признаку. Например "price=avg"')
    
    args = parser.parse_args()
    
    try:
        data = read_csv(args.file)
        
        filtered_data = apply_filter(data, args.where) if args.where else data
        
        aggregation_result = apply_aggregation(filtered_data, args.aggregate) if args.aggregate else {}
        
        display_results(filtered_data, aggregation_result)
    
    except FileNotFoundError:
        print(f"Error: Файл не найден - {args.file}")
    except Exception as e:
        print(f"Error: {str(e)}")


if __name__ == '__main__':
    main()