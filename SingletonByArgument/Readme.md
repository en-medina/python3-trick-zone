# Singleton By Argument
## Explanation
Here is implemented a thread-safe singleton by argument metaclass. As is by argument, it create a new instance of a class object if and only if  it is the first time you call that class with that unique arguments arragement. 

## Case of use
You might want to use this metaclass in a thread based environment where it necessary to share differents resources that implement the same class but defer in its initialization with the passed arguments, like database objects or I/O objects. 
