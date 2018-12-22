from subprocess import Popen, PIPE

from common import logger

# this is a synchronous function which calls process and returns exitcode, stdout and stderr
def call(args):
    p = Popen(args, stdout=PIPE, stderr=PIPE)
    logger.debug('call :: PID: %d, command: "%s"' % (p.pid, ' '.join(args)))
    stdout = p.stdout.read().decode('utf-8')
    p.stdout.close()
    logger.debug('call :: PID: %d, stdout: "%s"' % (p.pid, stdout))
    stderr = p.stderr.read().decode('utf-8')
    p.stderr.close()
    if stderr.strip():
        logger.error('call :: PID: %d, stderr: "%s"' % (p.pid, stderr))
    exitcode = p.wait()
    logger.debug('call :: PID: %d, errorcode: %d' % (p.pid, exitcode))
    return [exitcode, stdout, stderr]
