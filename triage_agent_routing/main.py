import asyncio
from agents import Agent, Runner

math_agent = Agent(
    name="math Expert",
    instructions="You help with math questions. Use formulas, examples, and step-by-step reasoning."
)

history_agent = Agent(
    name="history Expert",
    instructions="You help with history questions. Explain clearly with dates, people, and context."
)

general_agent = Agent(
    name="General Knowledge Expert",
    instructions="You help with general non-math and non-historyquestions. Be friendly and informative."
)


# triage (ルーティング担当)
triage_agent = Agent(
    name="Triage Agent",
    instructions=(
        "You are a router. Decide what kind of question the user is asking.\n"
        "- If it's math question, delegate to Math Export.\n"
        "- If it's history question, delegate to History Export.\n"
        "- Otherwise, answer yourself or delegate to General Knowledge Export.\n"
    ),
    handoffs=[math_agent, history_agent, general_agent],
    model="gpt-4o",   
)

async def main():
    print("Triage Agent Demo (type 'exit' to quit)")

    while True:
        question = input("You: ")
        if question.lower() == "exit":
            print("exiting...")
            break

        result = await Runner.run(triage_agent, question)
        print(f"Response: {result.final_output}")

if __name__ == "__main__":
    asyncio.run(main())