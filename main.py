# this is the main file which will be used to make some of the calls to api,tools,chains and Agents while using langchain
import os 
from dotenv import load_dotenv
from langchain_groq import chatgroq
import yfinance as yf
from langchain.agents import Agent, tools, initialize_agent
from langchain.chains import Chain
