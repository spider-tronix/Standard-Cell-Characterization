# Standard-Cell-Characterization
Open Source tool to build liberty files and for Characterizing Standard Cells using ngspice. Standard-cell characterization refers to the process of compiling data about the behavior of standard-cells. Timing and Power are two of the most important characteristics that needs to be determined for a standard cell before it is used in the design flow. These information are stored in a comman file format across the industry referred to as the liberty format (.lib). The .lib file of a standard cells describes these information in a predefined template so that it can be effectively used by the P&R tool 
<br/>
These Timing and Power Parameters change with respect to two important parameters which are **Input Slew (seconds)  and Output Loads (Farads)**. These parameters are varied across a given range to generate the characteristics of the standard cell.

## Timing Characterization : 
<img src="https://github.com/akilm/Standard-Cell-Characterization/blob/main/Image%20Files/Timing%20Waveforms.png" 
alt="Timing Waveforms" > <br/>
**rise transition, fall transition, cell rise, cell fall** are the different parameters which form the timing characteristics of a standard cell. Certain constants are required as input before determining these Timing Characteristics. These Values are different for each input pin.

```
slew_upper_threshold_pct_rise : 80;
slew_lower_threshold_pct_rise : 20;
slew_upper_threshold_pct_fall : 80;
slew_lower_threshold_pct_fall : 20;
input_threshold_pct_rise : 50;
input_threshold_pct_fall : 50;
output_threshold_pct_rise : 50;
output_threshold_pct_fall : 50;
```

## Power Characterization
Power Characterization can be classified into two different categories. 
1. **Rise and Fall power** dissipation associated with each of the inputs 
2. **Leakage Power** where the input is held static at a particular logic level and the power dissipation is characterised in the static condition.

# Algorithm for Timing Characterization
The entire tool is built on top of the features of ngspice-an opensource circuit simulator.Assuming a sample case where the standard cell needs to be characterized against 5-input slew values and 5-output capacitance values.
```
input_slew = [x1,x2,x3,x4,x5]
output_capacitance = [y1,y2,y3,y4,y5]
```

1. **Analyze the Logic Function of the Standard Cell**:
    The logic Function of the Combinational Circuit is analyzed to generate a test pattern - such that the output toggles with or out of phase with the input. This is very essential because hardcoding the voltage waveforms for all the nodes may sometimes result in a waveform that does not change with time and remains constant.
    ```
    Ex: Logic Function of a 2 input NAND Gate : !( A & B )
    ```
    The algorithm analyzes the logic function and assigns PULSE waveform for the input pin under characterization and determines the voltage of the other input node based on the logic function. In this case B cannot be set to low voltage - in which case the output would remain at 1 at all times. <br/>
    <img src="https://github.com/akilm/Standard-Cell-Characterization/blob/main/Image%20Files/Analyze%20Logic%20Function.PNG" 
alt="Analyze Logic Function" width = 554‬ height = 324 >
    

2. **Build Netlists**:
    The underlying methodology here is that the standard cells must be simulated for all the possible combinations of input slew and output capacitance. The netlist of the standard cell is taken as a base and different netlists are built based on the different combinations of input slew and output capacitance. For our examples, size(input_slew) = 5 and size(output_capacitance) = 5 --> a total of 5x5 = 25 netlists would be built and saved temporarily .<br/>
    <img src="https://github.com/akilm/Standard-Cell-Characterization/blob/main/Image%20Files/temporary_netlists_whole.PNG" 
alt="Netlists Whole" width = 1,219 height = 166 >
    <img src="https://github.com/akilm/Standard-Cell-Characterization/blob/main/Image%20Files/temporary_netlists_compare.PNG" 
alt="Netlists Compare" width = 1,071 height = 508 >
<br/>
    

3. **Run Simulations**:
    The netlists which are created in the previous step are run one after the other. The Netlists whicha built in the previos stage include an ngspice command to save the input,output voltage and the time vectors in a **.data file**. All the possible combinations are executed and the data files are stored temporarily in a folder.
    <img src="https://github.com/akilm/Standard-Cell-Characterization/blob/main/Image%20Files/spice%20file%20execution.PNG" 
alt="Data Files Different Combinations" >
    <img src="https://github.com/akilm/Standard-Cell-Characterization/blob/main/Image%20Files/spice%20file%20execution_1.PNG" 
alt="Data Files Different Combinations" >
    <img src="https://github.com/akilm/Standard-Cell-Characterization/blob/main/Image%20Files/datafiles%20all%20combination.PNG" 
alt="Data Files Different Combinations" >
    <img src="https://github.com/akilm/Standard-Cell-Characterization/blob/main/Image%20Files/data%20file%20generation.PNG" 
