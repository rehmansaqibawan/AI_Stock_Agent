import os
import certifi
import yfinance as yf
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import MessagesPlaceholder
from langchain.prompts import ChatPromptTemplate
from langchain_core.tools import tool
from langchain.schema import HumanMessage
from datetime import date

# Load environment variables
load_dotenv()
os.environ["SSL_CERT_FILE"] = certifi.where()

# Initialize LLM with API key
llm = ChatGroq(api_key=os.getenv("GROQ_API_KEY"))

# Define stock price retrieval tool
@tool
def get_stock_price(symbol: str) -> str:
    """Retrieves the current stock price given a stock symbol."""
    try:
        ticker = yf.Ticker(symbol)
        todays_data = ticker.history(period='1d')
        if todays_data.empty:
            return f"No stock price data found for {symbol}. It may be delisted."
        return f"The current stock price of {symbol} is ${todays_data['Close'].iloc[-1]:.2f}"
    except Exception as e:
        return f"Error retrieving stock price for {symbol}: {str(e)}"

# Additional tools for stock-related queries
@tool
def company_information(ticker: str) -> dict:
    """Retrieves company information like industry, sector, and market capitalization."""
    return yf.Ticker(ticker).get_info()

@tool
def last_dividend_and_earnings_date(ticker: str) -> dict:
    """Retrieves the last dividend date and earnings release dates."""
    return yf.Ticker(ticker).get_calendar()

@tool
def stock_news(ticker: str) -> dict:
    """Retrieves the latest news articles related to a stock ticker."""
    return yf.Ticker(ticker).get_news()

# Define tools list
tools = [
    get_stock_price,
    company_information,
    last_dividend_and_earnings_date,
    stock_news,
]

# Define agent prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant. Try to answer user queries using available tools."),
    MessagesPlaceholder(variable_name="messages"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

# Initialize agent and executor
finance_agent = create_tool_calling_agent(llm, tools, prompt)
finance_agent_executor = AgentExecutor(agent=finance_agent, tools=tools, verbose=True)

# Get user input and execute query
company_name = input("Enter the company name: ")
response = finance_agent_executor.invoke(
    {"messages": [HumanMessage(content=f"What is the stock price of {company_name}?")]}
)
print(response)
