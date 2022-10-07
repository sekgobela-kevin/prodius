# prodius
Calculating cartesian product is not easy if not using `itertools.product()`.
Prodius library allows to perform the same but also allowing iterables to
be callables that return iterable. Provided callables will be called when
iterable is needed to calculate cartesian product.

`itertools.product()` ofsen raise MemoryError when one of iterables is too
large. No matter matter the size of iterable, prodius will never write 
whole iterator into memory.

### Issues
- Iterables cannot be more than 11.
- Maybe be slower than `itertools.product()`.

### Installing
Prodius can be installed with pip in your command-line.
```bash
pip install prodius
```

### Usage
Prodius is just easy just like builtin `itertools.product()`.

Realise that this wont offer any benefit as iterator are passed direcly.
```python
import prodius

iterables = [range(10), range(10)]
for item in prodius.product(*iterables, repeat=2):
    print(item)
```


Prodius also allows iterables to contain callable that returns iterable.

The difference is that functions were used as iterables which provide
iterables on demand.
```python
import prodius

iterables = [lambda: range(10), lambda: range(10)]
for item in prodius.product(*iterables, repeat=2):
    print(item)
```

This compares `itertools.product()` with `prodius.product()`.
```python
import prodius

# prodius.product() is used to calculate cartesian product.
# No exception or MemoryError expected even if iterables are large.
iterables = [lambda: range(10**15), lambda: range(10**15)]
product = prodius.product(*iterables) # works as espected
```
```python
import itertools

# itertools.product() is used to calculate cartesian product.
# MemoryError expected as iterables are too large.
iterables = [range(10**15), range(10**15)]
product = itertools.product(*iterables) # MemoryError
```

Prodius also gives control of over items of iterable to be used in cartesian
product. That could be accomplised using `itertools.cycle()` by returning
different iterable each time function is called.
```python
import prodius
import itertools

foods_numbers_list = [[1,2], ["apple", "orange"]]
foods_numbers_cycle = itertools.cycle(foods_numbers_list)

def numbers_foods():
    return next(foods_numbers_cycle)

for item in prodius.product([100, 200], numbers_foods):
    print(item)
# (100, 1)
# (100, 2)
# (200, 'apple')
# (200, 'orange')
```
Notice that `100` was matched with numbers `(1, 2)` while `200` matched with
`('apple', 'orange')`. 

Thats a fantastic trick with prodius even if it does not have realworld 
application but who knows.

### License
[MIT license](https://github.com/sekgobela-kevin/prodius/blob/main/LICENSE)
