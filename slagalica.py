from __future__ import annotations

import os
import random
import re
import time
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import pygame
import pygame.freetype

WIDTH, HEIGHT = 1280, 800
FPS = 60

kolona = 6
br_slova = 12
polje_w, polje_h = 110, 90
polje_xrazmak, polje_yrazmak = 18, 18
PLAY_TIME = 60.0

BG = (18, 20, 26)
PANEL = (28, 32, 40)
PANEL_2 = (38, 44, 56)
TEXT = (236, 240, 245)
MUTED = (170, 176, 186)
ACCENT = (89, 166, 255)
GREEN = (66, 183, 107)
RED = (219, 92, 92)
YELLOW = (230, 184, 74)
USED = (118, 125, 138)
WHITE = (250, 250, 250)

slova = [
    "a", "b", "c", "č", "ć", "d", "dž", "đ", "e", "f",
    "g", "h", "i", "j", "k", "l", "lj", "m", "n", "nj",
    "o", "p", "r", "s", "š", "t", "u", "v", "z", "ž",
]

ALL_TOKENS = sorted(slova, key=len, reverse=True)


@dataclass
class polje:
    token: str
    rect: pygame.Rect
    used: int = 0


def tokenize_sr(text: str) -> Optional[list[str]]:
    s = text.lower().strip()
    if not s:
        return []
    tokens: list[str] = []
    i = 0
    while i < len(s):
        matched = None
        for tok in ALL_TOKENS:
            if s.startswith(tok, i):
                matched = tok
                break
        if matched is None:
            return None
        tokens.append(matched)
        i += len(matched)
    return tokens


class SerbianDictionary:
    def __init__(self):
        
        self.words = self._load_words()
        if not self.words:
            self.words = {
                "molim", "vas", "pozovite", "me", "na", "acts"
            }

    def _load_words(self) -> set[str]:
        candidates: list[Path] = []
        env_path = os.getenv("SR_WORDLIST", "").strip()
        if env_path:
            candidates.append(Path(env_path))

        candidates.extend([
            Path("sr-Latn.dic"),
        ])

        for path in candidates:
            if not path.exists() or not path.is_file():
                continue

            loaded: set[str] = set()
            try:
                with path.open("r", encoding="utf-8", errors="ignore") as f:
                    for i, raw in enumerate(f):
                        line = raw.strip().lower()
                        if not line:
                            continue
                        if i == 0 and line.isdigit():
                            continue
                        if line.startswith("#") or line.startswith("//"):
                            continue
                        word = line.split()[0]
                        word = word.split("/")[0]
                        word = re.sub(r"[^a-zčćđšž]+", "", word)
                        if not word:
                            continue
                        if tokenize_sr(word) is None:
                            continue
                        loaded.add(word)
            except Exception:
                continue

            if loaded:
                return loaded

        return set()

    def valid(self, word: str) -> bool:
        w = word.lower().strip()
        if not w:
            return False
        if tokenize_sr(w) is None:
            return False
        return w in self.words

    def moguce(self, word: str) -> bool:
        return self.valid(word)

    def best_word(self, available_tokens: list[str]) -> str:
        available = Counter(available_tokens)
        best = ""
        best_len = 0

        for word in self.words:
            toks = tokenize_sr(word)
            if toks is None:
                continue

            need = Counter(toks)
            if any(need[t] > available[t] for t in need):
                continue

            n = len(toks)
            if n > best_len or (n == best_len and len(word) > len(best)):
                best = word
                best_len = n

        return best

    def najbolja_rec(self, available_tokens: list[str]) -> str:
        return self.best_word(available_tokens)


