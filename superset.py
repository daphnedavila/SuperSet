from cmu_graphics import *
import copy, string, itertools, random

'''
Creative Elements:

Firstly, on the help screen, I have added growing text that tells the user to press n or p to play.
For my new creative theme, I have stars that vary in points, colors, and spins, as well as how many stars are in each card. 
In other words, there can be 4 total features with 4 things in each feature. In addition to this, you may press '7' to 
randomly change the background of the cards, and the background of the cards are gradients. With respect to the rounds and lives,
I have added dots to indicate how many rounds / lives there are left. Also, a timer is displayed on the side of the play screen. 
When you win the game, the screen turns green (gradient) and stars are seen sparkling. When you lose, the screen flashes red and 
black. Also, in the theme screen, the user can choose to have a random theme selected when they press r. 

'''

####################################################
# onAppStart: called only once when app is launched
####################################################

def onAppStart(app):
    app.newDims = [3,3,3]
    app.currDims = [3,3,3]
    app.randomBoardAndSet = getRandomBoardWithSet(app.currDims, 8)
    app.board = app.randomBoardAndSet[0]
    app.foundSet = app.randomBoardAndSet[1]
    app.cardsInSet = min(app.currDims)
    app.theme = 0
    app.rounds = 4
    app.lives = 2
    app.seconds = 0
    app.creativeThemeColor = None
    app.showRed = True
    newGame(app)

def newGame(app):
    app.angle1, app.angle2, app.angle3, app.angle4 = 0, 0, 0, 0
    app.gameOverLost = False
    app.gameOverWon = False
    app.clickedSet = []
    app.width = 1000
    app.height = 600
    app.playScreenCounter = 0
    app.errorMessage1 = False
    app.errorMessage2 = False
    app.errorMessage3 = False
    app.errorMessage4 = False
    app.borderColor = 'black'
    app.isHighlighted = False
    app.mouseX = 0
    app.mouseY = 0
    app.wonGame = False
    app.lostGame = False
    app.movingTextSize = 30



####################################################
# Code used by multiple screens
####################################################

def onKeyPressHelper(app, key):
    # Since every screen does the same thing on key presses, we can
    # write the main logic here and just have them call this helper fn
    # You should add/edit some code here...
    if   key == 'd': setActiveScreen('setDimsScreen')
    elif key == 't': setActiveScreen('setThemeScreen')
    elif key == '?': setActiveScreen('helpScreen')
    elif key == 'p': setActiveScreen('playScreen')
    elif key == 'n': #starts new game
        newGame(app)
        #color of cards gets reset in case you are in creative theme (creative element)
        app.creativeThemeColor = None
        app.seconds = 0
        app.lives = 2
        app.rounds = 4
        app.randomBoardAndSet = getRandomBoardWithSet(app.currDims, 8)
        app.board = app.randomBoardAndSet[0]
        app.foundSet = app.randomBoardAndSet[1]
        setActiveScreen('playScreen')

def drawScreenTitle(app, screenTitle):
    drawLabel(screenTitle, app.width/2, 50, size=16, bold=True)
    drawLabel('SuperSet!', app.width/2, 20, size=20, bold=True)





####################################################
# helpScreen
####################################################

def helpScreen_redrawAll(app):
    drawScreenTitle(app, 'Help Screen')
    drawLabel('Press p to play', app.width / 2, 100, size=16)
    drawLabel('Press n to start a new game', app.width / 2, 120, size=16)
    drawLabel('Press d to set dimensions (number of features and options)', app.width / 2, 140, size=16)
    drawLabel('Press t to set theme (how cards look)', app.width / 2, 160, size=16)
    drawLabel('Press ? to show help screen (this screen)', app.width / 2, 180, size=16)
    drawLabel('When playing, press h for hints', app.width / 2, 200, size=16)
    drawLine(100, 220, 900, 220)
    drawLabel('To play SuperSet, you must select a set of cards such that for each feature,', app.width / 2, 240, size = 16)
    drawLabel('they are either all the same or all different. For example,', app.width / 2, 260, size = 16)
    drawLabel('AAA - BAC - CAB is a set since all first characters are different, all', app.width / 2, 280, size = 16)
    drawLabel('second characters are the same, and all third characters are different.', app.width / 2, 300, size = 16)
    #growing text (part of creative element)
    drawLabel('Press p or n to play!', app.width / 2, app.height / 1.5, size = app.movingTextSize, bold = True, fill = 'blue')


