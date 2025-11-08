import sys
import pytest
from main import main


def test_no_files(capsys):
    original_argv = sys.argv.copy()
    sys.argv = ['main.py']
    try:
        with pytest.raises(SystemExit) as e:
            main()
        out = capsys.readouterr().out
        assert 'Файлы для отчета не предоставлены' in out
        assert e.value.code == -1
    finally:
        sys.argv = original_argv


def test_file_not_found(capsys):
    original_argv = sys.argv.copy()
    sys.argv = ['main.py', '--files', 'no_such_file.csv']
    try:
        with pytest.raises(SystemExit) as e:
            main()
        out = capsys.readouterr().out
        assert 'Файл no_such_file.csv не найден' in out
        assert e.value.code == -1
    finally:
        sys.argv = original_argv


def test_average_rating(capsys):
    original_argv = sys.argv.copy()
    sys.argv = [
        'main.py', '--files', 'products1.csv', '--report', 'average-rating'
    ]
    try:
        main()
        out = capsys.readouterr().out
        assert 'brand' in out and 'rating' in out
    finally:
        sys.argv = original_argv


def test_unsupported_report(capsys):
    original_argv = sys.argv.copy()
    sys.argv = [
        'main.py', '--files', 'products1.csv', '--report', 'unknown'
    ]
    try:
        main()
        out = capsys.readouterr().out
        assert 'Такой тип отчета не поддерживается' in out
    finally:
        sys.argv = original_argv
