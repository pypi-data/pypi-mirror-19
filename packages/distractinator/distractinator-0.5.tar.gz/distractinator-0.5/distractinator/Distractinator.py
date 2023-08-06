import serial, serial.tools.list_ports
import logging
import time
import importlib
import os
import sys
import argparse
import pkg_resources
import shutil
try:
    import ConfigParser as configparser
except:
    # Python 3
    import configparser
from .events import *
from .hardware import get_hardware_id, sanitize_hwid

class Distractinator:
    def __init__(self):
        # Parse the command line options!
        args = self.parse_cmd_line_opts()
        if args.example_custom_code:
            self.example_custom_code()
            sys.exit(0)

        # Set up logging!
        self.log = self.createlogger(args.log)
        self.log.info('distractd started.')

        # Find and parse the config file!
        if args.config:
            self.setup_config_file()
        else:
            self.config = self.config_file(print_err_msg=True)
            self.default_alert = self.use_default_alert()

        # Find and import the custom actions file!
        try:
            # Let's go find your custom file
            self.usermodule = self.customcode()
        except IOError:
            # I could not find the file you specified :(
            self.log.error("I could not find the custom actions file in the location you specified. :(")
            sys.exit(2)

        # Find and assign the correct port!
        self.p = self.autoconnect() # Won't you join me on the perennial quest?
        on_connect(usermodule=self.usermodule, log=self.log)

    def parse_cmd_line_opts(self):
        desc = "The Distractinator(TM) notifier!"
        parser = argparse.ArgumentParser(description=desc)
        parser.add_argument('--log', help='Absolute path to the desired log. (/path/to/file.log)', type=str, required=False)
        parser.add_argument('--config', help='Setup your config file.', action="store_true", default=False)
        parser.add_argument('--example_custom_code',
                            help='Prints the location of the example customevents.py file.',
                            action="store_true",
                            default=False)
        return parser.parse_args()

    def createlogger(self, logfile_location=None):
        logger = logging.getLogger()

        if logfile_location is None:
            handler = logging.StreamHandler()
        else:
            handler = logging.FileHandler(logfile_location)

        formatter = logging.Formatter('[%(asctime)s] %(levelname)-8s %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)
        return logger

    def config_file(self, print_err_msg=False):
        """ Look for config file in home directory.
            If found, return configparser object.
            If found but not parseable, exit with code 2.
            If not found, note this in the log and run setup_config_file.
        """
        config_location = os.path.join(os.path.expanduser('~'), '.distractinator.conf')
        if not os.path.exists(config_location):
            if print_err_msg:
                self.log.info('No config file found at {}.'.format(config_location))
            self.setup_config_file()

        try:
            cfg = configparser.ConfigParser()
            cfg.read(config_location)
            return cfg
        except:
            self.log.error('Config file at {} could not be read.'.format(config_location))
            sys.exit(2)

    def setup_config_file(self):
        """ Copy the sample configuration file (from examples/) into the user's home directory. """
        config_file = pkg_resources.resource_filename(__name__, 'examples/.distractinator.conf')
        desired_location = os.path.join(os.path.expanduser('~'), '.distractinator.conf')

        self.log.info('Copying the sample config file from {} to {}...'.format(config_file, desired_location))
        shutil.copy(config_file, desired_location)

        hwid = get_hardware_id()

        # Write the hwid to the config file
        config = configparser.ConfigParser()
        config.add_section('hardware')
        config.set('hardware', 'device_id', value=hwid)
        with open(desired_location, 'a') as configfile:
            config.write(configfile)

    def use_default_alert(self):
        """
        Use the default alert unless the user specifies otherwise
        explicitly in the config file.
        """
        try:
            return self.config_file(print_err_msg=False).getboolean('notifier', 'use_default_alert_function')
        except:
            return True

    def example_custom_code(self):
        custom_events_file = pkg_resources.resource_filename(__name__, 'examples/customevents.py')
        sys.stdout.write('Custom Events example file: {}\n'.format(custom_events_file))

    def customcode(self):
        """ Import customevents.py using location specified in config file. """
        if self.config_file(print_err_msg=False):
            try:
                path_to_custom_events = self.config_file().get('notifier', 'custom_script')
                self.log.info('Looking for custom script file at {}...'.format(path_to_custom_events))
            except configparser.NoOptionError:
                self.log.info('custom_script variable not set in config file.')
                return False

            if os.path.exists(path_to_custom_events):
                self.log.info("SUCCESS: Found custom script file at {}.".format(path_to_custom_events))
            else:
                self.log.error("Could not find a file named {}.".format(path_to_custom_events))
                raise IOError

            containing_dir = os.path.split(path_to_custom_events)[0]
            sys.path.append(containing_dir)
            return importlib.import_module('customevents')
        return False

    def get_hardware_id(self):
        try:
            return self.config_file().get('hardware', 'device_id')
        except (configparser.NoOptionError, configparser.NoSectionError):
            config_location = os.path.join(os.path.expanduser('~'), '.distractinator.conf')
            self.log.error("Looks like your config file got messed up during setup. That's okay!")
            self.log.error("You can fix this by removing the file ({}) and re-running distractd.".format(config_location))
            sys.exit(2)

    def identify_board(self, p):
        if sanitize_hwid(p.hwid) == self.get_hardware_id():
            return True
        return False

    def autoconnect(self):
        self.log.info('Attempting to find + connect to USB device...')

        device_not_found = True

        while device_not_found:
            known_ports = list(serial.tools.list_ports.comports())
            for p in known_ports:
                if self.identify_board(p):
                    self.log.info('Found device at address: {}'.format(p.device))
                    device_not_found = False
            time.sleep(1)

        try:
            return serial.Serial(p.device, 9600, timeout=10)
        except serial.serialutil.SerialException as err:
            if 'permission' in err.strerror.lower():
                sys.stderr.write('Please check the permissions on {}.\n'.format(p.device))
                sys.stderr.write('See README for details on resolving.\n')
                sys.exit(2)
            else:
                raise err

    def get_alert_title(self):
        try:
            return self.config_file().get('notifier', 'alert_title')
        except:
            return None

    def get_alert_msg(self):
        try:
            return self.config_file().get('notifier', 'alert_msg')
        except:
            return None

    def alert(self, title=None, msg=None):
        if self.use_default_alert():
            if self.get_alert_title() is None:
                title = "Pay Attention!"
            else:
                title = str(self.get_alert_title())

            if self.get_alert_msg() is None:
                msg = "Someone wants to speak with you."
            else:
                msg = str(self.get_alert_msg())

            rc = alert(title, msg)
            if rc == 0:
                self.log.info('/usr/bin/notify-send received return code 0')
            else:
                self.log.error('/usr/bin/notify-send received return code {}'.format(rc))

    def run(self, port=None):
        if port is None:
            port = self.p

        while True:
            try:
                serialMsg = port.readline().strip()
            except serial.serialutil.SerialException:
                self.log.error('USB disconnected.')
                on_disconnect(usermodule=self.usermodule, log=self.log)

                port = self.autoconnect()
                on_connect(usermodule=self.usermodule, log=self.log)

                serialMsg = port.readline().strip()

            if serialMsg in ('a_recvd', b'a_recvd'): # A Button
                self.log.info('Received {} from serial.'.format(serialMsg.strip()))
                run_action_a(usermodule=self.usermodule, log=self.log)

            if serialMsg in ('b_recvd', b'b_recvd'): # B Button
                self.log.info('Received {} from serial.'.format(serialMsg.strip()))
                run_action_b(usermodule=self.usermodule, log=self.log)

            if serialMsg in ('c_recvd', b'c_recvd'): # C Button
                self.log.info('Received {} from serial.'.format(serialMsg.strip()))
                run_action_c(usermodule=self.usermodule, log=self.log)

            if serialMsg in ('d_recvd', b'd_recvd'): # D Button
                self.log.info('Received {} from serial.'.format(serialMsg.strip()))
                self.alert()
                run_action_d(usermodule=self.usermodule, log=self.log)
