This package provides a pythonic way to organize dumping and pulling python objects and other type of files to a folder or a directory that is called repository.
A Repository can be created in any directory or folder, it suffices to initialize a Repository instance in a directory to start dumping and pulling object into it. .
Any directory or a folder that contains a .pyrepinfo binary file in it, is theoretically a pyrep Repository.By default dump and pull methods use pickle to serialize storing python objects.
Practically any other methods can be used simply by providing the means and the required libraries in a simple form of string.

