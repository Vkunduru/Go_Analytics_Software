class String_Node(object):

    def __init__(self, liberties = None, size = None):
        self.liberties = []
        size = 0

    #getter functions
    def get_libs(self):
        return self.liberties

    def get_size(self):
        return self.size


    # function can increase size var
    def inc_size(self, change):
        self.size += change

    # function can decrease size var
    def dec_size(self, change):
        self.size -= change

    #write function to remove the liberties passed as a list argument to self.liberties list
    def remove_libs(self, libs):
        pass

    # write function to add the liberties passed as a list argument to self.liberties list
    def add_libs(self, libs):
        pass

