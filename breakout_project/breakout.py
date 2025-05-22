"""
stanCode Breakout Project
Adapted from Eric Roberts's Breakout by
Sonja Johnson-Yu, Kylie Jue, Nick Bowman,
and Jerry Liao.

This program is a breakout game. The player
moves the paddle to bounce the ball and to
remove the bricks. If the ball falls out of
the GWindow, the lives that the player has
minus by 1. This game ends with either the
player runs out of lives or all the bricks
are removed.
"""

from campy.gui.events.timer import pause
from breakoutgraphics import BreakoutGraphics

FRAME_RATE = 1000 / 120  # 120 frames per second
NUM_LIVES = 10		 # Number of attempts


def main():
    graphics = BreakoutGraphics()
    # Add the animation loop here!
    lives = NUM_LIVES
    if lives != 0:
        graphics.dx = graphics.get_dx()
        graphics.dy = graphics.get_dy()
        ball_switch = False
        while True:
            pause(FRAME_RATE)
            graphics.enable_paddle_listener()
            if graphics.dy > 0:
                graphics.dy = graphics.get_dy()
            if not ball_switch:
                ball_switch = graphics.get_ball_switch()
            if ball_switch:
                graphics.ball.move(graphics.dx, graphics.dy)

                if graphics.ball.x+graphics.ball.width >= graphics.window.width or graphics.ball.x <= 0:
                    graphics.dx *= -1
                    while graphics.ball.x+graphics.ball.width >= graphics.window.width or graphics.ball.x <= 0:
                        graphics.ball.move(graphics.dx, graphics.dy)

                if graphics.ball.y <= 0:
                    graphics.dy *= -1

                if graphics.collision():
                    graphics.dy *= -1

                    if graphics.collision_with_right_side_of_paddle():
                        if graphics.dx <= 0:
                            graphics.dx *= -1

                    elif graphics.collision_with_left_side_of_paddle():
                        if graphics.dx >= 0:
                            graphics.dx *= -1
                    graphics.enable_paddle_listener()

                    if graphics.the_number_of_bricks == 0:
                        graphics.remove_ball()
                        graphics.window.remove(graphics.paddle)
                        graphics.winning()
                        break

                if graphics.is_ball_out_of_window():
                    lives -= 1
                    graphics.remove_ball()
                    if lives == 0:  
                        graphics.window.remove(graphics.paddle)
                        graphics.losing()
                        break
                    else:  
                        graphics.reset_ball()
                        graphics.dx = graphics.get_dx()
                        graphics.dy = graphics.get_dy()
                        ball_switch = False
                        graphics.enable_paddle_listener()


if __name__ == '__main__':
    main()
