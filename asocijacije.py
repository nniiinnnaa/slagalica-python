import pygame as pg
import sys
import random
import time
import globala

pg.init()

WIDTH = 1280
HEIGTH = 720

BACKGROUND = (100, 160, 240)

screen = pg.display.set_mode((WIDTH, HEIGTH))
screen.fill(BACKGROUND)
clock = pg.time.Clock()
dt = 0

# --- KONFIGURACIJA ---
SCREEN_WIDTH, SCREEN_HEIGHT = WIDTH, HEIGTH
RECT_WIDTH, RECT_HEIGHT = 260, 40
MARGIN = 80
SPACING = 10
CENTER_RECT_WIDTH, CENTER_RECT_HEIGHT = 120, 40
ROUND_TIME = 180  # 3 minuta u sekundama
PAUSE_BETWEEN_ROUNDS = 3  # sekunde

def get_quad_positions():
    positions = []
    qx, qy = MARGIN, MARGIN
    for i in range(4):
        positions.append((qx, qy + i * (RECT_HEIGHT + SPACING)))
    qx = SCREEN_WIDTH - RECT_WIDTH - MARGIN
    qy = MARGIN
    for i in range(4):
        positions.append((qx, qy + i * (RECT_HEIGHT + SPACING)))
    qx = MARGIN
    qy = SCREEN_HEIGHT - 4 * (RECT_HEIGHT + SPACING) - MARGIN
    for i in range(4):
        positions.append((qx, qy + i * (RECT_HEIGHT + SPACING)))
    qx = SCREEN_WIDTH - RECT_WIDTH - MARGIN
    qy = SCREEN_HEIGHT - 4 * (RECT_HEIGHT + SPACING) - MARGIN
    for i in range(4):
        positions.append((qx, qy + i * (RECT_HEIGHT + SPACING)))
    return positions

