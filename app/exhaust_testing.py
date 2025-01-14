import pygame
import pyaudio
import audioop
import math
import time

# PyAudio configuration
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
THRESHOLD_DB = 80  # Threshold in decibels

# Initialize PyAudio
p = pyaudio.PyAudio()
stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((500, 300))
pygame.display.set_caption("Vehicle Sound Monitor")
font = pygame.font.Font(None, 36)
done = False

# Colors
BACKGROUND_COLOR = (50, 50, 50)
TEXT_COLOR = (255, 255, 255)
BUTTON_COLOR = (200, 50, 50)
BUTTON_HOVER_COLOR = (255, 100, 100)
BUTTON_TEXT_COLOR = (255, 255, 255)

# Button dimensions
button_rect = pygame.Rect(180, 200, 140, 50)

# Variables for smoothing
decibel_history = []
history_size = 10  # Number of samples for smoothing
last_update_time = time.time()
update_interval = 0.2  # Update UI every 0.5 seconds

def calculate_decibels(data):
    """Convert audio RMS value to decibels."""
    rms = audioop.rms(data, 2)  # RMS value of the audio data
    if rms > 0:
        db = 20 * math.log10(rms / 32768)  # Normalize RMS to 16-bit range
        return max(0, db + 100)  # Adjust baseline and ensure no negative values
    return 0

while not done:
    # Read audio data from the microphone
    data = stream.read(CHUNK, exception_on_overflow=False)
    decibels = calculate_decibels(data)

    # Add decibel value to history for smoothing
    decibel_history.append(decibels)
    if len(decibel_history) > history_size:
        decibel_history.pop(0)  # Maintain history size

    # Calculate the rolling average
    smoothed_decibels = sum(decibel_history) / len(decibel_history)

    # Determine sound level
    level_status = "Above 80 dB" if smoothed_decibels > THRESHOLD_DB else "Below 80 dB"

    # Update the UI only at the specified interval
    if time.time() - last_update_time > update_interval:
        # Clear the screen
        screen.fill(BACKGROUND_COLOR)

        # Display decibel level
        db_text = font.render(f"Decibel Level: {smoothed_decibels:.2f} dB", True, TEXT_COLOR)
        screen.blit(db_text, (50, 50))

        # Display level status
        status_text = font.render(f"Status: {level_status}", True, TEXT_COLOR)
        screen.blit(status_text, (50, 100))

        # Draw the Quit button
        mouse_pos = pygame.mouse.get_pos()
        if button_rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, BUTTON_HOVER_COLOR, button_rect)
        else:
            pygame.draw.rect(screen, BUTTON_COLOR, button_rect)

        # Draw button text
        button_text = font.render("Quit", True, BUTTON_TEXT_COLOR)
        screen.blit(button_text, (button_rect.x + 35, button_rect.y + 10))

        # Flip the display
        pygame.display.flip()

        # Update the last update time
        last_update_time = time.time()

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect.collidepoint(event.pos):
                done = True

# Cleanup resources
stream.stop_stream()
stream.close()
p.terminate()
pygame.quit()