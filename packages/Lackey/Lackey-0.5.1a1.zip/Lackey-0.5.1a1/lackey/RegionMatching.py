from PIL import Image, ImageTk
import Tkinter as tk
import subprocess
import tempfile
import platform
import numpy
import time
import cv2
import sys
import os
import re


from .PlatformManagerWindows import PlatformManagerWindows
from .Exceptions import FindFailed
from .Settings import Settings, Debug
from .TemplateMatchers import PyramidTemplateMatcher as TemplateMatcher

if platform.system() == "Windows":
    PlatformManager = PlatformManagerWindows() # No other input managers built yet
else:
    # Avoid throwing an error if it's just being imported for documentation purposes
    if not os.environ.get('READTHEDOCS') == 'True':
        raise NotImplementedError("Lackey is currently only compatible with Windows.")

class Pattern(object):
    """ Defines a pattern based on a bitmap, similarity, and target offset """
    def __init__(self, path):
        ## Loop through image paths to find the image
        found = False
        for image_path in [Settings.BundlePath, os.getcwd()] + Settings.ImagePaths:
            full_path = os.path.join(image_path, path)
            if os.path.exists(full_path):
                # Image file not found
                found = True
                break
        ## Check if path is valid
        if not found:
            raise OSError("File not found: {}".format(path))
        self.path = full_path
        self.similarity = Settings.MinSimilarity
        self.offset = Location(0, 0)

    def similar(self, similarity):
        """ Returns a new Pattern with the specified similarity threshold """
        pattern = Pattern(self.path)
        pattern.similarity = similarity
        return pattern

    def exact(self):
        """ Returns a new Pattern with a similarity threshold of 1.0 """
        pattern = Pattern(self.path)
        pattern.similarity = 1.0
        return pattern

    def targetOffset(self, dx, dy):
        """ Returns a new Pattern with the given target offset """
        pattern = Pattern(self.path)
        pattern.similarity = self.similarity
        pattern.offset = Location(dx, dy)
        return pattern

    def getFilename(self):
        """ Returns the path to this Pattern's bitmap """
        return self.path

    def getTargetOffset(self):
        """ Returns the target offset as a Location(dx, dy) """
        return self.offset

    def debugPreview(self, title="Debug"):
        """ Loads and displays the image at ``Pattern.path`` """
        haystack = cv2.imread(self.path)
        cv2.imshow(title, haystack)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

