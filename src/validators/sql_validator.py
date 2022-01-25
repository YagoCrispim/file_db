def query_validator(query):
    if query == "":
        return False, "Empty query."

    action = query.split(" ")[0]
    allowed_methods = ['SELECT', 'INSERT', 'DELETE', 'UPDATE']
    
    if not action in allowed_methods:
        return False, "Invalid query."

    if "INSERT" in query:
        if "INTO" not in query:
            return False, "INTO not find in query."

        if "VALUES" not in query:
            return False, "VALUES not find in query."

    if action == "SELECT":
        if "FROM" not in query:
            return False, "FROM not find in query."

    # FIX's
    # Check if the table name was informed
    # if "WHERE" in query
    # if "DELETE" in query:
    #     return True, "UPDATE"

    # FIX's
    # Check if the table name was informed
    # if "WHERE" in query
    # if "UPDATE" in query:
    #     return True, "UPDATE"

    return True, ""
