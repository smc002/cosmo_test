import glob, unittest, os, os.path

test_file_strings = glob.glob('test_*.py')
module_strings = [str[0:len(str)-3] for str in test_file_strings]
testSuite = unittest.defaultTestLoader.loadTestsFromNames(module_strings)
#testSuite = unittest.TestSuite(suites)
logging_file = os.path.join(os.getenv('HOMEDRIVE'), os.getenv('HOMEPATH'), 'all_test.log')
f = open(logging_file, 'w')
unittest.TextTestRunner(verbosity=2, stream=f).run(testSuite)
f.close()
