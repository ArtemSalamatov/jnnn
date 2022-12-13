import random

CODES_BASE = dict()


def generate_code(task: str, chat_id: str, user_id: str):
    code = ''.join([str(random.randint(0, 9)) for digit in range(4)])
    CODES_BASE[code] = [task, chat_id, user_id]
    return code
