from struct import unpack_from, calcsize

from twistedlilypad.Requests.AbstractRequest import AbstractRequest, AbstractRequestCodec
from twistedlilypad.Utilities.EncoderUtilities import booleanEncoder


class RequestGetPlayers(AbstractRequest):
    opcode = 0x20

    def __init__(self, listPlayers, includeUUIDs=False):
        self.listPlayers = listPlayers
        self.includeUUIDs = includeUUIDs


class RequestGetPlayersCodec(AbstractRequestCodec):
    @staticmethod
    def encode(request):
        assert isinstance(request, RequestGetPlayers)

        if request.includeUUIDs is None:
            return booleanEncoder(request.listPlayers)
        else:
            return booleanEncoder(request.listPlayers) + booleanEncoder(request.includeUUIDs)

    @staticmethod
    def decode(payload):
        listPlayers = unpack_from('>B', payload)[0] == 0

        if len(payload) > calcsize('>B'):
            includeUUIDs = unpack_from('>B', payload)[0] == 0
        else:
            includeUUIDs = False

        return RequestGetPlayers(listPlayers, includeUUIDs)