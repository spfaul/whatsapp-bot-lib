class CommandHandler:
    def __init__(self, **kwargs):
        self.commMap = {} # str to func dictionary
        self.commPrefix = '/'

        for key, val in kwargs.items():
            setattr(self, key, val)


    def process(self, userInput: str)->None:
        targetComm = userInput.split(' ')[0]
        args = userInput.split(' ')[1:]

        # extract kwargs from args
        kwargs = {}
        for idx, argument in enumerate(args.copy()):
            if '=' in argument:
                key, val = argument.split('=', 1)
                kwargs[key] = val
                args.pop(idx)

        if not (targetComm[len(self.commPrefix):] in self.commMap.keys()):
            raise BaseException('Command does not exist')
        if not targetComm.startswith(self.commPrefix):
            return

        self.commMap[targetComm[len(self.commPrefix):]](args, kwargs)

    def add(self, commName : str, command: "function", override : bool=False)->None:
        if commName in self.commMap.keys() and not override:
            raise BaseException('Command Already Exists with Name, override with override=True')

        self.commMap[commName] = command



def getKwarg(kwargs: dict, key: str, defaultVal):
    if not (key in kwargs.keys()):
        return defaultVal
    else:
        return kwargs[key]

def strToInt(var: str)->"int/None":
    try:
        var = int(var)
        return var
    except ValueError:
        return None

def strToFloat(var: str)->"float/None":
    try:
        var = float(var)
        return var
    except ValueError:
        return None


if __name__ == '__main__':
    def form_pair_of_ints(args, kwargs):
        a = strToInt(args[0])
        b = strToInt(args[1])
        useSquareBrackets = getKwarg(kwargs, 'useSquareBrackets', 'false')

        positional_args = [a, b]
        if None in positional_args:
            return

        if useSquareBrackets == 'true':
            print( [a,b] )
        else:
            print( (a,b) )


    c = CommandHandler(commPrefix='/')
    c.add('intPair', form_pair_of_ints)

    c.process('/intPair 1 2 useSquareBrackets=false')

