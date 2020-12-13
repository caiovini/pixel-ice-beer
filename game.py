import pygame as pg
import pymunk as pm

import sys

from assets import Ball, fetch_hole_coordinates
from os.path import join

SCREEN_HEIGHT = 600
SCREEN_WIDTH = 500

GREEN = pg.Color(215, 215, 100)
BLACK = pg.Color(25, 25, 50)
BROWN = pg.Color(210, 105, 30)
BLUE = pg.Color(0, 0, 200)
YELLOW = pg.Color(255, 255, 0)

clock = pg.time.Clock()
space_step = 1/60


def main() -> None:
    pg.init()
    screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pg.display.set_caption("Pixel ice beer")

    holes_coordinates = fetch_hole_coordinates()
    font = pg.font.Font(join("fonts", "segoe-ui-symbol.ttf"), 20)

    line_x0 = 0
    line_y0 = 500
    line_x1 = SCREEN_WIDTH
    line_y1 = 500

    alpha_bg = pg.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    alpha_bg.set_alpha(128)
    alpha_bg.fill((BLACK))

    ball = Ball()
    ball.set_position(100, 400)

    space = pm.Space()
    space.gravity = (0.0, 600.0)

    pm.Segment.friction = pm.Circle.friction = 0.5
    pm.Segment.elasticity = pm.Circle.elasticity = 10
    shape = pm.Circle(ball.body, ball.radius, pm.Vec2d(0, 0))

    space.add(ball.body, shape)

    def create_static_lines() -> list:

        """
            Creates a list of segments
            pymunk will use these to calculate the physics of the ball
        """

        body = pm.Body(body_type=pm.Body.STATIC)
        
        segment_1 = pm.Segment(body, (line_x0, line_y0), (line_x1, line_y1), 5) # Segment to move the ball
        segment_2 = pm.Segment(body, (0, 0), (0, SCREEN_HEIGHT), 5)             # Left side line
        segment_3 = pm.Segment(body, (SCREEN_WIDTH, 0),
                            (SCREEN_WIDTH, SCREEN_HEIGHT), 5)                   # Right side line
        

        return [body, segment_1, segment_2, segment_3]

    run_space_steps = True
    seconds = score_ = 0
    game_win = game_over = done = False
    start_ticks = pg.time.get_ticks()
    while not done:

        screen.fill(GREEN)

        for event in pg.event.get():

            if event.type == pg.QUIT:
                done = True

            if event.type == pg.KEYDOWN:

                if event.key == pg.K_ESCAPE:
                    done = True

        if not game_over and not game_win:
            keys = pg.key.get_pressed()
            if 0 < line_y1 < SCREEN_HEIGHT:
                if keys[pg.K_RIGHT]:
                    score_ += 1
                    line_y1 -= 2

            keys = pg.key.get_pressed()
            if 0 < line_y0 < SCREEN_HEIGHT:
                if keys[pg.K_LEFT]:
                    score_ += 1
                    line_y0 -= 2

            if keys[pg.K_DOWN]:
                line_y1 += 1
                line_y0 += 1

            if keys[pg.K_UP]:
                score_ += 1
                line_y1 -= 1
                line_y0 -= 1

        static_lines = create_static_lines()
        space.add(*static_lines) # Add segments

        if run_space_steps:
            space.step(space_step)

        screen.blit(
            ball.image, (ball.body.position.x - ball.image.get_rect().size[0] / 2,
                         ball.body.position.y - ball.image.get_rect().size[1] / 4))

        for hole in holes_coordinates:
            rect, score = hole.values()

            pg.draw.circle(screen, BLACK, (rect.x, rect.y), rect.width, width=0)
            if score:
                pg.draw.circle(screen, BLUE, (rect.x, rect.y),
                               rect.width + 5, width=4)

            if(rect.colliderect(pg.Rect(ball.body.position.x, ball.body.position.y, 
                                            ball.radius, ball.radius))):
                if not game_over and not game_win:
                    if not score:
                        game_over = True
                    else:
                        game_win = True

        pg.draw.line(screen, BROWN, (line_x0, line_y0),
                     (line_x1, line_y1), width=4)

        label = font.render(
            f"SCORE: {score_}", 1, BLACK)
        screen.blit(label, (10, SCREEN_HEIGHT - 30))

        if not game_over and not game_win:
            seconds = (pg.time.get_ticks()-start_ticks)/1000

        label = font.render(
            f"TIME: {seconds}", 1, BLACK)
        screen.blit(label, (10, SCREEN_HEIGHT - 60))

        if game_over and not game_win:
            screen.blit(alpha_bg, (0, 0))
            label = font.render(
                "GAME OVER", 1, YELLOW)
            screen.blit(label, (SCREEN_WIDTH / 2.8, SCREEN_HEIGHT / 2.5))

        if game_win and not game_over:
            screen.blit(alpha_bg, (0, 0))
            label = font.render(
                "VICTORY !!!", 1, YELLOW)
            screen.blit(label, (SCREEN_WIDTH / 2.8, SCREEN_HEIGHT / 2.5))

        if not (0 < ball.body.position.x < SCREEN_WIDTH) or \
               not (0 < ball.body.position.y < SCREEN_HEIGHT):
                    game_over = True
                    run_space_steps = False

        pg.display.flip()
        space.remove(*static_lines) # Remove segments
        clock.tick(60)  # FPS


if __name__ == "__main__":
    sys.exit(main())
