import socket
import sys
import time

from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal, QThread

from GUI_Designer_Controller import Ui_MainWindow

class UDPReceiver(QThread):
    data_received = pyqtSignal(str)  # 데이터 수신 시그널 정의

    def __init__(self, ip, port):
        super().__init__()
        self.ip = ip
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('166.79.25.100', self.port))  # 12345 포트에서 수신
        self._running = True

    def run(self):
        while self._running:
            try :
                data, _ = self.sock.recvfrom(1024)  # 최대 1024바이트 수신
                self.data_received.emit(data.decode('utf-8'))  # 데이터 수신 시그널 발생
            except Exception as e :
                self.data_received.emit(f"Error: {str(e)}")
            time.sleep(0.1)

    def stop(self):
        self._running = False
        self.sock.close()

    def senddata(self, target: tuple, msg: str) -> None:
        self.sock.sendto(msg.encode(), target)

class ControllerGUI:
    def __init__(self):
        super().__init__()
        app = QtWidgets.QApplication(sys.argv)
        self.MainWindow = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.MainWindow)
        self.update_widgets()
        self.MainWindow.show()
        self.currentTime = ''
        self.rxMessage = ''

        self.Client_port_GUI = 0                                      # GUI 프로그램의 portNumber -> 컨트롤러와 같다
        self.Client_UDP = tuple()                                     # GUI 프로그램의 IP, portNumber
        self.port_ip=''                                               # 컨트롤러의 IP
        self.portNumber = 0                                           # 컨트롤러의 portNumber
        self.ip_port_Controller = None
        self.ui.pushButton_IP.clicked.connect(self.enter)
        self.receiver = None

        # region button clicked
        self.ui.Socket_Init_button.clicked.connect(self.Socket_Init_btn_clicked)
        self.ui.Vacuum_on_button.clicked.connect(self.Vac_on_btn_clicked)
        self.ui.Vacuum_off_button.clicked.connect(self.Vac_off_btn_clicked)
        self.ui.Clamp_Open_button.clicked.connect(self.Clamp_open_btn_clicked)
        self.ui.Clamp_Close_button.clicked.connect(self.Clamp_close_btn_clicked)
        self.ui.Rotation_0_button.clicked.connect(self.Rotation_0_btn_clicked)
        self.ui.Rotation_90_button.clicked.connect(self.Rotation_90_btn_clicked)
        self.ui.Socket_Open_button.clicked.connect(self.Socket_open_btn_clicked)
        self.ui.Socket_Close_button.clicked.connect(self.Socket_close_btn_clicked)
        # end region

        sys.exit(app.exec_())

    # region IP, portNumber 입력받기
    def enter(self):
        try:
            self.port_ip = str(self.ui.lineEdit_IP.text())
            self.portNumber = int(self.ui.lineEdit_portNumber.text())
            self.ip_port_Controller = (self.port_ip, self.portNumber)
            #GUI_Socket.init(ipAddress=self.port_ip, portNumber=self.portNumber)
            self.Client_port_GUI = self.portNumber
            self.Client_UDP = ('166.79.25.100', self.Client_port_GUI)
            self.ui.textBrowser_tx.append('PC IP: 166.79.25.100'+' PC Port Number:'+self.ui.lineEdit_portNumber.text())
            self.ui.textBrowser_rx.append('Port IP:'+self.ui.lineEdit_IP.text()+' Port Number:'+self.ui.lineEdit_portNumber.text())

            if self.receiver:
                self.receiver.stop()
                self.receiver.wait()

            self.start_receiving()
        except Exception as e:
            self.ui.textBrowser_tx.append(f"Error: {str(e)}")

    def start_receiving(self):
        ip = self.port_ip
        port = self.portNumber
        self.receiver = UDPReceiver(ip, port)
        self.receiver.data_received.connect(self.rxTextBrowser)
        self.receiver.start()

    # end region

    def Socket_Init_btn_clicked(self):
        try :
            self.receiver.senddata(self.ip_port_Controller, 'H2000000')
            self.currentTime=time.ctime()[11:19]
            self.ui.textBrowser_tx.append(self.currentTime+' ==> '+'H2000000')
        except Exception as e:
            self.ui.textBrowser_tx.append(f"Error: {str(e)}")
    def Vac_on_btn_clicked(self):
        try :
            self.receiver.senddata(self.ip_port_Controller, 'H1001000')
            self.currentTime=time.ctime()[11:19]
            self.ui.textBrowser_tx.append(self.currentTime+' ==> '+'H1001000')
        except Exception as e:
            self.ui.textBrowser_tx.append(f"Error: {str(e)}")
    def Vac_off_btn_clicked(self):
        try :
            self.receiver.senddata(self.ip_port_Controller, 'H1000000')
            self.currentTime=time.ctime()[11:19]
            self.ui.textBrowser_tx.append(self.currentTime+' ==> '+'H1000000')
        except Exception as e:
            self.ui.textBrowser_tx.append(f"Error: {str(e)}")
    def Clamp_open_btn_clicked(self):
        try :
            self.receiver.senddata(self.ip_port_Controller, 'H1201000')
            self.currentTime=time.ctime()[11:19]
            self.ui.textBrowser_tx.append(self.currentTime+' ==> '+'H11201000')
        except Exception as e:
            self.ui.textBrowser_tx.append(f"Error: {str(e)}")
    def Clamp_close_btn_clicked(self):
        try :
            self.receiver.senddata(self.ip_port_Controller, 'H1200000')
            self.currentTime=time.ctime()[11:19]
            self.ui.textBrowser_tx.append(self.currentTime+' ==> '+'H1200000')
        except Exception as e:
            self.ui.textBrowser_tx.append(f"Error: {str(e)}")
    def Rotation_0_btn_clicked(self):
        try :
            self.receiver.senddata(self.ip_port_Controller, 'H1300000')
            self.currentTime=time.ctime()[11:19]
            self.ui.textBrowser_tx.append(self.currentTime+' ==> '+'H1300000')
        except Exception as e:
            self.ui.textBrowser_tx.append(f"Error: {str(e)}")
    def Rotation_90_btn_clicked(self):
        try :
            self.receiver.senddata(self.ip_port_Controller, 'H1301000')
            self.currentTime=time.ctime()[11:19]
            self.ui.textBrowser_tx.append(self.currentTime+' ==> '+'H1301000')
        except Exception as e:
            self.ui.textBrowser_tx.append(f"Error: {str(e)}")
    def Socket_open_btn_clicked(self):
        try :
            self.receiver.senddata(self.ip_port_Controller, 'H1101000')
            self.currentTime=time.ctime()[11:19]
            self.ui.textBrowser_tx.append(self.currentTime+' ==> '+'H1101000')
        except Exception as e:
            self.ui.textBrowser_tx.append(f"Error: {str(e)}")
    def Socket_close_btn_clicked(self):
        try :
            self.receiver.senddata(self.ip_port_Controller, 'H1100000')
            self.currentTime=time.ctime()[11:19]
            self.ui.textBrowser_tx.append(self.currentTime+' ==> '+'H1100000')
        except Exception as e:
            self.ui.textBrowser_tx.append(f"Error: {str(e)}")
    def rxTextBrowser(self, rxMessage):
        self.currentTime = time.ctime()[11:19]
        self.ui.textBrowser_rx.append(self.currentTime +' ==> '+ rxMessage)

    def update_widgets(self):
        self.MainWindow.setWindowTitle('PyQt5 GUI')

if __name__ == "__main__":
    main = ControllerGUI()
