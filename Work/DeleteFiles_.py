import os
def Delete_Files(input_nodes,input_slew,output_capacitance):
    for i in range(len(input_nodes)):
        for j in range(len(input_slew)):
            for k in range(len(output_capacitance)):
                filename = str(i)+str(j)+str(k)+".cir"
                os.remove("../Characterization/"+filename)
                print("Deleted file " + filename)
                os.remove(input_nodes[i]+"_"+input_slew[j] + "_" + output_capacitance[k] +  ".data")
                print("Deleted file " + input_nodes[i]+"_"+input_slew[j] + "_" + output_capacitance[k] +  ".data")
