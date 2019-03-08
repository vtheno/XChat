import sys
 
from PyQt5 import QtCore,QtGui,QtWidgets, QtQml, QtQuickWidgets, QtQuick
# QtWebEngineWidgets, QtWebChannel
from PyQt5.QtCore import Qt

import pkg
import res

style = """
QScrollBar:vertical
{
    width:8px;
    background:rgba(0,0,0,0%);
    margin:0px,0px,0px,0px;
    padding-top:9px;
    padding-bottom:9px;
}
QScrollBar::handle:vertical
{
    width:8px;
    background:rgba(0,0,0,25%);
    border-radius:4px;
    min-height:20;
}
QScrollBar::handle:vertical:hover
{
    width:8px;
    background:rgba(0,0,0,50%);
    border-radius:4px;
    min-height:20;
}
QScrollBar::add-line:vertical
{
    height:9px;width:8px;
    border-image:url(:/images/a/3.png);
    subcontrol-position:bottom;
}
QScrollBar::sub-line:vertical
{
    height:9px;width:8px;
    border-image:url(:/images/a/1.png);
    subcontrol-position:top;
}
QScrollBar::add-line:vertical:hover
{
    height:9px;width:8px;
    border-image:url(:/images/a/4.png);
    subcontrol-position:bottom;
}
QScrollBar::sub-line:vertical:hover
{
    height:9px;width:8px;
    border-image:url(:/images/a/2.png);
    subcontrol-position:top;
}
QScrollBar::add-page:vertical,QScrollBar::sub-page:vertical
{
    background:rgba(0,0,0,10%);
    border-radius:4px;
}
"""
class SearchWidget(QtWidgets.QWidget):
    def __init__(self,parent = None):
        super(SearchWidget, self).__init__(parent)
        self.setStyleSheet("""
        margin: 0px;
        border: 0px;
        padding: 0px;
        background-color: #edeae8;
        """)

        self.setMaximumHeight(24)
        self.setMinimumHeight(24)
        qinput = QtWidgets.QLineEdit()
        qinput.setGeometry(0, 0, 215, 24)
        qinput.setStyleSheet("""
        QLineEdit{
            padding-left: 24px; 
            selection-background-color: gray;
        }""")
        qinput.setParent(self)
        qinput.setContextMenuPolicy(Qt.NoContextMenu)

        profile = QtWidgets.QLabel()
        profile.setGeometry(QtCore.QRect(0, 0, 24, 24))
        profile.setStyleSheet("""
        QLabel{
            background-image: url(:/img/search.png);
            background-repeat: no-repeat;
            background-position: center;
        }
        """)
        profile.setParent(qinput)

class UserItemWidget(QtWidgets.QWidget):
    def __init__(self,parent = None, username="vtheno", profile=":/img/profile.jpg"):
        super(UserItemWidget, self).__init__(parent)
        self.setStyleSheet("""
        background-color: transparent;
        """)
        self.setMaximumHeight(50)
        self.setMinimumHeight(50)
        
        self.profile_label = QtWidgets.QLabel()
        self.profile_label.setGeometry(0, 0, 50, 50)
        self.profile_label.setStyleSheet(f"""
        QLabel{{
            border-image: url({profile});
            background-repeat: no-repeat;
            background-position: center;
        }}
        """)
        self.profile_label.setParent(self)

        self.username_label = QtWidgets.QLabel(username)
        self.username_label.setGeometry(60, 5, 150, 20)
        self.username_label.setStyleSheet("""
        QLabel{
            color: #000000;
            font-size: 15px;
        }
        """)
        self.username_label.setParent(self)

        self.msg_label = QtWidgets.QLabel(username)
        self.msg_label.setGeometry(60, 25, 150, 20)
        self.msg_label.setStyleSheet("""
        QLabel{
            color: gray;
            font-size: 15px;
        }
        """)
        self.msg_label.setParent(self)

        self.user_config = {"username": username, "profile": profile}
    def update_config(self,  username: str, profile: str):
        self.username_label.setText(username)
        self.profile_label.setStyleSheet(f"""
        QLabel{{
            border-image: url({profile});
            background-repeat: no-repeat;
            background-position: center;
        }}
        """)

