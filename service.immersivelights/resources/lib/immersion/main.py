import xbmc
import xbmcaddon
from resources.lib.immersion.gui import GuiHandler
from resources.lib.immersion.logger import Logger
from resources.lib.immersion.monitor import Monitor
from resources.lib.immersion.settings import SettingsManager

class ImmersionService:
    last_check = -1
    manager = None

    def __init__(self):
        pass

    def runProgram(self):
        addon = xbmcaddon.Addon()
        logger = Logger(addon.getAddonInfo("name"))
        settings_manager = SettingsManager(addon.getSettings(), logger)
        player = xbmc.Player()
        output_handler = GuiHandler(addon, settings_manager)
        monitor = Monitor(settings_manager, player, output_handler, logger)
        monitor.main_loop()

        while not monitor.abortRequested():
            if monitor.waitForAbort(10):
                break