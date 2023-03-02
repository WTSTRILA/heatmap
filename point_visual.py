import pygame
import csv

monitor_width = 1280
monitor_height = 820

pygame.init()
screen = pygame.display.set_mode((monitor_width, monitor_height))

def draw_csv(file):
    with open(file, 'r') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            x = int(row[0])
            y = int(row[1])
            rect = pygame.Rect(x * monitor_width, y * monitor_height, monitor_width, monitor_height)
            pygame.draw.circle(screen, (0, 255, 0), (x, y), 3)
            pygame.draw.rect(screen, (255, 0, 0), rect)

draw_csv('output.csv')
pygame.display.update()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
