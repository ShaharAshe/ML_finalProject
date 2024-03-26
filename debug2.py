# %% [markdown]
# ### Submitted by:
# - Shahar Asher
# - Hadar Liel Harush

# %%
import numpy as np
import re

np.random.seed(0)

# %% [markdown]
# ### Question 1
# Generate a random logical expression in the format described in section A.

# %%
# q1

def GenRundomRull()->str:
    """
    Generates a random logical rule in string format.
    Selects a random combination of logical operators ('and' or 'or') 
    and pixel values ('p1', 'p2', ..., 'p9') to construct the rule.
    The rule may include logical operators, 'not' operators, and parentheses
    to represent complex logical expressions.
    """
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

# %% [markdown]
# ### Question 2
# Check if the generated rule matches the training set presented at the beginning of the question, and if so, determine that the rule is valid.

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
    """
    Removes parentheses, logical operators, and 'not' operators from a list representing a logical rule.
    """
    generare_rull_list = [re.findall(r'\(||\)||not||[0-9]||or||and', rull) for rull in lst.split(' ')]
    generare_rull_list = [r for rull in generare_rull_list for r in rull if r != '']
    return generare_rull_list

# %%
def addClosing(lst):
    print(lst)
    is_close = True
    is_in = False

    list_len = len(lst)
    i = 0
    while i <= list_len:
        if is_close and not is_in:
            lst.insert(i, '(')
            is_close = False
            list_len+=1
        elif (i == list_len or (lst[i] == 'and' and not is_in)) and not is_close:
                lst.insert(i, ')')
                is_close = True
                list_len+=1
                i+=1
        elif lst[i] == '(':
            is_in = True
        elif lst[i] == ')':
            is_in = False
        i+=1
    print(lst)
    return lst

# %%
def removeClosing(lst, rull_list_len, rull):
    temp_lst = []
    i = rull + 1
    lst[rull] = temp_lst
    while lst[i] != ')':
        if lst[i] == '(':
            lst, rull_list_len = removeClosing(lst, rull_list_len, i)
        elif lst[i] == 'not':
            lst[i+1] = f'-{lst[i+1]}'
            lst.pop(i)
            rull_list_len -= 1
        temp_lst.append(lst[i])
        lst.pop(i)
        rull_list_len -= 1
    else:
        lst.pop(i)
        rull_list_len -= 1
    return (lst, rull_list_len)

# %%
def removeNotAndClosing(lst):
    """
    Removes 'not' operators and closing parentheses from a list representing a logical rule.
    """
    rull_list_len = len(lst)
    rull = 0
    while rull < rull_list_len:
        if lst[rull] == 'not':
            lst[rull+1] = f'-{lst[rull+1]}'
            lst.pop(rull)
            rull_list_len -= 1
        elif lst[rull] == '(':
            lst, rull_list_len = removeClosing(lst, rull_list_len, rull)
        rull+=1
    return lst

# %%
def to_int(lst):
    """
    Converts elements in a nested list to integers if they represent numeric values.
    """
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
    """
    Evaluates a logical rule against a training set.
    """
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
    """
    Recursively evaluates a nested logical rule.
    """
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
# q2

def legalRull():
    """
    Generates a random logical rule and checks if it's a legal rule.
    """
    while True:
        generare_rull = GenRundomRull()
        generare_rull_list = removeP(generare_rull)
        print(generare_rull_list, end="\n\n")
        generare_rull_list = addClosing(generare_rull_list)
        print(generare_rull_list, end="\n\n")
        generare_rull_list = removeNotAndClosing(generare_rull_list)
        print(generare_rull_list, end="\n\n")
        generare_rull_list = to_int(generare_rull_list)
        check_rull_T = check_rull(generare_rull_list, treining_set_T)
        check_rull_F = check_rull(generare_rull_list, treining_set_F)
        is_rull_T = checkBoolRull(check_rull_T)
        is_rull_F = checkBoolRull(check_rull_F)
        
        if (is_rull_T and not is_rull_F):
            return generare_rull, True
        elif (not is_rull_T and is_rull_F):
            return generare_rull, False

# %%
generare_rull, classification = legalRull()
print(f'legal rull as --{classification}--:\n--------------------\n{generare_rull}')


# %% [markdown]
# ### Question 3
# Apply the valid rule to the example.

# %%
training_example = [[[1, 0, 0], [0, 1, 0], [0, 0, 1]]]

# %%
# q3

def activate_rull(rull, trining_set):
    """
    Activates a rule on a given training set.
    """
    generare_rull_list = removeP(generare_rull)
    print(generare_rull_list, end="\n\n")
    generare_rull_list = addClosing(generare_rull_list)
    print(generare_rull_list, end="\n\n")
    generare_rull_list = removeNotAndClosing(generare_rull_list)
    print(generare_rull_list, end="\n\n")
    generare_rull_list = to_int(generare_rull_list)
    print(generare_rull_list, end="\n\n")
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

# %% [markdown]
# ### Question 4
# Use a loop that utilizes the previous parts of the code to find 20 rules that yield True on the example, and 20 rules that yield False on the same example.

# %%
# q4

def find_rull(bool_r):
    """
    Finds legal rules classified as either True or False.
    """
    lst = []
    for i in range(20):
        while True:
            temp_rull = legalRull()
            if temp_rull[1] == bool_r:
                lst.append(temp_rull)
                break
    return lst

# %%
rulls_lst_T = find_rull(True)
rulls_lst_F = find_rull(False)

for r in rulls_lst_T:
    print(f'legal rull as --{r[1]}--:\n--------------------\n{r[0]}', end="\n\n")
for r in rulls_lst_F:
    print(f'legal rull as --{r[1]}--:\n--------------------\n{r[0]}', end="\n\n")
print(rulls_lst_T)
print(rulls_lst_F)

# %% [markdown]
# ### Question 5
# Write the results to a text file according to the following guidelines:
# - The file name will be txt.rules.
# - The first line in the file will be:  
#   `# Rules that give True on test`
# - Following that, the 20 rules that yield true on the test will appear, with each rule written on a separate line.
# - The 22nd line in the file will be:  
#   `# Rules that give False on test`
# - Following that, the 20 rules that yield false on the test will appear, with each rule written on a separate line.
# - There should be no empty lines in the file.

# %%
# q5

with open('.//rules.txt', 'w') as file:
    file.write('# Rules that give True on test\n')
    for rull in rulls_lst_T:
        file.write(f'{rull[0]}\n')
    file.write('# Rules that give False on test\n')
    for rull in rulls_lst_F:
        file.write(f'{rull[0]}\n')
with open('.//rules.txt', 'r+') as file:
    content = file.read()
    content = content.rstrip('\n')
with open('.//rules.txt', 'w') as file:
    file.write(content)


