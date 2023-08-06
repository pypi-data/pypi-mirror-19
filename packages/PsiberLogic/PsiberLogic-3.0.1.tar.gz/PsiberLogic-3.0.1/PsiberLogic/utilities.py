def compile():

    from . import FuzzySetup
    print('Compilation complete, Need to re-load interpreter after first compilation')
    print('Then recommended to run PsiberLogic.test()')

def test():

    from .demo import TipFIS
    TipFIS.Test()

    print("Test completed")
