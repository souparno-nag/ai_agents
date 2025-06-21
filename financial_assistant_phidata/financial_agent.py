from phi.agent import Agent
from phi.model.groq import Groq
from phi.tools.duckduckgo import DuckDuckGo
from phi.tools.yfinance import YFinanceTools

import os
from dotenv import load_dotenv
load_dotenv()

# Web Search Agent for financial news
web_search_agent = Agent(
    name="Web Search Agent",
    role="Search the web for latest financial news and information",
    model=Groq(model="llama3-8b-preview"),
    tools=[DuckDuckGo()],
    instructions=[
        "Always include sources in your response",
        "Focus on financial news and market analysis",
        "Provide recent and relevant information"
    ],
    markdown=True,
    show_tool_calls=True,
)

# Financial Analysis Agent using YFinance
finance_agent = Agent(
    name="Finance AI Agent",
    role="Analyze stocks and provide financial recommendations",
    model=Groq(model="llama3-8b-preview"),
    tools=[YFinanceTools(
        analyst_recommendations=True,
        company_news=True,
        technical_indicators=True,
        stock_fundamentals=True,
        stock_price = True,
    )],
    instructions=[
        "Present data in organized tables",
        "Provide both technical and fundamental analysis",
        "Include risk factors in recommendations"
    ],
    markdown=True,
    show_tool_calls=True,
)
    

# Combine both agents into a multi agent system

multi_agent = Agent(
    name="Financial Assistant",
    model=Groq(model="llama3-8b-preview"),
    team=[web_search_agent, finance_agent],
    instructions=[
        "Combine web information with financial data",
        "Provide comprehensive analysis",
        "Present information in a clear, structured format",
        "Always include both technical and fundamental factors"
    ],
    markdown=True,
    show_tool_calls=True
)

multi_agent.print_response("Summmarise analyst recommendations and share the latest news for NVIDIA")