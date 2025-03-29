import random
import os
import tkinter as tk
from tkinter import ttk, messagebox

def generate_fraction(min_val=1, max_val=9):
    """Generate a random fraction with coprime numerator and denominator."""
    from math import gcd
    numerator = random.randint(min_val, max_val)
    denominator = random.randint(min_val, max_val)
    while gcd(numerator, denominator) != 1:
        numerator = random.randint(min_val, max_val)
        denominator = random.randint(min_val, max_val)
    return (numerator, denominator)

def generate_algebra_problem():
    """Generate a random algebraic equation for x."""
    equation_type = random.choice([1, 2])
    
    if equation_type == 1:
        # a*x + b = c
        a = random.randint(1, 9)
        x_val = random.randint(0, 9)
        b = random.randint(0, 9)
        c = a * x_val + b
        question_str = f"Solve for x: \\(\\displaystyle {a}x + {b} = {c}\\)"
        answer_str = f"x = {x_val}"
    else:
        # a*x + b = c*x + d
        x_val = random.randint(0, 9)
        a = random.randint(1, 9)
        c = random.randint(1, 9)
        while c == a:
            c = random.randint(1, 9)
        b = random.randint(0, 9)
        d = b + x_val * (a - c)
        question_str = f"Solve for x: \\(\\displaystyle {a}x + {b} = {c}x + {d}\\)"
        answer_str = f"x = {x_val}"
    
    return question_str, answer_str

def generate_arithmetic_problem(difficulty):
    """Generate a single arithmetic problem based on difficulty."""
    if difficulty == '1':  
        operations = ['+', '-']
        num_range = (1, 10)
    elif difficulty == '2': 
        operations = ['+', '-', '/']
        num_range = (1, 20)
    elif difficulty == '3':  
        operations = ['+', '-', '/', 'fraction_mul']
        num_range = (1, 30)
    elif difficulty == '4':  
        operations = ['+', '-', '/', 'fraction_mul']
        num_range = (1, 50)
    else:
        operations = ['+', '-']
        num_range = (1, 10)
    
    op = random.choice(operations)
    
    if op == '+':
        a, b = random.randint(*num_range), random.randint(*num_range)
        question = f"\\(\\displaystyle {a} + {b}\\)"
        answer = a + b
    elif op == '-':
        a, b = random.randint(*num_range), random.randint(*num_range)
        if a < b:
            a, b = b, a
        question = f"\\(\\displaystyle {a} - {b}\\)"
        answer = a - b
    elif op == '/':
        b = random.randint(1, num_range[1])
        multiple = random.randint(*num_range)
        a = multiple * b
        question = f"\\(\\displaystyle {a} \\div {b}\\)"
        answer = a // b
    elif op == 'fraction_mul':
        num1, den1 = generate_fraction(1, 9)
        num2, den2 = generate_fraction(1, 9)
        question = f"\\(\\displaystyle \\frac{{{num1}}}{{{den1}}} \\times \\frac{{{num2}}}{{{den2}}}\\)"
        from math import gcd
        product_num = num1 * num2
        product_den = den1 * den2
        g = gcd(product_num, product_den)
        product_num //= g
        product_den //= g
        answer = f"{product_num}/{product_den}"
    else:
        a, b = random.randint(*num_range), random.randint(*num_range)
        question = f"\\(\\displaystyle {a} + {b}\\)"
        answer = a + b
    
    return question, str(answer)

