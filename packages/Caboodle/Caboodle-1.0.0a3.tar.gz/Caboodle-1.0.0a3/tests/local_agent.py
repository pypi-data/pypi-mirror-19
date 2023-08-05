from caboodle.agents.local import LocalAgent
import unittest

class LocalAgentTest(unittest.TestCase):
	'''
	Tests the LocalAgent to verify that it works correctly
	'''

	@classmethod
	def setUpClass(self):
		'''
		Creates a LocalAgent to test
		'''

		self.agent = LocalAgent()

	def test_init(self):
		'''
		Tests that the LocalAgent initializes correctly
		'''

		self.assertEqual(self.agent._cost, 0.0)

	def test_solve(self):
		'''
		Tests that the LocalAgent solves a Challenge correctly
		'''

		data = {'text': 'What is the answer to the question?'}

		self.agent.solve(data)
		self.assertEqual(data['result'], '42')

		with self.assertRaises(TypeError):
			self.agent.solve(None)

	def test_cost(self):
		'''
		Tests that the LocalAgent returns the correct cost
		'''

		self.assertEqual(self.agent.get_cost(), 0.0)

	def test_comparable(self):
		'''
		Tests that a LocalAgent can be compared to another Agent
		'''

		self.assertFalse(self.agent < self.agent)

		with self.assertRaises(TypeError):
			self.agent < None

	def test_success(self):
		'''
		Tests that a LocalAgent can handle a successful Challenge correctly
		'''

		data = {
			'text': 'What is the answer to the question?',
			'result': 42
		}

		self.assertFalse(self.agent.success(data))

	def test_fail(self):
		'''
		Tests that a LocalAgent can handle a failed Challenge correctly
		'''

		data = {
			'text': 'What is the answer to the question?',
			'result': 3.14
		}

		self.assertFalse(self.agent.fail(data))

if __name__ == '__main__':
	unittest.main()
