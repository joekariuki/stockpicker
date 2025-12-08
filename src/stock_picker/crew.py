from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool
from pydantic import BaseModel, Field
from typing import List

class TrendingCompany(BaseModel):
    """A company that is trending in the news and drawing attention"""
    name: str = Field(description="Company name")
    ticker: str = Field(description="Stock ticker symbol")
    reason: str = Field(description="Reason this company is trending in the news")

class TrendingCompanyList(BaseModel):
    """A list of trending companies in the news"""
    companies: List[TrendingCompany] = Field(description="List of trending companies in the news")

class TrendingCompanyResearch(BaseModel):   
    """Detailed re company in the news"""
    name: str = Field(description="Company name")
    market_position: str = Field(description="Current market position and competitive analysis")
    future_outlook: str = Field(description="Future outlook and growth prospects")
    investment_potential: str = Field(description="Investment potential and suitability for investment")

class TrendingCompanyResearchList(BaseModel):
    """A list of detailed research on all companies"""
    research_list: List[TrendingCompanyResearch] = Field(description="Comprehensive research on all trendingcompanies")


@CrewBase
class StockPicker():
    """StockPicker crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def trending_company_finder(self) -> Agent:
        return Agent(config=self.agents_config['trending_company_finder'], tools=[SerperDevTool()])

    @agent
    def financial_researcher(self) -> Agent:
        return Agent(config=self.agents_config['financial_researcher'], tools=[SerperDevTool()])

    @agent
    def stock_picker(self) -> Agent:
        return Agent(config=self.agents_config['stock_picker'])