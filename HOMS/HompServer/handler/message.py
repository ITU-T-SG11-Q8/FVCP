# 
# The MIT License
# 
# Copyright (c) 2022 ETRI
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
# 

from datetime import datetime, timedelta
import uuid


class HompOverlay:
    CREATION = 11
    MODIFICATION = 12
    REMOVAL = 13
    AUTH = 14
    BASE = 15

    def __init__(self, data):
        self.overlay_id = None
        self.title = None
        self.type = None
        self.sub_type = None
        self.owner_id = None
        #self.expires = None
        self.status = 'active'
        self.description = None
        self.heartbeat_interval = None
        self.heartbeat_timeout = None
        self.auth = HompOverlayAuth()
        self.cr_policy = HompOverlayCrPolicy()
        self.has_cr_policy = False

        self.service = HompService()

        self.set_data(data)

    def to_json(self, types):
        if types == self.CREATION:
            result = {
                'overlay-id': self.overlay_id,
                'type': self.type,
                'sub-type': self.sub_type,
                'owner-id': self.owner_id,
                'heartbeat-interval': self.heartbeat_interval,
                'heartbeat-timeout': self.heartbeat_timeout,
                'auth': self.auth.to_json(),
                'service-info': self.service.to_json()
            }

            if self.has_cr_policy:
                result['cr-policy'] = self.cr_policy.to_json()

            return {'overlay': result}

        elif types == self.MODIFICATION:
            result = {
                'overlay-id': self.overlay_id,
                'title': self.title,
                'owner-id': self.owner_id,
                #'expires': self.expires,
                'description': self.description
            }

            if self.auth.access_key is not None or self.auth.peer_list is not None:
                auth = {}
                if self.auth.access_key is not None:
                    auth['access_key'] = self.auth.access_key
                if self.auth.peer_list is not None:
                    auth['peerlist'] = self.auth.peer_list
                result['auth'] = auth
            
            if self.title is None:
                del result['title']
            #if self.expires is None:
            #    del result['expires']
            if self.description is None:
                del result['description']

            if self.service is not None:
                result_service = {}
                if self.service.start_datetime is not None:
                    result_service['start-datetime'] = self.service.start_datetime
                if self.service.end_datetime is not None:
                    result_service['end-datetime'] = self.service.end_datetime
                if self.service.title is not None:
                    result_service['title'] = self.service.title
                if self.service.description is not None:
                    result_service['description'] = self.service.description
                if self.service.source_list is not None:
                    result_service['source-list'] = self.service.source_list
                if self.service.block_list is not None:
                    result_service['block-list'] = self.service.block_list
                if self.service.channel_list is not None:
                    result_channel_list = []
                    for channel in self.service.channel_list:
                        result_channel_list.append({
                            'channel-id': channel.channel_id,
                            'source-list': channel.source_list,
                        })
                    result_service['channel-list'] = result_channel_list
                result['service-info'] = result_service

            return {'overlay': result}

        elif types == self.REMOVAL:
            return {'overlay': {'overlay-id': self.overlay_id}}

    def set_data(self, data):
        self.overlay_id = data.get('overlay-id') if 'overlay-id' in data else str(uuid.uuid4())
        self.title = data.get('title')
        self.type = data.get('type')
        self.sub_type = data.get('sub-type')
        self.owner_id = data.get('owner-id')
        #self.expires = data.get('expires') if 'expires' in data else 0
        self.description = data.get('description')
        self.heartbeat_interval = data.get('heartbeat-interval')
        self.heartbeat_timeout = data.get('heartbeat-timeout')
        self.set_auth(data.get('auth'))
        if 'cr-policy' in data:
            self.set_cr_policy(data.get('cr-policy'))

        self.set_service(data.get('service-info'))
        

    def is_valid(self, types):
        if types == self.CREATION:
            return self.valid_overlay() and self.valid_auth() and self.valid_cr_policy() and self.valid_service_info()
        elif types == self.BASE:
            return self.valid_base()
        elif types == self.AUTH:
            return self.valid_auth_key_or_peer()

    def valid_base(self):
        return self.overlay_id is not None and self.owner_id is not None and self.auth.admin_key is not None

    def valid_overlay(self):
        return self.title is not None and self.type is not None and self.sub_type is not None and \
               self.owner_id is not None and self.heartbeat_interval is not None and \
               self.heartbeat_timeout is not None and self.type == 'core' and self.sub_type == 'tree'

    def valid_auth(self):
        valid = self.auth.type is not None and (self.auth.type == 'closed' or self.auth.type == 'open') and \
                self.auth.admin_key is not None
        if valid and self.auth.type == 'closed':
            valid = self.valid_auth_key_or_peer()
        return valid

    def valid_auth_key_or_peer(self):
        return self.auth.access_key is not None or \
               (self.auth.peer_list is not None)

    def valid_cr_policy(self):
        if not self.has_cr_policy:
            return True
        return self.cr_policy.recovery_by == 'push' or self.cr_policy.recovery_by == 'pull'
    
    def valid_service_info(self):
        nowdate = datetime.now()
        if self.service.start_datetime is None or len(self.service.start_datetime) <= 0:
            self.service.start_datetime = nowdate.strftime('%Y%m%d%H%M%S')
        
        if self.service.end_datetime is None or len(self.service.end_datetime) <= 0:
            startdate = datetime.strptime(str(self.service.start_datetime), '%Y%m%d%H%M%S')
            enddate = startdate + timedelta(days=1)
            self.service.end_datetime = datetime.strftime(enddate, '%Y%m%d%H%M%S')

        if self.service.channel_list is None or len(self.service.channel_list) <= 0:
            return False
        for channel in self.service.channel_list:
            if channel.channel_type != 'control' and channel.channel_type != 'video/feature' and \
               channel.channel_type != 'audio' and channel.channel_type != 'text':
                return False
            
            if channel.channel_id is None or len(channel.channel_id) <= 0:
                return False

            if channel.channel_type != 'control':
                if channel.channel_attribute is None:
                    return False

        return True

    def set_auth(self, data):
        self.auth.keyword = data.get('keyword')
        self.auth.type = data.get('type')
        self.auth.admin_key = data.get('admin_key')

        if 'access_key' in data:
            self.auth.access_key = data.get('access_key')
        elif 'peerlist' in data:
            self.auth.peer_list = data.get('peerlist')
            self.auth.has_peer_list = len(self.auth.peer_list) > 0

    def set_cr_policy(self, data):
        self.has_cr_policy = True
        self.cr_policy.mN_Cache = data.get('mN_Cache')  # 데이터의 유지량, circular queue 의 크기는 이값보다 크게, 0이면 복구X
        self.cr_policy.mD_Cache = data.get('mD_Cache')  # 데이터의 최소 유지 시간
        self.cr_policy.recovery_by = data.get('recovery-by')  # push & pull

    def set_service(self, data):
        if data is None:
            return
        
        #self.service.service_id = data.get('overlay-id') if 'overlay-id' in data else str(uuid.uuid4())
        self.service.start_datetime = data.get('start-datetime') if 'start-datetime' in data else None
        self.service.end_datetime = data.get('end-datetime') if 'end-datetime' in data else None
        self.service.title = data.get('title') if 'title' in data else None
        self.service.description = data.get('description') if 'description' in data else None
        self.service.source_list = data.get('source-list') if 'source-list' in data else None
        self.service.block_list = data.get('block-list') if 'block-list' in data else None
        self.service.channel_list = []
        if 'channel-list' in data:
            chlist = data.get('channel-list')
            if chlist is not None:
                for channel in data.get('channel-list'):
                    self.service.channel_list.append(HompChannel(channel))


