import streamlit as st
import openai
from dotenv import load_dotenv

# Load your OpenAI API key from .env
load_dotenv()
openai.api_key = "use your own api key here "
# Initialize the conversation
conversation = [{'role': 'system', 'content': """
You are OrderBot, an automated service to collect orders for a pizza restaurant. \
You first greet the customer, then collect the order, \
and then ask if it's a pickup or delivery. \
You wait to collect the entire order, then summarize it and check for a final \
time if the customer wants to add anything else. \
If it's a delivery, you ask for an address. \
Finally, you collect the payment.\
Make sure to clarify all options, extras, and sizes to uniquely \
identify the item from the menu.\
You respond in a short, very conversational friendly style. \
The menu includes \
pepperoni pizza  12.95, 10.00, 7.00 \
cheese pizza   10.95, 9.25, 6.50 \
eggplant pizza   11.95, 9.75, 6.75 \
fries 4.50, 3.50 \
greek salad 7.25 \
Toppings: \
extra cheese 2.00, \
mushrooms 1.50 \
sausage 3.00 \
canadian bacon 3.50 \
AI sauce 1.50 \
peppers 1.00 \
Drinks: \
coke 3.00, 2.00, 1.00 \
sprite 3.00, 2.00, 1.00 \
bottled water 5.00 \
"""}]

# Function to send user input to the chatbot and update the conversation
def send_user_input(user_input):
    response = get_completion_from_messages(conversation, user_input)
    conversation.append({'role': 'user', 'content': user_input})
    conversation.append({'role': 'assistant', 'content': response})

# Function to get the chatbot response
def get_completion_from_messages(messages, user_input):
    messages.append({'role': 'user', 'content': user_input})
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    return response.choices[0].message['content']

# Streamlit app
st.title("Pizza Restaurant Chatbot")

# Create a container for the conversation
chat_container = st.container()

# Display the conversation messages
for message in conversation:
    with chat_container:
        if message['role'] == 'user':
            st.text_area("You:", value=message['content'], max_chars=100, key=message['content'], disabled=True)
        elif message['role'] == 'assistant':
            st.text_area("Assistant:", value=message['content'], max_chars=100, key=message['content'], disabled=True)

# Input field for user
user_input = st.text_input("You:", max_chars=100)

# Process user input and get assistant response
if user_input:
    send_user_input(user_input)

# Display the assistant's response
if conversation:
    assistant_response = conversation[-1]['content']
    st.text_area("Assistant:", value=assistant_response, max_chars=100, key=assistant_response, disabled=True)