def generate_test(difficulty, include_algebra, total_questions, points_per_q, 
                  arith_questions=None, alg_questions=None, arith_points=None, alg_points=None):
    """Generate test files based on GUI input and return the output directory."""
    problems = []
    
    if not include_algebra:
        for _ in range(total_questions):
            q, ans = generate_arithmetic_problem(difficulty)
            problems.append(('arithmetic', q, ans, points_per_q))
        total_points = total_questions * points_per_q
    else:
        for _ in range(arith_questions):
            q, ans = generate_arithmetic_problem(difficulty)
            problems.append(('arithmetic', q, ans, arith_points))
        for _ in range(alg_questions):
            aq, aans = generate_algebra_problem()
            problems.append(('algebra', aq, aans, alg_points))
        total_points = (arith_questions * arith_points) + (alg_questions * alg_points)
    
    # Questions .tex
    questions_content = [
        "\\documentclass[12pt]{article}",
        "\\usepackage[margin=1in]{geometry}",
        "\\usepackage{amsmath}",
        "\\begin{document}",
        "\\section*{Arithmetic Test}",
        "\\textbf{Name:}\\underline{\\hspace{8cm}}\\hfill \\textbf{Date:}\\underline{\\hspace{5cm}}",
        "\\vspace{1em}",
        f"\\textbf{{Total Questions:}} {len(problems)}\\\\",
        f"\\textbf{{Total Points:}} {total_points}\\\\",
        "\\vspace{1em}",
        "Answer each of the following questions clearly:",
        "\\\\[1em]"
    ]
    if include_algebra:
        questions_content.append(
            "\\textit{Algebra questions are labeled \"Solve for x:\". Be sure to show each step!}"
        )
    questions_content.append("\\begin{enumerate}")
    for i, (ptype, question, _, p_value) in enumerate(problems, 1):
        spacing = "\\vspace{4\\baselineskip}" if ptype == 'arithmetic' else "\\vspace{8\\baselineskip}"
        questions_content.append(f"\\item {question} \\textit{{({p_value} points)}}{spacing}")
    questions_content.extend(["\\end{enumerate}", "\\end{document}"])
    
    # Answers .tex
    answers_content = [
        "\\documentclass[12pt]{article}",
        "\\usepackage[margin=1in]{geometry}",
        "\\usepackage{amsmath}",
        "\\begin{document}",
        f"\\section*{{Answer Key (Difficulty {difficulty})}}",
        "\\begin{enumerate}"
    ]
    for i, (_, _, ans, p_value) in enumerate(problems, 1):
        answers_content.append(f"\\item {ans} \\textit{{({p_value} pts)}}")
    answers_content.extend(["\\end{enumerate}", "\\end{document}"])
    
    # Write files and return the directory
    output_dir = os.getcwd()
    with open(os.path.join(output_dir, "questions.tex"), "w", encoding="utf-8") as qf:
        qf.write("\n".join(questions_content))
    with open(os.path.join(output_dir, "answers.tex"), "w", encoding="utf-8") as af:
        af.write("\n".join(answers_content))
    
    return output_dir

