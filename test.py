import openai

result = openai.Completion.create(
	model="gpt-3.5-turbo-instruct",
	prompt="Who is the president of US?",
	max_tokens=256,
	temperature=0,
)

print(result.choices[0].text)