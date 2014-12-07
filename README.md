pyvenv .
source bin/activate
pip install xxx

deactivate

pip freeze > requirements.txt

pip install -r requirements.txt

Sequence Types
List:  [1, 2, 3]   -> mutable
Tuple: (1, 2, 3)   -> inmutable
Range: range(x, y) -> inmutable (es más bien como un tuple)

List comprehension
>>> [x**2 for x in range(0, 10)]
[0, 1, 4, 9, 16, 25, 36, 49, 64, 81]

>>>[(x, x**2) for x in range(0, 10)]
[(0, 0), (1, 1), (2, 4), (3, 9), (4, 16), (5, 25), (6, 36), (7, 49), (8, 64), (9, 81)]

Set comprehension
>>> {x for x in 'abracadabra' if x not in 'abc'}
{'r', 'd'}

Dict comprehension
>>> {x: x**2 for x in (2, 4, 6)}
{2: 4, 4: 16, 6: 36}

Sequence unpacking
x, y, z = (1, 2, 3)
u, v = [1, 2]

Sets (no hay repeticion de elementos)
>>> {'apple', 'orange', 'apple', 'pear', 'orange', 'banana'}
{'orange', 'banana', 'pear', 'apple'}

Dictionary (php: associative array, js: object)
>>> {'a': 1}
{'a': 1}
>>> dict(sape=4139, guido=4127, jack=4098)
{'sape': 4139, 'jack': 4098, 'guido': 4127}
>>> dict([('sape', 4139), ('guido', 4127), ('jack', 4098)])
{'sape': 4139, 'jack': 4098, 'guido': 4127}

Key puedes ser cualquier inmutable

OK:
>>> {(1,2): 1}
>>> {1: 1}
>>> {"a":1}

NO OK:
>>> {[1,2]:1}
>>> {(1, [2,3]): 1}
>>> {{'a': 1}: 2}

Looping List/Tuples/Sets:

for i, v in enumerate(['a', 'b', 'c']):
    print(i, v)

Looping Dicts:

for k, v in dict.items():
    print(k, v)

for k in sorted(dict.keys()):
    print(k, dict[k])

.keys()  => list of keys
.items() => list of (k, v) tuples

Looping with ZIP, REVERSED, SORTED:

>>> questions = ['name', 'quest', 'favorite color']
>>> answers = ['lancelot', 'the holy grail', 'blue']
>>> for q, a in zip(questions, answers):
...     print('What is your {0}?  It is {1}.'.format(q, a))
...
What is your name?  It is lancelot.
What is your quest?  It is the holy grail.
What is your favorite color?  It is blue.

>>> for i in reversed(range(1, 10, 2)):
...     print(i)
...
9
7
5
3
1

>>> basket = ['apple', 'orange', 'apple', 'pear', 'orange', 'banana']
>>> for f in sorted(set(basket)):
...     print(f)
...
apple
banana
orange
pear
