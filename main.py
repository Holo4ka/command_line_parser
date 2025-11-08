def main(argv=None):
    import argparse
    import sys
    import csv
    from tabulate import tabulate

    parser = argparse.ArgumentParser()
    parser.add_argument('--files', nargs='*')
    parser.add_argument('--report', default='average-rating')
    args, unknown = parser.parse_known_args(argv)
    if unknown:
        print('Получены неизвестные аргументы:')
        print(', '.join(unknown))
        sys.exit(-1)
    headers = None
    ratings = {}
    prices = {}
    if not args.files:
        print('Файлы для отчета не предоставлены')
        sys.exit(-1)
    try:
        for file in args.files:
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

    if args.report == 'average-rating':
        table_headers = ['', 'brand', 'rating']
        table = []
        i = 1
        for brand in ratings.keys():
            average_rating = sum(ratings[brand]) / len(ratings[brand])
            row = [str(i), brand, str(round(average_rating, 2))]
            table.append(row)
            i += 1
        table.sort(key=lambda x: -float(x[-1]))
        print(tabulate(table, headers=table_headers, tablefmt="outline"))
    elif args.report == 'average-price':
        table_headers = ['', 'brand', 'price']
        table = []
        i = 1
        for brand in prices.keys():
            average_price = sum(prices[brand]) / len(prices[brand])
            row = [str(i), brand, str(round(average_price, 2))]
            table.append(row)
            i += 1
        table.sort(key=lambda x: -float(x[-1]))
        print(tabulate(table, headers=table_headers, tablefmt="outline"))
    else:
        print('Такой тип отчета не поддерживается')
        sys.exit(-1)


if __name__ == "__main__":
    main()
