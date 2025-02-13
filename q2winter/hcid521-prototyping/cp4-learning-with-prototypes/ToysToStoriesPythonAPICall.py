import openai
response = openai.ChatCompletion.create(
    model=“gpt-4”,
    messages=[
        {“role”: “system”, “content”: “You are a storyteller that creates short, engaging children’s stories based on toy descriptions.“},
        {“role”: “user”, “content”: “Create a story using a stuffed dog, a rubber duck, and a unicorn plush.“}
    ]
)
print(response[“choices”][0][“message”][“content”])