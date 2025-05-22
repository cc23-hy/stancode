"""
stanCode Breakout Project
Adapted from Eric Roberts's Breakout by
Sonja Johnson-Yu, Kylie Jue, Nick Bowman, 
and Jerry Liao.

The coder needs to create a breakout game
by setting up the ball/paddle/bricks/mouse
and the collision may happen while the ball
is moving.
"""
from campy.graphics.gwindow import GWindow
from campy.graphics.gobjects import GOval, GRect, GLabel
from campy.gui.events.mouse import onmouseclicked, onmousemoved
import random
''''''


BRICK_SPACING = 5      # Space between bricks (in pixels). This space is used for horizontal and vertical spacing
BRICK_WIDTH = 40       # Height of a brick (in pixels)
BRICK_HEIGHT = 15      # Height of a brick (in pixels)
BRICK_ROWS = 10        # Number of rows of bricks
BRICK_COLS = 10        # Number of columns of bricks
BRICK_OFFSET = 50      # Vertical offset of the topmost brick from the window top (in pixels)
BALL_RADIUS = 10       # Radius of the ball (in pixels)
PADDLE_WIDTH = 75      # Width of the paddle (in pixels)
PADDLE_HEIGHT = 15     # Height of the paddle (in pixels)
PADDLE_OFFSET = 50     # Vertical offset of the paddle from the window bottom (in pixels)
INITIAL_Y_SPEED = 7    # Initial vertical speed for the ball
MAX_X_SPEED = 5        # Maximum initial horizontal speed for the ball


