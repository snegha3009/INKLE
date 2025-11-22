"""
Tourism Orchestrator Agent (Parent Agent)
Uses LangChain ReAct agent to coordinate child agents.
"""

from langchain.agents import create_react_agent, AgentExecutor
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from typing import Dict, Optional
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class TourismOrchestrator:
    """
    Parent Agent that orchestrates Weather and Places child agents.
    Uses LangChain's ReAct pattern for reasoning and acting.
    """
    
    def __init__(self, tools: list, verbose: bool = True):
        """
        Initialize the orchestrator agent.
        
        Args:
            tools: List of LangChain tools (WeatherAgent, PlacesAgent)
            verbose: Whether to print agent's reasoning process
        """
        self.tools = tools
        self.verbose = verbose
        
        # Initialize LLM
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError(
                "OPENAI_API_KEY not found. Please set it in .env file or environment variables."
            )
        
        self.llm = ChatOpenAI(
            temperature=0,  # Deterministic responses
            model=os.getenv("OPENAI_MODEL", "gpt-3.5-turbo"),
            openai_api_key=api_key
        )
        
        # Create agent
        self.agent = self._create_agent()
        self.agent_executor = AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            verbose=self.verbose,
            handle_parsing_errors=True,
            max_iterations=5
        )
    
    def _create_agent(self):
        """Create the ReAct agent with custom prompt"""
        
        template = """You are a tourism assistant helping users plan their trips.

You have access to these tools:
{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action (should be ONLY the place name)
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Important rules:
1. Extract the place name from the user's query
2. If user asks about weather, use WeatherAgent
3. If user asks about places to visit, use PlacesAgent
4. If user asks about both, use both tools
5. Always provide a natural, conversational response
6. If a place doesn't exist, respond: "I don't know this place exists"

Begin!

Question: {input}
Thought: {agent_scratchpad}"""

        prompt = PromptTemplate.from_template(template)
        
        return create_react_agent(self.llm, self.tools, prompt)
    
    def process_query(self, user_query: str) -> Dict:
        """
        Process a user query and return the response.
        
        Args:
            user_query: The user's input query
            
        Returns:
            Dict with 'output' (response) and 'success' (bool)
        """
        try:
            result = self.agent_executor.invoke({"input": user_query})
            return {
                "output": result["output"],
                "success": True
            }
        except Exception as e:
            error_msg = f"Error processing query: {str(e)}"
            print(error_msg)
            return {
                "output": "Sorry, I encountered an error processing your request.",
                "success": False,
                "error": str(e)
            }
    
    def chat(self):
        """Interactive chat loop for testing"""
        print("="*60)
        print("Tourism Assistant - Multi-Agent System")
        print("="*60)
        print("Ask me about weather or places to visit!")
        print("Type 'quit' or 'exit' to end the conversation.\n")
        
        while True:
            user_input = input("You: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("\nThank you for using Tourism Assistant! Goodbye!")
                break
            
            if not user_input:
                continue
            
            print("\nAssistant: ", end="")
            result = self.process_query(user_input)
            print(result["output"])
            print()


# For testing
if __name__ == "__main__":
    print("Testing Tourism Orchestrator...\n")
    
    # Import tools
    import sys
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from agents.tools import TourismTools
    
    # Create tools
    tools_factory = TourismTools()
    tools = tools_factory.create_tools()
    
    # Create orchestrator
    try:
        orchestrator = TourismOrchestrator(tools, verbose=True)
        print("✓ Orchestrator created successfully\n")
        
        # Start interactive chat
        orchestrator.chat()
        
    except ValueError as e:
        print(f"✗ Error: {e}")
        print("\nPlease create a .env file with your OPENAI_API_KEY")