def create_gui():
    """Create the GUI for the Arithmetic Test Generator."""
    root = tk.Tk()
    root.title("Arithmetic Test Generator")
    root.geometry("500x600")
    root.configure(bg="#F5F6F5")

    # Styles
    style = ttk.Style()
    style.configure("TLabel", background="#F5F6F5", font=("Segoe UI", 10))
    style.configure("TButton", font=("Segoe UI", 10))
    style.configure("TRadiobutton", background="#F5F6F5", font=("Segoe UI", 10))

    # Header
    header = ttk.Label(root, text="Arithmetic Test Generator", font=("Segoe UI", 14, "bold"), foreground="#2E7D32")
    header.pack(pady=10)

    # Difficulty Frame
    diff_frame = ttk.LabelFrame(root, text="Select Difficulty", padding=10)
    diff_frame.pack(fill="x", padx=10, pady=5)
    diff_var = tk.StringVar(value="1")
    difficulties = [
        ("1st-3rd Grade (1)", "1", "#1976D2"),
        ("4th Grade (2)", "2", "#AB47BC"),
        ("5th-6th Grade (3)", "3", "#FFB300"),
        ("6th-7th Grade (4)", "4", "#D32F2F")
    ]
    for text, value, color in difficulties:
        ttk.Radiobutton(diff_frame, text=text, value=value, variable=diff_var, 
                        style="TRadiobutton", command=lambda: update_color(diff_label, diff_var.get())).pack(anchor="w")
    
    def update_color(label, difficulty):
        colors = {"1": "#1976D2", "2": "#AB47BC", "3": "#FFB300", "4": "#D32F2F"}
        label.configure(foreground=colors.get(difficulty, "#1976D2"))

    diff_label = ttk.Label(diff_frame, text="Difficulty: 1st-3rd Grade", foreground="#1976D2")
    diff_label.pack(pady=5)

    # Algebra Frame
    alg_frame = ttk.LabelFrame(root, text="Include Algebra?", padding=10)
    alg_frame.pack(fill="x", padx=10, pady=5)
    alg_var = tk.BooleanVar(value=False)
    ttk.Checkbutton(alg_frame, text="Yes, include algebra questions", variable=alg_var, 
                    command=lambda: toggle_algebra_fields()).pack(anchor="w")

    # Input Frame
    input_frame = ttk.LabelFrame(root, text="Test Details", padding=10)
    input_frame.pack(fill="x", padx=10, pady=5)

    # Non-algebra inputs
    total_q_label = ttk.Label(input_frame, text="Total Questions:")
    total_q_label.pack(anchor="w")
    total_q_entry = ttk.Entry(input_frame)
    total_q_entry.pack(fill="x", pady=2)
    total_q_entry.insert(0, "10")

    points_q_label = ttk.Label(input_frame, text="Points per Question:")
    points_q_label.pack(anchor="w")
    points_q_entry = ttk.Entry(input_frame)
    points_q_entry.pack(fill="x", pady=2)
    points_q_entry.insert(0, "1")

    # Algebra inputs (hidden initially)
    arith_q_label = ttk.Label(input_frame, text="Arithmetic Questions:")
    arith_q_entry = ttk.Entry(input_frame)
    arith_points_label = ttk.Label(input_frame, text="Points per Arithmetic Q:")
    arith_points_entry = ttk.Entry(input_frame)
    alg_q_label = ttk.Label(input_frame, text="Algebra Questions:")
    alg_q_entry = ttk.Entry(input_frame)
    alg_points_label = ttk.Label(input_frame, text="Points per Algebra Q:")
    alg_points_entry = ttk.Entry(input_frame)

    def toggle_algebra_fields():
        if alg_var.get():
            total_q_label.pack_forget()
            total_q_entry.pack_forget()
            points_q_label.pack_forget()
            points_q_entry.pack_forget()
            arith_q_label.pack(anchor="w")
            arith_q_entry.pack(fill="x", pady=2)
            arith_q_entry.delete(0, tk.END)
            arith_q_entry.insert(0, "5")
            arith_points_label.pack(anchor="w")
            arith_points_entry.pack(fill="x", pady=2)
            arith_points_entry.delete(0, tk.END)
            arith_points_entry.insert(0, "1")
            alg_q_label.pack(anchor="w")
            alg_q_entry.pack(fill="x", pady=2)
            alg_q_entry.delete(0, tk.END)
            alg_q_entry.insert(0, "5")
            alg_points_label.pack(anchor="w")
            alg_points_entry.pack(fill="x", pady=2)
            alg_points_entry.delete(0, tk.END)
            alg_points_entry.insert(0, "2")
        else:
            arith_q_label.pack_forget()
            arith_q_entry.pack_forget()
            arith_points_label.pack_forget()
            arith_points_entry.pack_forget()
            alg_q_label.pack_forget()
            alg_q_entry.pack_forget()
            alg_points_label.pack_forget()
            alg_points_entry.pack_forget()
            total_q_label.pack(anchor="w")
            total_q_entry.pack(fill="x", pady=2)
            points_q_label.pack(anchor="w")
            points_q_entry.pack(fill="x", pady=2)

    # Generate Button
    def on_generate():
        try:
            difficulty = diff_var.get()
            include_algebra = alg_var.get()
            if not include_algebra:
                total_questions = int(total_q_entry.get())
                points_per_q = float(points_q_entry.get())
                output_dir = generate_test(difficulty, False, total_questions, points_per_q)
            else:
                arith_questions = int(arith_q_entry.get())
                alg_questions = int(alg_q_entry.get())
                arith_points = float(arith_points_entry.get())
                alg_points = float(alg_points_entry.get())
                output_dir = generate_test(difficulty, True, 0, 0, arith_questions, alg_questions, arith_points, alg_points)
            questions_path = os.path.abspath(os.path.join(output_dir, "questions.tex"))
            answers_path = os.path.abspath(os.path.join(output_dir, "answers.tex"))
            messagebox.showinfo("Success", 
                                f"Generated successfully!\n\n"
                                f"The generated files have been saved to:\n"
                                f"{questions_path}\n"
                                f"{answers_path}\n\n"
                                f"Next, use free online .tex to PDF converters to transform the two .tex files into LaTeX-formatted PDF files.")
        except ValueError as e:
            messagebox.showerror("Error", "Please enter valid numbers for all fields.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    generate_btn = ttk.Button(root, text="Generate Test", command=on_generate)
    generate_btn.pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    create_gui()
