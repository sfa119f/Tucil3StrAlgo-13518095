import copy
from time import perf_counter_ns

#Fungsi dengan parameter matriks puzzle dan mengembalikan boolean apakah sebuah puzzle dapat diselesaikan atau tidak
#Di dalam fungsi ini juga akan mencetak fungsi Kurang(i) dan Nilai Sigma(Kurang(i))+X
def ReachableGoal(a) :
    kurang = [0 for i in range (16)]
    for i in range (16) :
        if (a[i] == "X") :
            idxEmp = i
            temp = 16
        else :
            temp = int(a[i])
        for j in range (i+1, 16) :
            if(a[j] == "X"):
                temp2 = 16
            else :
                temp2 = int(a[j])
            if(temp > temp2) :
                kurang[temp-1] += 1
    for i in range (16) :
        print("Kurang ("+ str(i+1)+ ") =", kurang[i])
    print()
    if ((idxEmp+1)%2 == ((idxEmp)//4+1)%2) :
        print("Nilai Sigma(Kurang(i))+X =", sum(kurang))
        print()
        return (sum(kurang)%2 == 0)
    else :
        print("Nilai Sigma(Kurang(i))+X =", (sum(kurang)+1))
        print()
        return ((sum(kurang)+1)%2 == 0)

#Fungsi dengan parameter matriks puzzle dan mencetak puzzle ke layar
def PrintPuzzle(a) :
    for i in range (4) :
        for j in range (4) :
            print(a[i][j], end=" ")
        print()

#Fungsi dengan parameter matriks puzzle dan mengembalikan posisi X (ubin kosong) dengan nilai X antara 1 hingga 16
def LocX(a) :
    for i in range (4) :
        for j in range (4) :
            if (a[i][j] == "X") :
                return (i*4)+j+1

#Fungsi dengan parameter matriks puzzle dan char dir serta mengembalikan boolean apakah sebuah puzzle ubin kosongnya dapat di geser ke arah dir
def IsMoveToAvailable(a, dir) :
    locX = LocX(a)
    if (dir == "L") :
        if (locX == 1 or locX == 5 or locX == 9 or locX == 13) :
            return False
        else :
            return True
    elif (dir == "R") :
        if (locX == 4 or locX == 8 or locX == 12 or locX == 16) :
            return False
        else :
            return True
    elif (dir == "U") :
        if (locX > 0 and locX < 5) :
            return False
        else :
            return True
    elif (dir == "D") :
        if (locX > 12 and locX < 17) :
            return False
        else :
            return True

#Fungsi dengan parameter matriks puzzle dan char dir serta menggembalikan matrik puzzle setelah ubin kosongnya di geser ke arah dir
def MoveTo(a, dir) :
    b = copy.deepcopy(a)
    RowX = (LocX(a)-1)//4
    ColX = (LocX(a)-1)-(RowX*4)
    if (dir == "L") :
        b[RowX][ColX], b[RowX][ColX-1] = b[RowX][ColX-1], b[RowX][ColX]
    elif (dir == "R") :
        b[RowX][ColX], b[RowX][ColX+1] = b[RowX][ColX+1], b[RowX][ColX]
    elif (dir == "U") :
        b[RowX][ColX], b[RowX-1][ColX] = b[RowX-1][ColX], b[RowX][ColX]
    elif (dir == "D") :
        b[RowX][ColX], b[RowX+1][ColX] = b[RowX+1][ColX], b[RowX][ColX]
    return b

#Fungsi dengan parameter matriks dan mengembalikan jumlah ubin yang tidak kosong yang tidak terdapat pada susunan akhir
def nUbinNotFinal(a):
    temp = "1"
    count = 0
    for i in range (4) :
        for j in range (4) :
            if (temp != a[i][j] and a[i][j] != "X") :
                count += 1
            temp = str((i*4)+j+2)
    return count

#Fungsi dengan parameter matriks puzzle dan int depth serta mengembalikan cost simpul a dengan kedalaman depth
def Cost(a, depth) :
    return nUbinNotFinal(a)+depth 

####################################################################################################
#MAIN PROGRAM
pzl = [0 for i in range (16)]
namaFile = input("Masukkan nama file puzzle: ")
print()
print("Puzzle yang akan diselesaikan : ")
file = open(namaFile, "r")
for i in range (4) :
    strLine = file.readline().replace('\n', '').replace('\r', '')
    pzl[i*4], pzl[i*4+1], pzl[i*4+2], pzl[i*4+3] = strLine.split(" ")
    print(pzl[i*4], pzl[i*4+1], pzl[i*4+2], pzl[i*4+3])
print()
timeStart = perf_counter_ns()
countNode = 0
if (not ReachableGoal(pzl)) :
    print("Persoalan tidak dapat diselesaikan")
else :
    puzzle = [[0 for i in range (4)] for j in range (4)]
    for i in range (4) :
        for j in range (4) :
            puzzle[i][j] = pzl[i*4+j]
    if (nUbinNotFinal(puzzle) == 0) :
        print("Puzzle ini sudah pada susunan akhir! :")
        PrintPuzzle(puzzle)
    else :
        print("Urutan penyelesaian puzzle :")
        queue = []
        tplCostPzl = (Cost(puzzle, 0), puzzle, "Root", 0)
        queue.append(tplCostPzl)
        goal = False
        while (not goal) :
            temp = min(queue)
            if (nUbinNotFinal(temp[1]) == 0) :
                PrintPuzzle(temp[1])
                queue.remove(temp)
                goal = True
            else :
                PrintPuzzle(temp[1])
                depth = temp[3]+1
                if (IsMoveToAvailable(temp[1], "L") and temp[2] != "R") :
                    tempPzl = MoveTo(temp[1], "L")
                    tplCostPzl = (Cost(tempPzl, depth), tempPzl, "L", depth)
                    queue.append(tplCostPzl)
                    countNode +=1
                if (IsMoveToAvailable(temp[1], "R") and temp[2] != "L") :
                    tempPzl = MoveTo(temp[1], "R")
                    tplCostPzl = (Cost(tempPzl, depth), tempPzl, "R", depth)
                    queue.append(tplCostPzl)
                    countNode +=1
                if (IsMoveToAvailable(temp[1], "U") and temp[2] != "D") :
                    tempPzl = MoveTo(temp[1], "U")
                    tplCostPzl = (Cost(tempPzl, depth), tempPzl, "U", depth)
                    queue.append(tplCostPzl)
                    countNode +=1
                if (IsMoveToAvailable(temp[1], "D") and temp[2] != "U") :
                    tempPzl = MoveTo(temp[1], "D")
                    tplCostPzl = (Cost(tempPzl, depth), tempPzl, "D", depth)
                    queue.append(tplCostPzl)
                    countNode +=1
                queue.remove(temp)
                print("   ->   ")
print()    
timeEnd = perf_counter_ns()
print("Waktu eksekusi :", (timeEnd-timeStart)/pow(10,6), "milidetik")
print()
print("Jumlah simpul yang dibangkitkan :", countNode)