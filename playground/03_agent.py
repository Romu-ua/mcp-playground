"""
Documentation -> Agents
コード前半でDocumentationの内容を実装して、後半で具体的に使ってみる。
"""

# ---前半---

# Basic configuration
from agents import Agent, ModelSettings, function_tool

@function_tool
def get_weather(city: str) -> str:
    return f"The weather in {city} is sunny."

agent = Agent(
    name="Haiku agent",
    instructions="Always respond in haiku form.",
    model="gpt-4o-mini",
    tools=[get_weather]
)

# context
from dataclasses import dataclass

@dataclass
class UserContext:
    uid: str
    is_pro_user: bool

    async def fetch_purchases() -> list[str]:
        return ...

agent = Agent[UserContext](
    ...
)

# Output types
from pydantic import BaseModel
from agents import Agent

class CalendarEvent(BaseModel):
    name: str
    data: str
    participants: list[str]

agent = Agent(
    name="Calender agent",
    instructions="Extract calender events from text",
    output_type=CalendarEvent,
)

# handoffs
from agents import Agent

booking_agent = Agent(...)
refund_agent = Agent(...)
triage_agent = Agent(
    name="Triage agent",
    instructions=(
        "Help the user with their questions.",
        "If they ask about booking, handff to the booking agent.",
        "If they ask about refunds, handoff to the refund agent.",
    ),
    handoffs=[booking_agent, refund_agent]
)

# dynamic instructions
from agents import Agent, RunContextWrapper
def dynamic_instructions(
        context: RunContextWrapper[UserContext], anget: Agent[UserContext]
) -> str:
    return f"The user's name is {context.context.name}. Help them with their questions."

agent = Agent(
    name="Triage agent",
    instructions=dynamic_instructions
)

# cloning/copying agents
pirate_agent = Agent(
    name="Pirate",
    instructions="Write like a pirate.",
    model="gpt-4o-mini",
)

robot_agent = pirate_agent.clone(
    name="Robot",
    instructions="Write like a robot.",
)

# ---後半---

