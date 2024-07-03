class Target: #為客戶端代碼使用特定接口
    """
    The Target defines the domain-specific interface used by the client code.
    """ #目標定義了客戶端代碼使用的特定域接口

    def request(self) -> str:
        return "Target: The default target's behavior." #返回一個默認的行為描述


class Adaptee:
    """
    The Adaptee contains some useful behavior, but its interface is incompatible
    with the existing client code. The Adaptee needs some adaptation before the
    client code can use it.
    """ #Adaptee 包含一些有用的行為，但目前與現有的客戶端代碼不相容，在客戶端代碼使用Adaptee之前，需要進行調整

    #與Target 的接口不兼容

    def specific_request(self) -> str: 
        return ".eetpadA eht fo roivaheb laicepS" #返回一個倒敘的字串


class Adapter(Target, Adaptee):
    """
    The Adapter makes the Adaptee's interface compatible with the Target's
    interface via multiple inheritance.
    """ #Adapter 通過多重繼承使被適配者的接口與目標的接口兼容

    def request(self) -> str:
        return f"Adapter: (TRANSLATED) {self.specific_request()[::-1]}" #將字串反轉



def client_code(target: "Target") -> None: #接受一個實現Target接口的對象
    """
    The client code supports all classes that follow the Target interface.
    """ #客戶端代碼支持所有遵循目標的種類

    print(target.request(), end="")


if __name__ == "__main__":
    print("Client: I can work just fine with the Target objects:")
    target = Target()
    client_code(target)
    print("\n")

    adaptee = Adaptee()
    print("Client: The Adaptee class has a weird interface. "
          "See, I don't understand it:")
    print(f"Adaptee: {adaptee.specific_request()}", end="\n\n") 

    print("Client: But I can work with it via the Adapter:") #可以通過Adapter 使用他
    adapter = Adapter()
    client_code(adapter)