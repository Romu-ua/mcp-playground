import asyncio
from agents import Agent, Runner

base_agent = Agent(
    name="Neutral",
    instructions="You are a helpful assistant. Respond to the user naturally.",
    model="gpt-4o-mini",
)

# clone and define
pirate_agent = base_agent.clone(
    name="Pirate",
    instructions="Talk like a pirate. Be dramatic and use pirate slang like 'Arrr!' and 'Ahoy!'",
)

robot_agent = base_agent.clone(
    name="Robot",
    instructions="Respond in a robotic tone. Be precise and use language like 'processing' and 'confirmed'.",
)

poet_agent = base_agent.clone(
    name="Poet",
    instructions="Respond in poetic form. Use metaphor, rhyme, and emotion to express everything beautifully.",
)

kansai_agent = base_agent.clone(
    name="Kansai",
    instructions="Speak in Kansai dialect of Japanese. Be friendly, casual, and funny like a Kansai local.",
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
        agent_name = input("\nSelect an agent: ").strip().lower()
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
