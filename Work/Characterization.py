import subprocess
import os
import csv
import openpyxl
import openpyxl_ as xl
import NodeVoltages_ as nv
import NetlistBuilder_ as nb

import Characterize_ as Characterize
import DeleteFiles_ as delete
def NgSpice_Run(input_nodes,input_slew,output_capacitance):
    for i in range(len(input_nodes)):
        for j in range(len(input_slew)):
            for k in range(len(output_capacitance)):
                try:
                    filename = str(i)+str(j)+str(k)+".cir"
                    command = "ngspice -b ../Characterization/" + filename 
                    subprocess.check_call(command,shell=True)
                    #a = subprocess.check_output(['ngspice', '-b', filename], shell=True). subprocess.check_call()
                except:
                    print(filename + " spice file executed")
                    
    print("NGSpice Simulation Runs Successfully completed")
    
##---- Main Function----##
                
def main():

        ##----List The spice files in the directory and get the choice----##
    Netlists_Total = os.listdir("../Characterization/Netlists")
    i = 1 
    while(i<len(Netlists_Total)):
        if(Netlists_Total[i].endswith(".cir")) == False:
            Netlists_Total.pop(i)
        else:
            i=i+1
    for i in range(len(Netlists_Total)):
        print( str(i) + " : " + Netlists_Total[i])
    print("\n")
    choice = input("Enter the index of the circuit to be characterised \n")
    choice_file = Netlists_Total[int(choice)]
    input_read_file = choice_file.split(".")[0]

    logic_string = ''
    input_nodes = list()
    output_nodes = list()
    Vdd = 0
    T = 0
    input_slew = list()
    output_capacitance = list()
    slew_lower_threshold = 0
    slew_upper_threshold = 0

    [logic_string,input_nodes,output_nodes,Vdd,T,input_slew,output_capacitance,slew_lower_threshold,slew_upper_threshold] = xl.Read_input(input_read_file)

    print("Input slew Checking :    ")
    print(input_slew)
    ##-----Processing Netlist-----##
    f = open("../Characterization/Netlists/"+ choice_file, "r")
    circuit = f.read()
    circuit = circuit.split("\n")
    circuit.remove(".end")
    circuit.append("\nV1 Vdd 0 " + str(Vdd))
    source_circuit = circuit
    temp_circuit = list()
    cir = ''
    print("Source Circuit Read")
    print("Building Netlists")
    in_nodes = list()
    input_slew_original = list()

    slew_adjustment = 100/(slew_upper_threshold - slew_lower_threshold)
    for i in range(len(input_slew)):
        input_slew_original.append(str( slew_adjustment*float(input_slew[i][:-1]))+'n')

    print(input_slew_original)
    print(slew_upper_threshold)
    ##----- Create Netlists for all different combinations-----##
    for i in range(len(input_nodes)):
        for j in range(len(input_slew)):
            for k in range(len(output_capacitance)):
                in_nodes = input_nodes[:]
                in_nodes.remove(input_nodes[i])
                cir = nb.Netlist_Build(output_nodes,in_nodes,input_nodes[i],input_slew_original[j],output_capacitance[k],T,Vdd,source_circuit,logic_string)
                file = open("../Characterization/"+str(i)+str(j)+str(k)+".cir", "w")
                print("Netlist Build For " + str(i)+str(j)+str(k)+".cir" + " Complete ")
                file.write(cir)
                file.close()

    print("Netlists Built Successfully for all different combinations")

    print("Running Simulations")

    NgSpice_Run(input_nodes,input_slew,output_capacitance)
                
    Timing = [["cell_rise_time (ns)","cell_fall_time (ns)","output_rise_time (ns)","output_fall_time (ns)"]]

    print(" Characterization Algorithm beginning ... ")
    print(" Analyzing Data files ")
    m=1
    file = open("../Characterization/" + input_read_file+ "Characterisation Results" + ".txt", "w")
    string = ''
    rise_transition = list()
    cell_rise = list()
    fall_transition = list()
    cell_fall = list()


    for i in range(len(input_nodes)):
        for j in range(len(input_slew)):
            for k in range(len(output_capacitance)):
                Timing.append(Characterize.Characterization_run(input_nodes,input_slew_original[j],output_capacitance[k],input_nodes[i],slew_lower_threshold,slew_upper_threshold,Vdd))
                cell_rise.append(Timing[m][0])
                cell_fall.append(Timing[m][1])
                rise_transition.append(Timing[m][2])
                fall_transition.append(Timing[m][3])
                file.write(str(m) + ". Input Node : " + input_nodes[i] + " Input Slew : " + input_slew[j] + " Output Capacitance : " + output_capacitance[k])
                file.write("\n")
                file.write(str(Timing[0]))
                file.write("\n")
                file.write(str(Timing[m]))
                file.write("\n")
                file.write("\n")
                m = m+1
    x = 0
    file.close()
    workbook = openpyxl.Workbook()
    ##    name,workbook,input_nodes,output_capacitance,input_slew
    print("Input Slew Checking :    ")
    print(input_slew)
    xl.Excel_writer(" rise_transition ",workbook,input_nodes,output_capacitance,input_slew,rise_transition)
    xl.Excel_writer(" cell_rise  ",workbook,input_nodes,output_capacitance,input_slew,cell_rise)
    xl.Excel_writer(" fall_transition  ",workbook,input_nodes,output_capacitance,input_slew,fall_transition)
    xl.Excel_writer(" cell_fall  ",workbook,input_nodes,output_capacitance,input_slew,cell_fall)
    delete.Delete_Files(input_nodes,input_slew_original,output_capacitance,)
    workbook.save("../Characterization/"+input_read_file + ' Characterisation Results.xlsx')

    
if __name__ == "__main__":
    main()
    
