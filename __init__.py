from collections import abc
import inspect

# This class acts as a dictionary with the special property of raising a name error instead  of a key error
class DynamicScope(abc.Mapping):
    # Initilize the function with the dynamic_scope dictionary
    def __init__(self):
        self.dynamic_scope = {}
    # Uses the dictionary iterator method 
    def __iter__(self):
        return self.dynamic_scope.__iter__()
    
    #Special Get item that returns the name error instead of the key error  
    def __getitem__(self, key):
        # If the scope contains the key, return the key as normal
        if self.dynamic_scope.__contains__(key):
            return self.dynamic_scope.__getitem__(key)
        # If the key isnt contained, raise name error
        raise NameError(f"Name '{key}' is not defined.")

    # All of theese functions make calls to the dictionary to do it for them and have that return       
    def __len__(self):
        return self.dynamic_scope.__len__()
    def __setitem__(self, key, value):
        return self.dynamic_scope.__setitem__(key,value)
    def __delitem__(self,item):
        return self.dynamic_scope.__delitem__(item)
    def __contains__(self,key):
        return self.dynamic_scope.__contains__(key)


# This function compeltes the task in the lab to create a dynamic scope 
def get_dynamic_re()->dict:
        # Creating the dynamic scope object (Dict with special properties)
        dynamic_re = DynamicScope()

        # Observation of the stack 
        stack = inspect.stack(context=1)

        # Creating the coutner for the loop, starts at one because the 0th call is the call to get dynamic_re
        counter = 1
        
        # Loop runs until the __name__ is contained in the local vars. This happens at the bottom of the stack
        while  "__name__" not in stack[counter][0].f_locals:

            # Retreive the local varaibls from this call in the stack
            local_vars = stack[counter][0].f_locals

            # Retreive the free variables from this call in the stack
            free_var = list(stack[counter][0].f_code.co_freevars)

            # Iterates throgh all of the local variables
            for item in local_vars:
                # If the local variable is already in the Dynamic scope, that means a previous call has already added it so it should not be added again
                if(item not in dynamic_re):
                    # If the item is not a free variable then it can be added
                    if(item not in free_var):
                        # Add the the key and value to the dynamic scope
                        dynamic_re[item] = local_vars[item]

            # Iterate one more time through the loop
            counter += 1
        
        # Return the completed dynamic scope
        return dynamic_re


    

    
