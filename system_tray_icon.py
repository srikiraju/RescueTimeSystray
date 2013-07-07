import objc, re, os
from Foundation import *
from AppKit import *
from PyObjCTools import NibClassBuilder, AppHelper
import gc
import pprint
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_agg import FigureCanvasAgg

# code stolen from The Tao of Mac
# modified May 21, 2012 by Ian Simon

start_time = NSDate.date()

class Timer(NSObject):
  def set_timer_method(self, timer_method):
    self.timer_method = timer_method

  def set_image(self, prod):
    fig = plt.figure(figsize=[40,18], dpi=1, frameon=False)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    #plt.axis('off')
    colors = []
    prodN = []

    for a in prod:
        prodN.append(1 if abs(a-50) ==0 else abs(a-50))
        if a >= 50:
            colors.append('#5C832F')
        else:
            colors.append('#4C1B1B')
    print prodN
    print colors
    plt.bar([1,2,3,4,5], prodN[1:6], 1, color=colors[1:6])
    plt.yticks(range(50))

    plt.savefig('foo.png', dpi=1, transparent=True,  pad_inches=0, bbox_inches=0)
    #img = NSImage.alloc().initByReferencingFile_(filename)
    img = NSImage.alloc().initByReferencingFile_('foo.png')
    self.statusitem.setTitle_(str(int(prod[5]-50)))
    self.statusitem.setImage_(img)
    fig.clf()





  def applicationDidFinishLaunching_(self, notification):
    statusbar = NSStatusBar.systemStatusBar()
    # Create the statusbar item
    self.statusitem = statusbar.statusItemWithLength_(NSVariableStatusItemLength)
    # Let it highlight upon clicking
    self.statusitem.setHighlightMode_(1)
    # Set a tooltip
    self.statusitem.setToolTip_('RescueTime Productivity')
    self.statusitem.setEnabled_(TRUE)

    # Build a very simple menu
    self.menu = NSMenu.alloc().init()
    # Default event
    menuitem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_('Quit', 'terminate:', '')
    self.menu.addItem_(menuitem)
    # Bind it to the status item
    self.statusitem.setMenu_(self.menu)

    # Get the timer going
    self.timer = NSTimer.alloc().initWithFireDate_interval_target_selector_userInfo_repeats_(start_time, 240.0, self, 'tick:', None, True)
    NSRunLoop.currentRunLoop().addTimer_forMode_(self.timer, NSDefaultRunLoopMode)
    self.timer.fire()

  def tick_(self, notification):
    self.timer_method()

if __name__ == "__main__":
  app = NSApplication.sharedApplication()
  delegate = Timer.alloc().init()
  app.setDelegate_(delegate)
  AppHelper.runEventLoop()
