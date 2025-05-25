import sqlite3
import functools

def log_queries():
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Extract the query from positional or keyword arguments
            query = None
            if 'query' in kwargs:
                query = kwargs['query']
            elif len(args) > 0:
                query = args[0]

            if query:
                print(f"Executing SQL query: {query}")

            return func(*args, **kwargs)
        return wrapper
    return decorator

@log_queries()
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

# Example usage:
users = fetch_all_users(query="SELECT * FROM users")
