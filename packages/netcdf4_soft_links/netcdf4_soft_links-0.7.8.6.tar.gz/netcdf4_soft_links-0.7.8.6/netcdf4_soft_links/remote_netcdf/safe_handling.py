#External:
import os

# Define a context manager to suppress stdout and stderr.
#http://stackoverflow.com/questions/11130156/suppress-stdout-stderr-print-from-python-functions
class suppress_stdout_stderr(object):
    '''
    A context manager for doing a "deep suppression" of stdout and stderr in 
    Python, i.e. will suppress all print, even if the print originates in a 
    compiled C/Fortran sub-function.
       This will not suppress raised exceptions, since exceptions are printed
    to stderr just before a script exits, and after the context manager has
    exited (at least, I think that is why it lets exceptions through).      

    '''
    def __init__(self):
        # Open a pair of null files
        self.null_fds =  [os.open(os.devnull,os.O_RDWR) for x in range(2)]
        # Save the actual stdout (1) and stderr (2) file descriptors.
        self.save_fds = (os.dup(1), os.dup(2))
        #print(self.null_fds,self.save_fds)
        return

    def __enter__(self):

        # Assign the null pointers to stdout and stderr.
        for id in range(2):
            os.dup2(self.null_fds[id],id+1)
        return

    def __exit__(self, *_):
        for id in range(2):
            # Re-assign the real stdout/stderr back to (1) and (2)
            os.dup2(self.save_fds[id],id+1)
        return

    def close(self):
        for id in range(2):
            # Close the null files
            os.close(self.null_fds[id])
        #Close the duplicates:
        #Very important otherwise "too many files open"
        map(os.close,self.save_fds)
        return

class dummy_semaphore:
    def acquire(self):
        return 
    def release(self):
        return

