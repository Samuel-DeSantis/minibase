def singularize(word):
	irregular_plurals = {
        'people': 'person',
        'men': 'man',
        'children': 'child',
        'teeth': 'tooth',
        'feet': 'foot',
        'mice': 'mouse',
        'geese': 'goose',
        'data': 'datum'
    }

	if word.lower() in irregular_plurals:
		return irregular_plurals[word.lower()]

	# Rules for regular plurals
	if word.lower().endswith('ies'):
		return word[:-3] + 'y'
	elif word.lower().endswith('es'):
		if word.lower().endswith('sses') or word.lower().endswith('ches') or word.lower().endswith('shes') or word.lower().endswith('xes'):
			return word[:-2]
		elif word.lower().endswith('ves'):
			return word[:-3] + 'f'
		else:
			return word[:-1]
	elif word.lower().endswith('s'):
		return word[:-1]
	else:
		return word  # Word is already singular