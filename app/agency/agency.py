import contextvars
import os
from typing import Dict

from agency_swarm import Agency, set_openai_key
from app.agency.CEOAgent.CEOAgent import CEOAgent
from app.agency.QueryExecutorAgent.QueryExecutorAgent import QueryExecutorAgent
from webapp.service.vector_service import refresh_vector_index

ceo = CEOAgent()
query_executor = QueryExecutorAgent()
set_openai_key(os.environ.get('OPENAI_API_KEY')) # replace with your OpenAI API key
thread_state_storage = {}
thread_id_var = contextvars.ContextVar('thread_id')

agency = Agency([
                 ceo,
                 query_executor,
                 [ceo, query_executor],
                 ],
                shared_instructions='./agency_manifesto.md', # shared instructions for all agents
                max_prompt_tokens=25000, # default tokens in conversation for all agents
                temperature=0.3, # default temperature for all agents
                )

if __name__ == '__main__':
    refresh_vector_index()
    agency.demo_gradio()
