def Characterization_run(input_nodes,input_slew,output_capacitance,pulse_node,slew_lower_threshold,slew_upper_threshold,Vdd):
    filename = pulse_node+"_"+input_slew + "_" + output_capacitance +  ".data"
    #filename = "A_0.6n_0.1.data"
    file = open(filename,"r")
    vectors = file.read()
    vectors = vectors.split("\n")
    Vout = list()
    Vin = list()
    t = list()
    values = list()
    for i in range(len(vectors)):
        values_temp = vectors[i].split(" ")
        values = list()
        for j in range(len(values_temp)):
            if (len(values_temp[j])!=0):
                values.append(values_temp[j])
        try:
            t.append(float(values[0]))
        except:
            print("T Read complete")
        try:
            Vout.append(float(values[1]))
        except:
            print("Vout Read Complete")     
        try:
            Vin.append(float(values[3]))
        except:
            print("Vin Read Complete")
        values.clear()
        
    
    V_out_upper_threshold = (slew_upper_threshold/100)*Vdd
    V_out_lower_threshold = (slew_lower_threshold/100)*Vdd
    V_out_mid_threshold = 0.5*Vdd

    V_out_upper_line = list()
    V_out_upper_line_slope = list()
    V_out_lower_line = list()
    V_out_lower_line_slope = list()
    V_out_mid_line = list()
    V_out_mid_line_slope = list()

    for i in range(len(Vout)):
        if(abs(Vout[i] - V_out_upper_threshold)<0.1):
            V_out_upper_line.append(i)
            if(Vout[i]-Vout[i-1]<0):
                V_out_upper_line_slope.append(-1)
            else:
                V_out_upper_line_slope.append(1)
            #print(str(V_out_upper_threshold) + " " + str(Vout[i]))
        if(abs(Vout[i] - V_out_lower_threshold)<0.1):
            V_out_lower_line.append(i)
            if(Vout[i]-Vout[i-1]<0):
                V_out_lower_line_slope.append(-1)
            else:
                V_out_lower_line_slope.append(1)
        if(abs(Vout[i] - V_out_mid_threshold)<0.1):
            V_out_mid_line.append(i)
            if(Vout[i]-Vout[i-1]<0):
                V_out_mid_line_slope.append(-1)
            else:
                V_out_mid_line_slope.append(1)

##                
##            print(str(V_out_upper_threshold) + " " + str(Vout[i]))
##            print(str(V_out_lower_threshold) + " " + str(Vout[i]))
            
##    print(V_out_upper_line)
##    print(V_out_upper_line_slope)
##    print(V_out_lower_line)
##    print(V_out_lower_line_slope)

    i = 1
    while(i<len(V_out_upper_line)):
        if(V_out_upper_line_slope[i-1]==V_out_upper_line_slope[i]):
            if(Vout[V_out_upper_line[i]]-V_out_upper_threshold > Vout[V_out_upper_line[i-1]]-V_out_upper_threshold):
                V_out_upper_line.pop(i)
                V_out_upper_line_slope.pop(i)
            else:
                V_out_upper_line.pop(i-1)
                V_out_upper_line_slope.pop(i-1)
        else:
            i=i+1
            
    i = 1
    while(i<len(V_out_lower_line)):
        if(V_out_lower_line_slope[i-1]==V_out_lower_line_slope[i]):
            if(Vout[V_out_lower_line[i]]-V_out_lower_threshold > Vout[V_out_lower_line[i-1]]-V_out_lower_threshold):
                V_out_lower_line.pop(i)
                V_out_lower_line_slope.pop(i)
            else:
                V_out_lower_line.pop(i-1)
                V_out_lower_line_slope.pop(i-1)
        else:
            i=i+1

    i = 1
    while(i<len(V_out_mid_line)):
        if(V_out_mid_line_slope[i-1]==V_out_mid_line_slope[i]):
            if(Vout[V_out_mid_line[i]]-V_out_mid_threshold > Vout[V_out_mid_line[i-1]]-V_out_mid_threshold):
                V_out_mid_line.pop(i)
                V_out_mid_line_slope.pop(i)
            else:
                V_out_mid_line.pop(i-1)
                V_out_mid_line_slope.pop(i-1)
        else:
            i=i+1


##
##    print("filtered Values")
##    print("V_out_upper")
##    print(V_out_upper_line)
##    print(V_out_upper_line_slope)
##    print("V_out_mid")
##    print(V_out_mid_line)
##    print(V_out_mid_line_slope)
##    print("V_out_lower")
##    print(V_out_lower_line)
##    print(V_out_lower_line_slope)

    V_in_mid_line = list()
    V_in_mid_line_slope = list()
    V_in_mid_threshold = 0.5*Vdd

    for i in range(len(Vin)):
        if(abs(Vin[i] - V_in_mid_threshold)<0.1):
            V_in_mid_line.append(i)
            if(Vin[i]-Vin[i-1]<0):
                V_in_mid_line_slope.append(-1)
            else:
                V_in_mid_line_slope.append(1)


    i = 1
    while(i<len(V_in_mid_line)):
        if(V_in_mid_line_slope[i-1]==V_in_mid_line_slope[i]):
            if(Vin[V_in_mid_line[i]]-V_in_mid_threshold > Vin[V_in_mid_line[i-1]]-V_in_mid_threshold):
                V_in_mid_line.pop(i)
                V_in_mid_line_slope.pop(i)
            else:
                V_in_mid_line.pop(i-1)
                V_in_mid_line_slope.pop(i-1)
        else:
            i=i+1
        