class MessageInputWidget(QtWidgets.QPlainTextEdit):#.QTextEdit):
    def __init__(self, handler_message, parent=None):
        super(QtWidgets.QPlainTextEdit, self).__init__(parent)
        self.handler_message = handler_message
        self.setMaximumHeight(200)
        self.setMinimumHeight(200)
        self.setStyleSheet("""
        QPlainTextEdit {
            border: none;
            border-radius: 5px;
            background-color: #F5F5F5;
            selection-background-color: gray;
            padding-top: 32px;
        }
        """)
    def keyPressEvent(self, e):
        if (e.key() == Qt.Key_Return) and (e.modifiers() == Qt.ControlModifier):
            # print(dir(self))
            # html = self.toHtml()
            # msg = pkg.getAllTypeMsg(html)
            # print( msg )
            msg = self.toPlainText()
            self.handler_message(msg)
            self.clear()
        super(MessageInputWidget, self).keyPressEvent(e)

    def focusInEvent(self, e):
        self.setStyleSheet("""
        QPlainTextEdit {
            border: none;
            border-radius: 5px;
            background-color: #FFFFFF;
            selection-background-color: gray;
            selection-color: #F0F0F0;
            padding-top: 32px;
        }
        """)
        super(MessageInputWidget, self).focusInEvent(e)
        effect = QtWidgets.QGraphicsDropShadowEffect()
        effect.setBlurRadius(8)
        effect.setColor(QtGui.QColor("lightgray"))
        effect.setOffset(5, 5)
        self.parent().setGraphicsEffect(effect)

    def focusOutEvent(self, e):
        self.setStyleSheet("""
        QPlainTextEdit {
            border: none;
            border-radius: 5px;
            background-color: #F5F5F5;
            selection-background-color: gray;
            selection-color: #F0F0F0;
            padding-top: 32px;
        }
        """)
        super(MessageInputWidget, self).focusOutEvent(e)
        self.parent().setGraphicsEffect(None)

class MessagePanelWidget(QtWidgets.QWidget):
    def __init__(self, handler_message):
        QtWidgets.QWidget.__init__(self)
        self.init(handler_message)

    def init(self, handler_message):
        qbtn_image = QtWidgets.QPushButton()
        qbtn_image.setIcon(QtGui.QIcon(":/img/image.png"))
        qbtn_image.setStyleSheet("""
        QPushButton {
            background-color: transparent;
            border: none;
        }
        QPushButton:hover {
            background-color: lightgreen;
        }
        """)
        qbtn_image.setGeometry(0, 0, 32, 32)
        qbtn_image.setFocusPolicy(Qt.NoFocus)
        message_input = MessageInputWidget(handler_message, self)
        message_input.setGeometry(0, 0, 750, 200)
        # message_input.setFocusPolicy(Qt.NoFocus)
        message_input.setContextMenuPolicy(Qt.NoContextMenu)
        qbtn_image.setParent(message_input)

