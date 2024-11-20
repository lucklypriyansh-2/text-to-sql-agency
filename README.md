# Text-to-SQL Agency

Text-to-SQL Agency is a project that transforms natural language queries into SQL statements, streamlining database interactions for users. This solution is inspired by Pinterest's approach to Text-to-SQL conversion  and leverages the Agency Swarm framework for orchestrating AI agents :contentReference[oaicite:0]{index=0}.

## Features

- **Natural Language Processing**: Converts user queries in plain English into accurate SQL commands.
- **Agent-Based Architecture**: Utilizes the Agency Swarm framework to manage AI agents, enhancing modularity and scalability.
- **Customizable**: Easily adaptable to various database schemas and user requirements.

## Prerequisites

Before setting up the application, ensure you have the following installed:

- **Python 3.8 or higher**
- **pip** (Python package installer)
- **Virtualenv** (optional but recommended for creating isolated Python environments)

## Installation

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/lucklypriyansh-2/text-to-sql-agency.git
   cd text-to-sql-agency
   ```
2. # Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate

3. #Agency Swarm Configuration:

Configure the Agency Swarm framework by setting up the necessary agents and tools as per your requirements. Refer to the Agency Swarm documentation for detailed instructions.


Start the Application:
  ```bash
python app/main.py
  ```
Access the Web Interface:

4. #call api

  ```bash
curl --location 'http://127.0.0.1:9090/completions?message=pull%20reuest%20review%20time%20vs%20no%20of%20commits&threadId=121' \
--data ''

  ```
5. Sequence diagram:
![Sequence Diagram]([path/to/your/image.png](https://github.com/lucklypriyansh-2/text-to-sql-agency/blob/main/images/Untitled%20(1).png))
  
Submit Queries:

Enter your natural language query into the input field and submit. The application will process the input and return the corresponding SQL statement.


   