class Region(object):
    def __init__(self, *args):
        if len(args) == 4:
            x, y, w, h = args
        elif len(args) == 1:
            if isinstance(args[0], Region):
                x, y, w, h = args[0].getTuple()
            elif isinstance(args[0], tuple):
                x, y, w, h = args[0]
            else:
                raise TypeError("Unrecognized argument for Region()")
        else:
            raise TypeError("Unrecognized argument(s) for Region()")
        self.setROI(x, y, w, h)
        self._lastMatch = None
        self._lastMatches = []
        self._lastMatchTime = 0
        self.autoWaitTimeout = 3.0
        # Converts searches per second to actual second interval
        self._defaultScanRate = 1/Settings.WaitScanRate
        self._defaultMouseSpeed = Settings.MoveMouseDelay
        self._defaultTypeSpeed = 0.05
        self._raster = (0, 0)

    def setX(self, x):
        """ Set the x-coordinate of the upper left-hand corner """
        self.x = int(x)
    def setY(self, y):
        """ Set the y-coordinate of the upper left-hand corner """
        self.y = int(y)
    def setW(self, w):
        """ Set the width of the region """
        self.w = int(w)
    def setH(self, h):
        """ Set the height of the region """
        self.h = int(h)

    def getX(self):
        """ Get the x-coordinate of the upper left-hand corner """
        return self.x
    def getY(self):
        """ Get the y-coordinate of the upper left-hand corner """
        return self.y
    def getW(self):
        """ Get the width of the region """
        return self.w
    def getH(self):
        """ Get the height of the region """
        return self.h

    def moveTo(self, location):
        """ Change the upper left-hand corner to a new ``Location``

        Doesn't change width or height
        """
        if not location or not isinstance(location, Location):
            raise ValueError("moveTo expected a Location object")
        self.x = location.x
        self.y = location.y
        return self

    def setROI(self, *args):
        """ Set Region of Interest (same as Region.setRect()) """
        if len(args) == 4:
            x, y, w, h = args
        elif len(args) == 1:
            if isinstance(args[0], Region):
                x, y, w, h = args[0].getTuple()
            elif isinstance(args[0], tuple):
                x, y, w, h = args[0]
            else:
                raise TypeError("Unrecognized argument for Region()")
        else:
            raise TypeError("Unrecognized argument(s) for Region()")
        self.setX(x)
        self.setY(y)
        self.setW(w)
        self.setH(h)
    setRect = setROI

    def morphTo(self, region):
        """ Change shape of this region to match the given ``Region`` object """
        if not region or not isinstance(region, Region):
            raise TypeError("morphTo expected a Region object")
        self.setROI(region.x, region.y, region.w, region.h)
        return self

    def getCenter(self):
        """ Return the ``Location`` of the center of this region """
        return Location(self.x+(self.w/2), self.y+(self.h/2))
    def getTopLeft(self):
        """ Return the ``Location`` of the top left corner of this region """
        return Location(self.x, self.y)
    def getTopRight(self):
        """ Return the ``Location`` of the top right corner of this region """
        return Location(self.x+self.w, self.y)
    def getBottomLeft(self):
        """ Return the ``Location`` of the bottom left corner of this region """
        return Location(self.x, self.y+self.h)
    def getBottomRight(self):
        """ Return the ``Location`` of the bottom right corner of this region """
        return Location(self.x+self.w, self.y+self.h)

    def getScreen(self):
        """ Return an instance of the ``Screen`` object this region is inside.

        Checks the top left corner of this region (if it touches multiple screens) is inside.
        Returns None if the region isn't positioned in any screen.
        """
        screens = PlatformManager.getScreenDetails()
        for screen in screens:
            s_x, s_y, s_w, s_h = screen["rect"]
            if (self.x >= s_x) and (self.x < s_x + s_w) and (self.y >= s_y) and (self.y < s_y + s_h):
                # Top left corner is inside screen region
                return Screen(screens.index(screen))
        return None # Could not find matching screen

    def getLastMatch(self):
        """ Returns the last successful ``Match`` returned by ``find()``, ``exists()``, etc. """
        return self._lastMatch
    def getLastMatches(self):
        """ Returns the last successful set of ``Match`` objects returned by ``findAll()`` """
        return self._lastMatches
    def getTime(self):
        """ Returns the elapsed time in milliseconds to find the last match """
        return self._lastMatchTime

    def setAutoWaitTimeout(self, seconds):
        """ Specify the time to wait for an image to appear on the screen """
        self.autoWaitTimeout = float(seconds)
    def getAutoWaitTimeout(self):
        """ Returns the time to wait for an image to appear on the screen """
        return self.autoWaitTimeout
    def setWaitScanRate(self, seconds):
        """Set this Region's scan rate

        A find op should repeat the search for the given Visual rate times per second until
        found or the maximum waiting time is reached.
        """
        if seconds == 0:
            seconds = 3
        self._defaultScanRate = 1/seconds
    def getWaitScanRate(self):
        """ Get the current scan rate """
        return 1/self._defaultScanRate

    def offset(self, location, dy=0):
        """ Returns a new ``Region`` offset from this one by ``location``

        Width and height remain the same
        """
        if not isinstance(location, Location):
            # Assume variables passed were dx,dy
            location = Location(location, dy)
        r = Region(self.x+location.x, self.y+location.y, self.w, self.h).clipRegionToScreen()
        if r is None:
            raise FindFailed("Specified region is not visible on any screen")
            return None
        return r
    def grow(self, width, height=None):
        """ Expands the region by ``width`` on both sides and ``height`` on the top and bottom.

        If only one value is provided, expands the region by that amount on all sides.
        Equivalent to ``nearby()``.
        """
        if height is None:
            return self.nearby(width)
        else:
            return Region(
                self.x-width,
                self.y-height,
                self.w+(2*width),
                self.h+(2*height)).clipRegionToScreen()
    def inside(self):
        """ Returns the same object. Included for Sikuli compatibility. """
        return self
    def nearby(self, expand=50):
        """ Returns a new Region that includes the nearby neighbourhood of the the current region.

        The new region is defined by extending the current region's dimensions
        all directions by range number of pixels. The center of the new region remains the
        same.
        """
        return Region(
            self.x-expand,
            self.y-expand,
            self.w+(2*expand),
            self.h+(2*expand)).clipRegionToScreen()
    def above(self, expand=None):
        """ Returns a new Region above the current region with a height of ``expand`` pixels.

        Does not include the current region. If range is omitted, it reaches to the top of the
        screen. The new region has the same width and x-position as the current region.
        """
        if expand == None:
            x = self.x
            y = 0
            w = self.w
            h = self.y
        else:
            x = self.x
            y = self.y - expand
            w = self.w
            h = expand
        return Region(x, y, w, h).clipRegionToScreen()
    def below(self, expand=None):
        """ Returns a new Region below the current region with a height of ``expand`` pixels.

        Does not include the current region. If range is omitted, it reaches to the bottom
        of the screen. The new region has the same width and x-position as the current region.
        """
        if expand == None:
            x = self.x
            y = self.y+self.h
            w = self.w
            h = self.getScreen().getBounds()[3] - y # Screen height
        else:
            x = self.x
            y = self.y + self.h
            w = self.w
            h = expand
        return Region(x, y, w, h).clipRegionToScreen()
    def left(self, expand=None):
        """ Returns a new Region left of the current region with a width of ``expand`` pixels.

        Does not include the current region. If range is omitted, it reaches to the left border
        of the screen. The new region has the same height and y-position as the current region.
        """
        if expand == None:
            x = 0
            y = self.y
            w = self.x
            h = self.h
        else:
            x = self.x-expand
            y = self.y
            w = expand
            h = self.h
        return Region(x, y, w, h).clipRegionToScreen()
    def right(self, expand=None):
        """ Returns a new Region right of the current region with a width of ``expand`` pixels.

        Does not include the current region. If range is omitted, it reaches to the right border
        of the screen. The new region has the same height and y-position as the current region.
        """
        if expand == None:
            x = self.x+self.w
            y = self.y
            w = self.getScreen().getBounds()[2] - x
            h = self.h
        else:
            x = self.x+self.w
            y = self.y
            w = expand
            h = self.h
        return Region(x, y, w, h).clipRegionToScreen()

    def getBitmap(self):
        """ Captures screen area of this region, at least the part that is on the screen

        Returns image as numpy array
        """
        return PlatformManager.getBitmapFromRect(self.x, self.y, self.w, self.h)
    def debugPreview(self, title="Debug"):
        """ Displays the region in a preview window.

        If the region is a Match, circles the target area. If the region is larger than half the
        primary screen in either dimension, scales it down to half size.
        """
        region = self
        haystack = self.getBitmap()
        if isinstance(region, Match):
            cv2.circle(
                haystack,
                (region.getTarget().x - self.x, region.getTarget().y - self.y),
                5,
                255)
        if haystack.shape[0] > (Screen(0).getBounds()[2]/2) or haystack.shape[1] > (Screen(0).getBounds()[3]/2):
            # Image is bigger than half the screen; scale it down
            haystack = cv2.resize(haystack, (0, 0), fx=0.5, fy=0.5)
        cv2.imshow(title, haystack)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    def highlight(self, seconds=1):
        """ Temporarily using ``debugPreview()`` to show the region instead of highlighting it

        Probably requires transparent GUI creation/manipulation. TODO
        """
        PlatformManager.highlight((self.getX(), self.getY(), self.getW(), self.getH()), seconds)

    def find(self, pattern):
        """ Searches for an image pattern in the given region

        Throws ``FindFailed`` exception if the image could not be found.
        Sikuli supports OCR search with a text parameter. This does not (yet).
        """
        match = self.exists(pattern)
        if match is None:
            path = pattern.path if isinstance(pattern, Pattern) else pattern
            raise FindFailed("Could not find pattern '{}'".format(path))
            return None
        return match
    def findAll(self, pattern):
        """ Searches for an image pattern in the given region

        Returns ``Match`` object if ``pattern`` exists, empty array otherwise (does not
        throw exception). Sikuli supports OCR search with a text parameter. This does not (yet).
        """
        find_time = time.time()
        r = self.clipRegionToScreen()
        if r is None:
            raise FindFailed("Region outside all visible screens")
            return None
        seconds = self.autoWaitTimeout
        if isinstance(pattern, int):
            time.sleep(pattern)
            return
        if not pattern:
            time.sleep(seconds)
        if not isinstance(pattern, Pattern):
            if not isinstance(pattern, basestring):
                raise TypeError("find expected a string [image path] or Pattern object")
            pattern = Pattern(pattern)
        needle = cv2.imread(pattern.path)
        if needle is None:
            raise ValueError("Unable to load image '{}'".format(pattern.path))
        needle_height, needle_width, needle_channels = needle.shape
        positions = []
        timeout = time.time() + seconds

        # Check TemplateMatcher for valid matches
        matches = []
        while time.time() < timeout and len(matches) == 0:
            matcher = TemplateMatcher(r.getBitmap())
            matches = matcher.findAllMatches(needle, pattern.similarity)
            time.sleep(self._defaultScanRate)

        if len(matches) == 0:
            Debug.info("Couldn't find '{}' with enough similarity.".format(pattern.path))
            return iter([])

        # Matches found! Turn them into Match objects
        lastMatches = []
        for match in matches:
            position, confidence = match
            x, y = position
            lastMatches.append(
                Match(
                    confidence,
                    pattern.offset,
                    ((x+self.x, y+self.y), (needle_width, needle_height))))
        self._lastMatches = iter(lastMatches)
        Debug.info("Found match(es) for pattern '{}' at similarity ({})".format(pattern.path, pattern.similarity))
        self._lastMatchTime = (time.time() - find_time) * 1000 # Capture find time in milliseconds
        return self._lastMatches

    def wait(self, pattern, seconds=3):
        """ Searches for an image pattern in the given region, given a specified timeout period

        Functionally identical to find()
        Sikuli supports OCR search with a text parameter. This does not (yet).
        """
        if seconds:
            timeout = time.time() + seconds
        else:
            timeout = time.time()
        while True:
            match = self.exists(pattern)
            if match:
                return match
            if time.time() >= timeout:
                break
        path = pattern.path if isinstance(pattern, Pattern) else pattern
        raise FindFailed("Could not find pattern '{}'".format(path))
        return None
    def waitVanish(self, pattern, seconds=None):
        """ Waits until the specified pattern is not visible on screen.

        If ``seconds`` pass and the pattern is still visible, raises FindFailed exception.
        Sikuli supports OCR search with a text parameter. This does not (yet).
        """
        r = self.clipRegionToScreen()
        if r is None:
            raise FindFailed("Region outside all visible screens")
            return None
        if seconds is None:
            seconds = self.autoWaitTimeout
        if isinstance(pattern, int):
            time.sleep(pattern)
            return
        if not pattern:
            time.sleep(seconds)
        if not isinstance(pattern, Pattern):
            if not isinstance(pattern, basestring):
                raise TypeError("find expected a string [image path] or Pattern object")
            pattern = Pattern(pattern)

        needle = cv2.imread(pattern.path)
        match = True
        timeout = time.time() + seconds

        while match and time.time() < timeout:
            matcher = TemplateMatcher(r.getBitmap())
            # When needle disappears, matcher returns None
            match = matcher.findBestMatch(needle, pattern.similarity)
            time.sleep(self._defaultScanRate)
        if match:
            return False
            #self._findFailedHandler(FindFailed("Pattern '{}' did not vanish".format(pattern.path)))
    def exists(self, pattern, seconds=None):
        """ Searches for an image pattern in the given region

        Returns Match if pattern exists, None otherwise (does not throw exception)
        Sikuli supports OCR search with a text parameter. This does not (yet).
        """
        find_time = time.time()
        r = self.clipRegionToScreen()
        if r is None:
            raise FindFailed("Region outside all visible screens")
            return None
        if seconds is None:
            seconds = self.autoWaitTimeout
        if isinstance(pattern, int):
            # Actually just a "wait" statement
            time.sleep(pattern)
            return
        if not pattern:
            time.sleep(seconds)
        if not isinstance(pattern, Pattern):
            if not isinstance(pattern, basestring):
                raise TypeError("find expected a string [image path] or Pattern object")
            pattern = Pattern(pattern)
        needle = cv2.imread(pattern.path)
        if needle is None:
            raise ValueError("Unable to load image '{}'".format(pattern.path))
        needle_height, needle_width, needle_channels = needle.shape
        match = None
        timeout = time.time() + seconds

        # Consult TemplateMatcher to find needle
        while not match and time.time() < timeout:
            matcher = TemplateMatcher(r.getBitmap())
            match = matcher.findBestMatch(needle, pattern.similarity)
            time.sleep(self._defaultScanRate)

        if match is None:
            Debug.info("Couldn't find '{}' with enough similarity.".format(pattern.path))
            return None

        # Translate local position into global screen position
        position, confidence = match
        position = (position[0] + self.x, position[1] + self.y)
        self._lastMatch = Match(
            confidence,
            pattern.offset,
            (position, (needle_width, needle_height)))
        #self._lastMatch.debug_preview()
        Debug.info("Found match for pattern '{}' at ({},{}) with confidence ({}). Target at ({},{})".format(
            pattern.path,
            self._lastMatch.getX(),
            self._lastMatch.getY(),
            self._lastMatch.getScore(),
            self._lastMatch.getTarget().x,
            self._lastMatch.getTarget().y))
        self._lastMatchTime = (time.time() - find_time) * 1000 # Capture find time in milliseconds
        return self._lastMatch

    def click(self, target, modifiers=""):
        """ Moves the cursor to the target location and clicks the default mouse button. """
        target_location = None
        mouse = Mouse()
        if isinstance(target, Pattern):
            target_location = self.find(target).getTarget()
        elif isinstance(target, basestring):
            target_location = self.find(target).getTarget()
        elif isinstance(target, Match):
            target_location = target.getTarget()
        elif isinstance(target, Region):
            target_location = target.getCenter()
        elif isinstance(target, Location):
            target_location = target
        elif target is None and isinstance(self._lastMatch, Match):
            target_location = self._lastMatch.getTarget()
        else:
            raise TypeError("click expected Pattern, String, Match, Region, or Location object")
        if modifiers != "":
            PlatformManager.pressKey(modifiers)

        mouse.moveSpeed(target_location, self._defaultMouseSpeed)
        time.sleep(0.1) # For responsiveness
        if Settings.ClickDelay > 0:
            time.sleep(min(1.0, Settings.ClickDelay))
            Settings.ClickDelay = 0.0
        mouse.click()
        time.sleep(0.1)

        if modifiers != 0:
            PlatformManager.releaseKey(modifiers)
        Debug.history("Clicked at {}".format(target_location))
    def doubleClick(self, target, modifiers=""):
        """ Moves the cursor to the target location and double-clicks the default mouse button. """
        target_location = None
        mouse = Mouse()
        if isinstance(target, Pattern):
            target_location = self.find(target).getTarget()
        elif isinstance(target, basestring):
            target_location = self.find(target).getTarget()
        elif isinstance(target, Match):
            target_location = target.getTarget()
        elif isinstance(target, Region):
            target_location = target.getCenter()
        elif isinstance(target, Location):
            target_location = target
        else:
            raise TypeError("doubleClick expected Pattern, String, Match, Region, or Location object")
        if modifiers != "":
            PlatformManager.pressKey(modifiers)

        mouse.moveSpeed(target_location, self._defaultMouseSpeed)
        time.sleep(0.1)
        if Settings.ClickDelay > 0:
            time.sleep(min(1.0, Settings.ClickDelay))
            Settings.ClickDelay = 0.0
        mouse.click()
        time.sleep(0.1)
        if Settings.ClickDelay > 0:
            time.sleep(min(1.0, Settings.ClickDelay))
            Settings.ClickDelay = 0.0
        mouse.click()
        time.sleep(0.1)

        if modifiers != 0:
            PlatformManager.releaseKey(modifiers)
    def rightClick(self, target, modifiers=""):
        """ Moves the cursor to the target location and clicks the right mouse button. """
        target_location = None
        mouse = Mouse()
        if isinstance(target, Pattern):
            target_location = self.find(target).getTarget()
        elif isinstance(target, basestring):
            target_location = self.find(target).getTarget()
        elif isinstance(target, Match):
            target_location = target.getTarget()
        elif isinstance(target, Region):
            target_location = target.getCenter()
        elif isinstance(target, Location):
            target_location = target
        else:
            raise TypeError("rightClick expected Pattern, String, Match, Region, or Location object")

        if modifiers != "":
            PlatformManager.pressKey(modifiers)

        mouse.moveSpeed(target_location, self._defaultMouseSpeed)
        time.sleep(0.1)
        if Settings.ClickDelay > 0:
            time.sleep(min(1.0, Settings.ClickDelay))
            Settings.ClickDelay = 0.0
        mouse.click(Mouse.RIGHT)
        time.sleep(0.1)

        if modifiers != "":
            PlatformManager.releaseKey(modifiers)

    def hover(self, target):
        """ Moves the cursor to the target location """
        target_location = None
        mouse = Mouse()
        if isinstance(target, Pattern):
            target_location = self.find(target).getTarget()
        elif isinstance(target, basestring):
            target_location = self.find(target).getTarget()
        elif isinstance(target, Match):
            target_location = target.getTarget()
        elif isinstance(target, Region):
            target_location = target.getCenter()
        elif isinstance(target, Location):
            target_location = target
        else:
            raise TypeError("hover expected Pattern, String, Match, Region, or Location object")

        mouse.moveSpeed(target_location, self._defaultMouseSpeed)
    def drag(self, dragFrom):
        """ Starts a dragDrop operation.

        Moves the cursor to the target location and clicks the mouse in preparation to drag
        a screen element """
        dragFromLocation = None
        mouse = Mouse()
        if isinstance(dragFrom, Pattern):
            dragFromLocation = self.find(dragFrom).getTarget()
        elif isinstance(dragFrom, basestring):
            dragFromLocation = self.find(dragFrom).getTarget()
        elif isinstance(dragFrom, Match):
            dragFromLocation = dragFrom.getTarget()
        elif isinstance(dragFrom, Region):
            dragFromLocation = dragFrom.getCenter()
        elif isinstance(dragFrom, Location):
            dragFromLocation = dragFrom
        else:
            raise TypeError("drag expected dragFrom to be Pattern, String, Match, Region, or Location object")
        mouse.moveSpeed(dragFromLocation, self._defaultMouseSpeed)
        time.sleep(Settings.DelayBeforeMouseDown)
        mouse.buttonDown()
        Debug.history("Began drag at {}".format(dragFromLocation))
    def dropAt(self, dragTo, delay=None):
        """ Completes a dragDrop operation
        
        Moves the cursor to the target location, waits ``delay`` seconds, and releases the mouse
        button """
        mouse = Mouse()
        if isinstance(dragTo, Pattern):
            dragToLocation = self.find(dragTo).getTarget()
        elif isinstance(dragTo, basestring):
            dragToLocation = self.find(dragTo).getTarget()
        elif isinstance(dragTo, Match):
            dragToLocation = dragTo.getTarget()
        elif isinstance(dragTo, Region):
            dragToLocation = dragTo.getCenter()
        elif isinstance(dragTo, Location):
            dragToLocation = dragTo
        else:
            raise TypeError("dragDrop expected dragTo to be Pattern, String, Match, Region, or Location object")

        mouse.moveSpeed(dragToLocation, self._defaultMouseSpeed)
        time.sleep(delay if delay is not None else Settings.DelayBeforeDrop)
        mouse.buttonUp()
        Debug.history("Ended drag at {}".format(dragToLocation))
    def dragDrop(self, dragFrom, dragTo, modifiers=""):
        """ Performs a dragDrop operation.

        Holds down the mouse button on ``dragFrom``, moves the mouse to ``dragTo``, and releases
        the mouse button.

        ``modifiers`` may be a typeKeys() compatible string. The specified keys will be held
        during the drag-drop operation.
        """
        if modifiers != "":
            PlatformManager.pressKey(modifiers)

        self.drag(dragFrom)
        time.sleep(Settings.DelayBeforeDrag)
        self.dropAt(dragTo)

        if modifiers != "":
            PlatformManager.releaseKey(modifiers)

    def type(self, *args):
        """ Usage: type([PSMRL], text, [modifiers])

        If a pattern is specified, the pattern is clicked first. Doesn't support text paths.

        This implementation varies slightly from Sikuli by allowing a SendKeys variant format.
        The following special characters are available as modifiers:

        * ``^`` - Ctrl
        * ``+`` - Shift
        * ``%`` - Alt
        * ``@`` - Win/Meta/Cmd
        * ``~`` - Enter/Return

        They can be used to modify a single following character. ``^c`` will type Ctrl+C.
        If you need to modify multiple characters, use parentheses: ``+(abc)`` will hold down
        Shift and type "ABC".

        To enter these characters as literals, enclose them in brackets: ``{@}``
        """
        pattern = None
        text = None
        modifiers = None
        if len(args) == 1 and isinstance(args[0], basestring):
            # Is a string (or Key) to type
            text = args[0]
        elif len(args) == 2:
            if not isinstance(args[0], basestring) and isinstance(args[1], basestring):
                pattern = args[0]
                text = args[1]
            else:
                text = args[0]
                modifiers = args[1]
        elif len(args) == 3 and not isinstance(args[0], basestring):
            pattern = args[0]
            text = args[1]
            modifiers = args[2]
        else:
            raise TypeError("type method expected ([PSMRL], text, [modifiers])")

        if pattern:
            self.click(pattern)

        Debug.history("Typing '{}' with modifiers '{}'".format(text, modifiers))
        kb = Keyboard()
        if modifiers:
            kb.keyDown(modifiers)
        if Settings.TypeDelay > 0:
            typeSpeed = min(1.0, Settings.TypeDelay)
            Settings.TypeDelay = 0.0
        else:
            typeSpeed = self._defaultTypeSpeed
        kb.type(text, typeSpeed)
        if modifiers:
            kb.keyUp(modifiers)
        time.sleep(0.2)
    def paste(self, *args):
        """ Usage: paste([PSMRL], text)

        If a pattern is specified, the pattern is clicked first. Doesn't support text paths.
        ``text`` is pasted as is using the OS paste shortcut (Ctrl+V for Windows/Linux, Cmd+V
        for OS X). Note that `paste()` does NOT use special formatting like `type()`.
        """
        target = None
        text = ""
        if len(args) == 1 and isinstance(args[0], basestring):
            text = args[0]
        elif len(args) == 2 and isinstance(args[1], basestring):
            self.click(target)
            text = args[1]
        else:
            raise TypeError("paste method expected [PSMRL], text")

        PlatformManager.setClipboard(text)
        # Triggers OS paste for foreground window
        PlatformManager.osPaste()
        time.sleep(0.2)
    def getClipboard(self):
        """ Returns the contents of the clipboard

        Can be used to pull outside text into the application. """
        return PlatformManager.getClipboard()
    def text(self):
        """ OCR method. Todo. """
        raise NotImplementedError("OCR not yet supported")

    def mouseDown(self, button):
        """ Low-level mouse actions. """
        return PlatformManager.mouseButtonDown(button)
    def mouseUp(self, button):
        """ Low-level mouse actions """
        return PlatformManager.mouseButtonUp(button)
    def mouseMove(self, PSRML, dy=0):
        """ Low-level mouse actions """
        if isinstance(PSRML, int):
            # Assume called as mouseMove(dx, dy)
            offset = Location(PSRML, dy)
            PSRML = Mouse().getPos().offset(offset)
        Mouse().moveSpeed(PSRML)
    def wheel(self, PSRML, direction, steps):
        """ Clicks the wheel the specified number of ticks """
        self.mouseMove(PSRML)
        Mouse().wheel(direction, steps)
    def keyDown(self, keys):
        """ Concatenate multiple keys to press them all down. """
        return Keyboard().keyDown(keys)
    def keyUp(self, keys):
        """ Concatenate multiple keys to up them all. """
        return Keyboard().keyUp(keys)

    def isRegionValid(self):
        """ Returns false if the whole region is outside any screen, otherwise true """
        screens = PlatformManager.getScreenDetails()
        for screen in screens:
            s_x, s_y, s_w, s_h = screen["rect"]
            if (self.x+self.w < s_x or s_x+s_w < self.x or self.y+self.h < s_y or s_y+s_h < self.y):
                # Rects overlap
                return False
            return True

    def clipRegionToScreen(self):
        """ Returns the part of the region that is visible on a screen

        If the region is visible on multiple screens, returns the screen with the smallest ID.
        Returns None if the region is outside the screen.
        """
        if not self.isRegionValid():
            return None
        screens = PlatformManager.getScreenDetails()
        containing_screen = None
        for screen in screens:
            s_x, s_y, s_w, s_h = screen["rect"]
            if self.x >= s_x and self.x+self.w <= s_x+s_w and self.y >= s_y and self.y+self.h <= s_y+s_h:
                # Region completely inside screen
                return self
            elif self.x+self.w < s_x or s_x+s_w < self.x or self.y+self.h < s_y or s_y+s_h < self.y:
                # Region completely outside screen
                continue
            else:
                # Region partially inside screen
                x = max(self.x, s_x)
                y = max(self.y, s_y)
                w = min(self.w, s_w)
                h = min(self.h, s_h)
                return Region(x, y, w, h)
        return None


    # Partitioning constants
    NORTH 			= 202 # Upper half
    NORTH_WEST 		= 300 # Left third in upper third
    NORTH_MID 		= 301 # Middle third in upper third
    NORTH_EAST 		= 302 # Right third in upper third
    SOUTH 			= 212 # Lower half
    SOUTH_WEST 		= 320 # Left third in lower third
    SOUTH_MID 		= 321 # Middle third in lower third
    SOUTH_EAST 		= 322 # Right third in lower third
    EAST 			= 220 # Right half
    EAST_MID 		= 310 # Middle third in right third
    WEST 			= 221 # Left half
    WEST_MID 		= 312 # Middle third in left third
    MID_THIRD 		= 311 # Middle third in middle third
    TT 				= 200 # Top left quarter
    RR 				= 201 # Top right quarter
    BB 				= 211 # Bottom right quarter
    LL 				= 210 # Bottom left quarter

    MID_VERTICAL 	= "MID_VERT" # Half of width vertically centered
    MID_HORIZONTAL	= "MID_HORZ" # Half of height horizontally centered
    MID_BIG			= "MID_HALF" # Half of width/half of height centered

    def setRaster(self, rows, columns):
        """ Sets the raster for the region, allowing sections to be indexed by row/column """
        rows = int(rows)
        columns = int(columns)
        if rows <= 0 or columns <= 0:
            return self
        self._raster = (rows, columns)
        return self.getCell(0, 0)
    def getRow(self, row, numberRows=None):
        """ Returns the specified row of the region (if the raster is set)

        If numberRows is provided, uses that instead of the raster
        """
        row = int(row)
        if self._raster[0] == 0 or self._raster[1] == 0:
            return self
        if numberRows is None or numberRows < 1 or numberRows > 9:
            numberRows = self._raster[0]
        rowHeight = self.h / numberRows
        if row < 0:
            # If row is negative, count backwards from the end
            row = numberRows - row
            if row < 0:
                # Bad row index, return last row
                return Region(self.x, self.y+self.h-rowHeight, self.w, rowHeight)
        elif row > numberRows:
            # Bad row index, return first row
            return Region(self.x, self.y, self.w, rowHeight)
        return Region(self.x, self.y + (row * rowHeight), self.w, rowHeight)
    def getCol(self, column, numberColumns=None):
        """ Returns the specified column of the region (if the raster is set)

        If numberColumns is provided, uses that instead of the raster
        """
        column = int(column)
        if self._raster[0] == 0 or self._raster[1] == 0:
            return self
        if numberColumns is None or numberColumns < 1 or numberColumns > 9:
            numberColumns = self._raster[1]
        columnWidth = self.w / numberColumns
        if column < 0:
            # If column is negative, count backwards from the end
            column = numberColumns - column
            if column < 0:
                # Bad column index, return last column
                return Region(self.x+self.w-columnWidth, self.y, columnWidth, self.h)
        elif column > numberColumns:
            # Bad column index, return first column
            return Region(self.x, self.y, columnWidth, self.h)
        return Region(self.x + (column * columnWidth), self.y, columnWidth, self.h)
    def getCell(self, row, column):
        """ Returns the specified cell (if a raster is set for the region) """
        row = int(row)
        column = int(column)
        if self._raster[0] == 0 or self._raster[1] == 0:
            return self
        rowHeight = self.h / self._raster[0]
        columnWidth = self.h / self._raster[1]
        if column < 0:
            # If column is negative, count backwards from the end
            column = self._raster[1] - column
            if column < 0:
                # Bad column index, return last column
                column = self._raster[1]
        elif column > self._raster[1]:
            # Bad column index, return first column
            column = 0
        if row < 0:
            # If row is negative, count backwards from the end
            row = self._raster[0] - row
            if row < 0:
                # Bad row index, return last row
                row = self._raster[0]
        elif row > self._raster[0]:
            # Bad row index, return first row
            row = 0
        return Region(self.x+(column*columnWidth), self.y+(row*rowHeight), columnWidth, rowHeight)
    def get(self, part):
        """ Returns a section of the region as a new region

        Accepts partitioning constants, e.g. Region.NORTH, Region.NORTH_WEST, etc.
        Also accepts an int 200-999:
        * First digit:  Raster (*n* rows by *n* columns)
        * Second digit: Row index (if equal to raster, gets the whole row)
        * Third digit:  Column index (if equal to raster, gets the whole column)

        Region.get(522) will use a raster of 5 rows and 5 columns and return
        the cell in the middle.

        Region.get(525) will use a raster of 5 rows and 5 columns and return the row in the middle.
        """
        if part == self.MID_VERTICAL:
            return Region(self.x+(self.w/4), y, self.w/2, self.h)
        elif part == self.MID_HORIZONTAL:
            return Region(self.x, self.y+(self.h/4), self.w, self.h/2)
        elif part == self.MID_BIG:
            return Region(self.x+(self.w/4), self.y+(self.h/4), self.w/2, self.h/2)
        elif isinstance(part, int) and part >= 200 and part <= 999:
            raster, row, column = str(part)
            self.setRaster(raster, raster)
            if row == raster and column == raster:
                return self
            elif row == raster:
                return self.getCol(column)
            elif column == raster:
                return self.getRow(row)
            else:
                return self.getCell(row,column)
        else:
            return self
    def setRows(self, rows):
        """ Sets the number of rows in the raster (if columns have not been initialized, set to 1 as well) """
        self._raster[0] = rows
        if self._raster[1] == 0:
            self._raster[1] = 1
    def setCols(self, columns):
        """ Sets the number of columns in the raster (if rows have not been initialized, set to 1 as well) """
        self._raster[1] = columns
        if self._raster[0] == 0:
            self._raster[0] = 1
    def isRasterValid(self):
        return self.getCols() > 0 and self.getRows() > 0
    def getRows(self):
        return self._raster[0]
    def getCols(self):
        return self._raster[1]
    def getRowH(self):
        if self._raster[0] == 0:
            return 0
        return self.h / self._raster[0]
    def getColW(self):
        if self._raster[1] == 0:
            return 0
        return self.w / self._raster[1]

