
import base64

class Encrypter:
    @staticmethod
    def encode(data):
        return base64.b64encode(Encrypter.cesar_all(data, 1))

    @staticmethod
    def decode(data):
        return base64.b64decode(Encrypter.cesar_all(data, -1))

    @staticmethod
    def cesar_all(string, decalage):
        res = ''
        for char in string:
            res += Encrypter.cesar(char, decalage)
        return res

    @staticmethod
    def cesar(char, decalage):
        min_list = 'abcdefghijklmnopqrstuvwxyz'
        maj_list = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        if char in min_list:
            return min_list[(min_list.index(char)+decalage)%26]
        if char in maj_list:
            return maj_list[(maj_list.index(char)+decalage)%26]
        return char