def get_center_positions():
    center_x = SCREEN_WIDTH // 2
    center_y = SCREEN_HEIGHT // 2
    offset_distance_x = 110
    offset_distance_y = 70
    separation = 60
    offsets = [
        (-offset_distance_x - separation//2, -offset_distance_y),
        (offset_distance_x - CENTER_RECT_WIDTH + separation//2, -offset_distance_y),
        (-offset_distance_x - separation//2, offset_distance_y - 40),
        (offset_distance_x - CENTER_RECT_WIDTH + separation//2, offset_distance_y - 40),
    ]
    positions = []
    for dx, dy in offsets:
        positions.append((center_x + dx, center_y + dy))
    return positions

def get_final_position():
    center_x = SCREEN_WIDTH // 2
    center_y = SCREEN_HEIGHT // 2
    return (center_x - CENTER_RECT_WIDTH//2, center_y - CENTER_RECT_HEIGHT//2)

# --- BAZA ASOCIJACIJA ---
asocijacije_baza = [
    [
        "POL", "DINAMO", "FLUKS", "GVOŽĐE",
        "KRV", "ŽILA", "PROŠIRENJE", "NOGA",
        "IBRIŠIM", "MAŠINA", "NIT", "MAK",
        "MUZIKA", "TRUBA", "ZVUK", "PLOČA",
        "MAGNET", "VENA", "KONAC", "GRAMOFON",
        "IGLA"
    ],
    [
        "KOMANDA", "ORGAN", "GLAVA", "KORA",
        "KRALJ", "NASLEDNIK", "BELI KONJ", "MUZIČAR",
        "KUPUJEM", "PRODAJEM", "HALO", "SVAŠTARA",
        "ŠAKA", "PRSTEN", "PALAC", "SUDBINA",
        "MOZAK", "PRINC", "OGLASI", "PRST",
        "MALI"
    ],
    [
        "DIJAMANT", "KAMEN", "SAFIR", "ŽAD",
        "PLOMBA", "KOREN", "ŽIVAC", "PASTA",
        "FILM", "MAGAZIN", "OČEVIDAC", "SUD",
        "ELVIS", "PALATA", "ŠAH", "VLADAR",
        "DRAGULJ", "ZUB", "SVEDOK", "KRALJ",
        "KRUNA"
    ],
    [
        "INSEKT", "SIGNAL", "KROV", "PRIJEM",
        "RUKAVICA", "DVOBOJ", "PROTIVNICI", "DETERDŽENT",
        "OCENA", "KNJIGA", "UVREDA", "BROD",
        "ZRAČENJE", "OPSTANAK", "RADIO", "UŽIVO",
        "ANTENA", "DUEL", "DNEVNIK", "EMISIJA",
        "TV"
    ],
    [
        "ŠLJUNAK", "CEMENT", "VODA", "ARMATURA",
        "PORODICA", "PAS", "MODA", "PROZORI",
        "ZVUČNICI", "IGLA", "GLAS", "KUTIJA",
        "UGLJENIK", "ORGLICA", "TVRD", "NAKIT",
        "BETON", "KUĆA", "GRAMOFON", "DIJAMANT",
        "PLOČA"
    ],
    [
        "PROJEKAT", "OSTRVO", "VOL STRIT", "NJUJORK",
        "EGIPAT", "NIL", "GRAD", "GLAVNI",
        "CVET", "IME", "CRVENA", "VETAR",
        "KOŠARKA", "JUŽNO VOĆE", "KORA", "MAJMUN",
        "MENHETN", "KAIRO", "RUŽA", "BANANE",
        "VUDI ALEN"
    ],
    [
        "GEOMETRIJA", "STAN", "POVRŠINA", "O = 4 x A",
        "NAPOR", "A = P x T", "1. MAJ", "KNJIŽICA",
        "VITKA", "PUNA", "KRIVA", "PRAVA",
        "VIŠA", "OSNOVNA", "AUTO", "ĐACI",
        "KVADRAT", "RAD", "LINIJA", "ŠKOLA",
        "SVESKA"
    ],
    [
        "DIM", "PEPEO", "POŽAR", "PLAMEN",
        "PI", "OBIM", "PREČNIK", "EKV",
        "STOČARSTVO", "LEPŠE OD PARIZA", "MOKRIN", "POLJOPRIVREDA",
        "ŠAH", "NERVI", "KOMPJUTERSKA", "DRUŠTVENA",
        "VATRA", "KRUG", "SELO", "IGRA",
        "OLIMPIJADA"
    ],
    [
        "KINA", "SUV", "PRAH", "MUSKETA",
        "KORAN", "STABLO", "HRAST", "JAVOR",
        "SARMA", "KISELI", "SALATA", "GLAVA",
        "ŠPRICER", "STAKLO", "PODRUM", "GROŽĐE",
        "BARUT", "DRVO", "KUPUS", "VINO",
        "BURE"
    ],
    [
        "ŠTAMPA", "NOVINARI", "ISTOČNA", "ZAPADNA",
        "EVROPA", "DRŽAVA", "PECIVO", "POLUOSTRVO",
        "TROPSKA", "KONTINENTALNA", "PROMENE", "POJAS",
        "ZVUK", "MALA", "AUTOMOBIL", "FABRIKA",
        "KONFERENCIJA", "DANSKA", "KLIMA", "SIRENA",
        "KOPENHAGEN"
    ],
    [
        "UŠĆE", "NOVI", "ADA", "SRBIJA",
        "KOPANJE", "ZLATO", "BOR", "PATULJCI",
        "KRIVI", "SVETIONIK", "PARIZ", "PIZA",
        "KANAL", "ANTENA", "PROGRAM", "STANICA",
        "BEOGRAD", "RUDNIK", "TORANJ", "TV",
        "AVALA"
    ],
    [
        "BRAŠNO", "ŽITARICA", "PROJA", "KLIP",
        "RAZDOR", "BILJKA", "KLICA", "NS",
        "PLAŽA", "MATERIJAL", "BUBREG", "PUSTINJA",
        "SUPA", "ZAČIN", "CRNI", "LJUTINA",
        "KUKURUZ", "SEME", "PESAK", "BIBER",
        "ZRNO"
    ],
]
quad_labels = [
    "A1", "A2", "A3", "A4",
    "B1", "B2", "B3", "B4",
    "C1", "C2", "C3", "C4",
    "D1", "D2", "D3", "D4"
]
center_labels = ["A", "B", "C", "D"]
final_label = "KONAČNO"

font = pg.font.SysFont('Arial', 24)

def draw_board(board, revealed, quad_positions, center_positions, final_position):
    # Kvadrantna polja
    for idx, (rx, ry) in enumerate(quad_positions):
        color = (144, 238, 144) if revealed[idx] else (255, 255, 255)
        rect = pg.Rect(rx, ry, RECT_WIDTH, RECT_HEIGHT)
        pg.draw.rect(screen, color, rect, 0)
        pg.draw.rect(screen, (0, 0, 0), rect, 2)
        if revealed[idx]:
            text = font.render(board[idx], True, (0, 0, 0))
        else:
            text = font.render(quad_labels[idx], True, (100, 100, 100))
        text_rect = text.get_rect(center=rect.center)
        screen.blit(text, text_rect)

    # Središnja polja
    for i, (rx, ry) in enumerate(center_positions):
        idx = 16 + i
        color = (144, 238, 144) if revealed[idx] else (200, 200, 255)
        rect = pg.Rect(rx, ry, CENTER_RECT_WIDTH, CENTER_RECT_HEIGHT)
        pg.draw.rect(screen, color, rect, 0)
        pg.draw.rect(screen, (0, 0, 0), rect, 2)
        if revealed[idx]:
            text = font.render(board[idx], True, (0, 0, 128))
        else:
            text = font.render(center_labels[i], True, (80, 80, 160))
        text_rect = text.get_rect(center=rect.center)
        screen.blit(text, text_rect)

    # Konačno polje
    rx, ry = final_position
    color = (255, 255, 128) if revealed[20] else (255, 255, 0)
    rect = pg.Rect(rx, ry, CENTER_RECT_WIDTH, CENTER_RECT_HEIGHT)
    pg.draw.rect(screen, color, rect, 0)
    pg.draw.rect(screen, (0, 0, 0), rect, 2)
    if revealed[20]:
        text = font.render(board[20], True, (128, 64, 0))
    else:
        text = font.render(final_label, True, (128, 64, 0))
    text_rect = text.get_rect(center=rect.center)
    screen.blit(text, text_rect)

def asocijacije():
    global dt, clock, screen
    brojpoena = 2100
    # Izaberi nasumičnu asocijaciju
    words = random.choice(asocijacije_baza)
    board = [""] * 21
    revealed = [False] * 21
    quad_positions = get_quad_positions()
    center_positions = get_center_positions()
    final_position = get_final_position()
    selected_input = None
    input_text = ""
    message = ""
    round_start = time.time()
    finished = False

    while not finished:
        screen.fill(BACKGROUND)
        draw_board(board, revealed, quad_positions, center_positions, final_position)

        # Prikaz unosa i poruke
        if selected_input is not None:
            font2 = pg.font.SysFont('Arial', 28)
            txt = font2.render("Unos: " + input_text, True, (0, 0, 0))
            screen.blit(txt, (20, SCREEN_HEIGHT - 60))
        if message:
            font2 = pg.font.SysFont('Arial', 24)
            txt = font2.render(message, True, (255, 255, 255))
            screen.blit(txt, (20, screen.get_height() - 30))

        # Prikaz vremena
        elapsed = time.time() - round_start
        vreme = max(0, int(ROUND_TIME - elapsed))
        min_str = str(vreme // 60).zfill(2)
        sec_str = str(vreme % 60).zfill(2)
        timer_txt = font.render(f"Vreme: {min_str}:{sec_str}", True, (255, 255, 255))
        screen.blit(timer_txt, (SCREEN_WIDTH - 180, 20))

        # Prikaz poena
        points_txt = font.render(f"Poeni: {brojpoena}", True, (255, 255, 255))
        screen.blit(points_txt, (20, 20))

        pg.display.flip()

        mouse = {
            "x": pg.mouse.get_pos()[0],
            "y": pg.mouse.get_pos()[1],
            "left": pg.mouse.get_pressed()[0],
            "right": pg.mouse.get_pressed()[2]
        }

        for event in pg.event.get():
            if event.type == pg.QUIT:
                finished = True
                globala.stop()
                pg.quit()
                sys.exit()
                return brojpoena
            if event.type == pg.MOUSEBUTTONUP:
                x = mouse['x']
                y = mouse['y']
                found = False
                # Kvadrantna polja
                for idx, (rx, ry) in enumerate(quad_positions):
                    rect = pg.Rect(rx, ry, RECT_WIDTH, RECT_HEIGHT)
                    if rect.collidepoint(x, y):
                        if not revealed[idx]:
                            revealed[idx] = True
                            board[idx] = words[idx]
                            brojpoena -= 100  # Svako kvadrantsko polje 100 poena
                        found = True
                        selected_input = None
                        break
                # Središnja polja
                if not found:
                    for i, (rx, ry) in enumerate(center_positions):
                        rect = pg.Rect(rx, ry, CENTER_RECT_WIDTH, CENTER_RECT_HEIGHT)
                        group = i
                        if rect.collidepoint(x, y):
                            if any(revealed[group * 4 + j] for j in range(4)):
                                selected_input = 16 + i
                                input_text = ""
                                message = "Unesi reč za ovo polje i pritisni Enter."
                            else:
                                message = "Prvo otvori bar jedno polje u ovom kvadrantu!"
                            found = True
                            break
                # Konačno polje
                if not found:
                    rx, ry = final_position
                    rect = pg.Rect(rx, ry, CENTER_RECT_WIDTH, CENTER_RECT_HEIGHT)
                    if rect.collidepoint(x, y):
                        if any(revealed[16 + j] for j in range(4)):
                            selected_input = 20
                            input_text = ""
                            message = "Unesi reč za konačno polje i pritisni Enter."
                        else:
                            message = "Prvo otvori bar jedno središnje polje!"

            if event.type == pg.KEYDOWN:
                if selected_input is not None:
                    if event.key == pg.K_RETURN:
                        idx = selected_input
                        if input_text.strip().lower() == words[idx].lower():
                            revealed[idx] = True
                            board[idx] = words[idx]
                            # Središnja polja
                            if 16 <= idx <= 19:
                                group = idx - 16
                                unlocked = sum(revealed[group * 4 + i] for i in range(4))
                                poeni = 100 * (4 - unlocked)
                                brojpoena += poeni
                                message = f"Tačno! (+{poeni} poena)"
                                for i in range(4):
                                    quad_idx = group * 4 + i
                                    if not revealed[quad_idx]:
                                        revealed[quad_idx] = True
                                        board[quad_idx] = words[quad_idx]
                            # Konačno polje
                            elif idx == 20:
                                if not any(revealed[16 + j] for j in range(4)):
                                    unlocked = sum(revealed[:20])
                                    poeni = (20 - unlocked) * 100
                                    brojpoena += poeni
                                    message = f"Konačno rešenje! (+{poeni} poena)"
                                else:
                                    message = "Konačno rešenje!"
                                for i in range(21):
                                    revealed[i] = True
                                    board[i] = words[i]
                                finished = True
                            else:
                                message = "Tačno!"
                            selected_input = None
                        else:
                            message = "Pokušaj ponovo!"
                        input_text = ""
                    elif event.key == pg.K_BACKSPACE:
                        input_text = input_text[:-1]
                    else:
                        char = event.unicode
                        if char.isprintable():
                            input_text += char

        # Provera vremena
        elapsed = time.time() - round_start
        if elapsed > ROUND_TIME:
            for i in range(21):
                revealed[i] = True
                board[i] = words[i]
            message = "Vreme isteklo!"
            finished = True

        dt += clock.tick(60) / 1000
    return brojpoena


if __name__ == '__main__':
    brojpoena = asocijacije()
    print(brojpoena)
