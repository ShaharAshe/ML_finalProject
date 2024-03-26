import random

def GenRandomRule() -> str:
    """
    Generates a random logical rule in string format.
    Selects a random combination of logical operators ('and' or 'or') 
    and pixel values ('p1', 'p2', ..., 'p9') to construct the rule.
    The rule may include logical operators, 'not' operators, and parentheses
    to represent complex logical expressions.
    
    Returns:
        str: The randomly generated logical rule.
    """
    operators = ['and', 'or']
    pixels = ['p1', 'p2', 'p3', 'p4', 'p5', 'p6', 'p7', 'p8', 'p9']
    rule = ''
    
    rule_length = random.randint(1, 4) # changed upper limit to 4
    for i in range(rule_length):
        if i != 0:
            rule += f' {random.choice(operators)} '
        
        if random.randint(0, 9) == 0:
            rule += 'not '
        
        rule += random.choice(pixels)
        
        if random.randint(0, 9) == 0 and i != rule_length - 1:
            rule = '(' + rule
            rule += ')'
        
    return rule

def CheckRuleOnTrainingSet(rule: str, training_set_T: list, training_set_F: list) -> bool:
    """
    Checks if the given rule matches the training sets.
    
    Args:
        rule (str): The logical rule to be checked.
        training_set_T (list): List of lists representing the positive training set.
        training_set_F (list): List of lists representing the negative training set.
        
    Returns:
        bool: True if the rule matches both positive and negative training sets, False otherwise.
    """
    for sample in training_set_T:
        if not eval(rule, {}, {f'p{i+1}': pixel for i, pixel in enumerate(sample)}):
            return False
            
    for sample in training_set_F:
        if eval(rule, {}, {f'p{i+1}': pixel for i, pixel in enumerate(sample)}):
            return False
            
    return True

def WriteRulesToFile(rules_T: list, rules_F: list, filename: str = "txt.rules"):
    """
    Writes the true and false rules to a text file.
    
    Args:
        rules_T (list): List of rules that give True on the test.
        rules_F (list): List of rules that give False on the test.
        filename (str): Name of the text file to write the rules (default is "txt.rules").
    """
    with open(filename, 'w') as file:
        file.write("# Rules that give True on test\n")
        for rule in rules_T:
            file.write(rule + "\n")
        
        file.write("# Rules that give False on test\n")
        for rule in rules_F:
            file.write(rule + "\n")

# Define training sets
training_set_T = [[[1, 0, 0], [1, 0, 1], [0, 1, 0], [0, 1, 1]],
                  [[1, 0, 0], [0, 0, 1], [1, 0, 1], [1, 1, 0]],
                  [[1, 0, 0], [0, 0, 1], [0, 0, 0], [1, 1, 1]]]

training_set_F = [[[0, 0, 1], [0, 1, 0], [1, 0, 0], [1, 0, 1]],
                  [[0, 1, 0], [1, 0, 1], [0, 1, 0], [0, 1, 1]],
                  [[0, 1, 1], [1, 1, 0], [0, 1, 1], [0, 0, 0]]]

# Generate 20 rules that give True and 20 rules that give False
rules_T = []
rules_F = []

while len(rules_T) < 20 or len(rules_F) < 20:
    rule = GenRandomRule()
    if CheckRuleOnTrainingSet(rule, training_set_T, training_set_F):
        if len(rules_T) < 20:
            rules_T.append(rule)
    else:
        if len(rules_F) < 20:
            rules_F.append(rule)

# Write rules to file
WriteRulesToFile(rules_T, rules_F)
