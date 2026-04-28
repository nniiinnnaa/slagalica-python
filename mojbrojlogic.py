# ...na vrhu fajla...
from itertools import permutations, combinations
import math
import random
import threading
import time
import threading
import pygame
import re

def ocisti_zagrade(expr):
    # Ukloni zagrade oko brojeva
    expr = re.sub(r'\((\d+)\)', r'\1', expr)

    # Ukloni zagrade oko celog izraza ako su uparene
    while expr.startswith('(') and expr.endswith(')'):
        unutra = expr[1:-1]
        if unutra.count('(') == unutra.count(')'):
            expr = unutra
        else:
            break


    return expr


def najblizi_izraz(brojevi, cilj):
    memo = {}

    def ok(s):
        return '-' not in s and '+' not in s

    def gen_exprs(nums):
        key = tuple(sorted(n[0] for n in nums))
        if key in memo:
            return memo[key]

        results = []
        seen = set()

        if len(nums) == 1:
            results.append(nums[0])
        else:
            for i in range(1, len(nums)):
                for left in combinations(range(len(nums)), i):
                    right = [j for j in range(len(nums)) if j not in left]
                    left_exprs = gen_exprs([nums[j] for j in left])
                    right_exprs = gen_exprs([nums[j] for j in right])

                    for a_val, a_str in left_exprs:
                        for b_val, b_str in right_exprs:

                            # Addition
                            res = a_val + b_val
                            expr = f"{a_str}+{b_str}"
                            if res not in seen:
                                results.append((res, expr))
                                seen.add(res)

                            # Subtraction a - b
                            res = a_val - b_val
                            expr = f"{a_str}-({b_str})" if not ok(b_str) else f"{a_str}-{b_str}"
                            if res not in seen:
                                results.append((res, expr))
                                seen.add(res)

                            # Subtraction b - a
                            res = b_val - a_val
                            expr = f"{b_str}-({a_str})" if not ok(a_str) else f"{b_str}-{a_str}"
                            if res not in seen:
                                results.append((res, expr))
                                seen.add(res)

                            # Multiplication
                            res = a_val * b_val
                            a_fmt = a_str if ok(a_str) else f"({a_str})"
                            b_fmt = b_str if ok(b_str) else f"({b_str})"
                            expr = f"{a_fmt}*{b_fmt}"
                            if res not in seen:
                                results.append((res, expr))
                                seen.add(res)

                            # Division a / b
                            if b_val != 0 and a_val % b_val == 0:
                                res = a_val // b_val
                                expr = f"({a_str})/({b_str})"
                                if res not in seen:
                                    results.append((res, expr))
                                    seen.add(res)

                            # Division b / a
                            if a_val != 0 and b_val % a_val == 0:
                                res = b_val // a_val
                                expr = f"({b_str})/({a_str})"
                                if res not in seen:
                                    results.append((res, expr))
                                    seen.add(res)

        memo[key] = results
        return results

    najbolja_razlika = math.inf
    najbolja_resenja = []

    for perm in permutations(brojevi):
        initial = [(x, str(x)) for x in perm]
        for val, expr in gen_exprs(initial):
            diff = abs(val - cilj)
            if diff < najbolja_razlika:
                najbolja_razlika = diff
                najbolja_resenja = [(expr, val)]
            elif diff == najbolja_razlika:
                najbolja_resenja.append((expr, val))

    if najbolja_resenja:
        # Vrati najkraći izraz (po dužini stringa)
        najkraci = min(najbolja_resenja, key=lambda x: len(x[0]))
        cist_expr = ocisti_zagrade(najkraci[0]);
        return f"{cist_expr}={najkraci[1]}"
    return None

class GameLogic:
    def __init__(self):
        self.numbers = []
        self.target = None
        self.current_index = 0
        self.max_numbers = 6
        self.solution = None
        self.solving = False
        self.rolling_target = None
        self.target_locked = False
        self.solution = None
        self.solution_timer_duration = 60  # prvi tajmer
        self.second_timer_duration = 10    # drugi tajmer
        self.solution_timer_start = None
        self.solution_ready = False
        self.second_timer_start = None
        self.second_timer_active = False
        self.selected = [False] * 6
        self.input_text = ""
        
        # Dodato za animaciju brojeva
        self.rolling_numbers = [None] * 6
        self.locked = [False] * 6

    def toggle_selected(self, idx):
        if self.current_index > 6:  # Dozvoli selektovanje tek nakon izbora cilja
            if 0 <= idx < 6:
                self.selected[idx] = not self.selected[idx]

    def calculate_points(self):
        try:
            expr = self.input_text
            allowed = set(str(b) for b in self.numbers)
            allowed_ops = set("+-*/() ")
            for c in expr:
                if not (c in allowed_ops or c.isdigit()):
                    return 0
            value = eval(expr)
            if not isinstance(value, (int, float)) or self.target is None:
                return 0
            diff = abs(value - self.target)
            if diff == 0:
                return 30
            elif diff in (1, 2):
                return 25
            elif 3 <= diff <= 5:
                return 20
            elif 6 <= diff <= 10:
                return 15
            elif diff <= 20:
                return 10
            else:
                return 0
        except Exception:
            return 0

    def update(self):
        # Vrti samo broj u trenutnom kvadratiću koji je na redu za izbor
        if self.current_index < 6:
            i = self.current_index
            if i < 4:
                self.rolling_numbers[i] = random.randint(1, 9)
            elif i == 4:
                self.rolling_numbers[i] = random.choice([10, 15, 20])
            elif i == 5:
                self.rolling_numbers[i] = random.choice([25, 50, 75, 100])
        elif self.current_index == 6 and not self.target_locked:
            self.rolling_target = random.randint(100, 999)
        if self.solution_timer_start is not None and not self.solution_ready:
            if time.time() - self.solution_timer_start >= self.solution_timer_duration:
                self.solution_ready = True
                self.second_timer_start = time.time()
                self.second_timer_active = True
    def pick_next_number(self):
        if self.current_index < 6:
            self.locked[self.current_index] = True
            self.numbers.append(self.rolling_numbers[self.current_index])
            self.current_index += 1
        elif self.current_index == 6:
            self.target = self.rolling_target
            self.target_locked = True
            self.current_index += 1
            self.solution_ready = False
            self.solution_timer_start = time.time()
            self.start_solving_thread()

    def start_solving_thread(self):
        thread = threading.Thread(target=self.try_solve)
        thread.start()

    def try_solve(self):
        if len(self.numbers) == 6 and self.target is not None:
            resenje = najblizi_izraz(self.numbers, self.target)
            self.solution = resenje if resenje else "Nema rešenja."
        else:
            self.solution = None

    def add_number_to_expression(self, idx):
        # Dozvoli dodavanje broja samo ako je poslednji karakter u izrazu operator ili je izraz prazan
        if self.current_index > 6 and not self.selected[idx]:
            broj = str(self.numbers[idx])
            if self.input_text == "" or self.input_text[-1] in "+-*/(":
                self.input_text += broj
                self.selected[idx] = True

    def remove_number_from_expression(self, idx):
        broj = str(self.numbers[idx])
        # Ukloni broj samo ako je na kraju izraza
        if self.input_text.endswith(broj) and self.selected[idx]:
            self.input_text = self.input_text[:-len(broj)]
            self.selected[idx] = False

    def reset(self):
        self.numbers = []
        self.target = None
        self.current_index = 0
        self.solution = None
        self.rolling_target = None
        self.target_locked = False