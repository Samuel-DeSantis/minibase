def singularize(word):
	if 'ies' in word:
		return word[:-3] + 'y'
	elif 'es' in word:
		return word[:-2]
	else:
		return word[:-1]
	
def pluralize(word):
	if word[-1] == 'y' and word[-2] not in 'aeiou':
		return word[:-1] + 'ies'
	elif word[-1] in 'sxz' or word[-2:] in ['sh', 'ch']:
		return word + 'es'
	else:
		return word + 's'