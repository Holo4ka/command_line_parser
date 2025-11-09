def parse(argv=None):
    import argparse
    import sys
    parser = argparse.ArgumentParser()
    parser.add_argument('--files', nargs='*',
                        help='список файлов для анализа')
    parser.add_argument('--report', nargs='?',
                        help='тип отчета (поддерживаемые типы: average-rating, average-price')
    args, unknown = parser.parse_known_args(argv)
    if unknown:
        print('Получены неизвестные аргументы:')
        print(', '.join(unknown))
        sys.exit(-1)
    if not args.files:
        print('Файлы для отчета не предоставлены')
        sys.exit(-1)
    return args


def read_files(files):
    import csv
    import sys

    headers = None
    ratings = {}
    prices = {}
    data = {}
    try:
        for file in files:
            with open(file) as f:
                reader = csv.reader(f, delimiter=',')
                if headers is None:
                    headers = next(reader, None)
                else:
                    next(reader, None)
                for row in reader:
                    row = row[1:]
                    brand, price, rating = row
                    if brand not in ratings.keys():
                        ratings[brand] = [float(rating)]
                        prices[brand] = [int(price)]
                        data[brand] = [(int(price), float(rating))]
                    else:
                        ratings[brand].append(float(rating))
                        prices[brand].append(int(price))
                        data[brand].append((int(price), float(rating)))
    except FileNotFoundError as e:
        print(f'Файл {e.filename} не найден. Составление отчета прекращено')
        sys.exit(-1)
    return data  # {'ratings': ratings, 'prices': prices}


def calculate_average_rating(data):
    brands = data.keys()
    brand_ratings = {}
    for brand in brands:
        brand_ratings[brand] = [elem[1] for elem in data[brand]]
    result = {}
    for brand, ratings in brand_ratings.items():
        result[brand] = sum(ratings) / len(ratings)
    return result


def calculate_average_price(data):
    brands = data.keys()
    brand_ratings = {}
    for brand in brands:
        brand_ratings[brand] = [elem[0] for elem in data[brand]]
    result = {}
    for brand, ratings in brand_ratings.items():
        result[brand] = sum(ratings) / len(ratings)
    return result


def print_table_single_column(data, value_name):
    from tabulate import tabulate
    table_headers = ['', 'brand', value_name]
    table = []
    sorted_data = sorted(data.items(), key=lambda x: -x[1])

    for i, (brand, values) in enumerate(sorted_data, 1):
        row = [str(i), brand, str(round(values, 2))]
        table.append(row)

    print(tabulate(table, headers=table_headers, tablefmt='outline'))


REPORTS = {
    'average-rating': {
        'calculator': calculate_average_rating,
        'value_name': 'rating',
        'printer': print_table_single_column
    },
    'average-price': {
        'calculator': calculate_average_price,
        'value_name': 'price',
        'printer': print_table_single_column
    },
}


def main(argv=None):
    import sys

    args = parse(argv)

    if not args.report:
        print('Пожалуйста, укажите тип отчета')
        sys.exit(-1)

    if args.report not in REPORTS:
        print(f'Отчет {args.report} не поддерживается. Доступные отчеты: {", ".join(REPORTS.keys())}')
        sys.exit(-1)

    data = read_files(args.files)
    report_config = REPORTS[args.report]
    calculated_data = report_config['calculator'](data)
    report_config['printer'](calculated_data, report_config['value_name'])


if __name__ == '__main__':
    main()
