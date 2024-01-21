import turtle
import winsound


window = turtle.Screen()
window.title("Ping Pong")
window.bgcolor("black")
window.setup(width=800, height=600)
window.tracer(0)    # stops the window from updating

#   1st Paddle
paddle_one = turtle.Turtle()
paddle_one.speed(0)     # speed of animation, '0' for MAX
paddle_one.color("white")
paddle_one.shape("square")
paddle_one.shapesize(stretch_wid=5, stretch_len=1)  # 20*5 height
paddle_one.penup()
paddle_one.goto(-350, 0)    # (0, 0) is in middle
wid_one = 5

#   2nd Paddle
paddle_two = turtle.Turtle()
paddle_two.speed(0)     # speed of animation, '0' for MAX
paddle_two.color("white")
paddle_two.shape("square")
paddle_two.shapesize(stretch_wid=5, stretch_len=1)
paddle_two.penup()
paddle_two.goto(350, 0)    # (0, 0) is in middle
wid_two = 5

#   Ball
ball = turtle.Turtle()
ball.speed(0)     # speed of animation, '0' for MAX
ball.color("white")
ball.shape("circle")
ball.penup()
ball.goto(0, 0)    # (0, 0) is in middle
ball.dx = 0.2     # ball moves by 2 pixels
ball.dy = -0.2

# Multiple Balls List
balls = [ball]  # Start with one ball in the list

# Pause state
is_paused = False

# Pause and start the game
def toggle_pause():
    global is_paused
    is_paused = not is_paused

# Add a new ball to the game
def add_ball():
    new_ball = turtle.Turtle()
    new_ball.speed(0)
    new_ball.shape("circle")
    new_ball.color("white")
    new_ball.penup()
    new_ball.goto(0, 0)
    new_ball.dx = 0.2 * (-1 if len(balls) % 2 == 0 else 1)
    new_ball.dy = -0.2
    balls.append(new_ball)

# Keyboard event for pausing
window.onkeypress(toggle_pause, 'p')
# for scoring

score_one = 0
score_two = 0

write_score = turtle.Turtle()
write_score.speed(0)
write_score.color("white")
write_score.penup()
write_score.hideturtle()
write_score.goto(0, 260)
write_score.write("Player One: 0        Player Two: 0", align="center", font=("Courier", 24, "normal"))


# movement of paddle
def paddle_one_up():
    y = paddle_one.ycor()   # coordinates
    y += 50
    paddle_one.sety(y)


def paddle_one_down():
    y = paddle_one.ycor()   # coordinates
    y -= 50
    paddle_one.sety(y)


def paddle_two_up():
    y = paddle_two.ycor()   # coordinates
    y += 50
    paddle_two.sety(y)


def paddle_two_down():
    y = paddle_two.ycor()   # coordinates
    y -= 50
    paddle_two.sety(y)


# Keyboard Events
window.listen()
# Left one
window.onkeypress(paddle_one_up, 'w')
window.onkeypress(paddle_one_down, 's')
# right one
window.onkeypress(paddle_two_up, 'Up')
window.onkeypress(paddle_two_down, 'Down')

# Function to change paddle color back after 10 seconds
def reset_paddle_color(paddle):
    paddle.color("white")

# New variables to track when to add a ball and paddle power-up state
last_score_for_new_ball = [0, 0]  # [score_one, score_two]

# Function to update the score
def update_score(player_one, player_two):
    global score_one, score_two
    score_one += player_one
    score_two += player_two
    write_score.clear()
    write_score.write("Player One: {}        Player Two: {}".format(score_one, score_two), align="center", font=("Courier", 24, "normal"))

    # Check for paddle power-up and change color
    if score_one % 10 == 0 and score_one != 0:
        paddle_one.color("red")
        window.ontimer(lambda: reset_paddle_color(paddle_one), 10000)
    if score_two % 10 == 0 and score_two != 0:
        paddle_two.color("red")
        window.ontimer(lambda: reset_paddle_color(paddle_two), 10000)

# Collision detection with power-up logic
def check_collision(ball):
    normal_speed_dx, normal_speed_dy = 0.2, -0.2  # Define normal ball speed

    if (340 < ball.xcor() < 350) and (paddle_two.ycor() + 50 > ball.ycor() > paddle_two.ycor() - 50):
        ball.setx(340)
        ball.dx *= -1
        if paddle_two.color()[0] == "red":
            ball.dx = 1.5 * normal_speed_dx if ball.dx > 0 else -1.5 * normal_speed_dx
        else:
            ball.dx = normal_speed_dx if ball.dx > 0 else -normal_speed_dx
        winsound.PlaySound("bounce.wav", winsound.SND_ASYNC)

    elif (-350 < ball.xcor() < -340) and (paddle_one.ycor() + 50 > ball.ycor() > paddle_one.ycor() - 50):
        ball.setx(-340)
        ball.dx *= -1
        if paddle_one.color()[0] == "red":
            ball.dx = 1.5 * normal_speed_dx if ball.dx > 0 else -1.5 * normal_speed_dx
        else:
            ball.dx = normal_speed_dx if ball.dx > 0 else -normal_speed_dx
        winsound.PlaySound("bounce.wav", winsound.SND_ASYNC)

# Main game loop
while True:
    window.update()
    if not is_paused:
        
        
        # Move each ball in the list of balls
        for ball in balls:
            ball.setx(ball.xcor() + ball.dx)
            ball.sety(ball.ycor() + ball.dy)
            
            # Ball's Border checking
            if ball.ycor() > 290:
                ball.sety(290)
                ball.dy *= -1   # reversing direction
                winsound.PlaySound("bounce.wav", winsound.SND_ASYNC)

            elif ball.ycor() < -290:
                ball.sety(-290)
                ball.dy *= -1   # reversing direction
                winsound.PlaySound("bounce.wav", winsound.SND_ASYNC)
            # Check ball & paddle collisions with power-up logic
            check_collision(ball)
            # Ball's Left and Right Border checking
            if ball.xcor() > 390:   # past the right paddle
                ball.goto(0, 0)
                ball.dx *= -1
                update_score(1, 0)   # Player One Scores

            elif ball.xcor() < -390:   # past the left paddle
                ball.goto(0, 0)
                ball.dx *= -1
                update_score(0, 1)   # Player Two Scores

            # Collisions between ball & paddles
            if (340 < ball.xcor() < 350) and (paddle_two.ycor() + 50 > ball.ycor() > paddle_two.ycor() - 50):
                ball.setx(340)
                ball.dx *= -1
                # If paddle_two is red, increase ball speed
                if paddle_two.color() == ("red",):
                    ball.dx *= 1.5
                winsound.PlaySound("bounce.wav", winsound.SND_ASYNC)

            elif (-340 > ball.xcor() > -350) and (paddle_one.ycor() + 50 > ball.ycor() > paddle_one.ycor() - 50):
                ball.setx(-340)
                ball.dx *= -1
                if paddle_one.color() == ("red",):
                    ball.dx *= 1.5
                winsound.PlaySound("bounce.wav", winsound.SND_ASYNC)