# Jira User Story Generator

Give a project title, it researches best practices for that topic, generates user stories and creates Jira tickets automatically

## Brief Description

The system uses an orchestrator agent that coordinates multiple tools, including self-implemented Jira API integration tools and a web research tool.

## Features

### Custom Tool Implementation
- **JiraStoryCreationTool**: Self-implemented tool for creating Jira user stories
- **JiraSubtaskCreationTool**: Self-implemented tool for creating subtasks
- **ResearchTool**: Custom tool wrapping web search agent
- **StoryGenerationTool**: Custom tool using OpenAI structured output

### Multi-Agent Orchestration
- **Orchestrator Agent**: Coordinates the entire workflow
- **Research Agent**: Embedded ToolCallingAgent using DuckDuckGoSearchTool
- Agents work together in a coordinated pipeline

### Autonomous Operation
- **Automatically creates Jira projects** if they don't exist
- Interactive project selection or creation

## Project Structure

```
smolagents/
├── config.py              # Configuration (loads from .env)
├── jira_helpers.py        # Jira project management helpers
├── workflow.py            # Main orchestration workflow
├── main.py                # Entry point
├── tools/
│   ├── research_tool.py           # Web research tool
│   ├── story_generation_tool.py   # User story generation tool
│   ├── jira_story_tool.py         # Jira story creation tool
│   └── jira_subtask_tool.py       # Jira subtask creation tool
├── requirements.txt       
├── .gitignore            
└── README.md             
```

## Installation

1. **Install dependencies:**
   
   Create a virtual environment and install the requirements
   
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment variables:**
   
   Create a `.env` file in the project root with the following fields:

   ```bash
   OPENAI_API_KEY=your_openapi_key
   JIRA_URL=https://your-domain.atlassian.net
   JIRA_EMAIL=your-email@gmail.com
   JIRA_API_TOKEN=jira_token
   MODEL_ID=gpt-4.1-nano
   ```

   **Required fields:**
   - `OPENAI_API_KEY` 
   - `JIRA_URL` 
   - `JIRA_EMAIL` 
   - `JIRA_API_TOKEN` 

   **Optional fields:**
   - `MODEL_ID` - OpenAI model ID (defaults to "gpt-4.1-mini" if not provided)

3. **Get API Keys:**
   
   **OpenAI API Key:**
   - Sign up at https://platform.openai.com/
   - Go to API Keys section
   - Create a new API key
   
   **Jira API Token:**
   - Log into your Jira account
   - Go to: Account Settings → Security → API Tokens
   - Click "Create API Token"
   - Copy and paste into your `.env` file


## Usage

### Run the demo:
```bash
python main.py
```

The program will:
1. Ask for a project topic for which you want user stories
2. List existing Jira projects or let you create a new one
3. Research best practices for the topic
4. Generate user stories with subtasks
5. Create Jira tickets and subtasks automatically


## How It Works

### Architecture Overview

```
User Input → Project Setup → Orchestrator Agent → Research Tool → Story Generator Tool → Jira Story Tool → Jira Subtask Tool
```

### Step-by-Step Workflow

1. **Project Management**
   - Lists existing Jira projects
   - Prompts user to select or create a project
   - Automatically creates project if key doesn't exist

2. **Research Tool**
   - Uses embedded ToolCallingAgent with DuckDuckGoSearchTool
   - Searches web for best practices related to the topic
   - Returns research context

3. **Story Generation Tool**
   - Generates user stories with the reseach content:
     - Title
     - User story (As a... I want... So that...)
     - Acceptance criteria
     - Story points
     - Subtasks (2-3 per story)

4. **Jira Creation**
   - Creates user story tickets using JiraStoryCreationTool
   - Extracts issue_key from created story
   - Creates subtasks using JiraSubtaskCreationTool
   - Links subtasks to parent story automatically
