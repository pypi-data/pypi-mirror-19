========
GenTests
========

A module for generating tests from data with unittest

Installation:
=============

Install using pip::

	pip install gentests

Example:
========

The following test code will generate 10 tests::

	import unittest
	from gentests import gentests, vals

	def my_less_than(a,b):
	    '''Broken function to test'''
	    return a <= b

	@gentests
	class TestSomething(unittest.TestCase):


	    @vals([
	        'val_0',
	        'val_1',
	        'val_2'
	    ])
	    def test_False(self, value):
	        '''Test that fails'''
	        self.assertFalse(True)

	    @vals([
	        'val_0',
	        'val_1',
	        'val_2'
	    ])
	    def test_True(self, value):
	        '''Test that passes'''
	        self.assertTrue(True)

	    def name_test(original_name, left, right, result):
	        '''Explicitly name our tests based on our arguments'''
	        return '{0}_my_less_than_{1}_{2}_is_{3}'.format(
	            original_name,
	            str(left),
	            str(right),
	            str(result)
	        )

	    @vals([
	        (0, 1, True),
	        (0, 0, False), #Fails
	        (0, 2, True),
	        (2, 1, False),
	    ], name=name_test) #pass optional naming function
	    def test_MyLessThan(self, left, right, result):
	        '''Test where some pass and some fail'''
	        self.assertEqual(my_less_than(left, right), result)

	if __name__ == '__main__':
	    unittest.main()

that produce the following output::

	FFFF......
	======================================================================
	FAIL: test_False_gentest_0 (test.TestSomething)
	----------------------------------------------------------------------
	Traceback (most recent call last):
	  File "C:\Users\Redirection\windoj9\Documents\repos\GenTests\gentests.py", line 17, in <lambda>
	    return lambda other_self: base_func(other_self, *args)
	  File "C:\Users\Redirection\windoj9\Documents\repos\GenTests\test.py", line 19, in test_False
	    self.assertFalse(True)
	AssertionError: True is not false

	======================================================================
	FAIL: test_False_gentest_1 (test.TestSomething)
	----------------------------------------------------------------------
	Traceback (most recent call last):
	  File "C:\Users\Redirection\windoj9\Documents\repos\GenTests\gentests.py", line 17, in <lambda>
	    return lambda other_self: base_func(other_self, *args)
	  File "C:\Users\Redirection\windoj9\Documents\repos\GenTests\test.py", line 19, in test_False
	    self.assertFalse(True)
	AssertionError: True is not false

	======================================================================
	FAIL: test_False_gentest_2 (test.TestSomething)
	----------------------------------------------------------------------
	Traceback (most recent call last):
	  File "C:\Users\Redirection\windoj9\Documents\repos\GenTests\gentests.py", line 17, in <lambda>
	    return lambda other_self: base_func(other_self, *args)
	  File "C:\Users\Redirection\windoj9\Documents\repos\GenTests\test.py", line 19, in test_False
	    self.assertFalse(True)
	AssertionError: True is not false

	======================================================================
	FAIL: test_MyLessThan_my_less_than_0_0_is_False (test.TestSomething)
	----------------------------------------------------------------------
	Traceback (most recent call last):
	  File "C:\Users\Redirection\windoj9\Documents\repos\GenTests\gentests.py", line 17, in <lambda>
	    return lambda other_self: base_func(other_self, *args)
	  File "C:\Users\Redirection\windoj9\Documents\repos\GenTests\test.py", line 47, in test_MyLessThan
	    self.assertEqual(my_less_than(left, right), result)
	AssertionError: True != False

	----------------------------------------------------------------------
	Ran 10 tests in 0.006s

	FAILED (failures=4)
