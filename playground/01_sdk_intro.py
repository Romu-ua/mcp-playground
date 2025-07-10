"""
OpenAI Agents SDK intro
"""

from agents import Agent, Runner

agent = Agent(name="Assistant", instructions="You are a helpful assistant.")

result = Runner.run_sync(agent, "プログラミングに関する俳句を書いて下さい。")
print("agent result: ", result)
print("agent model:", agent.model)

