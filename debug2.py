# %% [markdown]
# ### Submitted by:
# - Shahar Asher
# - Hadar Liel Harush

# %%
import numpy as np
import re

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

# %%
treining_set_T = [[[1, 0, 0], [1, 0, 1], [0, 1, 0]],
                  [[1, 0, 0], [0, 0, 1], [1, 0, 1]],
                  [[1, 0, 0], [0, 0, 1], [0, 0, 0]]]
treining_set_F = [[[0, 0, 1], [0, 1, 0], [1, 0, 0]],
                  [[0, 1, 0], [1, 0, 1], [0, 1, 0]],
                  [[0, 1, 1], [1, 1, 0], [0, 1, 1]]]

# %%
# not p4 or (p4 or p8) and (p2 and p9) or p9
print(generare_rull.split(' '))
generare_rull_list = [re.findall(r'\(||\)||not||[0-9]||or||and', rull) for rull in generare_rull.split(' ')]
print(generare_rull_list)
generare_rull_list = [r for rull in generare_rull_list for r in rull if r != '']
print(generare_rull_list)

# %%
# not p4 or (p4 or p8) and (p2 and p9) or p9
rull_list_len = len(generare_rull_list)
rull = 0
while rull < rull_list_len:
    if generare_rull_list[rull] == 'not':
        generare_rull_list[rull+1] = f'-{generare_rull_list[rull+1]}'
        generare_rull_list.pop(rull)
        rull_list_len -= 1
    elif generare_rull_list[rull] == '(':
        temp_lst = []
        i = rull + 1
        generare_rull_list[rull] = temp_lst
        while generare_rull_list[i] != ')':
            temp_lst.append(generare_rull_list[i])
            generare_rull_list.pop(i)
            rull_list_len -= 1
        else:
            generare_rull_list.pop(i)
            rull_list_len -= 1
    rull+=1

# %%
def to_int(lst):
    filtered_list = []
    for rull in lst:
        if isinstance(rull, list):
            filtered_list.append(to_int(rull))
        elif rull != 'or' and rull != 'and':
            filtered_list.append(int(rull))
        else:
            filtered_list.append(rull)
    return filtered_list

# %%
generare_rull_list = to_int(generare_rull_list)
print(generare_rull_list)

# %%
def check_rull(rull_lst, treining_set):
    check_rull_lst = []
    for rull in rull_lst:
        if isinstance(rull, list):
            check_rull_lst.append(check_rull(rull, treining_set))
        elif rull == 'or' or rull == 'and':
            check_rull_lst.append(rull)
        else:
            for i in range(len(treining_set)):
                print(np.abs(rull))
                row = (np.abs(rull)//3)-1 if np.abs(rull)%3 == 0 else np.abs(rull)//3
                if i == 0:
                    check_rull_lst.append(treining_set[i][row][(np.abs(rull)%3)-1] != 0)
                    print(treining_set[i][row][(np.abs(rull)%3)-1] != 0)
                    print(check_rull_lst)
                else:
                    if treining_set[i][row][(np.abs(rull)%3)-1] != 0:
                        check_rull_lst[-1] = False
                    print(treining_set[i][row][(np.abs(rull)%3)-1] != 0)
                    print(check_rull_lst)
    return check_rull_lst

# %%
check_rull_T = check_rull(generare_rull_list, treining_set_T)
check_rull_F = check_rull(generare_rull_list, treining_set_F)

print(check_rull_T)
print(check_rull_F)


