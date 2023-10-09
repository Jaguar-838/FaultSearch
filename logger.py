import sys

class Logger(object):

    def __init__(self, _dir, _fname):
        self.log_dir = _dir
        self.full_name = _fname
        self.f = None

    def open(self):
        self.f = open(self.full_name, "w")

    def log(self, msg):
        #sys.stdout.write(msg)
        #sys.stdout.flush()
        self.f.write(msg)

    def close(self):
        self.f.close()
        
    def say(self, msg):
        sys.stdout.write(msg)
        sys.stdout.flush()

