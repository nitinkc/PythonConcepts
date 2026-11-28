# Foundations: values, control flow, and collections

Python programs manipulate **objects**. A variable is a name bound to an object; it is not a box that permanently
contains a value. This model explains assignment, mutability, function arguments, and copying.

## Basic values and types

| Category   | Built-in types            | Typical use                  |
|------------|---------------------------|------------------------------|
| Numeric    | `int`, `float`, `complex` | Counts and calculations      |
| Boolean    | `bool`                    | Conditions                   |
| Text       | `str`                     | Unicode text                 |
| Sequence   | `list`, `tuple`, `range`  | Ordered values               |
| Mapping    | `dict`                    | Key-value associations       |
| Set        | `set`, `frozenset`        | Unique values and membership |
| Null value | `None`                    | Absence of a value           |

- Inspect a value with `type(value)`. 
- Prefer explicit conversion—such as `int(text)`—at system boundaries rather than relying on implicit assumptions.
- Slicing uses `sequence[start:stop:step]`; `stop` is excluded. 
  - Negative indexes count from the end.


```python 
# { .python-runner title="Basic values experiment" }
name:str = "Ada" 
age:int = 36
flag:bool = True

# Type Hints
myList:List[int] = [1,2,3,"john"] # Python is dynamically typed, so it completely ignores "type hints" when running your code.
# For Static Type checking, use @typechecked `from typeguard import typechecked`
myList.append("new String")
for item in myList:
    print(item)
    
ordered = sorted(myList)

myTuple:Tuple = (1,2) # Immutable

myRange:int  = range(2,5)
first, *middle, last = myRange

# Curlies with Set and Dict
myDict:dict[str,int] = {"name": "Ada", "role": "engineer"}
role = myDict.get("role", "unknown")
print(role)
for key, value in myDict.items():
    print(key, value)

mySet: set[int] = {1, 2, 3}
for num in mySet:
    print(num)

print(type(myDict))
```

## Conditions and loops

Conditions use truth values. Empty collections, zero, `None`, and empty strings are false; most other objects are true.

```python
if not users:
    print("No users")
elif len(users) == 1:
    print("One user")
else:
    print(f"{len(users)} users")

for index, user in enumerate(users, start=1):
    print(index, user)
```

- `while` when repetition depends on state rather than on an iterable. 
- `break` exits a loop, 
- `continue` skips to its next iteration, and a loop's `else` block runs only when no `break` occurs.

## Choosing a collection

| Need                               | Use     | Important properties                    |
|------------------------------------|---------|-----------------------------------------|
| Ordered, changeable sequence       | `list`  | Duplicates allowed; fast append         |
| Fixed record or immutable sequence | `tuple` | Hashable when all elements are hashable |
| Key-value lookup                   | `dict`  | Insertion ordered; keys are unique      |
| Unique values or fast membership   | `set`   | Unordered; elements must be hashable    |

```python 
# { .python-runner title="Collection selection experiment" }
items = ["apple", "banana", "apple"]

# for item in set(items) -> get unique names from the set created with items
# and for each set value, count the number of items from the original items list -> items.count(item)
freq:dict[str,int] = {item: items.count(item) for item in set(items)}
print(freq) # {'banana': 1, 'apple': 2}
unique_items = set(items)
print(unique_items) # {'apple', 'banana'}
```

For counting real data, prefer `collections.Counter` over repeatedly calling `list.count`, which rescans the list.

## Mutability and identity

- `list`, `dict`, and `set` are **mutable**. 
- Numbers, strings, tuples, and frozen sets are **immutable**. 

Assignment ***_never_*** copies an object.

- Use `==` for value equality. 
- Use `is` for identity, most commonly `value is None`.

```python { .python-runner title="Mutability and identity experiment" }
original = [1, 2]
alias = original
alias.append(3)
assert original == [1, 2, 3]
assert alias is original
```


### Avoid shared mutable defaults

Default arguments are evaluated once when a function is defined.

```python
def add_item(item, items=None):
    if items is None:
        items = []
    items.append(item)
    return items
```

### Copy deliberately

```python
from copy import deepcopy

shallow = original.copy()  # nested objects remain shared
independent = deepcopy(original)
```

A comprehension also creates independent nested rows:

```python
grid = [[0] * 3 for _ in range(3)]
```

## Experiment: references and collections

Change the values, add a nested object, or replace the shallow copy with a different copying strategy.

```python { .python-runner title="References and collections experiment" }
original = {"languages": ["Python"], "active": True}
shallow = original.copy()
shallow["languages"].append("SQL")

print("original:", original)
print("shallow: ", shallow)
print("same dictionary:", original is shallow)
print("same nested list:", original["languages"] is shallow["languages"])
```

## Checkpoint

- Explain names, objects, equality, and identity.
- Choose between list, tuple, dictionary, and set.
- Predict whether an operation mutates an existing object.
- Avoid mutable default arguments and shared nested lists.
- Use control flow without unnecessary nesting.

**Next:** [Functions, scope, and modules](02_functions_scope_and_modules.md)
