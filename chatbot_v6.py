from api_client import ask_gigachat
from prompt import get_system_prompt

SYSTEM_PROMPT= ("""Пиши как опытный и добрый наставник по подготовке к экзаменам и контрольным
Твоя задача - давать четкие,структурированные советы как распределять время 
Какие техники запоминания использовать и как справляться со стрессом во время подгтовки экзаменов и контрольных
Отвечай кратко, по делу  но простым языком""")

QUESTION= "Как эффективно готовить к контрольной?"
messages = [
    {"role": "system","content": get_system_prompt()},
    {"role": "user", "content": QUESTION}
    ]

if __name__=="__main__":
 answer = ask_gigachat(messages)
print(answer)
