from sqlalchemy import text

from webapp.repository.db_engine import get_session


def run_query(query):
    session = get_session()
    try:
        # Execute the query
        result = session.execute(text(query))

        # Check if it’s a SELECT query to fetch results
        if query.strip().lower().startswith("select"):
            results = result.fetchall()  # Get all rows for SELECT queries
            # Convert results to a list of dictionaries for better readability
            columns = result.keys()
            return [dict(zip(columns, row)) for row in results]
        else:
            # Commit transaction for non-SELECT queries
            session.commit()
            return "Query executed successfully."

    except Exception as e:
        # Rollback in case of error and return error message
        session.rollback()
        return f"An error occurred: {e}"
