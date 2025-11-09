def parse(argv=None):
    import argparse
    import sys
    parser = argparse.ArgumentParser()
    parser.add_argument('--files', nargs='*')
    parser.add_argument('--report', default='average-rating')
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
                    else:
                        ratings[brand].append(float(rating))
                        prices[brand].append(int(price))
    except FileNotFoundError as e:
        print(f'Файл {e.filename} не найден. Составление отчета прекращено')
        sys.exit(-1)
    return {'ratings': ratings, 'prices': prices}


def calculate_average_rating(data):
    info = data['ratings']
    result = {}
    for brand, ratings in info.items():
        result[brand] = sum(ratings) / len(ratings)
    return result


def calculate_average_price(data):
    info = data['prices']
    result = {}
    for brand, prices in info.items():
        result[brand] = sum(prices) / len(prices)
    return result


def print_table(data, value_name='rating'):
    from tabulate import tabulate
    table_headers = ['', 'brand', value_name]
    table = []

    sorted_data = sorted(data.items(), key=lambda x: -x[1])

    for i, (brand, value) in enumerate(sorted_data, 1):
        row = [str(i), brand, str(round(value, 2))]
        table.append(row)

    print(tabulate(table, headers=table_headers, tablefmt='outline'))


REPORTS = {
    'average-rating': {
        'calculator': calculate_average_rating,
        'value_name': 'rating'
    },
    'average-price': {
        'calculator': calculate_average_price,
        'value_name': 'price'
    }
}


def main(argv=None):
    import sys

    args = parse(argv)

    if args.report not in REPORTS:
        print(f'Отчет {args.report} не поддерживается. Доступные отчеты: {", ".join(REPORTS.keys())}')
        sys.exit(-1)

    data = read_files(args.files)
    report_config = REPORTS[args.report]
    calculated_data = report_config['calculator'](data)
    print_table(calculated_data, report_config['value_name'])


if __name__ == '__main__':
    main()
