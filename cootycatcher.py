from graphics import *
import time


COLORS = {'red': [1, 2], 'green': [3, 4], 'blue': [5, 6], 'yellow': [7, 8]}

FORTUNES = {1: 'you will die alone and poorly dressed',
            2: 'a smile is your personal welcome mat',
            3: 'don\'t kiss an elephant on the lips today',
            4: 'the best angle from which to approach \nany problem is the TRYangle',
            5: 'do or do not, there is no try',
            6: 'when in anger, sing the alphabet',
            7: 'a great pleasure in life is doing what \nothers say you can\'t',
            8: 'fortune number eight'}


class Catcher():
    # Creates a fortune teller
    def __init__(self, colors=COLORS, fortunes=FORTUNES):
        
        self.colors = colors
        self.fortunes = fortunes

    # Draws the closed fortune teller on the screen
    def draw_catcher(self):
        self.polys = []
        offset = [250, 250]
        corners = [(0, 0), (0, -100), (-150, -150), (-100, 0)]

        for (reflection_x, reflection_y) in [[1, 1], [1, -1], [-1, 1], [-1, -1]]:
            points = []
            for (dx, dy) in corners:
                points.append(Point(reflection_x * dx + offset[0], reflection_y * dy + offset[1]))
            self.polys.append(Polygon(*points))

        circle_spots = [[200, 200], [300, 200], [300, 300], [200, 300]]
        self.circles = [Circle(Point(*spot), 25) for spot in circle_spots]
        for circle, color in zip(self.circles, self.colors.keys()):
            circle.setFill(color)

        self.image = self.polys + self.circles
        return self.image


    # Draws the fortune teller open on the screen
    def draw_open(self):
        for circle in self.circles:
            circle.undraw()

        line_one = Line(Point(250, 150), Point(150, 250))
        line_two = Line(Point(250, 150), Point(350, 250))
        line_three = Line(Point(250, 350), Point(150, 250))
        line_four = Line(Point(250, 350), Point(350, 250))

        self.open_image = [line_one, line_two, line_three, line_four]
        return self.open_image

    # Draws numbers on the fortune teller
    def draw_nums(self, num_list):
        num_one = Text(Point(225, 225), num_list[0])
        num_two = Text(Point(275, 225), num_list[1])
        num_three = Text(Point(275, 275), num_list[2])
        num_four = Text(Point(225, 275), num_list[3])

        self.num_image =[num_one, num_two, num_three, num_four]
        return self.num_image


