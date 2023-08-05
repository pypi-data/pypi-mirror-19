# https://github.com/jakm/txmsgpackrpc
# Copyright (c) 2015 Jakub Matys

from __future__ import print_function

from twisted.internet import address
from twisted.python import log

from txmsgpackrpc.constant import (MSGTYPE_REQUEST, MSGTYPE_NOTIFICATION,
                                   STATUS_OK, STATUS_ERR)


class AccesslogMixIn(object):

    logFormat = (u'%(peer)s %(msgType)s %(msgid)s "%(methodName)s '
                 u'%(params)s" %(status)s %(length)s')
    logResponse = False

    def __init__(self, logFormat=None):
        if logFormat is not None:
            self.logFormat = logFormat
        if '%(response)s' in self.logFormat:
            self.logResponse = True
        self.__reactor = None

    def logRPC(self, response, msgType, msgid, methodName, params, context):
        try:
            status, response, length = response

            if context is None:
                peer = '-'
            else:
                addr = context.peer
                if isinstance(addr, (address.IPv4Address, address.IPv6Address)):
                    peer = '%s:%s:%s' % (addr.type, addr.host, addr.port)
                elif isinstance(addr, address.UNIXAddress):
                    peer = 'UNIX:%s' % addr.name
                elif isinstance(addr, tuple):
                    # TODO: pack to the IAddress in *DatagramProtocol
                    peer = 'UDP:%s:%s' % addr[:2]
                else:
                    peer = '-'

            if self.logResponse:
                response = str(response)
                response = response.replace('\n', '\\n')
            else:
                response = ''

            msgType = ('REQUEST' if msgType == MSGTYPE_REQUEST else
                       'NOTIFICATION' if msgType == MSGTYPE_NOTIFICATION else
                       'UNKNOWN')

            msgid = msgid if msgid is not None else '-'

            status = ('OK' if status == STATUS_OK else
                      'ERR' if status == STATUS_ERR else
                      '???')

            log.msg(self.logFormat % {'peer': peer,
                                      'msgType': msgType,
                                      'msgid': msgid,
                                      'methodName': methodName,
                                      'params': params,
                                      'status': status,
                                      'response': response,
                                      'length': length})
        except Exception:
            log.err()
