import requests
from solana.rpc.api import Client
from solders.keypair import Keypair
from solders.pubkey import Pubkey
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters
import json

# Telegram bot details
bot_token = 'xxx'
chat_id = 'xxx'

# Solana Client and Wallet details
solana_client = Client("https://api.mainnet-beta.solana.com")
wallet_address = Pubkey.from_string("xxx")

# Read the private key from the file
with open('C:\\Users\\insid\\xxx.txt', 'r') as key_file:
    key_data = json.load(key_file)
    private_key_list = [int(x) for x in key_data['secret_key'].split(',')]
    private_key_bytes = bytes(private_key_list)
    keypair = Keypair.from_bytes(private_key_bytes)

# Default Sol Fee and Purchase amount
sol_fee = 0.001
sol_to_buy = 0.001
token_to_buy = None

# Function to check balance
async def check_balance(update: Update, context):
    balance_response = solana_client.get_balance(wallet_address)
    sol_balance = balance_response.value / 1e9  # Convert lamports to SOL
    await context.bot.send_message(chat_id=chat_id, text=f"Your current SOL balance is: {sol_balance:.4f} SOL")
    await display_menu(update, context)

# Function to set Sol quantity for purchase
async def set_sol_qty(update: Update, context):
    await context.bot.send_message(chat_id=chat_id, text=f"Current SOL to buy is: {sol_to_buy} SOL. Please send a new SOL quantity to use for buying.")
    context.user_data['expecting_sol_qty'] = True

# Function to set Sol fee
async def set_sol_fee(update: Update, context):
    await context.bot.send_message(chat_id=chat_id, text=f"Current Sol Fee is: {sol_fee} SOL. Please send a new fee value.")
    context.user_data['expecting_sol_fee'] = True

# Function to confirm and buy token
async def buy_token(update: Update, context):
    if token_to_buy and sol_to_buy:
        keyboard = [
            [InlineKeyboardButton("Yes", callback_data='confirm_buy'), InlineKeyboardButton("No", callback_data='cancel_buy')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await context.bot.send_message(chat_id=chat_id, text=f"Confirm buying {sol_to_buy} SOL of token {token_to_buy}?", reply_markup=reply_markup)
    else:
        await context.bot.send_message(chat_id=chat_id, text="Please set both token address and SOL quantity first.")

# Function to handle buy confirmation
async def confirm_buy(update: Update, context):
    global token_to_buy  # Declare it as global here
    if token_to_buy and sol_to_buy:
        # Here, you'd implement the logic to execute the purchase using sol_to_buy and token_to_buy.
        await context.bot.send_message(chat_id=chat_id, text=f"Executing purchase of {sol_to_buy} SOL for token {token_to_buy} with a fee of {sol_fee} SOL.")
        # Reset token_to_buy for future purchases
        token_to_buy = None
    await display_menu(update, context)

# Function to handle user input for token to buy
async def handle_input(update: Update, context):
    global sol_to_buy, sol_fee, token_to_buy  # Declare as global here

    # Check if expecting SOL quantity
    if 'expecting_sol_qty' in context.user_data and context.user_data['expecting_sol_qty']:
        try:
            sol_to_buy = float(update.message.text)
            await context.bot.send_message(chat_id=chat_id, text=f"Sol quantity set to {sol_to_buy} SOL.")
        except ValueError:
            await context.bot.send_message(chat_id=chat_id, text="Invalid SOL Quantity. Please enter a valid number.")
        context.user_data['expecting_sol_qty'] = False
        await display_menu(update, context)

    # Check if expecting SOL fee
    elif 'expecting_sol_fee' in context.user_data and context.user_data['expecting_sol_fee']:
        try:
            sol_fee = float(update.message.text)
            await context.bot.send_message(chat_id=chat_id, text=f"Sol fee set to {sol_fee} SOL.")
        except ValueError:
            await context.bot.send_message(chat_id=chat_id, text="Invalid SOL Fee. Please enter a valid number.")
        context.user_data['expecting_sol_fee'] = False
        await display_menu(update, context)

    # Check if expecting token address
    elif 'expecting_token' in context.user_data and context.user_data['expecting_token']:
        token_to_buy = update.message.text
        await context.bot.send_message(chat_id=chat_id, text="Proceeding to confirm the purchase.")
        await buy_token(update, context)  # Move directly to confirmation
        context.user_data['expecting_token'] = False

# Function to handle button presses
async def button(update: Update, context):
    query = update.callback_query
    await query.answer()

    if query.data == 'balance':
        await check_balance(update, context)
    elif query.data == 'set_qty':
        await set_sol_qty(update, context)
    elif query.data == 'set_fee':
        await set_sol_fee(update, context)
    elif query.data == 'buy':
        await context.bot.send_message(chat_id=chat_id, text="Please provide the token address you want to buy.")
        context.user_data['expecting_token'] = True
    elif query.data == 'sell':
        await sell_token(update, context)
    elif query.data == 'refresh':
        await refresh_position(update, context)
    elif query.data == 'confirm_buy':
        await confirm_buy(update, context)
    elif query.data == 'cancel_buy':
        await context.bot.send_message(chat_id=chat_id, text="Purchase canceled.")
        await display_menu(update, context)

# Function to display the menu with all buttons
async def display_menu(update: Update, context):
    keyboard = [
        [InlineKeyboardButton("Balance", callback_data='balance'), InlineKeyboardButton("Sol QTY", callback_data='set_qty')],
        [InlineKeyboardButton("Sol Fee", callback_data='set_fee'), InlineKeyboardButton("Buy", callback_data='buy')],
        [InlineKeyboardButton("Sell", callback_data='sell'), InlineKeyboardButton("Refresh", callback_data='refresh')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(chat_id=chat_id, text="..", reply_markup=reply_markup)  # No message text

# Setting up the bot using Application
application = Application.builder().token(bot_token).build()

# Handlers
application.add_handler(CommandHandler('start', display_menu))
application.add_handler(CallbackQueryHandler(button))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_input))

# Start the bot
application.run_polling()
