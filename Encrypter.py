
import base64

class Encrypter:
    left = b'<!DOCTYPE html> <html lang="en"> <head> <meta charset="utf-8"> </head><body><h1>Hello, world!</h1>'
    right = b'</body></html>'
    @staticmethod
    def encode(data):
        data = Encrypter.left+data+Encrypter.right
        data = data.replace('SSH', '$$%%BITE%%$$')
        data = data.replace('ssh', '$$%%bite%%$$')
        return base64.b64encode(data)
        #return base64.b64encode(Encrypter.cesar_all(data, 1))

    @staticmethod
    def decode(data):
        data = base64.b64decode(data)
        data = data[Encrypter.left.__len__():-Encrypter.right.__len__()]
        data = data.replace('$$%%BITE%%$$', 'SSH')
        data = data.replace('$$%%bite%%$$', 'ssh')
        return data
        #return Encrypter.cesar_all(base64.b64decode(data), -1)

    @staticmethod
    def cesar_all(string, decalage):
        string = str(string)
        print(string)
        res = ''
        for char in string:
            res += Encrypter.cesar(char, decalage)
        return bytes(res, 'UTF-8')

    @staticmethod
    def cesar(char, decalage):
        min_list = 'abcdefghijklmnopqrstuvwxyz'
        maj_list = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        if char in min_list:
            res = min_list[(min_list.index(char)+decalage)%26]
            return res
        if char in maj_list:
            return maj_list[(maj_list.index(char)+decalage)%26]
        return char

#res = Encrypter.encode('toto')
#print(res)
#res = Encrypter.decode(res)
#print(res)
