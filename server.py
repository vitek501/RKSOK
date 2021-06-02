import asyncio
from loguru import logger
from validation_clien import NotResponseValidationServerError, validation_client
from notebook import RKSOKNotebook



REQUESTS = ("ОТДОВАЙ", "УДОЛИ", "ЗОПИШИ")
REQUEST_RKSOK = "АМОЖНА? РКСОК/1.0"
INCORRECT_REQUEST = "НИПОНЯЛ РКСОК/1.0"
ENCODING = 'utf-8'
PROTOCOL = "РКСОК/1.0"


@logger.catch
async def handle_echo(reader, writer):
    while True:
        data = await reader.read(1024)
        message1 = data.decode(ENCODING)
        if message1 == '':
            break
        addr = writer.get_extra_info('peername')
        logger.info(f"Received {message1!r} from {addr!r}")
        if check_request(message1):
            try:
                request_validation = f"{REQUEST_RKSOK}\r\n{message1}"
                response_validation = validation_client('vragi-vezde.to.digital', 51624, request_validation)
                client = RKSOKNotebook(message1, response_validation)
                raw_response = client.process_request()
            except (NotResponseValidationServerError, ConnectionRefusedError):
                logger.info(f"Нет ответа от сервера проверки!")
                raw_response = f'{PROTOCOL}\r\nИзвините, нет ответа от сервера проверки!\r\nПопробуйте позже!\r\n\r\n'
        else:
            raw_response = f'{INCORRECT_REQUEST}\r\n\r\n'
        logger.info(f"Send: {raw_response}")
        writer.write(raw_response.encode(ENCODING))
        await writer.drain()
    writer.close()


async def main():
    server = await asyncio.start_server(
        handle_echo, '0.0.0.0', 8888)

    addr = server.sockets[0].getsockname()
    print(f'Serving on {addr}')

    async with server:
        await server.serve_forever()


def check_request(request):
    """Checks the request for compliance with the RKSOC standard"""

    head = request.split('\r\n')[0]
    status = head.split(' ')[0]
    name = ' '.join(head.split(' ')[1:-1])
    protocol = head.split(' ')[-1]
    for stat in REQUESTS:
        if status == stat:
            if protocol == PROTOCOL:
                print(name, len(name))
                if len(name) <= 30:
                    return True




                


if __name__ == "__main__":
    logger.add('log/debug.log', format="{time} - {level} - {message}", 
        level="DEBUG", rotation="1 MB", compression="zip")
    asyncio.run(main())


