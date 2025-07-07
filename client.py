import cohere

co = cohere.Client("1zBCvuhGnrdz0OvL7kCQK0DPN156z621652ODk2O")
response = co.generate(prompt="What is coding?")
print(response.generations[0].text)
