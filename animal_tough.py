import os
import pygame
import random
from tough import animals_tough

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
TIME_LIMIT = 1 * 60 * 1000  # 2 minutes in milliseconds

# Load and scale the background image
background_image = pygame.image.load('static/img/animals.png')
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
background_image.set_alpha(90)

def run_game():
    global win

    # Load words from a text file
    available_words = list(animals_tough.keys())
    total_words = len(available_words)
    used_words = []
    score = 0

    # Score and timer text
    font_score = pygame.font.SysFont(None, 50)
    font_timer = pygame.font.SysFont(None, 50)

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

        # Load the image associated with the word
        image_filename = animals_tough[word]
        image_path = os.path.join(os.getcwd(), image_filename)
        image = pygame.image.load(image_path)

        # Resize the image to fit the window
        image = pygame.transform.scale(image, (200, 200))

        # Main word guessing loop
        while True:
            current_time = pygame.time.get_ticks()
            elapsed_time = current_time - start_time
            remaining_time = TIME_LIMIT - elapsed_time

            if remaining_time <= 0:
                break  # Time is up, exit the word guessing loop

            win.fill(WHITE)
            win.blit(background_image, (0, 0))

            # Draw hangman
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

            # Draw the word
            font = pygame.font.SysFont(None, 50)
            text = font.render(' '.join(guessed), True, BLACK)
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT - 100))
            win.blit(text, text_rect)

            # Draw the image
            win.blit(image, (100, 250))

            # Draw the score
            score_text = font_score.render(f"Score: {score}", True, BLACK)
            win.blit(score_text, (60, 60))

            # Draw the timer
            minutes = remaining_time // 60000
            seconds = (remaining_time % 60000) // 1000
            timer_text = font_timer.render(f"Time Left: {minutes}:{seconds:02}", True, BLACK)
            timer_x = WIDTH - 270
            timer_y = 70
            win.blit(timer_text, (timer_x, timer_y))

            pygame.display.update()

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key >= pygame.K_a and event.key <= pygame.K_z:
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
        text = font.render(word, True, BLACK)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        win.blit(text, text_rect)
        pygame.display.update()
        pygame.time.delay(2000)

    # Calculate score percentage
    score_percentage = (score / total_words) * 100

    # Level complete or fail message
    win.fill(WHITE)
    win.blit(background_image, (0, 0))
    font = pygame.font.SysFont(None, 100)

    if score_percentage >= 50:
        text = font.render('Level Complete!', True, BLACK)
    else:
        text = font.render('Level Fail!', True, BLACK)

    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    win.blit(text, text_rect)

    final_score_text = font_score.render(f"Final Score: {score}/{total_words}", True, BLACK)
    final_score_rect = final_score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
    win.blit(final_score_text, final_score_rect)
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


