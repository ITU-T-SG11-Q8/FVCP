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

from flask import request
from flask_restful import Resource

from config import WEB_SOCKET_CONFIG, LOG_CONFIG
from classes.overlay import Overlay
from handler.message import HompOverlay, HompOverlayOwnership
from data.factory import Factory
from database.db_connector import DBConnector
import database.db_query as query


class HybridOverlay(Resource):
    def post(self):
        if LOG_CONFIG['PRINT_PROTOCOL_LOG']:
            print('[SERVER] {0} / {1}'.format(self.methods, self.endpoint))

        db_connector = DBConnector()
        try:
            request_data = request.get_json()
            print(request_data)
            request_overlay = HompOverlay(request_data.get('overlay'))

            if not request_overlay.is_valid(HompOverlay.CREATION):
                raise ValueError

            overlay_parameters = (
                request_overlay.overlay_id, request_overlay.title, request_overlay.type, request_overlay.sub_type,
                request_overlay.owner_id, request_overlay.status, request_overlay.description,
                request_overlay.heartbeat_interval, request_overlay.heartbeat_timeout, request_overlay.auth.keyword,
                request_overlay.auth.type, request_overlay.auth.admin_key, request_overlay.auth.access_key,
                request_overlay.cr_policy.mN_Cache, request_overlay.cr_policy.mD_Cache,
                request_overlay.cr_policy.recovery_by)
            db_connector.insert(query.INSERT_HP2P_OVERLAY, overlay_parameters)

            service_info_parameters = (request_overlay.overlay_id, request_overlay.service.start_datetime,
                                        request_overlay.service.end_datetime, request_overlay.service.title, request_overlay.service.description)
            request_overlay.service.service_id = db_connector.insert_get_id(query.INSERT_HP2P_SERVICE, service_info_parameters)

            if request_overlay.auth.has_peer_list:
                auth_peer_parameters = []
                for peer_id in request_overlay.auth.peer_list:
                    auth_peer_parameters.append((request_overlay.overlay_id, peer_id))
                db_connector.insert_all(query.INSERT_HP2P_AUTH_PEER, auth_peer_parameters)

            if request_overlay.service.source_list is not None and len( request_overlay.service.source_list ) > 0:
                source_info_parameters = []
                for source in request_overlay.service.source_list:
                    source_info_parameters.append((request_overlay.service.service_id, source))
                db_connector.insert_all(query.INSERT_HP2P_SERVICE_SOURCE, source_info_parameters)
            else:
                source_info_parameters = []
                source_info_parameters.append((request_overlay.service.service_id, '-'))
                db_connector.insert_all(query.INSERT_HP2P_SERVICE_SOURCE, source_info_parameters)
            
            if request_overlay.service.block_list is not None and len( request_overlay.service.block_list ) > 0:
                block_info_parameters = []
                for block in request_overlay.service.block_list:
                    block_info_parameters.append((request_overlay.service.service_id, block))
                db_connector.insert_all(query.INSERT_HP2P_SERVICE_BLOCK, block_info_parameters)
            
            if request_overlay.service.channel_list is not None and len( request_overlay.service.channel_list ) > 0:
                for channel in request_overlay.service.channel_list:
                    channel_info_parameters = (channel.channel_id, request_overlay.service.service_id, channel.channel_type)
                    db_connector.insert(query.INSERT_HP2P_CHANNEL, channel_info_parameters)

                    if channel.channel_type != 'control':
                        if channel.source_list is not None and len( channel.source_list ) > 0:
                            channel_source_parameters = []
                            for source in channel.source_list:
                                channel_source_parameters.append((channel.channel_id, request_overlay.service.service_id, source))
                            db_connector.insert_all(query.INSERT_HP2P_CHANNEL_SOURCE, channel_source_parameters)
                        elif channel.source_list is not None:
                            channel_source_parameters = []
                            channel_source_parameters.append((channel.channel_id, request_overlay.service.service_id, '-'))
                            db_connector.insert_all(query.INSERT_HP2P_CHANNEL_SOURCE, channel_source_parameters)

                        attr_parameters = []
                        for keyword, value in channel.channel_attribute.items():
                            attr_parameters.append((channel.channel_id, request_overlay.service.service_id, keyword, value))
                        db_connector.insert_all(query.INSERT_HP2P_CHANNEL_ATTRIBUTE, attr_parameters)

            overlay = Overlay()
            overlay.overlay_id = request_overlay.overlay_id
            overlay.heartbeat_interval = request_overlay.heartbeat_interval
            overlay.heartbeat_timeout = request_overlay.heartbeat_timeout
            overlay.start_datetime = request_overlay.service.start_datetime
            overlay.end_datetime = request_overlay.service.end_datetime

            Factory.get().add_overlay(overlay.overlay_id, overlay)
            Factory.get().get_web_socket_manager().send_create_overlay_message(request_overlay.overlay_id)
            Factory.get().get_web_socket_manager().send_log_message(request_overlay.overlay_id,
                                                                    request_overlay.owner_id,
                                                                    'Overlay Creation.')

            db_connector.commit()
            return request_overlay.to_json(HompOverlay.CREATION), 200
        except ValueError:
            db_connector.rollback()
            return 'BAD REQUEST', 400
        except Exception as exception:
            db_connector.rollback()
            return str(exception), 500

    def get(self):
        if LOG_CONFIG['PRINT_PROTOCOL_LOG']:
            print('[SERVER] {0} / {1}'.format(self.methods, self.endpoint))
        db_connector = DBConnector()
        try:
            result = {"overlay": []}
            where = ''
            parameters = None

            if len(request.args) > 0:
                if 'overlay-id' in request.args:
                    where = query.WHERE_OVERLAY_ID
                    parameters = request.args.get('overlay-id')
                elif 'title' in request.args:
                    where = query.WHERE_TITLE
                    parameters = ('%%%s%%' % request.args.get('title'))
                elif 'description' in request.args:
                    where = query.WHERE_DESCRIPTION
                    parameters = ('%%%s%%' % request.args.get('description'))

            select_overlay_list = db_connector.select(query.SELECT_HP2P_OVERLAY + where + query.ORDER_BY_CREATED_AT,
                                                      (parameters,) if parameters is not None else None)

            if len(select_overlay_list) > 0:
                for select_overlay in select_overlay_list:
                    overlay_id = select_overlay.get('overlay_id')

                    select_num_peers = db_connector.select_one(query.SELECT_NUM_PEERS, (overlay_id,))
                    num_peers = select_num_peers.get('num_peers') if select_num_peers is not None else 0

                    overlay = {
                        'overlay-id': overlay_id,
                        'title': select_overlay.get('title'),
                        'type': select_overlay.get('overlay_type'),
                        'sub-type': select_overlay.get('sub_type'),
                        'owner-id': select_overlay.get('owner_id'),
                        #'expires': select_overlay.get('expires'),
                        'status': {
                            'num_peers': num_peers,
                            'status': select_overlay.get('overlay_status')
                        },
                        'description': select_overlay.get('description'),
                        'auth': {
                            'type': select_overlay.get('auth_type')
                        }
                    }

                    if select_overlay.get('recovery_by') is not None:
                        overlay['cr-policy'] = {
                            'mN_Cache': select_overlay.get('mn_cache'),
                            'mD_Cache': select_overlay.get('md_cache'),
                            'recovery-by': select_overlay.get('recovery_by')
                        }
                    
                    service_info = query.get_service_info(db_connector, overlay_id)
                    if service_info is not None:
                        overlay['service-info'] = service_info
                    # select_service = db_connector.select_one(query.SELECT_HP2P_SERVICE_BY_OVERLAY_ID, (overlay_id,))
                    # if select_service is not None:
                    #     overlay['service-info'] = {
                    #         'start-datetime': datetime.strftime(select_service.get('start_datetime'), '%Y%m%d%H%M%S'),
                    #         'end-datetime': datetime.strftime(select_service.get('end_datetime'), '%Y%m%d%H%M%S'),
                    #         'title': select_service.get('title'),
                    #         'description': select_service.get('description')
                    #     }
                        
                    #     service_id = select_service.get('service_id')

                    #     select_channel_list = db_connector.select(query.SELECT_HP2P_CHANNEL_BY_SERVICE_ID, (service_id,))
                    #     if len(select_channel_list) > 0:
                    #         overlay['service-info']['channel-list'] = []
                    #         for select_channel in select_channel_list:
                    #             channel_id = select_channel.get('channel_id')
                    #             channel_type = select_channel.get('channel_type')

                    #             channel = {
                    #                 'channel-id': channel_id,
                    #                 'channel-type': channel_type
                    #             }

                    #             select_channel_attribute_list = db_connector.select(query.SELECT_HP2P_CHANNEL_ATTRIBUTE_BY_CHANNEL_ID_AND_SERVICE_ID, (channel_id, service_id))
                    #             if len(select_channel_attribute_list) > 0:
                    #                 channel_attribute = {}
                    #                 for select_channel_attribute in select_channel_attribute_list:
                    #                     channel_attribute[select_channel_attribute.get('keyword')] = select_channel_attribute.get('value')
                    #                 channel['channel-attribute'] = channel_attribute
                                
                    #             overlay['service-info']['channel-list'].append(channel)
                        

                    result["overlay"].append(overlay)

            return result, 200
        except Exception as exception:
            db_connector.rollback()
            return str(exception), 500
    
    def originId(self, id):
        rsltid = None

        if id is not None and id != '':
            rsltid = id.strip()

            if ';' in rsltid:
                rsltid = id.split(';')[0]
            else:
                rsltid = id
        
        return rsltid

    def checkOwnerId(self, ownerid, reqownerid):
        originreq = self.originId(reqownerid)
        originid = self.originId(ownerid)

        if originid is not None and originid != '' and originreq is not None and originreq != '':
            if ownerid != reqownerid:
                return False
        else:
            return False
        
        return True

    def put(self):
        if LOG_CONFIG['PRINT_PROTOCOL_LOG']:
            print('[SERVER] {0} / {1}'.format(self.methods, self.endpoint))
        db_connector = DBConnector()
        try:
            # RspCode_Success      = 200
            # RspCode_WrongRequest = 400
            # RspCode_JoinFailed   = 401
            # RspCode_AuthFailed   = 403
            # RspCode_NotFound     = 404
            # RspCode_Failed       = 500
            request_data = request.get_json()
            request_overlay = HompOverlay(request_data.get('overlay')) 

            if not request_overlay.is_valid(HompOverlay.BASE):
                raise ValueError

            select_overlay = db_connector.select_one(query.SELECT_HP2P_OVERLAY_BY_OVERLAY_ID, (
                request_overlay.overlay_id,))

            if select_overlay is None:
                return request_overlay.to_json(HompOverlay.MODIFICATION), 404

            if self.checkOwnerId(select_overlay.get('owner_id'), request_overlay.owner_id) is False:
                return request_overlay.to_json(HompOverlay.MODIFICATION), 403
            
            if select_overlay.get('auth_admin_key') != request_overlay.auth.admin_key:
                return request_overlay.to_json(HompOverlay.MODIFICATION), 403

            ownership = request_data.get('ownership')
            request_ownership = None

            if ownership is not None:
                request_ownership = HompOverlayOwnership(ownership)
                if not request_ownership.is_valid():
                    raise ValueError

            set_query = ''
            parameters = []
            if request_overlay.title is not None:
                set_query += query.SET_TITLE
                parameters.append(request_overlay.title)
            #if request_overlay.expires is not None:
            #    set_query += query.SET_EXPIRES
            #    parameters.append(request_overlay.expires)
            if request_overlay.description is not None:
                set_query += query.SET_DESCRIPTION
                parameters.append(request_overlay.description)
            if request_ownership is not None:
                if request_ownership.owner_id is not None:
                    set_query += query.SET_OWNER_ID
                    parameters.append(request_ownership.owner_id)
                    request_overlay.owner_id = request_ownership.owner_id
                if request_ownership.admin_key is not None:
                    set_query += query.SET_ADMIN_KEY
                    parameters.append(request_ownership.admin_key)
                    request_overlay.auth.admin_key = request_ownership.admin_key

            parameters.append(request_overlay.overlay_id)
            update_query = query.UPDATE_HP2P_OVERLAY + set_query + query.WHERE_OVERLAY_ID
            db_connector.update(update_query, parameters)

            auth_peer_list_parameters = []
            if request_overlay.is_valid(HompOverlay.AUTH):
                if request_overlay.auth.access_key is not None:
                    db_connector.update(query.UPDATE_HP2P_OVERLAY_SET_ACCESS_KEY,
                        (request_overlay.auth.access_key, request_overlay.overlay_id))
                
                if request_overlay.auth.peer_list is not None:
                    db_connector.delete(query.DELETE_HP2P_AUTH_PEER_BY_OVERLAY_ID, (request_overlay.overlay_id,))
                    if len( request_overlay.auth.peer_list ) > 0:
                        for peer_id in request_overlay.auth.peer_list:
                            auth_peer_list_parameters.append((request_overlay.overlay_id, peer_id))
                        db_connector.insert_all(query.INSERT_HP2P_AUTH_PEER, auth_peer_list_parameters)
                db_connector.update(query.UPDATE_HP2P_OVERLAY_AUTH_CLOSED_BY_OVERLAY_ID, (request_overlay.overlay_id,))
                if ((request_overlay.auth.access_key is not None and request_overlay.auth.access_key == '') or \
                    (request_overlay.auth.peer_list is not None and len(request_overlay.auth.peer_list) <= 0)) and \
                    select_overlay.get('auth_type') == 'closed':
                    db_connector.update(query.UPDATE_HP2P_OVERLAY_AUTH_OPEN_BY_OVERLAY_ID, (request_overlay.overlay_id,))

            block_info_parameters = []
            if request_overlay.service:
                select_service = db_connector.select_one(query.SELECT_HP2P_SERVICE_BY_OVERLAY_ID, (
                    request_overlay.overlay_id))
                
                if select_service is None:
                    db_connector.rollback()
                    return request_overlay.to_json(HompOverlay.MODIFICATION), 404
                
                set_query = ''
                parameters = []
                if request_overlay.service.title is not None:
                    set_query += query.SET_TITLE
                    parameters.append(request_overlay.service.title)
                if request_overlay.service.description is not None:
                    set_query += query.SET_DESCRIPTION
                    parameters.append(request_overlay.service.description)
                if request_overlay.service.start_datetime is not None:
                    set_query += query.SET_START_DATETIME
                    parameters.append(request_overlay.service.start_datetime)
                if request_overlay.service.end_datetime is not None:
                    set_query += query.SET_END_DATETIME
                    parameters.append(request_overlay.service.end_datetime)
                
                parameters.append(select_service.get("service_id"))
                update_query = query.UPDATE_HP2P_SERVICE + set_query + query.WHERE_SERVICE_ID
                db_connector.update(update_query, parameters)

                if request_overlay.service.source_list is not None:
                    db_connector.delete(query.DELETE_HP2P_SERVICE_SOURCE_BY_SERVICE_ID, (select_service.get("service_id"),))
                    if len( request_overlay.service.source_list ) > 0:
                        source_info_parameters = []
                        for source in request_overlay.service.source_list:
                            source_info_parameters.append((select_service.get("service_id"), source))
                        db_connector.insert_all(query.INSERT_HP2P_SERVICE_SOURCE, source_info_parameters)
                    else:
                        source_info_parameters = []
                        source_info_parameters.append((select_service.get("service_id"), '-'))
                        db_connector.insert_all(query.INSERT_HP2P_SERVICE_SOURCE, source_info_parameters)

                if request_overlay.service.block_list is not None:
                    db_connector.delete(query.DELETE_HP2P_SERVICE_BLOCK_BY_SERVICE_ID, (select_service.get("service_id"),))
                    if len( request_overlay.service.block_list ) > 0:
                        for block in request_overlay.service.block_list:
                            block_info_parameters.append((select_service.get("service_id"), block))
                        db_connector.insert_all(query.INSERT_HP2P_SERVICE_BLOCK, block_info_parameters)

                if request_overlay.service.channel_list is not None:
                    
                    for channel in request_overlay.service.channel_list:
                        if channel.channel_id is None or channel.channel_id == '':
                            db_connector.rollback()
                            return request_overlay.to_json(HompOverlay.MODIFICATION), 400
                        
                        db_connector.delete(query.DELETE_HP2P_CHANNEL_SOURCE_BY_SERVICE_ID_AND_CHANNEL_ID, (select_service.get("service_id"), channel.channel_id))
                        if channel.source_list is not None and len( channel.source_list ) > 0:
                            source_info_parameters = []
                            for source in channel.source_list:
                                source_info_parameters.append((channel.channel_id, select_service.get("service_id"), source))
                            db_connector.insert_all(query.INSERT_HP2P_CHANNEL_SOURCE, source_info_parameters)
                        elif channel.source_list is not None:
                            source_info_parameters = []
                            source_info_parameters.append((channel.channel_id, select_service.get("service_id"), '-'))
                            db_connector.insert_all(query.INSERT_HP2P_CHANNEL_SOURCE, source_info_parameters)

            overlay: Overlay = Factory.get().get_overlay(request_overlay.overlay_id)
            if overlay is not None:
                if request_overlay.service is not None:
                    if request_overlay.service.start_datetime is not None:
                        overlay.start_datetime = request_overlay.service.start_datetime
                    if request_overlay.service.end_datetime is not None:
                        overlay.end_datetime = request_overlay.service.end_datetime

            #if request_overlay.expires is not None:
            #    overlay.expires = request_overlay.expires

            #if overlay.expires > 0:
            #    overlay.update_time = datetime.now()

            Factory.get().get_web_socket_manager().send_log_message(request_overlay.overlay_id,
                                                                    request_overlay.owner_id, 'Overlay Modification.')
            db_connector.commit()

            if block_info_parameters is not None and len(block_info_parameters) > 0:
                for block in block_info_parameters:
                    db_connector.delete(query.DELETE_HP2P_PEER_LIKE, (block[1] + ';%', request_overlay.overlay_id))

            if auth_peer_list_parameters is not None and len(auth_peer_list_parameters) > 0:
                plist = ''
                for peer in auth_peer_list_parameters:
                    if plist != '':
                        plist += '|'
                    plist += peer[1] + '.*'

                db_connector.delete(query.DELETE_HP2P_PEER_NOT_REGEXP, (request_overlay.overlay_id, plist))

            db_connector.commit()

            return request_overlay.to_json(HompOverlay.MODIFICATION), 200
        except ValueError:
            db_connector.rollback()
            return 'BAD REQUEST', 400
        except Exception as exception:
            db_connector.rollback()
            return str(exception), 500

    def delete(self):
        if LOG_CONFIG['PRINT_PROTOCOL_LOG']:
            print('[SERVER] {0} / {1}'.format(self.methods, self.endpoint))
        db_connector = DBConnector()
        try:
            request_data = request.get_json()
            request_overlay = HompOverlay(request_data.get('overlay'))

            if not request_overlay.is_valid(HompOverlay.BASE):
                raise ValueError

            select_overlay = db_connector.select_one(query.SELECT_HP2P_OVERLAY_BY_OVERLAY_ID, (
                request_overlay.overlay_id))

            if select_overlay is None:
                return request_overlay.to_json(HompOverlay.REMOVAL), 404
            
            if self.checkOwnerId(select_overlay.get('owner_id'), request_overlay.owner_id) is False:
                return request_overlay.to_json(HompOverlay.REMOVAL), 403
            
            if select_overlay.get('auth_admin_key') != request_overlay.auth.admin_key:
                return request_overlay.to_json(HompOverlay.REMOVAL), 403

            db_connector.delete_hp2p_data(request_overlay.overlay_id)

            Factory.get().delete_overlay(request_overlay.overlay_id)
            Factory.get().get_web_socket_manager().send_remove_overlay_message(request_overlay.overlay_id)
            Factory.get().get_web_socket_manager().send_log_message(request_overlay.overlay_id,
                                                                    request_overlay.owner_id, 'Overlay Removal.')

            db_connector.commit()
            return request_overlay.to_json(HompOverlay.REMOVAL), 200
        except ValueError:
            db_connector.rollback()
            return 'BAD REQUEST', 400
        except Exception as exception:
            db_connector.rollback()
            return str(exception), 500