class Match(Region):
    """ Extended Region object with additional data on click target, match score """
    def __init__(self, score, target, rect):
        super(Match, self).__init__(rect[0][0], rect[0][1], rect[1][0], rect[1][1])
        self._score = float(score)
        if not target or not isinstance(target, Location):
            raise TypeError("Match expected target to be a Location object")
        self._target = target

    def getScore(self):
        """ Returns confidence score of the match """
        return self._score

    def getTarget(self):
        """ Returns the location of the match click target (center by default, but may be offset) """
        return self.getCenter().offset(self._target.x, self._target.y)

    def __repr__(self):
        return "Match[{},{} {}x{}] score={:2f}, target={}".format(self.x, self.y, self.w, self.h, self._score, self._target.getTuple())

class Screen(Region):
    """ Individual screen objects can be created for each monitor in a multi-monitor system. 

    Screens are indexed according to the system order. 0 is the primary monitor (display 1), 1 is the next monitor, etc.

    Lackey also makes it possible to search all screens as a single "virtual screen," arranged
    according to the system's settings. Screen(-1) returns this virtual screen. Note that the
    larger your search region is, the slower your search will be, so it's best practice to adjust
    your region to the particular area of the screen where you know your target will be.

    Note that Sikuli is inconsistent in identifying screens. In Windows, Sikuli identifies the
    first hardware monitor as Screen(0) rather than the actual primary monitor. However, on OS X
    it follows the latter convention. We've opted to make Screen(0) the actual primary monitor
    (wherever the Start Menu/System Menu Bar is) across the board.
    """
    def __init__(self, screenId=None):
        """ Defaults to the main screen. """
        if not isinstance(screenId, int) or screenId < -1 or screenId >= len(PlatformManager.getScreenDetails()):
            screenId = 0
        self._screenId = screenId
        x, y, w, h = self.getBounds()
        super(Screen, self).__init__(x, y, w, h)
    def getNumberScreens(self):
        """ Get the number of screens in a multi-monitor environment at the time the script is running """
        return len(PlatformManager.getScreenDetails())
    def getBounds(self):
        """ Returns bounds of screen as (x, y, w, h) """
        return PlatformManager.getScreenBounds(self._screenId)
    def capture(self, *args): #x=None, y=None, w=None, h=None):
        """ Captures the region as an image and saves to a temporary file (specified by TMPDIR, TEMP, or TMP environmental variable) """
        if len(args) == 0:
            # Capture screen region
            region = self
        elif isinstance(args[0], Region):
            # Capture specified region
            region = args[0]
        elif isinstance(args[0], tuple):
            # Capture region defined by specified tuple
            region = Region(*args[0])
        elif isinstance(args[0], basestring):
            # Interactive mode
            raise NotImplementedError("Interactive capture mode not defined")
        elif isinstance(args[0], int):
            # Capture region defined by provided x,y,w,h
            region = Region(*args)
        bitmap = region.getBitmap()
        tfile, tpath = tempfile.mkstemp(".png")
        cv2.imwrite(tpath, bitmap)
        return tpath
    def selectRegion(self, text=""):
        """ Not yet implemented """
        raise NotImplementedError()