class BreakoutGraphics:

    def __init__(self, ball_radius=BALL_RADIUS, paddle_width=PADDLE_WIDTH, paddle_height=PADDLE_HEIGHT,
                 paddle_offset=PADDLE_OFFSET, brick_rows=BRICK_ROWS, brick_cols=BRICK_COLS, brick_width=BRICK_WIDTH,
                 brick_height=BRICK_HEIGHT, brick_offset=BRICK_OFFSET, brick_spacing=BRICK_SPACING, title='Breakout'):

        self.window_width = brick_cols * (brick_width + brick_spacing) - brick_spacing
        self.window_height = brick_offset + 3 * (brick_rows * (brick_height + brick_spacing) - brick_spacing)
        self.window = GWindow(width=self.window_width, height=self.window_height, title=title)

        # Create a paddle
        self.brick_spacing = brick_spacing
        self.brick_cols = brick_cols
        self.paddle = GRect(paddle_width, paddle_height, x=(self.window_width - paddle_width)/2,
                            y=self.window_height - paddle_height - paddle_offset)
        self.paddle.color = 'black'
        self.paddle.filled = True
        self.paddle.fill_color = 'black'
        self.paddle_listener = True
        self.window.add(self.paddle)

        # Center a filled ball in the graphical window
        self.ball = GOval(ball_radius*2, ball_radius*2)
        self.ball.color = 'black'
        self.ball.filled = True
        self.ball.fill_color = 'black'
        self.window.add(self.ball, x=self.window_width/2-0.5*self.ball.width, y=self.window_height/2-self.ball.height)
        self.top_left = False
        self.top_right = False
        self.bottom_left = False
        self.bottom_right = False

        # Default initial velocity for the ball
        self.__dx = random.randint(1, MAX_X_SPEED)
        if random.random() > 0.5:
            self.__dx = - self.__dx
        self.__dy = INITIAL_Y_SPEED

        # Initialize our mouse listeners
        self.ball_switch = False
        self.mouse_switch = True
        onmouseclicked(self.handle_click)
        onmousemoved(self.paddle_moving)

        # Draw bricks
        self.the_number_of_bricks = brick_cols * brick_rows
        for i in range(brick_cols):
            for j in range(brick_rows):
                if j < 2:
                    self.brick = GRect(brick_width, brick_height)
                    self.brick.color = 'red'
                    self.brick.filled = True
                    self.brick.fill_color = 'red'
                    self.window.add(self.brick, x=i*(brick_width+brick_spacing),
                                    y=brick_offset+j*(brick_height+brick_spacing))
                elif 2 <= j < 4:
                    self.brick = GRect(brick_width, brick_height)
                    self.brick.color = 'orange'
                    self.brick.filled = True
                    self.brick.fill_color = 'orange'
                    self.window.add(self.brick, x=i*(brick_width+brick_spacing),
                                    y=brick_offset+j*(brick_height+brick_spacing))
                elif 4 <= j < 6:
                    self.brick = GRect(brick_width, brick_height)
                    self.brick.color = 'yellow'
                    self.brick.filled = True
                    self.brick.fill_color = 'yellow'
                    self.window.add(self.brick, x=i*(brick_width+brick_spacing),
                                    y=brick_offset+j*(brick_height+brick_spacing))
                elif 6 <= j < 8:
                    self.brick = GRect(brick_width, brick_height)
                    self.brick.color = 'green'
                    self.brick.filled = True
                    self.brick.fill_color = 'green'
                    self.window.add(self.brick, x=i*(brick_width+brick_spacing),
                                    y=brick_offset+j*(brick_height+brick_spacing))
                elif j >= 8:
                    self.brick = GRect(brick_width, brick_height)
                    self.brick.color = 'blue'
                    self.brick.filled = True
                    self.brick.fill_color = 'blue'
                    self.window.add(self.brick, x=i*(brick_width + brick_spacing),
                                    y=brick_offset+j*(brick_height+brick_spacing))

    def handle_click(self, event):
        if self.mouse_switch:
            self.ball_switch = True
            self.mouse_switch = False  # disable mouse listener while ball is moving

    def get_ball_switch(self):
        if self.ball_switch:
            self.ball_switch = False
            return True

    def is_ball_out_of_window(self):
        if self.ball.y + self.ball.height >= self.window.height:
            self.mouse_switch = True  # enable mouse listener
            return True
        else:
            return False

    def paddle_moving(self, event):
        if self.paddle_listener:
            if event.x-self.paddle.width*0.5 <= 0:
                self.paddle.x = 0
                self.paddle.y = self.window_height - PADDLE_OFFSET
            elif event.x+self.paddle.width*0.5 >= self.window.width:
                self.paddle.x = self.window.width-self.paddle.width
                self.paddle.y = self.window_height - PADDLE_OFFSET
            else:
                self.paddle.x = event.x - self.paddle.width * 0.5
                self.paddle.y = self.window_height - PADDLE_OFFSET

    def get_dx(self):
        self.__dx = random.randint(1, MAX_X_SPEED)
        if random.random() > 0.5:
            self.__dx = - self.__dx
        return self.__dx

    def get_dy(self):
        self.__dy = INITIAL_Y_SPEED
        return self.__dy

    def reset_ball(self):
        self.set_ball_position()
        self.window.add(self.ball)

    def set_ball_position(self):
        self.ball.x = self.window_width/2-0.5*self.ball.width
        self.ball.y = self.window_height/2-self.ball.height

    def remove_ball(self):
        self.window.remove(self.ball)

    def collision(self):
        self.top_left = self.window.get_object_at(self.ball.x, self.ball.y)
        self.top_right = self.window.get_object_at(self.ball.x + self.ball.width, self.ball.y)
        self.bottom_left = self.window.get_object_at(self.ball.x, self.ball.y + self.ball.height)
        self.bottom_right = self.window.get_object_at(self.ball.x + self.ball.width, self.ball.y + self.ball.height)
        is_ball_on_paddle = self.top_left == self.paddle or self.top_right == self.paddle or \
            self.bottom_left == self.paddle or self.bottom_right == self.paddle
        is_none = self.top_left is None and self.top_right is None and self.bottom_left is None and self.bottom_right is None
        is_brick = not is_ball_on_paddle and not is_none
        if is_brick:
            obj = self.top_left or self.top_right or self.bottom_left or self.bottom_right
            self.the_number_of_bricks -= 1
            self.window.remove(obj)
        return not is_none

    def collision_with_right_side_of_paddle(self):
        top_left = self.window.get_object_at(self.ball.x, self.ball.y)
        top_right = self.window.get_object_at(self.ball.x + self.ball.width, self.ball.y)
        bottom_left = self.window.get_object_at(self.ball.x, self.ball.y + self.ball.height)
        bottom_right = self.window.get_object_at(self.ball.x + self.ball.width, self.ball.y + self.ball.height)
        left = self.window.get_object_at(self.ball.x, self.ball.y + 0.5 * self.ball.height)
        right = self.window.get_object_at(self.ball.x + self.ball.width, self.ball.y + 0.5 * self.ball.height)
        if (bottom_left == self.paddle and bottom_right is None) or (top_left == self.paddle and top_right is None) or \
            (left == self.paddle and right is None):
            self.paddle_listener = False
            return True
        else:
            return False

    def collision_with_left_side_of_paddle(self):
        top_left = self.window.get_object_at(self.ball.x, self.ball.y)
        top_right = self.window.get_object_at(self.ball.x + self.ball.width, self.ball.y)
        bottom_left = self.window.get_object_at(self.ball.x, self.ball.y + self.ball.height)
        bottom_right = self.window.get_object_at(self.ball.x + self.ball.width, self.ball.y + self.ball.height)
        left = self.window.get_object_at(self.ball.x, self.ball.y + 0.5 * self.ball.height)
        right = self.window.get_object_at(self.ball.x + self.ball.width, self.ball.y + 0.5 * self.ball.height)
        if (bottom_right == self.paddle and bottom_left is None) or (top_right == self.paddle and top_left is None) or \
                (right == self.paddle and left is None):
            self.paddle_listener = False
            return True
        else:
            return False

    def enable_paddle_listener(self):
        if not self.paddle_listener:
            self.paddle_listener = True

    def losing(self):
        lose = GLabel("You lose :'(")
        lose.font = '-45'
        lose.color = 'olive'
        self.window.add(lose, x=self.window.width*0.5-lose.width*0.5, y=self.window.height*0.5)

    def winning(self):
        win = GLabel("You win :')")
        win.font = '-45'
        win.color = 'olive'
        self.window.add(win, x=self.window.width * 0.5 - win.width * 0.5, y=self.window.height * 0.5)
