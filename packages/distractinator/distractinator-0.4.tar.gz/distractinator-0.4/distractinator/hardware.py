import sys
import serial.tools.list_ports
from six.moves import input

explanation = """\nLet's make sure we can correctly identify your Distractinator(TM) hardware!

    1.) Plug in the Distractinator(TM), please.
    2.) Temporarily unplug any unnecessary USB peripherals (optional).
    3.) Read the list of devices. Assuming you don't have any other microcontrollers or devices
        needing a communication port, there should be only one obvious choice.
    4.) Select the correct device.

"""

def pretty_print_port(port):
    s = """
        Device: {}
        Manufacturer: {}
        Hardware ID: {}"""
    return s.format(port.device, port.manufacturer, port.hwid)

def _known_ports():
    all_known_ports = list(serial.tools.list_ports.comports())
    
    if all_known_ports == []:
        sys.stderr.write('No ports found. :( Is the Distractinator(TM) connected?')
        raise SystemExit(2)

    for idx, port in enumerate(all_known_ports):
        if port.device.endswith('ttyS4'):
            sys.stdout.write('\n(It is likely *not* this port.)\n')

        sys.stdout.write('[{}]: {}\n'.format(idx, pretty_print_port(port)))

    return all_known_ports

def prompt_for_port(explain=True):
    if explain:
        sys.stdout.write(explanation)
        # Explain, then confirm
        input('Press enter to continue!')

    all_known_ports = _known_ports() 
    port_id = None
    while port_id is None:
        port_id = input("\nSelect a port ('retry' if you still need to plug in the Distractinator(TM)): ")

        if port_id == 'retry':
            all_known_ports = _known_ports() 

        try:
            return all_known_ports[int(port_id)]
        except:
            port_id = None

def sanitize_hwid(hwid):
    return ' '.join(hwid.split(' ')[:2])

def get_hardware_id(debug=False):
    # Obtain hardware id
    correct_port = prompt_for_port().hwid
    # Strip off LOCATION data
    hwid = sanitize_hwid(correct_port)
    if debug:
        print(hwid)

    return hwid

if __name__ == '__main__':
    get_hardware_id()

