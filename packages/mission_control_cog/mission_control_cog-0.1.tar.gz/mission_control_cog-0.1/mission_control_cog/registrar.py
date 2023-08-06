from up.registrar import UpRegistrar



class Registrar(UpRegistrar):
    PORT_KEY = 'port'
    CONFIG_FILE_NAME = 'mission_control.yml'
    REMOTE_SERVER_KEY = 'remote_server'
    URL_KEY = 'url'

    CONFIG_TEMPLATE = """\
%s:
  %s: # Paste your URL here
  %s: # Paste your PORT here
""" % (REMOTE_SERVER_KEY, URL_KEY, PORT_KEY)

    def __init__(self):
        super().__init__('mission_control_cog')

    def register(self):
        external_modules = self._load_external_modules()
        if external_modules is not None:
            self._register_module('MissionControlProvider', 'mission_control_cog.modules.mission_control_module')
            self._write_external_modules()
        self._create_config(self.CONFIG_FILE_NAME, self.CONFIG_TEMPLATE)
        return True
