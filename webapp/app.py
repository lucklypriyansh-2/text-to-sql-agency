import uuid
from typing import Dict

from agency_swarm import Agency
from flask import Flask, jsonify, request

from app.agency.agency import thread_id_var, ceo, query_executor, thread_state_storage
from webapp.service.query_service import run_query
from webapp.service.vector_service import refresh_vector_index, query_index
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


def load_thread() -> Dict:
    """Load the state of a specific thread."""
    return thread_state_storage.get(thread_id_var.get(), {})


def save_thread(state: Dict) -> None:
    """Save the state of a specific thread."""
    thread_id = thread_id_var.get()
    if thread_id:
        thread_state_storage[thread_id] = state
        print(f"Thread state saved: {state}")


threads_callbacks = {
    "load": load_thread,
    "save": save_thread
}

@app.route('/refresh_index', methods=['GET'])
def refresh_index_endpoint():
    """API endpoint to refresh the vector index."""
    try:
        refresh_vector_index()
        return jsonify({"message": "Index refreshed successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/run_query', methods=['GET'])
def run_query_endpoint():
    """API endpoint to refresh the vector index."""
    try:
        results= run_query(query = request.args.get('query'))
        return jsonify({"results": results}),200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/completions', methods=['GET'])
def completions():
    """API endpoint to get a completion from the git-work-agency."""
    try:
        thread_id_var.set(request.args.get('threadId', str(uuid.uuid4())))
        agency = Agency([
            ceo,
            query_executor,
            [ceo, query_executor],
        ],
        threads_callbacks=threads_callbacks,
        max_prompt_tokens=25000,  # default tokens in conversation for all agents
        temperature=0,  # default temperature for all agents
        )

        data = agency.get_completion(
            message=request.args.get('message'),
        )
        return jsonify({"response": data}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/query_index', methods=['GET'])
def query_index_endpoint():
    """API endpoint to query the vector index."""
    query = request.args.get('query')
    if not query:
        return jsonify({"error": "Query parameter is required"}), 400
    try:
        results = query_index(query)
        return jsonify(results), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

