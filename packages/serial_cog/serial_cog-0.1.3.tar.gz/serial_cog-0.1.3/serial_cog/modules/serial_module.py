from threading import Event, Thread

import serial
from up.base_started_module import BaseStartedModule
from up.utils.up_logger import UpLogger


class SerialProvider(BaseStartedModule):
    BAUD_RATE_DEFAULT = 9600
    LOAD_ORDER = 0

    def __init__(self):
        super().__init__()
        self._load_order = self.LOAD_ORDER
        self.__serial_port = None
        self.__baud_rate = None
        self.__serial = None
        self.__receive_loop_lock = None
        self.__is_connected = False
        self.__receive_loop_lock = None
        self.__handler = SerialCommandHandler()

    def add_handler(self, cmd_type, handler, payload_size=0, args=None):
        self.__handler.add_handler(cmd_type, handler, payload_size, args)

    def remove_handler(self, cmd_type):
        self.__handler.remove_handler(cmd_type)

    def send_command(self, cmd, data=None):
        try:
            self.logger.debug("Sending command %s" % cmd)
            self.__serial.write(bytes(cmd, 'utf-8'))
            if data:
                self.__serial.write(data)
        except serial.SerialException as e:
            self._log_error("An error occurred during transmission to Arduino. Error was {}".format(e))

    def _execute_initialization(self):
        pass

    def _execute_start(self):
        if not self.port or not self.baud_rate:
            self.logger.critical('Port and baud rate must be set')
            raise ValueError('Port and baud rate must be set')
        self.__serial = serial.Serial()
        self.__serial.port = self.port
        self.__serial.baudrate = self.baud_rate
        self.__serial.open()
        self.__receive_loop_lock = Event()
        Thread(target=self.__receive_loop).start()
        self.__receive_loop_lock.wait(10)
        self.logger.debug('Serial port opened')
        return self.__serial.is_open

    def _execute_stop(self):
        if self.__serial and self.__serial.is_open:
            self.__serial.close()
            self.__is_connected = False

    def __receive_loop(self):
        while self.__serial.is_open:
            try:
                if self.__receive_loop_lock:
                    self.__receive_loop_lock.set()
                cmd_type = self.__serial.read(1)
                self.__is_connected = True
                payload_size = self.__handler.get_command_payload_size(cmd_type)
                payload = self.__serial.read(payload_size)
                self.__handler.execute_action(cmd_type, payload)
            except serial.SerialException as e:
                if self.started:
                    self._log_critical("Error during receiving Arduino data. Error was {}".format(e))
            except TypeError as e:
                if not self.started:
                    pass
                else:
                    raise e

    def load(self):
        return True

    @property
    def port(self):
        return self.__serial_port

    @port.setter
    def port(self, value):
        self.__serial_port = value

    @property
    def baud_rate(self):
        return self.__baud_rate

    @baud_rate.setter
    def baud_rate(self, value):
        self.__baud_rate = value


class SerialCommandHandler:
    def __init__(self):
        self.__handlers = {}
        self.__logger = UpLogger.get_logger()

    def add_handler(self, cmd_type, handler, payload_size=0, args=None):
        if not callable(handler):
            raise ValueError("Handler argument must be callable")
        type_bytes = bytes(cmd_type, 'utf-8')
        self.__handlers[type_bytes] = (handler, payload_size, args)
        self.__logger.debug("Handler for command type '%s' registered" % cmd_type)

    def remove_handler(self, cmd_type_bytes):
        self.__handlers[cmd_type_bytes] = None

    def execute_action(self, cmd_type_bytes, payload):
        cmd_type = cmd_type_bytes.decode('utf-8')
        self.__logger.debug("Executing action for cmd type '%s'" % cmd_type)
        handler = self.__handlers.get(cmd_type_bytes, None)
        if handler:
            args = handler[2]
            method = handler[0]
            if args is not None:
                method(payload, args)
            else:
                method(payload)
        else:
            self.__logger.warn("No handler for cmd type '%s' found" % cmd_type)

    def get_command_payload_size(self, cmd_type_bytes):
        handler = self.__handlers.get(cmd_type_bytes, None)
        if handler:
            return handler[1]
        return 0