class ApiHybridOverlayRemoval(Resource):
    def post(self):
        print('[SERVER] {0} / {1}'.format(self.methods, self.endpoint))
        db_connector = DBConnector()
        try:
            request_data = request.get_json()
            overlay_id = request_data.get('overlay-id')

            if overlay_id is None:
                raise ValueError

            select_overlay = db_connector.select_one(query.SELECT_HP2P_OVERLAY_BY_OVERLAY_ID, (overlay_id,))
            if select_overlay is None:
                raise ValueError

            db_connector.delete_hp2p_data(overlay_id)

            Factory.get().delete_overlay(overlay_id)
            Factory.get().get_web_socket_manager().send_remove_overlay_message(overlay_id)
            Factory.get().get_web_socket_manager().send_log_message(overlay_id, 'Administrator', 'Overlay Removal.')

            db_connector.commit()
            return {'overlay-id': overlay_id}, 200
        except ValueError:
            db_connector.rollback()
            return 'BAD REQUEST', 400
        except Exception as exception:
            db_connector.rollback()
            return str(exception), 500


class GetInitData(Resource):
    def get(self):
        print('[SERVER] {0} / {1}'.format(self.methods, self.endpoint))
        return {'WEB_SOCKET_PORT': WEB_SOCKET_CONFIG['PORT']}, 200


class GetOverlayCostMap(Resource):
    def get(self):
        print('[SERVER] {0} / {1}'.format(self.methods, self.endpoint))
        if len(request.args) > 0 and 'overlay_id' in request.args:
            overlay = Factory.get().get_overlay(request.args.get('overlay_id'))
            message = Factory.get().get_web_socket_manager().create_overlay_cost_map_message(overlay)
            return message, 200
        else:
            return None, 404
