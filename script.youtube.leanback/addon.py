# Kodi modules
import xbmc
import xbmcaddon
import xbmcgui

# Python modules
import platform
import os.path
import subprocess
import json

# Getting constants
__addon__ = xbmcaddon.Addon('script.youtube.leanback')
__addonId__ = __addon__.getAddonInfo('id')
__addonName__ = __addon__.getAddonInfo('name')
__version__ = __addon__.getAddonInfo('version')
__localizedMessages__ = __addon__.getLocalizedString


# Method to print logs on a standard way
def log(message, level=xbmc.LOGNOTICE):
    xbmc.log('[%s:v%s] %s' % (__addonId__, __version__, message.encode('utf-8')), level)
# end of log

# Starting the Addon
log("Starting " + __addonName__)

# Var to hold  the path where the EmulationStation executable is
executable = ""

# We are going to ask on which platform this is running so we can load the default executable location for it
if platform.system() == "Windows":
    # If the platform is Windows
    executable = __addon__.getSetting('windowsExecutable').decode('utf-8')
    log("Loaded Windows executable location from Settings: " + executable)

else:
    # Otherwise it is Linux
    executable = __addon__.getSetting('linuxExecutable').decode('utf-8')
    log("Loaded Linux executable location from Settings: " + executable)


# When you choose an executable from Kodi when changing Addon Settings, Kodi forces you to select an executable that exists, but we want to validate
# if the executable exists anyways, just in case the default value doesn't work or the settings were manually changed
if not os.path.isfile(executable):
    # This message prints something like: Chrome executable was not found, go to Addon-Configure and change it
    xbmcgui.Dialog().ok(__localizedMessages__(32000), __localizedMessages__(32001) ,__localizedMessages__(32002), __localizedMessages__(32003) + executable)
    # This message prints something like: Please check that Chrome is installed
    xbmcgui.Dialog().ok(__localizedMessages__(32004), __localizedMessages__(32005))
    # Log the error
    log("Chrome executable was not found on this specified location: " + executable, xbmc.LOGERROR)

else:
    # Var to hold current display sleep timer
    displayoff = ""

    # Var to hold current computer sleep timer
    shutdowntime = ""

    log("Starting Chrome executable: " + executable)
    if __addon__.getSetting('powersaving') == "true":
        log("Turning off powersavings")
        displayoff = str(json.loads(xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Settings.GetSettingValue", "params":{"setting":"powermanagement.displaysoff"},"id":1}'))["result"]["value"])
        log("Current display off time: " + displayoff)
        shutdowntime = str(json.loads(xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Settings.GetSettingValue", "params":{"setting":"powermanagement.shutdowntime"},"id":1}'))["result"]["value"])
        log("Current shutdown time: " + shutdowntime)
        xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Settings.SetSettingValue", "params":{"setting":"powermanagement.displaysoff","value":0},"id":1}')
        xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Settings.SetSettingValue", "params":{"setting":"powermanagement.shutdowntime","value":0},"id":1}')
    subprocess.call([executable,"--kiosk","https://www.youtube.com/tv"])
    if __addon__.getSetting('powersaving') == "true":
        log("Returning powersaving settings to inital value")
        xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Settings.SetSettingValue", "params":{"setting":"powermanagement.displaysoff","value":'+displayoff+'},"id":1}')
        xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Settings.SetSettingValue", "params":{"setting":"powermanagement.shutdowntime","value":'+shutdowntime+'},"id":1}')
   