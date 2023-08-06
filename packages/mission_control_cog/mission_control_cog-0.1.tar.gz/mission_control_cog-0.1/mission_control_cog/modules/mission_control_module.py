import json
import os

import yaml
from twisted.internet import reactor
from twisted.internet.endpoints import TCP4ClientEndpoint
from twisted.internet.protocol import connectionDone, ReconnectingClientFactory
from twisted.protocols.basic import LineReceiver
from up.base_started_module import BaseStartedModule
from up.commands.command import BaseCommand
from up.utils.up_logger import UpLogger

from mission_control_cog.registrar import Registrar


class MissionControlProvider(BaseStartedModule):
    PROXY_ADDRESS = 'raspilot.projekty.ms.mff.cuni.cz'

    def _execute_initialization(self):
        self.__protocol = MissionControlCommProtocol(self)

    def _execute_start(self):
        config_path = os.path.join(os.getcwd(), 'config', Registrar.CONFIG_FILE_NAME)
        address = None
        port = None
        if os.path.isfile(config_path):
            with open(config_path) as f:
                config = yaml.load(f)
                if config.get(Registrar.REMOTE_SERVER_KEY, None) is not None:
                    address = config[Registrar.REMOTE_SERVER_KEY].get(Registrar.URL_KEY, None)
                    port = config[Registrar.REMOTE_SERVER_KEY].get(Registrar.PORT_KEY)
        if address is not None and port is not None:
            endpoint = TCP4ClientEndpoint(reactor, address, port)
            endpoint.connect(MissionControlCommProtocolFactory(self.__protocol))
            return True
        self.logger.critical('Remote server address or port not set. Set it in %s' % config_path)
        return False

    def _execute_stop(self):
        pass

    def send_message(self, data):
        if self.__protocol.transport:
            reactor.callFromThread(self.__protocol.sendLine, data)

    def execute_command(self, command):
        self.up.command_receiver.execute_command(command)

    def on_connection_opened(self, address):
        self.logger.info("Connected to Mission Control on address {}".format(address))

    def on_connection_lost(self):
        if reactor.running:
            self.logger.error("Connection with Mission Control lost")
        else:
            self.logger.debug("Disconnected from Mission Control")


class MissionControlCommProtocol(LineReceiver):
    def __init__(self, callbacks):
        super().__init__()
        self.delimiter = bytes('\n', 'utf-8')
        self.__callbacks = callbacks
        self.__logger = UpLogger.get_logger()

    def lineReceived(self, line):
        try:
            parts = self.__parse_line(line)
            for part in parts:
                self.__callbacks.execute_command(BaseCommand.from_json(part))
        except json.JSONDecodeError as e:
            self.__logger.error("Invalid data received.\n\tData were {}.\n\tException risen is {}".format(line, e))
        except Exception as e:
            self.__logger.critical(
                "Exception occurred during data processing.\n\tData were {}.\n\tException risen is {}".format(line, e))

    def rawDataReceived(self, data):
        pass

    def connectionMade(self):
        self.__callbacks.on_connection_opened(self.transport.addr[0])

    def connectionLost(self, reason=connectionDone):
        self.__callbacks.on_connection_lost()

    @staticmethod
    def __parse_line(line):
        result = []
        opening = 0
        line_part = ''
        for ch in line.decode('utf-8'):
            if ch == '{':
                opening += 1
            if ch == '}':
                opening -= 1
            line_part += ch
            if opening == 0 and line_part != '':
                result.append(json.loads(line_part))
                line_part = ''
        return result


class MissionControlCommProtocolFactory(ReconnectingClientFactory):
    def __init__(self, protocol):
        super().__init__()
        self.__logger = UpLogger.get_logger()
        self.__protocol = protocol

    def clientConnectionFailed(self, connector, reason):
        self.__logger.debug("Connection failed")
        super().clientConnectionFailed(connector, reason)

    def clientConnectionLost(self, connector, unused_reason):
        self.__logger.debug("clientConnectionLost")
        super().clientConnectionLost(connector, unused_reason)

    def startedConnecting(self, connector):
        self.__logger.debug("startedConnecting")
        super().startedConnecting(connector)

    def buildProtocol(self, addr):
        return self.__protocol
