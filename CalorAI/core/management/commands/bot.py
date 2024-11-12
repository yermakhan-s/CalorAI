# from os import path
# from asgiref.sync import sync_to_async
# from django.conf import settings
# from django.core.management.base import BaseCommand, CommandError
# import logging
# from django.db.models import Sum

# from telegram import Update
# from telegram.ext import ApplicationBuilder, CommandHandler, CallbackContext, ContextTypes, filters, MessageHandler
# from core.models import MyUser, Calorie
# from datetime import date
# from openai_api.api_request import get_nutritional_info
# from django.conf import settings


# class Command(BaseCommand):
#     help = "Starts the Telegram bot"

#     def handle(self, *args, **options):
#         main()

# @sync_to_async
# def get_user(user_id):
#     return MyUser.objects.get(user_id=user_id)

# @sync_to_async
# def update_or_create_user(user_id, first_name, last_name, username):
#     user, created = MyUser.objects.update_or_create(
#         user_id=user_id,
#         defaults={
#             'first_name': first_name,
#             'last_name': last_name,
#             'username': username,
#         }
#     )
#     return user

# async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     user_id = update.effective_user.id
#     user = await update_or_create_user(
#         user_id=user_id,
#         first_name=update.effective_user.first_name,
#         last_name=update.effective_user.last_name,
#         username=update.effective_user.username
#     )
#     await update.message.reply_text(f'Hello {user.first_name}!')


# async def get_daily_cpfc(user):
#     today = date.today()
#     result = await sync_to_async(Calorie.objects.filter(user=user, created_date__date=today).aggregate)(
#         total_calories=Sum('calories'),
#         total_proteins=Sum('proteins'),
#         total_fats=Sum('fats'),
#         total_carbohydrates=Sum('carbohydrates'))
#     return {
#         'calories': result['total_calories'] or 0,
#         'proteins': result['total_proteins'] or 0,
#         'fats': result['total_fats'] or 0,
#         'carbohydrates': result['total_carbohydrates'] or 0,
#     }

# async def daily_summary(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     user_id = update.effective_user.id
#     user = await get_user(user_id)
#     cpfc = await get_daily_cpfc(user)  # Fixed variable name to 'cpfc'
#     message = (f"Your total intake today:\n"
#                f"Calories: {cpfc['calories']} kcal\n"
#                f"Proteins: {cpfc['proteins']} g\n"
#                f"Fats: {cpfc['fats']} g\n"
#                f"Carbohydrates: {cpfc['carbohydrates']} g")
#     await update.message.reply_text(message)

# async def add_cpfc_entry(user, description, cpfc):
#     await sync_to_async(Calorie.objects.create)(
#         user=user, 
#         description=description, 
#         calories=cpfc['calories'],
#         proteins=cpfc['proteins'],
#         fats=cpfc['fats'],
#         carbohydrates=cpfc['carbohydrates']
#     )

# def calculate_cpfc(description: str) -> int:
#     response = [350, 45, 456, 77]
#     response = get_nutritional_info(description)
#     f, p, cr, cl = [int(i) for i in response.split(' ')]
#     calories = cl
#     proteins = p
#     fats = f
#     carbohydrates = cr
#     return {
#         'calories': calories,
#         'proteins': proteins,
#         'fats': fats,
#         'carbohydrates': carbohydrates
#     }

# async def handle_food_description(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     user_id = update.effective_user.id
#     user = await get_user(user_id)
#     description = update.message.text

#     # Calculate CPFC based on the description
#     cpfc = calculate_cpfc(description)

#     # Save the CPFC entry to the database
#     await add_cpfc_entry(user, description, cpfc)

#     # Respond to the user
#     message = (f"Estimated nutritional values for this meal:\n"
#                f"Calories: {cpfc['calories']} kcal\n"
#                f"Proteins: {cpfc['proteins']} g\n"
#                f"Fats: {cpfc['fats']} g\n"
#                f"Carbohydrates: {cpfc['carbohydrates']} g")
#     await update.message.reply_text(message)


# def main() -> None:
#     app = ApplicationBuilder().token(settings.TELEGRAM_API_TOKEN).build()
#     app.add_handler(CommandHandler("start", start))
#     app.add_handler(CommandHandler("daily_summary", daily_summary))
    
#     # Handler for any text message that is not a command
#     app.add_handler(MessageHandler(filters.ALL, handle_food_description))

#     app.run_polling()


from django.core.management.base import BaseCommand, CommandError
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
from asgiref.sync import sync_to_async
from django.db.models import Sum
from core.models import MyUser, Calorie
from datetime import date
from openai_api.api_request import get_nutritional_info
from django.conf import settings


