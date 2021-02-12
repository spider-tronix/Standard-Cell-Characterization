import openpyxl
from openpyxl.styles import Font
def Read_input(filename):
    book = openpyxl.load_workbook("../Characterization/Netlists/" +filename + ".xlsx")
    sheet = book.active
    logic_string = sheet['B1'].value

    input_nodes = list()
    row = 2
    column = 'B'
    while(sheet[column+str(row)].value != None):
        input_nodes.append(sheet[column+str(row)].value)
        column = chr(ord(column)+1)

    output_nodes = list()
    row = 3
    column = 'B'
    while(sheet[column+str(row)].value != None):
        output_nodes.append(sheet[column+str(row)].value)
        column = chr(ord(column)+1)

    Vdd = sheet['B4'].value
    T = sheet['B5'].value

    input_slew = list()
    row = 6
    column = 'B'
    while(sheet[column+str(row)].value != None):
        input_slew.append(sheet[column+str(row)].value)
        column = chr(ord(column)+1)

    output_capacitance = list()
    row = 7
    column = 'B'
    while(sheet[column+str(row)].value != None):
        output_capacitance.append(sheet[column+str(row)].value)
        column = chr(ord(column)+1)

    slew_lower_threshold = sheet['B8'].value
    slew_upper_threshold =  sheet['B9'].value

    return [logic_string,input_nodes,output_nodes,Vdd,T,input_slew,output_capacitance,slew_lower_threshold,slew_upper_threshold]

def Excel_writer(name,workbook,input_nodes,output_capacitance,input_slew,t):
    
    for k in range(len(input_nodes)):
        worksheet = workbook.create_sheet(name +" IN " + input_nodes[k])
        column = 'B'
        row = 1
        
        ## Write Row Header
        for i in range(len(input_slew)):
            index = column + str(row)
            worksheet[index] =  str(input_slew[i]) + "s"
            worksheet[index].font = Font(bold=True)
            column = chr(ord(column)+1)

        column = 'A'
        row = 2
        
        ## Write Column Header
        for j in range(len(output_capacitance)):
            index = column + str(row)
            worksheet[index] =  str(output_capacitance[j]) + "F"
            worksheet[index].font = Font(bold=True)
            row = row+1

        column = 'B'
        row = 2
        m=0

        table_size = len(input_slew)*len(output_capacitance)
        for i in range(len(input_slew)):
            for j in range(len(output_capacitance)):
                index = chr(ord(column)+i) + str(row+j)
                worksheet[index] =  str(t[m+k*table_size]) + " ns"
                m=m+1
