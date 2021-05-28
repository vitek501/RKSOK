import asyncio
from validation_clien import validation_client
from notebook import RKSOKNotebook
from loguru import logger


REQUEST_RKSOK = "АМОЖНА? РКСОК/1.0"
ENCODING = 'utf-8'


@logger.catch
async def handle_echo(reader, writer):
    while True:
        data = await reader.read(1024)
        message = data.decode()
        if message == '\r\n':
            break
        addr = writer.get_extra_info('peername')
        print(f"Received {message!r} from {addr!r}")
        request_validation = f"{REQUEST_RKSOK}\r\n{message}"
        response_validation = validation_client('vragi-vezde.to.digital', 51624, request_validation)
        print(request_validation, response_validation)
        client = RKSOKNotebook(message, response_validation)    
        raw_response = client.process_request()
        print(f"Send: {raw_response}")
        writer.write(raw_response.encode(ENCODING))
        await writer.drain()
    writer.close()

async def main():
    server = await asyncio.start_server(
        handle_echo, '127.0.0.1', 8888)

    addr = server.sockets[0].getsockname()
    print(f'Serving on {addr}')

    async with server:
        await server.serve_forever()




if __name__ == "__main__":
    logger.add('debug.txt', format="{time} {level} {meassage}", 
        level="DEBUG", rotation="1 MB", compression="zip")
    asyncio.run(main())


