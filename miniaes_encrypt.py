import os
import sys
path = os.getcwd()
sys.path.append(path)

from miniaes_functions import *

MultiplyTable = [
    ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],#1
    ['0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F'],#2
    ['0','2','4','6','8','A','C','E','3','1','7','5','B','9','F','D'],#3
    ['0','3','6','5','C','F','A','9','B','8','D','E','7','4','1','2'],#4
    ['0','4','8','C','3','7','B','F','6','2','E','A','5','1','D','9'],#5
    ['0','5','A','F','7','2','D','8','E','B','4','1','9','C','3','6'],#6
    ['0','6','C','A','B','D','7','1','5','3','9','F','E','8','2','4'],#7
    ['0','7','E','9','F','8','1','6','D','A','3','4','2','5','C','B'],#8
    ['0','8','3','B','6','E','5','D','C','4','F','7','A','2','9','1'],#9
    ['0','9','1','8','2','B','3','A','4','D','5','C','6','F','7','E'],#10
    ['0','A','7','D','E','4','9','3','F','5','8','2','1','B','6','C'],#11
    ['0','B','5','E','A','1','F','4','7','C','2','9','D','6','8','3'],#12
    ['0','C','B','7','5','9','E','2','A','6','1','D','F','3','4','8'],#13
    ['0','D','9','4','1','C','8','5','2','F','B','6','3','E','A','7'],#14
    ['0','E','F','1','D','3','2','C','9','7','6','8','4','A','B','5'],#15
    ['0','F','D','2','9','6','4','8','1','E','C','3','8','7','5','A'],#16
   #  1   2   3   4   5   6   7   8   9   10  11  12  13  14  15  16
]

nibble_size = 4  # a nibble is four bits
constant_matrix = ['0011','0010','0010','0011'] #d0= 3, d1=2, d2=2, d3=3
rcon = ['0001','0010']

#3.2 NibbleSub, γ
def NibbleSub(nibblestr):
    inpu8tstr=['0000','0001','0010','0011','0100','0101','0110','0111','1000','1001','1010','1011','1100','1101','1110','1111']
    outputstr=['1110','0100','1101','0001','0010','1111','1011','1000','0011','1010','0110','1100','0101','1001','0000','0111']
    index=inpu8tstr.index(nibblestr)
    return outputstr[index]

#3.8 reverseNibbleSub, γ
def reNibbleSub(nibblestr):
    inpu8tstr=['0000','0001','0010','0011','0100','0101','0110','0111','1000','1001','1010','1011','1100','1101','1110','1111']
    outputstr=['1110','0011','0100','1000','0001','1100','1010','1111','0111','1101','1001','0110','1011','0010','0000','0101']
    index=inpu8tstr.index(nibblestr)
    return outputstr[index]

#3.3 ShiftRow, π
def ShiftRow(substring):
    a = substring[1]
    substring[1]=substring[3]
    substring[3]=a
    return substring

#3.4 MixColumn, θ
def MixColumn(nibblein):
    indexconst1 = int(constant_matrix[0],2)#d0
    indexin1 = int(nibblein[0],2)
    indexconst2 = int(constant_matrix[2], 2)
    indexin2 = int(nibblein[1], 2)
    multiply1 = int(MultiplyTable[indexconst1][indexin1],16)
    multiply2 = int(MultiplyTable[indexconst2][indexin2],16)
    d0=format(int(bin(multiply1^multiply2),2),'b').zfill(4)
    indexconst1 = int(constant_matrix[1],2)#d1
    indexin1 = int(nibblein[0],2)
    indexconst2 = int(constant_matrix[3], 2)
    indexin2 = int(nibblein[1], 2)
    multiply1 = int(MultiplyTable[indexconst1][indexin1],16)
    multiply2 = int(MultiplyTable[indexconst2][indexin2],16)
    d1=format(int(bin(multiply1^multiply2),2),'b').zfill(4)
    indexconst1 = int(constant_matrix[0],2)#d2
    indexin1 = int(nibblein[2],2)
    indexconst2 = int(constant_matrix[2], 2)
    indexin2 = int(nibblein[3], 2)
    multiply1 = int(MultiplyTable[indexconst1][indexin1],16)
    multiply2 = int(MultiplyTable[indexconst2][indexin2],16)
    d2=format(int(bin(multiply1^multiply2),2),'b').zfill(4)
    indexconst1 = int(constant_matrix[1],2)#d2
    indexin1 = int(nibblein[2],2)
    indexconst2 = int(constant_matrix[3], 2)
    indexin2 = int(nibblein[3], 2)
    multiply1 = int(MultiplyTable[indexconst1][indexin1],16)
    multiply2 = int(MultiplyTable[indexconst2][indexin2],16)
    d3=format(int(bin(multiply1^multiply2),2),'b').zfill(4)
    output=d0+d1+d2+d3
    return output

