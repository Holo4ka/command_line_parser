class FileExtensionError(Exception):
    def __init__(self, filename, *args):
        super().__init__(*args)
        self.filename = filename


def parse(argv=None):
    import argparse
    import sys
    parser = argparse.ArgumentParser()
    types = list(REPORTS.keys())
    parser.add_argument('--files', nargs='*',
                        help='список файлов для анализа')
    parser.add_argument('--report', nargs='?',
                        help=f'тип отчета (поддерживаемые типы: {types})')
    args, unknown = parser.parse_known_args(argv)
    if unknown:
        print('Получены неизвестные аргументы:')
        print(', '.join(unknown))
        sys.exit(-1)
    return args


def read_files(files):
    import csv
    import sys

    headers = None
    data = {}
    try:
        for file in files:
            if file.split('.')[-1] != 'csv':
                raise FileExtensionError(file)
            with open(file) as f:
                reader = csv.reader(f, delimiter=',')
                if headers is None:
                    headers = next(reader, None)
                else:
                    next(reader, None)
                for row in reader:
                    row = row[1:]
                    brand, price, rating = row
                    if brand not in data.keys():
                        data[brand] = [(int(price), float(rating))]
                    else:
                        data[brand].append((int(price), float(rating)))
    except FileNotFoundError as e:
        print(f'Файл {e.filename} не найден. Составление отчета прекращено')
        sys.exit(-1)
    except FileExtensionError as e:
        print(f'Файл {e.filename} не поддерживается')
        sys.exit(-1)
    return data


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

    if not args.files:
        print('Файлы для отчета не предоставлены')
        sys.exit(-1)

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
