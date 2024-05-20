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

from datetime import datetime


SHOW_DATABASES = "SHOW DATABASES LIKE %s"

CREATE_DATABASE = "CREATE DATABASE IF NOT EXISTS {0}"

USE_DATABASES = "USE {0}"

SHOW_HP2P_OVERLAY = "SHOW TABLES LIKE 'hp2p_overlay'"

CREATE_HP2P_OVERLAY = "CREATE TABLE IF NOT EXISTS hp2p_overlay ( " \
                      "overlay_id varchar(50) COLLATE utf8_unicode_ci NOT NULL, " \
                      "title varchar(100) COLLATE utf8_unicode_ci NOT NULL, " \
                      "overlay_type varchar(50) COLLATE utf8_unicode_ci NOT NULL, " \
                      "sub_type varchar(50) COLLATE utf8_unicode_ci NOT NULL, " \
                      "owner_id varchar(50) COLLATE utf8_unicode_ci NOT NULL, " \
                      "overlay_status varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL, " \
                      "description varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL, " \
                      "heartbeat_interval int(11) NOT NULL DEFAULT 0,  " \
                      "heartbeat_timeout int(11) NOT NULL DEFAULT 0, " \
                      "auth_keyword varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL, " \
                      "auth_type varchar(50) COLLATE utf8_unicode_ci NOT NULL,  " \
                      "auth_admin_key varchar(50) COLLATE utf8_unicode_ci NOT NULL,  " \
                      "auth_access_key varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL, " \
                      "mn_cache INT(11) NULL DEFAULT NULL, " \
                      "md_cache INT(11) NULL DEFAULT NULL, " \
                      "recovery_by VARCHAR(50) COLLATE utf8_unicode_ci DEFAULT NULL, " \
                      "created_at datetime NOT NULL, " \
                      "updated_at datetime NOT NULL,  " \
                      " PRIMARY KEY (`overlay_id`))"

SHOW_HP2P_PEER = "SHOW TABLES LIKE 'hp2p_peer'"

CREATE_HP2P_PEER = "CREATE TABLE IF NOT EXISTS hp2p_peer ( " \
                   "peer_id varchar(50) COLLATE utf8_unicode_ci NOT NULL, " \
                   "overlay_id varchar(50) COLLATE utf8_unicode_ci NOT NULL,  " \
                   "ticket_id int(11) DEFAULT NULL,  " \
                   "overlay_type varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL, " \
                   "sub_type varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL, " \
                   "expires int(11) DEFAULT NULL,  " \
                   "address varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL, " \
                   "auth_password varchar(50) COLLATE utf8_unicode_ci NOT NULL,  " \
                   "num_primary int(11) NOT NULL DEFAULT 0,  " \
                   "num_out_candidate int(11) NOT NULL DEFAULT 0, " \
                   "num_in_candidate int(11) NOT NULL DEFAULT 0, " \
                   "costmap longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,  " \
                   "created_at datetime DEFAULT NULL, " \
                   "updated_at datetime DEFAULT NULL, " \
                   "report_time datetime DEFAULT NULL, " \
                   " PRIMARY KEY (peer_id, overlay_id))"

SHOW_HP2P_AUTH_PEER = "SHOW TABLES LIKE 'hp2p_auth_peer'"

CREATE_HP2P_AUTH_PEER = "CREATE TABLE IF NOT EXISTS hp2p_auth_peer ( " \
                        "overlay_id varchar(50) COLLATE utf8_unicode_ci NOT NULL, " \
                        "peer_id varchar(50) COLLATE utf8_unicode_ci NOT NULL, " \
                        "updated_at datetime DEFAULT NULL, " \
                        "PRIMARY KEY (overlay_id, peer_id))"

DELETE_ALL_HP2P_AUTH_PEER = "DELETE FROM hp2p_auth_peer"

DELETE_ALL_HP2P_PEER = "DELETE FROM hp2p_peer"

DELETE_ALL_HP2P_OVERLAY = "DELETE FROM hp2p_overlay"

SELECT_HP2P_OVERLAY = "SELECT * FROM hp2p_overlay"
# SELECT_HP2P_OVERLAY = "SELECT " \
#                       "overlay_id, title, overlay_type, sub_type, owner_id, expires, overlay_status, auth_type " \
#                       "FROM hp2p_overlay"

