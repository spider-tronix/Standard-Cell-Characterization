def Test_Pattern_Gen(logic_string,input_nodes,pulse_node):
    pulse_high = logic_string[:].replace(pulse_node,'1')
    pulse_low = logic_string[:].replace(pulse_node,'0')
    pattern_list = list()
    for i in range(2**(len(input_nodes))):
        a = bin(i).replace('0b','')
        while(len(a)<(len(input_nodes))):
            a = '0'+a
        pattern_list.append(a)
    pulse_low_list = list()
    pulse_high_list = list()
    input_nodes_floating = input_nodes[:]
    for i in range(len(pattern_list)):
        low = pulse_low[:]
        high = pulse_high[:]
        for j in range(len(input_nodes_floating)):
            low = low.replace(input_nodes_floating[j],pattern_list[i][j])
            high = high.replace(input_nodes_floating[j],pattern_list[i][j])
        pulse_low_list.append(low)
        pulse_high_list.append(high)
    print(pulse_low_list)
    print(pulse_high_list)
    for i in range(len(pulse_low_list)):
        result_low = Evaluate_Postfix(Infix_PostFix(pulse_low_list[i]))
        result_high = Evaluate_Postfix(Infix_PostFix(pulse_high_list[i]))
        if(result_low != result_high):
            print("Pattern Found")
            return pattern_list[i]

    return "No pattern Found"

def Infix_PostFix(logic_string):
    Operator_Stack = list()
    output = ''
    logic_string = logic_string.replace(' ','')
    for i in range(len(logic_string)):
        if logic_string[i].isnumeric() == True:
            output = output + logic_string[i]
        elif logic_string[i] == '(':
            Operator_Stack.append(logic_string[i])
        elif logic_string[i] == ')':
            while(Operator_Stack[len(Operator_Stack)-1] != '('):
                output = output + Operator_Stack.pop()
            Operator_Stack.pop()
        elif len(Operator_Stack) == 0 :
            Operator_Stack.append(logic_string[i])
        elif Operator_Stack[len(Operator_Stack)-1] == '(':
            Operator_Stack.append(logic_string[i])
        else : 
            output = output + Operator_Stack.pop()
            Operator_Stack.append(logic_string[i])
    while(len(Operator_Stack) != 0):
        output = output + Operator_Stack.pop()
    return output

def Evaluate_Postfix(string):
    Stack = list()
    result = 0 
    for i in range(len(string)):
        if string[i].isnumeric() == True:
            Stack.append(string[i])
        else:
            if string[i] == '&':
                result = int(Stack.pop()) & int(Stack.pop())
            elif string[i] == '|':
                result = int(Stack.pop()) | int(Stack.pop())
            elif string[i] == '!':
                result = int(Stack.pop()) ^ 1
            Stack.append(result)
    return result
