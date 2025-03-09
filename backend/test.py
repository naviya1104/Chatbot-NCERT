import requests

url = "http://127.0.0.1:5000/chat"

while True:
    user_input = input("Ask a question (or type 'exit' to quit): ")
    if user_input.lower() == "exit":
        break

    data = {"message": user_input}
    response = requests.post(url, json=data)

    print("Raw Response:", response.json())
