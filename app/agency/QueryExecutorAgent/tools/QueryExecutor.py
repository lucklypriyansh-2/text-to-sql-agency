from agency_swarm.tools import BaseTool
from pydantic import Field
from sqlalchemy import text
from webapp.repository.db_engine import get_session

class QueryExecutor(BaseTool):
    """
    This tool executes a SQL query against a database using SQLAlchemy.
    It validates the SQL query's syntax, executes it, and returns the results for SELECT queries.
    """

    query: str = Field(
        ..., description="The SQL query to be executed."
    )

    def run(self):
        """
        Executes the SQL query using SQLAlchemy session.
        If it's a SELECT query, it fetches and returns the results.
        Reports errors if any occur during execution.
        """
        session = get_session()
        try:
            # Execute the query
            result = session.execute(text(self.query))

            # Check if it’s a SELECT query to fetch results

            results = result.fetchall()  # Get all rows for SELECT queries
                # Convert results to a list of dictionaries for better readability
            columns = result.keys()
            session.commit()
            return [dict(zip(columns, row)) for row in results]


        except Exception as e:
            # Rollback in case of error and return error message
            session.rollback()
            return f"An error occurred: {e}"

        finally:
            session.close()