SELECT_HP2P_OVERLAY_BY_OVERLAY_ID = "SELECT * FROM hp2p_overlay WHERE overlay_id = %s"

SELECT_HP2P_SERVICE_BY_OVERLAY_ID = "SELECT * FROM hp2p_service WHERE overlay_id = %s"

SELECT_HP2P_CHANNEL_BY_SERVICE_ID = "SELECT * FROM hp2p_channel WHERE service_id = %s"

SELECT_HP2P_CHANNEL_ATTRIBUTE_BY_CHANNEL_ID_AND_SERVICE_ID = "SELECT * FROM hp2p_channel_attribute " \
                                                             "WHERE channel_id = %s AND service_id = %s"

SELECT_HP2P_CHANNEL_SOURCE_LIST_BY_CHANNEL_ID_AND_SERVICE_ID = "SELECT * FROM hp2p_channel_source " \
                                                             "WHERE channel_id = %s AND service_id = %s"

SELECT_HP2P_SERVICE_SOURCE_BY_SERVICE_ID = "SELECT * FROM hp2p_service_source WHERE service_id = %s"

SELECT_HP2P_SERVICE_BLOCK_BY_SERVICE_ID = "SELECT * FROM hp2p_service_block WHERE service_id = %s"

SELECT_HP2P_SERVICE_BLOCK_BY_OVERLAY_ID = "SELECT bl.peer_id FROM hp2p_service_block bl, hp2p_service se WHERE se.overlay_id = %s AND se.service_id = bl.service_id"

SELECT_HP2P_PEER_BY_OVERLAY_ID = "SELECT * FROM hp2p_peer WHERE overlay_id = %s ORDER BY ticket_id"

DELETE_HP2P_PEER = "DELETE FROM hp2p_peer WHERE peer_id = %s AND overlay_id = %s"

DELETE_HP2P_PEER_LIKE = "DELETE FROM hp2p_peer WHERE peer_id LIKE %s AND overlay_id = %s"

DELETE_HP2P_PEER_NOT_REGEXP = "DELETE FROM hp2p_peer WHERE overlay_id = %s AND peer_id NOT REGEXP (%s)"

DELETE_HP2P_PEER_BY_OVERLAY_ID = "DELETE FROM hp2p_peer WHERE overlay_id = %s"

DELETE_HP2P_OVERLAY_BY_OVERLAY_ID = "DELETE FROM hp2p_overlay WHERE overlay_id = %s"

DELETE_HP2P_AUTH_PEER_BY_OVERLAY_ID = "DELETE FROM hp2p_auth_peer WHERE overlay_id = %s"

UPDATE_HP2P_OVERLAY_AUTH_CLOSED_BY_OVERLAY_ID = "UPDATE hp2p_overlay SET auth_type = 'closed' WHERE overlay_id = %s"

UPDATE_HP2P_OVERLAY_AUTH_OPEN_BY_OVERLAY_ID = "UPDATE hp2p_overlay SET auth_type = 'open' WHERE overlay_id = %s"

DELETE_HP2P_SERVICE_SOURCE_BY_SERVICE_ID = "DELETE FROM hp2p_service_source WHERE service_id = %s"

DELETE_HP2P_SERVICE_BLOCK_BY_SERVICE_ID = "DELETE FROM hp2p_service_block WHERE service_id = %s"

DELETE_HP2P_CHANNEL_SOURCE_BY_SERVICE_ID_AND_CHANNEL_ID = "DELETE FROM hp2p_channel_source WHERE service_id = %s AND channel_id = %s"

INSERT_HP2P_OVERLAY = "INSERT INTO hp2p_overlay " \
                      "(overlay_id, title, overlay_type, sub_type, owner_id, overlay_status," \
                      "description, heartbeat_interval, heartbeat_timeout, auth_keyword, auth_type, " \
                      "auth_admin_key, auth_access_key, mn_cache, md_cache, recovery_by," \
                      " created_at, updated_at) " \
                      "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, " \
                      "NOW(), NOW())"

INSERT_HP2P_SERVICE = "INSERT INTO hp2p_service " \
                      "(overlay_id, start_datetime, end_datetime, title, description) " \
                      "VALUES (%s, %s, %s, %s, %s)"

