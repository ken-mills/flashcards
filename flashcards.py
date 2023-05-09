# Displays words from csv file and asks user to translate the word
# If correct, move word to next box of 3 boxes
# study box 1 every day, study box 2 every 2 days, study box 3 every 5 days
# when using windows 10 command line python must run in utf-8 mode using one of two approaches
# 	You can use the Python UTF-8 Mode to change the default text encoding to UTF-8. You can enable the Python UTF-8 Mode via the -X utf8 command line option, #   or the PYTHONUTF8=1 environment variable.
# Boxes are stored as json files and processed as lists


import csv
import os
import re
import sys
import json
import glob

def get_alts(word, box):
	translations = []
	for w in box:
		if word == w[0]:
			translations.append(w[1])
	return translations

def is_correct(answer, alternates):
	if answer in alternates:
		return True
	return False
	
def has_multiple_translations(item):
	if len(item[1]) > 1:
		return True
	return False
	
def purge_boxes(dir, pattern):
	for f in os.listdir(dir):
		if re.search(pattern, f):
#			print("Deleting...",os.path.join(dir, f))
			os.remove(os.path.join(dir, f))
	

cwd = os.getcwd()

mode = sys.argv[1]
if mode == "T":
	print("Testing mode")
	purge_boxes(cwd,'^box\d.json')


current_box = input('Which box would you like to study (1,2,3)?: ')
current_box_int = int(current_box)

print("Working on box " + current_box)
current_box_path = cwd + '\\box' + current_box + '.json'
words_path = cwd + '\\words.csv'

#print(current_box_path)
box = []

try:

#	print("opening box ")

	# read file
	with open(current_box_path, 'r') as json_file:
		data=json_file.read()

	# parse file
	box = json.loads(data)
	

except:

	if current_box_int == 1:
#		print("Creating box1 from words file.")
		with open(words_path, newline='',encoding='utf-8') as csvfile:
			box = list(csv.reader(csvfile, delimiter=','))

		#find words with multiple translations, in words .csv more than once.	
		with_alternates = []
		for i in box:
			alts = get_alts(i[0],box)
			new = [i[0],alts]
			with_alternates.append(new)
#			if len(alts) > 1:
#				print(new)
#				print('\n')

		box = with_alternates.copy()
			
		with open(current_box_path, 'w', encoding='utf-8') as f:
			json.dump(with_alternates, f, ensure_ascii=False, indent=3)

#Review mode just lists 20 words in box 1 for review
if mode == 'R':
	print("Review mode", end='\n\n')
	for x in range(20):
		print('Word:', box[x][0], 'translates to: ',end='')
		resultString = ', '.join(box[x][1])
		print(resultString, end='\n')
	sys.exit()

try:
	i = 0
	answer = ''
	know = []
	need_practice = []
	keep_in_box = []
	
	if len(box) == 0:
		print("Sorry this box is empty")
	
	while i < len(box):
		item = box[i]
		word = box[i][0]
		translations = box[i][1]
		number_of_translations = len(translations)
		translation_index = 0
		number_correct = 0
		number_wrong = 0
#		if a word has multiple translations, ask about each one.
#		when all translations are correct then move to the next box.
#		otherwise word remains in the box with all translations.		
		if has_multiple_translations:
			print()
			print(word, 'has',number_of_translations,'translations.')
		
		for trans in translations:
			answer = input('\t translation: ')
			if is_correct(answer, translations):
				print('Excellent!',end='\n')
				number_correct += 1
			else:
				print('Boo!\n')
				number_wrong += 1
				if number_wrong <= number_of_translations:
					print("here you go:", translations, end='\n')
				
		if number_correct == number_of_translations:
			know.append(box[i])
			if current_box_int == 3:
				keep_in_box.append(box[i])
		else:
			need_practice.append(box[i])
			if current_box_int == 1:
				keep_in_box.append(box[i])

		i += 1
except KeyboardInterrupt:
	pass
	
#put box back together by getting slice of box not shown
remaining_items = box[i:]
keep_in_box.extend(remaining_items)

if False:
	if len(keep_in_box) > 0:
		for x in range(10):
			print()
			print(keep_in_box[x][0],',',end='')


	
#list of words that need practice
if len(need_practice) > 1 :
	print()
	print("\nYou need to practice these words again: ")
	for practice in need_practice:
		print(practice[0], ',', end='')
	if current_box_int > 1:
		#Move items to 
		print("Moving these words back to box ", str(current_box_int - 1))

		box_path = cwd + '\\box' + str(current_box_int - 1) + '.json'
		other_box = []
		with open(box_path, 'r') as json_file:
			data=json_file.read()
			# creat list from other box
			other_box = json.loads(data)

			#extend the list, don't use append or insert on list of lists 
			need_practice.extend(other_box)

		with open(box_path, 'w', encoding='utf-8') as f:
			json.dump(need_practice, f, ensure_ascii=False, indent=3)	
		
	print()
	
# process the list of words you know
if len(know) > 1 :
	print()
	print("You seem to know these words: ", end='')
	for each_word in know:
		print(each_word[0], ',', end='')
	if current_box_int < 3:
		print("\nMoving these words to box ", str(current_box_int + 1))

		box_path = cwd + '\\box' + str(current_box_int + 1) + '.json'
		other_box = []
		try:
			with open(box_path, 'r') as json_file:
				data=json_file.read()
				# creat list from other box
				other_box = json.loads(data)
		except:
			print("Creating new box")

		#extend the list, don't use append or insert on list of lists 
		other_box.extend(know)
		
		with open(box_path, 'w', encoding='utf-8') as f:
			json.dump(other_box, f, ensure_ascii=False, indent=3)	
		f.close()

		print()

#write out current contents of box after making moves from current box
with open(current_box_path, 'w', encoding='utf-8') as f:
	json.dump(keep_in_box, f, ensure_ascii=False, indent=3)	