class Game:
    def __init__(self):
        pygame.init()
        pygame.freetype.init()
        
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("slagalica")
        self.clock = pygame.time.Clock()
        
        self.font_small = pygame.freetype.SysFont("DejaVu Sans", 22)
        self.font_med = pygame.freetype.SysFont("DejaVu Sans", 28)
        self.font_tile = pygame.freetype.SysFont("DejaVu Sans", 32)
        self.font_word = pygame.freetype.SysFont("DejaVu Sans", 36)
        self.font_big = pygame.freetype.SysFont("DejaVu Sans", 40)

        self.polja: list[polje] = []
        self.selection: list[int] = []

        self.faza = 1
        self.revealed = 0
        self.start_time: Optional[float] = None
        self.running = 1

        self.dictionary = SerbianDictionary()

        self.prihvatljiva_rec = 0
        self.krajnja_rec = ""
        self.igrac_rec = ""
        self.poeni = 0

        self._make_layout()

    def _make_layout(self):
        grid_w = kolona * polje_w + (kolona - 1) * polje_xrazmak
        grid_h = 2 * polje_h + (1 * polje_yrazmak)

        self.grid_x = (WIDTH - grid_w) // 2
        self.grid_y = 290

        self.word_box = pygame.Rect(250, 160, 700, 70)
        self.timer = pygame.Rect(250, 80, 760, 24)

        self.polja = []
        for i in range(br_slova):
            r = i // kolona
            c = i % kolona
            x = self.grid_x + c * (polje_w + polje_xrazmak)
            y = self.grid_y + r * (polje_h + polje_yrazmak)
            self.polja.append(polje("", pygame.Rect(x, y, polje_w, polje_h)))

    def reveal(self):
        if self.revealed >= br_slova:
            return
        self.polja[self.revealed].token = random.choice(slova)
        self.revealed += 1

        if self.revealed == br_slova:
            self.faza = 2
            self.start_time = time.time()

    def word(self):
        return "".join(self.polja[i].token for i in self.selection)

    def add(self, i):
        t = self.polja[i]
        if t.used or not t.token:
            return
        t.used = True
        self.selection.append(i)
        self.prihvatljiva_rec = self.dictionary.moguce(self.word())

    def back(self):
        if not self.selection:
            return
        i = self.selection.pop()
        self.polja[i].used = 0
        self.prihvatljiva_rec = self.dictionary.moguce(self.word())

    def time_left(self):
        if self.start_time is None:
            return PLAY_TIME
        return max(0.0, PLAY_TIME - (time.time() - self.start_time))

    def finish_round(self):
        available = [t.token for t in self.polja if t.token]

        player_word = self.word()
        self.igrac_rec = player_word
        tokens = tokenize_sr(player_word)

        if self.dictionary.moguce(player_word) and tokens:
            self.poeni = 2 * len(tokens)
        else:
            self.poeni = 0

        self.krajnja_rec = self.dictionary.najbolja_rec(available)
        self.faza = 3

    def update(self):
        if self.faza == 2 and self.time_left() <= 0:
            self.finish_round()

    def draw_center_text(self, font, text, x, y, color):
        surf, rect = font.render(text, fgcolor=color)
        rect.center = (x, y)
        self.screen.blit(surf, rect)

    def draw(self):
        self.screen.fill(BG)

        if self.faza in (1, 2):
            pygame.draw.rect(self.screen, PANEL, self.timer, border_radius=10)
            if self.faza == 2:
                fill = self.timer.copy()
                fill.width = int(self.timer.width * (1 - self.time_left() / PLAY_TIME))
                pygame.draw.rect(self.screen, GREEN, fill, border_radius=10)

            self.draw_center_text(self.font_big, "SLAGALICA", WIDTH // 2, 40, TEXT)

            pygame.draw.rect(self.screen, PANEL, self.word_box, border_radius=12)
            word_surf, word_rect = self.font_word.render(self.word(), fgcolor=WHITE)
            word_rect.center = self.word_box.center
            self.screen.blit(word_surf, word_rect)

            color = GREEN if self.prihvatljiva_rec else RED if self.word() else YELLOW
            pygame.draw.circle(self.screen, color, (WIDTH - 120, 360), 40)

            for t in self.polja:
                pygame.draw.rect(
                    self.screen,
                    PANEL_2 if not t.used else USED,
                    t.rect,
                    border_radius=10,
                )
                pygame.draw.rect(self.screen, ACCENT, t.rect, 2, border_radius=10)

                if t.token:
                    surf, rect = self.font_tile.render(t.token.upper(), fgcolor=WHITE)
                    rect.center = t.rect.center
                    self.screen.blit(surf, rect)

            hint = "Razmak dugme bira slova" if self.faza == 1 else "Dodirom se biraju slova, backspace briše poslednje"
            hint_surf, hint_rect = self.font_small.render(hint, fgcolor=MUTED)
            hint_rect.center = (WIDTH // 2, 760)
            self.screen.blit(hint_surf, hint_rect)

        else:
            panel = pygame.Rect(160, 170, 960, 420)
            pygame.draw.rect(self.screen, PANEL, panel, border_radius=18)
            pygame.draw.rect(self.screen, ACCENT, panel, 2, border_radius=18)

            self.draw_center_text(self.font_big, "slagalica", WIDTH // 2, 225, TEXT)
            self.font_med.render_to(self.screen, (panel.x + 60, panel.y + 120), "Vreme je isteklo.", TEXT)
            y0 = panel.y + 120
            step = 55

            self.font_med.render_to(
                self.screen,
                (panel.x + 60, y0 + step * 0),
                "Vreme je isteklo.",
                TEXT,
            )

            self.font_med.render_to(
                self.screen,
                (panel.x + 60, y0 + step * 1),
                f"Vaša reč: {self.igrac_rec or 'ne postoji'}",
                TEXT,
            )

            self.font_med.render_to(
                self.screen,
                (panel.x + 60, y0 + step * 2),
                f"Najduža prihvatljiva reč: {self.krajnja_rec or 'ne postoji'}",
                TEXT,
            )

            self.font_med.render_to(
                self.screen,
                (panel.x + 60, y0 + step * 3),
                f"Osvojili ste {self.poeni} poena.",
                TEXT,
            )

            self.font_small.render_to(
                self.screen,
                (panel.x + 60, y0 + step * 4),
                "Pritisni razmak da zatvoriš igru.",
                MUTED,
            )

        pygame.display.flip()

    def run(self):
        while self.running:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    self.running = 0

                elif e.type == pygame.KEYDOWN:
                    if self.faza == 3:
                        self.running = 0
                    elif self.faza == 1 and e.key == pygame.K_SPACE:
                        self.reveal()
                    elif self.faza == 2 and e.key in (pygame.K_BACKSPACE, pygame.K_DELETE):
                        self.back()

                elif e.type == pygame.MOUSEBUTTONDOWN and self.faza == 2:
                    for i, t in enumerate(self.polja):
                        if t.rect.collidepoint(e.pos):
                            self.add(i)
                            break

            self.update()
            self.draw()
            self.clock.tick(FPS)

        pygame.quit()


if __name__ == "__main__":
    Game().run()
