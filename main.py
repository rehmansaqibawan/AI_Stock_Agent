# this is the main file which will be used to make some of the calls to api,tools,chains and Agents while using langchain
import os 
from dotenv import load_dotenv
from langchain_groq import ChatGroq
import yfinance as yf
from langchain.agents import Agent, tools, initialize_agent
import environ
import certifi


env = environ.Env()
environ.Env.read_env()

# Load the API key
os.environ["SSL_CERT_FILE"] = certifi.where()
os.environ["GROQ_API_KEY"] = env("GROQ_API_KEY")
print("GROQ_API_KEY:", os.getenv("GROQ_API_KEY"))
llm = ChatGroq(api_key=os.getenv("GROQ_API_KEY"))


response = llm.invoke("What is the stock price of Apple?")
print(response)
