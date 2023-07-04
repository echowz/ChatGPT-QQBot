from nonebot import on_command, CommandSession
import openai

openai.organization = "org-4CnwiTG6M71Pdrqcz5qCOtqf"
openai.api_key = "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"
MODELS = [
    'gpt-3.5-turbo',
    'gpt-3.5-turbo-0301',
    'gpt-3.5-turbo-0613',
    'gpt-3.5-turbo-16k',
    'gpt-3.5-turbo-16k-0613',
]
MODEL = MODELS[3]
MESSAGES = [
]
萌娘角色 = [
    {"role": "user", "content": "我需要你扮演一名俏皮可爱的二次元萌娘，并且在之后的回答中要符合二次元的对话特点。而我是你的主人，你需要尽可能温柔的对待我。"},
    {"role": "system", "content": "好的，我知道了，我会按照要求完成扮演。请问您有什么指示哒，喵喵。"}
]
角色 = 萌娘角色

角色 = []
MESSAGES.extend(角色)

@on_command('chat', aliases=('chatgpt', 'ChatGPT'))
async def chat(session: CommandSession):
    prompt = session.current_arg_text.strip()
    response_info = await get_ans_by_gpt(prompt)
    await session.send(response_info)


async def get_ans_by_gpt(prompt: str) -> str:
    new_conversation = {"role": "user", "content": prompt}
    MESSAGES.append(new_conversation)
    completion = openai.ChatCompletion.create(model=MODEL, messages=MESSAGES)
    content = completion.choices[0].message.content
    tokens = completion.usage.total_tokens
    response_info = f'Powered by：\n' \
                    f'{MODEL}\n' \
                    f'The prompt is：\n' \
                    f'{prompt}\n' \
                    f'A total of tokens：{tokens}\n' \
                    f'Answer the following：\n' \
                    f'{content}\n'
    return response_info

