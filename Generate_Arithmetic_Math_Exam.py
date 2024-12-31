import random
import os

# ANSI escape codes for coloring text in the console
GREEN = "\033[92m"
CYAN = "\033[96m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"  # Resets color to default

def generate_fraction(min_val=1, max_val=9):
    """
    Generate a random fraction within a specified range,
    ensuring numerator and denominator are coprime.
    """
    from math import gcd
    numerator = random.randint(min_val, max_val)
    denominator = random.randint(min_val, max_val)
    while gcd(numerator, denominator) != 1:
        numerator = random.randint(min_val, max_val)
        denominator = random.randint(min_val, max_val)
    return (numerator, denominator)

def generate_algebra_problem():
    """
    Generates a random algebraic equation for x.
    Types:
      1) a*x + b = c
      2) a*x + b = c*x + d
    All expressions use \displaystyle for bigger display.
    """
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
    """
    Generates a single arithmetic problem (non-algebra)
    based on difficulty and returns (question, answer).
    Uses \displaystyle for bigger expressions.
    """
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
        # Even if "hard," these are the advanced arithmetic ops
        operations = ['+', '-', '/', 'fraction_mul']
        num_range = (1, 50)
    else:
        # Fallback
        operations = ['+', '-']
        num_range = (1, 10)
    
    op = random.choice(operations)
    
    if op == '+':
        a = random.randint(*num_range)
        b = random.randint(*num_range)
        question = f"\\(\\displaystyle {a} + {b}\\)"
        answer = a + b
        
    elif op == '-':
        a = random.randint(*num_range)
        b = random.randint(*num_range)
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
        question = (
            f"\\(\\displaystyle \\frac{{{num1}}}{{{den1}}}"
            f" \\times \\frac{{{num2}}}{{{den2}}}\\)"
        )
        from math import gcd
        product_num = num1 * num2
        product_den = den1 * den2
        g = gcd(product_num, product_den)
        product_num //= g
        product_den //= g
        
        answer = f"{product_num}/{product_den}"
    
    else:
        # Fallback
        a = random.randint(*num_range)
        b = random.randint(*num_range)
        question = f"\\(\\displaystyle {a} + {b}\\)"
        answer = a + b
    
    return question, str(answer)

