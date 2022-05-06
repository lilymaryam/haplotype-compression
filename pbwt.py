from cmath import inf
import sys
from tarfile import LENGTH_NAME
import numpy
import argparse

def convertXtoInts(X, alphabetDict):
    newX = []
    for x in X:
        str = ''
        for a in x:
            if a in alphabetDict:
                str += alphabetDict[a]
        newX.append(str)
    return newX
            

def constructReversePrefixSortMatrix(X, alphabet):
    #Creates the Mx(N+1) matrix (A)
    M = len(X)
    N = (0 if len(X) == 0 else len(X[0]))
    A = numpy.empty(shape=[M, 1 if len(X) == 0 else N+1 ], dtype=int) 

    #Fill in first column of A
    for i in range(M):
        A[i][0] = i

    #iterate through columns of A
    for k in range(N):
        a = []
        #create a 2-D list to hold the positions of the sequences after sorting 
        for alph in range(len(alphabet)):
            a.append([])

        #iterate through indices of column 
        for i in A[:,k]:
            
            pos = alphabet.index(X[i][k])
            a[pos].append(i)
            
            '''
            #consider changing this to find index wo iterating 
            #iterate through alphabet to sort prefixes
            for alph in range(len(alphabet)):
                #sort prefixes by adding them to the sublists of a
                
                if X[i][k] == alphabet[alph]:
                    a[alph].append(i)
                    break
            '''
        
        #column k+1 in A is a sublists concatenated       
        array = []
        for sub in a:
            array += sub

        A[:,k+1] = array

    return A


def constructYFromX(X, alphabet):
    #Creates the MxN matrix
    M = len(X)
    N = (0 if len(X) == 0 else len(X[0]))
    Y = numpy.empty(shape=[M, 0 if len(X) == 0 else N ], dtype=int)
    
    #create the A matrix 
    A = constructReversePrefixSortMatrix(X, alphabet)

    #iterate through i and j of A and construct Y using the function above
    for i in range(M):
        for j in range(N):
            #print(i,j)
            #print(A[i][j])
            #print(Y[i][j])
            #print(X[A[i][j]][j*2:(j*2)+bits])

            Y[i][j] = X[A[i][j]][j]
            #print(type(Y[i][j]))

    return Y



def constructXFromY(Y,alphabet):
    #Creates the MxN matrix
    X = numpy.empty(shape=[len(Y), 0 if len(Y) == 0 else len(Y[0]) ], dtype=int)

    #Code to write - you're free to define extra functions
    #(inline or outside of this function) if you like.
    
    #create A
    A = numpy.zeros(shape=[len(X), 1 if len(X) == 0 else len(X[0])+1 ], dtype=int) 
    
    M = len(X)

    #create first col of A
    for i in range(M):
        A[i][0] = i

    #iterate through number of columns in Y
    for k in range(len(Y[0,:])):

        #iterate through number of rows in A
        for m in range(len(A[:,0])):
            #use formula from #2 to create column of X from Y
            X[A[m][k]][k] = Y[m][k]
        
        #make next column of A
        a = []
        for alph in range(len(alphabet)):
            a.append([])


        #a = []
        #b = []

        #iterate through # of cols in Y
        for i in range(len(Y[:,k])):
            pos = alphabet.index(str(Y[i][k]))
            a[pos].append(A[i][k])
            #use values in Y to construc A
            
            '''
            if Y[i][k] == 0:
                a.append(A[i][k])
                    
            else:
                b.append(A[i][k])
            '''

        #Create next col of A  
        array = []
        for sub in a:
            array += sub      
        A[:,k+1] = array
    
    return list(map(lambda i : "".join(map(str, i)), X)) #Convert back to a list of strings

def runLenEncode(string):
    encoding = "" # stores output string
    i = 0
    while i < len(string):
        # count occurrences of character at index `i`
        count = 1
        while i + 1 < len(string) and string[i] == string[i + 1]:
            count = count + 1
            i = i + 1
        # append current character and its count to the result
        encoding += str(count) + string[i]
        i = i + 1
    return encoding

def compressYMat(Y,conversionAlph):
    compressed=[]
    keys=list(conversionAlph.keys())
    values=list(conversionAlph.values())
    for n in range(Y.shape[1]):
        string=''
        for y in range(len(Y[:,n])):
            string += keys[values.index(str(Y[:,n][y]))]
        compressed.append(runLenEncode(string))
    return compressed


def main():
    print("pbwt main")
    #test code
    X = ['ACG',  'ACC', 'GAC', 'TCG', 'GGT', 'TTT', 'GTT']
    conversionAlph = {'A':'0', 'C':'1', 'G':'2', 'T':'3'}
    #note that alphabet must be a set of integers
    alph = ['0','1', '2', '3']

    X = convertXtoInts(X, conversionAlph)
    print(X)
    #test code
    Y = constructYFromX(X, alph)
   # print(Y)
    #test code
    # print(constructXFromY(Y,alph))
    # print(compressYMat(Y,conversionAlph))

if __name__ == '__main__':
    main()