def helpScreen_onStep(app):
    #makes the text grow 
    app.movingTextSize += 1
    if app.movingTextSize == 50:
        app.movingTextSize = 30


def helpScreen_onKeyPress(app, key):
    onKeyPressHelper(app, key)

####################################################
# setDimsScreen
####################################################

def setDimsScreen_onScreenActivate(app):
    print('''

********************************************
You just activated the setDims Screen!
You can put code here (in setDimsScreen_onScreenActivate)
to do something each time the user activates this screen.
********************************************
''')

def setDimsScreen_redrawAll(app):
    drawLabel('A few rules for dimensions:', 500, 100, size=16, fill = 'blue', bold = True)
    if app.theme == 0:
        drawLabel('It looks like you are using the Letter Theme', 500, 120, fill = 'blue')
        drawLabel('You must have 5 or fewer features and at least 2 features (items in the list)', 500, 140)
        drawLabel('Dimensions can have at MOST one 5 and must sum to 15 or less (or else app is too slow)', 500, 160)
    elif app.theme == 1:
        drawLabel('It looks like you are using the Standard Theme', 500, 120, fill = 'blue')
        drawLabel('You must have at most 4 features and at least 2 features (items in the list).', 500, 140)
        drawLabel('The only number inputted can be 3. If this rule is broken, Letter Theme will automatically start.', 500, 160)
        drawLabel('Dimensions must sum to 15 or less (or else app is too slow)', 500, 180)

    elif app.theme == 2:
        drawLabel('It looks like you are using the Special Theme', 500, 120, fill = 'blue')
        drawLabel('You must have at most 4 features and at least 2 features (items in the list)', 500, 140)
        drawLabel('You cannot input a number greater than 4 or less than 3. If this rule is broken, Letter Theme will automatically start.', 500, 160)
        drawLabel('Dimensions must sum to 15 or less (or else app is too slow)', 500, 180)
    
    elif app.theme == 3:
        drawLabel("It looks like you are using Daphne's Creative Theme", 500, 120, fill = 'blue')
        drawLabel('You must have at most 4 features and at least 2 features (items in the list).', 500, 140)
        drawLabel('You cannot input a number greater than 4 or less than 3. If this rule is broken, Letter Theme will automatically start.', 500, 160)
        drawLabel('Dimensions must sum to 15 or less (or else app is too slow)', 500, 180)
        
    


        

    drawLabel(f'Current dimensions: {app.currDims}', 500, app.height / 2 - 20, size=16)
    drawLabel(f'Type your new dimensions: {app.newDims}', 500, app.height / 2 + 20, size=16)
    drawLabel('Hit enter when done', 500, app.height / 2 + 40, size = 16)
    drawScreenTitle(app, 'Set Dimensions Screen')
    if app.errorMessage1:
        drawLabel('Must have 5 or fewer features!', 500, 250, fill = 'red', size=16)
    elif app.errorMessage2:
        drawLabel('Must have at least 2 features!', 500, 250, fill='red', size=16)
    elif app.errorMessage3:
        drawLabel('Dims can have at most one 5 (or app is too slow)', 500, 250, fill='red', size=16)
    elif app.errorMessage4:
        drawLabel('Dims must sum to 15 or less (or app is too slow)', 500, 250, fill='red', size=16)


