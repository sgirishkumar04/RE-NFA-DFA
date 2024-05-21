import graphviz
import collections
import json

def prepareForDrawing(states, end_state, prev_start):
    # make the last state as out state
    states["S" + str(end_state)]["terminalState"] = True
    # sort the state ascending
    states = collections.OrderedDict(sorted(states.items()))
    # loop over sorted states and save them as the given example to json file
    # return the json file content to be displayed in graph format
    states.update({"startingState": ("S" + str(prev_start))})
    with open('out/nfa.json', 'w') as fp:
        json.dump(states, fp, ensure_ascii=True)
    print(states)
    return states

def construct_node(state, nfa, starting_state, graph):
    # construct a graph node using given state
    # check whether state is terminal to draw double circle
    if nfa[state]['terminalState']:
        graph.node(state, label=state, shape='doublecircle')
    else:
        graph.node(state, label=state, shape='circle')
    # check whether state is starting to draw input arrow
    if state == starting_state:
        graph.edge('start', state)

def visualize(nfa):
    # visualize output NFA into a directed graph
    # initialize directed graph
    graph = graphviz.Digraph(comment='NFA Visualization')
    # set graph flow from left to right
    graph.graph_attr['rankdir'] = 'LR'
    # set entry point
    graph.node('start', label='start', shape='plaintext')
    # get the starting state of NFA
    starting_state = nfa['startingState']
    del nfa['startingState']
    # initialize nodes list
    nodes = list()
    # loop over each NFA state
    for state in nfa:
        # check whether state is created or not
        if not state in nodes:
            # add state to created nodes
            nodes.append(state)
            # construct a graph node for the state
            construct_node(state, nfa, starting_state, graph)
        # loop over each successor state
        for successor in nfa[state]:
            # skip 'terminalstate' key
            if successor != 'terminalState':
                # check whether successor state is created or not
                if nfa[state][successor] in nodes:
                    # create an edge between two states
                    graph.edge(state, nfa[state][successor], label=successor)
                else:
                    # add state to created nodes
                    nodes.append(nfa[state][successor])
                    # construct a graph node for the state
                    construct_node(nfa[state][successor], nfa, starting_state, graph)
                    # create an edge between two states
                    graph.edge(state, nfa[state][successor], label=successor)
    # set output format to SVG
    graph.format = 'svg'
    # render final graph
    graph.render('out/nfa-graph', view=False)

class NFA:
    def __init__(self, no_state, states, no_alphabet, alphabets, start,
                 no_final, finals, no_transition, transitions):
        self.no_state = no_state
        self.states = states
        self.no_alphabet = no_alphabet
        self.alphabets = alphabets

        # Adding epsilon alphabet to the list
        # and incrementing the alphabet count
        self.alphabets.append('e')
        self.no_alphabet += 1
        self.start = start
        self.no_final = no_final
        self.finals = finals
        self.no_transition = no_transition
        self.transitions = transitions
        self.graph = graphviz.Digraph()

        # Dictionaries to get index of states or alphabets
        self.states_dict = dict()
        for i in range(self.no_state):
            self.states_dict[self.states[i]] = i
        self.alphabets_dict = dict()
        for i in range(self.no_alphabet):
            self.alphabets_dict[self.alphabets[i]] = i

        # transition table is of the form
        # [From State + Alphabet pair] -> [Set of To States]
        self.transition_table = dict()
        for i in range(self.no_state):
            for j in range(self.no_alphabet):
                self.transition_table[str(i) + str(j)] = []
        for i in range(self.no_transition):
            self.transition_table[str(self.states_dict[self.transitions[i][0]])
                                  + str(self.alphabets_dict[
                                      self.transitions[i][1]])].append(
                self.states_dict[self.transitions[i][2]])

    # Method to get input from User
    @classmethod
    def fromUser(cls):
        with open("output.json", 'r') as file:
            nfa_json = json.load(file)
            
        no_state = nfa_json["no_state"]
        states = nfa_json["states"]
        no_alphabet = nfa_json["no_alphabet"]
        alphabets = nfa_json["alphabets"]
        start = nfa_json["start"]
        no_final = nfa_json["no_final"]
        finals = nfa_json["finals"]
        no_transition = nfa_json["no_transition"]
        transitions = nfa_json["transitions"]
        return cls(no_state, states, no_alphabet, alphabets, start,
                   no_final, finals, no_transition, transitions)

    # Method to represent quintuple
    def __repr__(self):
        return "Q : " + str(self.states) + "\nΣ : " + str(self.alphabets) + "\nq0 : " + str(self.start) + "\nF : " + str(
            self.finals) + "\nδ : \n" + str(self.transition_table)

    def getEpsilonClosure(self, state):

        # Method to get Epsilon Closure of a state of NFA
        # Make a dictionary to track if the state has been visited before
        # And a array that will act as a stack to get the state to visit next
        closure = dict()
        closure[self.states_dict[state]] = 0
        closure_stack = [self.states_dict[state]]

        # While stack is not empty the loop will run
        while (len(closure_stack) > 0):

            # Get the top of stack that will be evaluated now
            cur = closure_stack.pop(0)

            # For the epsilon transition of that state,
            # if not present in closure array then add to dict and push to stack
            for x in self.transition_table[
                str(cur) + str(self.alphabets_dict['e'])]:
                if x not in closure.keys():
                    closure[x] = 0
                    closure_stack.append(x)
            closure[cur] = 1
        return closure.keys()

    def getStateName(self, state_list):
        if -1 in state_list:
            return 'ϕ'
        else:
            # Get name from set of states to display in the final DFA diagram
            name = ''
            for x in state_list:
                name += self.states[x]
            return name

    def isFinalDFA(self, state_list):

        # Method to check if the set of state is final state in DFA
        # by checking if any of the set is a final state in NFA
        for x in state_list:
            for y in self.finals:
                if (x == self.states_dict[y]):
                    return True
        return False


