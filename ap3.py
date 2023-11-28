import tkinter as tk
from tkinter import messagebox

class Question:
    def __init__(self, prompt, options, correct_option, points, correct_feedback, incorrect_feedback):
        self.prompt = prompt
        self.options = options
        self.correct_option = correct_option
        self.points = points
        self.correct_feedback = correct_feedback
        self.incorrect_feedback = incorrect_feedback


class Puzzle:
    def __init__(self, description, solution, points, correct_feedback, incorrect_feedback):
        self.description = description
        self.solution = solution
        self.points = points
        self.correct_feedback = correct_feedback
        self.incorrect_feedback = incorrect_feedback


class QuizApp:
    def __init__(self, master, questions, puzzles):
        self.master = master
        self.master.title("Quiz Espacial")
        self.master.geometry("800x600")
        self.master.configure(bg="black")

        self.questions = questions
        self.puzzles = puzzles
        self.score = 0

        self.current_question_index = 0
        self.current_puzzle_index = 0

        self.intro_label = tk.Label(master, text="Bem-vindo, explorador espacial!", font=("Arial", 20, "bold"), bg="black", fg="white")
        self.intro_label.pack(pady=10)

        self.start_button = tk.Button(master, text="Iniciar Quiz", command=self.start_quiz, font=("Arial", 16), bg="green", fg="white")
        self.start_button.pack(pady=20)

        self.score_label = tk.Label(master, text="Pontuação: 0", font=("Arial", 16), bg="black", fg="white")
        self.score_label.pack(pady=10)

        self.var = tk.StringVar()
        self.var.set(None)  # Variável para armazenar a opção selecionada

        self.master.bind('<Return>', self.enter_pressed)  # Bind 'Enter' key press event

    def start_quiz(self):
        self.intro_label.pack_forget()
        self.start_button.pack_forget()

        self.ask_question()

    def ask_question(self):
        if self.current_question_index < len(self.questions):
            question = self.questions[self.current_question_index]

            self.question_label = tk.Label(self.master, text=question.prompt, font=("Arial", 18), bg="black", fg="white")
            self.question_label.pack(pady=10)

            for i, option in enumerate(question.options):
                option_radio = tk.Radiobutton(self.master, text=option, variable=self.var, value=str(i), font=("Arial", 14), bg="black", fg="white", selectcolor="black")
                option_radio.pack()

            self.submit_button = tk.Button(self.master, text="Enviar Resposta", command=self.check_answer, font=("Arial", 14), bg="green", fg="white")
            self.submit_button.pack(pady=20)

        elif self.current_puzzle_index < len(self.puzzles):
            self.ask_puzzle()

        else:
            self.show_result()

    def ask_puzzle(self):
        puzzle = self.puzzles[self.current_puzzle_index]

        self.question_label = tk.Label(self.master, text=puzzle.description, font=("Arial", 18), bg="black", fg="white")
        self.question_label.pack(pady=10)

        self.user_solution_entry = tk.Entry(self.master, font=("Arial", 14), bg="white", fg="black")
        self.user_solution_entry.pack(pady=10)

        self.submit_button = tk.Button(self.master, text="Enviar Solução", command=self.check_solution, font=("Arial", 14), bg="green", fg="white")
        self.submit_button.pack(pady=20)

    def check_answer(self):
        selected_option = self.var.get()
        question = self.questions[self.current_question_index]

        if selected_option == str(question.correct_option):
            messagebox.showinfo("Resposta Correta", f"{question.correct_feedback} Você ganhou {question.points} pontos.")
            self.score += question.points
        else:
            messagebox.showerror("Resposta Incorreta", question.incorrect_feedback)

        self.current_question_index += 1
        self.clear_widgets()
        self.update_score()
        self.ask_question()

    def check_solution(self):
        user_solution = self.user_solution_entry.get()
        puzzle = self.puzzles[self.current_puzzle_index]

        if user_solution == puzzle.solution:
            messagebox.showinfo("Solução Correta", f"{puzzle.correct_feedback} Você ganhou {puzzle.points} pontos.")
            self.score += puzzle.points
        else:
            messagebox.showerror("Solução Incorreta", puzzle.incorrect_feedback)

        self.current_puzzle_index += 1
        self.clear_widgets()
        self.update_score()
        self.ask_question()

    def show_result(self):
        result_label = tk.Label(self.master, text=f"Sua pontuação final é {self.score} pontos.", font=("Arial", 20, "bold"), bg="black", fg="white")
        result_label.pack(pady=20)

        if self.score == sum([question.points for question in self.questions]) + sum([puzzle.points for puzzle in self.puzzles]):
            congrats_label = tk.Label(self.master, text="Parabéns! Você acertou todas as perguntas e quebra-cabeças. Você é um verdadeiro mestre do conhecimento!", font=("Arial", 16), bg="green", fg="white")
            congrats_label.pack(pady=10)
        else:
            thanks_label = tk.Label(self.master, text="Obrigado por explorar o universo em busca de conhecimento!", font=("Arial", 16), bg="black", fg="white")
            thanks_label.pack(pady=10)

    def update_score(self):
        self.score_label.config(text=f"Pontuação: {self.score}")

    def clear_widgets(self):
        for widget in self.master.winfo_children():
            widget.pack_forget()

    def enter_pressed(self, event):
        if self.submit_button.winfo_ismapped():
            self.submit_button.invoke()


