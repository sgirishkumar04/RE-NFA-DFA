import json
import sys
from graphviz import Digraph

non_symbols = ['+', '*', '.', '(', ')']
nfa = {}

class charType:
    SYMBOL = 1
    CONCAT = 2
    UNION  = 3
    KLEENE = 4

class NFAState:
    def __init__(self):
        self.next_state = {}

class ExpressionTree:
    def __init__(self, charType, value=None):
        self.charType = charType
        self.value = value
        self.left = None
        self.right = None

def make_exp_tree(regexp):
    stack = []
    for c in regexp:
        if c == "+":
            z = ExpressionTree(charType.UNION)
            z.right = stack.pop()
            z.left = stack.pop()
            stack.append(z)
        elif c == ".":
            z = ExpressionTree(charType.CONCAT)
            z.right = stack.pop()
            z.left = stack.pop()
            stack.append(z)
        elif c == "*":
            z = ExpressionTree(charType.KLEENE)
            z.left = stack.pop() 
            stack.append(z)
        elif c == "(" or c == ")":
            continue  
        else:
            stack.append(ExpressionTree(charType.SYMBOL, c))
    return stack[0]

def compPrecedence(a, b):
    p = ["+", ".", "*"]
    return p.index(a) > p.index(b)

def compute_regex(exp_t):
    # returns E-NFA
    if exp_t.charType == charType.CONCAT:
        return do_concat(exp_t)
    elif exp_t.charType == charType.UNION:
        return do_union(exp_t)
    elif exp_t.charType == charType.KLEENE:
        return do_kleene_star(exp_t)
    else:
        return eval_symbol(exp_t)

def eval_symbol(exp_t):
    start = NFAState()
    end = NFAState()
    start.next_state[exp_t.value] = [end]
    return start, end

def do_concat(exp_t):
    left_nfa  = compute_regex(exp_t.left)
    right_nfa = compute_regex(exp_t.right)
    left_nfa[1].next_state['e'] = [right_nfa[0]]  # Replace '$' with 'e'
    return left_nfa[0], right_nfa[1]

def do_union(exp_t):
    start = NFAState()
    end = NFAState()
    first_nfa = compute_regex(exp_t.left)
    second_nfa = compute_regex(exp_t.right)
    start.next_state['e'] = [first_nfa[0], second_nfa[0]]  # Replace '$' with 'e'
    first_nfa[1].next_state['e'] = [end]  # Replace '$' with 'e'
    second_nfa[1].next_state['e'] = [end]  # Replace '$' with 'e'
    return start, end

def do_kleene_star(exp_t):
    start = NFAState()
    end = NFAState()
    starred_nfa = compute_regex(exp_t.left)
    start.next_state['e'] = [starred_nfa[0], end]  # Replace '$' with 'e'
    starred_nfa[1].next_state['e'] = [starred_nfa[0], end]  # Replace '$' with 'e'
    return start, end

def arrange_transitions(state, states_done, symbol_table):
    global nfa
    if state in states_done:
        return
    states_done.append(state)
    for symbol in list(state.next_state):
        if symbol not in nfa['letters']:
            nfa['letters'].append(symbol)
        for ns in state.next_state[symbol]:
            if ns not in symbol_table:
                symbol_table[ns] = sorted(symbol_table.values())[-1] + 1
                q_state = "q" + str(symbol_table[ns])  # Change state to lowercase
                nfa['states'].append(q_state)
            nfa['transition_function'].append(["q" + str(symbol_table[state]), 'e' if symbol == '$' else symbol, "q" + str(symbol_table[ns])])  # Replace '$' with 'e'
        for ns in state.next_state[symbol]:
            arrange_transitions(ns, states_done, symbol_table)

def notation_to_num(str):
    return int(str[1:])

def final_st_dfs():
    global nfa
    for st in nfa["states"]:
        count = 0
        for val in nfa['transition_function']:
            if val[0] == st and val[2] != st:
                count += 1
        if count == 0 and st not in nfa["final_states"]:
            nfa["final_states"].append(st)

