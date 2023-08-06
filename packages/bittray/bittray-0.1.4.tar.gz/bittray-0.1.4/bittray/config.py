import logging
import os
from matplotlib import font_manager
from webcolors import name_to_rgb
try:
    import ConfigParser as configparser
except ImportError:
    import configparser


class TrayConf(object):
    """
    Configuration handling for bittray
    """
    def __init__(self):
        # TODO configuratble
        configfile = '.config/bittray/bittray.cfg'
        self.configfile = os.path.join(os.path.expanduser('~'), configfile)
        self.config = configparser.RawConfigParser(allow_no_value=True)
        self._write_default_config()
        self._read_config()
        self._update_config()

    def _write_default_config(self):
        """
        Create the default config file if it doesn't exist yet.
        """
        if os.path.isfile(self.configfile):
            return
        conf_dir = os.path.dirname(self.configfile)
        if not os.path.exists(conf_dir):
            logging.info('Creating config dir {}'.format(conf_dir))
            os.makedirs(conf_dir)
        logging.info('Writing default configuration to {}'.format(self.configfile))
        self.config.add_section('Behavior')
        self.config.set(
            'Behavior',
            '; delay between price updates in milliseconds'
        )
        self.config.set('Behavior', 'timer', 5000)
        self.config.add_section('Price')
        self.config.set('Price', '; one of bitstamp, coindesk, bitfinex')
        self.config.set('Price', 'exchange', 'bitfinex')
        self.config.add_section('Look')
        self.config.set(
            'Look',
            '; if Roboto is not available a fallback will be used'
        )
        self.config.set('Look', 'font', 'Roboto')
        self.config.set(
            'Look',
            '; If font_path is set it takes precedence'
        )
        self.config.set(
            'Look',
            '; font_path=/usr/share/fonts/truetype/liberation/LiberationMono-Bold.ttf'
        )
        self.config.set(
            'Look',
            '; For valid colors see https://en.wikipedia.org/wiki/Web_colors'
        )
        self.config.set('Look', 'color', 'lightgreen')
        self.config.set('Look', 'background', 'black')
        self.config.set(
            'Look',
            '; You should probably set the size to the height of your systray'
        )
        self.config.set('Look', 'size', 20)
        self._write_config()

    def _write_config(self):
        with open(self.configfile, 'wb') as configfile:
            self.config.write(configfile)

    def _read_config(self):
        self.config.read(self.configfile)

    def _update_config(self):
        """
        Add default values for settings added after initial release.
        """
        updated = False
        if not self.config.has_section('Electrum'):
            self.config.add_section('Electrum')
            self.config.set('Electrum', 'enable', 'Off')
            self.config.set('Electrum', 'walletpath', '~/.electrum/wallets/')
            self.config.set('Electrum', 'path', '/usr/bin/electrum')
            updated = True

        if not self.config.has_section('Bitcoin'):
            self.config.add_section('Bitcoin')
            self.config.set('Bitcoin', 'enable', 'Off')
            self.config.set('Bitcoin', 'host', '127.0.0.1')
            self.config.set('Bitcoin', 'port', '8332')
            self.config.set('Bitcoin', '; user=rpcuser')
            self.config.set('Bitcoin', '; password=rpcpass')
            updated = True

        # self.config.set('Behavior', 'click', '/bin/true')
        # self.config.set('Behavior', 'notify', 'On')
        # self.config.set('Behavior', 'notify_change_type', 'percent')
        # self.config.set('Behavior', 'notify_change_value', 10)
        # self.config.set('Behavior', 'notify_change_period', '24h')
        # self.config.set('Behavior', 'notify_abs', '1000, 1500, 2000')
        # self.config.set('Behavior', 'notify_quiet', '1h')

        if updated:
            self._write_config()

    def _get(self, namespace, attribute):
        return self.config.get(namespace, attribute)

    def get_font_path(self):
        try:
            font_path = self._get('Look', 'font_path')
        except configparser.NoOptionError:
            font = self._get('Look', 'font')
            font_path = font_manager.findfont(font)
        return font_path

    def get_color(self, namespace, attribute):
        """
        Return rgba
        """
        color = self._get(namespace, attribute)
        return name_to_rgb(color)

    def get_int(self, namespace, attribute):
        return int(self._get(namespace, attribute))

    def get_str(self, namespace, attribute):
        return self._get(namespace, attribute)

    def get_bool(self, namespace, attribute):
        value = self._get(namespace, attribute)
        if value == 'On' or value == 'on':
            return True
        return False

    def get_path(self, namespace, attribute):
        path = self._get(namespace, attribute)
        return os.path.expanduser(path)

    def get_path_files(self, namespace, attribute):
        path = self.get_path(namespace, attribute)
        return [
            os.path.join(path, f)
            for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
