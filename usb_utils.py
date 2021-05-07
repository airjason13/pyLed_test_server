import usb.core
import usb.util
import jlog
log = jlog.logging_init("usb_utils")
pico_vid = 0x0000
pico_pid = 0x0001
"""
function : find_pico
parameter : void
return : pico devices
"""
def find_pico():
    # find our device
    devs = list(usb.core.find( find_all=True, idVendor=pico_vid, idProduct=pico_pid))

    #log.debug("find_pico")
    # was it found?
    if devs is None:
        #raise ValueError('Device not found')
        log.debug("no picos")

    #for dev in devs:
    #    print("dev :", dev.get_active_configuration())
    return devs

def get_ep(dev):
    cfg = dev.get_active_configuration()
    intf = cfg[(0, 0)]

    outep = usb.util.find_descriptor(
        intf,
        # match the first OUT endpoint
        custom_match= \
            lambda e: \
                usb.util.endpoint_direction(e.bEndpointAddress) == \
                usb.util.ENDPOINT_OUT)

    inep = usb.util.find_descriptor(
        intf,
        # match the first IN endpoint
        custom_match= \
            lambda e: \
                usb.util.endpoint_direction(e.bEndpointAddress) == \
                usb.util.ENDPOINT_IN)
    return outep, inep