print("E-NFA to DFA")

# Uncomment the following two lines to get input from the user
# nfa = NFA.fromUser() # To get input from user
# print(repr(nfa)) # To print the quintuple in console

# Uncomment the following two lines to get input from the user
nfa = NFA.fromUser()  # To get input from user
print(repr(nfa))  # To print the quintuple in console

# Making an object of Digraph to visualize NFA diagram
nfa.graph = graphviz.Digraph()

# Adding states/nodes in NFA diagram
for x in nfa.states:
    # If state is not a final state, then border shape is single circle
    # Else it is double circle
    if (x not in nfa.finals):
        nfa.graph.attr('node', shape='circle')
        nfa.graph.node(x)
    else:
        nfa.graph.attr('node', shape='doublecircle')
        nfa.graph.node(x)

# Adding start state arrow in NFA diagram
nfa.graph.attr('node', shape='none')
nfa.graph.node('')
nfa.graph.edge('', nfa.start)

# Adding edge between states in NFA from the transitions array
for x in nfa.transitions:
    nfa.graph.edge(x[0], x[2], label=('ε', x[1])[x[1] != 'e'])

# Makes a pdf with name nfa.graph.pdf and views the pdf
nfa.graph.render('nfa', view=True)

# Making an object of Digraph to visualize DFA diagram
dfa = graphviz.Digraph()

# Finding epsilon closure beforehand so to not recalculate each time
epsilon_closure = dict()
for x in nfa.states:
    epsilon_closure[x] = list(nfa.getEpsilonClosure(x))

# First state of DFA will be epsilon closure of start state of NFA
# This list will act as stack to maintain till when to evaluate the states
dfa_stack = list()
dfa_stack.append(epsilon_closure[nfa.start])

# Check if start state is the final state in DFA
if (nfa.isFinalDFA(dfa_stack[0])):
    dfa.attr('node', shape='doublecircle')
else:
    dfa.attr('node', shape='circle')
dfa.node(nfa.getStateName(dfa_stack[0]))

# Adding start state arrow to start state in DFA
dfa.attr('node', shape='none')
dfa.node('')
dfa.edge('', nfa.getStateName(dfa_stack[0]))

# List to store the states of DFA
dfa_states = list()
dfa_states.append(epsilon_closure[nfa.start])

