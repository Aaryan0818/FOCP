import random
import json
import datetime

# Function to load responses from the JSON file
def load_responses():
    try:
        with open("responses.json", "r") as file:
            data = json.load(file)
            return data["responses"]
    except FileNotFoundError:
        print("Error: responses.json file not found.")
        exit()

# Define a list of possible agent names
agent_names = ["Alex", "Siri", "Jennifer", "Sam", "Simon", "David", "Robert", "Peter"]

# Randomly choose an agent name
agent_name = random.choice(agent_names)

# Get the responses from the JSON file
responses = load_responses()

# Path for log file
log_file_path = "chat_log.txt"

# Function to log the conversation
def log_conversation(user_input, agent_response):
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_file_path, "a") as log_file:
        log_file.write(f"[{current_time}] User: {user_input}\n[{current_time}] {agent_response}\n\n")

# Function to get random agent responses if no keyword match is found
def get_random_response():
    responses = [
        "Can you please clarify your question?",
        "I'm not sure about that. Let me check!",
        "That's an interesting question, let me think...",
        "Sorry, I don't know the answer to that.",
        "Hmm, I haven't come across that yet!"
    ]
    return random.choice(responses)

# Simulate random disconnection
def should_disconnect():
    return random.random() < 0.1  # 10% chance of disconnecting

# Chat function
def start_chat():
    print("Hello! Welcome to the University of Poppleton Chatbot.")
    user_name = input("Please enter your name: ")
    print(f"Hello {user_name}! I'm {agent_name}, your virtual assistant. Ask me anything!")
    
    # Log the start of the session
    log_conversation({user_name},f"{agent_name}: Hello {user_name}! I'm {agent_name}, your virtual assistant.")
    
    interactions = 0
    while True:
        user_question = input(f"{user_name}: ")

        # Exit condition
        if user_question.lower() in ["bye", "exit", "quit"]:
            farewell_message = f"Goodbye, {user_name}! Have a great day!"
            print(f"{agent_name}: {farewell_message}")
            log_conversation(user_question, f"{agent_name}: {farewell_message}")
            break
        
        # Simulate a random disconnection
        if should_disconnect():
            disconnect_message = "Oh no, I'm experiencing some technical difficulties. Goodbye!"
            print(f"{agent_name}: {disconnect_message}")
            log_conversation(user_question, f"{agent_name}: {disconnect_message}")
            break

        # Check if any keyword exists in the question
        response = get_random_response()  # Default response if no keyword is found
        for keyword, answer in responses.items():
            if keyword.lower() in user_question.lower():
                response = answer
                break

        # Log the interaction
        log_conversation(user_question, response)
        
        # Display the response
        print(f"{agent_name}: {response}")

        # Random disconnection chance after 5 interactions
        interactions += 1
        if interactions > 5 and random.random() < 0.1:  # 10% chance after 5 interactions
            reboot_message = "Oops! I think I need to reboot. Catch you later!"
            print(f"{agent_name}: {reboot_message}")
            log_conversation(user_question, f"{agent_name}: {reboot_message}")
            break

# Start the chat
start_chat()