if __name__ == "__main__":
    questions = [
        Question("Qual é a capital do Brasil?", ["São Paulo", "Rio de Janeiro", "Brasília"], 2, 10,
                 "Resposta correta! Brasília é a capital do Brasil.", "Resposta incorreta. A capital do Brasil é Brasília."),
        Question("Quantos planetas existem em nosso sistema solar?", ["7", "9", "8"], 2, 20,
                 "Correto! Existem 8 planetas em nosso sistema solar.", "Resposta errada. Nosso sistema solar possui 8 planetas."),
        Question("Qual é o símbolo químico para o oxigênio?", ["Ox", "O", "O2"], 1, 15,
                 "Você acertou! 'O' é o símbolo químico do oxigênio.", "Errado. O símbolo químico do oxigênio é 'O'."),
        Question("Quem escreveu 'Dom Quixote'?", ["Miguel de Cervantes", "Gabriel García Márquez", "Paulo Coelho"], 0, 25,
                 "Isso mesmo! Miguel de Cervantes é o autor de 'Dom Quixote.", "Incorreto. O autor de 'Dom Quixote' é Miguel de Cervantes."),
        Question("Qual é a fórmula química da água?", ["H2O2", "CO2", "H2O"], 2, 15,
                 "Correto! A fórmula química da água é H2O.", "Errado. A fórmula química da água é H2O.")
    ]

    puzzles = [
        Puzzle("Resolva o quebra-cabeça: 3 * 4 = ?", "12", 10,
               "Bom trabalho! A resposta correta é 12.", "Resposta incorreta. O resultado correto é 12."),
        Puzzle("Resolva o quebra-cabeça: 7 + 8 = ?", "15", 15,
               "Ótimo! 7 + 8 é igual a 15.", "Errado. A resposta correta é 15."),
        Puzzle("Resolva o quebra-cabeça: Qual é o resultado de 2^3?", "8", 20,
               "Você acertou! 2^3 é igual a 8.", "Incorreto. A resposta correta é 8."),
        Puzzle("Resolva o quebra-cabeça de lógica: Se 5 + 3 = 28, 9 + 1 = 810, então 6 + 3 = ?",
               "63", 25, "Excelente! A resposta é 63.", "Errado. A solução é 63.")
    ]

    root = tk.Tk()
    app = QuizApp(root, questions, puzzles)
    root.mainloop()
