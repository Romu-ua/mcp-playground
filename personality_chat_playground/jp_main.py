import asyncio
from agents import Agent, Runner

base_agent = Agent(
    name="Neutral",
    instructions="You are a helpful assistant. Respond to the user naturally.",
    model="gpt-4o-mini",
)

pirate_agent = base_agent.clone(
    name="Pirate",
    instructions="海賊のように話してください。『アホイ！』『ヨーソロー！』などのスラングを使って、陽気で大胆に答えてください。",
)

robot_agent = base_agent.clone(
    name="Robot",
    instructions="ロボットのように話してください。正確で機械的な口調を使い、『処理中です』『確認しました』などの語彙を含めてください。",
)

poet_agent = base_agent.clone(
    name="Poet",
    instructions="詩人のように表現してください。隠喩や韻を踏み、感情豊かに美しく表現してください。",
)

kansai_agent = base_agent.clone(
    name="Kansai",
    instructions="関西弁で話してください。親しみやすく、ユーモアを交えて楽しく答えてください。",
)

base_agent = Agent(
    name="Neutral",
    instructions="親切なアシスタントとして、自然な日本語で丁寧に答えてください。",
    model="gpt-4o-mini",
)


# personality chat dictionary
agents = {
    "pirate": pirate_agent,
    "robot": robot_agent,
    "poet": poet_agent,
    "kansai": kansai_agent,
    "neutral": base_agent,
}

async def main():
    print("Personality Chat Playground (type 'exit' to quit)\n")
    print("Available agents:", ", ".join(agents.keys()))

    while True:
        agent_name = input("\nSelect an agent ").strip().lower()
        if agent_name not in agents:
            print("Unknown agent. Please try again.")
            continue
        if agent_name == "exit":
            print("Exiting the playground.")
            break
        agent = agents[agent_name]
        print(f"\nChatting with {agent.name}. Type 'exit' to stop.")

        while True:
            user_input = input("You: ")
            if user_input.lower() == "exit":
                print("Exiting chat with", agent.name)
                break
            result = await Runner.run(agent, user_input)
            print(f"{agent.name}: {result.final_output}")

if __name__ == "__main__":
    asyncio.run(main())