class Play():

    def __init__(self):
        self.background = GraphWin("Cooty Catcher", 500, 500)

        # Gives the user the option to customize the fortune teller
        if self.customize_catcher():
            self.catcher = Catcher(self.colors, self.fortunes)
        else:
            self.catcher = Catcher()

        # Draws the fortune teller
        for item in self.catcher.draw_catcher():
            item.draw(self.background)

    def customize_catcher(self):
        custom_message = Text(Point(250, 200), "Customize?")
        yes_message = Text(Point(200, 250), "Yes")
        no_message = Text(Point(300, 250), "No")
        custom_message.draw(self.background)
        yes_message.draw(self.background)
        no_message.draw(self.background)
        
        pick = self.background.getMouse()
        pick_x = pick.getX()

        custom_message.undraw()
        yes_message.undraw()
        no_message.undraw()

        # Checks if user has chosen to customize
        if pick_x < 250:
            # If yes, prompts for custom colors and fortunes
            self.colors = {}
            self.fortunes = {}
            
            message = Text(Point(250, 200), "Write an X11 color\npress Enter")
            message.draw(self.background)
            for i in range(1, 9):
                if i % 2 != 0:
                    color_entry = Entry(Point(250, 250), 50)
                    color_entry.draw(self.background)
                    while self.background.getKey() != "Return":
                        continue
                    color = color_entry.getText()
                    self.colors[color] = [i, i + 1]
                    color_entry.undraw()
            
            message.setText("Write a fortune\npress Enter")
            for j in range(1, 9):
                fortune_entry = Entry(Point(250, 250), 50)
                fortune_entry.draw(self.background)
                while self.background.getKey() != "Return":
                    continue
                fortune = fortune_entry.getText()
                self.fortunes[j] = fortune
                fortune_entry.undraw()
            message.undraw()

            return True

        else:
            return False

    # Allows the user to pick colors/numbers in the fortune teller
    def mouse_click(self, option_list, target_item):
        pick_message = message_block('Pick a {}'.format(target_item),
                                    [250, 50])
        for item in pick_message:
            item.draw(self.background)

        pick = self.background.getMouse()
        pick_x = pick.getX()
        pick_y = pick.getY()

        if (150 <= pick_x <= 250) and (150 <= pick_y <= 250):
            var = option_list[0]
        elif (250 <= pick_x <= 350) and (150 <= pick_y <= 250):
            var = option_list[1]
        elif (250 <= pick_x <= 350) and (250 <= pick_y <= 350):
            var = option_list[2]
        elif (150 <= pick_x <= 250) and (250 <= pick_y <= 350):
            var = option_list[3]

        for item in pick_message:
            item.undraw()

        return var

    # Simulates the fortune teller opening and closing during a turn
    def switch(self, start, num_list):
        # Create second list of number to simulate switch
        num_list_two = clean_list([(i + 2) % 8 for i in num_list])

        self.current_draw_list = []

        # Check where the start point for the switch is a color or number
        if type(start) == str:
            color = start
        elif type(start) == int:
            start = [i for i in range(1, start + 1)]
            color = 'black'
        else:
            raise ValueError

        # Cycle through the letter or numbers
        for j in range(len(start)):
            # Undraw any numbers currently drawn
            for render in self.current_draw_list:
                render.undraw()
            # Draw a header number or letter as each switch occurs
            draw_item = Text(Point(250, 50), start[j])
            draw_item.setFill(color)
            draw_item.setSize(36)
            draw_item.draw(self.background)
            # Determine which number list to draw
            if len(start) % 2 == 0:
                if j % 2 == 0:
                    current_num_list = num_list_two
                else:
                    current_num_list = num_list
            else:
                if j % 2 == 0:
                    current_num_list = num_list
                else:
                    current_num_list = num_list_two

            # Draw the number list
            self.current_draw_list = self.catcher.draw_nums(current_num_list)

            for render in self.current_draw_list:
                render.draw(self.background)

            # Wait so user can see what is happening
            time.sleep(.5)

            # Undraw the header number or letter
            draw_item.undraw()

        return self.current_draw_list

    # Allows user to pick a color, return the numbers assoicate with that color
    def color_pick(self):
        # Get user selection
        color = self.mouse_click(self.catcher.colors.keys(), 'color')

        # Generate list of numbers, based on color selection
        self.num_choices = []
        if len(color) % 2 != 0:
            for value in self.catcher.colors[color]:
                self.num_choices.append((value + 1) % 8)
                self.num_choices.append((value + 5) % 8)
        else:
            for value in self.catcher.colors[color]:
                self.num_choices.append((value + 7) % 8)
                self.num_choices.append((value + 3) % 8)
        
        # Clean number list for drawing
        self.num_choices = clean_list(self.num_choices)

        # Draw open fortune teller
        for item in self.catcher.draw_open():
            item.draw(self.background)

        # Simulate switch and draw numbers
        self.num_choice_draw = self.switch(color, self.num_choices)

        # Return number list for user to choose from
        return self.num_choices

    # Allows user to pick a number, returns final set of numbers based on pick
    def num_pick(self, catcher_nums):
        # Get user selection
        num = self.mouse_click(catcher_nums, 'number')

        # Generate the final list of numbers, based on user selection
        self.final_nums = []
        if num % 2 == 0:
            self.final_nums = catcher_nums
        else:
            for item in catcher_nums:
                self.final_nums.append((item + 2) % 8)

        # Clean number list
        self.final_nums = clean_list(self.final_nums)

        # Remove previous number list
        for item in self.num_choice_draw:
            item.undraw()

        # Simulate switch and draw final numbers
        self.switch(num, self.final_nums)

        # Return the final list of number for the fortune pick
        return self.final_nums

    # Allows user to pick a fortune from the final number options
    def fortune_pick(self, final_nums):
        # Get user selection
        fortune_num = self.mouse_click(final_nums, 'fortune')

        #Print fortune
        fortune_message = message_block(self.catcher.fortunes[fortune_num],
                                        [250, 250])
        for item in fortune_message:
            item.draw(self.background)
    
    # Runs the game
    def turn(self):
        nums = self.color_pick()
        finals = self.num_pick(nums)
        self.fortune_pick(finals)

        # Wait for user to click on the screen then close
        self.background.getMouse()
        self.background.close()

# Draw a message block on the screen
def message_block(message, center):
    message_back = Rectangle(Point(center[0] - 100, center[1] - 20),
        Point(center[0] + 100, center[1] + 20))
    message_back.setFill('white')
    message_text = Text(Point(center[0], center[1]), message)

    message_block = [message_back, message_text]

    return message_block

# Cleans up a number list for future use
def clean_list(num_list):
    if 0 in num_list:
        num_list[num_list.index(0)] = 8

    num_list.sort()

    return num_list


game = Play()
game.turn()