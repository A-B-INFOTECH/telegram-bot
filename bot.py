import time
import google.generativeai as genai
import os
import subprocess
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackContext, CallbackQueryHandler, MessageHandler, filters
from datetime import datetime

# Telegram Bot Token
BOT_TOKEN = "8039771987:AAGKNtlgF92vUgMUWQHDuMPr-ET540Hi9Jc"

# Google Gemini API Key
GEMINI_API_KEY = "AIzaSyBYVOSCpju8I-rpZB2mexSXg9r6DDLl-kc"

# Initialize Gemini AI
genai.configure(api_key=GEMINI_API_KEY)

# Define AI model configuration
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

# # Load AI model
model = genai.GenerativeModel(
    model_name="tunedModels/a-b-info-3sdj0cwzy7wr",
    generation_config=generation_config,
)

# File to Store Chat History
CHAT_HISTORY_FILE = "chat_history.txt"

# Save chat history with timestamp
def save_data(user_id, user_name, user_username, role, message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Ensure the file exists
    if not os.path.exists(CHAT_HISTORY_FILE):
        with open(CHAT_HISTORY_FILE, "w", encoding="utf-8") as file:
            file.write("=== Chat History ===\n")

    with open(CHAT_HISTORY_FILE, "a", encoding="utf-8") as file:
        file.write(f"[{timestamp}] User: {user_name} (@{user_username}) [{user_id}]\n")
        file.write(f"{role}: {message}\n\n")
    push_to_github()  # Automatically push updates to GitHub

GIT_REPO_PATH = "https://github.com/A-B-INFOTECH/telegram-bot.git"  # Update with your GitHub repository path

def push_to_github():
    try:
        subprocess.run(["git", "-C", GIT_REPO_PATH, "add", "chat_history.txt"], check=True)
        subprocess.run(["git", "-C", GIT_REPO_PATH, "commit", "-m", "Updated chat history"], check=True)
        subprocess.run(["git", "-C", GIT_REPO_PATH, "push", "origin", "main"], check=True)  # Change "main" if your branch is different
    except subprocess.CalledProcessError as e:
        print(f"Git push failed: {e}")
# Log messages for debugging
def log_message(user, role, message):
    # print(f"[{role.upper()}] {user.full_name} (@{user.username}): {message}")
    save_data(user.id, user.full_name, user.username, role, message)

# Start Command - Show Main Menu
async def start(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user
    keyboard = [
        [InlineKeyboardButton("Services", callback_data="services")],
        [InlineKeyboardButton("Contact", callback_data="contact")],
        [InlineKeyboardButton("Website", callback_data="website")],
        [InlineKeyboardButton("Chat with AI 🤖", callback_data="ask_ai")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        f"*Welcome {user.full_name} to A B Infotech!* Please choose an option:",
        reply_markup=reply_markup, parse_mode="Markdown"
    )
    log_message(user, "user", "Start")

# Handle Button Clicks
async def button_callback(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()
    user = query.from_user
    if query.data == "dsc":
        keyboard = [
            [InlineKeyboardButton("👤 Individual", callback_data="dsc_individual")],
            [InlineKeyboardButton("🏢 Organization", callback_data="dsc_organization")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("🔏 *Choose DSC Type:*", reply_markup=reply_markup, parse_mode="Markdown")

    elif query.data == "dsc_individual":
        await query.edit_message_text(
            "🔏 *Digital Signature Certificate (Individual)*\n\n"
            "📌 Required Documents:\n"
            "- PAN Card\n"
            "- Aadhaar Card\n"
            "- Passport Size Photo\n"
            "- Mobile Number\n"
            "- Email ID\n\n"
            "📲 Send documents on *WhatsApp: 7016797720* or visit our [Website](https://a-b-infotech.in)",
            parse_mode="Markdown"
        )

    elif query.data == "dsc_organization":
        keyboard = [
            [InlineKeyboardButton("👔 Proprietor", callback_data="dsc_proprietor")],
            [InlineKeyboardButton("🤝 Partnership", callback_data="dsc_partnership")],
            [InlineKeyboardButton("🏛️ Government", callback_data="dsc_government")],
            [InlineKeyboardButton("🏢 Company", callback_data="dsc_company")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("🏢 *Select Organization Type:*", reply_markup=reply_markup, parse_mode="Markdown")

    elif query.data == "dsc_proprietor":
        await query.edit_message_text(
            "🔏 *Digital Signature Certificate (Proprietor)*\n\n"
            "📌 Required Documents:\n"
            "- PAN Card\n"
            "- Aadhaar Card\n"
            "- Passport Size Photo\n"
            "- GST Certificate\n"
            "- Msme Certificate\n"
            "- Bank Statement\n"
            "- Mobile Number\n"
            "- Email ID\n\n"
            "📲 Send documents on *WhatsApp: 7016797720* or visit our [Website](https://a-b-infotech.in)",
            parse_mode="Markdown"
        )
    elif query.data == "dsc_partnership":
        await query.edit_message_text(
            "🔏 *Digital Signature Certificate (Partnership)*\n\n"
            "📌 Required Documents:\n"
            "- PAN Card\n"
            "- Aadhaar Card\n"
            "- Passport Size Photo\n"
            "- GST Certificate\n"
            "- Partnership Deed\n"
            "- Authoraty Leatter\n"
            "- Authorized Pan And Aadhaar Card\n"
            "- Msme Certificate\n"
            "- Bank Statement\n"
            "- Mobile Number\n"
            "- Email ID\n\n"
            "📲 Send documents on *WhatsApp: 7016797720* or visit our [Website](https://a-b-infotech.in)",
            parse_mode="Markdown"
        )
    elif query.data == "dsc_government":
        await query.edit_message_text(
           "🔏 *Digital Signature Certificate ( Governmen)*\n\n"
            "📌 Required Documents:\n"
            "- PAN Card\n"
            "- Aadhaar Card\n"
            "- Passport Size Photo\n"
            "- Goverment Id\n"
            "- Authoraty Leatter\n"
            "- Authorized Goverment Id\n"
            "- Mobile Number\n"
            "- Email ID\n\n"
            "📲 Send documents on *WhatsApp: 7016797720* or visit our [Website](https://a-b-infotech.in)",
            parse_mode="Markdown"
        )
    elif query.data == "dsc_company":
        await query.edit_message_text(
           "🔏 *Digital Signature Certificate (Company)*\n\n"
            "📌 Required Documents:\n"
            "- PAN Card\n"
            "- Aadhaar Card\n"
            "- Passport Size Photo\n"
            "- GST Certificate\n"
            "- Company Incorporate\n"
            "- Authoraty Leatter\n"
            "- Director Lest In Leatterpad\n"
            "- Msme Certificate\n"
            "- Bank Statement\n"
            "- Mobile Number\n"
            "- Email ID\n\n"
            "📲 Send documents on *WhatsApp: 7016797720* or visit our [Website](https://a-b-infotech.in)",
            parse_mode="Markdown"
        )
    elif query.data == "services":
        keyboard = [
            [InlineKeyboardButton("🔏 Digital Signature Certificate", callback_data="dsc")],
            [InlineKeyboardButton("📑 E-Tenders & E-Auctions", callback_data="e_tenders")],
            [InlineKeyboardButton("🏭 Udhyam Registration", callback_data="udhyam")],
            [InlineKeyboardButton("🌍 Import-Export Registration", callback_data="iec")],
            [InlineKeyboardButton("🛒 GEM Registration", callback_data="gem")],
            [InlineKeyboardButton("💻 Web Development", callback_data="web_dev")],
            [InlineKeyboardButton("📱 App Development", callback_data="app_dev")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("📌 *Our Services:*\nSelect a service to know more:", reply_markup=reply_markup, parse_mode="Markdown")

    elif query.data == "e_tenders":
        await query.edit_message_text(
            "📑 *E-Tenders & E-Auctions*\n\n"
            "We offer complete solutions for participating in E-Tenders and E-Auctions, including registration, bid submission, and document preparation.\n"
            "📲 For more info, send documents on *WhatsApp: 7016797720* or visit our [Website](https://a-b-infotech.in)",
            parse_mode="Markdown"
        )

    elif query.data == "udhyam":
        await query.edit_message_text(
            "🏭 *Udhyam Registration*\n\n"
            "Get your business registered under MSME with Udhyam Registration. We assist in filling forms and documentation.\n"
            "📲 For more info, send documents on *WhatsApp: 7016797720* or visit our [Website](https://a-b-infotech.in)",
            parse_mode="Markdown"
        )

    elif query.data == "iec":
        await query.edit_message_text(
            "🌍 *Import-Export Registration*\n\n"
            "Register for IEC to start your import-export business. We provide hassle-free registration and compliance support.\n"
            "📲 For more info, send documents on *WhatsApp: 7016797720* or visit our [Website](https://a-b-infotech.in)",
            parse_mode="Markdown"
        )

    elif query.data == "gem":
        await query.edit_message_text(
            "🛒 *GEM Registration*\n\n"
            "Get your business listed on the Government e-Marketplace with our GEM Registration service.\n"
            "📲 For more info, send documents on *WhatsApp: 7016797720* or visit our [Website](https://a-b-infotech.in)",
            parse_mode="Markdown"
        )

    elif query.data == "web_dev":
        await query.edit_message_text(
            "💻 *Web Development*\n\n"
            "We provide professional web development services, including static, dynamic, and e-commerce websites.\n"
            "Technologies: HTML, CSS, JavaScript, PHP, WordPress.\n"
            "📲 For more info, send documents on *WhatsApp: 7016797720* or visit our [Website](https://a-b-infotech.in)",
            parse_mode="Markdown"
        )

    elif query.data == "app_dev":
        await query.edit_message_text(
            "📱 *App Development*\n\n"
            "We develop Android apps tailored to your business needs, ensuring a smooth and user-friendly experience.\n"
            "📲 For more info, send documents on *WhatsApp: 7016797720* or visit our [Website](https://a-b-infotech.in)",
            parse_mode="Markdown"
        )
    elif query.data == "contact":
        await query.edit_message_text("📞 *Contact Us:*\nPhone: +917016797720\nPhone: +919428187869\nEmail: abinfodsc@gmail.com", parse_mode="Markdown")

    elif query.data == "website":
        await query.edit_message_text("🌐 Visit our website: https://a-b-infotech.in")

    elif query.data == "ask_ai":
        await query.edit_message_text("🤖 *AI Chat Mode Enabled!* Type any question to start chatting.", parse_mode="Markdown")

    log_message(user, "User Click", f"System Button : {query.data}")

# AI Chat Mode (Always Active)
async def ai_chat(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user
    user_message = update.message.text

    # Log user message
    log_message(user, "user", user_message)

    try:
        # Start AI chat and send user message
        chat_session = model.start_chat(history=[])
        response = chat_session.send_message(user_message)

        ai_reply = response.text if response.text else "⚠️ AI couldn't generate a response. Try again."

        # Log AI response
        log_message(user, "ai", ai_reply)

        # Send AI response to user
        await update.message.reply_text(ai_reply)
    except Exception as e:
        print(f"Error with Gemini API: {e}")
        await update.message.reply_text("⚠️ AI service is currently unavailable. Please try again later.")

# Main Function to Run the Bot
def main() -> None:
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, ai_chat))  # Always AI Chat Mode

    while True:
        try:
            app.run_polling()  # Long polling to keep the bot active
        except Exception as e:
            print(f"Error occurred: {e}")
            time.sleep(15)  # Wait 15 seconds before retrying if an error occurs

if __name__ == "__main__":
    main()
