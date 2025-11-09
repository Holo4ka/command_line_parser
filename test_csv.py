from main import main
import pytest


@pytest.fixture
def sample_csv(tmp_path):
    file_path = tmp_path / 'sample.csv'
    with open(file_path, 'w') as f:
        f.write(
            'id,brand,price,rating\n'
            '1,BrandA,100,4.5\n'
            '2,BrandB,200,3.8\n'
            '3,BrandA,150,4.7\n'
        )
    return str(file_path)


@pytest.fixture
def two_samples_csv(tmp_path):
    file1 = tmp_path / 'file1.csv'
    file2 = tmp_path / 'file2.csv'
    with open(file1, 'w') as f:
        f.write(
            'id,brand,price,rating\n'
            '1,BrandA,100,4.5\n'
            '2,BrandB,200,3.9\n'
            '3,BrandA,150,4.7\n'
        )
    with open(file2, 'w') as f:
        f.write(
            'id,brand,price,rating\n'
            '1,BrandA,110,4.6\n'
            '2,BrandC,150,4.8\n'
            '3,BrandB,170,4.5\n'
        )
    return str(file1), str(file2)


def parse_report(output):
    data = {}
    lines = output.split('\n')[3:]
    for line in lines:
        parts = line.split('|')
        if len(parts) >= 4:
            brand = parts[2].strip()
            value = float(parts[3])
            data[brand] = value
    return data


def test_single_csv_correct(sample_csv, capsys):
    # Средний рейтинг
    main(['--files', sample_csv, '--report', 'average-rating'])
    captured = capsys.readouterr()
    data = parse_report(captured.out)
    assert data['BrandA'] == 4.6
    assert data['BrandB'] == 3.8

    # Средняя цена
    main(['--files', sample_csv, '--report', 'average-price'])
    captured = capsys.readouterr()
    data = parse_report(captured.out)
    assert data['BrandA'] == 125
    assert data['BrandB'] == 200


def test_several_csvs_correct(two_samples_csv, capsys):
    file1, file2 = two_samples_csv

    # Средний рейтинг
    main(['--files', file1, file2, '--report', 'average-rating'])
    captured = capsys.readouterr()
    data = parse_report(captured.out)
    assert data['BrandA'] == 4.6
    assert data['BrandB'] == 4.2
    assert data['BrandC'] == 4.8

    # Средняя цена
    main(['--files', file1, file2, '--report', 'average-price'])
    captured = capsys.readouterr()
    data = parse_report(captured.out)
    assert data['BrandA'] == 120
    assert data['BrandB'] == 185
    assert data['BrandC'] == 150
