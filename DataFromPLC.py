class DataFromPLC:

    def __init__(self, client__, byte, bit, size):
        self.__info = client__.db_read(byte, bit, size)

    @property
    def info(self):
        return self.__info
# end class
