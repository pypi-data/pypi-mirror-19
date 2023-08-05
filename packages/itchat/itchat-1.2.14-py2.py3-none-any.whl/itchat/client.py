#coding=utf8
import os, sys, time, re, io
import threading, subprocess
import json, xml.dom.minidom, mimetypes
import copy, pickle, random
import traceback
try:
    import Queue
except ImportError:
    import queue as Queue

import requests

from . import config, storage, out, tools

BASE_URL = config.BASE_URL
QR_DIR = 'QR.jpg'

class client(object):
    def __init__(self):
        self.storageClass = storage.Storage()
        self.memberList = self.storageClass.memberList
        self.mpList = self.storageClass.mpList
        self.chatroomList = self.storageClass.chatroomList
        self.msgList = self.storageClass.msgList
        self.loginInfo = {}
        self.s = requests.Session()
        self.uuid = None
        self.debug = False
    def dump_login_status(self, fileDir):
        try:
            with open(fileDir, 'w') as f: f.write('DELETE THIS')
            os.remove(fileDir)
        except:
            raise Exception('Incorrect fileDir')
        status = {
            'loginInfo' : self.loginInfo,
            'cookies'   : self.s.cookies.get_dict(),
            'storage'   : self.storageClass.dumps()}
        with open(fileDir, 'wb') as f:
            pickle.dump(status, f)
    def load_login_status(self, fileDir):
        try:
            with open(fileDir, 'rb') as f:
                j = pickle.load(f)
        except Exception as e:
            return False
        self.loginInfo = j['loginInfo']
        self.s.cookies = requests.utils.cookiejar_from_dict(j['cookies'])
        self.storageClass.loads(j['storage'])
        msgList, contactList = self.__get_msg()
        if (msgList or contactList) is None:
            self.s.cookies.clear()
            del self.chatroomList[:]
            # other info will be automatically cleared
            return False
        else:
            if contactList: self.__update_chatrooms(contactList)
            if msgList:
                msgList = self.__produce_msg(msgList)
                for msg in msgList: self.msgList.put(msg)
            out.print_line('Login successfully as %s\n'%self.storageClass.nickName, True)
            self.start_receiving()
            return True
    def auto_login(self, enableCmdQR=False, picDir=None):
        def open_QR():
            for get_count in range(10):
                out.print_line('Getting uuid', True)
                while not self.get_QRuuid(): time.sleep(1)
                out.print_line('Getting QR Code', True)
                if self.get_QR(enableCmdQR=enableCmdQR, picDir=picDir): break
                elif 9 <= get_count:
                    out.print_line('Failed to get QR Code, please restart the program')
                    sys.exit()
            out.print_line('Please scan the QR Code', True)
        open_QR()
        while 1:
            status = self.check_login(picDir=picDir)
            if status == '200':
                break
            elif status == '201':
                out.print_line('Please press confirm', True)
            elif status == '408':
                out.print_line('Reloading QR Code\n', True)
                open_QR()
        self.web_init()
        self.show_mobile_login()
        tools.clear_screen()
        self.get_contact(True)
        out.print_line('Login successfully as %s\n'%self.storageClass.nickName, False)
        self.start_receiving()
    def get_QRuuid(self):
        url = '%s/jslogin'%BASE_URL
        params = {
            'appid' : 'wx782c26e4c19acffb',
            'fun'   : 'new', }
        headers = { 'User-Agent' : config.USER_AGENT }
        r = self.s.get(url, params=params, headers=headers)
        regx = r'window.QRLogin.code = (\d+); window.QRLogin.uuid = "(\S+?)";'
        data = re.search(regx, r.text)
        if data and data.group(1) == '200':
            self.uuid = data.group(2)
            return self.uuid
    def get_QR(self, uuid=None, enableCmdQR=False, picDir=None):
        try:
            if uuid == None: uuid = self.uuid
            url = '%s/qrcode/%s'%(BASE_URL, uuid)
            headers = { 'User-Agent' : config.USER_AGENT }
            r = self.s.get(url, stream=True, headers=headers)
            picDir = picDir or QR_DIR
            with open(picDir, 'wb') as f: f.write(r.content)
        except:
            return False
        if enableCmdQR:
            tools.print_cmd_qr(picDir, enableCmdQR = enableCmdQR)
        else:
            tools.print_qr(picDir)
        return True
    def check_login(self, uuid=None, picDir=None):
        if uuid is None: uuid = self.uuid
        url = '%s/cgi-bin/mmwebwx-bin/login'%BASE_URL
        params = 'tip=1&uuid=%s&_=%s'%(uuid, int(time.time()))
        headers = { 'User-Agent' : config.USER_AGENT }
        r = self.s.get(url, params=params, headers=headers)
        regx = r'window.code=(\d+)'
        data = re.search(regx, r.text)
        if data and data.group(1) == '200':
            os.remove(picDir or QR_DIR)
            regx = r'window.redirect_uri="(\S+)";'
            self.loginInfo['url'] = re.search(regx, r.text).group(1)
            headers = { 'User-Agent' : config.USER_AGENT }
            r = self.s.get(self.loginInfo['url'], headers=headers, allow_redirects=False)
            self.loginInfo['url'] = self.loginInfo['url'][:self.loginInfo['url'].rfind('/')]
            for indexUrl, detailedUrl in (
                    ("wx2.qq.com"      , ("file.wx2.qq.com", "webpush.wx2.qq.com")),
                    ("wx8.qq.com"      , ("file.wx8.qq.com", "webpush.wx8.qq.com")),
                    ("qq.com"          , ("file.wx.qq.com", "webpush.wx.qq.com")),
                    ("web2.wechat.com" , ("file.web2.wechat.com", "webpush.web2.wechat.com")),
                    ("wechat.com"      , ("file.web.wechat.com", "webpush.web.wechat.com"))):
                fileUrl, syncUrl = ['https://%s/cgi-bin/mmwebwx-bin' % url for url in detailedUrl]
                if indexUrl in self.loginInfo['url']:
                    self.loginInfo['fileUrl'], self.loginInfo['syncUrl'] = \
                        fileUrl, syncUrl
                    break
            else:
                self.loginInfo['fileUrl'] = self.loginInfo['syncUrl'] = self.loginInfo['url']
            self.loginInfo['deviceid'] = 'e' + repr(random.random())[2:17]
            self.loginInfo['msgid'] = int(time.time() * 1000)
            self.loginInfo['BaseRequest'] = {}
            for node in xml.dom.minidom.parseString(r.text).documentElement.childNodes:
                if node.nodeName == 'skey':
                    self.loginInfo['skey'] = self.loginInfo['BaseRequest']['Skey'] = node.childNodes[0].data
                elif node.nodeName == 'wxsid':
                    self.loginInfo['wxsid'] = self.loginInfo['BaseRequest']['Sid'] = node.childNodes[0].data
                elif node.nodeName == 'wxuin':
                    self.loginInfo['wxuin'] = self.loginInfo['BaseRequest']['Uin'] = node.childNodes[0].data
                elif node.nodeName == 'pass_ticket':
                    self.loginInfo['pass_ticket'] = self.loginInfo['BaseRequest']['DeviceID'] = node.childNodes[0].data
            return '200'
        elif data and data.group(1) == '201':
            return '201'
        elif data and data.group(1) == '408':
            return '408'
        else:
            return '0'
    def web_init(self):
        url = '%s/webwxinit?r=%s' % (self.loginInfo['url'], int(time.time()))
        payloads = {
            'BaseRequest': self.loginInfo['BaseRequest'], }
        headers = { 'ContentType': 'application/json; charset=UTF-8', 'User-Agent' : config.USER_AGENT }
        r = self.s.post(url, data = json.dumps(payloads), headers = headers)
        dic = json.loads(r.content.decode('utf-8', 'replace'))
        tools.emoji_formatter(dic['User'], 'NickName')
        self.loginInfo['InviteStartCount'] = int(dic['InviteStartCount'])
        self.loginInfo['User'] = tools.struct_friend_info(dic['User'])
        self.loginInfo['SyncKey'] = dic['SyncKey']
        self.loginInfo['synckey'] = '|'.join(['%s_%s' % (item['Key'], item['Val']) for item in dic['SyncKey']['List']])
        self.storageClass.userName = dic['User']['UserName']
        self.storageClass.nickName = dic['User']['NickName']
        return dic['User']
    def update_chatroom(self, userName, detailedMember=False):
        url = '%s/webwxbatchgetcontact?type=ex&r=%s' % (self.loginInfo['url'], int(time.time()))
        headers = { 'ContentType': 'application/json; charset=UTF-8', 'User-Agent' : config.USER_AGENT }
        payloads = {
            'BaseRequest': self.loginInfo['BaseRequest'],
            'Count': 1,
            'List': [{
                'UserName': userName,
                'ChatRoomId': '', }], }
        j = json.loads(self.s.post(url, data = json.dumps(payloads), headers = headers
                ).content.decode('utf8', 'replace'))['ContactList'][0]

        if detailedMember:
            def get_detailed_member_info(encryChatroomId, memberList):
                url = '%s/webwxbatchgetcontact?type=ex&r=%s' % (self.loginInfo['url'], int(time.time()))
                headers = { 'ContentType': 'application/json; charset=UTF-8', 'User-Agent' : config.USER_AGENT }
                payloads = {
                    'BaseRequest': self.loginInfo['BaseRequest'],
                    'Count': len(j['MemberList']),
                    'List': [{'UserName': member['UserName'], 'EncryChatRoomId': j['EncryChatRoomId']} \
                        for member in memberList],
                    }
                return json.loads(self.s.post(url, data = json.dumps(payloads), headers = headers
                        ).content.decode('utf8', 'replace'))['ContactList']
            MAX_GET_NUMBER = 50
            totalMemberList = []
            for i in range(len(j['MemberList']) / MAX_GET_NUMBER + 1):
                memberList = j['MemberList'][i*MAX_GET_NUMBER: (i+1)*MAX_GET_NUMBER]
                totalMemberList += get_detailed_member_info(j['EncryChatRoomId'], memberList)
            j['MemberList'] = totalMemberList

        self.__update_chatrooms([j])
        return self.storageClass.search_chatrooms(userName=j['UserName'])
    def get_contact(self, update=False):
        if 1 < len(self.memberList) and not update: return copy.deepcopy(self.memberList)
        url = '%s/webwxgetcontact?r=%s&seq=0&skey=%s' % (self.loginInfo['url'],
            int(time.time()), self.loginInfo['skey'])
        headers = { 'ContentType': 'application/json; charset=UTF-8', 'User-Agent' : config.USER_AGENT }
        r = self.s.get(url, headers=headers)
        tempList = json.loads(r.content.decode('utf-8', 'replace'))['MemberList']
        del self.memberList[:]
        del self.mpList[:]
        chatroomList = []
        # chatroomList will not be cleared because:
        # when initializing, it's cleared once
        # when updating, there's not need for clearing
        self.memberList.append(self.loginInfo['User'])
        for m in tempList:
            tools.emoji_formatter(m, 'NickName')
            if m['Sex'] != 0:
                self.memberList.append(m)
            elif not (any([str(n) in m['UserName'] for n in range(10)]) and
                    any([chr(n) in m['UserName'] for n in (
                    list(range(ord('a'), ord('z') + 1)) +
                    list(range(ord('A'), ord('Z') + 1)))])):
                continue # userName have number and str
            elif '@@' in m['UserName']:
                m['isAdmin'] = None # this value will be set after update_chatroom
                chatroomList.append(m)
            elif '@' in m['UserName']:
                if m['VerifyFlag'] & 8 == 0:
                    self.memberList.append(m)
                else:
                    self.mpList.append(m)
        if chatroomList: self.__update_chatrooms(chatroomList)
        return copy.deepcopy(chatroomList)
    def get_friends(self, update=False):
        if update: self.get_contact(update=True)
        return copy.deepcopy(self.memberList)
    def get_chatrooms(self, update=False):
        ''' get chatrooms
         * if update is set to True, this will only return chatrooms in contact
        '''
        if update:
            return self.get_contact(update=True)
        else:
            return copy.deepcopy(self.chatroomList)
    def get_mps(self, update=False):
        if update: self.get_contact(update=True)
        return copy.deepcopy(self.mpList)
    def show_mobile_login(self):
        url = '%s/webwxstatusnotify?lang=zh_CN&pass_ticket=%s'%(self.loginInfo['url'],self.loginInfo['pass_ticket'])
        payloads = {
                'BaseRequest': self.loginInfo['BaseRequest'],
                'Code': 3,
                'FromUserName': self.storageClass.userName,
                'ToUserName': self.storageClass.userName,
                'ClientMsgId': int(time.time()),
                }
        headers = { 'ContentType': 'application/json; charset=UTF-8', 'User-Agent' : config.USER_AGENT }
        r = self.s.post(url, data = json.dumps(payloads), headers = headers)
    def start_receiving(self):
        def maintain_loop():
            i = self.__sync_check()
            count = 0
            while i and count <4:
                try:
                    if i != '0':
                        msgList, contactList = self.__get_msg()
                        if contactList: self.__update_chatrooms(contactList)
                        if msgList:
                            msgList = self.__produce_msg(msgList)
                            for msg in msgList: self.msgList.put(msg)
                    i = self.__sync_check()
                    count = 0
                except requests.exceptions.RequestException as e:
                    count += 1
                    if self.debug: traceback.print_exc()
                    time.sleep(count * 3)
                except Exception as e:
                    out.print_line(str(e), False)
                    if self.debug: traceback.print_exc()
            out.print_line('LOG OUT', False)
        maintainThread = threading.Thread(target = maintain_loop)
        maintainThread.setDaemon(True)
        maintainThread.start()
    def __sync_check(self):
        url = '%s/synccheck' % self.loginInfo.get('syncUrl', self.loginInfo['url'])
        params = {
            'r'        : int(time.time() * 1000),
            'skey'     : self.loginInfo['skey'],
            'sid'      : self.loginInfo['wxsid'],
            'uin'      : self.loginInfo['wxuin'],
            'deviceid' : self.loginInfo['deviceid'],
            'synckey'  : self.loginInfo['synckey'],
            '_'        : int(time.time() * 1000),}
        headers = { 'User-Agent' : config.USER_AGENT }
        r = self.s.get(url, params=params, headers=headers)
        regx = r'window.synccheck={retcode:"(\d+)",selector:"(\d+)"}'
        pm = re.search(regx, r.text)
        if pm is None or pm.group(1) != '0' : return None
        return pm.group(2)
    def __get_msg(self):
        url = '%s/webwxsync?sid=%s&skey=%s&pass_ticket=%s'%(
            self.loginInfo['url'], self.loginInfo['wxsid'], self.loginInfo['skey'],self.loginInfo['pass_ticket'])
        payloads = {
            'BaseRequest': self.loginInfo['BaseRequest'],
            'SyncKey': self.loginInfo['SyncKey'],
            'rr': ~int(time.time()), }
        headers = { 'ContentType': 'application/json; charset=UTF-8', 'User-Agent' : config.USER_AGENT }
        r = self.s.post(url, data=json.dumps(payloads), headers=headers)
        dic = json.loads(r.content.decode('utf-8', 'replace'))
        if dic['BaseResponse']['Ret'] != 0: return None, None
        self.loginInfo['SyncKey'] = dic['SyncCheckKey']
        self.loginInfo['synckey'] = '|'.join(['%s_%s' % (item['Key'], item['Val']) for item in dic['SyncCheckKey']['List']])
        return dic['AddMsgList'], dic['ModContactList']
    def __update_chatrooms(self, l):
        oldUsernameList = []
        for chatroom in l:
            # format NickName & DisplayName & self keys
            tools.emoji_formatter(chatroom, 'NickName')
            for member in chatroom['MemberList']:
                if self.storageClass.userName == member['UserName']:
                    chatroom['self'] = member
                tools.emoji_formatter(member, 'NickName')
                tools.emoji_formatter(member, 'DisplayName')
            # get useful information from old version of this chatroom
            oldChatroom = tools.search_dict_list(
                self.chatroomList, 'UserName', chatroom['UserName'])
            if oldChatroom is not None:
                memberList, oldMemberList = \
                    chatroom['MemberList'], oldChatroom['MemberList']
                # update member list
                if memberList:
                    for member in memberList:
                        oldMember = tools.search_dict_list(
                            oldMemberList, 'UserName', member['UserName'])
                        if oldMember is not None:
                            for k in oldMember:
                                member[k] = member[k] or oldMember[k]
                else:
                    chatroom['MemberList'] = oldMemberList
                # update other info
                for k in oldChatroom:
                    chatroom[k] = chatroom.get(k) or oldChatroom[k]
                # ready for deletion
                oldUsernameList.append(oldChatroom['UserName'])
            # update OwnerUin
            if chatroom.get('ChatRoomOwner'):
                chatroom['OwnerUin'] = tools.search_dict_list(
                    chatroom['MemberList'], 'UserName', chatroom['ChatRoomOwner'])['Uin']
            # update isAdmin
            if 'OwnerUin' in chatroom and chatroom['OwnerUin'] != 0:
                chatroom['isAdmin'] = \
                    chatroom['OwnerUin'] == int(self.loginInfo['wxuin'])
            else:
                chatroom['isAdmin'] = None
        # delete old chatrooms
        oldIndexList = []
        for i, chatroom in enumerate(self.chatroomList):
            if chatroom['UserName'] in oldUsernameList:
                oldIndexList.append(i)
        oldIndexList.sort(reverse=True)
        for i in oldIndexList: del self.chatroomList[i]
        # add new chatrooms
        for chatroom in l:
            self.chatroomList.append(chatroom)
    def __get_download_fn(self, url, msgId):
        def download_fn(downloadDir=None):
            params = {
                'msgid': msgId,
                'skey': self.loginInfo['skey'],}
            headers = { 'User-Agent' : config.USER_AGENT }
            r = self.s.get(url, params=params, stream=True, headers = headers)
            tempStorage = io.BytesIO()
            for block in r.iter_content(1024):
                tempStorage.write(block)
            if downloadDir is None: return tempStorage.getvalue()
            with open(downloadDir, 'wb') as f: f.write(tempStorage.getvalue())
        return download_fn
    def __produce_msg(self, l):
        rl = []
        srl = [40, 43, 50, 52, 53, 9999]
        # 40 msg, 43 videochat, 50 VOIPMSG, 52 voipnotifymsg, 53 webwxvoipnotifymsg, 9999 sysnotice
        for m in l:
            if '@@' in m['FromUserName'] or '@@' in m['ToUserName']:
                self.__produce_group_chat(m)
            else:
                tools.msg_formatter(m, 'Content')
            if m['MsgType'] == 1: # words
                if m['Url']:
                    regx = r'(.+?\(.+?\))'
                    data = re.search(regx, m['Content'])
                    data = 'Map' if data is None else data.group(1)
                    msg = {
                        'Type': 'Map',
                        'Text': data,}
                else:
                    msg = {
                        'Type': 'Text',
                        'Text': m['Content'],}
            elif m['MsgType'] == 3 or m['MsgType'] == 47: # picture
                download_fn = self.__get_download_fn(
                    '%s/webwxgetmsgimg' % self.loginInfo['url'], m['NewMsgId'])
                msg = {
                    'Type'     : 'Picture',
                    'FileName' : '%s.%s'%(time.strftime('%y%m%d-%H%M%S', time.localtime()),
                        'png' if m['MsgType'] == 3 else 'gif'),
                    'Text'     : download_fn, }
            elif m['MsgType'] == 34: # voice
                download_fn = self.__get_download_fn(
                    '%s/webwxgetvoice' % self.loginInfo['url'], m['NewMsgId'])
                msg = {
                    'Type': 'Recording',
                    'FileName' : '%s.mp4' % time.strftime('%y%m%d-%H%M%S', time.localtime()),
                    'Text': download_fn,}
            elif m['MsgType'] == 37: # friends
                msg = {
                    'Type': 'Friends',
                    'Text': {
                        'status'        : m['Status'],
                        'userName'      : m['RecommendInfo']['UserName'],
                        'ticket'        : m['Ticket'],
                        'userInfo' : m['RecommendInfo'], }, }
            elif m['MsgType'] == 42: # name card
                msg = {
                    'Type': 'Card',
                    'Text': m['RecommendInfo'], }
            elif m['MsgType'] == 49: # sharing
                if m['AppMsgType'] == 6:
                    msg = m
                    cookiesList = {name:data for name,data in self.s.cookies.items()}
                    def download_atta(attaDir=None):
                        url = self.loginInfo['fileUrl'] + '/webwxgetmedia'
                        params = {
                            'sender': msg['FromUserName'],
                            'mediaid': msg['MediaId'],
                            'filename': msg['FileName'],
                            'fromuser': self.loginInfo['wxuin'],
                            'pass_ticket': 'undefined',
                            'webwx_data_ticket': cookiesList['webwx_data_ticket'],}
                        headers = { 'User-Agent' : config.USER_AGENT }
                        r = self.s.get(url, params=params, stream=True, headers=headers)
                        tempStorage = io.BytesIO()
                        for block in r.iter_content(1024):
                            tempStorage.write(block)
                        if attaDir is None: return tempStorage.getvalue()
                        with open(attaDir, 'wb') as f: f.write(tempStorage.getvalue())
                    msg = {
                        'Type': 'Attachment',
                        'Text': download_atta, }
                elif m['AppMsgType'] == 17:
                    msg = {
                        'Type': 'Note',
                        'Text': m['FileName'], }
                elif m['AppMsgType'] == 2000:
                    regx = r'\[CDATA\[(.+?)\][\s\S]+?\[CDATA\[(.+?)\]'
                    data = re.search(regx, m['Content'])
                    if data:
                        data = data.group(2).split(u'。')[0]
                    else:
                        data = 'You may found detailed info in Content key.'
                    msg = {
                        'Type': 'Note',
                        'Text': data, }
                else:
                    msg = {
                        'Type': 'Sharing',
                        'Text': m['FileName'], }
            elif m['MsgType'] == 51: # phone init
                msg = {
                    'Type': 'Init',
                    'Text': m['ToUserName'], }
            elif m['MsgType'] == 62: # tiny video
                msgId = m['MsgId']
                def download_video(videoDir=None):
                    url = '%s/webwxgetvideo' % self.loginInfo['url']
                    params = {
                        'msgid': msgId,
                        'skey': self.loginInfo['skey'],}
                    headers = {'Range': 'bytes=0-', 'User-Agent' : config.USER_AGENT }
                    r = self.s.get(url, params=params, headers=headers, stream=True)
                    tempStorage = io.BytesIO()
                    for block in r.iter_content(1024):
                        tempStorage.write(block)
                    if videoDir is None: return tempStorage.getvalue()
                    with open(videoDir, 'wb') as f: f.write(tempStorage.getvalue())
                msg = {
                    'Type': 'Video',
                    'FileName' : '%s.mp4' % time.strftime('%y%m%d-%H%M%S', time.localtime()),
                    'Text': download_video, }
            elif m['MsgType'] == 10000:
                msg = {
                    'Type': 'Note',
                    'Text': m['Content'],}
            elif m['MsgType'] == 10002:
                regx = r'\[CDATA\[(.+?)\]\]'
                data = re.search(regx, m['Content'])
                data = 'System message' if data is None else data.group(1).replace('\\', '')
                msg = {
                    'Type': 'Note',
                    'Text': data, }
            elif m['MsgType'] in srl:
                msg = {
                    'Type': 'Useless',
                    'Text': 'UselessMsg', }
            else:
                out.print_line('MsgType Unknown: %s\n%s'%(m['MsgType'], str(m)), False)
                srl.append(m['MsgType'])
                msg = {
                    'Type': 'Useless',
                    'Text': 'UselessMsg', }
            m = dict(m, **msg)
            rl.append(m)
        return rl
    def __produce_group_chat(self, msg):
        r = re.match('(@[0-9a-z]*?):<br/>(.*)$', msg['Content'])
        if not r: return
        actualUserName, content = r.groups()
        chatroom = self.storageClass.search_chatrooms(userName=msg['FromUserName'])
        member = tools.search_dict_list((chatroom or {}).get(
            'MemberList') or [], 'UserName', actualUserName)
        if member is None:
            chatroom = self.update_chatroom(msg['FromUserName'])
            member = tools.search_dict_list((chatroom or {}).get(
                'MemberList') or [], 'UserName', actualUserName)
        msg['ActualUserName'] = actualUserName
        msg['ActualNickName'] = member['DisplayName'] or member['NickName']
        msg['Content']        = content
        tools.msg_formatter(msg, 'Content')
        atFlag = '@' + (chatroom['self']['DisplayName']
            or self.storageClass.nickName)
        msg['isAt'] = (
            (atFlag + (u'\u2005' if u'\u2005' in msg['Content'] else ' '))
            in msg['Content']
            or
            msg['Content'].endswith(atFlag))
    def send_raw_msg(self, msgType, content, toUserName):
        url = '%s/webwxsendmsg'%self.loginInfo['url']
        payloads = {
            'BaseRequest': self.loginInfo['BaseRequest'],
            'Msg': {
                'Type': msgType,
                'Content': content,
                'FromUserName': self.storageClass.userName,
                'ToUserName': (toUserName if toUserName else self.storageClass.userName),
                'LocalID': self.loginInfo['msgid'],
                'ClientMsgId': self.loginInfo['msgid'],
                }, }
        self.loginInfo['msgid'] += 1
        headers = { 'ContentType': 'application/json; charset=UTF-8', 'User-Agent' : config.USER_AGENT }
        r = self.s.post(url, data=json.dumps(payloads, ensure_ascii=False).encode('utf8'), headers=headers)
        return r.json()
    def send_msg(self, msg='Test Message', toUserName=None):
        r = self.send_raw_msg(1, msg, toUserName)
        return r['BaseResponse']['Ret'] == 0
    def __upload_file(self, fileDir, isPicture = False, isVideo = False):
        if not tools.check_file(fileDir): return
        url = self.loginInfo.get('fileUrl', self.loginInfo['url']) + \
            '/webwxuploadmedia?f=json'
        # save it on server
        fileSize = str(os.path.getsize(fileDir))
        cookiesList = {name:data for name,data in self.s.cookies.items()}
        fileType = mimetypes.guess_type(fileDir)[0] or 'application/octet-stream'
        files = {
            'id': (None, 'WU_FILE_0'),
            'name': (None, os.path.basename(fileDir)),
            'type': (None, fileType),
            'lastModifiedDate': (None, time.strftime('%a %b %d %Y %H:%M:%S GMT+0800 (CST)')),
            'size': (None, fileSize),
            'mediatype': (None, 'pic' if isPicture else 'video' if isVideo else'doc'),
            'uploadmediarequest': (None, json.dumps({
                'BaseRequest': self.loginInfo['BaseRequest'],
                'ClientMediaId': int(time.time()),
                'TotalLen': fileSize,
                'StartPos': 0,
                'DataLen': fileSize,
                'MediaType': 4, }, separators = (',', ':'))),
            'webwx_data_ticket': (None, cookiesList['webwx_data_ticket']),
            'pass_ticket': (None, 'undefined'),
            'filename' : (os.path.basename(fileDir), open(fileDir, 'rb'), fileType), }
        headers = { 'User-Agent' : config.USER_AGENT }
        r = self.s.post(url, files = files, headers = headers)
        return json.loads(r.text)['MediaId']
    def send_file(self, fileDir, toUserName=None):
        if toUserName is None: toUserName = self.storageClass.userName
        mediaId = self.__upload_file(fileDir)
        if mediaId is None: return False
        url = '%s/webwxsendappmsg?fun=async&f=json' % self.loginInfo['url']
        data = {
            'BaseRequest': self.loginInfo['BaseRequest'],
            'Msg': {
                'Type': 6,
                'Content': ("<appmsg appid='wxeb7ec651dd0aefa9' sdkver=''><title>%s</title>"%os.path.basename(fileDir) +
                    "<des></des><action></action><type>6</type><content></content><url></url><lowurl></lowurl>" +
                    "<appattach><totallen>%s</totallen><attachid>%s</attachid>"%(str(os.path.getsize(fileDir)), mediaId) +
                    "<fileext>%s</fileext></appattach><extinfo></extinfo></appmsg>"%os.path.splitext(fileDir)[1].replace('.','')),
                'FromUserName': self.storageClass.userName,
                'ToUserName': toUserName,
                'LocalID': self.loginInfo['msgid'],
                'ClientMsgId': self.loginInfo['msgid'], }, }
        self.loginInfo['msgid'] += 1
        headers = {
            'User-Agent': config.USER_AGENT,
            'Content-Type': 'application/json;charset=UTF-8', }
        r = self.s.post(url, data=json.dumps(data, ensure_ascii=False).encode('utf8'), headers=headers)
        return True
    def send_image(self, fileDir, toUserName=None):
        if toUserName is None: toUserName = self.storageClass.userName
        mediaId = self.__upload_file(fileDir, isPicture=not fileDir[-4:] == '.gif')
        if mediaId is None: return False
        url = '%s/webwxsendmsgimg?fun=async&f=json' % self.loginInfo['url']
        data = {
            'BaseRequest': self.loginInfo['BaseRequest'],
            'Msg': {
                'Type': 3,
                'MediaId': mediaId,
                'FromUserName': self.storageClass.userName,
                'ToUserName': toUserName,
                'LocalID': self.loginInfo['msgid'],
                'ClientMsgId': self.loginInfo['msgid'], }, }
        self.loginInfo['msgid'] += 1
        if fileDir[-4:] == '.gif':
            url = '%s/webwxsendemoticon?fun=sys' % self.loginInfo['url']
            data['Msg']['Type'] = 47
            data['Msg']['EmojiFlag'] = 2
        headers = {
            'User-Agent': config.USER_AGENT,
            'Content-Type': 'application/json;charset=UTF-8', }
        r = self.s.post(url, data=json.dumps(data, ensure_ascii=False).encode('utf8'), headers=headers)
        return True
    def send_video(self, fileDir, toUserName = None):
        if toUserName is None: toUserName = self.storageClass.userName
        mediaId = self.__upload_file(fileDir, isVideo=True)
        if mediaId is None: return False
        url = '%s/webwxsendvideomsg?fun=async&f=json&pass_ticket=%s' % (
            self.loginInfo['url'], self.loginInfo['pass_ticket'])
        payloads = {
            'BaseRequest': self.loginInfo['BaseRequest'],
            'Msg': {
                'Type'         : 43,
                'MediaId'      : mediaId,
                'FromUserName' : self.storageClass.userName,
                'ToUserName'   : toUserName,
                'LocalID'      : self.loginInfo['msgid'],
                'ClientMsgId'  : self.loginInfo['msgid'], },
            'Scene': 0, }
        self.loginInfo['msgid'] += 1
        headers = {
            'User-Agent' : config.USER_AGENT,
            'Content-Type': 'application/json;charset=UTF-8', }
        r = self.s.post(url, data=json.dumps(data, ensure_ascii=False).encode('utf8'), headers=headers)
        return True
    def set_alias(self, userName, alias):
        url = '%s/webwxoplog?lang=%s&pass_ticket=%s'%(
            self.loginInfo['url'], 'zh_CN', self.loginInfo['pass_ticket'])
        data = {
            'UserName'    : userName,
            'CmdId'       : 2,
            'RemarkName'  : alias,
            'BaseRequest' : self.loginInfo['BaseRequest'], }
        headers = { 'User-Agent' : config.USER_AGENT }
        j = self.s.post(url, json.dumps(data, ensure_ascii=False).encode('utf8'), headers=headers).json()
        return j['BaseResponse']['Ret'] == 0
    def add_friend(self, userName, status=2, ticket='', userInfo={}):
        ''' Add a friend or accept a friend
            * for adding status should be 2
            * for accepting status should be 3 '''
        url = '%s/webwxverifyuser?r=%s&pass_ticket=%s'%(self.loginInfo['url'], int(time.time()), self.loginInfo['pass_ticket'])
        payloads = {
            'BaseRequest': self.loginInfo['BaseRequest'],
            'Opcode': status, # 3
            'VerifyUserListSize': 1,
            'VerifyUserList': [{
                'Value': userName,
                'VerifyUserTicket': ticket, }], # ''
            'VerifyContent': '',
            'SceneListCount': 1,
            'SceneList': 33, # [33]
            'skey': self.loginInfo['skey'], }
        headers = { 'ContentType': 'application/json; charset=UTF-8', 'User-Agent' : config.USER_AGENT }
        r = self.s.post(url, data = json.dumps(payloads), headers = headers)
        if userInfo: # add user to storage
            self.memberList.append(tools.struct_friend_info(userInfo))
        return r.json()
    def get_head_img(self, userName=None, chatroomUserName=None, picDir=None):
        ''' get head image
         * if you want to get chatroom header: only set chatroomUserName
         * if you want to get friend header: only set userName
         * if you want to get chatroom member header: set both
        '''
        params = {
            'userName': userName or chatroomUserName,
            'skey': self.loginInfo['skey'], }
        url = '%s/webwxgeticon' % self.loginInfo['url']
        if chatroomUserName is None:
            infoDict = self.storageClass.search_friends(userName=userName)
            if infoDict is None: return None
        else:
            if userName is None:
                url = '%s/webwxgetheadimg' % self.loginInfo['url']
            else:
                chatroom = self.storageClass.search_chatrooms(userName=chatroomUserName)
                if chatroomUserName is None: return None
                if chatroom['EncryChatRoomId'] == '':
                    chatroom = self.update_chatroom(chatroomUserName)
                params['chatroomid'] = chatroom['EncryChatRoomId']
        headers = { 'User-Agent' : config.USER_AGENT }
        r = self.s.get(url, params=params, stream=True, headers=headers)
        tempStorage = io.BytesIO()
        for block in r.iter_content(1024):
            tempStorage.write(block)
        if picDir is None: return tempStorage.getvalue()
        with open(picDir, 'wb') as f: f.write(tempStorage.getvalue())
    def create_chatroom(self, memberList, topic = ''):
        url = ('%s/webwxcreatechatroom?pass_ticket=%s&r=%s'%(
                self.loginInfo['url'], self.loginInfo['pass_ticket'], int(time.time())))
        data = {
            'BaseRequest': self.loginInfo['BaseRequest'],
            'MemberCount': len(memberList),
            'MemberList': [{'UserName': member['UserName']} for member in memberList],
            'Topic': topic, }
        headers = {'content-type': 'application/json; charset=UTF-8', 'User-Agent' : config.USER_AGENT }
        r = self.s.post(url, data=json.dumps(data, ensure_ascii=False).encode('utf8', 'ignore'),headers=headers)
        return r.json()
    def set_chatroom_name(self, chatroomUserName, name):
        url = ('%s/webwxupdatechatroom?fun=modtopic&pass_ticket=%s'%(
            self.loginInfo['url'], self.loginInfo['pass_ticket']))
        data = {
            'BaseRequest': self.loginInfo['BaseRequest'],
            'ChatRoomName': chatroomUserName,
            'NewTopic': name, }
        headers = {'content-type': 'application/json; charset=UTF-8', 'User-Agent' : config.USER_AGENT}
        return self.s.post(url, data=json.dumps(data, ensure_ascii=False).encode('utf8', 'ignore'), headers=headers).json()
    def delete_member_from_chatroom(self, chatroomUserName, memberList):
        url = ('%s/webwxupdatechatroom?fun=delmember&pass_ticket=%s'%(
            self.loginInfo['url'], self.loginInfo['pass_ticket']))
        params = {
            'BaseRequest': self.loginInfo['BaseRequest'],
            'ChatRoomName': chatroomUserName,
            'DelMemberList': ','.join([member['UserName'] for member in memberList]), }
        headers = {'content-type': 'application/json; charset=UTF-8', 'User-Agent' : config.USER_AGENT}
        return self.s.post(url, data=json.dumps(params),headers=headers).json()
    def add_member_into_chatroom(self, chatroomUserName, memberList,
            useInvitation=False):
        ''' add or invite member into chatroom
         * there are two ways to get members into chatroom: invite or directly add
         * but for chatrooms with more than 40 users, you can only use invite
         * but don't worry we will auto-force userInvitation for you when necessary
        '''
        if not useInvitation:
            chatroom = self.storageClass.search_chatrooms(userName=chatroomUserName)
            if not chatroom: chatroom = self.update_chatroom(chatroomUserName)
            if len(chatroom['MemberList']) > self.loginInfo['InviteStartCount']: useInvitation = True
        if useInvitation:
            fun, memberKeyName = 'invitemember', 'InviteMemberList'
        else:
            fun, memberKeyName = 'addmember', 'AddMsgList'
        url = ('%s/webwxupdatechatroom?fun=%s&pass_ticket=%s'%(
            self.loginInfo['url'], fun, self.loginInfo['pass_ticket']))
        params = {
            'BaseRequest'  : self.loginInfo['BaseRequest'],
            'ChatRoomName' : chatroomUserName,
            memberKeyName  : ','.join([member['UserName'] for member in memberList]), }
        headers = {'content-type': 'application/json; charset=UTF-8', 'User-Agent' : config.USER_AGENT}
        return self.s.post(url, data=json.dumps(params),headers=headers).json()

if __name__ == '__main__':
    wcc = WeChatClient()
    wcc.login()
