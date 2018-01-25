############################################
# Faisal Alnahhas                          #
# VM Translator                            #
# CSCI 230                                 #
# Fall 2016                                #
############################################

import os
import glob

#program = input("Select a .vm file ")
#fin = open(program + ".vm")
#in_text_vm = fin.readlines()
#fin.close()

#target = open("FibonacciElement.asm", "w")
#target.truncate()
#target.write(asm_out)
#for filename in glob.glob(os.path.join(path, "*.vm")):
#    target.write(output2)

#target.close()

symbol_table = {"local":"LCL", 'argument':"ARG", 'this':"THIS", 'that':"THAT"}
pointer_temp = {"pointer":"3", "temp":"5"}

gt_counter = 0
lt_counter = 0
eq_counter = 0
RAM_counter = 0
lbl_counter = 0

set_SP = "@256\nD=A\n@SP\nM=D\n"
asm_out = set_SP



def parse(in_text_vm):
    stripped_org = []
    for line in in_text_vm:
        if len(line) > 2 and line [0:2] != "//":
            stripped_org.append(line.strip())

    for line in range(len(stripped_org)):
        comInd = stripped_org[line].find("//")
        if comInd != -1:
            stripped_org[line] = stripped_org[line][:comInd]
    return stripped_org
        


def parse_dic(stripped_org):
    parsed_dic={}
    for line in range(len(stripped_org)):
        parsed_dic[line] = stripped_org[line].split()#re.findall ("\w+", stripped_org[line])
    return parsed_dic


def push(value):
    return "@" + str(value) + "\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"

def pop():
    return "@SP\nM=M-1\nA=M\nD=M\n"

def add():
    return pop() + "@SP\nM=M-1\nA=M\nMD=D+M\n@SP\nM=M+1\n"

def sub():
    return pop() + "@SP\nM=M-1\nA=M\nMD=M-D\n@SP\nM=M+1\n"

def And():
    return pop() + "@SP\nM=M-1\nA=M\nD=D&M\nM=D\n@SP\nM=M+1\n"

def Or():
    return pop() + "@SP\nM=M-1\nA=M\nD=D|M\nM=D\n@SP\nM=M+1\n"

def neg():
    return pop() + "@SP\nA=M\nM=-D\n@SP\nM=M+1\n"

def Not():
    return pop() + "@SP\nA=M\nM=!D\n@SP\nM=M+1\n"

def eq():
   global eq_counter
   eq_counter += 1
   return sub() + "@ISZERO" + str(eq_counter) + "\nD;JEQ\n@NOTZERO" + str(eq_counter) + "\nD;JNE\n(ISZERO" \
          + str(eq_counter) + ")\n" + "@SP\nA=M-1\nM=-1\n@LOC_EQ" + str(eq_counter) + "\n0;JMP\n(NOTZERO" + str(eq_counter) + \
          ")\n@SP\nA=M-1\n" + "M=0\n(LOC_EQ" + str(eq_counter) + ")\n" + "\n@SP\nA=M-1\n"
           
def gt():
   global gt_counter
   gt_counter += 1
   return sub() + "@GREATERTHAN" + str(gt_counter) + "\nD;JGT\n@LESSTHANEQ" + str(gt_counter) +  \
          "\nD;JLE\n(GREATERTHAN" + str(gt_counter) + ")\n" + "@SP\nA=M-1\nM=-1\n" \
          "@LOC_GT" + str(gt_counter) + "\n0;JMP\n(LESSTHANEQ" + str(gt_counter) + ")\n" + "@SP\nA=M-1\n" \
          + "M=0\n(LOC_GT" + str(gt_counter) + ")\n" + "@SP\nA=M-1\n"

def lt():
   global lt_counter
   lt_counter += 1
   return sub() + "@LESSTHAN" + str(lt_counter) + "\nD;JLT\n@GREATERTHANEQ" + str(lt_counter) \
          + "\nD;JGE\n(GREATERTHANEQ" + str(lt_counter) + ")\n" \
          + "@SP\nA=M-1\nM=0\n@LOC_LT" + str(lt_counter) + "\n0;JMP\n(LESSTHAN" + str(lt_counter) + ")\n" \
          + "@SP\nA=M-1\n" + "M=-1\n(LOC_LT" + str(lt_counter) + ")\n" + "@SP\nA=M-1\n"           