class Command(BaseCommand):
    help = "Starts the Telegram bot"

    def handle(self, *args, **options):
        main()


# Database helpers
@sync_to_async
def get_user(user_id):
    return MyUser.objects.get(user_id=user_id)


@sync_to_async
def update_or_create_user(user_id, first_name, last_name, username):
    user, created = MyUser.objects.update_or_create(
        user_id=user_id,
        defaults={
            'first_name': first_name,
            'last_name': last_name,
            'username': username,
        }
    )
    return user


@sync_to_async
def add_cpfc_entry(user, description, cpfc):
    entry = Calorie.objects.create(
        user=user,
        description=description,
        calories=cpfc['calories'],
        proteins=cpfc['proteins'],
        fats=cpfc['fats'],
        carbohydrates=cpfc['carbohydrates']
    )
    return entry.id  # Return the ID of the created entry


@sync_to_async
def delete_cpfc_entry(entry_id):
    Calorie.objects.filter(id=entry_id).delete()


# Telegram command handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user = await update_or_create_user(
        user_id=user_id,
        first_name=update.effective_user.first_name,
        last_name=update.effective_user.last_name,
        username=update.effective_user.username
    )
    await update.message.reply_text(f'Hello {user.first_name}! Input the food description and get its nutritional value. Accuracy directly corresponds to the amount of details provided.')


async def handle_food_description(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user = await get_user(user_id)
    description = update.message.text

    # Calculate CPFC based on the description
    cpfc = calculate_cpfc(description)

    # Save the CPFC entry in the database and get its ID
    entry_id = await add_cpfc_entry(user, description, cpfc)

    # Prepare the response with a delete button
    message = (f"Estimated nutritional values for this meal:\n"
               f"Calories: {cpfc['calories']} kcal\n"
               f"Proteins: {cpfc['proteins']} g\n"
               f"Fats: {cpfc['fats']} g\n"
               f"Carbohydrates: {cpfc['carbohydrates']} g")
    keyboard = [[InlineKeyboardButton("🗑 Delete", callback_data=f"delete_{entry_id}")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Send the response message with the delete button
    await update.message.reply_text(message, reply_markup=reply_markup)


async def delete_response(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # Extract the entry ID from the callback data
    entry_id = int(query.data.split("_")[1])

    # Delete the database entry
    await delete_cpfc_entry(entry_id)

    # Edit the original message to indicate deletion
    original_text = query.message.text

    # Function to add overline to each character
    def apply_overline(text):
        return "".join(char + "̶" for char in text)

    crossed_out_text = "\n".join(apply_overline(line) for line in original_text.split("\n"))

    await query.edit_message_text(
        crossed_out_text,
        parse_mode=ParseMode.HTML  # Use HTML as Markdown doesn't support these characters
    )


async def get_daily_cpfc(user):
    today = date.today()
    result = await sync_to_async(Calorie.objects.filter(user=user, created_date__date=today).aggregate)(
        total_calories=Sum('calories'),
        total_proteins=Sum('proteins'),
        total_fats=Sum('fats'),
        total_carbohydrates=Sum('carbohydrates')
    )
    return {
        'calories': result['total_calories'] or 0,
        'proteins': result['total_proteins'] or 0,
        'fats': result['total_fats'] or 0,
        'carbohydrates': result['total_carbohydrates'] or 0,
    }


async def daily_summary(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user = await get_user(user_id)
    cpfc = await get_daily_cpfc(user)
    message = (f"Your total intake today:\n"
               f"Calories: {cpfc['calories']} kcal\n"
               f"Proteins: {cpfc['proteins']} g\n"
               f"Fats: {cpfc['fats']} g\n"
               f"Carbohydrates: {cpfc['carbohydrates']} g")
    await update.message.reply_text(message)


# CPFC Calculation (mocked)
def calculate_cpfc(description: str):
    response = get_nutritional_info(description)  # Replace with actual API call
    f, p, cr, cl = [int(i) for i in response.split(' ')]
    return {
        'calories': cl,
        'proteins': p,
        'fats': f,
        'carbohydrates': cr
    }


def main() -> None:
    app = ApplicationBuilder().token(settings.TELEGRAM_API_TOKEN).build()

    # Command Handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("daily_summary", daily_summary))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_food_description))

    # Callback Query Handler for Delete Button
    app.add_handler(CallbackQueryHandler(delete_response, pattern="^delete_"))

    # Run the bot
    app.run_polling()

