from typing import List, Any

from agency_swarm.agents import Agent
from pydantic import BaseModel, Field


class QueryExecutorAgent(Agent):
    def __init__(self):
        super().__init__(
            name="QueryExecutorAgent",
            description="This agent is responsible for translating user requests into executable queries, loading relevant tables, schema, and similar queries, and running the query.",
            instructions="./instructions.md",
            files_folder="./files",
            schemas_folder="./schemas",
            tools=[],
            tools_folder="./tools",
            temperature=0.3,
            max_prompt_tokens=25000,
            response_format=QueryResponse
        )



class RowResponse(BaseModel):
    values: List[str] = Field(..., description="Values of a row")

class QueryResponse(BaseModel):
    columns: List[str] = Field(..., description="List of columns ")
    rows: List[RowResponse] = Field(..., description="List of rows")