def push_pointer(arg):
    return "@3\n" + "D=A\n" + "@" + str(arg) + "\nA=D+A\n" + "D=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"

def pop_pointer(arg):
    return "@3\nD=A\n" + "@" + str(arg) + "\nAD=D+A\n@13\nM=D\n" + pop() + "@13\nA=M\nM=D\n"

def push_local(arg):
    return "@LCL\nD=M\n" + "@" + str(arg) + "\nAD=D+A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"

def pop_local(arg):
    return  "@LCL\nD=M\n" + "@" + str(arg) + "\nAD=D+A\n@13\nM=D\n" + pop() + "@13\nA=M\nM=D\n"


def push_static(program, x):
    return "@" + str(program) + "." + str(x) + "\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"

def pop_static(program, v):
    return pop() + "@" + program + "." + str(v) +  "\nM=D\n"
    

def make_label():
    global lbl_counter
    lbl_counter += 1
    return "Label" + str(lbl_counter)

def push2(v):
    return "@" + str(v) + "\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"


def call(arg_1, arg_2):
    global asm_out
    get_label = make_label()
    return push(get_label) + push2("LCL") + push2("ARG") + push2("THIS") + push2("THAT") \
               + "@SP\nAD=M\nM=D\n@SP\nM=M+1\n" + push(arg_2) + sub() + push("5") + sub() + pop() \
               + "@ARG\nM=D\n@SP\nD=M\n@LCL\nM=D\n" + "@" + str(arg_1) + "\n0;JMP\n(" \
               + str(get_label) + ")\n"
    


