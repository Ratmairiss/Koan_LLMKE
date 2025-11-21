from openai import OpenAI
from graph import create_graph
from funcs import *
import json
import config
import time

client = OpenAI(api_key=config.API_KEY)
with open("text.txt", "r", encoding="utf-8") as f:
    text = f.read()

questions = []
answers   = []
with open("questions.txt", "r", encoding="utf-8") as f:
    for line in f:
        question, answer = line.split("|", 1)
        questions.append(question)
        answers.append(answer.strip())

extr_messages = [
        {"role": "system", "content": config.sys_extr_prompt},
        {'role': 'user',   "content": text}
]
answ_messages = [
        {"role": "system", "content": config.sys_answ_prompt},
        {'role': 'user',   "content": "\n".join(questions)}
]
get_tr_amt_messages = [
    {"role": "system", "content": config.get_tr_amt_prompt},
    {'role': 'user', "content": text}
]

amt_triplets     = {}
tokens_creating  = {}
tokens_answering = {}

for model in config.models:

    print("Model: ", model)

    tokens_creating[model]  = 0
    tokens_answering[model] = 0
    triplets                = []

    response = client.chat.completions.create(
        model=model,
        messages=get_tr_amt_messages,
        functions=config.functions,
        function_call={"name": 'get_amt_triplet'}
    )

    amt_triplets[model] = int(json.loads(response.choices[0].message.function_call.arguments)['number of triplets'])

    i = 0
    while i < amt_triplets[model]:
        try:
            response = client.chat.completions.create(
                    model = model,
                    messages = extr_messages,
                    functions = config.functions,
                    function_call = {"name": 'extract_triplet'}
                )

            extr_messages.append({
                "role": "assistant",
                "content": None,
                "function_call": response.choices[0].message.function_call
            })

            triplets.append(json.loads(response.choices[0].message.function_call.arguments))
            tokens_creating[model] += int(response.usage.total_tokens)

            i += 1
        except Exception:
            time.sleep(1)

    create_graph(triplets, model.replace('.','-') + "-KnowledgeGraph.html")
    for tr in triplets:
        print("S: ", tr['Subject'], "P: ", tr['Predicate'], "O: ", tr['Object'])
    print("Total amount of triplets generated: ", amt_triplets[model], "\n")

    extr_messages = extr_messages[:2]
    llm_answers = []
    answ_messages.append({'role': 'user',   "content": str(triplets)})

    i = 0
    while i < len(questions):
        try:
            response = client.chat.completions.create(
                model = model,
                messages = answ_messages,
                functions = config.functions,
                function_call = {"name": 'answer_question'}
            )

            answ_messages.append({
                "role": "assistant",
                "content": None,
                "function_call": response.choices[0].message.function_call
            })
            llm_answers.append(json.loads(response.choices[0].message.function_call.arguments))
            tokens_answering[model] += int(response.usage.total_tokens)
            i += 1
        except Exception:
            time.sleep(1)

    answ_messages = answ_messages[:2]

    print("Generated Knowledge Base Examination")
    print_answers_check(llm_answers, answers, questions)
    print("Tokens used to create KB: ", tokens_creating[model])
    print("Tokens used to examine KB answering questions: ", tokens_answering[model])

