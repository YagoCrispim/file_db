from src.FileDB import run

try:
    # SELECT's
    sql = "SELECT * FROM test"
    # sql = "SELECT * FROM dev"
    # sql = "SELECT (name, age) FROM dev WHERE id = 1"
    # sql = "SELECT (id, name, age, grade) FROM dev WHERE id = 2"
    # sql = "SELECT * FROM dev WHERE id = 2"
    # sql = "SELECT (grade) FROM dev WHERE name = 'Fulano'"
    # sql = "SELECT (name, age) FROM dev WHERE name = 'Fulano'"

    # INSERT's
    # sql = "insert into dev (name, age, grade) values ('Fulano','35','5'), ('Fulano','40','10')"

    # DELETE's
    # sql = "DELETE FROM dev WHERE id = 29"

    # UPDATE's
    # sql = "UPDATE dev SET name = 'Fulaninho' WHERE id = 2"
    # sql = "UPDATE dev SET name = 'Beltranovsky', age = '150', grade = '20' WHERE id = 2"

    result = run(sql)
    print(result)
except Exception as e:
    print(e)
