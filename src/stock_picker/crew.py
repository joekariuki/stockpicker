from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from pydantic import BaseModel
from typing import List


@CrewBase
class StockPicker():
    """StockPicker crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'


