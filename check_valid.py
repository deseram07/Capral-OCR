#performs validation and corrects ID if possible
#
#Author: Buddhika De Seram

def check(id):
	flag = 1
	final = 0
	pos = 0
	position = 0
	alternative = []
	possible = []
	while flag:

		# if number of characters in ID is less than 4, wrong detection
		if len(id) < 4:
			# print 'here'
			flag = 0
			break

			#list of possible solutions
		no_matches = []		#count of how many matches in list possible
		f = open('E:\\Code\\Capral-OCR\\database\\available.txt', 'r')

		data = f.readlines()
		for i in data:
			i = i.strip('\n')
			# first check: is length of item in database same as id detected
			if len(i) == len(id) or len(i) == len(id)+1:
				possible.append(i)
		# print possible
			
		if len(possible) == 0:
			break
		# second check: check if detected in one go
		for i in possible:
			if id == i:
				# print "Matched"
				final = 1
				flag = 0
				break
		# third check: check every character select most matching item in sequence
		
		highest_match = 0	#current highest match

		#in the list of possible, every number is iterated in order to look for matches, matches are recorded in no_matches
		for i in possible:
			match = 0
			x = 0
			for j in id:
				if i[x] == j:
					match+=1
				x+=1
			no_matches.append(match)

			#list of closest results

		for i in no_matches:
			if i > highest_match:
				highest_match = i
				pos = position
				alternative = []
			if i == highest_match:
				alternative.append(possible[position])		#list alternative is appended with ID that has the highest matches. number of matches are all same
			position += 1
		
		#decides the number of allowed errors
		if len(id)>5:
			error = 3
		else:
			error = 2

		

		if no_matches[pos] > (len(id) - error):
			final = 1
			break
		elif len(alternative) != 1 and no_matches[pos] > (len(id) - error-1):	#if there is more than one alternative, display error and store alternatives in a txt file
			final = 0
			break
		else:
			final = 0
			break
	if pos == 0:
		possible.append('None')
	return (final, alternative, possible[pos])
