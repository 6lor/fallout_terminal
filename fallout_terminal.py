from colorama import init
init()
from colorama import Fore, Back, Style
import json
import random
import time
import string
import os


class Terminal():
	def __init__(self, words, special, debug = False):
		random.shuffle(words)							# Shuffle the words list
		self.words = words[:10]							# Assign 10 random words
		self.special = special							# Assign duds to self
		self.w_to_output = self.words + self.special	# Combine words and duds
		random.shuffle(self.w_to_output)				# Shuffle the words and duds
		self.debug = debug
		self.victory = False							# Victory flag
		self.code = self.words[rand_num(0,9)]			# The key word
		self.turns = 4 									# Number of turns
		self.lines = self.screen(self.debug)						# Create screen
		self.user_input = ""							# User input variable
		self.out = ""									# Terminal output

	def add_turn(self, value = 1):						# Add a turn
		self.turns += value


	def remove_turn(self):								# Remove a trun
		self.turns -= 1
	

	def validate_input(self):							# Input validation with no loops 	
		word = input((" " * 42) +"> ").upper()
		self.user_input = word

		if word in self.words or word in self.special:
			total = 0
			if word == self.code:
				self.victory = True
				self.out = "Valid pass"
			elif word in self.special:
				for num,line in enumerate(self.lines["Code"]):
					if word in line:
						if "\x1b[37m" in line:
							self.lines["Code"][num] = self.lines["Code"][num].replace("\x1b[37m" + word, gen_char(len(word)))
						else:
							self.lines["Code"][num] = self.lines["Code"][num].replace(word, gen_char(len(word)))
							self.special.remove(word)
					else:
						pass
				self.out = "Dud accepted"
				self.add_turn()
			else:
				for i in word:
					for l in self.code:
						if i == l:
							total += 1
				
				self.out = "Likeness=" + str(total)
				self.remove_turn()
		else:
			self.out = "Not in terminal"
		
		self.add_past_line()


	def screen(self, debug = False):					# Screen generation
		rows = {}
		row_len = 12
		rows["Title"] = Fore.GREEN + "Welcome to ROBCO Industries (TM) Termlink\n\nPassword Required\n\n"
		rows["Code"] = [] # That is where the generated code go
		rows["IO"] = [" "]*16 # That is where the IO history goes

		for r in range(0,18): # Generate 9 rows with no words
			rows["Code"].append(gen_char(row_len))

		for num, word in enumerate(self.w_to_output,3): # Generate the main body
			l = gen_char(rand_num(0,(row_len - len(word)))) # Generate the number of characters to the left of the word
			r = gen_char(row_len - len(word) - len(l)) # Calculate the number of characters to the right

			if debug: # Custom coloring in case if the debug is enabled
				word = Fore.WHITE + word
				l = Fore.GREEN + l
				r = Fore.GREEN + r

			rows["Code"].append(l + word + r)

		random.shuffle(rows["Code"])
		return rows

	def __str__(self):									# String method
		to_return = self.lines['Title']
		to_return += 'Attempts Remaining: '
		for num in range(0,self.turns):
			to_return += '\u2588 '
		to_return +='\n'
		tmp = ""
		for num, item in enumerate(list(map(lambda x: x[0]+"  "+x[1], zip(memory_address,self.lines['Code']))),1):
			if num %2 == 0:
				tmp += item + '  ' + self.lines["IO"][int(num/2)-1] + "\n"
				to_return += tmp
			else:
				tmp = item + '  '

		return to_return[:len(to_return)]

	
	def add_past_line(self):							# Side stdout
		# Remove first two items from the list
		del self.lines["IO"][0]
		del self.lines["IO"][0]
		del self.lines["IO"][0]
		# Add user input
		self.lines["IO"].append(self.user_input)
		if not self.victory:
			self.lines["IO"].append("Access denied")
		else:
			self.lines["IO"].append("Access granted")
		# Add terminal result
		self.lines["IO"].append(self.out)


	def slow_print(self):
		tmp = str(self).split("\n")
		for line in tmp:
			for char in line:
				print(char, end="")
				time.sleep(0.001)
			print("\n", end="")


def clear():
	os.system('cls' if os.name == "nt" else 'clear')
		

def gen_char(chars = 1):								# Random character generation
	return ''.join(random.choices(string.digits + string.punctuation, k=chars)) #string.ascii_letters + 


def rand_num(low,high):									# Random number generation
	t = random.randint(low,high)
	return t


all_words = json.load(open("words.json", "r"))
memory_address = ["0x3700", "0x3701", "0x3702", "0x3703", "0x3704", "0x3705", "0x3706", "0x3707", "0x3708", "0x3709", "0x370A", "0x370B","0x370C", "0x370D", "0x370E", "0x370F", "0x3710", "0x3711", "0x3712", "0x3713", "0x3714", "0x3715",  "0x3716", "0x3717", "0x3718", "0x3719", "0x371A", "0x371B","0x371C", "0x371D", "0x371E", "0x371F"]

if __name__ == "__main__":
	try:
		term = Terminal(all_words["MEDIUM"], all_words["SPECIAL"],False) # Last value enables or disabes highlits for the words
		clear()
		term.slow_print()
		while term.turns > 0:
			clear()
			print(term,end = "")
			term.validate_input()
			if term.victory:
				break
		if term.victory:
			out = "Welcome!"
		else:
			out = "Terminal locked down"
		clear()
		print(str(term) + out,end = "")
		time.sleep(5)
		clear()

	except KeyboardInterrupt:
		clear()
		print("Thank you for playing safe!")





