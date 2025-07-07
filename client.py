import cohere

co = cohere.Client("API_KEY")
response = co.generate(prompt="What is coding?")
print(response.generations[0].text)
