#!/usr/bin/python

import sys, re, inspect, unittest
from datetime import datetime
from init import *
exec ('from ' + suite + ' import *') #same as `from web import *`; var suite is set in init.py
#from web import digestCredentialTests as digestCredentialTests

def printTestSuits():
	global testSuites
	print >> sys.stderr, "Test Suites:"
	for testSuite in testSuites:
		print >> sys.stderr, "\t" + testSuite
	return

def validateSuites(suites):
	global testSuites
	for i in range(1, len(suites)):
		if suites[i] == 'all': continue
		elif suites[i] not in testSuites:
			print >> sys.stderr, suites[i]
			return 1
	return 0

testSuitePattern = re.compile("([a-zA-Z]+)Tests")
testSuites = []
for testSuite in dir():
	if re.match(testSuitePattern, testSuite):
		testSuites.append(testSuite)

if len(sys.argv) <= 1:
	print >> sys.stderr, '\nUsage: run.py [all | suit(s)]\nWhere suit(s) is one or more from:'
	printTestSuits()
	exit(1)
elif validateSuites(sys.argv) != 0:
	print >> sys.stderr, "Error: not valid suite/s"
	exit(1)
elif str(sys.argv[1]) == 'all':
	for i in range(len(testSuites)):
		testSuites[i] = suite + '.' + testSuites[i]
		testCase = 'all'
else:
	testSuites = []
	testCase = 'all'
	for i in range(1, len(sys.argv)):
		suiteName = str(sys.argv[i])
		testSuites.append(suite + '.' + suiteName)

	if len(testSuites) == 1:
		testCases = ['all']
		testCasePattern = re.compile("test_([0-9]+)_([a-zA-Z_]+)")
		print >> sys.stderr, "Select which test to run:\n\tall"
		for testCase in inspect.getmembers(eval(suiteName).Cases, predicate=inspect.ismethod):
			if re.match(testCasePattern, testCase[0]):
				print >> sys.stderr, '\t' + testCase[0]
				testCases.append(testCase[0])

		testCase = raw_input('> ')
		if testCase not in testCases:
			print >> sys.stderr, '\nError: ' + testCase + ' is not valid test from ' + suiteName
			exit(1)

testLoader = unittest.TestLoader()

#suite = testLoader.loadTestsFromModule(digestCredentialTests)
#suite = testLoader.loadTestsFromTestCase(module.Cases)
#print functions (tests) from class (.Cases)
#print dir(module.Cases)
#suite = testLoader.loadTestsFromName('test_1_change_digestUser', module.Cases)

if __name__ == "__main__":
	logFile = 'results/logfile_' + str(datetime.now()).replace(' ', '_') + '.log'
	fp = open(logFile, "w")
	print >> sys.stderr, 'Starting ...'
	for suiteName in testSuites:
		module = sys.modules[suiteName]
		if testCase == 'all':
			suite = testLoader.loadTestsFromModule(module)
		else:
			suite = testLoader.loadTestsFromName(testCase, module.Cases)
		print >> fp, 'Starting suite:', suiteName
		print >> fp, 'Number of tests:', suite.countTestCases()
		print >> sys.stderr, 'Running: ' + suiteName + ' ...'
		unittest.TextTestRunner(stream = sys.stderr, verbosity = 2).run(suite)
		#unittest.TextTestRunner(stream = fp, verbosity = 2).run(suite)
	fp.close()
	print >> sys.stderr, 'END'