class Location(object):
    """ Basic 2D point object """
    def __init__(self, x, y):
        self.setLocation(x, y)

    def getX(self):
        """ Returns the X-component of the location """
        return self.x
    def getY(self):
        """ Returns the Y-component of the location """
        return self.y

    def setLocation(self, x, y):
        """Set the location of this object to the specified coordinates."""
        self.x = int(x)
        self.y = int(y)

    def offset(self, dx, dy):
        """Get a new location which is dx and dy pixels away horizontally and vertically from the current location."""
        return Location(self.x+dx, self.y+dy)

    def above(self, dy):
        """Get a new location dy pixels vertically above the current location."""
        return Location(self.x, self.y-dy)
    def below(self, dy):
        """Get a new location dy pixels vertically below the current location."""
        return Location(self.x, self.y+dy)
    def left(self, dx):
        """Get a new location dx pixels horizontally to the left of the current location."""
        return Location(self.x-dx, self.y)
    def right(self, dx):
        """Get a new location dx pixels horizontally to the right of the current location."""
        return Location(self.x+dx, self.y)

    def getTuple(self):
        """ Returns coordinates as a tuple (for some PlatformManager methods) """
        return (self.x, self.y)

    def __repr__(self):
        return "(Location object at ({},{}))".format(self.x, self.y)

