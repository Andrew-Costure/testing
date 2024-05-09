import subprocess
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

class Cmd:
    def __init__(self):
        self.test = 'test'

    # 执行非交互命令
    def run_cmd_with_timeout(self, cmd, timeout=None):
        p = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        
        try:
            stdout, stderr = communicate_with_timeout(p, timeout=timeout)
            result = stdout.decode('utf-8').strip()
        except TimeoutExpired:
            result = "Command execution timed out"
        
        return p.returncode, result

# Example usage:
if __name__ == "__main__":
    cmd_executor = Cmd()
    return_code, output = cmd_executor.run_cmd_with_timeout("sleep 5 && ls", timeout=10)
    print("Return Code:", return_code)
    print("Output:", output)