def generate_test():
    """
    Main driver:
      1. Asks user for difficulty.
      2. Asks if they want to include algebra.
         - If 'n', ask total questions + single point value.
         - If 'y', ask # arithmetic Q, # algebra Q, plus separate point values.
      3. Generates .tex files for questions + answers, with spacing:
         - Arithmetic => \vspace{4\baselineskip}
         - Algebra => \vspace{8\baselineskip}
      4. Displays total points at the top of the test.
      5. Uses 1-inch margins in the .tex output
      6. Console menu text is colored using ANSI escape codes.
    """
    # Colored "Welcome" text in green
    print(f"{GREEN}Welcome to the Arithmetic Test Generator!{RESET}")
    
    print("======================================================== \n")
    
    # Show difficulty levels in colorful text
    print(f"{CYAN}Difficulty levels:{RESET}")
    print(f"{BLUE}1. For 1st to 3rd Grade level Math (enter '1'){RESET}")
    print(f"{MAGENTA}2. For 4th Grade level Math (enter '2'){RESET}")
    print(f"{YELLOW}3. For 5th to 6th Grade level Math (enter '3'){RESET}")
    print(f"{RED}4. For 6th to 7th Grade level Math  (enter '4'){RESET}")
    
    print("======================================================== \n")
    
    difficulty = input("Select difficulty level by number choice from the menu (e.g.,1 for '1-3rd Grade level ', 2 for '4th Grade Level', \n 3 for'5-6th Grade Levl', 4 for  '6-7th Grade level'): ").strip()
    
    # Algebra or not
    algebra_choice = input("Would you like to include Algebra questions? (y/n): ").strip().lower()
    include_algebra = (algebra_choice == 'y')
    
    problems = []
    total_arithmetic = 0
    total_algebra = 0
    arithmetic_points = 0.0
    algebra_points = 0.0
    
    if not include_algebra:
        # Simple approach: total + single point value
        total_questions = int(input("How many questions total would you like? "))
        points_per_question = float(input("How many points is each question worth? "))
        
        for _ in range(total_questions):
            q, ans = generate_arithmetic_problem(difficulty)
            problems.append(('arithmetic', q, ans, points_per_question))
        
        total_arithmetic = total_questions
        total_algebra = 0
        arithmetic_points = points_per_question
        
    else:
        # Algebra approach:
        total_arithmetic = int(input("How many arithmetic questions? "))
        total_algebra = int(input("How many algebra questions? "))
        
        arithmetic_points = float(input("How many points per arithmetic question? "))
        algebra_points = float(input("How many points per algebra question? "))
        
        # Generate arithmetic questions
        for _ in range(total_arithmetic):
            q, ans = generate_arithmetic_problem(difficulty)
            problems.append(('arithmetic', q, ans, arithmetic_points))
        
        # Generate algebra questions
        for _ in range(total_algebra):
            aq, aans = generate_algebra_problem()
            problems.append(('algebra', aq, aans, algebra_points))
        
        # If you want them in random order, uncomment:
        # import random
        # random.shuffle(problems)
    
    # Summaries
    total_questions = total_arithmetic + total_algebra
    total_points = (total_arithmetic * arithmetic_points) + (total_algebra * algebra_points)
    
    # Build questions.tex with 1 inch margins
    questions_content = [
        "\\documentclass[12pt]{article}",
        "\\usepackage[margin=1in]{geometry}",  # 1 inch all-around margin
        "\\usepackage{amsmath}",
        "\\begin{document}",
        "\\section*{Arithmetic Test}",
        # Name/Date fields
        "\\textbf{Name:}\\underline{\\hspace{8cm}}\\hfill"
        "\\textbf{Date:}\\underline{\\hspace{5cm}}",
        "\\vspace{1em}",
        f"\\textbf{{Total Questions:}} {total_questions}\\\\",
        f"\\textbf{{Total Points:}} {total_points}\\\\",  # Show total points
        "\\vspace{1em}",
        "Answer each of the following questions clearly:",
        "\\\\[1em]"
    ]
    
    if include_algebra:
        questions_content.append(
            "\\textit{Algebra questions are labeled \"Solve for x:\". "
            "Be sure to show each step!}"
        )
    
    questions_content.append("\\begin{enumerate}")
    
    for i, (ptype, question, ans, p_value) in enumerate(problems, start=1):
        if ptype == 'arithmetic':
            # Arithmetic => \vspace{4\baselineskip}
            questions_content.append(
                f"\\item {question} \\textit{{({p_value} points)}}\\vspace{{4\\baselineskip}}"
            )
        else:
            # Algebra => \vspace{8\baselineskip}
            questions_content.append(
                f"\\item {question} \\textit{{({p_value} points)}}\\vspace{{8\\baselineskip}}"
            )
    
    questions_content.append("\\end{enumerate}")
    questions_content.append("\\end{document}")
    
    # Build answers.tex with 1 inch margins
    answers_content = [
        "\\documentclass[12pt]{article}",
        "\\usepackage[margin=1in]{geometry}",
        "\\usepackage{amsmath}",
        "\\begin{document}",
        f"\\section*{{Answer Key (Difficulty {difficulty})}}",
        "\\begin{enumerate}"
    ]
    
    for i, (ptype, q, ans, p_value) in enumerate(problems, start=1):
        answers_content.append(
            f"\\item {ans} \\textit{{({p_value} pts)}}"
        )
    
    answers_content.append("\\end{enumerate}")
    answers_content.append("\\end{document}")
    
    # Write .tex files
    with open("questions.tex", "w", encoding="utf-8") as qf:
        qf.write("\n".join(questions_content))
    # File creation message in green
    print(f"Questions written to {GREEN}questions.tex{RESET}")
    print(f"You can use free online '.tex to PDF' conversion tools from the internet to convert {GREEN}questions.tex{RESET} to human legible PDF file")
    
    with open("answers.tex", "w", encoding="utf-8") as af:
        af.write("\n".join(answers_content))
    # File creation message in green
    print(f"Answer key written to {GREEN}answers.tex{RESET}")
    print(f"You can use free online '.tex to PDF' conversion tools from the internet to convert {GREEN}answers.tex{RESET} to human legible PDF file")

if __name__ == "__main__":
    generate_test()