def setDimsScreen_onKeyPress(app, key):
    app.errorMessage1 = False
    app.errorMessage2 = False
    app.errorMessage3 = False
    app.errorMessage4 = False
    
    if key == 'p': 
        app.newDims = copy.copy(app.currDims)
    
    if key == 'backspace':
        app.newDims = app.newDims[:-1]
       
    elif key.isdigit():
        if (key == '3' or key == '4' or key == '5') :
            app.newDims.append(int(key))
        
    elif key == 'enter':
        if 1 < len(app.newDims) < 6:
            sum = 0
            for dim in app.newDims:
                sum += dim
            if sum > 15:
                app.errorMessage4 = True
            if app.newDims.count(5) > 1:
                app.errorMessage3 = True
            else:
                app.currDims = copy.copy(app.newDims)
                app.randomBoardAndSet = getRandomBoardWithSet(app.currDims, 8)
                app.board = app.randomBoardAndSet[0]
                app.foundSet = app.randomBoardAndSet[1]

                app.cardsInSet = min(app.currDims)
                setActiveScreen('playScreen')
        
        elif len(app.newDims) > 5:
            app.errorMessage1 = True
        elif len(app.newDims) < 2:
            app.errorMessage2 = True
        


        
    onKeyPressHelper(app, key)

def outRange(app):
    if app.theme == 1:
        if len(app.newDims) > 4:
            return True
        for num in app.newDims:
            if num > 3:
                return True
        return False
    elif app.theme == 2 or app.theme == 3:
        if len(app.newDims) > 4:
            return True
        for num in app.newDims:
            if num > 4:
                return True
        return False

####################################################
# setThemeScreen
####################################################

def setThemeScreen_redrawAll(app):
    drawScreenTitle(app, 'Set Theme Screen')
    drawLabel('Choose a Theme:', app.width / 2, 140, size = 16, bold = True)
    drawLabel('Letter Theme', app.width / 2, 180, size=16, fill = 'red' if app.theme == 0 else 'black')
    drawLabel('Standard Theme', app.width / 2, 200, size = 16, fill = 'red' if app.theme == 1 else 'black')
    drawLabel('Special Theme', app.width / 2, 220, size = 16, fill = 'red' if app.theme == 2 else 'black')
    drawLabel("Daphne's Creative Theme", app.width / 2, 240, size = 16, fill = 'red' if app.theme == 3 else 'black')
    drawLabel('OR click r and you will randomly be selected a theme', app.width / 2, 260, size = 16, bold = True)

def setThemeScreen_onKeyPress(app, key):
    if key == 'down':
        if app.theme < 3:
            app.theme += 1
    elif key == 'up':
        if app.theme > 0:
            app.theme -= 1
    elif key == 'r':
        app.theme = random.randint(0,3)
        setActiveScreen('playScreen')
    
        
    onKeyPressHelper(app, key)

####################################################
# playScreen
####################################################

