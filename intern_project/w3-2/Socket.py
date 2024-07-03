# 歐規插座，一律為3孔
class European_Socket:
    def voltage(self):
        return 220

    def HoleNumber(self):
        return 3

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

# 測試
european_socket = European_Socket()
usa_socket1 = USA_Socket1()
usa_socket2 = USA_Socket2()

print(european_socket.HoleNumber())  # 輸出: 3
print(usa_socket1.HoleNumber())      # 輸出: 2
print(usa_socket2.HoleNumber())      # 輸出: 3
