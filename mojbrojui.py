import pygame
import threading
import time

class GameUI:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        self.font = pygame.font.Font(None, 48)
        self.target_font = pygame.font.Font(None, 64)
        self.solution_font = pygame.font.Font(None, 36)
        self.input_font = pygame.font.Font(None, 48)
        # Dugmici: lista tuple (rect, label)
        self.buttons = []
        self.button_labels = ['+', '-', '*', '/', '(', ')']
        self.button_animations = [0.0 for _ in self.button_labels]
        self.create_buttons()

    def create_buttons(self):
        # Kreiraj dugmiće na dnu ekrana
        btn_w, btn_h = 70, 60
        spacing = 30
        total_width = btn_w * len(self.button_labels) + spacing * (len(self.button_labels) - 1)
        start_x = (self.width - total_width) // 2
        y = self.height - btn_h - 30
        self.buttons = []
        for i, label in enumerate(self.button_labels):
            rect = pygame.Rect(start_x + i * (btn_w + spacing), y, btn_w, btn_h)
            self.buttons.append((rect, label))

    def draw_text_center(self, text, rect, font, color=(0, 0, 0)):
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=rect.center)
        self.screen.blit(text_surface, text_rect)

    def handle_event(self, event, game_logic=None):
            if game_logic is not None and (game_logic.current_index <= 6 or game_logic.solution_ready):
                return

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and game_logic is not None:
                # Koordinate kvadratića
                square_size = 90
                spacing = 30
                big_spacing = 70
                start_x = (self.width - (square_size * 6 + spacing * 3 + big_spacing * 2)) // 2
                y = 390 - self.height // 4
                mx, my = event.pos
                for i in range(6):
                    x = start_x + i * square_size + min(i, 3) * spacing + max(0, i - 3) * big_spacing
                    rect = pygame.Rect(x, y, square_size, square_size)
                    if rect.collidepoint(mx, my):
                        if not game_logic.selected[i]:
                            game_logic.add_number_to_expression(i)
                        elif game_logic.input_text.endswith(str(game_logic.numbers[i])):
                            game_logic.remove_number_from_expression(i)
                pos = event.pos
                for idx, (rect, label) in enumerate(self.buttons):
                    if rect.collidepoint(pos):
                        # Animacija pritiska dugmeta
                        self.button_animations[idx] = time.time()
                        expr = game_logic.input_text
                        # Dodaj operator samo ako poslednji karakter postoji i nije operator
                        if label in "+-*/":
                            if expr and (expr[-1].isdigit() or expr[-1] == ")"):
                                game_logic.input_text += label
                        # Dodaj zagradu otvaranja uvek, zagradu zatvaranja samo ako ima smisla
                        elif label == "(":
                            if not expr or expr[-1] in "+-*/(":
                                game_logic.input_text += label
                        elif label == ")":
                            if expr.count("(") > expr.count(")") and expr and (expr[-1].isdigit() or expr[-1] == ")"):
                                game_logic.input_text += label

            if event.type == pygame.KEYDOWN and game_logic is not None:
                # Dozvoli samo BACKSPACE i ENTER, ali NE dozvoli unos cifara
                if event.key == pygame.K_BACKSPACE:
                    expr = game_logic.input_text
                    if expr:
                        if not expr[-1].isdigit():
                            game_logic.input_text = expr[:-1]
                        else:
                            i = len(expr) - 1
                            while i >= 0 and expr[i].isdigit():
                                i -= 1
                            game_logic.input_text = expr[:i+1]
                            poslednji_broj = expr[i+1:]
                            for idx, broj in enumerate(game_logic.numbers):
                                if str(broj) == poslednji_broj and game_logic.selected[idx]:
                                    game_logic.selected[idx] = False
                                    break
                elif event.key == pygame.K_RETURN:
                    if game_logic.solution_timer_start is not None and not game_logic.solution_ready:
                        game_logic.solution_timer_start -= game_logic.solution_timer_duration
                # Ne dozvoli unos cifara sa tastature
                # elif event.unicode in '0123456789':
                #     pass
                elif event.unicode in '+-*/()':
                    expr = game_logic.input_text
                    label = event.unicode
                    if label in "+-*/":
                        if expr and (expr[-1].isdigit() or expr[-1] == ")"):
                            game_logic.input_text += label
                    elif label == "(":
                        if not expr or expr[-1] in "+-*/(":
                            game_logic.input_text += label
                    elif label == ")":
                        if expr.count("(") > expr.count(")") and expr and (expr[-1].isdigit() or expr[-1] == ")"):
                            game_logic.input_text += label

    def render(self, game_logic):
        self.screen.fill((230, 230, 230))

        offset_y = -self.height // 4

        # Gradient pozadina
        for y in range(self.height):
            color = (200 - y // 10, 220 - y // 20, 255 - y // 30)
            pygame.draw.line(self.screen, color, (0, y), (self.width, y))

        rect_color = (60, 60, 60)
        border_color = (30, 30, 30)

        # Tajmer linija iznad pravougaonika za cilj
        target_rect = pygame.Rect(200, 220 + offset_y, 400, 80)
        bar_y = target_rect.top - 26
        if game_logic.solution_timer_start is not None and not game_logic.solution_ready:
            total = game_logic.solution_timer_duration
            elapsed = time.time() - game_logic.solution_timer_start
            percent = max(0, min(1, 1 - elapsed / total))
            bar_width = int(640 * percent)
            r = int(255 * (1 - percent))
            g = int(255 * percent)
            b = 0
            bar_color = (r, g, b)
            bar_rect = pygame.Rect(200, bar_y, bar_width, 16)
            pygame.draw.rect(self.screen, bar_color, bar_rect, border_radius=8)
        elif game_logic.second_timer_active and game_logic.second_timer_start is not None:
            total = game_logic.second_timer_duration
            elapsed = time.time() - game_logic.second_timer_start
            percent = max(0, min(1, 1 - elapsed / total))
            bar_width = int(640 * percent)
            r = int(255 * (1 - percent))
            g = int(255 * percent)
            b = 0
            bar_color = (r, g, b)
            bar_rect = pygame.Rect(200, bar_y, bar_width, 16)
            pygame.draw.rect(self.screen, bar_color, bar_rect, border_radius=8)
        # Pravougaonik za cilj
        pygame.draw.rect(self.screen, rect_color, target_rect, border_radius=15)
        pygame.draw.rect(self.screen, border_color, target_rect, 4, border_radius=15)
        target_text = str(game_logic.rolling_target) if game_logic.rolling_target is not None else ""
        if game_logic.target is not None:
            target_text = str(game_logic.target)
        self.draw_text_center(target_text, target_rect, self.target_font, (220, 220, 220))

        # Prostor za unos rešenja
        input_rect = pygame.Rect(100, self.height - 170, self.width - 200, 60)
        pygame.draw.rect(self.screen, (245, 245, 245), input_rect, border_radius=10)
        pygame.draw.rect(self.screen, (120, 120, 120), input_rect, 2, border_radius=10)
        self.draw_text_center(game_logic.input_text, input_rect, self.input_font, (40, 40, 40))

        # Prikaz razlike nakon isteka vremena
        if game_logic.solution_ready:
            value_str = "X"
            try:
                expr = game_logic.input_text
                allowed = set(str(b) for b in game_logic.numbers)
                allowed_ops = set("+-*/() ")
                for c in expr:
                    if not (c in allowed_ops or c.isdigit()):
                        raise Exception("Nevalidan karakter")
                value = eval(expr)
                if isinstance(value, (int, float)):
                    value_str = str(int(value))
                else:
                    value_str = "X"
            except Exception:
                value_str = "X"
            # Prikaz vrednosti desno od input_rect
            value_rect = pygame.Rect(input_rect.right + 10, input_rect.top, 80, input_rect.height)
            pygame.draw.rect(self.screen, (245, 245, 245), value_rect, border_radius=10)
            pygame.draw.rect(self.screen, (120, 120, 120), value_rect, 2, border_radius=10)
            self.draw_text_center(value_str, value_rect, self.input_font, (30, 120, 30))

        # Kvadratići sa brojevima
        square_size = 90
        spacing = 30
        big_spacing = 70
        start_x = (self.width - (square_size * 6 + spacing * 3 + big_spacing * 2)) // 2
        y = 390 + offset_y
        
        for i in range(6):
            x = start_x + i * square_size + min(i, 3) * spacing + max(0, i - 3) * big_spacing
            rect = pygame.Rect(x, y, square_size, square_size)
            pygame.draw.rect(self.screen, (255, 255, 255), rect, border_radius=10)
            pygame.draw.rect(self.screen, border_color, rect, 3, border_radius=10)
            if hasattr(game_logic, "selected") and game_logic.selected[i] and game_logic.current_index > 6:
                pygame.draw.rect(self.screen, (180, 180, 180), rect, border_radius=10)  # Siva pozadina
            else:
                pygame.draw.rect(self.screen, (255, 255, 255), rect, border_radius=10)
            pygame.draw.rect(self.screen, border_color, rect, 3, border_radius=10)
            if i < len(game_logic.numbers):
                self.draw_text_center(str(game_logic.numbers[i]), rect, self.font)
            elif game_logic.rolling_numbers[i] is not None:
                self.draw_text_center(str(game_logic.rolling_numbers[i]), rect, self.font, (180, 180, 180))

        # Dugmići na dnu
        anim_duration = 0.18  # trajanje animacije u sekundama
        for idx, (rect, label) in enumerate(self.buttons):
            center = rect.center
            radius = rect.width // 2

            # Animacija: ako je dugme skoro pritisnuto, malo ga smanji i potamni
            scale = 1.0
            color_boost = 1.0
            if self.button_animations[idx] > 0:
                elapsed = time.time() - self.button_animations[idx]
                if elapsed < anim_duration:
                    scale = 0.92 + 0.08 * (1 - elapsed / anim_duration)
                    color_boost = 0.85 + 0.15 * (elapsed / anim_duration)
                else:
                    self.button_animations[idx] = 0.0

            # Preračunaj centar i poluprečnik za animaciju
            draw_radius = int(radius * scale)
            draw_center = center

            # Senka
            shadow_offset = int(5 * scale)
            pygame.draw.circle(self.screen, (180, 180, 180), (draw_center[0] + shadow_offset, draw_center[1] + shadow_offset), draw_radius)

            # Gradijent (od svetlo plave do bele)
            grad_color1 = tuple(int(c * color_boost) for c in (210, 220, 255))
            grad_color2 = tuple(int(c * color_boost) for c in (240, 240, 255))
            for r in range(draw_radius, 0, -1):
                ratio = r / draw_radius
                color = (
                    int(grad_color1[0] * ratio + grad_color2[0] * (1 - ratio)),
                    int(grad_color1[1] * ratio + grad_color2[1] * (1 - ratio)),
                    int(grad_color1[2] * ratio + grad_color2[2] * (1 - ratio)),
                )
                pygame.draw.circle(self.screen, color, draw_center, r)

            # Tamni okvir
            pygame.draw.circle(self.screen, (60, 90, 160), draw_center, draw_radius, 4)

            # Labela
            self.draw_text_center(label, pygame.Rect(draw_center[0] - draw_radius, draw_center[1] - draw_radius, 2 * draw_radius, 2 * draw_radius), self.font, (30, 40, 80))
        # Prikaz rešenja (takođe pomereno na gore)
        solution_rect = pygame.Rect(50, 520 + offset_y, self.width - 100, 70)
        if game_logic.solution_ready and game_logic.solution:
            self.draw_text_center(game_logic.solution, solution_rect, self.solution_font, (200, 0, 0))

        pygame.display.flip()