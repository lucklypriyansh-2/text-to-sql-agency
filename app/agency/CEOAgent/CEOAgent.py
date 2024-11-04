from agency_swarm.agents import Agent
from pydantic import BaseModel, Field
from typing import List, Literal

class CEOAgent(Agent):
    def __init__(self):
        super().__init__(
            name="CEOAgent",
            description="This agent is responsible for managing high-level decision-making and delegating tasks to the QueryExecutor agent.",
            instructions="./instructions.md",
            files_folder="./files",
            schemas_folder="./schemas",
            tools=[],
            tools_folder="./tools",
            temperature=0.3,
            max_prompt_tokens=25000,
            response_format=CEOAgentResponse
        )
        
    def response_validator(self, message):
        return message



class NameValuePair(BaseModel):
    dimensionName: str = Field(..., description="The name of dimension.")
    dimensionValue: str = Field(..., description="the value of dimension.")

class DataPoint(BaseModel):
    name: str = Field(..., description="The label or name for the data point on the chart.")
    value: List[NameValuePair] = Field(..., description="The numerical value associated with this data point.")

class ChartConfig(BaseModel):

    chartType: Literal["line", "bar", "pie","Not Possible"] = Field(
        ...,
        description="The type of chart to render. Supported values are 'line', 'bar',  'pie' and Not Possible in case data points are not suitable for any chart type."
    )
    data: List[DataPoint] = Field(
        None,
        description="A list of data points, each containing a 'name' and 'value', to plot on the chart."
    )
    xAxisKey: str = Field(
        None,
        description="The key to be used for values on the x-axis. Should match one of the attributes in 'data'."
    )
    yAxisKey: str = Field(
        None,
        description="The key to be used for values on the y-axis. Should match one of the attributes in 'data'."
    )

class CEOAgentResponse(BaseModel):
    chartConfig: ChartConfig = Field(..., description="The configuration for the chart.")
    queryExecutorResponse: str = Field(..., description="The response from the QueryExecutor Translated into a human readable sentence including the every data points and explaining the columns ")

