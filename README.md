# CSV Data Processor

Проект представляет собой консольный скрипт для обработки CSV-файлов с поддержкой фильтрации и агрегации данных.

## Функциональность

- Чтение CSV-файлов
- Фильтрация данных по условиям:
  - Операторы: `>`, `<`, `>=`, `<=`, `=`, `!=`
  - Поддержка текстовых и числовых полей
- Агрегация данных:
  - Доступные функции: `avg`, `min`, `max`, `sum`, `count`
  - Работа только с числовыми полями
- Красивый табличный вывод с помощью библиотеки `tabulate`

## Установка

1. Клонируйте репозиторий:
  bash git clone
  https://github.com/yourusername/csv-processor.git
  cd csv-processor
2. Установите зависимости:
   pip install tabulate pytest pytest-cov

## Использование

Базовый синтаксис:
  python main.py --file <путь_к_файлу.csv> [--where "условие"] [--aggregate "агрегация"]
1. Вывод всего содержимого файла:
   python main.py --file products.csv
2. Фильтрация по рейтингу:
   python main.py --file products.csv --where "rating>4.7"
3. Расчет среднего значения:
   python main.py --file products.csv --aggregate "price=avg"
4. Комбинирование фильтрации и агрегации:
   python main.py --file products.csv --where "brand=xiaomi" --aggregate "rating=min"

## Формат параметров:

--where: "поле оператор значение" (без кавычек)
Пример: "price>1000", "brand=apple"

--aggregate: "поле=функция"
Пример: "rating=avg", "price=max"

## Тестирование

Для запуска тестов:
  pytest test_main.py -v
ИЛИ
Для проверки покрытия:
  pytest --cov=main test_main.py

## Требования

Python 3.8+
Зависимости: tabulate (для форматированного вывода)
             pytest и pytest-cov (для тестирования)

## Ограничения
  a) Агрегация работает только с числовыми полями
  б) Поддерживаются только простые условия (без AND/OR)
  в) Входные файлы должны быть валидными CSV

## Пример вывода

+------------------+----------+-------+--------+
| name             | brand    | price | rating |
+------------------+----------+-------+--------+
| iphone 15 pro    | apple    | 999   | 4.9    |
| galaxy s23 ultra | samsung  | 1199  | 4.8    |
+------------------+----------+-------+--------+