##    print("V_in_Mid")
##    print(V_in_mid_line)
##    print(V_in_mid_line_slope)
    t_rise = list()
    t_fall = list()
    t_temp_1 = 0
    t_temp_2 = 0



    ## Find Output Rise and Fall Delay
    for i in range(len(V_out_upper_line_slope)):
        
        ## Fall
        if (V_out_upper_line_slope[i] == -1):
    ##        if Vout[V_out_upper_line[i]] >  V_out_upper_threshold :
    ##            t_temp_1 = t[i] + (V_out_upper_threshold - Vout[V_out_upper_line[i]])*(t[V_out_upper_line[i]+1]-t[V_out_upper_line[i]])/(Vout[V_out_upper_line[i]+1]-Vout[V_out_upper_line[i]])
    ##        else :
    ##            t_temp_1 = t[i] + (V_out_upper_threshold - Vout[V_out_upper_line[i]])*(t[V_out_upper_line[i]-1]-t[V_out_upper_line[i]])/(Vout[V_out_upper_line[i]-1]-Vout[V_out_upper_line[i]])
    ##
    ##        if Vout[V_out_lower_line[i]] >  V_out_lower_threshold :
    ##            t_temp_2 = t[i] + (V_out_lower_threshold - Vout[V_out_lower_line[i]])*(t[V_out_lower_line[i]+1]-t[V_out_lower_line[i]])/(Vout[V_out_lower_line[i]+1]-Vout[V_out_lower_line[i]])
    ##        else :
    ##            t_temp_2 = t[i] + (V_out_lower_threshold - Vout[V_out_lower_line[i]])*(t[V_out_lower_line[i]-1]-t[V_out_lower_line[i]])/(Vout[V_out_lower_line[i]-1]-Vout[V_out_lower_line[i]])
    ##        t_fall.append(t_temp_2-t_temp_1)
            t_fall.append(t[V_out_lower_line[i]]-t[V_out_upper_line[i]]) 
            
        ## Rise
        else:
    ##        if Vout[V_out_upper_line[i]] >  V_out_upper_threshold :
    ##            t_temp_1 = t[i] + (V_out_upper_threshold - Vout[V_out_upper_line[i]])*(t[V_out_upper_line[i]-1]-t[V_out_upper_line[i]])/(Vout[V_out_upper_line[i]-1]-Vout[V_out_upper_line[i]])
    ##        else:
    ##            t_temp_1 = t[i] + (V_out_upper_threshold - Vout[V_out_upper_line[i]])*(t[V_out_upper_line[i]+1]-t[V_out_upper_line[i]])/(Vout[V_out_upper_line[i]+1]-Vout[V_out_upper_line[i]])
    ##
    ##        if Vout[V_out_lower_line[i]] >  V_out_lower_threshold :
    ##            t_temp_2 = t[i] + (V_out_lower_threshold - Vout[V_out_lower_line[i]])*(t[V_out_lower_line[i]-1]-t[V_out_lower_line[i]])/(Vout[V_out_lower_line[i]-1]-Vout[V_out_lower_line[i]])
    ##        else :
    ##            t_temp_2 = t[i] + (V_out_lower_threshold - Vout[V_out_lower_line[i]])*(t[V_out_lower_line[i]+1]-t[V_out_lower_line[i]])/(Vout[V_out_lower_line[i]+1]-Vout[V_out_lower_line[i]])
    ##        t_rise.append(t_temp_1-t_temp_2)
            t_rise.append(t[V_out_upper_line[i]]-t[V_out_lower_line[i]] ) 
            

##    print("T fall Output")
##    print(t_fall)
##    print("T rise Output")
##    print(t_rise)
    try:
        output_rise_time  = sum(t_rise)/len(t_rise)
    except:
        print(filename)
    output_fall_time  = sum(t_fall)/len(t_fall)

##    print("Output Rise Time in ns : ")
##    print(output_rise_time*10**9)
##    print("Output Fall Time in ns : ")
##    print(output_fall_time*10**9)

    t_cell_rise = list()
    t_cell_fall = list()
    t_temp_1 = 0
    t_temp_2 = 0

    ## Find Cell Rise and Cell Fall Delay
    for i in range(len(V_in_mid_line_slope)):
        ## Fall
        if (V_out_mid_line_slope[i] == -1):
            t_cell_fall.append(t[V_out_mid_line[i]]-t[V_in_mid_line[i]])
        else:
            t_cell_rise.append(t[V_out_mid_line[i]]-t[V_in_mid_line[i]])

##    print("Cell Fall delay")
##    print(t_cell_fall)
##    print("Cell Rise delay")
##    print(t_cell_rise)

    cell_rise_time = sum(t_cell_rise)/len(t_cell_rise)
    cell_fall_time = sum(t_cell_fall)/len(t_cell_fall)

##    print("Cell rise delay")
##    print(cell_rise_time)
##    print("Cell fall delay")
##    print(cell_fall_time)

    return [cell_rise_time*(10**9),cell_fall_time*(10**9),output_rise_time*(10**9),output_fall_time*(10**9)]
