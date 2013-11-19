def ROR(x, n, bits=32):
    mask = (2**n) - 1
    mask_bits = x & mask
    return (x >> n) | (mask_bits << (bits - n))

def ROL(x, n, bits=32):
    return ROR(x, bits - n, bits)

def decrypt(obf='test'):
# not implemented
    return 'test'

def encrypt(psw='test'):
    psw = psw.encode('gbk')
    obf = bytearray() 
    for (i, char) in enumerate(psw):
        n = int(char)
        n_r = ROL(n, i+1, bits=8)
        obf.append(int(n_r))
    obf = obf.decode('gbk')
    return obf

if __name__ == '__main__':
    print(encrypt('test'))
