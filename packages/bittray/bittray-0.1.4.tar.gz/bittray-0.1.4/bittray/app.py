import logging
import os
import signal
import subprocess
import notify2 as notify
import wx
import requests

from exchanges.bitstamp import Bitstamp
from exchanges.coindesk import CoinDesk
from exchanges.bitfinex import Bitfinex

from bitcoinrpc.authproxy import AuthServiceProxy
from bitcoinrpc.authproxy import JSONRPCException

from bittray import config
from bittray import trayicon


ID_ICON_TIMER = wx.NewId()
TRAY_TOOLTIP = 'Network problem?'


class TaskBarIcon(wx.TaskBarIcon):
    """
    This is the interactive systray icon.
    """
    def __init__(self, frame):
        self.frame = frame
        super(TaskBarIcon, self).__init__()
        # self.Bind(wx.EVT_TASKBAR_LEFT_DOWN, self.on_left_click)
        notify.init('bittray')
        self.conf = config.TrayConf()
        self.trayicon = trayicon.TrayIcon(self.conf)
        if self.conf.get_bool('Bitcoin', 'enable'):
            self._connect_api()
        signal.signal(signal.SIGUSR1, self.signal_handler)

    def signal_handler(self, signal, frame):
        """
        Handle SIGUSR1

        I'm not sure why, but I think this code only runs when do_update
        is called.
        """
        self.conf._read_config()
        self.conf._connect_api()

    def _connect_api(self):
        rpc_user = self.conf.get_str('Bitcoin', 'user')
        rpc_pass = self.conf.get_str('Bitcoin', 'password')
        rpc_host = self.conf.get_str('Bitcoin', 'host')
        rpc_port = self.conf.get_str('Bitcoin', 'port')
        connection_string = "http://{}:{}@{}:{}".format(
            rpc_user, rpc_pass, rpc_host, rpc_port)
        self.rpc_connection = AuthServiceProxy(connection_string)

    def create_menu_item(self, menu, label, func):
        """
        Add a menu item to the systray icon menu.
        """
        item = wx.MenuItem(menu, -1, label)
        menu.Bind(wx.EVT_MENU, func, id=item.GetId())
        menu.AppendItem(item)
        return item

    def _rpc_to_str(self, data):
        r = ''
        for key, value in data.items():
            r += '{}: {}\n'.format(key, value)
        return r

    def _rpc_notify(self, label, data):
        data = self._rpc_to_str(data)
        n = notify.Notification(label, data)
        n.show()

    def rpc_getinfo(self, event):
        self._rpc_notify('Info', data=self.rpc_connection.getinfo())

    def rpc_getblockchaininfo(self, event):
        self._rpc_notify('Blockchain info', data=self.rpc_connection.getblockchaininfo())

    def CreatePopupMenu(self):
        """
        Gerenate the wx menu
        """
        menu = wx.Menu()
        if self.conf.get_bool('Electrum', 'enable'):
            menu_electrum = wx.Menu()
            wallets = self.conf.get_path_files('Electrum', 'walletpath')
            electrum = self.conf.get_path('Electrum', 'path')
            for wallet in wallets:
                label = os.path.basename(wallet)

                def launch_electrum(event, wallet=wallet, electrum=electrum):
                    """
                    Launch electrum
                    """
                    subprocess.Popen([electrum, '-w', wallet])

                self.create_menu_item(menu_electrum, label, launch_electrum)
            menu.AppendMenu(1, 'Electrum', menu_electrum)
        if self.conf.get_bool('Bitcoin', 'enable'):
            menu_bitcoin = wx.Menu()
            self.create_menu_item(menu_bitcoin, 'getinfo', self.rpc_getinfo)
            self.create_menu_item(menu_bitcoin, 'getblockchaininfo', self.rpc_getblockchaininfo)
            menu.AppendMenu(1, 'Bitcoin', menu_bitcoin)
        menu.AppendSeparator()
        self.create_menu_item(menu, 'Quit', self.on_quit)
        return menu

    def set_icon_timer(self):
        """
        Sets the icon timer to kick off the main loop.
        """
        self.icon_timer = wx.Timer(self, ID_ICON_TIMER)
        wx.EVT_TIMER(self, ID_ICON_TIMER, self.do_update)
        self.icon_timer.Start(self.conf.get_int('Behavior', 'timer'))
        self.do_update()  # Fire the first right away

    def set_icon(self, value):
        """
        Update icon and tooltip
        """
        icon = self.trayicon.get_icon(value)
        tooltip = self.conf.get_str('Price', 'exchange')
        self.SetIcon(icon, tooltip)

    def do_update(self, event=None):
        """
        The main loop
        """
        logging.debug('Update tray icon')
        price = self.get_price()
        self.set_icon(price)

    def on_quit(self, event):
        """
        Quit the application.
        """
        wx.CallAfter(self.Destroy)
        self.frame.Close()

    def get_price(self):
        """
        Get the price from an exchange
        """
        exchange = self.conf.get_str('Price', 'exchange')
        if exchange == 'coindesk':
            exchange = CoinDesk()
        elif exchange == 'bitstamp':
            exchange = Bitstamp()
        elif exchange == 'bitfinex':
            exchange = Bitfinex()
        else:
            exchange = Bitstamp()
        try:
            price = '{0:.0f}'.format(exchange.get_current_price())
        except requests.exceptions.ConnectionError:
            price = 'err'
        return price


class App(wx.App):
    """
    Them main systray app

    This should fetch the price periodically, and display notifications,
    play alerts and such.
    """
    def OnInit(self):
        frame = wx.Frame(None)
        self.SetTopWindow(frame)
        self.icon = TaskBarIcon(frame)
        self.icon.set_icon_timer()
        return True
