import asyncio
from agents import Agent, Runner, InputGuardrail, GuardrailFunctionOutput
from pydantic import BaseModel
from dataclasses import dataclass
from homework_guardrail import check_homework_guardrail

qa_agent = Agent(
    name="QA Assistant",
    instructions="Answer user questions helpfully and clearly.",
    model="gpt-4o",
    input_guardrails=[
        InputGuardrail(guardrail_function=check_homework_guardrail)
    ]
)

async def main():
    print("Guardrail Q&A Bot (type 'exit' to quit)")

    while True:
        question = input("You: ")
        if question.lower() == "exit":
            print("Exiting...")
            break

        result = await Runner.run(qa_agent, question)
        print(f"AI:{result.final_output}")


if __name__ == "__main__":
    asyncio.run(main())

"""
You: こんにちは！
AI:こんにちは！今日はどのようなお手伝いができますか？
You: x^2 + 2x + 1 = 0    
宿題判定されました
Traceback (most recent call last):
~~
TypeError: GuardrailFunctionOutput.__init__() got an unexpected keyword argument 'message'
[non-fatal] Tracing: server error 500, retrying.
"""