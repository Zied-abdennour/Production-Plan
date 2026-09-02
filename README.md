# Production Planner

An AI-assisted production planning system that combines a Genetic Algorithm with a local LLM and Retrieval-Augmented Generation (RAG) to generate, store, retrieve, and query optimized production plans.

## Overview

The system allows users to:

- Define production orders
- Define products and their operations
- Configure workplaces
- Define production rates
- Configure Genetic Algorithm parameters
- Generate optimized production schedules
- Visualize schedules on a production timeline
- Store equal-score production plans
- Store plan embeddings in ChromaDB
- Retrieve relevant production plans using semantic search
- Ask questions about production plans using a local LLM

## Architecture

```text
Production Data
      |
      v
Streamlit GUI
      |
      v
Genetic Algorithm
      |
      +--> Production Sequence
      +--> Workplace Assignment
      +--> Schedule
      |
      v
Optimized Production Plans
      |
      v
data/plans.json
      |
      v
Ollama + nomic-embed-text
      |
      v
ChromaDB
      |
      v
RAG Retriever
      |
      v
Qwen3 0.6B
      |
      v
Production Planning Assistant
```

## Technologies

- Python
- Streamlit
- Genetic Algorithms
- Ollama
- Qwen3 0.6B
- nomic-embed-text
- ChromaDB
- Requests
- Pandas
- NumPy

## Project Structure

```text
Production-Plan/
|
+-- app.py
+-- requirements.txt
+-- setup.ps1
|
+-- algorithm/
|   +-- genetic_algorithm.py
|   +-- decoder.py
|   +-- crossover.py
|   +-- mutation.py
|   +-- score.py
|
+-- data/
|   +-- example_data.py
|   +-- plans.json
|   +-- chroma/
|
+-- gui/
|   +-- style.py
|
+-- pages/
|   +-- dashboard.py
|   +-- workplaces.py
|   +-- operations.py
|   +-- products.py
|   +-- rates.py
|   +-- orders.py
|   +-- parameters.py
|   +-- results.py
|
+-- rag/
    +-- plan_store.py
    +-- retrieve.py
    +-- chatbot.py
```

## Requirements

- Python 3.11 or newer
- Windows PowerShell
- Internet connection during the first setup

Ollama and the required AI models are handled by the provided `setup.ps1` script.

## Installation

### 1. Clone the repository

```powershell
git clone <repository-url>
cd Production-Plan
```

### 2. Run the setup script

Open PowerShell in the project directory and run:

```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\setup.ps1
```

The setup script:

1. Installs the Python dependencies from `requirements.txt`.
2. Checks whether Ollama is available.
3. Pulls `qwen3:0.6b`.
4. Pulls `nomic-embed-text`.
5. Starts the local Ollama server.
6. Checks that the Ollama API is available.
7. Displays the installed Ollama models.

No manual Python package installation is required when using `setup.ps1`.

> Note: `setup.ps1` assumes Ollama is already installed on the computer. The script cannot install the Ollama Windows application itself. After Ollama is installed once, the script handles the model setup and local server startup.

## Ollama

The application uses Ollama as the local AI server.

The server runs locally at:

```text
http://localhost:11434
```

The project uses two models with different purposes.

### Qwen3 0.6B

Used by the chatbot to generate answers:

```text
qwen3:0.6b
```

### nomic-embed-text

Used to convert production plans and user questions into embeddings:

```text
nomic-embed-text
```

These embeddings are stored in ChromaDB for semantic retrieval.

## Running the Application

After setup, start Streamlit:

```powershell
streamlit run app.py
```

Streamlit will start the local web application.

If Ollama was not started by `setup.ps1`, start it with:

```powershell
ollama serve
```

Then run:

```powershell
streamlit run app.py
```

## Using the Production Planner

### 1. Load Data

Use the sidebar:

```text
Load Example Data
```

or enter your own production data.

### 2. Configure Production

The application supports:

- Workplaces
- Operations
- Products
- Production rates
- Orders
- Deadlines

### 3. Configure the Genetic Algorithm

Default parameters:

```text
Generations: 100
Population size: 50
Selection percentage: 20%
Mutation rate: 10%
```

### 4. Run Optimization

Open the `Results` page and click:

```text
Run Genetic Algorithm
```

The system generates production schedules and evaluates them using the project's scoring function.

The lower the score, the better the schedule according to the current scoring mechanism.

## Production Timeline

The Results page displays the optimized schedule horizontally.

