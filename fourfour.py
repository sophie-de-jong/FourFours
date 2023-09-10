from settings import *
from typing import Iterable
import itertools

# Class responsible for solving the popular four fours math problem. (https://en.wikipedia.org/wiki/Four_fours)
class FourFours:

	# The num variable defines the problem basis. For example: num = 4 
	# means the algorithm will compute the four fours problem and 
	# num = 5 means the algorithm will compute the five fives problem.
	def __init__(self, num: int=4) -> None:
		self.num = num
		self.str_num = str(num)
		concat_num = ''
		assert self.num >= 1
		
		# Initialize a list to contain hash tables. Each table in the list represents how many 
		# digits were used up to get the key result (e.g. the second hash table contains 
		# equations with 3 digits). The tables contain key-value pairs of the equation string 
		# and it's result such that eval(t[x]) == x.
		self.eqn_tables = []
		self.current_table = t = {}
		
		# Construct self.num hash tables and append to the list.
		for n in range(1, self.num + 1):
			t.clear()
			
			# Manually add concatenated numbers (e.g. 44, 4444)
			concat_num += self.str_num
			x = float(concat_num)
			if self.is_valid_answer(x):
				t[x] = concat_num
			
			# Manually add decimal numbers (e.g. 0.4, 0.444)
			decimal_num = '.' + concat_num
			x = float(decimal_num)
			t[x] = decimal_num
			
			# Loop through every combination of hash tables who's indices in eqn_tables add up to n. 
			# This ensures that hash table n will always contain n + 1 digits in its equation.
			for a, b in self.addends(n):
				t1 = self.eqn_tables[a - 1]
				t2 = self.eqn_tables[b - 1]
				self.get_binary_combs(t1, t2)
			
			self.get_unary_combs(t.copy())
			self.eqn_tables.append(t.copy())
	
	# Takes two input iterables t1, t2 and computes the result between each combination in pairs 
	# on every binary operator. Each result gets appended to an equation table. 
	def get_binary_combs(self, t1: dict, t2: dict) -> None:
		for x, y in itertools.product(t1, t2):
			for str_oper, oper in BINARY_OPERS:
				try:
					# Cast result to float because some functions return integers and we want type safety.
					result = float(oper(x, y))
				except (OverflowError, ZeroDivisionError):
					# We can safely ignore all errors because either the calculated value
					# would have been way too large for the dictionary anyway, or we tried
					# divide by zero.
					continue
					
				if self.is_valid_answer(result):
					eqn = self.eqn_str(str_oper, t1[x], t2[y])
					self.current_table[result] = eqn		
	
	# Takes an input iterable t and computes the result on every unary operator. Each result 
	# gets appended to an equation table.
	def get_unary_combs(self, t: dict) -> None:
		for x in t:
			for str_oper, oper in UNARY_OPERS:
				try:
					# Cast result to float because some functions return integers and we want type safety.
					result = float(oper(x))
				except (OverflowError, ValueError):
					# We can safely ignore all errors because either the calculated value
					# would have been way too large for the dictionary anyway, or we tried
					# to put a negative number into a square root function.
					continue
					
				if self.is_valid_answer(result):
					eqn = self.eqn_str(str_oper, t[x])
					self.current_table[result] = eqn		
	
	# Returns True if x is valid answer to an equation and can be added to an equation table.
	def is_valid_answer(self, x: float) -> bool:
		return all((
			x not in self.current_table,
			x.is_integer(),
			x >= MIN_BOUND,
			x <= MAX_BOUND,
		))
	
	# Construct equation string by formatting the operator string with its operand(s).
	def eqn_str(self, str_oper: str, *args: str) -> str:
		if not args:
			return str_oper
		
		# Add parenthesis to any equation with 2 or more digits. This is to avoid unessecary 
		# parenthesis while still respecting operator precedence.
		operands = (f'({s})' if s.count(self.str_num) > 1 and s.count(self.str_num) != len(s) else s for s in args)
		eqn = str_oper.format(*operands)
		return eqn
	
	# Yields all addends a, b such that a+b == n
	def addends(self, n: int) -> Iterable[tuple[int, int]]:
		for i in range(1, n):
			yield (n - i, i)
	
	# Export solution as a text file.
	def export(self) -> None:
		t = self.eqn_tables[-1]
		solution_strs = []
		total_solutions = 0

		# Loop through all solutions and count how many solutions there are as 
		# well as format solution strings
		for n in range(MAX_BOUND + 1):
			if n in t:
				sol = f'{n} = {t[n]}'
				total_solutions += 1
			else:
				sol = f'{n}: no solution found'
			
			solution_strs.append(sol)

		# Open file and write header info.
		with open(f'{self.num}-{self.num}s.txt', 'w', encoding='utf-8') as txt:
			txt.write('-'*50 + f'\n{self.num} {self.num}\'s solutions\n' + '-'*50 + '\n')
			txt.write(f'{total_solutions}/{MAX_BOUND} solutions found ')
			txt.write(f'({100 * (total_solutions / MAX_BOUND):.2f}%)\n\n')

			# Display which operators we're used.
			txt.write('Operators used:\n')
			for str_oper, _ in BINARY_OPERS:
				txt.write(str_oper.format("x", "y") + '\n')
			for str_oper, _ in UNARY_OPERS:
				txt.write(str_oper.format("x") + '\n')
			
			# Display solutions.
			txt.write('-'*50 + '\n')
			for solution in solution_strs:
				txt.write(solution + '\n')


# Test.
if __name__ == '__main__':
	f = FourFours(6)
	f.export() 
		
		