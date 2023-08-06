import argparse

PROTOCOLS = ['udp', 'tcp', 'rest']

def ping(port, destination, protocol, timeout=10):
    """
    Send a request appropriate for the requested protocol to destination at port.
    Listen for timeout seconds for a well-known response.
    """

    resp = None
    if protocol == "rest":
        import wsgiref_wrapper
        resp = wsgiref_wrapper.get_and_check(destination, port)
        return True if resp else False
    else:
        import scapy_wrapper
        resp = scapy_wrapper.send_and_listen(
            destination_ip=destination,
            destination_port=port,
            protocol=protocol,
            timeout=timeout)
        #TODO: Make this check better
        try:
            if resp[0].res:
                return True
        except IndexError:
            return False


def listen(port, protocol, timeout=3600):
    """
    Initiate a listener for the given protocol that will listen for timeout seconds.
    """

    if protocol == 'tcp':
        import scapy_wrapper
        scapy_wrapper.listen(
            port=port,
            protocol=protocol,
            reaction=scapy_wrapper.Reactions.respond_tcp,
            timeout=timeout)
    elif protocol == 'udp':
        import scapy_wrapper
        scapy_wrapper.listen(
            port=port,
            protocol=protocol,
            reaction=scapy_wrapper.Reactions.respond_udp,
            timeout=timeout)
    elif protocol == 'rest':
        import wsgiref_wrapper
        wsgiref_wrapper.start_server(port, timeout=timeout)
    else:
        raise Exception("Unsupported protocol type")
