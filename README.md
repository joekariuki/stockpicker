<div align="center">
    <h1>StockPicker</h1>
    <p>
        A multi-agent AI system that identifies trending companies, runs financial research, and produces first pass stock investment ideas in under 5 minutes.
    </p>

</div>

## Overview

StockPicker uses a team of specialized AI agents to analyze market trends and surface promising investment opportunities. It searches for trending companies in a chosen sector, runs deep financial research, and provides detailed investment recommendations with clear reasons why.

## Demo

![StockPicker Demo](demo.gif)

_This is a technical demo, not investment advice._

> **Note**: The demo may take a few seconds to load.
>
> Watch StockPicker identify trending companies, run research, and make investment recommendations.

## How it works

StockPicker runs a sequential workflow with three specialized agents and a manager agent:

### 1. Trending Company Finder (Financial News Analyst Agent)

- Searches the latest news for trending companies in the specified sector
- Identifies 2-3 new companies that haven't been analyzed before
- Uses web search to find current market trends
- Outputs a structured list of trending companies

### 2. Financial Researcher (Senior Financial Researcher Agent)

- Receives the list of trending companies
- Conducts comprehensive research on each company
- Analyzes market position, competitive landscape, and future outlook
- Evaluates investment potential for each company
- Generates detailed research reports

### 3. Stock Picker Agent (Stock Picker from Research)

- Synthesizes all research findings
- Selects the best investment opportunity
- Provides detailed rationale for the selection
- Explains why other companies were not chosen
- Optionally sends push notifications with the decision

### Manager Agent

The manager agent coordinates the workflow, delegates tasks, and keeps the system focused on selecting the best investment opportunity.

### Memory systems

- **Short-term memory**: Maintains context during the current run
- **Long-term memory**: Persists knowledge across runs using SQLite
- **Entity memory**: Tracks specific companies and entities so they are not analyzed twice

## Features

- **Multi-agent collaboration**: Three specialized agents work together while a manager coordinates tasks
- **Advanced memory systems**:
  - Short-term memory for recent context
  - Long-term memory for persistent knowledge
  - Entity memory for tracking companies and entities
- **Intelligent web search**: Real-time internet search using the Serper API
- **Structured outputs**: Pydantic models ensure consistent, validated data structures
- **Push notifications**: Optional push notification support via Pushover API
- **Sector-specific analysis**: Configurable sector focus (default: Technology)
- **Comprehensive reports**: Generates JSON and Markdown reports with detailed analysis
- **Duplicate prevention**: Agents remember previously analyzed companies to avoid repetition

## Tech stack

- **Framework**: [CrewAI](https://crewai.com) - Multi-agent AI orchestration
- **Language**: Python 3.10 - 3.13
- **LLM providers**:
  - OpenAI GPT-4o-mini (for agents)
  - OpenAI GPT-4o (for manager)
- **Memory storage**:
  - SQLite (long-term memory)
  - RAG storage with OpenAI embeddings (short-term and entity memory)
- **Tools**:
  - SerperDevTool (web search)
  - PushNotificationTool (optional push notifications)
- **Data validation**: Pydantic v2
- **Package management**: UV (fast Python package installer)

## Prerequisites

- Python >=3.10 and <3.14
- [UV](https://docs.astral.sh/uv/) package manager
- OpenAI API key
- Serper API key (for web search)
- (Optional) Pushover credentials for push notifications

## Installation

### Step 1: Install UV

If you haven't already, install UV:

```bash
pip install uv
```

### Step 2: Clone and navigate

```bash
git clone <repository-url>
cd stockpicker
```

### Step 3: Install dependencies

Install project dependencies using CrewAI CLI:

```bash
crewai install
```

Or manually with UV:

```bash
uv sync
```

### Step 4: Environment configuration

Copy the `.env.example` file to `.env` and add your API keys:

```bash
cp .env.example .env
```

Then edit the `.env` file and fill in your API keys:

```bash
# Required
OPENAI_API_KEY=your_openai_api_key_here
SERPER_API_KEY=your_serper_api_key_here

# Optional - for push notifications
PUSHOVER_USER=your_pushover_user_key
PUSHOVER_TOKEN=your_pushover_token

# Optional - for Chroma vector store
CHROMA_OPENAI_API_KEY=your_chroma_openai_api_key_here
```

### Step 5: Verify installation

Verify the installation by checking the project structure:

```bash
ls -la src/stock_picker/
```

You should see:

- `crew.py` - Main crew configuration
- `main.py` - Entry point
- `config/` - Agent and task configurations
- `tools/` - Custom tools

## Disclaimer

This tool is for research and educational purposes only. It does not provide investment advice. Always conduct your own due diligence before making investment decisions.

## Usage

### Basic usage

Run the StockPicker with default settings (Technology sector):

```bash
crewai run
```

Or using Python directly:

```bash
python -m stock_picker.main
```

### Customization

#### Modify agents

Edit `src/stock_picker/config/agents.yaml` to customize agent roles, goals, and backstories.

#### Modify tasks

Edit `src/stock_picker/config/tasks.yaml` to adjust task descriptions, expected outputs, and dependencies.

#### Change sector

Edit `src/stock_picker/main.py` to change the sector:

```python
inputs = {
    'sector': 'Healthcare',  # Change to your desired sector
    'current_year': str(datetime.now().year)
}
```

#### Enable push notifications

Uncomment the push notification tool in `src/stock_picker/crew.py`:

```python
@agent
def stock_picker(self) -> Agent:
    return Agent(
        config=self.agents_config['stock_picker'],
        tools=[PushNotificationTool()],  # Uncommented
        memory=True
    )
```

## Project structure

```
stock_picker/
├── src/
│   └── stock_picker/
│       ├── __init__.py
│       ├── crew.py              # Crew configuration and agent definitions
│       ├── main.py              # Entry point
│       ├── config/
│       │   ├── agents.yaml      # Agent configurations
│       │   └── tasks.yaml       # Task definitions
│       └── tools/
│           └── push_tool.py     # Push notification tool
├── output/                      # Generated reports
│   ├── trending_companies.json
│   ├── research_report.json
│   └── decision.md
├── memory/                      # Memory storage
│   └── long_term_memory_storage.db
├── knowledge/                   # Knowledge base
│   └── user_preference.txt
├── pyproject.toml               # Project configuration
├── uv.lock                      # Dependency lock file
└── README.md
```

## Output

The system generates three output files:

1. **`output/trending_companies.json`**: List of trending companies with names, tickers, and reasons
2. **`output/research_report.json`**: Comprehensive research on each company including market position, future outlook, and investment potential
3. **`output/decision.md`**: Final decision with chosen company, rationale, and reasons for not selecting others

## Configuration

### Agents configuration

Agents are defined in `src/stock_picker/config/agents.yaml`. Each agent has:

- **role**: The agent's role in the team
- **goal**: What the agent aims to achieve
- **backstory**: Context about the agent's expertise
- **llm**: The language model to use

### Tasks configuration

Tasks are defined in `src/stock_picker/config/tasks.yaml`. Each task has:

- **description**: What the task should accomplish
- **expected_output**: The format of the output
- **agent**: Which agent handles the task
- **context**: Dependencies on other tasks
- **output_file**: Where to save the results

## Development

### Running tests

```bash
crewai test
```

### Adding custom tools

1. Create a new tool in `src/stock_picker/tools/`
2. Inherit from `crewai.tools.BaseTool`
3. Implement the `_run` method
4. Add the tool to the appropriate agent in `crew.py`

### Memory customization

Memory systems can be customized in `crew.py`:

- Adjust embedding models
- Change storage paths
- Modify memory types

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
