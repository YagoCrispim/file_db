from src.services.sql_normalizer import sql_normalizer


def test_reserved_words_to_uppercase():
    res = sql_normalizer('select * from users where id = 1')

    assert res == 'SELECT * FROM users WHERE id = 1'