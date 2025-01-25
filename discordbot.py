# discordbot.py
import discord
from discord.ext import commands, tasks
import asyncio
#import openai  # Import OpenAI for API usage


from husky import get_user_husky, user_huskies

# Bot setup
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix="~", intents=intents)

# OpenAI API Setup
#openai.api_key = "YOUR_OPENAI_API_KEY"  # Replace with your OpenAI API key

# AI Question Generation
async def generate_ai_questions(num_questions):
    questions = {}
    for i in range(1, num_questions + 1):
        # Use OpenAI to generate a multiple-choice question
        prompt = (
            "Generate a multiple-choice question on a general topic. Include four answer options and indicate the correct answer."
        )
        try:
            response = openai.Completion.create(
                engine="text-davinci-003",  # Adjust the engine as needed
                prompt=prompt,
                max_tokens=150,
                temperature=0.7,
            )
            ai_output = response.choices[0].text.strip()

            # Parse the response into question and answers
            lines = ai_output.split("\n")
            question = lines[0]
            answers = [line for line in lines[1:5]]  # Extract the four answers
            correct_index = next(
                (i for i, ans in enumerate(answers) if "(correct)" in ans), None
            )

            if correct_index is not None:
                correct_index = correct_index
                answers = [ans.replace("(correct)", "").strip() for ans in answers]
                questions[i] = {
                    "question": question,
                    "answers": answers,
                    "correct": correct_index,
                }
            else:
                # Skip the question if no correct answer is found
                continue

        except Exception as e:
            print(f"Error generating question {i}: {e}")
            continue

    return questions

# Command to run an AI-powered quiz
@bot.command()
async def ai_quiz(ctx, num_questions: int):
    if num_questions <= 0 or num_questions > 50:
        await ctx.send("Please choose a number between 1 and 50.")
        return

    await ctx.send(f"Generating {num_questions} questions using AI. Please wait...")

    try:
        ai_questions = await generate_ai_questions(num_questions)
        if not ai_questions:
            await ctx.send("Failed to generate questions. Please try again later.")
            return

        question_ids = list(ai_questions.keys())

        score = 0
        for question_id in question_ids:
            q_data = ai_questions[question_id]
            question_text = f"**Question {question_id}:** {q_data['question']}\n"
            for i, answer in enumerate(q_data["answers"]):
                question_text += f"{i + 1}. {answer}\n"
            await ctx.send(question_text)

            def check_answer(msg):
                return msg.author == ctx.author and msg.channel == ctx.channel and msg.content.isdigit()

            try:
                answer_msg = await bot.wait_for("message", check=check_answer, timeout=60)
                user_answer = int(answer_msg.content) - 1

                if user_answer == q_data["correct"]:
                    score += 1
                    await ctx.send("Correct!")
                else:
                    await ctx.send(f"Wrong! The correct answer was: {q_data['answers'][q_data['correct']]}")
            except Exception:
                await ctx.send("You took too long to answer. Moving to the next question.")

        await ctx.send(f"AI Quiz finished! You scored {score}/{num_questions}.")
    except Exception as e:
        await ctx.send(f"An error occurred while generating the quiz: {e}")

# Pomodoro Timer Command
@bot.command()
async def ptimer(ctx, work_time: int = 25, break_time: int = 5):
    """
    Starts a Pomodoro timer with a default 25-minute work session and a 5-minute break.
    """
    try:
        await ctx.send(f"Pomodoro timer started! Working for {work_time} minutes.")

        # Work timer
        await asyncio.sleep(work_time * 60)
        await ctx.send(f"Time's up! Take a {break_time}-minute break.")

        # Break timer
        await asyncio.sleep(break_time * 60)
        await ctx.send("Break's over! Time to get back to work!")
    except Exception as e:
        await ctx.send("An error occurred with the Pomodoro timer.")
        print(f"Error: {e}")

# Daily reset and stat decay
@tasks.loop(hours=24)
async def daily_reset():
    for user_id, husky in user_huskies.items():
        husky.decay()
        husky.reset_daily_study()
    print("Daily stats updated for all users (decay applied if goal not met).")

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

    daily_reset.start()  # Start the daily reset loop

# Run the bot
bot.run('...')

