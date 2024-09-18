
import streamlit as st
import random

# A list of random jokes
jokes = [
    "Why don't scientists trust atoms? Because they make up everything!",
    "Why did the math book look sad? Because it had too many problems.",
    "What do you call fake spaghetti? An impasta!",
    "Why was the stadium so cool? It was filled with fans!",
    "Why don't skeletons fight each other? They don't have the guts."
]

# Title of the app
st.title("Random Joke Generator")

# Display an introductory message
st.write("Click the button below to get a random joke!")

# Button to trigger joke generation
if st.button('Get a Joke'):
    # Select a random joke from the list
    joke = random.choice(jokes)
    st.success(joke)
else:
    st.write("Waiting for you to press the button...")
