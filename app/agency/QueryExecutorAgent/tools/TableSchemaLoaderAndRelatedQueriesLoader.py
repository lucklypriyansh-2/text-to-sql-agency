from agency_swarm.tools import BaseTool
from pydantic import Field
import sqlite3

from sqlalchemy import text

from webapp.repository.db_engine import get_engine
from webapp.service.vector_service import query_index


class TableSchemaLoaderAndRelatedQueriesLoader(BaseTool):
    """
    These tools find the relevant tables and their schemas based on the user's request.'. It uses the vectorized prompt search to find relevant tables and their schemas.
    This tools also provides example  queries to the user's request. which can be used as examples of queries that can be used to answer the user's request.
    The related queries should be only treated as examples and should be adapted to the specific use case.The related queries contain reasoning for the example queries.
    watch carefully the reasoning for the example queries.'
    '
    """
    user_request: str = Field(
        None, description="The refined user's request. which contains all the relevant keywords and phrases from the user's request."
    )

    def run(self):
        """
        Uses the vectorized prompt search to find relevant tables and their schemas.
        """

        try:
           return query_index(self.user_request)
        except Exception as e:
            return f"An error occurred while querying the vector index: {e}"



