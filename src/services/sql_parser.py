import re


def sql_parser(sql: str) -> dict:
    mid_lang: dict = {}

    if "INSERT" in sql:

        data: list = []
        regex = r"\((.*?)\)"

        sql_splited: list = sql.split(" ")
        table_name: str = sql_splited[2]

        between_parentheses: list = re.findall(regex, sql, re.MULTILINE)
        columns: list = between_parentheses[0].split(",")

        for idx, item in enumerate(between_parentheses):
            if idx != 0:
                el: list = []
                item_splited: list = item.split(",")

                for i in item_splited:
                    el.append(i.replace('"', ""))

                data.append(el)

        mid_lang["action"] = "INSERT"
        mid_lang["columns"] = columns
        mid_lang["data"] = data
        mid_lang["table_name"] = table_name

        return mid_lang

    if "SELECT" in sql:
        query_splited = sql.split(" ")
        table_name = query_splited[query_splited.index("FROM") + 1]

        mid_lang["action"] = "SELECT"
        mid_lang["table_name"] = table_name

        if "*" in query_splited:
            mid_lang["columns"] = "*"
            return mid_lang

        regex = r"\((.*?)\)"
        columns = re.findall(regex, sql, re.MULTILINE)

        mid_lang["columns"] = columns[0].split(",")

        id_position = query_splited.index("WHERE") + 3
        id = query_splited[id_position]

        if int(id) < 0:
            raise Exception("Id cannot be 0 or negative.")

        # FIX: tem forma melhor de pegar o id
        mid_lang["where"] = {"id": id}

        return mid_lang

    if "UPDATE" in sql:

        query_splited = sql.split(" ")
        table_name = query_splited[1]

        # FIX: tem forma melhor de pegar o id
        id_position = query_splited.index("WHERE") + 3
        id = query_splited[id_position]

        if int(id) < 0:
            raise Exception("Id cannot be 0 or negative.")

        data_obj = {}
        reg = regex = r"\w* = '\w*'"
        columns = re.findall(reg, sql, re.MULTILINE)

        for column in columns:
            column_splited = column.split(" = ")
            data_obj[column_splited[0]] = column_splited[1].replace("'", "")


        # FIX: tem forma melhor de pegar o id
        set_stmt_position = query_splited.index("SET")
        column = query_splited[set_stmt_position + 1]

        mid_lang["action"] = "UPDATE"
        mid_lang["table_name"] = table_name
        mid_lang["data"] = data_obj
        mid_lang["where"] = {"id": id}

        return mid_lang

    if "DELETE" in sql:
        query_splited = sql.split(" ")
        table_name = query_splited[query_splited.index("FROM") + 1]

        mid_lang["table_name"] = table_name

        id_position = query_splited.index("WHERE") + 3
        id = query_splited[id_position]

        if int(id) < 0:
            raise Exception("Id cannot be 0 or negative.")

        mid_lang["action"] = "DELETE"
        # FIX: tem forma melhor de pegar o id
        mid_lang["where"] = {"id": id}

        return mid_lang
