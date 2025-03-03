import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
from mcstatus import JavaServer

TOKEN = "blahblah"
SERVER_ADDRESS = "s4.pixelmon.cristalix.gg"

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

async def get_minecraft_server_status():
    try:
        server = JavaServer.lookup(SERVER_ADDRESS)
        status = server.status()

        online_players = status.players.online
        max_players = status.players.max
        player_names = [player.name for player in status.players.sample] if status.players.sample else []

        return {
            "online_players": online_players,
            "max_players": max_players,
            "player_names": player_names
        }
    except Exception as e:
        return {"error": str(e)}

async def pixel_online(update: Update, context: CallbackContext) -> None:
    server_info = await get_minecraft_server_status()

    if "error" in server_info:
        await update.message.reply_text(f"❌ Ошибка при получении данных: {server_info['error']}")
        return

    online_players = server_info["online_players"]
    max_players = server_info["max_players"]
    player_names = server_info["player_names"]

    message = f"▶ **Текущий онлайн:** {online_players}/{max_players}\n\n"

    if player_names:
        message += "**Игроки онлайн:**\n```\n" + "\n".join(player_names) + "\n```\n"
    
    important_players = {"DedSchweppesss", "DevilAsh", "tkirit", "Snowly_Penguin"}
    if any(player in important_players for player in player_names):
        message += "⚠ **Модераторы на сервере\!**"

    await update.message.reply_markdown_v2(message)

async def start_msg(update:Update, context: CallbackContext) -> None:
    message = (
        "дарова ёптить\n\n"
        "/pixelonline ёбни, и я скажу кто там сидит"
    )

    await update.message.reply_text(message)

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("pixelonline", pixel_online))
    app.add_handler(CommandHandler("start",start_msg))

    print("Бот запущен...")
    app.run_polling()

if __name__ == "__main__":
    main()
