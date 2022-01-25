import os

from src.interactors.Tsv import Tsv


def test_select_all():
    instance = Tsv()

    res = instance.select({'action': 'SELECT', 'table_name': 'test', 'columns': '*'})

    assert res[0:3] == [['id name  age  grade'], ["1 'Fulano' '35' '5'"], ["2 'Ciclano' '40' '10'"]]


def test_select_specific_cols():
    instance = Tsv()

    res = instance.select({'action': 'SELECT', 'table_name': 'test', 'columns': ['name'], 'where': {'id': '1'}})

    assert res[1] == ["'Fulano'"]


def test_create_table_if_not_exist():
    instance = Tsv()
    instance.create_table_if_not_exist('db/create_table_test.tsv', {'id': 'INTEGER', 'name': 'Fulano', 'age': '25', 'grade': '5'})

    file = open('db/create_table_test.tsv', 'r')
    content = file.read()

    assert content == 'id\tid\tname\tage\tgrade\t\n'

    os.remove('db/create_table_test.tsv')


def test_insert():
    instance = Tsv()

    res = instance.insert({'action': 'INSERT', 'columns': ['name', ' age', ' grade'], 'data': [["'Fulano'", "'35'", "'5'"], ["'Ciclano'", "'40'", "'10'"]], 'table_name': 'test_insert_table'})
    test_assert = res

    assert test_assert == 0

    os.remove('db/test_insert_table.tsv')


def test_delete():
    instance = Tsv()
    instance.insert({'action': 'INSERT', 'columns': ['name', ' age', ' grade'], 'data': [["'TESTE'", "'350'", "'50'"]], 'table_name': 'delete_test_table_name'})
    instance.delete({'table_name': 'delete_test_table_name', 'action': 'DELETE', 'where': {'id': '1'}})
    
    content = instance.select({'action': 'SELECT', 'table_name': 'delete_test_table_name', 'columns': '*'})

    assert content == [['id name  age  grade']]

    os.remove('db/delete_test_table_name.tsv')


def test_map_file_columns():
    instance = Tsv()

    columns = instance.map_data_obj_to_file_columns('test')

    assert columns == {'id': 0, 'name': 1, 'age': 2, 'grade': 3}


def test_update():
    instance = Tsv()

    instance.insert({'action': 'INSERT', 'columns': ['name', ' age', ' grade'], 'data': [["'TESTE'", "'80'", "'80'"]], 'table_name': 'update_test_table_name'})
    instance.update({'action': 'UPDATE', 'table_name': 'update_test_table_name', 'data': {'name': 'TESTE', 'age': '20', 'grade': '8'}, 'where': {'id': '1'}})    
    content = instance.select({'action': 'SELECT', 'table_name': 'update_test_table_name', 'columns': '*'})

    assert content == [['id name  age  grade'], ["1 'TESTE' '20' '8'"]]

    os.remove('db/update_test_table_name.tsv')


def test_new_id_generation():
    instance = Tsv()

    for _ in range(0, 4):
        instance.insert({'action': 'INSERT', 'columns': ['name', ' age', ' grade'], 'data': [["'TESTE'", "'80'", "'80'"]], 'table_name': 'new_id_test_table_name'})

    id = instance.get_new_id('db/new_id_test_table_name.tsv')

    assert id == 5

    os.remove('db/new_id_test_table_name.tsv')


def test_write_on_file():
    instance = Tsv()

    instance.write_on_file('db/write_test.tsv', 'test string', 'INSERT')

    file = open('db/write_test.tsv', 'r')
    content = file.read()

    assert content == 'test string'

    os.remove('db/write_test.tsv')


def test_format_data():
    instance = Tsv()

    data = instance.format_data({'name': "'Fulano'", 'age': "'35'", 'grade': "'5'"})

    assert data == 'name\tage\tgrade\t\n'


def test_format_data_is_header():
    instance = Tsv()

    data = instance.format_data({'name': "'Fulano'", 'age': "'35'", 'grade': "'5'"}, True)

    assert data == 'id\tname\tage\tgrade\t\n'


def test_read_from_file():
    instance = Tsv()

    instance.write_on_file('db/read_test.tsv', 'test string', 'INSERT')

    data = instance.read_from_file('db/read_test.tsv', 0)

    assert data == ['test string']

    os.remove('db/read_test.tsv')
