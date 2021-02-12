import NodeVoltages_ as nv
def Netlist_Build(output_nodes,input_nodes,Pulse_Node,input_slew,output_capacitance,Time_Period,Vdd,source_circuit,logic_string):
    
    print ("\n for input " + Pulse_Node +  " vs " + " output node Y\n" )
    temp_circuit = source_circuit[:]
    temp_circuit.append("CL " + output_nodes[0] + " " + "0 " + output_capacitance + "F")
    
    ## Pulsating Node :  Syntax 	 PULSE(V1 V2 TD TR TF PW PER) Ex : V2 A 0 PULSE(0 1.8 0 0 0 5 10)
    ## V2 A 0 PULSE(0 1.8 0 0.06n 0.06n 10.0n 20n)
    temp_circuit.append("V2 " + Pulse_Node + " 0" + " PULSE(0 " + str(Vdd) + " 0 " +  input_slew + " "  + input_slew + " " + str(Time_Period/2) + "n " + str(Time_Period) + "n)")
    
    ## other input nodes
    k=3
    Vnodes = nv.Test_Pattern_Gen(logic_string,input_nodes,Pulse_Node)
    for i in range(len(input_nodes)):
        if(Vnodes[i]=='0'):
            temp_circuit.append("V" + str(k) + " " + input_nodes[i] + " 0 0")
        else:
            temp_circuit.append("V" + str(k) + " " + input_nodes[i] + " 0 " + str(Vdd))
        k = k + 1
        
    ## Add .tran command
    temp_circuit.append(".tran 0.001n 50n")

    ## Add control commands
    temp_circuit.append(".control")
    temp_circuit.append("run")
    temp_circuit.append("wrdata "+Pulse_Node+"_"+input_slew + "_" + output_capacitance +  ".data" + " v(Y) " + "v(" +  Pulse_Node + ")")
    temp_circuit.append(".endc")
    ## Add .end command 
    temp_circuit.append(".end")
    
    ## Concatenate all Values
    result = ''
    for l in range(len(temp_circuit)):
        result = result + "\n" + temp_circuit[l]
##    print(result)

    ## Return Result
    return result

