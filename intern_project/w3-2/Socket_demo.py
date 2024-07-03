# 歐規插座，一律為3孔，省略 HoleNumber 方法
class European_Socket:
    def voltage(self):
      return 220

# 美規插座，有2孔/3孔
class USA_Socket1:
    def voltage(self):
      return 110

    def HoleNumber(self):
      return 2

class USA_Socket2:
    def voltage(self):
      return 110

    def HoleNumber(self):
      return 3
    
# 配接器
class Adapter(European_Socket):
    __socket = None
    def __init__(self, socket = None):
      self.__socket = socket
   
    def HoleNumber(self):
      # 是否為歐規
      if self.__socket is None or isinstance(self.__socket, European_Socket):
        return 3
        
      return self.__socket.HoleNumber()
    

# 測試      
socket = USA_Socket1()
adapter = Adapter(socket)
print(adapter.HoleNumber())
      
adapter2 = Adapter()     # 由於_socket=None，因此輸出會為3
print(adapter2.HoleNumber())