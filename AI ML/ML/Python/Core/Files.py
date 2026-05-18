import os

class FileReader:
    def __init__(self,filename):
        self.filename = filename
    
    def Print(self):
    #    f = open(self.filename, "rt")
    #    print(f.read())
        with open(self.filename) as f:
            print(f.read())

    def Create(self):
        if (not(os.path.exists(self.filename))):
            with open(self.filename, "x") as f:
                f.write("this is my content")

obj = FileReader(r"C:\Users\rvemula1\Downloads\SavedQuery.txt")
obj.Print()

obj = FileReader(r"C:\Users\rvemula1\Downloads\demofile.txt")
obj.Create()