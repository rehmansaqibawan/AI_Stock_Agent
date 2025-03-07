# this is the main file which will be used to make some of the calls to api,tools,chains and Agents while using langchain
import os 
from dotenv import load_dotenv
from langchain_groq import ChatGroq
import yfinance as yf
from langchain.agents import Agent, tools, initialize_agent
import environ
import certifi
from langchain.agents import AgentType, Tool, initialize_agent
from langchain_core.tools import tool, StructuredTool
from datetime import date
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain.prompts import ChatPromptTemplate
from langchain_core.prompts import MessagesPlaceholder
from langchain import hub
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain.prompts import ChatPromptTemplate
from langchain_core.prompts import MessagesPlaceholder



env = environ.Env()
environ.Env.read_env()

# Load the API key
os.environ["SSL_CERT_FILE"] = certifi.where()
os.environ["GROQ_API_KEY"] = env("GROQ_API_KEY")
print("GROQ_API_KEY:", os.getenv("GROQ_API_KEY"))
llm = ChatGroq(api_key=os.getenv("GROQ_API_KEY"))


response = llm.invoke("What is the stock price of Apple?")
print(response)

llm = ChatGroq(temperature=0, groq_api_key=os.getenv("GROQ_API_KEY"))

def get_stock_price(symbol):
    ticker = yf.Ticker(symbol)
    todays_data = ticker.history(period='1d')
    return f"The current stock price of {symbol} is ${todays_data['Close'].iloc[-1]:.2f}"

tools = [
    Tool(
        name="StockPrice",
        func=get_stock_price,
        description="Useful for getting the stock price of a company. The input should be the stock symbol of the company."
    )
]

agent = initialize_agent(
    tools, 
    llm, 
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

query = "What's the current stock price of Nvidia?"
response = agent.invoke(query)
print(response)

@tool
def get_stock_price(symbol):
    """Use this tool to get the stock price of a company. The input should be the stock symbol of the company."""
    ticker = yf.Ticker(symbol)
    todays_data = ticker.history(period='1d')
    return f"The current stock price of {symbol} is ${todays_data['Close'].iloc[-1]:.2f}"

tools = [get_stock_price]

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful assistant. Try to answer user query using available tools.",
        ),
        MessagesPlaceholder(variable_name="messages"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)



finance_agent = create_tool_calling_agent(llm, tools, prompt)

finance_agent_executor = AgentExecutor(agent=finance_agent, tools=tools, verbose=True)

from langchain_core.messages import HumanMessage

response = finance_agent_executor.invoke({"messages": [HumanMessage(content="What is the stock price of Apple?")]})
response