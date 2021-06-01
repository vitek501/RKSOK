import socket


ENCODING = 'utf-8'

def validation_client(server: str, port: int, request_body: str):
        """Sends request to RKSOK server and return response as string."""

        conn = socket.create_connection((server, port))
        conn.sendall(request_body.encode(ENCODING))
        raw_response = receive_response_body(conn)
        return raw_response


def receive_response_body(conn) -> str:
        """Receives data from socket connection and returns it as string,
        decoded using ENCODING

        """
        
        response = b""
        while True:
            data = conn.recv(1024)
            if not data: break
            response += data
        return response.decode(ENCODING)