class HompOverlayAuth:
    def __init__(self):
        self.keyword = None
        self.type = None
        self.admin_key = None
        self.access_key = None
        self.peer_list = None
        self.has_peer_list = False

    def to_json(self):
        result = {
            'type': self.type,
            'admin_key': self.admin_key
        }

        if self.keyword is not None:
            result['keyword'] = self.keyword

        if self.access_key is not None:
            result['access_key'] = self.access_key
        elif self.has_peer_list:
            result['peerlist'] = self.peer_list

        return result

class HompOverlayOwnership:
    def __init__(self, data):
        self.owner_id = None
        self.admin_key = None
        self.set_data(data)

    def set_data(self, data):
        self.owner_id = data.get('owner-id')
        self.admin_key = data.get('admin-key')

    def is_valid(self):
        return self.owner_id is not None or self.admin_key is not None

class HompOverlayCrPolicy:
    def __init__(self):
        self.mN_Cache = None
        self.mD_Cache = None
        self.recovery_by = None

    def to_json(self):
        return {
            'mN_Cache': self.mN_Cache,
            'mD_Cache': self.mD_Cache,
            'recovery-by': self.recovery_by
        }

class HompOverlayPeer:
    JOIN = 11
    REFRESH = 12
    REPORT = 13
    LEAVE = 14
    BASE = 15

    def __init__(self, data):
        self.overlay_id = None
        self.type = None
        self.sub_type = None
        self.expires = None
        self.auth = HompOverlayAuth()
        self.recovery = None
        self.ticket_id = None
        self.peer = HompPeer()
        self.status_code = None
        self.heartbeat_interval = None
        self.heartbeat_timeout = None
        self.cr_policy = HompOverlayCrPolicy()
        self.status = HompPeerStatus()
        self.has_cr_policy = False
        self.has_status = False
        self.service = HompService()

        self.set_data(data)

    def set_data(self, data):
        overlay_data = data.get('overlay')
        self.overlay_id = overlay_data.get('overlay-id')
        self.type = overlay_data.get('type')
        self.sub_type = overlay_data.get('sub-type')
        if 'auth' in overlay_data and 'access_key' in overlay_data.get('auth'):
            self.auth.access_key = overlay_data.get('auth').get('access_key')

        #self.recovery = overlay_data.get('recovery') if 'recovery' in overlay_data else False
        

        if 'peer' in data:
            peer_data = data.get('peer')
            self.peer.peer_id = peer_data.get('peer-id')
            self.peer.address = peer_data.get('address')
            if 'display-name' in peer_data:
                self.peer.display_name = peer_data.get('display-name')
            if 'auth' in peer_data:
                if 'password' in peer_data.get('auth'):
                    self.peer.auth.password = peer_data.get('auth').get('password')
                if 'public-key' in peer_data.get('auth'):
                    self.peer.auth.public_key = peer_data.get('auth').get('public-key')
            self.status_code = 202 if self.sub_type == 'tree' else 200
            self.expires = peer_data.get('expires')
            self.ticket_id = peer_data.get('ticket-id')

            if 'status' in data:
                self.has_status = True
                peer_status_data = data.get('status')
                self.status.num_primary = peer_status_data.get('num_primary')
                self.status.num_out_candidate = peer_status_data.get('num_out_candidate')
                self.status.num_in_candidate = peer_status_data.get('num_in_candidate')
                self.status.costmap = peer_status_data.get('costmap')

            # app_data 사용안함.
            # self.app_data = data.get('app') if 'app' in data else []
            # self.has_app_data = len(self.app_data) > 0
        else:
            self.peer.peer_id = overlay_data.get('peer-id')
            if 'auth' in overlay_data and 'password' in overlay_data.get('auth'):
                self.peer.auth.password = overlay_data.get('auth').get('password')
            if 'status' in overlay_data:
                self.has_status = True
                peer_status_data = overlay_data.get('status')
                self.status.num_primary = peer_status_data.get('num_primary')
                self.status.num_out_candidate = peer_status_data.get('num_out_candidate')
                self.status.num_in_candidate = peer_status_data.get('num_in_candidate')
                self.status.costmap = peer_status_data.get('costmap')

    def set_overlay_data(self, data):
        self.heartbeat_interval = data.get('heartbeat_interval')
        self.heartbeat_timeout = data.get('heartbeat_timeout')

        self.cr_policy.mN_Cache = data.get('mn_cache')
        self.cr_policy.mD_Cache = data.get('md_cache')
        self.cr_policy.recovery_by = data.get('recovery_by')
        self.has_cr_policy = self.cr_policy.recovery_by is not None

    def set_service(self, data):
        if data is None:
            return
        
        #self.service.service_id = data.get('overlay-id') if 'overlay-id' in data else str(uuid.uuid4())
        self.service.start_datetime = data.get('start-datetime') if 'start-datetime' in data else None
        self.service.end_datetime = data.get('end-datetime') if 'end-datetime' in data else None
        self.service.title = data.get('title') if 'title' in data else None
        self.service.description = data.get('description') if 'description' in data else None
        self.service.source_list = data.get('source-list') if 'source-list' in data else None
        self.service.block_list = data.get('block-list') if 'block-list' in data else None
        self.service.channel_list = []
        for channel in data.get('channel-list'):
            self.service.channel_list.append(HompChannel(channel))

    def valid_base(self):
        return self.overlay_id is not None and self.peer.peer_id is not None and \
               self.peer.address is not None and self.peer.auth.password is not None

    def valid_status(self):
        return self.has_status and self.status.num_primary is not None and \
               self.status.num_out_candidate is not None and self.status.num_in_candidate is not None and \
               self.status.costmap is not None

    def is_valid(self, types):
        if types == HompOverlayPeer.JOIN:
            return self.valid_base() and self.type is not None and self.sub_type is not None
        elif types == HompOverlayPeer.REFRESH:
            return self.valid_base()
        elif types == HompOverlayPeer.REPORT:
            return self.overlay_id is not None and self.valid_status()
        elif types == HompOverlayPeer.LEAVE:
            return self.overlay_id is not None and self.peer.peer_id is not None and \
                   self.peer.auth.password is not None

    def to_json(self, types, peer_info_list=None):
        if types == self.BASE:
            return {'overlay': {'overlay-id': self.overlay_id}}
        elif types == self.JOIN:
            result_overlay = {
                'overlay-id': self.overlay_id,
                'type': self.type,
                'sub-type': self.sub_type,
                'status': {
                    'num_peers': len(peer_info_list),
                    'peer_info_list': peer_info_list,
                    'status': 'active'
                },
                'heartbeat-interval': self.heartbeat_interval,
                'heartbeat-timeout': self.heartbeat_timeout,
                'service-info': self.service.to_json()
            }

            if self.status_code == 200:
                del result_overlay['heartbeat-interval']
                del result_overlay['heartbeat-timeout']
                del result_overlay['ticket-id']

            if self.has_cr_policy and self.status_code == 202:
                result_overlay['cr-policy'] = self.cr_policy.to_json()
            
            result_peer = {
                'peer-id': self.peer.peer_id,
                'ticket-id': self.ticket_id,
                'expires': self.expires,
                'display-name': self.peer.display_name,
            }

            result = {'overlay': result_overlay, 'peer': result_peer}
            # if self.has_app_data:
            #     result['app'] = self.app_data
            return result
        elif types == self.REFRESH:
            result = {
                'overlay': {
                    'overlay-id': self.overlay_id
                },
                'peer': {
                    'peer-id': self.peer.peer_id,
                    'expires': self.expires
                    # 'address': self.peer.address,
                    # 'auth': {
                    #     'password': self.peer.auth.password
                    # }
                }
            }
            # if self.has_app_data:
            #     result['app'] = self.app_data
            return result


