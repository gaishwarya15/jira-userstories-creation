from atlassian import Jira
import config

def get_jira_client():
    """Jira client"""
    return Jira(
        url=config.JIRA_URL,
        username=config.JIRA_EMAIL,
        password=config.JIRA_API_TOKEN,
        cloud=True
    )

def list_projects():
    """
    List of all existing Jira projects
    """
    try:
        jira = get_jira_client()
        projects = jira.projects(included_archived=False)
        return projects if projects else []
    except Exception as e:
        print(f"Error listing projects: {e}")
        return []

def create_project(project_key: str, project_name: str):
    """
    Creating new Jira project
    """
    try:
        import requests
        from requests.auth import HTTPBasicAuth
        
        jira = get_jira_client()
        url = f"{config.JIRA_URL}/rest/api/3/project"
        auth = HTTPBasicAuth(config.JIRA_EMAIL, config.JIRA_API_TOKEN)
        headers = {"Accept": "application/json", "Content-Type": "application/json"}
        
        payload = {
            "key": project_key,
            "name": project_name,
            "projectTypeKey": "software",
            "projectTemplateKey": "com.pyxis.greenhopper.jira:gh-simplified-agility-kanban",
            "description": f"Auto-generated project for: {project_name}",
            "leadAccountId": jira.myself()['accountId']
        }
        
        response = requests.post(url, json=payload, headers=headers, auth=auth)
        
        if response.status_code == 201:
            return True
        else:
            try:
                error_data = response.json()
                if 'errors' in error_data:
                    error_msgs = []
                    for key, value in error_data['errors'].items():
                        error_msgs.append(f"{key}: {value}")
                    error_msg = "; ".join(error_msgs)
                    print(f"Failed to create project: {error_msg}")
                else:
                    print(f"Failed to create project: {response.text}")
            except:
                print(f"Failed to create project: {response.text}")
            return False
            
    except Exception as e:
        print(f"Error creating project: {e}")
        return False
