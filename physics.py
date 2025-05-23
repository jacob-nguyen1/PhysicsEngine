import pygame
import random
import math

class Ball:

    def __init__(self, radius, x, y):
        self.radius = radius
        self.v = 4.1887902 * self.radius**3
        self.m = 1500 * self.v
        self.x = x
        self.y = y
        self.v_x = 0 
        self.v_y = 0
        self.v = math.sqrt(self.v_x**2+self.v_y**2)
        self.a_x = 0
        self.a_y = -9.8
        self.a = math.sqrt(self.a_x**2+self.a_y**2)
        self.elasticity = 0.4
        self.k_e = 0.5 * self.m * self.v**2
        self.p = self.m * self.v
        self.image = pygame.transform.scale(pygame.image.load("ball.png"), (radius*2,radius*2))



def main():
    balls = []
    correction = 0

    pygame.init()
    screen = pygame.display.set_mode((640, 512))
    clock = pygame.time.Clock()
    running = True
    while running:
        elapsed_seconds = pygame.time.get_ticks() / 1000
        screen.fill("light green")
        
        frametime = pygame.time.get_ticks() / 1000 - correction
        correction = elapsed_seconds
        
        for ball in balls:
            ball.x += ball.v_x * frametime
            ball.y += ball.v_y * frametime
            ball.v_x += ball.a_x * frametime * 100
            ball.v_y += ball.a_y * frametime * 100

            # Ground collision
            if ball.y - ball.radius <= 0:
                ball.y = ball.radius
                if abs(ball.v_y) < 81:
                    ball.v_y = 0
                else:
                    ball.v_y *= -ball.elasticity

            # Wall collisions
            if ball.x - ball.radius <= 0:
                ball.x = ball.radius
                ball.v_x *= -ball.elasticity
            if ball.x + ball.radius >= 640:
                ball.x = 640 - ball.radius
                ball.v_x *= -ball.elasticity

            # Ball to ball collision (chatgpt)
            for other_ball in [ball_ for ball_ in balls if ball_ != ball]:
                # Calculate distance between ball centers
                distance = math.sqrt((other_ball.x - ball.x)**2 + (other_ball.y - ball.y)**2)
                
                # Check if distance is less than the sum of their radii => collision
                if distance < ball.radius + other_ball.radius:
                    
                    # Calculate collision angle
                    collision_angle = math.atan2(other_ball.y - ball.y, other_ball.x - ball.x)
                    
                    # Calculate overlap
                    overlap = 0.5 * (ball.radius + other_ball.radius - distance)
                    
                    # Displace the balls by the overlap to avoid sticking
                    ball.x -= overlap * math.cos(collision_angle)
                    ball.y -= overlap * math.sin(collision_angle)
                    other_ball.x += overlap * math.cos(collision_angle)
                    other_ball.y += overlap * math.sin(collision_angle)
                    
                    # Calculate new velocities in normal direction (along the collision angle)
                    ball_vx_normal = ball.v_x * math.cos(collision_angle) + ball.v_y * math.sin(collision_angle)
                    other_ball_vx_normal = other_ball.v_x * math.cos(collision_angle) + other_ball.v_y * math.sin(collision_angle)
                    
                    # Using one-dimensional elastic collision equations to get new normal velocities
                    ball_vx_normal_new = ((ball.m - other_ball.m) * ball_vx_normal + 2 * other_ball.m * other_ball_vx_normal) / (ball.m + other_ball.m)
                    other_ball_vx_normal_new = ((other_ball.m - ball.m) * other_ball_vx_normal + 2 * ball.m * ball_vx_normal) / (ball.m + other_ball.m)
                    
                    # Convert the new normal velocities back to x, y velocities
                    ball_vx_normal_diff = ball_vx_normal_new - ball_vx_normal
                    other_ball_vx_normal_diff = other_ball_vx_normal_new - other_ball_vx_normal
                    
                    ball.v_x += ball_vx_normal_diff * math.cos(collision_angle)
                    ball.v_y += ball_vx_normal_diff * math.sin(collision_angle)
                    
                    other_ball.v_x += other_ball_vx_normal_diff * math.cos(collision_angle)
                    other_ball.v_y += other_ball_vx_normal_diff * math.sin(collision_angle)

            screen.blit(ball.image, ball.image.get_rect(center=(ball.x, 512-ball.y)))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x = pygame.mouse.get_pos()[0]
                y = 512-pygame.mouse.get_pos()[1]
                new_ball = Ball(75, x, y)
                balls.append(new_ball)
        
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()


if __name__ == "__main__":
    main()