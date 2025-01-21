from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import ConfigurableField
from langchain_core.tools import tool
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_openai import ChatOpenAI

# Define your tools using decorators
@tool
def get_weather(location: str) -> str:
    """Get current temperature for a given location."""
    # Simulated response for the example
    return "Sunny"

@tool
def send_email(to: str, subject: str, body: str) -> str:
    """Send an email to a given recipient with a subject and message."""
    # Simulated response
    return f"Email sent to {to}."

@tool
def search_knowledge_base(query: str, options: dict) -> str:
    """Query a knowledge base to retrieve relevant info on a topic."""
    # Simulated response
    return f"Results for query: {query}"

# Set up the prompt structure
prompt = ChatPromptTemplate.from_messages([
    ("system", "You're a helpful assistant"), 
    ("human", "{input}"), 
    ("placeholder", "{agent_scratchpad}"),
])

# Initialize tools
tools = [get_weather, send_email, search_knowledge_base]

# Set up the language model
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# Create the agent
agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# Invoke the agent with the user query
result = agent_executor.invoke({"input": "What is the weather like in Paris today?"})

print(result)
