lowercase_reserverd_words = ['select', 'from', 'where', 'insert', 'into', 'values', 'delete', 'update']

def sql_normalizer(sql):
    splited = sql.split(' ')
    
    for word in splited:
        if word in lowercase_reserverd_words:
            splited[splited.index(word)] = word.upper()

    return ' '.join(splited)