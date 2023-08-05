from jug import TaskGenerator
@TaskGenerator
def jug_system(args, check_exit=True, return_token=False, run_after=None):
    '''jug_system(['/usr/bin/echo', 'Hello', 'World'], check_exit=True, return_token=False, run_after=None)

    A variation on `os.system` using jug

    Parameters
    ----------

    args : list of str
        args[0] should be the executable to call
    check_exit : bool, optional
        By default, checks the return value of the command (which should be zero).
    return_token : bool, optional
        By default, this function returns None, but if `return_token` is true,
        then it returns a token to be used with `run_after`
    run_after : anything
        This argument is ignored, but see below why it's useful:

    Example
    -------

    Run a simple command::

        jug_system(['echo', 'Hello', 'World'])

    Run two commands, so that the second only runs after the first::

        token = jug_system(['bash', '-c', "sort input.txt > output.txt"], return_token=True)
        jug_system(['bash', '-c', "wc -l output.txt > nl.txt"], run_after=token)

    '''
    import subprocess
    ret = subprocess.call(args)
    if check_exit and ret != 0:
        raise SystemError("Error in system")
    if return_token:
        from jug.hash import hash_one
        return hash_one(('jug_system', 'output_hash', args))