class Mouse(object):
    """ Mid-level mouse routines. Interfaces with ``PlatformManager`` """
    def __init__(self):
        self._defaultScanRate = 0.01

    # Class constants
    WHEEL_DOWN = 0
    WHEEL_UP = 1
    LEFT = 0
    MIDDLE = 1
    RIGHT = 2

    def move(self, location):
        """ Moves cursor to specified ``Location`` """

        # Check if move point is outside a monitor rectangle
        if not PlatformManager.isPointVisible(location.x, location.y):
            # move point is outside a monitor rectangle. Snap to closest edge of primary monitor.
            s_x, s_y, s_w, s_h = Screen(0).getBounds()
            location.x = min(max(location.x, s_x), s_x+s_w)
            location.y = min(max(location.y, s_y), s_y+s_h)

        PlatformManager.setMousePos(location.getTuple())

    def getPos(self):
        """ Gets ``Location`` of cursor """
        x, y = PlatformManager.getMousePos()
        return Location(x, y)

    def moveSpeed(self, location, seconds=0.3):
        """ Moves cursor to specified ``Location`` over ``seconds``.

        If ``seconds`` is 0, moves the cursor immediately. Used for smooth
        somewhat-human-like motion.
        """
        if seconds == 0:
            # If the mouse isn't on the main screen, snap to point automatically instead of
            # trying to track a path back
            self.move(location)
            return

        # Check if move point is outside a monitor rectangle
        if not PlatformManager.isPointVisible(location.x, location.y):
            # move point is outside a monitor rectangle. Snap to closest edge of primary monitor.
            s_x, s_y, s_w, s_h = Screen(0).getBounds()
            location.x = min(max(location.x, s_x), s_x+s_w)
            location.y = min(max(location.y, s_y), s_y+s_h)

        frames = int(seconds / self._defaultScanRate)
        while frames > 0:
            mouse_pos = self.getPos()
            deltax = int(round(float(location.x - mouse_pos.x) / frames))
            deltay = int(round(float(location.y - mouse_pos.y) / frames))
            self.move(Location(mouse_pos.x + deltax, mouse_pos.y + deltay))
            frames -= 1
            time.sleep(self._defaultScanRate)

    def click(self, button=0):
        """ Clicks the specified mouse button.

        Use Mouse.LEFT, Mouse.MIDDLE, Mouse.RIGHT
        """
        PlatformManager.clickMouse(button)
    def buttonDown(self, button=0):
        """ Holds down the specified mouse button.

        Use Mouse.LEFT, Mouse.MIDDLE, Mouse.RIGHT
        """
        PlatformManager.mouseButtonDown(button)
    def buttonUp(self, button=0):
        """ Releases the specified mouse button.

        Use Mouse.LEFT, Mouse.MIDDLE, Mouse.RIGHT
        """
        PlatformManager.mouseButtonUp(button)
    def wheel(self, direction, steps):
        """ Clicks the wheel the specified number of steps in the given direction.

        Use Mouse.WHEEL_DOWN, Mouse.WHEEL_UP
        """
        return PlatformManager.mouseWheel(direction, steps)