INSERT_HP2P_SERVICE_SOURCE = "INSERT INTO hp2p_service_source " \
                             "(service_id, peer_id) " \
                             "VALUES (%s, %s)"

INSERT_HP2P_SERVICE_BLOCK = "INSERT INTO hp2p_service_block " \
                             "(service_id, peer_id) " \
                             "VALUES (%s, %s)"

INSERT_HP2P_CHANNEL = "INSERT INTO hp2p_channel " \
                      "(channel_id, service_id, channel_type) " \
                      "VALUES (%s, %s, %s)"

INSERT_HP2P_CHANNEL_SOURCE = "INSERT INTO hp2p_channel_source " \
                             "(channel_id, service_id, peer_id) " \
                             "VALUES (%s, %s, %s)"

INSERT_HP2P_CHANNEL_ATTRIBUTE = "INSERT INTO hp2p_channel_attribute " \
                                "(channel_id, service_id, keyword, value) " \
                                "VALUES (%s, %s, %s, %s)"

INSERT_HP2P_AUTH_PEER = "INSERT INTO hp2p_auth_peer (overlay_id, peer_id, updated_at) VALUES (%s, %s, now())"

ORDER_BY_CREATED_AT = " ORDER BY created_at"

WHERE_OVERLAY_ID = " WHERE overlay_id = %s"

WHERE_SERVICE_ID = " WHERE service_id = %s"

WHERE_TITLE = " WHERE title LIKE %s"

WHERE_DESCRIPTION = " WHERE description LIKE %s"

SELECT_NUM_PEERS = "SELECT COUNT(*) AS num_peers FROM hp2p_peer WHERE overlay_id = %s"

SELECT_HP2P_OVERLAY_BY_ADMIN_KEY = "SELECT overlay_id, auth_access_key, owner_id FROM hp2p_overlay " \
                                   "WHERE overlay_id = %s AND auth_admin_key = %s"

UPDATE_HP2P_OVERLAY = "UPDATE hp2p_overlay SET updated_at = now()"

SET_TITLE = ", title = %s"

SET_EXPIRES = ", expires = %s"

SET_DESCRIPTION = ", description = %s"

SET_OWNER_ID = ", owner_id = %s"

SET_ADMIN_KEY = ", auth_admin_key = %s"

UPDATE_HP2P_SERVICE = "UPDATE hp2p_service SET updated_at = now()"

SET_START_DATETIME = ", start_datetime = %s"

SET_END_DATETIME = ", end_datetime = %s"

UPDATE_HP2P_OVERLAY_SET_ACCESS_KEY = "UPDATE hp2p_overlay SET auth_access_key = %s WHERE overlay_id = %s"

SELECT_AUTH_PEER_ID_LIST = "SELECT peer_id FROM hp2p_auth_peer WHERE overlay_id = %s"

SELECT_OVERLAY_ACCESS_KEY = "SELECT auth_access_key FROM hp2p_overlay WHERE overlay_id = %s"

SELECT_AUTH_PEER_ID = "SELECT peer_id FROM hp2p_auth_peer WHERE overlay_id = %s AND peer_id = %s"

SELECT_HP2P_PEER_PASSWORD = "SELECT * FROM hp2p_peer WHERE peer_id = %s AND overlay_id = %s AND auth_password = %s"

SELECT_RECOVERY_PEER_LIST = "SELECT v_p_t.peer_id, v_p_t.address FROM " \
                            " (SELECT p_t.*,@rownum := @rownum + 1 AS rank1 FROM " \
                            " (SELECT * FROM hp2p_peer WHERE " \
                            " overlay_id = %s AND num_primary > 0) p_t," \
                            " (SELECT @rownum := 0) r " \
                            " ORDER BY p_t.ticket_id) v_p_t " \
                            "WHERE v_p_t.rank1 <= %s AND v_p_t.ticket_id < %s " \
                            "ORDER BY v_p_t.rank1 DESC LIMIT %s"

SELECT_PEER_LIST = "SELECT v_p_t.peer_id, v_p_t.address FROM " \
                   " (SELECT p_t.*,@rownum := @rownum + 1 AS rank1 FROM " \
                   " (SELECT * FROM hp2p_peer WHERE " \
                   " overlay_id = %s AND num_primary > 0) p_t," \
                   " (SELECT @rownum := 0) r " \
                   " ORDER BY p_t.ticket_id) v_p_t " \
                   "WHERE v_p_t.rank1 >= %s LIMIT %s"

