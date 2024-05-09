import signal
import os

class TimeoutExpired(Exception):
    pass

def communicate_with_timeout(proc, input=None, timeout=None):
    def _timeout_handler(signum, frame):
        raise TimeoutExpired()
    signal.signal(signal.SIGALRM, _timeout_handler)
    signal.alarm(timeout)

    try:
        stdoutdata, stderrdata = proc.communicate(input)
        signal.alarm(0)
        return stdoutdata, stderrdata
    except TimeoutExpired:
        os.killpg(proc.pid, signal.SIGKILL)
        raise
