""" A location-aware script to manage ringer volume """

__author__ = 'Marco Bonifacio <bonifacio.marco@gmail.com>'
__license__ = 'MIT License'

import android
import time

# Parameters
SSID = {'bonix-lan': 'casa',
        'ZENIT SECURED WPA': 'lavoro'}
RINGER = {'casa': 5,
          'lavoro': 2,
          'sconosciuto': 5}

# Functions
def check_ssid(droid):
    """ Check if wireless network SSID is known.
    Args:
        droid: an Android instance.
    Returns:
        a string representing a known or unknown environment. """
    state = 'sconosciuto'
    try:
        lwifi = droid.wifiGetScanResults().result
        lssid = [w['ssid']for w in lwifi]
        for s in lssid:
            if s in SSID:
                state = SSID[s]
    except Exception, e:
        droid.notify('PyLocale', 'Errore: {}'.format(e))
    finally:
        return(state)

def check_state(droid, state, stateold):
    """ Check if environment has changed.
    Args:
        droid: an Android instance.
        state: a string, the present state.
        stateold: a string, the former state.
    Returns:
        a binary true if environment has changed. """
    if state != stateold:
        droid.vibrate()
        if state != 'sconosciuto':
            droid.makeToast('Sei a {}'.format(state))
        else:
            droid.makeToast('Sei uscito da {}'.format(stateold))
        return(True)
    else:
        return(False)

def set_ringer(droid, state):
    """ Set the ringer volume depending on state.
    Args:
        droid: an Android instance.
        state: a string, the present state.
    Returns:
        nothing. """
    droid.setRingerVolume(RINGER[state])
    droid.makeToast('Volume: {}'.format(RINGER[state]))

if __name__ == '__main__':
    droid = android.Android()
    state = 'sconosciuto'
    while True:
        stateold = state
        state = check_ssid(droid)
        changed = check_state(droid, state, stateold)
        if changed is True:
            set_ringer(droid, state)
        time.sleep(300)