def translation(function, parsed_dic):
    global set_SP
    global asm_out 
    temp_counter = RAM_counter % 8 + 5
 #   temp_ram = list(range(5,13))
    for line in range(len(parsed_dic)):
        if len(parsed_dic[line])==3:
            arg_0 = parsed_dic[line][0]
            arg_1 = parsed_dic[line][1]
            arg_2 = parsed_dic[line][2]

        if len(parsed_dic[line])==2:
            arg_0 = parsed_dic[line][0]
            arg_1 = parsed_dic[line][1]

        if len(parsed_dic[line])==1:
            arg_0 = parsed_dic[line][0]


        #group 1
        if arg_0 == "add":
            asm_out += add()

        if arg_0 == "sub":
            asm_out +=  sub()

        if arg_0 == "and":
            asm_out += And()

        if arg_0 == "or":
            asm_out += Or()

        # group 2
        if arg_0 == "not":
            asm_out += Not()

        if arg_0 == "neg":
            asm_out += neg()

        # group 3
        if arg_0 == "eq":
            asm_out += eq()

        if arg_0 == "lt":
            asm_out += lt()

        if arg_0 == "gt":
            asm_out += gt()



        if arg_0 == "push" and arg_2.isdigit():
            if arg_1 == "local" or arg_1 == "argument" or arg_1 == "this" or arg_1 == "that":
                asm_out += "@" + str(symbol_table[arg_1]) + "\nD=M\n@"+str(arg_2) \
                           + "\nA=D+A\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"
                

            elif arg_1 == "pointer" or arg_1 == "temp":
                asm_out += "@"+str(pointer_temp[arg_1])+"\nD=A\n@"+str(arg_2)+"\nA=D+A\nD=M\n"\
                        "@SP\nA=M\nM=D\n@SP\nM=M+1\n"
            
            elif arg_1 == "constant":
                asm_out += push(arg_2)


        if arg_0 == "pop" and arg_2.isdigit():
            if arg_1 == "local" or arg_1 == "argument" or arg_1 == "this" or arg_1 == "that":
                asm_out += "@" + str(symbol_table[arg_1]) + "\nD=M\n@"+(arg_2)+"\nAD=D+A\n@R" + str(temp_counter) \
                + "\nM=D\n" + pop() + "@R" + str(temp_counter) + "\nA=M\nM=D\n"

            if arg_1 == "pointer" or arg_1 == "temp":
                asm_out += "@"+str(pointer_temp[arg_1])+"\nD=A\n@"+str(arg_2)+"\nAD=D+A\n@R5" \
                + "\nM=D\n"+ pop() + "@R5" + "\nA=M\nM=D\n"

        if arg_0 == "push" and arg_1 == "static":
            asm_out += push_static(path, arg_2)

        if arg_0 == "pop" and arg_1 == "static":
            asm_out += pop_static(path, arg_2)

        if arg_0 == "label":
            asm_out += "(" + str(arg_1) + ")\n"

        if arg_0 == "goto":
            asm_out += "@" + str(arg_1) + "\n0;JMP\n"

        if arg_0 == "if-goto":
            asm_out += pop() + "\n@" + str(arg_1) + "\nD;JNE\n"

        if arg_0 == "function":
            asm_out += "(" + str(arg_1) + ")\n"
            for i in range(0,int(arg_2)):
                asm_out += push(0)

        if arg_0 == "return":
            asm_out +="@LCL\nD=M\n@R13\nM=D\n" \
            + "@5\nD=A\n@13\nD=M-D\nA=D\nD=M\n@14\nM=D\n" \
            + pop() + "@ARG\nA=M\nM=D\n" \
            + "@ARG\nD=M\n@SP\nM=D+1\n" \
            + "@4\nD=A\n@13\nD=M-D\nA=D\nD=M\n@LCL\nM=D\n" \
            + "@3\nD=A\n@13\nD=M-D\nA=D\nD=M\n@ARG\nM=D\n" \
            + "@2\nD=A\n@13\nD=M-D\nA=D\nD=M\n@THIS\nM=D\n" \
            + "@1\nD=A\n@13\nD=M-D\nA=D\nD=M\n@THAT\nM=D\n" \
            + "@14\nA=M\n0;JMP\n"
            #Frame = LCL
            #Ret = *(Frame - 5)
            #*Arg = pop
            #SP = Arg+1
            #THAT = *(Frame - 1)
            #THIS = *(Frame - 2)
            #ARG = *(Frame - 3)
            #LCL = *(Frame - 4)
            #goto Ret

        #if arg_0 == "call":
#            call("Sys.init", 0)
        if arg_0 == "call":
             asm_out += call(arg_1, arg_2)

             
    return asm_out
        


#write_to = open(program + ".asm", "w")
#write_to.truncate()
#output = translation(parse_dic(parse(in_text_vm)))
#print(output)
#write_to.write(output)
#write_to.close()

#output2= translation(parse_dic(parse(target)))
path = input("Please type in the folder that contains the .vm files you need to test ")
def main():
    ls = []
    ls2 = []
   # path = input("Please type in the folder that contains the .vm files you need to test ")
    split_path = path.split("/")[-1]

    target = open(path + "/" + split_path + ".asm", "w")
    target.truncate()
    #Bootstrap
    target.write("@256\nD=A\n@SP\nM=D\n" + call("Sys.init", 0))

    for files in glob.glob(os.path.join(path, "*.vm")):
        fin = open(files)
        vm_file = fin.readlines()
        target.write(translation(files.split("/")[-1], parse_dic(parse(vm_file))))
        fin.close()
                             
    
 #   for files in glob.glob(os.path.join(path, "*.vm")):
#        fin = open(files)
#        ls.append(fin.readlines())
#        fin.close()
#    print(ls)
#    for lines in ls:
#        for l in lines:
#            ls2.append(l)
    print(ls2)

#    target.truncate
 #   target.write(asm_out)
 #   target.write("@256\nD=A\n@SP\nM=D\n" + call("Sys.init", 0))

#    target.write(translation(parse_dic(parse(ls2))))
    print(target)
    target.close()
#    parsed = parse(in_text_vm)
#    print(parse_dic(parsed))
main()

#def main2():
#    parsed = parse(target)
#    print(parse_dic(target))    
#main2()

      
