import pygame

pygame.init()
window = pygame.display.set_mode((800, 600))
pygame.display.set_caption("ControllerSandbox")

controller = pygame.joystick.Joystick(0)

done = False
while not done:
    if controller.get_button(0): #A for playstation = X / Colour is Red
        pygame.draw.rect(window, (255, 0, 0), [0, 0, 800, 600])
    if controller.get_button(1): #B for playstation = O / Colour is Green
        pygame.draw.rect(window, (0, 255, 0), [0, 0, 800, 600])
    if controller.get_button(2): #X for playstation = SQUARE / Colour is Blue
        pygame.draw.rect(window, (0, 0, 255), [0, 0, 800, 600])
    if controller.get_button(3): #Y for playstation = Triangle / Colour is Orange
        pygame.draw.rect(window, (255, 165, 0), [0, 0, 800, 600])
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    pygame.display.update()

pygame.quit()