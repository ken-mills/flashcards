# flashcards.py, see Readme

import csv
import os
import re
import sys
import json
import glob
import random

def get_alts(word, box):
	translations = []
	for w in box:
		try:
			if word == w[0]:
				translations.append(w[1])
		except:
			print("Error with csv file :", box )
	return translations

def is_correct(answer, alternates):
	if answer in alternates:
		return True
	return False

def has_multiple_translations(item):
	if len(item) > 1:
		return True
	return False

def purge_boxes(dir, pattern):
	for f in os.listdir(dir):
		if re.search(pattern, f):
#			print("Deleting...",os.path.join(dir, f))
			os.remove(os.path.join(dir, f))

def build_group_list(files):
	temp= []
	for count, f in enumerate(files):
		fname = f.split('.')
		temp.append([count,fname[0],f])
	return temp

def has_only_short_answers(possible_translations):
	for p in possible_translations:
		if len(p.split()) > 2:
			return False
	return True

def build_distractor_list(current_translation, box):
	temp = []
	for d in box:
		dd = d[1][0]
		l = len(dd.split())
		if l > 2 and dd != current_translation :
			temp.append(dd)
	return temp


cwd = os.getcwd()

mode = sys.argv[1]
if mode == "T":
	print("Testing mode")
	purge_boxes(cwd,'^box\d.json')

files = glob.glob('*.csv')

filelist = build_group_list(files)
for f in filelist:
	print(f[0],f[1])

group = int(input("Select a group of words to study. :"))

current_box = input('Which box would you like to study? (1,2,3): ')
current_box_int = int(current_box)

print("Working on box " + current_box)
current_box_path = cwd + '\\' + filelist[group][1] + current_box + '.json'
words_path = cwd + '\\' + filelist[group][2]

box = []

try:

	# read file
	with open(current_box_path, 'r') as json_file:
		data=json_file.read()

	# parse file
	box = json.loads(data)


except:
# 	No box 1! Might be test mode which deletes boxes.
	if current_box_int == 1:
		print("Creating box1 from", words_path)
		with open(words_path, newline='',encoding='utf-8') as csvfile:
			box = list(csv.reader(csvfile, delimiter=','))

		flip = input('Would you like to study the reverse translation? (Y/N): ')
		if flip == 'Y':
			flipped = []
			for word in box:
				flipped.append([word[1],word[0]])
			box = flipped.copy()

		#find words with multiple translations, in words .csv more than once.
		with_alternates = []
		for i in box:
			alts = get_alts(i[0],box)
			new = [i[0],alts]
			with_alternates.append(new)

		box = with_alternates.copy()

# Create box 1 json file.
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
		distractor_list = []
#		if a word has multiple translations, ask about each one.
#		when all translations are correct then move to the next box.
#		otherwise word remains in the box with all translations.
#		if a word has a long translation, build a list of distractors, display them,
#		and ask the user to pick the correct one.

		if has_only_short_answers(translations):

			if has_multiple_translations(translations):
				print()
				print(word, 'has',number_of_translations,'translations.')
			else:
				print()
				print(word, 'has one translation.')

			for trans in translations:
				answer = input('\t The translation is: ')
				if is_correct(answer, translations):
					print('Excellent!', translations, end='\n\n')
					number_correct += 1
				else:
					print('Boo!')
					number_wrong += 1
					if number_wrong <= number_of_translations:
						print("here you go:", translations, end='\n\n')

		else:
			#assuming a long answer has only one answer, show 4
			distractors = []
			distractor_list = build_distractor_list(translations[0], box)

			distractors.append(translations[0])
			x = slice(3)
			distractors.extend(distractor_list[x])
			random.shuffle(distractors)

			for count, distractor in enumerate(distractors):
				print(count, distractor)
			print('Translate: ', word )
			answer = int(input('Pick correct answer:'))

			if distractors.index(translations[0]) == answer:
				print('Excellent!', translations[0], end='\n\n')
				number_correct += 1
			else:
				print('Boo!',translations[0], end='\n')
				number_wrong += 1


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
	print("\nYou need to practice these words/phrases again: ")
	for practice in need_practice:
		print(practice[0], ',', end='')
	if current_box_int > 1:
		#Move items to
		print("Moving these words back to box ", str(current_box_int - 1))

		box_path = cwd + '\\' +filelist[group][1] + str(current_box_int - 1) + '.json'
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
	print("You seem to know these words/phrases: ", end='')
	for each_word in know:
		print(each_word[0], ',', end='')
	if current_box_int < 3:
		print("\nMoving these words to box ", str(current_box_int + 1))

		box_path = cwd + '\\' + filelist[group][1] + str(current_box_int + 1) + '.json'
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