class MFrame(QtWidgets.QWidget):
    def __init__(self, window: QtWidgets.QWidget):
        QtWidgets.QWidget.__init__(self)
        self.window = window
        self.resize(1060,720)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.setObjectName("MFrame")
        self.setMouseTracking(True)
        self.setStyleSheet("""
        #MFrame {
            background:rgba(245,245,245,0.9); 
            border-radius:15px;
        }
        """)
        self.setAttribute(Qt.WA_TranslucentBackground, False) # tranlate alpha to 0
        self.init()

    def paintEvent(self, e):
        super(MFrame, self).paintEvent(e)
        # if parent windows WA_TranslucentBackground
        # then repaint frame with style
        opt = QtWidgets.QStyleOption()
        opt.initFrom(self)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        self.style().drawPrimitive(QtWidgets.QStyle.PE_Widget, opt, painter, self)
        # very important
        # print( dir(evt) )
        # self.message_view.update()
        # self.update()

    def init(self):
        qbtn_close = QtWidgets.QPushButton(self)
        qbtn_close.setIcon(QtGui.QIcon(":/img/close.png"))
        qbtn_close.setGeometry(1006,0,32,32)
        close_style = """
        QPushButton {
            border: none;
            background-color: #F5F5F5;
            border-top-right-radius: 15px;
        }
        QPushButton:hover {
            background-color: #FDA085;
        }
        """ 
        qbtn_close.setStyleSheet(close_style)
        qbtn_close.setFocusPolicy(Qt.NoFocus)
        qbtn_close.clicked.connect(self.window.close)

        qbtn_hide = QtWidgets.QPushButton(self)
        qbtn_hide.setIcon(QtGui.QIcon(":/img/hide.png"))
        qbtn_hide.setGeometry(974,0,32,32)
        hide_style = """
        QPushButton {
            border: none;
            background-color: #F5F5F5;
        }
        QPushButton:hover {
            background-color: lightgreen;
        }
        """ 
        qbtn_hide.setStyleSheet(hide_style)
        qbtn_hide.setFocusPolicy(Qt.NoFocus)
        qbtn_hide.clicked.connect(self.window.hide)
        # user list
        listWidget = QtWidgets.QListWidget(self)
        listWidget.setGeometry(32, 60, 215, 600)
        listWidget.setStyleSheet("""
        QListWidget::item:selected:!active {
            border: 0px;
            background-color: lightgreen;
        }
        QListWidget::item:selected {
            border: 0px;
            background-color: lightgray;
        }
        QListWidget::item:hover {
            background: skyblue;
        }
        QListWidget {
            border: none;
            background-color: #edeae8;
        }
        """)
        # listWidget.setIconSize(QtCore.QSize(50, 200))
        listWidget.verticalScrollBar().setStyleSheet(style)
        # listWidget.itemClicked.connect(lambda item: print(item.type()))
        listWidget.itemPressed.connect(self.listItemAction)
        listWidget.setFocusPolicy(Qt.NoFocus) # hidden select border
        for i in range(20):
            item = QtWidgets.QListWidgetItem()
            # item.setIcon(QtGui.QIcon("img/profile.jpg"))
            item.setSizeHint(QtCore.QSize(200, 50))
            user = UserItemWidget(listWidget)
            item.setData(0, user)
            listWidget.addItem(item)
            listWidget.setItemWidget(item, user)

        search_bar = SearchWidget(self)
        search_bar.setGeometry(32, 32, 215, 20)



        self.message_view = MessageViewWidget(self)
        self.message_view.setGeometry(255, 35, 750, 420)

        """
        # old version
        def handler_message( data: [(str, str)] ):
            # msgType = 'txt' | 'img'
            # data: (msgType * string) list
            if data:
                #self.message_view.cfg.changeTitle(data)
                for typ, msg in msg_list:
                    if typ == 'img':
                        img_path = msg #.replace('file:///', '')
                        print( img_path )
                        channel = MessageItem(img_path, True, True)
                        self.message_view.msgStack.appendChannel(channel)
                    elif typ == 'txt':
                        msg = pkg.autoWrap(msg)
                        print( repr(msg) )
                        channel = MessageItem(msg, True, False)
                        self.message_view.msgStack.appendChannel(channel)
        """
        def handler_message( data: str ):
            msg = pkg.autoWrap(data)
            print( msg.split("\n") )
            channel = MessageItem(msg, True, False)
            self.message_view.msgStack.appendChannel(channel)

        message_panel = MessagePanelWidget(handler_message)
        message_panel.setParent(self)
        message_panel.setGeometry(255, 460, 750, 200)
        
    def listItemAction(self, item: QtWidgets.QListWidgetItem):
        # print( item )
        username = item.data(0).user_config["username"]
        self.message_view.cfg.changeTitle(f"chat with: {username}")
        # self.message_view.update()
        # item.data(0).update_config(
        #     username="new user",
        #     profile="img/profile-1.jpg"
        # )

class MWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(MWindow,self).__init__(parent)
        self.resize(1060, 720)
        layout = QtWidgets.QHBoxLayout()
        self.setObjectName('MWindow')
        
        self.setWindowTitle("chat")

        self.widget = MFrame(window=self)
        layout.addWidget(self.widget)
        self.setLayout(layout)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)  # no title bar
        self.setAttribute(Qt.WA_TranslucentBackground) # tranlate alpha to 0
        # drag init
        self.press_flag = False
        # shadow effect
        effect = QtWidgets.QGraphicsDropShadowEffect()
        effect.setBlurRadius(8)
        effect.setColor(QtGui.QColor("lightgray"))
        effect.setOffset(3, 3)
        self.widget.setGraphicsEffect(effect)
        # set frame shadow effect

        self.tray = QtWidgets.QSystemTrayIcon()
        self.tray.setParent(self)
        icon = QtGui.QIcon(':/img/icon.png')
        self.setWindowIcon(icon)
        self.tray.setIcon(icon)
        tray_menu = QtWidgets.QMenu(self)#QtWidgets.QApplication.desktop())
        showAction = QtWidgets.QAction('&Show', self, triggered=self.show)
        hideAction = QtWidgets.QAction('&Hide', self, triggered=self.hide)
        quitAction = QtWidgets.QAction('&Quit', self, triggered=self.close)
        tray_menu.setStyleSheet("""
        QMenu{
            border: none;
            background-color: #FFFFFF;
            color: #000000;
        }
        QMenu::item {
            background-color: transparent;
        }
        QMenu::item:selected {
            background-color: lightgray;
        }
        """)
        tray_menu.addAction(showAction)
        tray_menu.addAction(hideAction)
        tray_menu.addSeparator()
        tray_menu.addAction(quitAction)
        self.tray.setContextMenu(tray_menu)
        self.tray.show() # auto show tray, if no show, when window close it will stay
        
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.press_flag = True
            self.m_Position = event.globalPos() - self.pos()
            event.accept()
            self.setCursor(QtGui.QCursor(Qt.OpenHandCursor))

    def mouseMoveEvent(self, QMouseEvent):
        if Qt.LeftButton and self.press_flag:
            self.move(QMouseEvent.globalPos() - self.m_Position)
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        self.press_flag = False
        self.setCursor(QtGui.QCursor(Qt.ArrowCursor))

    def closeEvent(self, event):
        # auto hide tray on window close
        if self.tray.isVisible():
            self.tray.hide()

