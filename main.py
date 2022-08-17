from telegram.ext import Updater, CommandHandler, Filters, MessageHandler, ConversationHandler
import os
from random import randint, choice
from bottt import TOKEN

token = os.getenv(TOKEN)
updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher


candy_count = 300
max_candy_takes = 28
PLAYER, MOVE = range(2)
player_1 = ''
player_2 = 'Winnie the Pooh'
current_player = None

print('Bot works...')


def start(update, context):
    global candy_count
    candy_count = 300  #update initial quantity
    arg = context.args
    if not arg:
        context.bot.send_message(update.effective_chat.id,
                                 f"Hello! My name {player_2}. Let's play a game!\n"
                                 f"I have {candy_count} candies,"
                                 f" in one move you need to take from 1 to {max_candy_takes} candies.\n"
                                 f"Whoever takes the last candies-wins")
    context.bot.send_message(update.effective_chat.id, 'What is your name?')
    return PLAYER


def player_name(update, context):
    """
    game begin, add the name of player
    """
    global player_1, player_2, current_player
    player_1 = update.message.text
    current_player = choice([player_1, player_2])  
    context.bot.send_message(update.effective_chat.id, f'First move {current_player}')
    if current_player == player_2:
        bot_move(update, context)  # passing the move to the bot
    else:
        context.bot.send_message(update.effective_chat.id, 'How many candies will you take?')  
    return MOVE


def take_move(update, context):  # player turn
    global candy_count, current_player
    try:  # checking the number of candies
        take_candies = int(update.message.text)
        if 1 <= take_candies <= max_candy_takes:
            candy_count -= take_candies
        else:
            context.bot.send_message(update.effective_chat.id,
                                     f'You can take from 1 to {max_candy_takes} candies at a time')
            return MOVE
    except:
        context.bot.send_message(update.effective_chat.id, f'Input number from 1 to 28')
        return MOVE
    context.bot.send_message(update.effective_chat.id, f'{candy_count} candies left on the table...')
    if candy_count <= max_candy_takes:  # checking bot win
        context.bot.send_message(update.effective_chat.id,
                                 f'{player_2} took the last {candy_count} candies and WIN!')
        return ConversationHandler.END
    bot_move(update, context)  # pass move to bot


def bot_move(update, context):  # bot move
    global candy_count, current_player
    take_candies = randint(1, max_candy_takes)
    candy_count -= take_candies
    context.bot.send_message(update.effective_chat.id, f'{player_2} take {take_candies} candies')
    if candy_count <= max_candy_takes:  # checking win
        context.bot.send_message(update.effective_chat.id,
                                 f'{player_1} took the last {candy_count} candies and WIN!')
        return ConversationHandler.END
    else:  # pass move to player
        context.bot.send_message(update.effective_chat.id, f'{candy_count} candies left on the table...')
        context.bot.send_message(update.effective_chat.id, 'How many candies will you take?')
        return MOVE


def stop(update, context):  # finish
    context.bot.send_message(update.effective_chat.id, 'The game is over!')
    return ConversationHandler.END


def unknown_command(update, context):  # обработчик неизвестных команд и/или сообщений
    context.bot.send_message(update.effective_chat.id, f'I can play only with candies...')
    context.bot.send_message(update.effective_chat.id, f'Do you want to play again? Press /start')


conv_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={
        PLAYER: [MessageHandler(Filters.text, player_name)],
        MOVE: [MessageHandler(Filters.text, take_move)]},
    fallbacks=[CommandHandler('stop', stop)])
message_handler = MessageHandler(Filters.text, unknown_command)
unknown_handler = MessageHandler(Filters.command, unknown_command)

dispatcher.add_handler(conv_handler)
dispatcher.add_handler(message_handler)
dispatcher.add_handler(unknown_handler)

updater.start_polling()
updater.idle()
