import checkpy.tests as t
import checkpy.lib as lib
import checkpy.assertlib as assertlib

@t.test(0)
def hasBeweging(test):
	test.test = lambda : assertlib.fileContainsFunctionDefinitions(_fileName, "beweging")
	test.description = lambda : "definieert de functie `beweging()`"

@t.passed(hasBeweging)
@t.test(1)
def correctOutput(test):
	def testMethod():
		lines = [line for line in lib.outputOf(_fileName).split("\n") if line.strip()]
		answers = [-87, -86, -83, -81, -68, -67, -66, -65, 14, 15, 16, 74, 75, 76, 81, 87]
		nAnswers = len(answers)
		nCorrect = 0
		for answer in answers[:]:
			for line in lines:
				if assertlib.contains(line, str(answer)):
					lines.remove(line)
					answers.remove(answer)
					nCorrect += 1
					break
			else:
				nCorrect -= 1
		return nCorrect == nAnswers, "Miste o.a. verwachte antwoorden {}\nVond o.a. op de volgende regels een niet kloppend antwoord: {}".format(answers[:2], lines[:2])

	test.test = testMethod
	test.description = lambda : "print de juiste hoeken waarbij de vogel de sensor raakt"