class ViewConfig(QtCore.QObject):
    #textChanged = QtCore.pyqtSignal(str)
    modifyTitle = QtCore.pyqtSignal(str, arguments=["title"])
    def __init__(self, parent):
        QtCore.QObject.__init__(self)
        # self.parent = parent
        # self.modifyTitle.connect(self.changeTitle)
    @QtCore.pyqtSlot(str)
    def changeTitle(self, title: str):
        self.modifyTitle.emit(title)
        # self.parent.update()

class MessageItem(QtCore.QObject):
    msgChanged = QtCore.pyqtSignal()
    flagChanged = QtCore.pyqtSignal()
    typeChanged = QtCore.pyqtSignal()

    def __init__(self, msg='', selfSend=False, msgType=False, *args, **kwargs):
        QtCore.QObject.__init__(self, *args, **kwargs)
        self._msg = msg
        self._selfSend = selfSend
        self._msgType = msgType
    @QtCore.pyqtProperty('QString', notify=msgChanged)
    def msg(self):
        return self._msg
    @msg.setter
    def msg(self, msg):
        if msg != self._msg:
            self._msg = msg
            self.msgChanged.emit()
    @QtCore.pyqtProperty(bool, notify=typeChanged)
    def msgType(self):
        return self._msgType
    @msgType.setter
    def msgType(self, msgType):
        if msgType != self._msgType:
            self._msgType = msgType
            self.typeChanged.emit()

    @QtCore.pyqtProperty(bool, notify=flagChanged)
    def selfSend(self):
        return self._selfSend

    @selfSend.setter
    def selfSend(self, flag):
        if flag != self._selfSend:
            self._selfSend = flag
            self.flagChanged.emit()

class MessageStack(QtCore.QObject):
    itemsChanged = QtCore.pyqtSignal()
    def __init__(self, parent, *args, **kwargs):
        QtCore.QObject.__init__(self, *args, **kwargs)
        # self.parent = parent
        self._items = [
            MessageItem('hello'),
            MessageItem('hi')
        ]

    @QtCore.pyqtProperty(QtQml.QQmlListProperty, notify=itemsChanged)
    def items(self):
        return QtQml.QQmlListProperty(MessageItem, self, self._items)

    @items.setter
    def items(self, items):
        if items != self._items:
            self._items = items
            self.itemsChanged.emit()
            # self.parent.update()

    def appendChannel(self, channel):
        self._items.append(channel)
        self.itemsChanged.emit()
        # self.parent.update()

class MessageViewWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        # QtQml.qmlRegisterType(ViewConfig, 'ViewConfig', 1, 0, 'ViewConfig')
        self.view = QtQuickWidgets.QQuickWidget(self)
        rootCtx = self.view.rootContext()
        self.cfg = ViewConfig(self)
        self.msgStack = MessageStack(self)
        rootCtx.setContextProperty('viewConfig', self.cfg)
        QtQml.qmlRegisterType(MessageItem, 'Message', 1, 0, 'Message')
        QtQml.qmlRegisterType(MessageStack, 'Message', 1, 0, 'Store')
        rootCtx.setContextProperty('msgStack', self.msgStack)
        self.view.setSource(QtCore.QUrl("qrc:///qml/message-view.qml"))
        # self.view.show()

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.repaint)
        self.timer.start(50)

        # rootItem = view.rootObject()
        # rootItem : QtQuickWidgets.QQuickItem
        # print(rootItem.property("cfg") )
        # print( rootItem.objectName() )
        # print( help(rootItem.findChild) )
        # for item in rootItem.childItems():
        
    
if __name__=="__main__":
 
    mapp= QtWidgets.QApplication(sys.argv)
    # QtCore.QCoreApplication.setAttribute(Qt.AA_UseSoftwareOpenGL)
    window = MWindow()
    window.show()
    
    sys.exit(mapp.exec_())
