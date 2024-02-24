import xbmc
import datetime
from . import utils

class ImmersionService:
    last_check = -1
    manager = None

    def __init__(self):
        pass

    def runProgram(self):
        monitor = xbmc.Monitor()
        startup = True

        # run until abort requested
        while(True):

            if startup:
                utils.showNotification('Immersive lights starting up')
                pass

            startup = False

            # calculate the sleep time (next minute)
            currentSec = datetime.datetime.now()
            if(monitor.waitForAbort(60 - currentSec.second)):
                break