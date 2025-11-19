import json
from smolagents import Tool
from atlassian import Jira
import config

class JiraSubtaskCreationTool(Tool):
    """
    Tool for creating Jira subtasks
    """
    name = "jira_subtask_creator"
    description = "Creates a Jira subtask under a parent issue"
    
    inputs = {
        "parent_issue_key": {"type": "string", "description": "Parent issue key from jira_story_creator response."},
        "title": {"type": "string", "description": "Subtask title from the subtask object"},
        "description": {"type": "string", "description": "Subtask description from the subtask object"}
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
    
    def forward(self, parent_issue_key: str, title: str, description: str) -> str:
        """Create a Jira subtask"""
        try:
            subtask_type = None
            try:
                issue_types = self.jira.get_issue_types()
                
                for itype in issue_types:
                    name_lower = itype['name'].lower()
                    is_subtask = itype.get('subtask', False)
                    
                    if is_subtask or name_lower in ['sub-task', 'subtask', 'sub task']:
                        subtask_type = itype['name']
                        break
                
                if not subtask_type:
                    available_types = [t['name'] for t in issue_types]
                    return json.dumps({
                        'status': 'error',
                        'message': f"No subtask type found. Available: {', '.join(available_types)}"
                    })
            except Exception as e:
                return json.dumps({
                    'status': 'error',
                    'message': f"Failed to get issue types: {str(e)}"
                })
            
            subtask_dict = {
                'project': {'key': self.project_key},
                'parent': {'key': parent_issue_key},
                'summary': title,
                'description': description,
                'issuetype': {'name': subtask_type}
            }
            
            new_subtask = self.jira.create_issue(fields=subtask_dict)
            
            return json.dumps({
                'status': 'success',
                'issue_key': new_subtask['key']
            })
        except Exception as e:
            return json.dumps({'status': 'error', 'message': str(e)})