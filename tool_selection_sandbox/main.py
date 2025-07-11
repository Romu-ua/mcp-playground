import asyncio
from agents import Agent, Runner, function_tool
from datetime import datetime
import random

# ツールの定義
@function_tool
def get_weather(city: str) -> str:
    weather = random.choice(["sunny", "cloudy", "rainy", "stormy"])
    return f"The weather in {city} is currently {weather}."

@function_tool
def get_time(city: str) -> str:
    now = datetime.utcnow()
    return f"The current UTC time for {city} is {now.strftime('%Y-%m-%d %H:%M:%S')}."

@function_tool
def tell_joke() -> str:
    return "Why did the programmer quit his job? Because he didn't get arrays."


tool_agent = Agent(
    name="Toolful Assistatnt",
    instructions=(
        "You are a helpful assistant that uses tools to answer questions when appropriate.\n"
        "Use the correct tool depending on what the user is asking."
    ),
    tools=[get_weather, get_time, tell_joke],
    model="gpt-4o-mini"
)

async def main():
    print("Tool Use Sandbox (type 'exit' to quit)")
    print("Available tools: weather, time, joke")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("Exiting...")
            break
        result = await Runner.run(tool_agent, user_input)
        print(f"AI: {result.final_output}\n")

if __name__ == "__main__":
    asyncio.run(main())