def arrange_nfa(fa):
    global nfa
    nfa['states'] = []
    nfa['letters'] = []
    nfa['transition_function'] = []
    nfa['start_states'] = []
    nfa['final_states'] = []
    q_1 = "q" + str(1)  # Change state to lowercase
    nfa['states'].append(q_1)
    arrange_transitions(fa[0], [], {fa[0] : 1})
    st_num = [notation_to_num(i) for i in nfa['states']]
    nfa["start_states"].append("q1")  # Change state to lowercase
    final_st_dfs()

def add_concat(regex):
    global non_symbols
    l = len(regex)
    res = []
    for i in range(l - 1):
        res.append(regex[i])
        if regex[i] not in non_symbols:
            if regex[i + 1] not in non_symbols or regex[i + 1] == '(':
                res += '.'
        if regex[i] == ')' and regex[i + 1] == '(':
            res += '.'
        if regex[i] == '*' and regex[i + 1] == '(':
            res += '.'
        if regex[i] == '*' and regex[i + 1] not in non_symbols:
            res += '.'
        if regex[i] == ')' and regex[i + 1] not in non_symbols:
            res += '.'

    res += regex[l - 1]
    return res

def compute_postfix(regexp):
    stk = []
    res = ""
    for c in regexp:
        if c not in non_symbols or c == "*":
            res += c
        elif c == ")":
            while len(stk) > 0 and stk[-1] != "(":
                res += stk.pop()
            stk.pop()
        elif c == "(":
            stk.append(c)
        elif len(stk) == 0 or stk[-1] == "(" or compPrecedence(c, stk[-1]):
            stk.append(c)
        else:
            while len(stk) > 0 and stk[-1] != "(" and not compPrecedence(c, stk[-1]):
                res += stk.pop()
            stk.append(c)
    while len(stk) > 0:
        res += stk.pop()
    return res

def polish_regex(regex):
    reg = add_concat(regex)
    regg = compute_postfix(reg)
    return regg

def load_regex():
    with open(sys.argv[1], 'r') as inpjson:
        regex = json.loads(inpjson.read())
    return regex

def draw_nfa_graph():
    global nfa
    dot = Digraph()
    dot.attr(rankdir='LR')
    dot.node('start', shape='point')
    dot.edge('start', nfa["start_states"][0])
    for transition in nfa['transition_function']:
        dot.edge(transition[0], transition[2], label=transition[1])
    for state in nfa["final_states"]:
        dot.node(state, shape='doublecircle')
    dot.render('nfa_graph', format='png', cleanup=True)


    

def output_nfa_to_json(filename):
    global nfa
    states = nfa['states']
    transition_function = nfa['transition_function']
    start_states = nfa['start_states']
    final_states = nfa['final_states']
    letters = nfa['letters']

    # Convert states to lowercase and replace '$' with 'e'
    states = [state.lower() for state in states]
    start_states = [state.lower() for state in start_states]
    final_states = [state.lower() for state in final_states]
    transition_function = [[s[0].lower(), 'e' if s[1] == '$' else s[1], s[2].lower()] for s in transition_function]

    # Construct the dictionary
    nfa_dict = {
        "no_state": len(states),
        "states": states,
        "no_alphabet": len(letters),
        "alphabets": letters,
        "start": start_states[0],
        "no_final": len(final_states),
        "finals": final_states,
        "no_transition": len(transition_function),
        "transitions": transition_function
    }

    # Write the dictionary to a JSON file
    with open(filename, 'w') as json_file:
        json.dump(nfa_dict, json_file, indent=2)


def load_regex_from_input():
    regex = input("Enter RE:")
    return {"regex": regex}

if __name__ == "__main__":
    r = load_regex_from_input()
    reg = r['regex']
    
    pr = polish_regex(reg)
    et = make_exp_tree(pr)
    fa = compute_regex(et)
    arrange_nfa(fa)
    
    output_filename = "output.json"
    
    output_nfa_to_json(output_filename)
