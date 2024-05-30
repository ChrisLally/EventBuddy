from pyrogram import Client, filters, enums

from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    KeyboardButton,
    MenuButton,
    MenuButtonWebApp,
    MenuButtonCommands,
    WebAppInfo,
    Poll,
    BotCommand,
    BotCommandScopeChat,
    InputMediaPhoto
)

from pyrogram.helpers import array_chunk


app = Client("my_bot")

from handlers._start import _start
from handlers._about import _about
from handlers._reset import _reset
from handlers._create_wallet import _create_wallet

from respond import respond

@app.on_message(filters.command("start") & filters.private)
async def start_handler(app, message):
    await _start(app, message)

@app.on_message(filters.command("about") & filters.private)
async def about_handler(app, message):
    await _about(app, message)

@app.on_message(filters.command("reset") & filters.private)
async def reset_handler(app, message):
    await _reset(app, message)

    

# Global variables to store quiz data
quiz_data = {}  # Store user answers
current_question = {}  # Track current question for each user


async def send_question(chat_id, question_num, question_text, options):
    # Create a list of InlineKeyboardButtons first 
    buttons = [InlineKeyboardButton(opt, callback_data=f"q{question_num}_{opt}") for opt in options]

    # Then create a 2x2 grid using array_chunk
    button_rows = array_chunk(buttons, 2)  
    keyboard = InlineKeyboardMarkup(button_rows)

    await app.send_message(chat_id, f"Question {question_num}:\n{question_text}", reply_markup=keyboard)
    current_question[chat_id] = question_num


async def start_quiz(chat_id):
    quiz_data[chat_id] = []  # Initialize answer list for the user
    await send_question(
        chat_id,
        1,
        "Select blockchain:",
        ["Sui", "Stellar"]
    )


@app.on_message(filters.command("create_wallet") & filters.private)
async def quiz(client, message):
    await start_quiz(message.chat.id)


@app.on_callback_query(filters.regex(r"^q(\d+)_(.+)"))
#@app.on_message(filters.command("create_wallet") & filters.private)
async def handle_answer(client, callback_query):
    chat_id = callback_query.from_user.id
    if chat_id not in current_question:
        return

    question_num = int(callback_query.matches[0].group(1))
    answer = callback_query.matches[0].group(2)

    #quiz_data[chat_id].append(answer)

    # Delete the original question message
    await app.delete_messages(chat_id, callback_query.message.id)

    # Send the answer confirmation message
    await app.send_message(chat_id, f"Question {question_num}:\nAnswer {question_num}: {answer}")
    #print("GOT ANSWER",answer)
    # if question_num == 1:
    #     await send_question(
    #         chat_id,
    #         2,
    #         "What is the largest mammal on Earth?",
    #         ["Elephant", "Blue Whale", "Giraffe", "Hippopotamus"]
    #     )
    # elif question_num == 2:
    #     await send_question(
    #         chat_id,
    #         3,
    #         "What is the chemical symbol for gold?",
    #         ["Ag", "Au", "Fe", "Hg"]
    #     )
    # elif question_num == 3:
    #     # Score the quiz
    #     correct_answers = ["Paris", "Blue Whale", "Au"]
    #     score = sum(1 for user_answer, correct in zip(quiz_data[chat_id], correct_answers) if user_answer == correct)
    
    await app.send_message(
        chat_id,
        f"You selected {answer}"
    )
    # del quiz_data[chat_id]
    # del current_question[chat_id]
    
    # Answer the callback query to remove the loading animation
    await callback_query.answer()
    
    await _create_wallet(app, chat_id, answer)

@app.on_message(filters.text & filters.private)
async def respond_handler(app,message):
    await respond(message)

app.run()