

class CommandHandler:
    def __init__(self):
        self.commMap = {} # str to func dictionary
        self.commPrefix = '/' 


    def process(self, userInput: str)->None:
        targetComm = userInput.split(' ')[0]
        args = userInput.split(' ')[1:]

        if not (targetComm[len(self.commPrefix):] in self.commMap.keys()):
            raise BaseException('Command does not exist')
        if not targetComm.startswith(self.commPrefix):
            return

        self.commMap[targetComm[len(self.commPrefix):]](*args)

    def add(self, commName : str, command: "function", override : bool=False):
        if commName in self.commMap.keys() and not override:
            raise BaseException('Command Already Exists with Name, override with force=True')

        self.commMap[commName] = command




def castToInt(var):
    try:
        var = int(var)
        return var
    except ValueError:
        return None

if __name__ == '__main__':
    def addNums(*args):
        total = 0
        for num in args:
            num = castToInt(num)
            if num != None:
                total += num
        print(total)

    def form_pair_of_ints(*args):
        a = castToInt(args[0])
        b = castToInt(args[1])

        positional_args = [a, b]
        if None in positional_args:
            return

        print( (a,b) )


    c = CommandHandler()
    c.add('addInts', addNums)
    c.add('intPair', form_pair_of_ints)

    c.process('/addInts 1 str')
    c.process('/intPair 1 2')

