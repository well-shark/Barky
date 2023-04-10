import sys
import argparse
import configparser

import os
import json
import requests


class Bark():

    def __init__(self, client_key=None, server=None, store_config=True):

        self.config_file = os.path.expanduser('~/.bark/config.ini')
        _server, _client_key = self.get_config()

        if client_key is None and _client_key is None:
            raise ValueError('client_key is required, please get it from your bark app.')
        
        self.key = client_key if client_key is not None else _client_key

        if server is None:
            s = 'https://api.day.app' if _server is None else _server
        else:
            s = server[:-1] if server[-1] == '/' else server
        
        self.url = f'{s}/push'

        if store_config:
            self.store_config(s, self.key)

    def send(self, body, title=None, level=None, active=None, 
            timeSensitive=None, passive=None, badge=None, 
            autoCopy=None, copy=None, sound=None, icon=None, 
            group=None, isArchive=None, url=None, verbose=True):
        '''
        Parameters
        -----------
        - body: 推送内容
        - title: 推送标题
        - level: 推送中断级别
            - active: 默认值，系统会立即亮屏显示通知
            - timeSensitive: 时效性通知，可在专注状态下显示通知。
            - passive: 仅将通知添加到通知列表，不会亮屏提醒。
        - active: 默认值，系统会立即亮屏显示通知
        - timeSensitive: 时效性通知，可在专注状态下显示通知。
        - passive: 仅将通知添加到通知列表，不会亮屏提醒。
        - badge: 推送角标，可以是任意数字
        - autoCopy: iOS14.5以下自动复制推送内容, iOS14.5以上需手动长按推送或下拉推送
        - copy: 复制推送时，指定复制的内容，不传此参数将复制整个推送内容。
        - sound: 可以为推送设置不同的铃声
        - icon: 为推送设置自定义图标，设置的图标将替换默认Bark图标。
                图标会自动缓存在本机，相同的图标 URL 仅下载一次。
        - group: 对消息进行分组，推送将按group分组显示在通知中心中。
                也可在历史消息列表中选择查看不同的群组。
        - isArchive: 传 1 保存推送，传其他的不保存推送，不传按APP内设置来决定是否保存。
        - url: 点击推送时，跳转的URL, 支持URL Scheme 和 Universal Link
        '''
        # 循环遍历参数，将非空参数添加到 params 中
        params = {k:v for k,v in locals().items() if v is not None and k != 'self' and k != 'verbose'}
        # 增加 key
        params['device_key'] = self.key
        # 指定 Content-Type
        headers = {'Content-Type': 'application/json; charset=utf-8'}
        # 判断 sound 是否有效
        if sound is not None and sound not in self.get_vaild_sound():
            raise ValueError('{} is not a valid sound, please use get_vaild_sound() to get valid sound.'.format(sound))
        try:
            response = requests.post(self.url, data=json.dumps(params), headers=headers)
            if response.status_code != 200:
                if verbose:
                    print('Error sending notification: {}, {}'.format(response.status_code, response.text))
                return False
            else:
                if verbose:
                    print('Sent notification: {}'.format(response.text))
                return True
        except Exception as e:
            if verbose:
                print('Error sending notification: {}'.format(e))
            return False
    
    def get_vaild_sound(self):
        '''
        获取可用的 sound
        '''
        return ['alarm', 'anticipate', 'bell', 'birdsong', 'bloom', 'calypso', 
                'chime', 'choo', 'descent', 'electronic', 'fanfare', 'glass', 
                'gotosleep', 'healthnotification', 'horn', 'ladder', 'mailsent', 
                'minuet', 'multiwayinvitation', 'newmail', 'newflash', 'noir', 
                'paymentsuccess', 'shake', 'sherwoodforest', 'silence', 'spell', 
                'suspense', 'telegraph', 'tiptoes', 'typewriters', 'update',]

    def store_config(self, server, key):
        '''
        存储配置
        '''
        if not os.path.exists(os.path.expanduser('~/.bark')):
            os.mkdir(os.path.expanduser('~/.bark'))

        config = configparser.ConfigParser()
        config.set('DEFAULT', 'server', server)  
        config.set('DEFAULT', 'client_key', key)
        config.write(open(self.config_file, 'w'))

    def get_config(self):
        '''
        获取配置
        '''
        if not os.path.exists(self.config_file):
            return None, None
        else:
            config = configparser.ConfigParser()
            config.read(self.config_file)
            server = config['DEFAULT']['server']
            key = config['DEFAULT']['client_key']
            return key, server

def main(*argv):
    ''' For build command line tool
    '''
    if not argv:
        argv = list(sys.argv)

    parser = argparse.ArgumentParser(description='Bark command line tool')

    parser.add_argument('-s', '--server', help='server url', default=None)
    parser.add_argument('-k', '--client_key', help='client key', required=True)
    
    args = parser.parse_args(argv[1:])
    Bark(args.server, args.client_key, store_config=True)

if __name__ == '__main__':
    # Test Here
    server_url = 'server url'
    key = 'your key'
    bark = Bark(server=server_url, client_key=key)

    bark.send('Hello World')
