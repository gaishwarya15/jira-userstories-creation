from smolagents import Tool, ToolCallingAgent, LiteLLMModel, DuckDuckGoSearchTool
import config

class ResearchTool(Tool):
    name = "research_agent"
    description = "Searches web for best practices and features related to a topic"
    
    inputs = {
        "topic": {"type": "string", "description": "Topic to research"}
    }
    output_type = "string"
    
    def __init__(self):
        super().__init__()
        model = LiteLLMModel(
            model_id=config.MODEL_ID,
            api_key=config.OPENAI_API_KEY
        )
        self.agent = ToolCallingAgent(
            tools=[DuckDuckGoSearchTool()],
            model=model,
            max_steps=1
        )
    
    def forward(self, topic: str) -> str:
        try:
            query = f"Search for best practices and common features for: {topic}. Respond in English."
            result = self.agent.run(query)
            return str(result)[:400]
        except Exception as e:
            return f"Research failed: {str(e)}"