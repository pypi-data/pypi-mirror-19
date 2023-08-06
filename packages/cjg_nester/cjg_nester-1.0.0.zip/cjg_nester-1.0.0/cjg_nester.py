Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:53:40) [MSC v.1500 64 bit (AMD64)] on win32
Type "copyright", "credits" or "license()" for more information.
>>> if 43>42:
	print("don't panic!")

	
don't panic!
>>> if 43>42:
	print("don't panic!")

	
don't panic!
>>> movie =["Nikita","Muly","2012-2-1"]
>>> print(movie[1])
Muly
>>> cast = ["Cleese","Palin","Jones","Idle"]
>>> print(cast)
['Cleese', 'Palin', 'Jones', 'Idle']
>>> print(len(cast))
4
>>> print(cast[1])
Palin
>>> cast.append("Gillian")
>>> print(cast )
['Cleese', 'Palin', 'Jones', 'Idle', 'Gillian']
>>> cast.pop()
'Gillian'
>>> print(cast )
['Cleese', 'Palin', 'Jones', 'Idle']
>>> cast.extend(["Gillian","Chapman"])
>>> print(cast)
['Cleese', 'Palin', 'Jones', 'Idle', 'Gillian', 'Chapman']
>>> cast.remove ("Chapman")
>>> print(cast)
['Cleese', 'Palin', 'Jones', 'Idle', 'Gillian']
>>> cast.insert(1,"ChenJin")
>>> print(cast)
['Cleese', 'ChenJin', 'Palin', 'Jones', 'Idle', 'Gillian']
>>> fav_movies = ["The Holy Grail","The Life of Brian"]
>>> for each-flick in fav_movies:
	print(each-flick)
	
SyntaxError: can't assign to operator
>>> count = 0
>>> while count<len(fav_movies):
	print(fav_movies[count])
	count = count + 1

	
The Holy Grail
The Life of Brian
>>> movies = ["The Holy Grail","1975","Terry","Join",["Champ","Text",["Chess","Hungry","Happy"]]]
>>> print(movie)
['Nikita', 'Muly', '2012-2-1']
>>> print(movies )
['The Holy Grail', '1975', 'Terry', 'Join', ['Champ', 'Text', ['Chess', 'Hungry', 'Happy']]]
>>> for each_items in movies:
	if isinstance(each_items,list)
	
SyntaxError: invalid syntax
>>> for each_items in movies:
	if isinstance(each_items,list)
	
SyntaxError: invalid syntax
>>> for each_items in movies:
	if isinstance(each_items,list):
		for nested_items in each_items:
			print(nested_items)
	else:
		print(each_items)

		
The Holy Grail
1975
Terry
Join
Champ
Text
['Chess', 'Hungry', 'Happy']
>>> for each_items in movies:
	if isinstance(each_items,list):
		for nested_items in each_items:
			if isinstance(nested_items,list):
				for every_items in nested_items:
					print(every_items)
			else:
				print(nested_items)
	else:
		print(each_items)

		
The Holy Grail
1975
Terry
Join
Champ
Text
Chess
Hungry
Happy
>>> 
>>> def print_lol(the_list):
	for each_items in the_list:
		if isinstance(each_items,list)
		
SyntaxError: invalid syntax
>>> def print_lol(the_list):
	for each_items in the_list:
		if isinstance(each_items,list):
			print_lol(each_items)
		else:
			print(each_items)

			
>>> print_lol(movies)
The Holy Grail
1975
Terry
Join
Champ
Text
Chess
Hungry
Happy
>>> def print_circle(the_list):
	for each_items in the_list:
		if isinstance(each_items,list)
		
SyntaxError: invalid syntax
>>> def print_circle(the_list):
	for each_items in the_list:
		if isinstance(each_items,list):
			print_circle(each_items)
		else:
			print(each_items)

			
>>> print_circle(movies)
The Holy Grail
1975
Terry
Join
Champ
Text
Chess
Hungry
Happy
>>> import nester
cast=["Palin","Cleese","Idle","Jones","Gilliam","Chapman"]
print_lol(cast)




