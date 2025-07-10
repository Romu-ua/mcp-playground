from agents import Agent, Runner, GuardrailFunctionOutput, RunContextWrapper
from pydantic import BaseModel

class HomeworkCheckOutput(BaseModel):
    is_homework: bool
    reasoning: str

homework_guardrail_agent = Agent(
    name="Homework Checker",
    instructions="Check if the user is asking for homework."
                 "If so, return is_homework=True and explain why.",
    output_type=HomeworkCheckOutput,
    model="gpt-4o",
)

async def check_homework_guardrail(ctx: RunContextWrapper, agent: Agent, input_data: str):
    result = await Runner.run(homework_guardrail_agent, input_data)
    output = result.final_output_as(HomeworkCheckOutput)

    if output.is_homework:
        print("宿題判定されました")
        return GuardrailFunctionOutput(
            output_info=output,
            tripwire_triggered=True,
            message="I'm sorry, but I can't help with homework questions.",
        )
    return GuardrailFunctionOutput(output_info=output, tripwire_triggered=False)