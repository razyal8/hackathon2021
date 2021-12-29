import threading

class gameMember:
  def __init__(self, name = None, conn  = None, port  = None):
    self.name = name
    self.conn = conn
    self.port = port


# class game:
#   def __init__(self) -> None:
  
#   lock = threading.Lock()
#   lock.acquire()
#   # increment()
#   lock.release()