class Keyboard(object):
    """ Mid-level keyboard routines. Interfaces with ``PlatformManager`` """
    def __init__(self):
        pass

    def keyDown(self, keys):
        """ Holds down the specified keys """
        return PlatformManager.pressKey(keys)
    def keyUp(self, keys):
        """ Releases the specified keys """
        return PlatformManager.releaseKey(keys)
    def type(self, text, delay=0.1):
        """ Types ``text`` with ``delay`` seconds between keypresses """
        return PlatformManager.typeKeys(text, delay)

class App(object):
    """ Allows apps to be selected by title, PID, or by starting an
    application directly. Can address individual windows tied to an
    app.

    For more information, see [Sikuli's App documentation](http://sikulix-2014.readthedocs.io/en/latest/appclass.html#App)
    """
    def __init__(self, identifier=None):
        self._pid = None
        self._search = identifier
        self._title = ""
        self._exec = ""
        self._params = ""
        self._process = None
        self._defaultScanRate = 0.1
        self.proc = None
        
        # Replace class methods with instance methods
        self.focus = self._focus_instance
        self.close = self._close_instance
        self.open = self._open_instance

        # Process `identifier`
        if isinstance(identifier, int):
            # `identifier` is a PID
            Debug.log(3, "Creating App by PID ({})".format(identifier))
            self._pid = identifier
        elif isinstance(identifier, basestring):
            # `identifier` is either part of a window title
            # or a command line to execute. If it starts with a "+",
            # launch it immediately. Otherwise, store it until open() is called.
            Debug.log(3, "Creating App by string ({})".format(identifier))
            launchNow = False
            if identifier.startswith("+"):
                # Should launch immediately - strip the `+` sign and continue
                launchNow = True
                identifier = identifier[1:]
            # Check if `identifier` is an executable commmand
            # Possible formats:
            # Case 1: notepad.exe C:\sample.txt
            # Case 2: "C:\Program Files\someprogram.exe" -flag

            # Extract hypothetical executable name
            if identifier.startswith('"'):
                executable = identifier[1:].split('"')[0]
                params = identifier[len(executable)+2:].split(" ") if len(identifier) > len(executable) + 2 else []
            else:
                executable = identifier.split(" ")[0]
                params = identifier[len(executable)+1:].split(" ") if len(identifier) > len(executable) + 1 else []

            # Check if hypothetical executable exists
            if self._which(executable) is not None:
                # Found the referenced executable
                self._exec = executable
                self._params = params
                # If the command was keyed to execute immediately, do so.
                if launchNow:
                    self.open()
            else:
                # No executable found - treat as a title instead. Try to capture window.
                self._title = identifier
                self.open
        else:
            self._pid = -1 # Unrecognized identifier, setting to empty app

        self._pid = self.getPID() # Confirm PID is an active process (sets to -1 otherwise)

    def _which(self, program):
        """ Private method to check if an executable exists

        Shamelessly stolen from http://stackoverflow.com/questions/377017/test-if-executable-exists-in-python
        """
        def is_exe(fpath):
            return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

        fpath, fname = os.path.split(program)
        if fpath:
            if is_exe(program):
                return program
        else:
            for path in os.environ["PATH"].split(os.pathsep):
                path = path.strip('"')
                exe_file = os.path.join(path, program)
                if is_exe(exe_file):
                    return exe_file
        return None

    @classmethod
    def pause(cls, waitTime):
        time.sleep(waitTime)

    @classmethod
    def focus(cls, appName):
        """ Searches for exact text, case insensitive, anywhere in the window title. 

        Brings the matching window to the foreground.

        As a class method, accessible as `App.focus(appName)`. As an instance method,
        accessible as `App(appName).focus()`.
        """
        app = cls(appName)
        return app.focus()
    def _focus_instance(self):
        """ In instances, the ``focus()`` classmethod is replaced with this instance method. """
        if self._title:
            Debug.log(3, "Focusing app with title like ({})".format(self._title))
            PlatformManager.focusWindow(PlatformManager.getWindowByTitle(re.escape(self._title)))
            if self.getPID() == -1:
                self.open()
        elif self._pid and self._pid != -1:
            Debug.log(3, "Focusing app with pid ({})".format(self._pid))
            PlatformManager.focusWindow(PlatformManager.getWindowByPID(self._pid))
        return self

    @classmethod
    def close(cls, appName):
        """ Closes the process associated with the specified app.

        As a class method, accessible as `App.class(appName)`.
        As an instance method, accessible as `App(appName).close()`.
        """
        return cls(appName).close()
    def _close_instance(self):
        if self._process:
            self._process.terminate()
        elif self.getPID() != -1:
            PlatformManager.killProcess(self.getPID())

    @classmethod
    def open(self, executable):
        """ Runs the specified command and returns an App linked to the generated PID.

        As a class method, accessible as `App.open(executable_path)`.
        As an instance method, accessible as `App(executable_path).open()`.
        """
        return App(executable).open()
    def _open_instance(self, waitTime=0):
        if self._exec != "":
            # Open from an executable + parameters
            self._process = subprocess.Popen([self._exec] + self._params, shell=False)
            self._pid = self._process.pid
        elif self._title != "":
            # Capture an existing window that matches self._title
            self._pid = PlatformManager.getWindowPID(
                PlatformManager.getWindowByTitle(
                    re.escape(self._title)))
        time.sleep(waitTime)
        return self

    @classmethod
    def focusedWindow(cls):
        """ Returns a Region corresponding to whatever window is in the foreground """
        x, y, w, h = PlatformManager.getWindowRect(PlatformManager.getForegroundWindow())
        return Region(x,y,w,h)

    def getWindow(self):
        """ Returns the title of the main window of the currently open app.

        Returns an empty string if no match could be found.
        """
        if self.getPID() != -1:
            return PlatformManager.getWindowTitle(PlatformManager.getWindowByPID(self.getPID()))
        else:
            return ""
    def getName(self):
        """ Returns the short name of the app as shown in the process list """
        return PlatformManager.getProcessName(self.getPID())
    def getPID(self):
        """ Returns the PID for the associated app (or -1, if no app is associated or the app is not running) """
        if self._pid is not None:
            if not PlatformManager.isPIDValid(self._pid):
                self._pid = -1
            return self._pid
        return -1

    def hasWindow(self):
        """ Returns True if the process has a window associated, False otherwise """
        return PlatformManager.getWindowByPID(self.getPID()) is not None

    def window(self, windowNum=0):
        """ Returns the region corresponding to the specified window of the app.

        Defaults to the first window found for the corresponding PID.
        """
        if self._pid == -1:
            raise FindFailed("Window not found for app \"{}\"".format(self))
        x,y,w,h = PlatformManager.getWindowRect(PlatformManager.getWindowByPID(self._pid, windowNum))
        return Region(x,y,w,h).clipRegionToScreen()

    def setUsing(self, params):
        self._params = params.split(" ")

    def __repr__(self):
        """ Returns a string representation of the app """
        return "[{pid}:{executable} ({windowtitle})] {searchtext}".format(pid=self._pid, executable=self.getName(), windowtitle=self.getWindow(), searchtext=self._search)

    def isRunning(self, waitTime=0):
        """ If PID isn't set yet, checks if there is a window with the specified title. """
        waitUntil = time.time() + waitTime
        while True:
            if self.getPID() > 0:
                return True
            else:
                self._pid = PlatformManager.getWindowPID(PlatformManager.getWindowByTitle(re.escape(self._title)))

            # Check if we've waited long enough
            if time.time() > waitUntil:
                break
            else:
                time.sleep(self._defaultScanRate)
        return self.getPID() > 0

