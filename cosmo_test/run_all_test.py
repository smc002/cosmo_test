import glob, unittest, os, os.path
import stress_test


test_file_strings = glob.glob('test_*.py')
module_strings = [str[0:len(str)-3] for str in test_file_strings]
testSuite = unittest.defaultTestLoader.loadTestsFromNames(module_strings)
unittest.TextTestRunner(verbosity=2).run(testSuite)
# stress test is disabled due to selenium couldn't be handle by cx_freeze to exe
# stress_test.stress_test(10)


#testSuite = unittest.TestSuite(suites)
# logging_file = os.path.join(os.getenv('HOMEDRIVE'), os.getenv('HOMEPATH'), 'all_test.log')
# f = open(logging_file, 'w')
# unittest.TextTestRunner(verbosity=2, stream=f).run(testSuite)
# f.close()