alt="Data Files" >

4. **Characterization**:
    Each of these .data files is read and the vectors are analyzed to find the **tripping points** (points where the input and output voltages cross the upper threshold (0.8* Vdd), lower threshold (0.2* Vdd) and mid threshold (0.5* Vdd). The slopes (rising or falling) at these points are also determined. Based on the above obtained data, the values of rise transition, fall transition, cell rise and cell fall times are determined. These values are found for multiple rising and falling edges and averaged to reduce errors.
    
5. **Format Output Data**
    The output is currently formatted in two different forms -a text file and an excel file. The excel file stores the different tables under each pin for different parameters as given below. `Work under Progress: Format the data in Liberty file format (.lib)`
    <img src="https://github.com/akilm/Standard-Cell-Characterization/blob/main/Image%20Files/Characterization%20Results_1.PNG" 
alt= "Characterization Files" >

<img src="https://github.com/akilm/Standard-Cell-Characterization/blob/main/Image%20Files/Characterization%20Results_2.PNG" 
 alt= "Characterization Files 2 " >

<img src="https://github.com/akilm/Standard-Cell-Characterization/blob/main/Image%20Files/Characterization%20Results%20Text%20Files.PNG" 
 alt= "Characterization Files 3 ">

6. **Delete Temporary Files**
    The temporary netlists created and .data files are deleted . Hence, the working directory is cleaned and all the temporary data is removed.

# Input Files and Directory Structure
1. Netlist : The netlist is expected to be present inside the Characterization/Netlist folder . All the .cir files present in this directory will be automatically listed during the tool run and the user has to enter the index number corresponding to the particular netlist.
2. Input Data : The tool expects a .xlsx file with the same name as the Netlist which contains the following details : Logic Function, input nodes , output node, Vdd, T (Time period), input_slew, output_capacitance, slew_lower_threshold, slew_upper_threshold values.
<img src="https://github.com/akilm/Standard-Cell-Characterization/blob/main/Image%20Files/Input%20File.PNG" 
 alt= "Input Files ">

# Output Files :
1. Tabular Data : An excel file is created with multiple sheets with each sheet corresponding to a particular input nodes' timing parameter table [rise transition, fall transition, cell rise, cell fall]
2. Text File :  A text file with different combinations of input slew and output capacitance is also created.
3. .Lib Format : Under Development


# Code Structure
1. [Characterization.py](https://github.com/akilm/Standard-Cell-Characterization/blob/main/Work/Characterization.py) : Main Script which utilises other scripts to generate the necessary output files. Also contains the function for running ngspice simulation using subprocess library.
2. [NodeVoltages_.py](https://github.com/akilm/Standard-Cell-Characterization/blob/main/Work/NodeVoltages_.py) : Analyses the logic function of the standard cell and determines the node voltages (both constant and pulse waveforms) for each netlist.
3. [NetlistBuilder_.py](https://github.com/akilm/Standard-Cell-Characterization/blob/main/Work/NetlistBuilder_.py) : For Building the Netlists for different combinations and saving them in the characterization folder.
4. [Characterize_.py](https://github.com/akilm/Standard-Cell-Characterization/blob/main/Work/Characterize_.py) : Analyzes the .data files to find the timing characteristics for different input nodes.[rise transition, fall transition, cell rise, cell fall.
5. [openpyxl_.py](https://github.com/akilm/Standard-Cell-Characterization/blob/main/Work/openpyxl_.py) : Reads the input values for standard cell characterization. Also used for formatting and writing the output into excel file.
6. [DeleteFiles_.py](https://github.com/akilm/Standard-Cell-Characterization/blob/main/Work/DeleteFiles_.py) : Deletes the temporary netlists and data files created during characterization and frees up the memory.

# Steps to run
1. Clone the Repository <br/>
    ``` git clone ```
2. Place the netlist and the .xlsx file with all the input paramters inside the ```Standard-Cell-Characterization/Characterization/Netlists``` Folder. [Sample Formats]() are given in this repository.
3. Run the charaterization.py script from the terminal or using Python idle. <br/>
``` ~/Standard-Cell-Library-skywater-130/Work$ python3 Characterization.py```
4. The script will list all the netlists given inside the directory, enter the index number of the standard cell to be characterised .
5. Outputs would be generated and saved in the Characterization folder.

<img src="https://github.com/akilm/Standard-Cell-Characterization/blob/main/Image%20Files/Steps%20to%20run.PNG" 
 alt= "Steps to run ">

# Work-Left
- Power Characterization
- Liberty Files (.lib) Format Generation
- Optimize to reduce Run-Time
# Acknowledgements
- Kunal Ghosh, Co-founder (VSD Corp. Pvt. Ltd)