INSERT_HP2P_PEER = "INSERT INTO hp2p_peer " \
                   "(peer_id, display_name, overlay_id, ticket_id ,overlay_type, sub_type, expires, address, " \
                   "auth_password, auth_public_key, created_at, updated_at) " \
                   "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW(), NOW())"

SELECT_TOP_PEER = "SELECT peer_id, address FROM hp2p_peer WHERE overlay_id = %s ORDER BY ticket_id LIMIT 1"

UPDATE_HP2P_PEER = "UPDATE hp2p_peer SET updated_at = NOW(), expires = %s WHERE overlay_id = %s AND peer_id = %s"

SELECT_HP2P_PEER = "SELECT * FROM hp2p_peer WHERE overlay_id = %s AND peer_id LIKE %s"

UPDATE_HP2P_PEER_COST_MAP = "UPDATE hp2p_peer SET " \
                            "num_primary = %s, num_out_candidate = %s, " \
                            "num_in_candidate = %s, costmap = %s, report_time = NOW() " \
                            "WHERE overlay_id = %s AND peer_id = %s"

def get_service_info(db_connector, overlay_id, with_source_list=False):
    select_service = db_connector.select_one(SELECT_HP2P_SERVICE_BY_OVERLAY_ID, (overlay_id,))
    if select_service is not None:
        serviceinfo = {
            'start-datetime': datetime.strftime(select_service.get('start_datetime'), '%Y%m%d%H%M%S'),
            'end-datetime': datetime.strftime(select_service.get('end_datetime'), '%Y%m%d%H%M%S'),
            'title': select_service.get('title'),
            'description': select_service.get('description')
        }

        service_id = select_service.get('service_id')

        if with_source_list:
            select_service_source_list = db_connector.select(SELECT_HP2P_SERVICE_SOURCE_BY_SERVICE_ID, (service_id,))
            serviceinfo['source-list'] = []
            if len(select_service_source_list) > 0:
                for select_service_source in select_service_source_list:
                    source_peer_id = select_service_source.get('peer_id')
                    if source_peer_id != '-':
                        serviceinfo['source-list'].append(source_peer_id)
                    else:
                        del serviceinfo['source-list']
                        break

            select_service_block_list = db_connector.select(SELECT_HP2P_SERVICE_BLOCK_BY_SERVICE_ID, (service_id,))
            serviceinfo['block-list'] = []
            if len(select_service_block_list) > 0:
                for select_service_block in select_service_block_list:
                    serviceinfo['block-list'].append(select_service_block.get('peer_id'))

        select_channel_list = db_connector.select(SELECT_HP2P_CHANNEL_BY_SERVICE_ID, (service_id,))
        if len(select_channel_list) > 0:
            serviceinfo['channel-list'] = []
            for select_channel in select_channel_list:
                channel_id = select_channel.get('channel_id')
                channel_type = select_channel.get('channel_type')

                channel = {
                    'channel-id': channel_id,
                    'channel-type': channel_type
                }

                if channel_type != 'control':
                    if with_source_list:
                        select_channel_source_list = db_connector.select(SELECT_HP2P_CHANNEL_SOURCE_LIST_BY_CHANNEL_ID_AND_SERVICE_ID, (channel_id, service_id))
                        if len(select_channel_source_list) > 0:
                            channel['source-list'] = []
                            for select_channel_source in select_channel_source_list:
                                source_peer_id = select_channel_source.get('peer_id')
                                if source_peer_id != '-':
                                    channel['source-list'].append(source_peer_id)
                                else:
                                    del channel['source-list']
                                    break
                
                    select_channel_attribute_list = db_connector.select(SELECT_HP2P_CHANNEL_ATTRIBUTE_BY_CHANNEL_ID_AND_SERVICE_ID, (channel_id, service_id))
                    if len(select_channel_attribute_list) > 0:
                        channel_attribute = {}
                        for select_channel_attribute in select_channel_attribute_list:
                            channel_attribute[select_channel_attribute.get('keyword')] = select_channel_attribute.get('value')
                        channel['channel-attribute'] = channel_attribute
                
                serviceinfo['channel-list'].append(channel)
        return serviceinfo
    
    return None