def playScreen_redrawAll(app):
    drawScreenTitle(app, 'Play Screen')
    drawLabel('Click on cards to select and deselect', 500, 70, size = 16)
    drawLabel('Press h for hints (hints cost 15 seconds each)', 500, 90, size = 16)
    drawLabel(f'Select a set with {app.cardsInSet} cards', 500, 110, size = 16)
    if app.theme == 3 and not outRange(app):
        drawLabel("Since you are on Daphne's Creative Theme, you may click 7 to change the color of the cards!", 500, 130, size = 16, bold = True)
    if app.rounds !=0 and app.lives != 0:
        
        
        # this is for the top row of the board (first 4 cards)
        for i in range(len(app.board) // 2):

            if app.board[i] in app.clickedSet:
                color = 'yellow'
                dashes = True
                if len(app.clickedSet) == len(app.foundSet) and isSet(app.clickedSet):
                    color = 'green'
                    drawLabel('Correct! Press any key or mouse to continue', 500, 150, size=16, fill='green')
                elif len(app.clickedSet) == len(app.foundSet) and not isSet(app.clickedSet):
                    color = 'red'
                    drawLabel('Those cards do not form a set. Press any key or mouse to continue.', 500, 150, size=16, fill='red')
            else:
                dashes = False
                color = 'black'
           
            drawRect(200 + 150*i, 170, 120, 180, borderWidth = 6, border = color, fill = app.creativeThemeColor if (app.theme == 3 and not outRange(app)) else None, dashes = dashes)
            #reverts back to letter theme if any other theme is out of range (dimensions)
            if app.theme == 0 or outRange(app):
                drawLabel(str(app.board[i]), 260 + 150*i, 260, size = 28, bold = True)
            if not outRange(app):

                if app.theme == 1:
                    drawBoardTheme1(app, 170, 0)
                elif app.theme == 2:
                    drawBoardTheme2(app, 170, 0)
                elif app.theme == 3:
                    drawBoardTheme3(app, 170, 0)

        # this is for the bottom row of the board (last 4 cards)
        for i in range(len(app.board) // 2):

            if app.board[i+4] in app.clickedSet:
                dashes = True
                color = 'yellow'
                if len(app.clickedSet) == len(app.foundSet) and isSet(app.clickedSet):
                    color = 'green'
                    drawLabel('Correct! Press any key or mouse to continue', 500, 150, size=16, fill='green')
    
                elif len(app.clickedSet) == len(app.foundSet) and not isSet(app.clickedSet):
                    color = 'red'
                    drawLabel('Those cards do not form a set. Press any key or mouse to continue.', 500, 150, size=16, fill='red')
    
            
            else:
                dashes = False
                color = 'black'
     
            drawRect(200 + 150*i, 395, 120, 180, borderWidth = 6, border = color, fill = app.creativeThemeColor if (app.theme == 3 and not outRange(app)) else None, dashes = dashes)
            #reverts back to letter theme if any other theme is out of range (dimensions)
            if app.theme == 0 or outRange(app):
                drawLabel(str(app.board[i + 4]), 260 + 150*i, 485, size = 28, bold = True)
            if not outRange(app):
                if app.theme == 1:
                    drawBoardTheme1(app, 395, 4)
                elif app.theme == 2:
                    drawBoardTheme2(app, 395, 4)
                elif app.theme == 3:
                    drawBoardTheme3(app, 395, 4)
    
    if app.gameOverWon:

        drawRect(0, 0, app.width, app.height, fill =gradient('paleGreen', 'green'))
        #draws stars that are randomly placed so that it seems like they are shimmering
        for i in range(20):
            randomCx = random.randint(0, app.width)
            randomCy = random.randint(0, app.width)
            drawStar(randomCx, randomCy, 10, 4, fill = random.choice(['goldenrod', 'lightYellow', 'yellow']))
        drawLabel(f'You won in {app.seconds} seconds!', 500, 300, size=50, bold = True, fill = 'black')
        drawLabel('Press n for new game', 500, 350, size = 16, fill = 'black')
    
        
        
    elif app.gameOverLost:
        drawRect(0, 0, app.width, app.height, fill =gradient('tomato', 'red') if app.showRed else 'black')
        drawLabel('Game over. You lost :(', 500, 300, size=50, bold = True, fill = 'black' if app.showRed else 'white')
        drawLabel('Press n for new game', 500, 350, size = 16, fill = 'black' if app.showRed else 'white')


    
    if not app.gameOverWon and not app.gameOverLost:
        drawLabel('Timer:', 108, 200, size=20)
        drawLabel(f'{app.seconds}', 108, 240, size=20)
        
        drawLabel(f'Rounds:', app.width - 130, app.height / 2, size=16)
        drawLabel(f'Lives:', app.width - 130, app.height / 2 + 20, size=16)
        #draws dots for lives
        for i in range(app.lives):
            drawCircle(app.width - 80 + 22*i, app.height / 2 + 20, 8, fill = 'red')
        #draws dots for rounds
        for i in range(app.rounds): 
            drawCircle(app.width - 80 + 22*i, app.height / 2, 8, fill = 'blue')


#drawing the standard theme
def drawBoardTheme1(app, y, index):
    #setting the standard features in case they are not looped over
    opacity = 100
    numShapes = 1
    for i in range(len(app.board) // 2): #looping over each card
        for j in range(len(app.board[i])):#looping over each letter in the card
            if j == 0: 
                if app.board[i + index][j] == 'A':
                    shape = 'oval'
                elif app.board[i + index][j] == 'B':
                    shape = 'star'
                elif app.board[i + index][j] == 'C':
                    shape = 'polygon'
            elif j ==  1:
                if app.board[i + index][j] == 'A':
                    color = 'red'
                    border = 'red'
                elif app.board[i + index][j] == 'B':
                    color = 'green'
                    border = 'green'
                elif app.board[i + index][j] == 'C':
                    color = 'blue'
                    border = 'blue'
            elif j == 2:
                if app.board[i + index][j] == 'A':
                    numShapes = 1
                elif app.board[i + index][j] == 'B':
                    numShapes = 2
                elif app.board[i + index][j] == 'C':
                    numShapes = 3

            elif j == 3:
                if app.board[i + index][j] == 'A':
                    opacity = 100
                    color = 'white'
                elif app.board[i + index][j] == 'B':
                    opacity = 20
                elif app.board[i + index][j] == 'C':
                    opacity = 100


        for x in range(numShapes):

            centerY = y + (180 / numShapes)*(x+1) - (90 / numShapes)
            centerX = 260 + 150*i
            if shape == 'oval':
                drawOval(centerX, centerY, 84, 42, fill = color, border = border, borderWidth = 4, opacity = opacity)
            elif shape == 'star':
                drawStar(centerX, centerY, 25.2, 5, fill = color, border = border, borderWidth = 4, opacity = opacity)
            elif shape == 'polygon':
                drawRegularPolygon(centerX, centerY, 25, 4, fill = color, border = border, borderWidth = 4, opacity = opacity)

#drawing the special theme
def drawBoardTheme2(app, y, index):
    for i in range(len(app.board) // 2): #looping over each card
        #setting the standard features in case they are not looped over
        angle = app.angle1
        border = 2
        dashes = False
        for j in range(len(app.board[i])):#looping over each letter in the card
            if j == 0:
                if app.board[i + index][j] == 'A':
                    points = 3
                elif app.board[i + index][j] == 'B':
                    points = 4
                elif app.board[i + index][j] == 'C':
                    points = 5
                elif app.board[i + index][j] == 'D':
                    points = 6
            elif j == 1:
                if app.board[i + index][j] == 'A':
                    color = 'orange'
                elif app.board[i + index][j] == 'B':
                    color = 'pink'
                elif app.board[i + index][j] == 'C':
                    color = 'cyan'
                elif app.board[i + index][j] == 'D':
                    color = 'purple'
            elif j == 2:
                if app.board[i + index][j] == 'A':
                    angle = app.angle1
                elif app.board[i + index][j] == 'B':
                    angle = app.angle2
                elif app.board[i + index][j] == 'C':
                    angle = app.angle3
                elif app.board[i + index][j] == 'D':
                    angle = app.angle4
            elif j == 3:
                if app.board[i + index][j] == 'A':
                    dashes = False
                    border = 2
                elif app.board[i + index][j] == 'B':
                    dashes = True
                elif app.board[i + index][j] == 'C':
                    dashes = False
                    border = 5
                elif app.board[i + index][j] == 'D':
                    border = 0

        centerY = y + 90
        centerX = 260 + 150*i
        drawRegularPolygon(centerX, centerY, 40, points, fill = color, border = 'black', rotateAngle = angle, borderWidth = border, dashes = dashes)

#drawing my creative theme (part of creative element)
def drawBoardTheme3(app, y, index):
    #setting the standard features in case they are not looped over

    spin = 0
    numShapes = 1
    for i in range(len(app.board) // 2): #looping over each card
        for j in range(len(app.board[i])):#looping over each letter in the card
            if j == 0: 
                if app.board[i + index][j] == 'A':
                    points = 3
                elif app.board[i + index][j] == 'B':
                    points = 4
                elif app.board[i + index][j] == 'C':
                    points = 5
                elif app.board[i + index][j] == 'D':
                    points = 6
            elif j ==  1:
                if app.board[i + index][j] == 'A':
                    color = 'plum'
                elif app.board[i + index][j] == 'B':
                    color = 'mediumTurquoise'
                elif app.board[i + index][j] == 'C':
                    color = 'darkSeaGreen'
                elif app.board[i + index][j] == 'D':
                    color = 'magenta'
            elif j == 2:
                if app.board[i + index][j] == 'A':
                    numShapes = 1
                elif app.board[i + index][j] == 'B':
                    numShapes = 2
                elif app.board[i + index][j] == 'C':
                    numShapes = 3
                elif app.board[i + index][j] == 'D':
                    numShapes = 4
            elif j == 3:
                if app.board[i + index][j] == 'A':
                    spin = app.angle1
                elif app.board[i + index][j] == 'B':
                    spin = app.angle2
                elif app.board[i + index][j] == 'C':
                    spin = app.angle3
                elif app.board[i + index][j] == 'D':
                    spin = app.angle4


        for x in range(numShapes):
            centerY = y + (180 / numShapes)*(x+1) - (90 / numShapes)
            centerX = 260 + 150*i
            drawStar(centerX, centerY, 20, points, fill = color, border = 'black' if app.creativeThemeColor == None else 'white', rotateAngle = spin)


def playScreen_onKeyPress(app, key):
    if app.wonGame and app.rounds != 0:
        app.rounds -= 1
        newGame(app)
        app.randomBoardAndSet = getRandomBoardWithSet(app.currDims, 8)
        app.board = app.randomBoardAndSet[0]
        app.foundSet = app.randomBoardAndSet[1]
        return
    elif app.lostGame and app.lives != 0:
        app.lives -= 1
        newGame(app)
        app.randomBoardAndSet = getRandomBoardWithSet(app.currDims, 8)
        app.board = app.randomBoardAndSet[0]
        app.foundSet = app.randomBoardAndSet[1]
        return
        
    if key == 'h':
        if not app.gameOverWon:
            app.seconds += 15
            
        #checks if the card clicked is not part of the found set, in which case it will remove it which 
        #in turn will unhighlight it
        for i in range(len(app.foundSet)):
            if len(app.clickedSet) > i and app.clickedSet[i] not in app.foundSet:
                app.clickedSet.remove(app.clickedSet[i])
                return
        #checks if the card in the found set is in the clicked set (this is after all possible wrong cards are removed)
        #if it is not in the clicked set, it adds it, which in turn will highlight it.
        for i in range(len(app.foundSet)):
            if app.foundSet[i] not in app.clickedSet:
                app.clickedSet.append(app.foundSet[i])
                return
    
    #changes background of the cards given the theme is the new creative theme
    if key == '7' and app.theme == 3 and not outRange(app):
        colors = ['thistle', 'black', 'royalBlue', 'paleVioletRed', 'silver', 'lime', 'crimson']
        app.creativeThemeColor = gradient(random.choice(colors), random.choice(colors), start='bottom')
        
            
    onKeyPressHelper(app, key)

def playScreen_onMousePress(app, mouseX, mouseY):
    if app.wonGame and app.rounds != 0:
        app.rounds -= 1
        app.randomBoardAndSet = getRandomBoardWithSet(app.currDims, 8)
        app.board = app.randomBoardAndSet[0]
        app.foundSet = app.randomBoardAndSet[1]
        newGame(app)
    elif app.lostGame and app.lives != 0:
        app.lives -= 1
        app.randomBoardAndSet = getRandomBoardWithSet(app.currDims, 8)
        app.board = app.randomBoardAndSet[0]
        app.foundSet = app.randomBoardAndSet[1]
        newGame(app) 
    
    #checks if the person clicked on a card in the top row
    #if so, it gets added to the clicked set which highlights it
    for i in range(len(app.board) // 2):
        if 200 + 150*i <= mouseX <= 320 + 150*i and 170 <= mouseY <= 350:
            if app.board[i] not in app.clickedSet:
                app.clickedSet.append(app.board[i])
            else:
                app.clickedSet.remove(app.board[i])

    #checks the bottom row for the same conditions as seen above
    for i in range(len(app.board) // 2):
        if 200 + 150*i <= mouseX <= 320 + 150*i and 395 <= mouseY <= 575:
            if app.board[i+4] not in app.clickedSet:
                app.clickedSet.append(app.board[i+4])
            else:
                app.clickedSet.remove(app.board[i+4])


    
    
    

    
def playScreen_onStep(app):
    #spin speeds for special feature and creative feature
    app.angle1 += 10
    app.angle2 -= 10
    app.angle3 += 5
    app.angle4 -= 5
    app.playScreenCounter += 1
    if app.playScreenCounter % 30 == 0 and not app.gameOverWon:
        app.seconds += 1
    
    if len(app.clickedSet) == len(app.foundSet) and isSet(app.clickedSet):
        app.wonGame = True

    if len(app.clickedSet) == len(app.foundSet) and not isSet(app.clickedSet):
        app.lostGame = True 
    
    if app.lives == 0:
        #makes the flashing red screen when you lose
        if app.playScreenCounter % 15 == 0:
            app.showRed = not app.showRed
        #resets background of cards in case you are on the creative theme (creative element)
        app.creativeThemeColor = None
        app.gameOverLost = True

    if app.rounds == 0:
        #resets background of cards in case you are on the creative theme (creative element)
        app.creativeThemeColor = None
        app.gameOverWon = True

    

###############################################
# Functions copied from console-based app
###############################################

# Copy-Paste required code from console-based app here!
# Just copy your helper functions along with stringProduct() and
# combinations().  You do not need to copy the
# "Console-Based playSuperSet (for debugging)" section.

def stringProduct(L):
    # This helper function (which is extremely useful for makeSuperSetDeck)
    # is provided for students, since it uses some concepts we have not
    # yet covered.  This takes a list of strings and returns a list of
    # their product -- that is, a list of strings where the first character
    # is any letter from the first string, the second character is the any
    # letter from the second string, and so on.
    # For example:
    # stringProduct(['AB', 'CDE']) returns ['AC', 'AD', 'AE', 'BC', 'BD', 'BE']
    # Also:
    # stringProduct(['AB', 'CD', 'EFG']) returns ['ACE', 'ACF', 'ACG', 'ADE',
    #                                             'ADF', 'ADG', 'BCE', 'BCF',
    #                                             'BCG', 'BDE', 'BDF', 'BDG']   
    resultTuples = list(itertools.product(*L))
    resultStrings = [''.join(t) for t in resultTuples]
    return resultStrings

def combinations(L, n):
    # This helper function (which is extremely useful for findFirstSet)
    # is provided for students, since it uses some concepts we have not
    # yet covered.  
    # Given a list of values L and a non-negative integer n,
    # this function returns a list of all the possible lists
    # made up of any n values in L.
    # For example:
    # combinations(['A', 'B', 'C', 'D'], 2) returns:
    # [['A', 'B'], ['A', 'C'], ['A', 'D'], ['B', 'C'], ['B', 'D'], ['C', 'D']]
    # See how this is a list of all the possible lists made up of
    # any 2 values in L.
    # Also, order does not matter.  See how ['A', 'B'] is in the result
    # and so ['B', 'A'] is not.
    return [list(v) for v in itertools.combinations(L, n)]

###############################################
# Functions for you to write
###############################################

def allSame(L):
    prevElem = None
    for elem in L:
        if prevElem == None:
            prevElem = elem
        if elem != prevElem:
            return False
    return True
    # Returns True if all the values in the list L are equal and False
    # otherwise.  You may assume L is non-empty.

def allDiffer(L):
    seenElems = []
    for elem in L:
        if seenElems == []:
            seenElems.append(elem)
            continue
        if elem in seenElems:
            return False
        seenElems.append(elem)
    return True
    # Returns True if all the values in the list L are different and False
    # otherwise.  You may assume L is non-empty.

def isSet(cards):
    numCards = len(cards)
    numFeatures = len(cards[0])
    for i in range(numFeatures):
        possibleSet = []
        for j in range(numCards):
            possibleSet.append(cards[j][i])
        if not allDiffer(possibleSet) and not allSame(possibleSet):
            return False
    return True
    # Given a list of cards, return True if those cards form a set,
    # and False otherwise.
    # Here you may assume the list of cards is non-empty and that each card
    # is a string of valid options from the same list of possible features.
    # Thus, just confirm that for every feature, every card either has the
    # same option or every card has a different option.

def makeSuperSetDeck(dims):
    allStrings = []
    for i in range(len(dims)):
        card = ''
        for j in range(dims[i]):
            newLetter = chr(ord('A') + j)
            card += newLetter
        allStrings.append(card)
    return stringProduct(allStrings)
    # This generates all possible cards with the given dimensions
    # and returns them in a sorted list.
    # For example, consider makeSuperSetDeck([3,4]):
    # Here, there are two features:
    #     * feature0 has 3 features ('A', 'B', or 'C')
    #     * feature1 has 4 features ('A', 'B', 'C', or 'D')
    # Each card in the deck includes an option from each feature,
    # resulting in this deck:
    # ['AA', 'AB', 'AC', 'AD', 'BA', 'BB', 'BC', 'BD', 'CA', 'CB', 'CC', 'CD']
    # Thus, makeSuperSetDeck([3,4]) returns that list.
    # Hint: use stringProduct() here!

def boardContainsSelection(board, selection):
    for card in selection:
        if card not in board:
            return False
    return True
    # helper function for checkSelectionIsSet()
    # Return True if every card in the selection (a list of cards) is
    # also on the board (another list of cards), and False otherwise.

def checkSelectionIsSet(board, selection, cardsPerSet):
    if board == []:
        return 'Empty board!'
    elif len(selection) != cardsPerSet:
        return 'Wrong number of cards!'
    elif not boardContainsSelection(board, selection):
        return 'Some of those cards are not on the board!'
    elif not allDiffer(selection):
        return 'Some of those cards are duplicates!'
    elif not isSet(selection):
        return 'Those cards do not form a set!'
    return True 
    # Given a board (a list of cards from the deck), a selection
    # (a non-empty list of cards on the board), and the cardsPerSet
    # (a positive number of cards required to make a set), return True
    # if the selection is legal and in fact forms a set.
    # Instead of returning False, return a string with a
    # description of why the selection is not a set, as such:
    # 1. If the board is empty, return 'Empty board!'
    # 2. If the number of cards in the selection does not match the
    #    required number of cards in a set, return 'Wrong number of cards!'
    # 3. If any of the cards in the selection are not actually on the board,
    #    return 'Some of those cards are not on the board!'
    # 4. If any of the cards in the selection are duplicates,
    #    return 'Some of those cards are duplicates!'
    # 5. If the cards in the selection do not form a legal set,
    #    return 'Those cards do not form a set!'

def findFirstSet(board, cardsPerSet):
    for comb in combinations(board, cardsPerSet):
        if isSet(comb):
            return comb
    return None
    # helper function for dealUntilSetExists()
    # Given a possibly-empty board, and a positive number of cards per set,
    # loop over combinations(board, cardsPerSet) and return the
    # first list of cards that are on the board and form a set.  Return None
    # if there are no sets on the board.
    # Note that this function will be tested when we test dealUntilSetExists.
    # Hint: you will want to use the combinations() helper function
    # that we provided above.

def dealUntilSetExists(deck, cardsPerSet):
    newBoard = []
    i = 0
    while findFirstSet(newBoard, cardsPerSet) == None:
        newBoard.append(deck[i])
        i += 1
    foundSet = findFirstSet(newBoard, cardsPerSet)
    return sorted(foundSet)
    # Start with an empty board.
    # Keep adding cards from the top of the deck (that is, "dealing")
    # (without modifying the deck) to the board until
    # there is a set among the cards in the board.
    # Return a sorted list of just the cards that form that set.
    # Notes:
    #  1. This function does not deal a fixed number of cards.  It keeps
    #     dealing until it finds a set, no matter how many cards that requires.
    #  2. You can ignore the error case where the deck runs out
    #     of cards before a set is found -- that is, you should never return None.
    # Hint: findFirstSet will be useful here.

def getRandomBoardWithSet(dims, targetBoardSize):
    deck = makeSuperSetDeck(dims)
    random.shuffle(deck)
    cardsPerSet = min(dims)
    foundSet = dealUntilSetExists(deck, cardsPerSet)
    board = copy.copy(foundSet)
    for card in deck:
        if card not in board:
            if len(board) != targetBoardSize:
                board.append(card)
    return sorted(board), foundSet
    # Make a new SuperSet deck with the given dimensions,
    # then shuffle the deck, deal cards until a set is dealt.
    # Call that the foundSet.
    # Then, form a board starting with that set, and adding
    # more cards from the deck (that are not already in the set)
    # until the board is the given size.  Then sort and return it
    # in a tuple along with the foundSet.
    # Hint: to randomly shuffle a list L, do this:  random.shuffle(L),
    # which mutatingly shuffles (randomizes the order) of the list L.

####################################################
# main function
####################################################

def main():
    runAppWithScreens(initialScreen='helpScreen')

main()
