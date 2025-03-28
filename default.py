# -*- coding: utf-8 -*-

#
# xbmc.executebuiltin(f'RunPlugin(plugin://script.test.notifier/?addon={addon}&message={message})')
#

import sys
from urllib.parse import parse_qs
import urllib.request
import urllib.parse

import xbmc
import xbmcaddon

ADDON = xbmcaddon.Addon().getSetting

if __name__ == '__main__':

    args = parse_qs(sys.argv[2][1:], keep_blank_values=True)
    for key, val in args.items():
        args[key] = val[0]

    addon = xbmcaddon.Addon()
    url = addon.getSetting('url')
    name = args.get('addon', addon.getAddonInfo('name'))
    message = args.get('message')

    if url and message:
        # local notification
        # xbmc.executebuiltin('Notification("%s","%s",%d,"%s")' % (name, message, 3000, ''))
        # remote notification
        # データをURLエンコード（フォーム形式）
        data = urllib.parse.urlencode({
            'addon': name,
            'message': message
        }).encode('utf-8')
        # ヘッダー設定
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        # リクエスト作成
        req = urllib.request.Request(url, data=data, headers=headers)
        # 送信してレスポンスを取得
        with urllib.request.urlopen(req) as response:
            response.read().decode('utf-8')
