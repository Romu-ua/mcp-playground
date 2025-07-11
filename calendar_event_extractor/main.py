"""
LLMの生成結果をカレンダーに登録できるデータ構造に限定していることが本質
"""

import asyncio 
from agents import Agent, Runner
from pydantic import BaseModel
from typing import List

class CalenderEvent(BaseModel):
    "会議名、日付、参加者リストを含むカレンダーイベントのデータ構造"
    name: str
    date: str
    participants: List[str]

calender_agent = Agent(
    name="Calender Event Extractor",
    instructions=(
        "Extract calendar envents from the input."
        "Return the event's name, data and participants."
    ),
    output_type=CalenderEvent,
    model="gpt-4o-mini"
)

async def main():
    print("Calender Evnet Extractor (type 'exit' to quit)")

    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("Exiting...")
            break

        result = await Runner.run(calender_agent, user_input)
        
        try:
            parsed = result.final_output_as(CalenderEvent)
            print("\n Evnet Parsed: ")
            print(f"Name: {parsed.name}")
            print(f"Data: {parsed.date}")
            print(f"Participants: {', '.join(parsed.participants)}\n")
        except Exception as e:
            print("Please ensure the input is in the correct format.")
            print(f"Raw output: \n {result.final_output}\n")

if __name__ == "__main__":
    asyncio.run(main())


