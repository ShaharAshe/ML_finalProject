import numpy as np


np.random.seed(0)

def GenRundomRull()->str:
    operators = ['and', 'or', 'not']
    pixels = ['p1', 'p2', 'p3', 'p4', 'p5', 'p6', 'p7', 'p8', 'p9']
    rull = ''
    closing = []

    rull_len = np.random.randint(1, 10)
    for i in range(rull_len):
        is_closing = False
        if i != 0:
            rull += ' '
            rull += f'{np.random.choice(operators, 1)[0]} '
            is_closing = np.random.randint(10) != 0
        if is_closing and len(closing) == 0 and i != rull_len-1:
            rull += '('
            closing.append(')')
        else:
            is_closing = False

        if np.random.randint(10) == 0:
            rull += 'not '
        rull += f'{np.random.choice(pixels,1)[0]}'
        if not is_closing and len(closing) != 0:
            rull += ')'
            closing.pop()
    return rull

print(GenRundomRull())