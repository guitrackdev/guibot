"""
This class is a collection of interactive actions using pyautogui. The intent
of this class is to define an extra layer between who is doing the gui
interaction's automation and the users. This way an unique Gateway provided
for the user to become technology independent.

Creator: Cristian Rodriguez Canto
Date: Nov-17-2018
"""

import pyautogui, time, sys, os
from tkinter import *

class AutomatedGuiActions:

    #Path to be indepent from context
    internalPath = os.path.abspath(os.path.dirname(__file__))
    #Standard sleep duration for most of the cases. When you do more than
    #one action a lag is needed to wait for the new system UI state
    #appears
    sleepDuration = 0.5

    #Constructor, define mouse velocity
    def __init__(self, UIspeed = "human"):
        if UIspeed == "human":
            self.moveToSpeed = 1
            self.verticalDragRelSpeed = 0.5
            self.simpleScrollSpeed = 1
            self.selectCheckBoxAndTypeTextSpeed = 0.25
            self.dragTopLeftImagedragRelSpeed = 0.5
            self.typeAndEnterSpeed = 0.25
            self.dragToLeftUpperCornerSpeed = 0.7
        #A robot velocity sets the moves and other interactions who don't
        #cause functional troubles to zero.
        if UIspeed == "robot":
            self.moveToSpeed = 0
            self.verticalDragRelSpeed = 0
            self.simpleScrollSpeed = 0
            self.selectCheckBoxAndTypeTextSpeed = 0
            self.dragTopLeftImagedragRelSpeed = 0.2
            self.typeAndEnterSpeed = 0
            self.dragToLeftUpperCornerSpeed = 0.2

    #Search an image and returns the center position
    def SearchCenterImage(self, image):
        import sys
        try:
            x, y = pyautogui.locateCenterOnScreen(image);
        except FileNotFoundError:
            pyautogui.alert(text="Not found file", title='Error on image: ' + image , button='OK')
        except TypeError:
            self.ImageNotFoundInfo(image)
        else:
            return x,y

    #Search an image and returns the top left position
    def SearchTopLeftImage(self, image):
        import sys
        try:
            x, y, z, w = pyautogui.locateOnScreen(image);
        except FileNotFoundError:
            pyautogui.alert(text="Not found file", title='Error on image: ' + image , button='OK')
        except TypeError:
            self.ImageNotFoundInfo(image)
        else:
            return x, y

    #This function Moves to an image and then clicks on it
    def MoveAndLeftClickToImage(self, image):
        x, y = self.SearchCenterImage(image)
        pyautogui.moveTo(x, y, self.moveToSpeed)
        pyautogui.click(x, y)
        time.sleep(self.sleepDuration)

    #This function Moves to an image and then double clicks on it
    #it's a code duplication? yes. It's needed to be improved
    def MoveAndLeftDoubleClickToImage(self, image):
        x, y = self.SearchCenterImage(image)
        pyautogui.moveTo(x, y, self.moveToSpeed)
        pyautogui.doubleClick(x, y)
        time.sleep(self.sleepDuration)

    #This function performs a simple vertical drag in the center of an image
    def SimpleVerticalDrag(self, image):
        self.MoveAndLeftClickToImage(image)
        pyautogui.mouseDown()
        time.sleep(self.sleepDuration)
        pyautogui.dragRel(45, -100, duration = self.verticalDragRelSpeed) # move up
        pyautogui.mouseUp()
        time.sleep(self.sleepDuration)
        pyautogui.press('esc')

    #This function performs a scroll in the center of an image
    def SimpleScroll(self, image):
        pyautogui.click()
        self.MoveAndLeftClickToImage(image)
        pyautogui.scroll(200, self.simpleScrollSpeed)
        #This particular two lines below is just because
        #To be sure that the scroll is made to a non highlighted
        #image. Some images when you clic on then become highlighted
        #that can interfere with the next image recognition.
        #
        #Fell free to modify this without break automated tests
        pyautogui.moveRel(-10,-10)
        pyautogui.click()
        time.sleep(self.sleepDuration)

    #This function clicks on a image of a checkbox, press tab and fill a textbox
    #The context is a checkbox who enabled a text input right next to it
    #so, pressing tab will get me to the text input.
    def SelectCheckBoxAndTypeText(self, image, text):
        self.MoveAndLeftClickToImage(image)
        self.PressTab()
        pyautogui.typewrite(text, interval = self.selectCheckBoxAndTypeTextSpeed)

    #This function clicks on a image of a checkbox, press tab and fill a textbox
    def SelectCheckBoxAndTypeTextVeryFast(self, image, text):
        self.MoveAndLeftClickToImage(image)
        self.PressTab()
        pyautogui.typewrite(text)

    #A simple press wrapper
    def PressTab(self):
        pyautogui.press('tab')

    #A simple press wrapper
    def PressEnter(self):
        pyautogui.press('enter')

    #A simple press wrapper
    def PressText(self, number):
        pyautogui.press(number)

    #Do a right click in the current mouse position
    def RightClick(self):
        pyautogui.rightClick()

    #Type a text
    def TypeAndEnter(self, text):
        pyautogui.typewrite(text, interval = self.typeAndEnterSpeed)
        pyautogui.press('enter')
        time.sleep(self.sleepDuration)

    #Simulates a click and drag of an image for certain pixels
    def DragTopLeftImage(self, image, x, y):
        xMove, yMove = self.SearchTopLeftImage(image)
        pyautogui.moveTo(xMove, yMove, self.moveToSpeed)
        pyautogui.click(xMove, yMove)
        pyautogui.click(xMove+1, yMove+1)
        pyautogui.click(xMove+2, yMove+2)
        pyautogui.mouseDown()
        pyautogui.dragRel(x, y, duration = self.dragTopLeftImagedragRelSpeed)
        pyautogui.mouseUp()

    #This function clicks on an image and drag it to the upper left corner
    #Is used to move windows aside
    def DragToLeftUpperCorner(self, image):
        x, y ,z, w= pyautogui.locateOnScreen(image)
        pyautogui.moveTo(x, y, self.moveToSpeed)
        pyautogui.mouseDown(x, y)
        pyautogui.dragTo(10, 10, self.dragToLeftUpperCornerSpeed)
        pyautogui.mouseUp()

    #This function see 10 times if an image appears in the screens
    #Useful for splash screens or tasks that takes longert than others
    #This method now search the desire image in the top corner, but
    #this info can be parametrized
    #(sleeps for 2 seconds between attempts)
    def WaitUntilSeeImage(self, image):
        i = 1
        while i < 10:
            try:
                x, y = pyautogui.locateCenterOnScreen(image, region=(0,0, 300, 400));
            except Exception:
                pass
            else:
                i = 10
            time.sleep(2)
        i += 1

    #This function creates a window using tkinter and displays the not found image
    #Differs from the pyautogui.alert because that one can't show images
    def ImageNotFoundInfo(self, image):
        root = Tk()
        title = 'Error on image: ' + image
        root.title(title)
        text = "Not found image on screen. Look for a resolution problem or a windows blocking the image you need to find"
        text1 = Text(root, height=20, width=30)
        photo=PhotoImage(file=image)
        text1.insert(END,'\n')
        text1.image_create(END, image=photo)
        text1.pack(side=TOP)
        text2 = Text(root, height=20, width=50)
        scroll = Scrollbar(root, command=text2.yview)
        text2.configure(yscrollcommand=scroll.set)
        text2.tag_configure('big', font=('Verdana', 16, 'bold'))
        text2.tag_bind('follow', '<1>', lambda e, t=text2: t.insert(END, "Not now, maybe later!"))
        text2.insert(END,text, 'big')
        text2.pack(side=LEFT)
        scroll.pack(side=RIGHT, fill=Y)
        root.mainloop()

    #Window only method (Windows 8 or 10, don't know if 7 have this hotkeys)
    #Look for a window and press win + down to hide the window
    def DisposeAWindow(self, image):
        pyautogui.click(pyautogui.locateCenterOnScreen(image))
        pyautogui.keyDown('winleft')
        pyautogui.press('down')
        pyautogui.keyUp('winleft')

def main():
    #This example, and the image that looks for, was tested on a xubuntu
    #machine, in a 1366 x 768 resolution. Change the image for another
    #who works for you. The results must be a mouse move to the center of the image,
    #and a left click.

    core = AutomatedGuiActions()
    core.MoveAndLeftClickToImage('test_images/test.jpeg')

if __name__ == "__main__":
    main()
