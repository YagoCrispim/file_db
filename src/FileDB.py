# =-=-=-=-= Interactors =-=-=-=-=
from .interactors.Tsv import Tsv

# =-=-=-=-= Services =-=-=-=-=
from .services.sql_parser import sql_parser
from .services.sql_normalizer import sql_normalizer

# =-=-=-=-= Validators =-=-=-=-=
from .validators.sql_validator import query_validator

# TODO: New feature soon
# def run(raw_sql, driver=None):

def run(raw_sql):
    # =-=-=-=-= Validation =-=-=-=-=
    sql = sql_normalizer(raw_sql)
    validation, message = query_validator(sql)

    if not validation:
        raise Exception(message)

    # =-=-=-=-= Execution =-=-=-=-=
    query = sql_parser(sql)
    result = Tsv().run(query)

    return result