class HompPeerAuth:
    def __init__(self):
        self.password = None
        self.public_key = None


class HompPeer:
    def __init__(self):
        self.peer_id = None
        self.address = None
        self.auth = HompPeerAuth()
        self.display_name = None



class HompPeerStatus:
    def __init__(self):
        self.num_primary = None
        self.num_out_candidate = None
        self.num_in_candidate = None
        self.costmap = None

class HompService:
    def __init__(self) -> None:
        self.service_id = None
        self.start_datetime = None
        self.end_datetime = None
        self.title = None
        self.description = None
        self.source_list = None
        self.block_list = None
        self.channel_list = None

    def to_json(self):
        result = {
            'start-datetime': self.start_datetime,
            'end-datetime': self.end_datetime,
        }

        if self.title is not None:
            result['title'] = self.title
        if self.description is not None:
            result['description'] = self.description
        if self.source_list is not None:
            result['source-list'] = self.source_list
        else:
            result['source-list'] = []
        if self.block_list is not None:
            result['block-list'] = self.block_list
        else:
            result['block-list'] = []

        channels = []
        for channel in self.channel_list:
            channels.append(channel.to_json())
        result['channel-list'] = channels

        return result

class HompChannel:
    def __init__(self, data) -> None:
        self.channel_id = data.get('channel-id') if 'channel-id' in data else str(uuid.uuid4())
        self.channel_type = data.get('channel-type')
        self.channel_attribute = data.get('channel-attribute')
        self.source_list = data.get('source-list')

    def to_json(self):
        result = {
            'channel-id': self.channel_id,
            'channel-type': self.channel_type,
            'channel-attribute': self.channel_attribute,
        }

        if self.source_list is not None:
            result['source-list'] = self.source_list

        return result