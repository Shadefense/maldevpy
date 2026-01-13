import pygame
pygame.init()

# Set up the drawing window
screen_width = 500
screen_height = 500
screen = pygame.display.set_mode([screen_width, screen_height])

# Set initial position and speed for the circle
circle_x = screen_width // 2
circle_y = screen_height // 2
circle_radius = 20
circle_speed = 5

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Run until the user asks to quit
running = True
while running:
    # Set the frame rate (e.g., 60 FPS)
    clock.tick(60)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get the state of all keyboard buttons
    keys = pygame.key.get_pressed()

    # Update the circle's position based on pressed keys
    # Note: in Pygame, the top-left corner is (0,0). Moving up means decreasing the y-coordinate.
    if keys[pygame.K_UP]:
        circle_y -= circle_speed
    if keys[pygame.K_DOWN]:
        circle_y += circle_speed
    if keys[pygame.K_LEFT]:
        circle_x -= circle_speed
    if keys[pygame.K_RIGHT]:
        circle_x += circle_speed

    # Optional: Keep the circle within the screen boundaries
    circle_x = max(circle_radius, min(circle_x, screen_width - circle_radius))
    circle_y = max(circle_radius, min(circle_y, screen_height - circle_radius))

    # Drawing
    screen.fill((255, 255, 255)) # Fill background with white to clear previous frames
    pygame.draw.circle(screen, (0, 0, 255), (circle_x, circle_y), circle_radius)

    # Flip the display to make our drawings visible
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()
