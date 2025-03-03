import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import os
from mcstatus import JavaServer

SERVER_ADDRESS = "s4.pixelmon.cristalix.gg"
IMPORTANT_PLAYERS = {"DedSchweppesss", "DevilAsh", "tkirit", "Snowly_Penguin"}  # Список важных игроков

class MinecraftServerStatusApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Minecraft Server Status")
        self.root.configure(bg="black")
        self.root.resizable(False, False)

        style = ttk.Style()
        style.configure("TLabel", background="black", foreground="white")
        style.configure("TFrame", background="black")
        style.configure("Treeview", background="black", foreground="white", fieldbackground="black")
        style.map("Treeview", background=[("selected", "grey")])

        self.main_frame = ttk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.online_label = ttk.Label(self.main_frame, text="Онлайн: 0/0", font=("Arial", 16))
        self.online_label.pack(pady=13)

        self.tree = ttk.Treeview(self.main_frame, columns=("Player"), show="headings", height=13)
        self.tree.heading("Player", text="Игроки онлайн")
        self.tree.pack(fill=tk.BOTH, expand=True, padx=13, pady=13)

        self.important_players_online = set()
        self.notification_shown = False

        self.update_thread = threading.Thread(target=self.update_status, daemon=True)
        self.update_thread.start()

    def get_minecraft_server_status(self):
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

    def update_status(self):
        while True:
            server_info = self.get_minecraft_server_status()

            if "error" in server_info:
                self.online_label.config(text="Ошибка при получении данных")
            else:
                online_players = server_info["online_players"]
                max_players = server_info["max_players"]
                player_names = server_info["player_names"]

                player_names_sorted = sorted(player_names, key=str.lower)

                self.online_label.config(text=f"Онлайн: {online_players}/{max_players}")

                for row in self.tree.get_children():
                    self.tree.delete(row)

                for i, player in enumerate(player_names_sorted):
                    if i < 12:
                        if player in IMPORTANT_PLAYERS:
                            self.tree.insert("", "end", values=(player,), tags=("important",))
                        else:
                            self.tree.insert("", "end", values=(player,))
                    else:
                        break

                if online_players >= 13:
                    remaining_players = online_players - 12
                    self.tree.insert("", "end", values=(f"... и ещё {remaining_players} игроков",))

                self.tree.tag_configure("important", foreground="red")

                current_important_players = set(player_names_sorted).intersection(IMPORTANT_PLAYERS)

                if current_important_players and not self.notification_shown:
                    self.notification_shown = True
                    self.show_notification(current_important_players)

                if not current_important_players:
                    self.notification_shown = False
                    self.important_players_online.clear()

            time.sleep(5)

    def show_notification(self, important_players):
        """Показывает уведомление о входе важных игроков."""
        players_list = ", ".join(important_players)
        response = messagebox.askyesno(
            "тихо там","хуй зашел, выйти?"
        )

        if response:
            self.kill_java_process()

    def kill_java_process(self):
        """Убивает процесс java.exe."""
        try:
            os.system("taskkill /f /im java.exe")
            print("Процесс java.exe убит.")
        except Exception as e:
            print(f"Ошибка при убийстве процесса java.exe: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = MinecraftServerStatusApp(root)
    root.mainloop()