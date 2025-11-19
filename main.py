"""
Jira User Story Generator
- ResearchTool 
- StoryGenerationTool
- JiraStoryCreationTool
- JiraSubtaskCreationTool
"""
from workflow import create_jira_stories

def main():
    print("Jira User Story Generator\n")
    topic = input("Enter project Topic: ").strip()
    if not topic:
        print("Error: Project Topic is required")
        return
    
    print()
    
    result = create_jira_stories(topic=topic)
    
    if result['status'] == 'success':
        print("\nWorkflow completed successfully")
    else:
        print(f"\nWorkflow failed: {result.get('message', 'Unknown error')}")


if __name__ == "__main__":
    main()

