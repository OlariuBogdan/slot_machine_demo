import tkinter as tk
import random
import pygame

# Lista de simboluri
SYMBOLS = ["Cherry", "Lemon", "Orange", "Plum", "Bell", "Star"]
CARD_COLORS = ["Red", "Black"]

class SlotMachine:
    def __init__(self, root):
        self.root = root
        self.root.title("Slot Machine")

        # Setăm fereastra în modul fullscreen
        self.root.attributes("-fullscreen", True)

        # Bind pentru ieșirea din modul fullscreen
        self.root.bind("<Escape>", self.exit_fullscreen)

        # Inițializăm pygame pentru sunete
        pygame.mixer.init()
        self.spin_sound = self.load_sound("sounds/spin.wav")
        self.win_sound = self.load_sound("sounds/win.wav")

        # Creditul inițial al jucătorului și statistici
        self.credits = 100
        self.total_wins = 0
        self.total_spins = 0
        self.bet = 10  # Suma inițială pariată
        self.max_bet = 1000  # Valoarea maximă a pariului

        # Frame pentru centrare
        self.frame = tk.Frame(root, bg='lightblue')
        self.frame.place(relx=0.5, rely=0.5, anchor="center")

        # Încărcăm imaginile simbolurilor
        self.symbol_images = {
            "Cherry": self.load_image("images/cherry.png"),
            "Lemon": self.load_image("images/lemon.png"),
            "Orange": self.load_image("images/orange.png"),
            "Plum": self.load_image("images/plum.png"),
            "Bell": self.load_image("images/bell.png"),
            "Star": self.load_image("images/star.png")
        }

        # Etichete pentru afișarea simbolurilor
        self.label1 = tk.Label(self.frame, image=self.symbol_images["Cherry"])
        self.label1.grid(row=0, column=0, padx=10, pady=10)

        self.label2 = tk.Label(self.frame, image=self.symbol_images["Lemon"])
        self.label2.grid(row=0, column=1, padx=10, pady=10)

        self.label3 = tk.Label(self.frame, image=self.symbol_images["Orange"])
        self.label3.grid(row=0, column=2, padx=10, pady=10)

        # Butoane pentru gestionarea pariurilor
        button_frame = tk.Frame(self.frame, bg='lightblue')
        button_frame.grid(row=1, column=0, columnspan=3, pady=20)

        self.min_bet_button = tk.Button(button_frame, text="Min Bet", command=self.set_min_bet, font=("Helvetica", 16))
        self.min_bet_button.grid(row=0, column=0, padx=5)

        self.decrease_bet_button = tk.Button(button_frame, text="Decrease Bet", command=self.decrement_bet, font=("Helvetica", 16))
        self.decrease_bet_button.grid(row=0, column=1, padx=5)

        self.increment_bet_button = tk.Button(button_frame, text="Increase Bet", command=self.increment_bet, font=("Helvetica", 16))
        self.increment_bet_button.grid(row=0, column=2, padx=5)

        self.max_bet_button = tk.Button(button_frame, text="Max Bet", command=self.set_max_bet, font=("Helvetica", 16))
        self.max_bet_button.grid(row=0, column=3, padx=5)

        self.spin_button = tk.Button(self.frame, text="Spin", command=self.spin, font=("Helvetica", 20))
        self.spin_button.grid(row=2, column=1, pady=20)

        # Butonul de "Risk"
        self.risk_button = tk.Button(self.frame, text="Risk", command=self.risk_game, font=("Helvetica", 20))
        self.risk_button.grid(row=2, column=2, pady=20)
        self.risk_button.grid_forget()  # Ascunde butonul de risc initial

        # Afișăm suma pariată
        self.bet_label = tk.Label(self.frame, text=f"Bet Amount: {self.bet}", font=("Helvetica", 16), bg='lightblue')
        self.bet_label.grid(row=3, column=0, columnspan=3, pady=10)

        # Etichetă pentru afișarea mesajului de câștig/pierdere
        self.result_label = tk.Label(self.frame, text="", font=("Helvetica", 24), bg='lightblue')
        self.result_label.grid(row=4, column=0, columnspan=3)

        # Etichete pentru afișarea creditelor și câștigurilor totale
        self.credits_label = tk.Label(self.frame, text=f"Credits: {self.credits}", font=("Helvetica", 16), bg='lightblue')
        self.credits_label.grid(row=5, column=0, columnspan=3)

        self.wins_label = tk.Label(self.frame, text=f"Total Wins: {self.total_wins}", font=("Helvetica", 16), bg='lightblue')
        self.wins_label.grid(row=6, column=0, columnspan=3)

        self.spins_label = tk.Label(self.frame, text=f"Total Spins: {self.total_spins}", font=("Helvetica", 16), bg='lightblue')
        self.spins_label.grid(row=7, column=0, columnspan=3)

    def load_sound(self, file):
        try:
            return pygame.mixer.Sound(file)
        except pygame.error as e:
            print(f"Error loading sound: {e}")
            return None

    def load_image(self, file):
        try:
            return tk.PhotoImage(file=file)
        except tk.TclError as e:
            print(f"Error loading image: {e}")
            return None

    def increment_bet(self):
        if self.bet < self.max_bet:
            self.bet += 10
            if self.bet > self.max_bet:
                self.bet = self.max_bet
        self.bet_label.config(text=f"Bet Amount: {self.bet}")

    def decrement_bet(self):
        if self.bet > 10:
            self.bet -= 10
        else:
            self.bet = self.max_bet  # Resetează la max_bet dacă ajunge la 10
        self.bet_label.config(text=f"Bet Amount: {self.bet}")

    def set_min_bet(self):
        self.bet = 10
        self.bet_label.config(text=f"Bet Amount: {self.bet}")

    def set_max_bet(self):
        self.bet = self.max_bet
        self.bet_label.config(text=f"Bet Amount: {self.bet}")

    def spin(self):
        if self.bet > self.credits:
            self.result_label.config(text="Insufficient credits!", fg="red")
            return

        # Verifică dacă există suficiente resurse pentru a reda sunetele
        if not self.spin_sound or not self.win_sound:
            self.result_label.config(text="Error loading sound files.", fg="red")
            return

        # Redăm sunetul de rotire
        pygame.mixer.Sound.play(self.spin_sound)

        self.credits -= self.bet
        self.total_spins += 1

        # Începem animația de rulare
        self.animate_reel()

    def animate_reel(self):
        symbols = SYMBOLS
        for _ in range(30):  # Mai multe iterații pentru a da senzația de rotire
            self.label1.config(image=self.symbol_images[random.choice(symbols)])
            self.label2.config(image=self.symbol_images[random.choice(symbols)])
            self.label3.config(image=self.symbol_images[random.choice(symbols)])
            self.root.update()
            self.root.after(50)
        
        # După animație, afișăm simbolurile finale
        self.show_final_result()

    def show_final_result(self):
        result = [random.choice(SYMBOLS) for _ in range(3)]
        
        self.label1.config(image=self.symbol_images[result[0]])
        self.label2.config(image=self.symbol_images[result[1]])
        self.label3.config(image=self.symbol_images[result[2]])

        payout = 0
        multiplier = 1

        if "Star" in result:
            multiplier = 3
            self.result_label.config(text="Star Symbol! 3x Multiplier!", fg="purple")

        if result[0] == result[1] == result[2]:
            payout = self.bet * 5
            self.result_label.config(text="Congratulations! You win!", fg="green")
            if result[0] == "Bell":
                self.start_bonus_round()
            self.risk_button.grid(row=2, column=2, pady=20)  # Arată butonul de risc
        elif result[0] == result[1] or result[1] == result[2] or result[0] == result[2]:
            payout = self.bet * 2
            self.result_label.config(text="Two of a kind! You win 2x!", fg="green")
            self.risk_button.grid(row=2, column=2, pady=20)  # Arată butonul de risc
        else:
            self.result_label.config(text="Sorry, you lose. Try again!", fg="red")
            self.risk_button.grid_forget()  # Ascunde butonul de risc

        payout *= multiplier
        self.total_wins += payout
        self.credits += payout

        # Redăm sunetul de câștig
        if payout > 0:
            pygame.mixer.Sound.play(self.win_sound)

        self.update_labels()

        # Dacă jucătorul rămâne fără credite
        if self.credits <= 0:
            self.result_label.config(text="Game over! No more credits.", fg="red")
            self.spin_button.config(state=tk.DISABLED)

    def risk_game(self):
        # Funcția pentru jocul de risc
        answer = tk.messagebox.askquestion("Risk", "Do you want to gamble your winnings?")  # Confirmare
        if answer == 'yes':
            card_color = random.choice(CARD_COLORS)
            guess = tk.simpledialog.askstring("Risk", "Guess the card color (Red/Black):")
            if guess:
                if guess.capitalize() == card_color:
                    self.total_wins *= 2
                    self.result_label.config(text=f"Correct! You doubled your winnings to {self.total_wins}!", fg="blue")
                else:
                    self.total_wins = 0
                    self.result_label.config(text="Wrong! You lost your winnings.", fg="red")
                self.update_labels()
                self.risk_button.grid_forget()  # Ascunde butonul de risc după jocul de risc

    def start_bonus_round(self):
        self.result_label.config(text="Bonus Round! Free spin!", fg="blue")
        self.root.after(2000, self.spin)  # Pornim rotirea gratuită după 2 secunde

    def exit_fullscreen(self, event=None):
        self.root.attributes("-fullscreen", False)
        self.root.geometry("800x600")  # Setează dimensiunea dorită a ferestrei

    def save_game(self):
        with open("savegame.txt", "w") as file:
            file.write(f"{self.credits}\n{self.total_wins}\n{self.total_spins}\n{self.bet}")

    def load_game(self):
        try:
            with open("savegame.txt", "r") as file:
                data = file.readlines()
                self.credits = int(data[0].strip())
                self.total_wins = int(data[1].strip())
                self.total_spins = int(data[2].strip())
                self.bet = int(data[3].strip())
                self.update_labels()
        except FileNotFoundError:
            pass  # Nu există fișier de salvare

# Inițializăm fereastra principală
root = tk.Tk()
app = SlotMachine(root)
app.load_game()  # Încarcă progresul jocului, dacă există
root.mainloop()
