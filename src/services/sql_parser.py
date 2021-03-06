import re


def sql_parser(sql: str) -> dict:
    mid_lang: dict = {}
    raw_sql_splited: list = sql.split(" ")

    if "INSERT" in sql:
        table_name: str = raw_sql_splited[2]

        data_between_parentheses: list = re.findall(r"\((.*?)\)", sql, re.MULTILINE)
        
        new_data: list = []
        columns: list = data_between_parentheses[0].split(",")

        for idx, item in enumerate(data_between_parentheses):
            if idx == 0: continue

            data_element: list = []
            item_splited: list = item.split(",")

            for i in item_splited:
                data_element.append(i.replace('"', ""))

            new_data.append(data_element)

        mid_lang["action"] = "INSERT"
        mid_lang["columns"] = columns
        mid_lang["data"] = new_data
        mid_lang["table_name"] = table_name

        return mid_lang

    if "SELECT" in sql:
        table_name = raw_sql_splited[raw_sql_splited.index("FROM") + 1]

        if not "WHERE" in raw_sql_splited and "*" in raw_sql_splited:
            mid_lang["action"] = "SELECT"
            mid_lang["columns"] = "*"
            mid_lang["table_name"] = table_name
            
            return mid_lang

        where_condition = __return_where_condition(raw_sql_splited)

        data_between_parentheses: list = re.findall(r"\((.*?)\)", sql, re.MULTILINE)
        
        if not data_between_parentheses: data_between_parentheses = "*"

        mid_lang["action"] = "SELECT"
        mid_lang["columns"] = data_between_parentheses[0].split(",")
        mid_lang["table_name"] = table_name
        mid_lang["where"] = where_condition

        return mid_lang

    if "UPDATE" in sql:
        table_name = raw_sql_splited[1]

        where_condition = __return_where_condition(raw_sql_splited)
        
        columns = re.findall(r"\w* = '\w*'", sql, re.MULTILINE)

        data_obj = {}
        for column in columns:
            column_splited = column.split(" = ")
            data_obj[column_splited[0]] = column_splited[1].replace("'", "")

        set_stmt_position = raw_sql_splited.index("SET")
        column = raw_sql_splited[set_stmt_position + 1]

        mid_lang["action"] = "UPDATE"
        mid_lang["data"] = data_obj
        mid_lang["table_name"] = table_name
        mid_lang["where"] = where_condition

        return mid_lang

    if "DELETE" in sql:
        where_condition = __return_where_condition(raw_sql_splited)

        table_name = raw_sql_splited[raw_sql_splited.index("FROM") + 1]

        mid_lang["action"] = "DELETE"
        mid_lang["table_name"] = table_name
        mid_lang["where"] = where_condition

        return mid_lang

def __return_where_condition(sql_splited: list) -> str:
    where_condition_position = sql_splited.index("WHERE")
    condition = sql_splited[where_condition_position]

    try:
        key = sql_splited[where_condition_position + 1]
        value = sql_splited[where_condition_position + 3]

        return {key: value}
    except:
        return condition

