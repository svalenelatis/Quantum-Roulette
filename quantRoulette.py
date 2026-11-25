import math

import pygame

import random_module


WIDTH = 1000
HEIGHT = 720
STARTING_MONEY = 100
SPIN_DURATION_MS = 2600
CHIP_VALUES = (1, 5, 10, 25)
BET_OPTIONS = ("Red", "Black", "Odd", "Even", "1-18", "19-36")
RED_NUMBERS = {
    1, 3, 5, 7, 9, 12, 14, 16, 18,
    19, 21, 23, 25, 27, 30, 32, 34, 36,
}
WHEEL_ORDER = (
    0, 32, 15, 19, 4, 21, 2, 25, 17, 34, 6, 27, 13, 36, 11, 30, 8, 23,
    10, 5, 24, 16, 33, 1, 20, 14, 31, 9, 22, 18, 29, 7, 28, 12, 35, 3, 26,
)

BACKGROUND = (16, 28, 29)
WHITE = (240, 244, 241)
MUTED = (174, 191, 186)
GREEN = (22, 123, 75)
RED = (177, 52, 62)
BLACK = (42, 49, 53)
DISABLED = (65, 75, 76)


def number_color(number: int) -> tuple[int, int, int]:
    if number == 0:
        return GREEN
    return RED if number in RED_NUMBERS else BLACK


def is_winning_bet(bet: str, number: int) -> bool:
    if bet == "Red":
        return number in RED_NUMBERS
    if bet == "Black":
        return number != 0 and number not in RED_NUMBERS
    if bet == "Odd":
        return number != 0 and number % 2 == 1
    if bet == "Even":
        return number != 0 and number % 2 == 0
    if bet == "1-18":
        return 1 <= number <= 18
    if bet == "19-36":
        return 19 <= number <= 36
    return False


def draw_button(
    surface: pygame.Surface,
    rect: pygame.Rect,
    label: str,
    font: pygame.font.Font,
    *,
    selected: bool = False,
    enabled: bool = True,
) -> None:
    color = DISABLED if not enabled else (GREEN if selected else (38, 57, 57))
    pygame.draw.rect(surface, color, rect, border_radius=8)
    border_color = (129, 210, 165) if selected and enabled else (73, 99, 95)
    pygame.draw.rect(surface, border_color, rect, width=2, border_radius=8)
    text = font.render(label, True, WHITE if enabled else MUTED)
    surface.blit(text, text.get_rect(center=rect.center))


