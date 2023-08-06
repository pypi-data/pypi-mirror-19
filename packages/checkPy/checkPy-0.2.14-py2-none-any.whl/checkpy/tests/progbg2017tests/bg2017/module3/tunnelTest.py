import checkpy.tests as t
import checkpy.lib as lib
import checkpy.assertlib as assertlib

@t.test(0)
def containsRequiredFunctionDefinitions(test):
	test.test = lambda : assertlib.fileContainsFunctionDefinitions(_fileName, "tunnel")
	test.description = lambda : "definieert de functie `tunnel()`"

@t.passed(containsRequiredFunctionDefinitions)
@t.test(1)
def correctMaxSpeed(test):
	test.test = lambda : assertlib.numberOnLine(28474.32, lib.getLine(lib.outputOf(_fileName), 0), deviation = 500)
	test.description = lambda : "print de maximale snelheid van de appel"

@t.passed(containsRequiredFunctionDefinitions)
@t.test(2)
def correctTimeTillReturn(test):
	test.test = lambda : assertlib.numberOnLine(5061, lib.getLine(lib.outputOf(_fileName), 1), deviation = 50)
	test.description = lambda : "print het tijdstip van terugkeer na loslaten"
