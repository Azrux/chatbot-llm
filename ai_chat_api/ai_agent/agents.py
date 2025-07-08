"""
This module defines the AI agents used in the application.
"""
from langchain_openai import ChatOpenAI


gpt_turbo = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.3)
gpt_4 = ChatOpenAI(model="gpt-4", temperature=0.3)
