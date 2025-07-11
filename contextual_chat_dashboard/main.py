import asyncio
from dataclasses import dataclass, field
from typing import List
from agents import Agent, Runner, function_tool, RunContextWrapper, ModelSettings

@dataclass
class DashboardContext:
    uid: str
    notes: List[str] = field(default_factory=list)

    def add_note(self, content: str):
        print(f"[DEBUG] BEFORE: notes = {self.notes}")
        self.notes.append(content)
        print(f"[DEBUG] AFTER: notes = {self.notes}")
    
    # 使用しないが、getter的に定義
    def list_notes(self) -> List[str]:
        return self.notes
    

@function_tool
def add_note(ctx: DashboardContext, content: str) -> str:
    ctx.add_note(content)
    return f"Note added: {content}"

@function_tool
def show_notes(ctx: DashboardContext) -> str:
    print(f"[DEBUG] Notes when calling show_notes = {ctx.notes}")
    if not ctx.notes:
        return "No notes yet."
    return "\n".join(f"- {note}" for note in ctx.notes)


def dynamic_instructions(ctx: RunContextWrapper[DashboardContext], agent: Agent) -> str:
    return (
        f"You are a helpful assistant for user {ctx.context.uid}. "
        "Use tools to add or show notes. Always greet the user with their UID."
    )

# [DashboardContext]は型ヒント
agent = Agent[DashboardContext](
    name="Dashboard Agent",
    instructions=dynamic_instructions,
    tools=[add_note, show_notes],
    model="gpt-4o",
    tool_use_behavior="auto",
    model_settings=ModelSettings(tool_choice="required") 
)

async def main():
    print("Dashboard REPL Agent (type 'exit' to quit)")

    ctx = DashboardContext(uid="user42")

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() == "exit":
            break
        
        result = await Runner.run(agent, user_input, context=ctx)
        print(f"\n {agent.name}: {result.final_output}\n")

if __name__ == "__main__":
    asyncio.run(main())