# CUSTOM HEADER PYTHON MODULE MADY BY KPT

# function to leave spaces
def gimmi_Some_Space_pybro( Sure_how_Many_Lines_bro ):
    print( (Sure_how_Many_Lines_bro - 1) * "\n" )

# function to check if a number is even
def check_Even(number):
    if number % 2 == 0:
        return True

# function to return the extension of a file.
def file_Extension_Return(File_Name):
    return File_Name[File_Name.index("."):]

def count_Character_In_File(File_Name, Char_To_Check):
    fin = open( File_Name, "r" )
    stuffInFile = fin.read()
    
    count = 0
    for i in stuffInFile:
        if i == Char_To_Check:
            count += 1
    fin.close()
    return count

def count_Characters_In_File(File_Name):
    fin = open( File_Name, "r" )
    stuffInFile = fin.read()
    count = stuffInFile.__len__()
    fin.close()
    return count