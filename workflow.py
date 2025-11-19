import json
from typing import List, Dict
from smolagents import ToolCallingAgent, LiteLLMModel
import config
from jira_helpers import list_projects, create_project

from tools.research_tool import ResearchTool
from tools.story_generation_tool import StoryGenerationTool
from tools.jira_story_tool import JiraStoryCreationTool
from tools.jira_subtask_tool import JiraSubtaskCreationTool

research_tool = ResearchTool()
story_tool = StoryGenerationTool()
jira_story_tool = JiraStoryCreationTool()
jira_subtask_tool = JiraSubtaskCreationTool()

orchestrator_model = LiteLLMModel(
    model_id=config.MODEL_ID,
    api_key=config.OPENAI_API_KEY
)

orchestrator_agent = ToolCallingAgent(
    tools=[
        research_tool,
        story_tool,
        jira_story_tool,
        jira_subtask_tool
    ],
    model=orchestrator_model,
    max_steps=30
)


def create_jira_stories(topic: str, project_key: str = None) -> Dict:
    """
    Jira Stories Generator
    """
    print(f"Topic: {topic}\n")
    
    # Get or create project 
    if not project_key:
        print("Listing projects...")
        projects = list_projects()
        
        if projects:
            print(f"\nExisting projects ({len(projects)}):")
            for proj in projects[:5]:
                print(f"  {proj['key']}: {proj['name']}")
        
        print(f"\nEnter project key (existing or new): ", end="")
        project_key = input().strip().upper()
        
        if not project_key:
            print("Error: Project key is required")
            return {"status": "error", "message": "No project key provided"}
        
        existing_keys = {proj['key'].upper() for proj in projects} if projects else set()
        
        if project_key not in existing_keys:
            print(f"\nProject '{project_key}' not found. Creating new project...")
            project_name = f"{project_key} - {topic}"
            if create_project(project_key, project_name):
                print(f"Created project: {project_key} ({project_name})")
                print()
            else:
                print(f"Failed to create project: {project_key}")
                return {"status": "error", "message": f"Failed to create project {project_key}"}
        else:
            print(f"Using existing project: {project_key}\n")
    
    jira_story_tool.project_key = project_key
    jira_subtask_tool.project_key = project_key

    
    task = f"""
Complete the full workflow for topic: {topic}

1. Use research_agent tool to research best practices for: {topic}

2. Use story_generator tool with the research context to generate user stories with subtasks

3. REPEAT FOR EACH USER STORY in the story_generator response:
   
   a. Use jira_story_creator tool with:
        * title: Use the "title" field from the story
        * description
        * Acceptance Criteria:
        * story_points
   
   b. WAIT for jira_story_creator response and extract the "issue_key" (e.g., "TEST7-1")
   
   c. Use jira_subtask_creator tool with:
      - REPEAT for each subtask in the story's "subtasks" array:
          - parent_issue_key: The actual issue_key from step 3b (NOT a placeholder)
          - title: Use the subtask's "title" field
          - description: Use the subtask's "description" field

Project: {project_key}
Topic: {topic}

CRITICAL: 
- Extract ALL fields from each story in the story_generator JSON response
- Include user_story text AND all acceptance_criteria in the description
- Create ALL subtasks for each story
- Use the actual issue_key returned from jira_story_creator for subtasks
- Process each story completely (story + all its subtasks) before moving to next story

Execute all steps sequentially and provide a summary at the end.
"""
    
    try:
        result = orchestrator_agent.run(task)
        print(f"\nAgent Workflow Completed")
        print(f"\nResult: {result}\n")
        
        return {
            "status": "success",
            "result": str(result)
        }
        
    except Exception as e:
        print(f"\nError: {e}")
        return {"status": "error", "message": str(e)}

