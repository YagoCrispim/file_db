from pathlib import Path
from typing import List

import pytest
from config import db_folder

class Tsv:
    def __init__(
        self,
        location: str = db_folder,
        extension: str = ".tsv",
    ):
        self.__location = location
        self.__extension = extension


    @pytest.mark.skip(reason="No need to test this method")
    def run(self, query: dict): # pragma: no cover
        if query["action"] == "SELECT":
            return self.select(query)

        if query["action"] == "INSERT":
            return self.insert(query)

        if query["action"] == "UPDATE":
            return self.update(query)

        if query["action"] == "DELETE":
            return self.delete(query)


    def insert(self, query: dict):
        table: str = query["table_name"]
        table_path: str = self.__location + table + self.__extension

        self.create_table_if_not_exist(table_path, query["columns"])

        try:
            for item in query["data"]:

                row = self.format_data(item)
                id: str = self.get_new_id(table_path)
                line: str = str(id) + '\t' + row

                self.write_on_file(table_path, line, "INSERT")
        except Exception as e: # pragma: no cover
            raise Exception(e)

        return 0


    def select(self, query: dict):
        res = []

        if query['columns'] == '*' and not "where" in query.keys():
            table = self.read_from_file(self.__location + query["table_name"] + self.__extension)
            
            for item in table:
                if item == '\n': continue

                final = item.replace('\t', ' ')[:-1]
                res.append([final.rstrip()])
            
            return res

        header_map = self.map_data_obj_to_file_columns(query["table_name"])
        table = self.read_from_file(self.__location + query["table_name"] + self.__extension)

        for item in table:
            items_in_column = item.split('\t')[:-1]
            
            col_to_filter = next(iter(query['where']))
            value_to_find = query['where'][col_to_filter]
            col_value = items_in_column[header_map[col_to_filter]]

            if col_value == value_to_find:
                if query["columns"][0] == "*":
                    res.append([item.replace('\t', ' ').rstrip()])
                else:
                    col_result = []
                    for col in query["columns"]:
                        col_name = col.replace(' ', '')
                        col_value = items_in_column[header_map[col_name]]
                        col_result.append(col_value)

                    res.append(col_result)

        return res


    @pytest.mark.skipif(reason="No need to test this method")
    def update(self, query: dict):     
        try:
            header_map = self.map_data_obj_to_file_columns(query["table_name"])
            path = self.__location + query["table_name"] + self.__extension
            file = open(path, 'r')
            lines = file.readlines()
            file.close()

            updated_file = open(path, 'w')

            for line in lines:
                id = line.split('\t')[0]

                if id == query['where']['id']:
                    line = line.split('\t')[:-1]
                    columns_to_change = query['data'].keys()

                    for column in columns_to_change:
                        if column in header_map:
                            line[header_map[column]] = f"'{query['data'][column]}'"

                    line = self.format_data(line, is_header=False)
                    updated_file.write(line)
                else:
                    updated_file.write(line)

            updated_file.close()
            
            return 0
        except Exception as e: # pragma: no cover
            raise Exception(e)
        finally:
            updated_file.close()


    @pytest.mark.skipif(reason="No need to test this method")
    def delete(self, query: dict):   
        try:
            path = self.__location + query["table_name"] + self.__extension   
            
            file = open(path, 'r')
            lines = file.readlines()
            file.close()

            updated_file = open(path, 'w')
            for line in lines:
                id = line.split('\t')[0]
            
                if id != query['where']['id']:
                    updated_file.write(line)

            updated_file.close()
        except Exception as e: # pragma: no cover
            raise Exception(e)

    
    def map_data_obj_to_file_columns(self, table_name: str):
        column_map = {}
        header = self.read_from_file(self.__location + table_name + self.__extension, 0)
        header = header[0].split('\t')[:-1]

        for i, item in enumerate(header):
            item = item.replace(' ', '')
            column_map[item] = i

        return column_map


    def get_new_id(self, table_path: str) -> str:
        try:
            last_line: list = self.read_from_file(table_path, line=-1)
            id = last_line[0].split("\t")[0]

            if id == 'id' or id == '\n':
                return 1
            
            return int(id) + 1
        except Exception as e: # pragma: no cover
            raise Exception(e)


    def write_on_file(self, table_path: str, data: str, action: str):
        parameter: str = 'a' if action == "INSERT" else 'r'

        with open(table_path, parameter) as table:
            table.write(data)


    def format_data(self, data: list, is_header: bool = False) -> str:
        line: str = ""
        
        if is_header: line += "id\t"

        for item in data:
            line.replace(' ', '')
            line += item + "\t"
        
        line += "\n"

        return line


    def create_table_if_not_exist(self, table_path: str, data: list):
        path: object = Path(table_path)
        if not path.exists():
            header: str = self.format_data(data, is_header=True)
            self.write_on_file(table_path, header, "INSERT")


    def read_from_file(self, table_path: str, line: int or 'str' = '*') -> List[str]:
        file: list = []
        lines_from_file: list = []

        try:
            with open(table_path, "r") as table:
                file: list = table.readlines()

            if line == '*':
                return file
            
            if line != '*':
                lines_from_file.append(file[line])
            
            else: # pragma: no cover
                lines_from_file.append(file)

        except: # pragma: no cover
            lines_from_file.append("")

        return lines_from_file
