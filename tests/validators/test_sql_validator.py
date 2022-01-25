from src.validators.sql_validator import query_validator

def test_empty_query():
    boolean, message = query_validator('')

    assert boolean == False
    assert message == "Empty query."

def test_allowed_sql():
    sql = 'SELECT * FROM users'
    boolean, message = query_validator(sql)

    assert boolean == True
    assert message == ""


def test_not_allowed_sql():
    sql = 'SELECIONE * FROM users'
    boolean, message = query_validator(sql)

    assert boolean == False
    assert message == "Invalid query."

def test_incomplete_sql_without_into_stmt():
    sql = 'INSERT test users'
    boolean, message = query_validator(sql)

    assert boolean == False
    assert message == "INTO not find in query."

def test_incomplete_sql_without_values_stmt():
    sql = 'INSERT test INTO users ("teste", "teste")'
    boolean, message = query_validator(sql)

    assert boolean == False
    assert message == "VALUES not find in query."

def test_incomplete_sql_without_from_stmt():
    sql = 'SELECT * USERS'
    boolean, message = query_validator(sql)

    assert boolean == False
    assert message == "FROM not find in query."

