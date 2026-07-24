from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from app.agents.state import AgentState
from app.agents.nodes.planner import planner_node
from app.agents.nodes.retriever import retrieve_node
from app.agents.nodes.responder import generate_node

#1. initialize the state graph 
workflow = StateGraph(AgentState)

#2. define the nodes 
workflow.add_node("planner",planner_node)
workflow.add_node("retriever", retrieve_node)
workflow.add_node("responder", generate_node)

#3.define teh edges & routing logic 
