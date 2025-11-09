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


def test_no_args(capsys):
    with pytest.raises(SystemExit) as exc_info:
        main([])
    captured = capsys.readouterr()
    assert exc_info.value.code != 0
    assert 'Файлы для отчета не предоставлены' in captured.out

    with pytest.raises(SystemExit) as exc_info:
        main(['--files'])
    captured = capsys.readouterr()
    assert exc_info.value.code != 0
    assert 'Файлы для отчета не предоставлены' in captured.out


def test_incorrect_args(capsys):
    unknown_args = ['--test', 'test', 'unknown', 'u']
    with pytest.raises(SystemExit) as exc_info:
        main(unknown_args)
    captured = capsys.readouterr()
    res = captured.out.split('\n')
    assert exc_info.value.code != 0
    assert 'Получены неизвестные аргументы:' in res[0]
    assert all([arg in res[1] for arg in unknown_args])


def test_no_such_file(capsys):
    with pytest.raises(SystemExit) as exc_info:
        main(['--files', 'file1.csv', '--report', 'average-rating'])
    captured = capsys.readouterr()
    assert exc_info.value.code != 0
    assert 'Файл file1.csv не найден. Составление отчета прекращено' in captured.out


def test_no_report(sample_csv, capsys):
    with pytest.raises(SystemExit) as exc_info:
        main(['--files', sample_csv])
    captured = capsys.readouterr()
    assert exc_info.value.code != 0
    assert 'Пожалуйста, укажите тип отчета' in captured.out

    with pytest.raises(SystemExit) as exc_info:
        main(['--files', sample_csv, '--report'])
    captured = capsys.readouterr()
    assert exc_info.value.code != 0
    assert 'Пожалуйста, укажите тип отчета' in captured.out


def test_unsupported_report(sample_csv, capsys):
    with pytest.raises(SystemExit) as exc_info:
        main(['--files', sample_csv, '--report', 'average-smth'])
    captured = capsys.readouterr()
    assert exc_info.value.code != 0
    assert 'Отчет average-smth не поддерживается' in captured.out
