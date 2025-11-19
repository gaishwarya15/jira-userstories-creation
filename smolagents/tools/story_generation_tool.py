import json
from typing import List
from smolagents import Tool
from pydantic import BaseModel
import openai
import config

class Subtask(BaseModel):
    """Subtask structure"""
    title: str
    description: str

class UserStory(BaseModel):
    """User story structure"""
    title: str
    user_story: str
    acceptance_criteria: List[str]
    story_points: int
    subtasks: List[Subtask]

class UserStories(BaseModel):
    """Collection of user stories"""
    stories: List[UserStory]

class StoryGenerationTool(Tool):
    """
    Generating user stories with subtasks
    """
    name = "story_generator"
    description = "Generates user stories for a given feature topic with optional research context"
    
    inputs = {
        "topic": {"type": "string", "description": "Feature topic to generate stories for"},
        "research_context": {"type": "string", "description": "Optional research context to inform story generation", "nullable": True}
    }
    output_type = "string"
    
    def forward(self, topic: str, research_context: str = "") -> str:
        """To generate user stories"""
        context_section = ""
        if research_context:
            context_section = f"\n\nResearch Context:\n{research_context}\n\nUse this research to inform your user stories."
        
        prompt = f"""Generate short, concise, 5 or more user stories for: {topic}{context_section}

Each story should have:
- A clear title
- User story in format: "As a [user], I want [goal], so that [benefit]"
- Few acceptance criteria
- Story points (1-5)
- 2-3 subtasks (specific implementation tasks)

Focus on security, usability and best practices based on the research context."""
        
        try:
            client = openai.OpenAI(api_key=config.OPENAI_API_KEY)
            
            completion = client.beta.chat.completions.parse(
                model=config.MODEL_ID,
                messages=[
                    {"role": "system", "content": "You are a product manager creating user stories."},
                    {"role": "user", "content": prompt}
                ],
                response_format=UserStories,
            )
            
            user_stories = completion.choices[0].message.parsed
            stories_list = [story.model_dump() for story in user_stories.stories]
            
            return json.dumps({"status": "success", "stories": stories_list})
            
        except Exception as e:
            return json.dumps({"status": "error", "message": str(e)})