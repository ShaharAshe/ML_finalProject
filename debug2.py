# %% [markdown]
# ### Submitted by:
# - Shahar Asher
# - Hadar Liel Harush

# %%
import numpy as np
import re

np.random.seed(0)

# %%
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
treining_set_T = [[[1, 0, 0], [1, 0, 1], [0, 1, 0]],
                  [[1, 0, 0], [0, 0, 1], [1, 0, 1]],
                  [[1, 0, 0], [0, 0, 1], [0, 0, 0]]]
treining_set_F = [[[0, 0, 1], [0, 1, 0], [1, 0, 0]],
                  [[0, 1, 0], [1, 0, 1], [0, 1, 0]],
                  [[0, 1, 1], [1, 1, 0], [0, 1, 1]]]

# %%
# not p4 or (p4 or p8) and (p2 and p9) or p9
def removeP(lst):
    generare_rull_list = [re.findall(r'\(||\)||not||[0-9]||or||and', rull) for rull in lst.split(' ')]
    generare_rull_list = [r for rull in generare_rull_list for r in rull if r != '']
    return generare_rull_list

# %%
# not p4 or (p4 or p8) and (p2 and p9) or p9
def removeNotAndClosing(lst):
    rull_list_len = len(lst)
    rull = 0
    while rull < rull_list_len:
        if lst[rull] == 'not':
            lst[rull+1] = f'-{lst[rull+1]}'
            lst.pop(rull)
            rull_list_len -= 1
        elif lst[rull] == '(':
            temp_lst = []
            i = rull + 1
            lst[rull] = temp_lst
            while lst[i] != ')':
                if lst[i] == 'not':
                    lst[i+1] = f'-{lst[i+1]}'
                    lst.pop(i)
                    rull_list_len -= 1
                temp_lst.append(lst[i])
                lst.pop(i)
                rull_list_len -= 1
            else:
                lst.pop(i)
                rull_list_len -= 1
        rull+=1
    return lst

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
def check_rull(rull_lst, treining_set):
    check_rull_lst = []
    for rull in rull_lst:
        if isinstance(rull, list):
            check_rull_lst.append(check_rull(rull, treining_set))
        elif rull == 'or' or rull == 'and':
            check_rull_lst.append(rull)
        else:
            for i in range(len(treining_set)):
                row = (np.abs(rull)//3)-1 if np.abs(rull)%3 == 0 else np.abs(rull)//3
                if i == 0:
                    if rull > 0:
                        check_rull_lst.append(treining_set[i][row][(np.abs(rull)%3)-1] != 0)
                    else:
                        check_rull_lst.append(treining_set[i][row][(np.abs(rull)%3)-1] == 0)
                else:
                    if rull > 0:
                        if treining_set[i][row][(np.abs(rull)%3)-1] == 0:
                            check_rull_lst[-1] = False
                    else:
                        if treining_set[i][row][(np.abs(rull)%3)-1] != 0:
                            check_rull_lst[-1] = False

    return check_rull_lst

# %%
def checkBoolRull(rull_lst):
    bool_rull_lst = []
    operator = ''
    for rull in range(len(rull_lst)):
        if isinstance(rull_lst[rull], list):
            bool_lst_temp = checkBoolRull(rull_lst[rull])
            if bool_rull_lst == []:
                bool_rull_lst.append(bool_lst_temp)
            elif operator == 'or':
                bool_rull_lst[0] = bool_rull_lst[0] or bool_lst_temp
            elif operator == 'and':
                bool_rull_lst[0] = bool_rull_lst[0] and bool_lst_temp
        elif bool_rull_lst == []:
            bool_rull_lst.append(rull_lst[rull])
        elif rull_lst[rull] == 'or':
            operator = 'or'
        elif rull_lst[rull] == 'and':
            operator = 'and'
        else:
            if operator == 'or':
                bool_rull_lst[0] = bool_rull_lst[0] or rull_lst[rull]
            elif operator == 'and':
                bool_rull_lst[0] = bool_rull_lst[0] and rull_lst[rull]
    return bool_rull_lst[0]

# %%
def legalRull():
    while True:
        generare_rull = GenRundomRull()
        generare_rull_list = removeP(generare_rull)
        generare_rull_list = removeNotAndClosing(generare_rull_list)
        generare_rull_list = to_int(generare_rull_list)
        check_rull_T = check_rull(generare_rull_list, treining_set_T)
        check_rull_F = check_rull(generare_rull_list, treining_set_F)
        is_rull_T = checkBoolRull(check_rull_T)
        is_rull_F = checkBoolRull(check_rull_F)
        
        if (is_rull_T and not is_rull_F):
            return generare_rull, True
        elif (is_rull_T and not is_rull_F):
            return generare_rull, False

# %%
generare_rull, classification = legalRull()
print(f'legal rull as --{classification}--:\n--------------------\n{generare_rull}')


# %%
training_example = [[[1, 0, 0], [0, 1, 0], [0, 0, 1]]]

# %%
def activate_rull(rull, trining_set):
    generare_rull_list = removeP(generare_rull)
    generare_rull_list = removeNotAndClosing(generare_rull_list)
    generare_rull_list = to_int(generare_rull_list)
    check_rull_ex = check_rull(generare_rull_list, treining_set_T)
    is_rull_ex = checkBoolRull(check_rull_ex)
    return is_rull_ex

# %%
if activate_rull(generare_rull, training_example):
    if classification:
        print('The rull is working correctly')
    else:
        print('The rull is not working correctly')
else:
    if classification:
        print('The rull is not working correctly')
    else:
        print('The rull is working correctly')

# %%
rulls_lst_T = []
rulls_lst_F = []

for i in range(20):
    while True:
        temp_rull = legalRull()
        if temp_rull[1]:
            rulls_lst_T.append(temp_rull)
            break
for i in range(20):
    while True:
        temp_rull = legalRull()
        if not temp_rull[1]:
            rulls_lst_F.append(temp_rull)
            break

print(rulls_lst_T)
print(rulls_lst_F)


