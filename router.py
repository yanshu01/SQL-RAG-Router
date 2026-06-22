def route_query(query):

    query = query.lower()

    sql_keywords = [
        "salary",
        "department",
        "employee",
        "employees",
        "name"
    ]

    for keyword in sql_keywords:
        if keyword in query:
            return "sql"

    return "rag"