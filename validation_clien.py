import socket


ENCODING = 'utf-8'


class NotResponseValidationServerError(Exception):
    """An error that occurs when there is no response
    from the verification server.
    """

    pass


def validation_client(server: str, port: int, request_body: str):
    """Sends request to RKSOK server and return response as string."""

    conn = socket.create_connection((server, port))
    conn.sendall(request_body.encode(ENCODING))
    try:
        raw_response = receive_response_body(conn)
        return raw_response
    except socket.timeout:
        raise NotResponseValidationServerError()
        

def receive_response_body(conn) -> str:
    """Receives data from socket connection and returns it as string,
    decoded using ENCODING

    """
      
    response = b""
    while True:
        conn.settimeout(5)
        data = conn.recv(1024)
        if not data: break
        response += data
    return response.decode(ENCODING)

