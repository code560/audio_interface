import datetime
import thread


def i(msg):
    log('INFO', msg)


def w(msg):
    log('WARN', msg)


def e(msg):
    log('ERR', msg)


def d(msg):
    log('Debug', msg)
    pass


def log(tag, msg):
    print("[{0}] {1}({2}): {3}".format(
        tag, datetime.datetime.today(), thread.get_ident(), msg))
    pass