```text
Time ->   0       10       20       30       40       50       60

WP1       [Order1 Op1]             [Order3 Op3]
WP2               [Order2 Op1] [Order3 Op1]
WP3                         [Order2 Op3] [Order1 Op3]
```

Each block represents an operation assigned to a workplace.

## RAG Pipeline

After the Genetic Algorithm finishes, equal-score plans are saved to:

```text
data/plans.json
```

The plans are converted into text.

The text is sent to Ollama using:

```text
nomic-embed-text
```

The resulting vectors are stored in:

```text
data/chroma/
```

The complete RAG process is:

```text
Production Plans
      |
      v
Text Representation
      |
      v
nomic-embed-text
      |
      v
Embeddings
      |
      v
ChromaDB
      |
      v
Semantic Retrieval
```

## Testing the Retriever

Run:

```powershell
python -m rag.retrieve
```

Enter a question such as:

```text
Which plans have a score of 0?
```

The retriever returns the production plans that are semantically closest to the question.

Example:

```text
--- Retrieved Plan ---
Distance: 0.7621
Production plan Plan_07.
Score: 0.
...
```

The distance is the similarity-search distance returned by ChromaDB. Lower distance generally means the retrieved document is closer to the query embedding.

## Testing the Chatbot

Run:

```powershell
python -m rag.chatbot
```

The chatbot:

1. Receives the user's question.
2. Creates an embedding for the question.
3. Searches ChromaDB.
4. Retrieves relevant production plans.
5. Sends the retrieved information to Qwen3 0.6B.
6. Generates an answer based on the retrieved plans.

Example questions:

```text
Which plans have a score of 0?
```

```text
What workplaces are used by Plan_42?
```

```text
What are the differences between Plan_42 and Plan_48?
```

```text
Why can two plans have the same score?
```

## Streamlit Chatbot

The chatbot can also be integrated into the Streamlit interface.

The GUI communicates with the RAG pipeline:

```text
User Question
      |
      v
Retriever
      |
      v
ChromaDB
      |
      v
Relevant Plans
      |
      v
Qwen3 0.6B
      |
      v
Answer displayed in Streamlit
```

## Data Storage

The main plan file is:

```text
data/plans.json
```

Its structure contains information such as:

```json
{
  "best_score": 0,
  "number_of_equal_plans": 48,
  "plans": [
    {
      "plan_id": "Plan_01",
      "score": 0,
      "sequence": [],
      "workplace_assignment": {},
      "schedule": []
    }
  ]
}
```

The vector database is stored locally in:

```text
data/chroma/
```

This directory contains the persistent ChromaDB data.

## Genetic Algorithm

The optimization process includes:

- Population initialization
- Selection
- Precedence-preserving crossover
- Workplace crossover
- Sequence mutation
- Workplace mutation
- Schedule decoding
- Score calculation

Main implementation:

```text
algorithm/genetic_algorithm.py
```

## Scoring

The optimization objective is:

```text
Minimize Score
```

The scoring mechanism is implemented in:

```text
algorithm/score.py
```

Depending on the current implementation, the score can account for production constraints such as:

- Order deadlines
- Workplace conflicts
- Operation timing
- Schedule feasibility

## Local AI

The AI components run locally through Ollama.

```text
Qwen3 0.6B
      |
      v
Ollama
      |
      v
localhost:11434
```

No external LLM API is required for the chatbot.

Embeddings are also generated locally:

```text
nomic-embed-text
```

## Useful Commands

Install dependencies manually:

```powershell
python -m pip install -r requirements.txt
```

Run setup:

```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\setup.ps1
```

Check Ollama models:

```powershell
ollama list
```

Run Qwen directly:

```powershell
ollama run qwen3:0.6b
```

Start Ollama:

```powershell
ollama serve
```

Run Streamlit:

```powershell
streamlit run app.py
```

Test the RAG retriever:

```powershell
python -m rag.retrieve
```

Test the chatbot:

```powershell
python -m rag.chatbot
```

## Future Improvements

Possible extensions include:

- PDDL-based production planning
- Temporal planning
- Multi-objective optimization
- More production constraints
- Automatic JSON validation
- Better plan comparison
- RAG answer verification
- Natural-language production order creation
- LLM-generated structured production requests
- Production KPI dashboards
- Database integration
- Multi-user deployment
- Integration with ERP or MES systems

## License

This project is intended for educational, research, and experimental purposes.
