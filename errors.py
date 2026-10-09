class BeastlinkError(Exception):
    pass


class NodeConnectionError(BeastlinkError):
    pass


class PlayerError(BeastlinkError):
    pass