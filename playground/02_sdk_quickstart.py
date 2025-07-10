"""
python sdkのquickstart

[memo]
--  handoffs ---
triage_agent = Agent(
    name="Triage Agent",
    instructions="You determine which agent to use based on the user's homework question",
    handoffs=[history_tutor_agent, math_tutor_agent]
)

handoffsでエージェントを渡す時に何を見ているのか？
おそらくnameとhandoff_descriptionを見ている？他に見ている部分はあるのか？
TODO : その辺を調べる

-- orchestration --
from agents import Runner

async def main():
    result = await Runner.run(triage_agent, "What is the capital of France?")
    print(result.final_output)

handoffsとorchestrationの違いは何か？
-> handoffsはエージェント間の引き継ぎを行うためのもので、orchestrationはエージェントの実行を管理するためのもの。

-- auardrail --

from agents import GuardrailFunctionOutput, Agent, Runner
from pydantic import BaseModel

class HomeworkOutput(BaseModel):
    is_homework: bool
    reasoning: str

guardrail_agent = Agent(
    name="Guardrail check",
    instructions="Check if the user is asking about homework.",
    output_type=HomeworkOutput,
)

async def homework_guardrail(ctx, agent, input_data):
    result = await Runner.run(guardrail_agent, input_data, context=ctx.context)
    final_output = result.final_output_as(HomeworkOutput)
    return GuardrailFunctionOutput(
        output_info=final_output,
        tripwire_triggered=not final_output.is_homework,
    )

ユーザーの入出力を検証する
pydanticでモデルの型を指定している。
実際にエージェントを動かしている部分はresult = await Runner.run(guardrail_agent, input_data, context=ctx.context)
ここであり、それ以降は出力のパースとtripwrireで処理の停止もしくは警告？をしている。

全てをまとめると ↓
"""

from agents import Agent, InputGuardrail, GuardrailFunctionOutput, Runner
from pydantic import BaseModel
import asyncio

class HomeworkOutput(BaseModel):
    is_homework: bool
    reasoning: str

guardrail_agent = Agent(
    name="Guardrail check",
    instructions="Check if the user is asking about homework.",
    output_type=HomeworkOutput,
)

math_tutor_agent = Agent(
    name="Math Tutor",
    handoff_description="Specialist agent for math questions",
    instructions="You provide help with math problems. Explain your reasoning at each step and include examples",
)

history_tutor_agent = Agent(
    name="History Tutor",
    handoff_description="Specialist agent for historical questions",
    instructions="You provide assistance with historical queries. Explain important events and context clearly.",
)


async def homework_guardrail(ctx, agent, input_data):
    result = await Runner.run(guardrail_agent, input_data, context=ctx.context)
    final_output = result.final_output_as(HomeworkOutput)
    return GuardrailFunctionOutput(
        output_info=final_output,
        tripwire_triggered=not final_output.is_homework,
    )

triage_agent = Agent(
    name="Triage Agent",
    instructions="You determine which agent to use based on the user's homework question",
    handoffs=[history_tutor_agent, math_tutor_agent],
    input_guardrails=[
        InputGuardrail(guardrail_function=homework_guardrail),
    ],
)

async def main():
    result = await Runner.run(triage_agent, "who was the first president of the united states?")
    print(result.final_output)

    result = await Runner.run(triage_agent, "what is life")
    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())

"""
output:

The first President of the United States was George Washington. He served from 1789 to 1797 and was unanimously elected by the Electoral College. Washington is often called the Father of His Country 
due to his leadership during the American Revolutionary War and his role in the formation of the new nation. His presidency set many precedents, including the tradition of a peaceful transition 
of power and the two-term limit, which later became law with the 22nd Amendment. Washington's leadership helped consolidate the new government and establish a sense of national unity.

Traceback (most recent call last):
~~
agents.exceptions.InputGuardrailTripwireTriggered: Guardrail InputGuardrail triggered tripwire
"""