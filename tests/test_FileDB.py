from src.FileDB import run

def test_run_valid_query():
    raw_sql = 'select * from test'
    result_length = len(run(raw_sql))
    assert result_length > 0

def test_run_invalid_query():
    try:
      run('select * test')
    except Exception as e:
      assert e.args[0] == 'FROM not find in query.'