from ast import Try
from src.services.sql_parser import sql_parser


def test_should_generate_valid_insert_midlang():
    res = sql_parser("INSERT INTO test (name, age, grade) VALUES ('Fulano','35','5'), ('Ciclano','40','10')")
    valid_midlang = {'action': 'INSERT', 'columns': ['name', ' age', ' grade'], 'data': [["'Fulano'", "'35'", "'5'"], ["'Ciclano'", "'40'", "'10'"]], 'table_name': 'test'}

    assert res == valid_midlang


def test_should_generate_valid_select_all_midlang():
    res = sql_parser("SELECT * FROM test")
    valid_midlang = {'action': 'SELECT', 'table_name': 'test', 'columns': '*'}

    assert res == valid_midlang


def test_should_generate_valid_select_specific_midlang():
    res = sql_parser("SELECT (name, age) FROM test WHERE id = 1")
    valid_midlang = {'action': 'SELECT', 'table_name': 'test', 'columns': ['name', ' age'], 'where': {'id': '1'}}

    assert res == valid_midlang


def test_should_return_exception_negative_id_select_stmt():
    try:
        sql_parser("SELECT (name, age) FROM test WHERE id = -1")
    except Exception as e:
        assert e.args[0] == "Id cannot be 0 or negative."
    

def test_should_generate_valid_update_midlang():
    res = sql_parser("UPDATE dev SET name = 'Fulano', age = '35', grade = '5' WHERE id = 1")
    valid_midlang = {'action': 'UPDATE', 'table_name': 'dev', 'data': {'name': 'Fulano', 'age': '35', 'grade': '5'}, 'where': {'id': '1'}}

    assert res == valid_midlang


def test_should_return_exception_select_specific_negative_id_update_stmt():
    try:
        sql_parser("UPDATE test SET name = 'Fulano' WHERE id = -1")
    except Exception as e:
        assert e.args[0] == "Id cannot be 0 or negative."


def test_should_generate_valid_delete_midlang():
    res = sql_parser("DELETE FROM test WHERE id = 1")
    valid_midlang = {'table_name': 'test', 'action': 'DELETE', 'where': {'id': '1'}}

    assert res == valid_midlang


def test_should_return_exception_negative_id_delete_stmt():
    try:
        sql_parser("DELETE FROM test WHERE id = -1")
    except Exception as e:
        assert e.args[0] == "Id cannot be 0 or negative."