# Loop will run till this stack is not empty
while (len(dfa_stack) > 0):
    # Getting top of the stack for current evaluation
    cur_state = dfa_stack.pop(0)

    # Traversing through all the alphabets for evaluating transitions in DFA
    for al in range((nfa.no_alphabet) - 1):
        # Set to see if the epsilon closure of the set is empty or not
        from_closure = set()
        for x in cur_state:
            # Performing Union update and adding all the new states in set
            from_closure.update(
                set(nfa.transition_table[str(x) + str(al)]))

        # Check if epsilon closure of the new set is not empty
        if (len(from_closure) > 0):
            # Set for the To state set in DFA
            to_state = set()
            for x in list(from_closure):
                to_state.update(set(epsilon_closure[nfa.states[x]]))

            # Check if the to state already exists in DFA and if not then add it
            if list(to_state) not in dfa_states:
                dfa_stack.append(list(to_state))
                dfa_states.append(list(to_state))

                # Check if this set contains final state of NFA
                # to get if this set will be final state in DFA
                if (nfa.isFinalDFA(list(to_state))):
                    dfa.attr('node', shape='doublecircle')
                else:
                    dfa.attr('node', shape='circle')
                dfa.node(nfa.getStateName(list(to_state)))

            # Adding edge between from state and to state
            dfa.edge(nfa.getStateName(cur_state),
                     nfa.getStateName(list(to_state)),
                     label=nfa.alphabets[al])

        # Else case for empty epsilon closure
        # This is a dead state(ϕ) in DFA
        else:

            # Check if any dead state was present before this
            # if not then make a new dead state ϕ
            if (-1) not in dfa_states:
                dfa.attr('node', shape='circle')
                dfa.node('ϕ')

                # For new dead state, add all transitions to itself,
                # so that machine cannot leave the dead state
                for alpha in range(nfa.no_alphabet - 1):
                    dfa.edge('ϕ', 'ϕ', nfa.alphabets[alpha])

                # Adding -1 to list to mark that dead state is present
                dfa_states.append(-1)

            # Adding transition to dead state
            dfa.edge(nfa.getStateName(cur_state, ),
                     'ϕ', label=nfa.alphabets[al])

# Makes a pdf with name dfa.pdf and views
dfa.render('dfa', view=True)

# Display transition table for DFA
print("\nTransition Table for DFA:")
print("{:<10} |".format(""), end="")
for alphabet in nfa.alphabets[:-1]:
    print("{:<10} |".format(alphabet), end="")
print("\n" + "-" * (12 * len(nfa.alphabets)))

# Print each row of the transition table
for state_index, state in enumerate(dfa_states):
    if state == -1:
        # Skip printing transitions for the dead state
        continue

    print("{:<10} |".format(nfa.getStateName(state)), end="")
    for alphabet_index in range(nfa.no_alphabet - 1):
        alphabet = nfa.alphabets[alphabet_index]
        from_closure = set()
        for x in state:
            from_closure.update(
                set(nfa.transition_table[str(x) + str(alphabet_index)]))
        to_state = set()
        for x in list(from_closure):
            to_state.update(set(epsilon_closure[nfa.states[x]]))
        
        # Check if the to_state is the dead state 'ϕ'
        if len(to_state) == 0:
            print("{:<10} |".format('ϕ'), end="")
        else:
            print("{:<10} |".format(nfa.getStateName(to_state)), end="")
    print()

# Display transition functions for each state in the DFA
for state_index, state in enumerate(dfa_states):
    # Skip printing transitions for the dead state
    if state == -1:
        continue

    # Print transition functions for each alphabet
    for alphabet_index in range(nfa.no_alphabet - 1):
        alphabet = nfa.alphabets[alphabet_index]
        from_closure = set()
        for x in state:
            from_closure.update(
                set(nfa.transition_table[str(x) + str(alphabet_index)]))
        to_state = set()
        for x in list(from_closure):
            to_state.update(set(epsilon_closure[nfa.states[x]]))
        
        # Format the state names for printing
        from_state_name = nfa.getStateName(state)
        to_state_name = nfa.getStateName(to_state) if len(to_state) > 0 else 'ϕ'

        # Split state names by comma, sort them, and join them
        from_state_name = ','.join(sorted(from_state_name.split(',')))
        to_state_name = ','.join(sorted(to_state_name.split(',')))


        # Print the transition function
        print(f"The δ' transition for state {from_state_name} is obtained as:")
        print(f"δ'({from_state_name}, {alphabet}) = {to_state_name}")

    # Add a newline for clarity
    print()
