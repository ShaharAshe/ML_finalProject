# %% [markdown]
# ### Submitted by:
# - Shahar Asher
# - Hadar Liel Harush

# %%
import numpy as np

# %%
np.random.seed(0)

def GenRundomRull()->str:
    operators = ['and', 'or']
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

# %%
generare_rull = GenRundomRull()
print(generare_rull)
generare_rull_list = generare_rull.split(' ')
print(generare_rull_list)

# %%
treining_set_T = [[[1, 0, 0], [1, 0, 1], [0, 1, 0]],
                  [[1, 0, 0], [0, 0, 1], [1, 0, 1]],
                  [[1, 0, 0], [0, 0, 1], [0, 0, 0]]]
treining_set_F = [[[0, 0, 1], [0, 1, 0], [1, 0, 0]],
                  [[0, 1, 0], [1, 0, 1], [0, 1, 0]],
                  [[0, 1, 1], [1, 1, 0], [0, 1, 1]]]

# %%
# not p4 or (p4 or p8) and (p2 and p9) or p9

operator:str = ''
result_T:bool = []
result_F:bool = []
is_not: bool = False

for i in range(len(generare_rull_list)):
    curr_bool_T:bool = True
    curr_bool_F:bool = True

    if generare_rull_list[i] == 'or' or generare_rull_list[i] == 'and':
        operator = generare_rull_list[i]
    elif generare_rull_list[i] == 'not':
        is_not = True
    elif generare_rull_list[i][0] == '(':
        for t in treining_set_T:
            if not t[int(generare_rull_list[i][2])//3][(int(generare_rull_list[i][2])%3)-1]:
                curr_bool_t = False
        if is_not:
            curr_bool_T = not curr_bool_T
        
        for f in treining_set_F:
            if not f[int(generare_rull_list[i][2])//3][(int(generare_rull_list[i][2])%3)-1]:
                curr_bool_F = False
        if is_not:
            curr_bool_F = not curr_bool_F

        i += 1

        if not len(result_F):
            result_F.append(curr_bool)
        elif operator == 'or':
            result_F[0] = result_F[0] or curr_bool
        elif operator == 'and':
            result_F[0] = result_F[0] and curr_bool
        
        operator = ''
        i+=1
    else:
        for t in treining_set_T:
            print(generare_rull_list[i][1])
            if not t[int(generare_rull_list[i][1])//3][(int(generare_rull_list[i][1])%3)]:
                curr_bool = False
        if is_not:
            curr_bool = not curr_bool
        
        if not len(result_T):
                result_T.append(curr_bool)
        elif operator == 'or':
            result_T[0] = result_T[0] or curr_bool
        elif operator == 'and':
            result_T[0] = result_T[0] and curr_bool

        curr_bool = True

        for f in treining_set_F:
            if not f[int(generare_rull_list[i][1])//3][(int(generare_rull_list[i][1])%3)-1]:
                curr_bool = False
        if is_not:
            curr_bool = not curr_bool
        
        if not len(result_F):
            result_F.append(curr_bool)
        elif operator == 'or':
            result_F[0] = result_F[0] or curr_bool
        elif operator == 'and':
            result_F[0] = result_F[0] and curr_bool
        
        operator = ''



