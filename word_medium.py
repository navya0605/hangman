import pygame
import random
from medium import word_medium

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 1000, 800
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hangman Game")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Timer setting
TIME_LIMIT = 3 * 60 * 1000  # 5 minutes in milliseconds

# Load and scale the background image
background_image = pygame.image.load('static/img/word.png')
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
background_image.set_alpha(90)

def draw_hangman(win, attempts):
    pygame.draw.line(win, BLACK, (500, 600), (800, 600), 5)  # Base
    pygame.draw.line(win, BLACK, (700, 600), (700, 250), 5)  # Pole
    pygame.draw.line(win, BLACK, (700, 250), (500, 250), 5)  # Beam
    pygame.draw.line(win, BLACK, (500, 250), (500, 300), 5)  # Rope

    if attempts >= 1:
        pygame.draw.circle(win, BLACK, (500, 330), 40, 5)  # Head
    if attempts >= 2:
        pygame.draw.line(win, BLACK, (500, 370), (500, 500), 5)  # Body
    if attempts >= 3:
        pygame.draw.line(win, BLACK, (500, 400), (450, 450), 5)  # Left Arm
    if attempts >= 4:
        pygame.draw.line(win, BLACK, (500, 400), (550, 450), 5)  # Right Arm
    if attempts >= 5:
        pygame.draw.line(win, BLACK, (500, 500), (450, 550), 5)  # Left Leg
    if attempts >= 6:
        pygame.draw.line(win, BLACK, (500, 500), (550, 550), 5)  # Right Leg

def draw_text(win, text, font, color, center):
    rendered_text = font.render(text, True, color)
    text_rect = rendered_text.get_rect(center=center)
    win.blit(rendered_text, text_rect)

def display_word(win, word, guessed):
    font = pygame.font.SysFont(None, 50)
    display_text = ' '.join(guessed)
    draw_text(win, display_text, font, BLACK, (WIDTH // 2, HEIGHT - 100))

def display_score_timer(win, score, remaining_time):
    font_score = pygame.font.SysFont(None, 50)
    font_timer = pygame.font.SysFont(None, 50)

    score_text = f"Score: {score}"
    draw_text(win, score_text, font_score, BLACK, (100, 70))

    minutes = remaining_time // 60000
    seconds = (remaining_time % 60000) // 1000
    timer_text = f"Time Left: {minutes}:{seconds:02}"
    draw_text(win, timer_text, font_timer, BLACK, (WIDTH - 270, 70))

def wrap_text(text, font, max_width):
    words = text.split(' ')
    lines = []
    current_line = []

    for word in words:
        test_line = ' '.join(current_line + [word])
        if font.size(test_line)[0] <= max_width:
            current_line.append(word)
        else:
            lines.append(' '.join(current_line))
            current_line = [word]

    lines.append(' '.join(current_line))
    return lines

def run_game():
    global win

    # Load words from the dictionary
    available_words = list(word_medium.keys())
    total_words = len(available_words)
    used_words = []
    score = 0

    # Start the timer
    start_time = pygame.time.get_ticks()

    # Main game loop
    while available_words:
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - start_time
        remaining_time = TIME_LIMIT - elapsed_time

        if remaining_time <= 0:
            break  # Time is up, exit the game loop

        word = random.choice(available_words)
        available_words.remove(word)
        used_words.append(word)

        guessed = ['_' for _ in word]
        attempts = 0
        correct = False
        guessed_letters = set()
        hint = word_medium[word]

        # Main word guessing loop
        while True:
            current_time = pygame.time.get_ticks()
            elapsed_time = current_time - start_time
            remaining_time = TIME_LIMIT - elapsed_time

            if remaining_time <= 0:
                break  # Time is up, exit the word guessing loop

            win.fill(WHITE)
            win.blit(background_image, (0, 0))
            draw_hangman(win, attempts)
            display_word(win, word, guessed)
            display_score_timer(win, score, remaining_time)

            # Display the hint above the guessed word
            font_hint = pygame.font.SysFont(None, 40)
            wrapped_hint = wrap_text(hint, font_hint, WIDTH - 40)
            for i, line in enumerate(wrapped_hint):
                draw_text(win, line, font_hint, BLACK, (WIDTH // 2, HEIGHT - 600 - (30 * len(wrapped_hint)) + (30 * i)))

            pygame.display.update()

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif event.type == pygame.KEYDOWN:
                    if pygame.K_a <= event.key <= pygame.K_z:
                        letter = chr(event.key).upper()
                        if letter not in guessed_letters:
                            guessed_letters.add(letter)
                            if letter in word:
                                for i in range(len(word)):
                                    if word[i] == letter:
                                        guessed[i] = letter
                                if '_' not in guessed:
                                    correct = True
                                    score += 1
                                    break
                            else:
                                attempts += 1

            if correct or attempts == 6:
                pygame.time.delay(2000)
                break

        # Reveal the word after guess
        win.fill(WHITE)
        win.blit(background_image, (0, 0))
        display_word(win, word, word)
        pygame.display.update()
        pygame.time.delay(2000)

    # Calculate score percentage
    score_percentage = (score / total_words) * 100

    # Level complete or fail message
    win.fill(WHITE)
    win.blit(background_image, (0, 0))
    font = pygame.font.SysFont(None, 100)

    if score_percentage >= 50:
        text = 'Level Complete!'
    else:
        text = 'Level Fail!'

    draw_text(win, text, font, BLACK, (WIDTH // 2, HEIGHT // 2 - 50))
    final_score_text = f"Final Score: {score}/{total_words}"
    draw_text(win, final_score_text, pygame.font.SysFont(None, 50), BLACK, (WIDTH // 2, HEIGHT // 2 + 50))
    pygame.display.update()

    # Keep the window open for a while to show the final score
    pygame.time.delay(5000)

    # Final loop to handle quitting
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

if __name__ == "__main__":
    run_game()


