import os
import sys
path = os.getcwd()
sys.path.append(path)

#字符串转换成二进制字符串
def string_to_binary(string):
    binary=bin(int(string,2))
    return binary

#将二进制串按按字节划分
def generate_matrix(binary):
    matrix = [binary[i : i+4]
        for i in range(0, len(binary), 4)]
    return matrix

#返回半字节的二进制表示
def nibbles_to_bits(nibbles):
    binary = []
    for i in range(0, len(nibbles)):
        tmp = str(nibbles[i])
        binary.append(bin(int(tmp, 2)))
    return(binary)

#字符串转二进制再做异或操作
def string_bitwise_xor(s1, s2):
    xorresult=bin(int(s1,2)^int(s2,2))
    return xorresult
    # return ''.join(chr(ord(a) ^ ord(b)) for a,b in zip(s1,s2))