def draw_wheel(
    surface: pygame.Surface,
    center: tuple[int, int],
    angle: float,
    number: int,
    spinning: bool,
    fonts: dict[str, pygame.font.Font],
) -> None:
    center_x, center_y = center
    outer_radius = 174
    label_radius = 139
    pocket_angle = 2 * math.pi / len(WHEEL_ORDER)

    for index, value in enumerate(WHEEL_ORDER):
        start = angle + index * pocket_angle - math.pi / 2
        end = start + pocket_angle
        points = [center]
        for step in range(5):
            position = start + (end - start) * step / 4
            points.append((
                round(center_x + outer_radius * math.cos(position)),
                round(center_y + outer_radius * math.sin(position)),
            ))
        pygame.draw.polygon(surface, number_color(value), points)

        label_angle = (start + end) / 2
        label_position = (
            round(center_x + label_radius * math.cos(label_angle)),
            round(center_y + label_radius * math.sin(label_angle)),
        )
        label = fonts["pocket"].render(str(value), True, WHITE)
        surface.blit(label, label.get_rect(center=label_position))

    pygame.draw.circle(surface, (211, 187, 111), center, outer_radius, width=3)
    pygame.draw.circle(surface, (18, 50, 39), center, 96)
    pygame.draw.circle(surface, (211, 187, 111), center, 96, width=2)

    result_text = fonts["result"].render(str(number), True, number_color(number))
    surface.blit(result_text, result_text.get_rect(center=(center_x, center_y - 10)))
    caption = "SPINNING" if spinning else "LAST NUMBER"
    caption_text = fonts["small"].render(caption, True, MUTED)
    surface.blit(caption_text, caption_text.get_rect(center=(center_x, center_y + 43)))


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Roulette")
    clock = pygame.time.Clock()
    rand = random_module.QuantumRNG(100, True)
    fonts = {
        "title": pygame.font.SysFont(None, 42),
        "body": pygame.font.SysFont(None, 27),
        "small": pygame.font.SysFont(None, 20),
        "button": pygame.font.SysFont(None, 24),
        "pocket": pygame.font.SysFont(None, 16),
        "result": pygame.font.SysFont(None, 68),
    }

    balance = STARTING_MONEY
    stake = 10
    selected_bet: str | None = None
    result = 0
    message = "Choose a chip and a bet, then spin."
    spinning = False
    game_over = False
    spin_started = 0
    wheel_angle = 0.0
    animation_number = 0
    animation_timer = 0

    chip_buttons = {
        value: pygame.Rect(228 + index * 138, 493, 112, 42)
        for index, value in enumerate(CHIP_VALUES)
    }
    bet_buttons = {
        bet: pygame.Rect(55 + index * 150, 550, 132, 44)
        for index, bet in enumerate(BET_OPTIONS)
    }
    spin_button = pygame.Rect(410, 620, 180, 54)

    running = True
    while running:
        delta_ms = clock.tick(60)
        now = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if spinning or game_over:
                    continue
                for value, rect in chip_buttons.items():
                    if rect.collidepoint(event.pos) and value <= balance:
                        stake = value
                        if selected_bet is not None:
                            message = f"${stake} on {selected_bet}. Press Spin when ready."
                        break
                for bet, rect in bet_buttons.items():
                    if rect.collidepoint(event.pos) and stake <= balance:
                        selected_bet = bet
                        message = f"${stake} on {bet}. Press Spin when ready."
                        break
                if spin_button.collidepoint(event.pos):
                    if selected_bet is None:
                        message = "Choose a bet before spinning."
                    elif stake > balance:
                        message = "Choose a chip you can afford."
                    else:
                        balance -= stake
                        spinning = True
                        spin_started = now
                        animation_timer = now
                        message = "The wheel is spinning..."

        if spinning:
            wheel_angle += delta_ms / 1000 * 5.5
            if now - animation_timer >= 75:
                animation_number = (animation_number + 7) % 37
                result = animation_number
                animation_timer = now

            if now - spin_started >= SPIN_DURATION_MS:
                result = rand.random(0, 36)
                spinning = False
                if is_winning_bet(selected_bet or "", result):
                    balance += stake * 2
                    message = f"{result} - You won ${stake}. Place your next bet."
                else:
                    message = f"{result} - You lost ${stake}. Place your next bet."
                    if balance == 0:
                        game_over = True
                        message = f"{result} - No money left. Game over."
                selected_bet = None
                affordable_chips = [value for value in CHIP_VALUES if value <= balance]
                if affordable_chips and stake > balance:
                    stake = max(affordable_chips)

        screen.fill(BACKGROUND)
        title = fonts["title"].render("ROULETTE", True, WHITE)
        screen.blit(title, title.get_rect(center=(WIDTH // 2, 34)))
        balance_text = fonts["body"].render(f"Money: ${balance}", True, WHITE)
        screen.blit(balance_text, balance_text.get_rect(center=(WIDTH // 2, 78)))
        message_text = fonts["small"].render(message, True, MUTED)
        screen.blit(message_text, message_text.get_rect(center=(WIDTH // 2, 112)))

        draw_wheel(
            screen, (WIDTH // 2, 294),
            wheel_angle, result, spinning, fonts,
        )

        chip_heading = fonts["small"].render("CHOOSE CHIP", True, MUTED)
        screen.blit(chip_heading, chip_heading.get_rect(center=(WIDTH // 2, 475)))
        for value, rect in chip_buttons.items():
            draw_button(
                screen,
                rect,
                f"${value}",
                fonts["button"],
                selected=stake == value,
                enabled=value <= balance and not spinning and not game_over,
            )

        bet_heading = fonts["small"].render("CHOOSE BET (PAYS 1:1)", True, MUTED)
        screen.blit(bet_heading, bet_heading.get_rect(center=(WIDTH // 2, 532)))
        for bet, rect in bet_buttons.items():
            draw_button(
                screen,
                rect,
                bet,
                fonts["button"],
                selected=selected_bet == bet,
                enabled=stake <= balance and not spinning and not game_over,
            )

        draw_button(
            screen,
            spin_button,
            "GAME OVER" if game_over else ("SPINNING..." if spinning else "SPIN"),
            fonts["button"],
            selected=not spinning and not game_over,
            enabled=selected_bet is not None and not spinning and not game_over,
        )
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()