import pygame
import pyaudio
import audioop
import math
import time
import random
import os
import sys

# Suppress Pygame's startup message
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"


# PyAudio configuration
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
THRESHOLD_DB = 10  # Modification threshold
TEST_DURATION = 10  # Run for 10 seconds

# Initialize PyAudio
p = pyaudio.PyAudio()
stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((500, 350))
pygame.display.set_caption("Exhaust Sound Test")
font_large = pygame.font.Font(None, 50)
font_small = pygame.font.Font(None, 30)

# UI Colors
BACKGROUND_COLOR = (30, 30, 30)
WAVE_COLOR = (0, 150, 255)
TEXT_COLOR = (255, 255, 255)
GREEN = (0, 200, 0)
RED = (200, 0, 0)

# Function to calculate decibels with better handling of silence
def calculate_decibels(data):
    rms = audioop.rms(data, 2)
    if rms > 0:
        db = 20 * math.log10(rms / 32768)  # Convert to decibels
        return max(0.1, db + 100)  # Avoid returning 0
    return 0.1  # Small non-zero value to prevent incorrect averaging

# Function to generate wave animation
def draw_waveform(amplitude):
    screen.fill(BACKGROUND_COLOR)
    wave_height = int(amplitude * 2)  # Scale the wave height

    # Draw wave pattern
    for i in range(0, 500, 20):
        height_variation = random.randint(-wave_height, wave_height)
        pygame.draw.line(screen, WAVE_COLOR, (i, 175 - height_variation), (i, 175 + height_variation), 3)

    pygame.display.flip()

# Collect sound readings for 10 seconds
decibel_readings = []
start_time = time.time()

while time.time() - start_time < TEST_DURATION:
    data = stream.read(CHUNK, exception_on_overflow=False)
    decibels = calculate_decibels(data)
    decibel_readings.append(decibels)

    # Draw wave animation based on sound level
    draw_waveform(decibels)

# Calculate final values
average_db = sum(decibel_readings) / len(decibel_readings)
modification_status = "MODIFIED" if average_db > THRESHOLD_DB else "NOT MODIFIED"
status_color = RED if modification_status == "MODIFIED" else GREEN

# Show final result
screen.fill(BACKGROUND_COLOR)
result_text = font_large.render(modification_status, True, status_color)
avg_text = font_small.render(f"Avg Sound Level: {average_db:.2f} dB", True, TEXT_COLOR)
screen.blit(result_text, (130, 120))
screen.blit(avg_text, (130, 180))

pygame.display.flip()

print(modification_status)

# Allow user to quit manually after seeing the result
done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
            done = True


# Cleanup
stream.stop_stream()
stream.close()
p.terminate()
pygame.quit()