#3.5 KeyAddition, σKi
def KeyAddition(P,roundkey):
    xorresult = string_bitwise_xor(P, roundkey)
    output = format(int(xorresult, 2), 'b').zfill(16)
    return output

#3.6 The Mini-AES Key-schedul
def KeySchedule(firstkey):
    round0key=firstkey
    nibblekey=generate_matrix(firstkey)
    w=[]
    for i in range(4):
        w.append(nibblekey[i])
    nibblesubw3=NibbleSub(w[3])
    w.append(string_bitwise_xor(string_bitwise_xor(w[0],nibblesubw3),rcon[0]))
    for i in range(5,8):
        w.append(string_bitwise_xor(w[i-4],w[i-1]))
    for i in range(4,8):
        w[i]=format(int(w[i], 2), 'b').zfill(4)
    round1key=w[4]+w[5]+w[6]+w[7]
    nibblesubw7=NibbleSub(w[7])
    w.append(string_bitwise_xor(string_bitwise_xor(w[4],nibblesubw7),rcon[1]))
    for i in range(9,12):
        w.append(string_bitwise_xor(w[i-4],w[i-1]))
    for i in range(8,12):
        w[i]=format(int(w[i], 2), 'b').zfill(4)
    round2key = w[8] + w[9] + w[10] + w[11]
    key=[round0key,round1key,round2key]
    print('Derivation of the Round Keys:',key)
    return key

#3.7 Mini-AES Encryption
def Encrypt(P,K):
    print("Example of Mini-AES Encryption Printed step-by-step")
    print('P-input:',P)
    print('K-key:',K)
    roundkey = KeySchedule(K)
    step1 = KeyAddition(P,K)
    print('A-keyaddition1:',step1)
    generate1=generate_matrix(step1)
    step2 = [NibbleSub(generate1[0]),NibbleSub(generate1[1]),NibbleSub(generate1[2]),NibbleSub(generate1[3])]
    print('B-Nibblesub:',step2)
    step3 = ShiftRow(step2)
    print('C-Shiftrow',step3)
    step4 = MixColumn(step3)
    print('D-Mixcolumn:',step4)
    step5 = KeyAddition(step4,roundkey[1])
    print('E-keyaddition2:',step5)
    generate5=generate_matrix(step5)
    step6 = [NibbleSub(generate5[0]),NibbleSub(generate5[1]),NibbleSub(generate5[2]),NibbleSub(generate5[3])]
    print('F-Nibblesub2:', step6)
    step7 = ShiftRow(step6)
    print('G-Shiftrow',step7)
    step7 = "".join(step7)
    step8 = KeyAddition(step7, roundkey[2])
    print('H-The final ciphertext:', step8)
    print('-------------------------------------')
    print('\n')
    return

#3.8 Mini-AES Decryption
def Decrypt(P,K):
    #ste1 key addition
    print("Example of Mini-AES Decryption Printed step-by-step")
    print('final ciphertext from encryption:',P)
    print('K-key:',K)
    roundkey = KeySchedule(K)
    step1 = KeyAddition(P,roundkey[2])
    print('keyaddition2:',step1)
    generate1=generate_matrix(step1)
    step2 = [reNibbleSub(generate1[0]),reNibbleSub(generate1[1]),reNibbleSub(generate1[2]),reNibbleSub(generate1[3])]
    print('ReNibblesub:',step2)
    step3 = ShiftRow(step2)
    print('Shiftrow',step3)
    step3 = "".join(step3)
    step4 = KeyAddition(step3, roundkey[1])
    print('keyaddition1:', step4)
    step5 = MixColumn(generate_matrix(step4))
    print('Mixcolumn:',step5)
    generate5=generate_matrix(step5)
    step6 = [reNibbleSub(generate5[0]),reNibbleSub(generate5[1]),reNibbleSub(generate5[2]),reNibbleSub(generate5[3])]
    print('ReNibblesub:', step6)
    step7 = ShiftRow(step6)
    print('Shiftrow', step7)
    step7 = "".join(step7)
    step8 = KeyAddition(step7,roundkey[0])
    print('The original plaintext:',step8)
    print('---------------------------------------')
    print('\n')
    return

P= '1001110001100011'
K='1100001111110000'
final_ciphertext = '0111001011000110'
Encrypt(P,K)
Decrypt(final_ciphertext,K)