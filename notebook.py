from os import remove
from typing import Union


GET = "ОТДОВАЙ"
DELETE = "УДОЛИ"
WRITE = "ЗОПИШИ"

RESPONSE = {
    "OK": "НОРМАЛДЫКС",
    "NOTFOUND": "НИНАШОЛ",
    "NOT_APPROVED": "НИЛЬЗЯ",
    "INCORRECT_REQUEST": "НИПОНЯЛ",
    }


PROTOCOL = "РКСОК/1.0"
ENCODING = "UTF-8"


class RKSOKNotebook:
    """Notebook working with RKSOK server."""

    def __init__(self, request_validation: str, response_validation: str):
        self.request_validation = request_validation
        self.response_validation = response_validation
        self._name = self.parse_name()


    def parse_name(self) -> str:
        """Checks the length of a name """

        inquiry = self.request_validation.split('\r\n')[0]
        name = ' '.join(inquiry.split(' ')[1:-1])
        return name


    def process_request(self) -> str:
        '''Processes requests and returns a response string'''
        
        for request_verb in (GET, DELETE, WRITE):
            if self.request_validation.startswith(request_verb):
                break
        else:
            return f'{RESPONSE["INCORRECT_REQUEST"]}\r\n\r\n'
        if self.response_validation.startswith(RESPONSE["NOT_APPROVED"]):
            return self.response_validation
        else:
            if len(self._name) > 30:
                return f'{RESPONSE["INCORRECT_REQUEST"]}\r\n\r\n'
            try:
                text = self.process_notebook(request_verb)
            except (OSError, FileNotFoundError):
                return f'{RESPONSE["NOTFOUND"]} {PROTOCOL}\r\n\r\n' # Failed requests
            if self.request_validation.startswith(GET):
                if not text:
                    return f'{RESPONSE["NOTFOUND"]} {PROTOCOL}\r\n\r\n' # GET request without phone number
                else:
                    text = text.replace('\n', '\r\n')
                    return f'{RESPONSE["OK"]} {PROTOCOL}\r\n{text}\r\n\r\n'
            else:
                return f'{RESPONSE["OK"]} {PROTOCOL}\r\n\r\n'

    
    def process_notebook(self, request:str) -> Union[str]:
        '''Running a function depending on the type of request'''

        data = '\r\n'.join(self.request_validation.split('\r\n')[1:])
        if request == GET:
                return self.read_notebook(self._name)
        elif request == WRITE:
                return self.notebook_entry(self._name, data)
        elif request == DELETE:
                return self.deleting_from_notebook(self._name)


    def notebook_entry(self, name: str, phone: str) -> None:
        '''Creates a file named (name) containing (phone)'''

        with open(f'notebook/{name}.txt', mode='w') as f:
            f.write(f'{phone.strip()}')


    def read_notebook(self, name: str) -> str:
        '''Reads information from a file (name)'''

        with open(f'notebook/{name}.txt', mode='r') as f:
            return f.read()


    def deleting_from_notebook(self, name: str) -> None:
        '''Deletes the file(name)'''

        remove(f'notebook/{name}.txt')
