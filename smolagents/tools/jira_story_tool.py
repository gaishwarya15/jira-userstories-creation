import json
from smolagents import Tool
from atlassian import Jira
import config

class JiraStoryCreationTool(Tool):
    """
    Tool for creating stories in Jira
    """
    name = "jira_story_creator"
    description = "Creates a Jira user story with title, description and story points. Returns JSON with 'issue_key' field that must be used as parent_issue_key when creating subtasks."
    
    inputs = {
        "title": {"type": "string", "description": "Story title"},
        "description": {"type": "string", "description": "Story description"},
        "story_points": {"type": "integer", "description": "Story points (1-5)"}
    }
    output_type = "string"
    
    def __init__(self):
        super().__init__()
        self.jira = Jira(
            url=config.JIRA_URL,
            username=config.JIRA_EMAIL,
            password=config.JIRA_API_TOKEN,
            cloud=True
        )
        self.project_key = "AUTO"
    
    def forward(self, title: str, description: str, story_points: int) -> str:
        """Create a Jira story"""
        try:
            try:
                project = self.jira.project(self.project_key)
            except Exception as e:
                return json.dumps({'status': 'error', 'message': f"Project '{self.project_key}' not found: {str(e)}"})
            
            try:
                issue_types = self.jira.project_issue_types(project['id'])
                
                issue_type_name = 'Task'
                for itype in issue_types:
                    if itype['name'].lower() == 'story':
                        issue_type_name = 'Story'
                        break
                    elif itype['name'].lower() == 'task':
                        issue_type_name = 'Task'
            except:
                issue_type_name = 'Task'
            
            issue_dict = {
                'project': {'key': self.project_key},
                'summary': title,
                'description': description,
                'issuetype': {'name': issue_type_name},
            }
            
            new_issue = self.jira.create_issue(fields=issue_dict)
            issue_url = f"{config.JIRA_URL}/browse/{new_issue['key']}"
            
            return json.dumps({
                'status': 'success',
                'issue_key': new_issue['key'],
                'issue_url': issue_url,
                'issue_id': new_issue['id']
            })
        except Exception as e:
            error_msg = str(e)
            if 'project' in error_msg.lower():
                error_msg = f"Project issue: {error_msg}"
            elif 'permission' in error_msg.lower() or 'unauthorized' in error_msg.lower():
                error_msg = f"Permission denied: {error_msg}"
            return json.dumps({'status': 'error', 'message': error_msg})