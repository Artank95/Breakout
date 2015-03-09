import math
import pygame
import time

# Define some colors
black = (0, 0, 0)
white = (255, 255, 255)
blue = (0, 0, 255)

# Size of break-out blocks
block_width = 23
block_height = 15

class Block(pygame.sprite.Sprite):
    """This class represents each block that will get knocked out by the ball
    It derives from the "Sprite" class in Pygame """

    def __init__(self, color, x, y):
        """ Constructor. Pass in the color of the block, 
            and its x and y position. """

        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)

        # Create the image of the block of appropriate size
        # The width and height are sent as a list for the first parameter.
        self.image = pygame.Surface([block_width, block_height])

        # Fill the image with the appropriate color
        self.image.fill(color)

        # Fetch the rectangle object that has the dimensions of the image
        self.rect = self.image.get_rect()

        # Move the top left of the rectangle to x,y.
        # This is where our block will appear..
        self.rect.x = x
        self.rect.y = y


class Ball(pygame.sprite.Sprite):
    """ This class represents the ball        
        It derives from the "Sprite" class in Pygame """

    # Speed in pixels per cycle
    speed = 15.0

    # Floating point representation of where the ball is
    x = 0.0
    y = 180.0

    # Direction of ball (in degrees)
    direction = 200

    width = 20
    height = 20

    # Constructor. Pass in the color of the block, and its x and y position
    def __init__(self):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)

        # Create the image of the ball
        self.image = pygame.Surface([self.width, self.height])

        # Color the ball
        self.image.fill(white)

        # Get a rectangle object that shows where our image is
        self.rect = self.image.get_rect()

        # Get attributes for the height/width of the screen
        self.screenheight = pygame.display.get_surface().get_height()
        self.screenwidth = pygame.display.get_surface().get_width()

    def bounce(self, diff):
        """ This function will bounce the ball 
            off a horizontal surface (not a vertical one) """

        self.direction = (180 - self.direction) % 360
        self.direction -= diff

    def update(self):
        """ Update the position of the ball. """
        # Sine and Cosine work in degrees, so we have to convert them
        direction_radians = math.radians(self.direction)

        # Change the position (x and y) according to the speed and direction
        self.x += self.speed * math.sin(direction_radians)
        self.y -= self.speed * math.cos(direction_radians)

        # Move the image to where our x and y are
        self.rect.x = self.x
        self.rect.y = self.y

        # Do we bounce off the top of the screen?
        if self.y <= 0:
            self.bounce(0)
            self.y = 1

        # Do we bounce off the left of the screen?
        if self.x <= 0:
            self.direction = (360 - self.direction) % 360
            self.x = 1

        # Do we bounce of the right side of the screen?
        if self.x > self.screenwidth - self.width:
            self.direction = (360 - self.direction) % 360
            self.x = self.screenwidth - self.width - 1

        # Did we fall off the bottom edge of the screen?
        if self.y > 600:
            return True
        else:
            return False

class Player(pygame.sprite.Sprite):
    """ This class represents the bar at the bottom that the player controls. """

    def __init__(self):
        """ Constructor for Player. """
        # Call the parent's constructor
        pygame.sprite.Sprite.__init__(self)

        self.width = 100
        self.height = 20
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill((white))

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.screenheight = pygame.display.get_surface().get_height()
        self.screenwidth = pygame.display.get_surface().get_width()

        self.rect.x = 0
        self.rect.y = self.screenheight-self.height

    def update(self):
        """ Update the player position. """
        # Get where the mouse is
        pos = pygame.mouse.get_pos()
        # Set the left side of the player bar to the mouse position
        self.rect.x = pos[0]
        # Make sure we don't push the player paddle 
        # off the right side of the screen
        if self.rect.x > self.screenwidth - self.width:
            self.rect.x = self.screenwidth - self.width

# Call this function so the Pygame library can initialize itself
pygame.init()

# Create an 800x600 sized screen
screen = pygame.display.set_mode([800, 600])

def text_objects(text,font):
    textSurface = font.render(text, True, white)
    return textSurface, textSurface.get_rect()

def text(text, x_text, y_text, font_size):
    TextFont = pygame.font.Font('freesansbold.ttf', font_size)
    TextSurf, TextRect = text_objects(text, TextFont)
    TextRect.center = ((x_text), (y_text))
    screen.blit(TextSurf, TextRect)



