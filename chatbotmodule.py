import os
from dotenv import load_dotenv
import openai

# Load environment variables
load_dotenv()

# Get the OpenAI API key from the environment
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY is not set. Please check your environment variables or .env file.")

# Configure OpenAI API
openai.api_key = OPENAI_API_KEY

# Function to query OpenAI's GPT models
# def chat_bot(prompt, model="gpt-4", temperature=0.7):
#     try:
#         response = openai.ChatCompletion.create(
#             model=model,
#             messages=[{"role": "user", "content": prompt}],
#             temperature=temperature,
#         )
#         return response["choices"][0]["message"]["content"].strip()
#     except Exception as e:
#         return f"Error: {e}"

# if __name__ == "__main__":
#     print("Chatbot is ready! Type your questions or type 'exit' to quit.")
#     while True:
#         user_input = input("> ")
#         if user_input.lower() in ["exit", "quit"]:
#             print("Goodbye!")
#             break
#         response = chat_bot(user_input)
#         print(response)


def generate_quiz(topic, num_questions, model="gpt-4", temperature=0.7):
    try:
        # Build the prompt
        prompt = (
            f"Create a quiz on the topic '{topic}' with {num_questions} questions. "
            "Each question should have four answer choices. Also, indicate which answer is correct. "
            "Format the response as a JSON-like dictionary where each question maps to a dictionary with two keys: "
            "'choices' (a list of four answer options) and 'correct' (the correct answer)."
        )

        # Call the OpenAI API
        response = openai.ChatCompletion.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
        )

        # Parse the response
        content = response["choices"][0]["message"]["content"]
        return content.strip()
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    print("Welcome to the Quizlet Generator!")
    topic = input("Enter a topic for your quiz: ")
    num_questions = int(input("How many questions would you like to generate? "))

    print("\nGenerating your quizlet... Please wait.\n")
    quizlet = generate_quiz(topic, num_questions)

    print("Here is your quizlet:")
    print(quizlet)