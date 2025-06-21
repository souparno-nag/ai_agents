import os
from dotenv import load_dotenv
load_dotenv()
# Import necessary libraries
import phi
from phi.agent import Agent
from phi.model.groq import Groq
from phi.tools.duckduckgo import DuckDuckGo
from phi.tools.yfinance import YFinanceTools

from phi.app import Playground
from phi.app.serve import serve_playground_app

phi.api = os.getenv("PHI_API_KEY")

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

app = Playground(
    agents=[finance_agent, web_search_agent],
    title="Financial Analysis Assistant",
    description="AI-powered stock analysis and market insights"
).get_app()

# if __name__ == "__main__":
#     serve_playground_app("playground:app", reload=True)

if __name__ == "__main__":
    serve_playground_app(app=app, reload=True)