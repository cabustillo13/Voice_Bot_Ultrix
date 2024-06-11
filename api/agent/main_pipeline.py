import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain.agents import tool
from langchain.agents import AgentExecutor
from langchain.agents.output_parsers import OpenAIFunctionsAgentOutputParser
from langchain.agents.format_scratchpad import format_to_openai_function_messages
from langchain_community.tools.convert_to_openai import format_tool_to_openai_function

from langchain_core.prompts import ChatPromptTemplate
from langchain.prompts import MessagesPlaceholder

from typing import Dict
from langchain.pydantic_v1 import BaseModel, Field

from api.agent.tools.search_on_google import google_search
from api.agent.tools.scraping_website import get_text_from_website


# Load the environment variables
load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")


# Load Large Language Model (LLM)
llm = ChatOpenAI(
    model_name="gpt-4-1106-preview",
    temperature=0,
    streaming=False,
)


# Define your custom tools
class GoogleSearch(BaseModel):
    """Google Search Class tool"""
    query: str = Field(description="A really high quality google search prompt")


@tool("search-on-google", args_schema=GoogleSearch)
def search_on_google(query: str) -> Dict:
    """Search the internet for the latest information about a topic."""
    print("API 1")
    result = google_search(query)
    return result


class ScrapingWebsite(BaseModel):
    """Web Scraping Class tool"""
    url: str = Field(description="url of website that needs to be scraped")


@tool("scraping-website", args_schema=ScrapingWebsite)
def scraping_website(url: str) -> str:
    """Scrape website content via url, do NOT make up urls."""
    print("API 2")
    result = get_text_from_website(url)
    return result


tools = [
    search_on_google,
    scraping_website,
]

# Bind the tools to the LLM
llm_with_tools = llm.bind(functions=[format_tool_to_openai_function(t) for t in tools])


role_assistant_prompt = """
You are a Market Intelligence Analyst. 
Your main role is to assist in the collection and analysis of market intelligence on various companies. 
Your goal is to provide a comprehensive view of the company's current position and activities in the market. 
You present this information in a structured format, highlighting key insights and trends. 
You strive to ensure that the information is current, relevant, and accurately reflects the company's market environment to support strategic decision-making. 
Citing credible sources is a priority to maintain the integrity and accuracy of the information provided.

You work at IgniteSoft (ignitesoftinc.com)
IgniteSoft is a leading AI solutioning company dedicated to crafting cutting-edge software applications powered by generative AI
BE BRIEF. YOUR FINAL ANSWER HAS TO HAVE LESS THAN 20 WORDS.
"""
    
# Create the prompt
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", role_assistant_prompt),
        MessagesPlaceholder(variable_name="chat_history"),
        ("user", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)

# Create the Agent
# We use this structure instead of "create_openai_tools_agent" to avoid Runtime errors and out of memory on Lambda AWS
agent = (
    {
        "input": lambda x: x["input"],
        "agent_scratchpad": lambda x: format_to_openai_function_messages(
            x["intermediate_steps"]
        ),
        "chat_history": lambda x: x["chat_history"],
    }
    | prompt
    | llm_with_tools
    | OpenAIFunctionsAgentOutputParser()
)

# Execute Agent
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    return_intermediate_steps=False,
)
