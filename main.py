import code
from minibase.database import Database

db = Database()

code.interact(local=locals())


# db.table('users').create(
#   columns=[
#     ['name', 'text'],
#     ['age', 'integer']
#   ]
# )

# db.table('users').record.create(['John Doe', 30])
# db.table('users').record.create(['Jane Doe', 25])
# db.table('users').record.create(['Alice', 35])

# db.table('users').record.create(['Bill', 54])

# print(db.table('users').record.update(4, ['name'], ['Bill']))

# print(db.table('users').record.read(4))

# print(db.table('users').record.update(4, ['name'], ['William']))


# class Configuration:
#   def __init__(self, a=1, b=2, c=3):
#     self.a = a
#     self.b = b
#     self.c = c

#   def set(self):
#     return self.a, self.b, self.c

# class A(Configuration):
#   def __init__(self, *args):
#     super().__init__(*args)

# class Configuration:
#     def __init__(self, a=1, b=2, c=3, **kwargs):
#         self.a = a
#         self.b = b
#         self.c = c
#         # Store any additional keyword arguments for potential future use
#         self._extra_config = kwargs  # Or just 'self.extra = kwargs'

#     # def set(self):
#     #     return self.a, self.b, self.c

#     # def update(self, **kwargs):
#     #     """Update configuration attributes."""
#     #     for key, value in kwargs.items():
#     #         if hasattr(self, key):  # Check if the attribute exists
#     #             setattr(self, key, value)
#     #         else:
#     #             # Handle unknown attributes (e.g., store in _extra_config, raise error, etc.)
#     #             self._extra_config[key] = value # Example: store in extra config
#     #             #Or raise an exception:
#     #             #raise AttributeError(f"Configuration has no attribute '{key}'")

# class A(Configuration):
#     def __init__(self,**kwargs): #  *args, 
#         # Extract configuration-related kwargs
#         # config_kwargs = {k: kwargs.pop(k) for k in list(kwargs) if k in ['a', 'b', 'c']}
#         super().__init__(**kwargs) # Pass config and remaining kwargs

#         # Any other initialization for A that is not configuration
#         self.name = kwargs.get('name', "DefaultName") # Example

# a = A(a=5)
# print(a.a)
# print(a.b)
# print(a.c)