def button(msg, button_x, button_y, button_w, button_h,colour,action= None): 
   
    pos = pygame.mouse.get_pos()
    mouse_x = pos[0]
    mouse_y = pos[1]
    click = pygame.mouse.get_pressed()
   
   
    #Buttons:
    if button_x+button_w > mouse_x > button_x and button_y+button_h > mouse_y > button_y:
        pygame.draw.rect(screen, colour, (button_x,button_y,button_w,button_h))
        if click[0] == 1 and action!= None:
            if action == "Play":
                game_loop()
               
            elif action == "Quit":
                pygame.quit()
                quit()
            
            elif action == "Instructions":
                instructions()

    smallText = pygame.font.Font("freesansbold.ttf", 30)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ((button_x+(button_w/2),(button_y+(100/2))))
    screen.blit(textSurf, textRect)







def game_intro():
    display_width=800 
    display_height=600
    pygame.display.set_caption("Break out main menu")
    intro=True
    
    while intro:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit() 
                quit()
        screen.fill(black)
        largeText=pygame.font.Font("freesansbold.ttf",50)
        TextSurf, TextRect = text_objects("Breakout", largeText)
        TextRect.center = ((display_width/2), (display_height/6))
        screen.blit(TextSurf, TextRect)
        
        button("Start game",300,150,200,100,blue,"Play")
        button("Quit game",300,450,200,100,blue,"Quit")  
        button("Instructions",300,300,200,100,blue,"Instructions")
        
        pygame.display.update()


def instructions():
    done = True
    while done:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit() 
                quit()
        screen.fill(black)
        
        text("The objective of the game is to break all the bricks on the screen", 400, 100, 15)
        text("Do not let the ball hit the floor or else the game will end",400, 200, 15)
        text("Use the mouse to direct the paddle in order to hit the ball and stop it from touching the floor",400, 300, 15)
        
        button("start game",300,400,200,100,blue,"Play")
        button("quit game",300,500,200,100,blue,"Quit")  
        
        
        pygame.display.update()






def game_loop():
        
    # Set the title of the window
    pygame.display.set_caption('Breakout')
    
    # Enable this to make the mouse disappear when over our window
    pygame.mouse.set_visible(0)
    
    # This is a font we use to draw text on the screen (size 36)
    font = pygame.font.Font(None, 36)
    
    # Create a surface we can draw on
    background = pygame.Surface(screen.get_size())
    
    # Create sprite lists
    blocks = pygame.sprite.Group()
    balls = pygame.sprite.Group()
    allsprites = pygame.sprite.Group()
    
    # Create the player paddle object
    player = Player()
    allsprites.add(player)
    
    # Create the ball
    ball = Ball()
    allsprites.add(ball)
    balls.add(ball)
    
    # The top of the block (y position)
    top = 80
    
    # Number of blocks to create
    blockcount = 32
    
    # --- Create blocks
    
    # Five rows of blocks
    for row in range(5):
        # 32 columns of blocks
        for column in range(0, blockcount):
            # Create a block (color,x,y)
            block = Block(blue, column * (block_width + 2) + 1, top)
            blocks.add(block)
            allsprites.add(block)
        # Move the top of the next row down
        top += block_height + 2
    
    # Clock to limit speed
    clock = pygame.time.Clock()
    
    # Is the game over?
    game_over = False
    
    # Exit the program?
    exit_program = False
    
    # Main program loop
    while exit_program != True:
    
        # Limit to 30 fps
        clock.tick(30)
    
        # Clear the screen
        screen.fill(black)
    
        # Process the events in the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_program = True
                game_intro()
    
        # Update the ball and player position as long
        # as the game is not over.
        if not game_over:
            # Update the player and ball positions
            player.update()
            game_over = ball.update()
    
        # If we are done, print game over
        if game_over:
            text = font.render("Game Over", True, white)
            textpos = text.get_rect(centerx=background.get_width()/2)
            textpos.top = 300
            screen.blit(text, textpos)
            pygame.display.update()
            time.sleep(2)
            game_intro()
    
    
        # See if the ball hits the player paddle
        if pygame.sprite.spritecollide(player, balls, False):
            # The 'diff' lets you try to bounce the ball left or right 
            # depending where on the paddle you hit it
            diff = (player.rect.x + player.width/2) - (ball.rect.x+ball.width/2)
    
            # Set the ball's y position in case 
            # we hit the ball on the edge of the paddle
            ball.rect.y = screen.get_height() - player.rect.height - ball.rect.height - 1
            ball.bounce(diff)
    
        # Check for collisions between the ball and the blocks
        deadblocks = pygame.sprite.spritecollide(ball, blocks, True)
    
        # If we actually hit a block, bounce the ball
        if len(deadblocks) > 0:
            ball.bounce(0)
    
            # Game ends if all the blocks are gone
            if len(blocks) == 0:
                game_over = True

        # Draw Everything
        allsprites.draw(screen)
    
        # Flip the screen and show what we've drawn
        pygame.display.flip()
        
game_intro() 
game_loop()
pygame.quit()