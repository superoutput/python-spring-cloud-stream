import logging
import os
from subprocess import Popen, PIPE
import subprocess
import time

from py4j.java_gateway import (
    JavaGateway, GatewayParameters, find_jar_path, OutputConsumer,
    ProcessConsumer, quiet_close)

logger = logging.getLogger("")

# NOTE 1 - This is a copy of py4j.java_gateway.launch_gateway with the addition of the return_proc parameter.
def launch_gateway(port=0, jarpath="", classpath="", javaopts=[],
                   die_on_exit=False, redirect_stdout=None,
                   redirect_stderr=None, daemonize_redirect=True,
                   java_path="java", create_new_process_group=False,
                   enable_auth=False, return_proc=False):
    """Launch a `Gateway` in a new Java process.

    The redirect parameters accept file-like objects, Queue, or deque. When
    text lines are sent to the stdout or stderr of the child JVM, these lines
    are redirected to the file-like object (``write(line)``), the Queue
    (``put(line)``), or the deque (``appendleft(line)``).

    The text line will contain a newline character.

    Only text output is accepted on stdout and stderr. If you wish to
    communicate with the child JVM through bytes, you need to create your own
    helper function.

    :param port: the port to launch the Java Gateway on.  If no port is
        specified then an ephemeral port is used.
    :param jarpath: the path to the Py4J jar.  Only necessary if the jar
        was installed at a non-standard location or if Python is using
        a different `sys.prefix` than the one that Py4J was installed
        under.
    :param classpath: the classpath used to launch the Java Gateway.
    :param javaopts: an array of extra options to pass to Java (the classpath
        should be specified using the `classpath` parameter, not `javaopts`.)
    :param die_on_exit: if `True`, the Java gateway process will die when
        this Python process exits or is killed.
    :param redirect_stdout: where to redirect the JVM stdout. If None (default)
        stdout is redirected to os.devnull. Otherwise accepts a
        file descriptor, a queue, or a deque. Will send one line at a time
        to these objects.
    :param redirect_stderr: where to redirect the JVM stdout. If None (default)
        stderr is redirected to os.devnull. Otherwise accepts a
        file descriptor, a queue, or a deque. Will send one line at a time to
        these objects.
    :param daemonize_redirect: if True, the consumer threads will be daemonized
        and will not prevent the main Python process from exiting. This means
        the file descriptors (stderr, stdout, redirect_stderr, redirect_stdout)
        might not be properly closed. This is not usually a problem, but in
        case of errors related to file descriptors, set this flag to False.
    :param java_path: If None, Py4J will use $JAVA_HOME/bin/java if $JAVA_HOME
        is defined, otherwise it will use "java".
    :param create_new_process_group: If True, the JVM is started in a new
        process group. This ensures that signals sent to the parent Python
        process are not forwarded to the JVM. For example, sending
        Ctrl-C/SIGINT won't interrupt the JVM. If the python process dies, the
        Java process will stay alive, which may be a problem for some scenarios
        though.
    :param enable_auth: If True, the server will require clients to provide an
        authentication token when connecting.
    :param return_proc: If True, returns the Popen object returned when the JVM
        process was created.

    :rtype: the port number of the `Gateway` server or, when auth enabled,
            a 2-tuple with the port number and the auth token.
    """
    popen_kwargs = {}

    if not jarpath:
        jarpath = find_jar_path()

    if not java_path:
        java_home = os.environ.get("JAVA_HOME")
        if java_home:
            java_path = os.path.join(java_home, "bin", "java")
        else:
            java_path = "java"

    # Fail if the jar does not exist.
    if not os.path.exists(jarpath):
        raise Py4JError("Could not find py4j jar at {0}".format(jarpath))

    # Launch the server in a subprocess.
    classpath = os.pathsep.join((jarpath, classpath))
    command = [java_path, "-classpath", classpath] + javaopts + \
              ["py4j.GatewayServer"]
    if die_on_exit:
        command.append("--die-on-broken-pipe")
    if enable_auth:
        command.append("--enable-auth")
    command.append(str(port))
    logger.debug("Launching gateway with command {0}".format(command))

    # stderr redirection
    close_stderr = False
    if redirect_stderr is None:
        stderr = open(os.devnull, "w")
        close_stderr = True
    elif isinstance(redirect_stderr, Queue) or\
            isinstance(redirect_stderr, deque):
        stderr = PIPE
    else:
        stderr = redirect_stderr
        # we don't need this anymore
        redirect_stderr = None

    # stdout redirection
    if redirect_stdout is None:
        redirect_stdout = open(os.devnull, "w")

    if create_new_process_group:
        popen_kwargs.update(get_create_new_process_group_kwargs())

    proc = Popen(command, stdout=PIPE, stdin=PIPE, stderr=stderr,
                 **popen_kwargs)

    # Determine which port the server started on (needed to support
    # ephemeral ports)
    _port = int(proc.stdout.readline())

    # Read the auth token from the server if enabled.
    _auth_token = None
    if enable_auth:
        _auth_token = proc.stdout.readline()[:-1]

    # Start consumer threads so process does not deadlock/hangs
    OutputConsumer(
        redirect_stdout, proc.stdout, daemon=daemonize_redirect).start()
    if redirect_stderr is not None:
        OutputConsumer(
            redirect_stderr, proc.stderr, daemon=daemonize_redirect).start()
    ProcessConsumer(proc, [redirect_stdout], daemon=daemonize_redirect).start()

    if close_stderr:
        # XXX This will quiet ResourceWarning in Python 3.5+
        # This only close the fd in this process, not in the JVM process, which
        # makes sense.
        quiet_close(stderr)

    if enable_auth:
        output = (_port, _auth_token)
    else:
        output = _port

    if return_proc:
        if isinstance(output, tuple):
            output = output + (proc, )
        else:
            output = (_port, proc)

    return output


# NOTE 2: this is a copy of JavaGateway.launch_gateway with the addition of return_proc
def get_java_gateway(
        port=0, jarpath="", classpath="", javaopts=[],
        die_on_exit=False, redirect_stdout=None,
        redirect_stderr=None, daemonize_redirect=True, java_path="java",
        create_new_process_group=False, enable_auth=False):
    _ret = launch_gateway(
        port, jarpath, classpath, javaopts, die_on_exit,
        redirect_stdout=redirect_stdout, redirect_stderr=redirect_stderr,
        daemonize_redirect=daemonize_redirect, java_path=java_path,
        create_new_process_group=create_new_process_group,
        enable_auth=enable_auth, return_proc=True)

    if enable_auth:
        _port, _auth_token, proc = _ret
    else:
        _port, proc, _auth_token = _ret + (None, )
    gateway = JavaGateway(
        gateway_parameters=GatewayParameters(port=_port,
                                                auth_token=_auth_token))
    # NOTE 3: the Popen object is now available with gateway._proc
    gateway._proc = proc
    return gateway


def main():
    for i in range(10):
        gateway = get_java_gateway(die_on_exit=True)
        print(gateway.jvm.System.currentTimeMillis())
        gateway.shutdown()

        # NOTE 4: This is how you can send a newline and terminate the process
        gateway._proc.stdin.write("\n".encode("utf-8"))
        gateway._proc.stdin.flush()
        
        # NOTE 5: Alternatively terminate the process with the terminate signal
        # gateway._proc.terminate()

        # NOTE 6: in a next release, I would probably do it this way:
        # gateway.shutdown(terminate_launched_jvm=True)

    # NOTE 7: just to let you check that no processes are left running at this point...
    time.sleep(40)


if __name__ == "__main__":
    main()