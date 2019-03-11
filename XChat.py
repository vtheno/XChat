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
class SearchInputWidget(QtWidgets.QLineEdit):
    def __init__(self, handler, parent=None):
        QtWidgets.QLineEdit.__init__(self, parent)
        self.setStyleSheet("""
        QLineEdit{
            padding-left: 24px; 
            selection-background-color: gray;
        }""")
        self.handler = handler
    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Return:
            text = self.text()
            self.handler(text, ":/img/profile.jpg")
            self.clear()
        QtWidgets.QLineEdit.keyPressEvent(self, e)

class SearchWidget(QtWidgets.QWidget):
    def __init__(self,handler, parent = None):
        QtWidgets.QWidget.__init__(self, parent)
        self.setStyleSheet("""
        margin: 0px;
        border: 0px;
        padding: 0px;
        background-color: #edeae8;
        """)

        self.setMaximumHeight(24)
        self.setMinimumHeight(24)
        self.input = SearchInputWidget(handler, self)
        self.input.setGeometry(0, 0, 215, 24)
        self.input.setContextMenuPolicy(Qt.NoContextMenu)
        
        # qinput.keyPressEvent = keyPressEvent
        icon = QtWidgets.QLabel()
        icon.setGeometry(QtCore.QRect(0, 0, 24, 24))
        icon.setStyleSheet("""
        QLabel{
            background-image: url(:/img/search.png);
            background-repeat: no-repeat;
            background-position: center;
        }
        """)
        icon.setParent(self.input)

class UserItemWidget(QtWidgets.QWidget):
    def __init__(self,parent = None, username="vtheno", profile=":/img/profile.jpg"):
        QtWidgets.QWidget.__init__(self, parent)
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

class MessageInputWidget(QtWidgets.QTextEdit):#.QTextEdit):
    def __init__(self, handler_message, parent=None):
        QtWidgets.QTextEdit.__init__(self, parent)
        self.handler_message = handler_message
        self.setMaximumHeight(200)
        self.setMinimumHeight(200)
        self.setStyleSheet("""
        QTextEdit {
            border: none;
            border-radius: 5px;
            background-color: #F5F5F5;
            selection-background-color: gray;
            padding-top: 32px;
        }
        """)
        self.verticalScrollBar().setStyleSheet(style)
        self.setAcceptRichText(False)
        
    def keyPressEvent(self, e):
        if (e.key() == Qt.Key_Return) and (e.modifiers() == Qt.ControlModifier):
            msg = self.toPlainText()
            if self.handler_message(msg):
                self.clear()
        QtWidgets.QTextEdit.keyPressEvent(self, e)

    def focusInEvent(self, e):
        self.setStyleSheet("""
        QTextEdit {
            border: none;
            border-radius: 5px;
            background-color: #FFFFFF;
            selection-background-color: gray;
            selection-color: #F0F0F0;
            padding-top: 32px;
        }
        """)
        QtWidgets.QTextEdit.focusInEvent(self, e)
        effect = QtWidgets.QGraphicsDropShadowEffect()
        effect.setBlurRadius(8)
        effect.setColor(QtGui.QColor("lightgray"))
        effect.setOffset(5, 5)
        self.parent().setGraphicsEffect(effect)

    def focusOutEvent(self, e):
        self.setStyleSheet("""
        QTextEdit {
            border: none;
            border-radius: 5px;
            background-color: #F5F5F5;
            selection-background-color: gray;
            selection-color: #F0F0F0;
            padding-top: 32px;
        }
        """)
        QtWidgets.QTextEdit.focusOutEvent(self, e)
        self.parent().setGraphicsEffect(None)

class MessagePanelWidget(QtWidgets.QWidget):
    def __init__(self, handler_message):
        QtWidgets.QWidget.__init__(self)
        self.max_len = 1500
        self.current_len = 0
        self.init(handler_message)
    def textChanged(self):
        # print("changed")
        temp = self.message_input.toPlainText()
        self.current_len = len(temp)
        if self.current_len > self.max_len:
            self.message_input.setPlainText(temp[0:self.max_len])
            self.message_input.moveCursor(QtGui.QTextCursor.End, QtGui.QTextCursor.MoveAnchor)
        else:
            text = f"{self.current_len}/{self.max_len}"
            self.size_label.setText(text)

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
        self.size_label = QtWidgets.QLabel()
        self.size_label.setText(f"{self.current_len}/{self.max_len}")
        self.size_label.setGeometry(670, 0, 70, 32)
        self.size_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.message_input = MessageInputWidget(handler_message, self)
        self.message_input.setGeometry(0, 0, 750, 200)
        # message_input.setFocusPolicy(Qt.NoFocus)
        self.message_input.setContextMenuPolicy(Qt.NoContextMenu)
        self.message_input.textChanged.connect(self.textChanged)
        qbtn_image.setParent(self.message_input)
        self.size_label.setParent(self.message_input)

class MFrame(QtWidgets.QWidget):
    def __init__(self, window: QtWidgets.QWidget):
        QtWidgets.QWidget.__init__(self)
        self.window = window
        self.resize(1060, 820)
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
        QtWidgets.QWidget.paintEvent(self, e)
        # if parent windows WA_TranslucentBackground
        # then repaint frame with style
        opt = QtWidgets.QStyleOption()
        opt.initFrom(self)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        self.style().drawPrimitive(QtWidgets.QStyle.PE_Widget, opt, painter, self)

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
        listWidget.setGeometry(32, 60, 215, 700)
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

        #listWidget.itemClicked.connect(self.listItemAction)
        listWidget.currentItemChanged.connect(self.listItemCurrentChanged)
        listWidget.setFocusPolicy(Qt.NoFocus) # hidden select border

        def appendUserItem(username, profile):
            item = QtWidgets.QListWidgetItem()
            item.setSizeHint(QtCore.QSize(200, 50))
            user = UserItemWidget(listWidget, username, profile)
            # print( dir(item) )
            # print( dir(user) )
            def remove():
                print('remove')
                # item.setFlags(item.flags() & ~Qt.ItemIsSelectable)
                item.setSelected(False)
                listWidget.takeItem(listWidget.row(item))
                self.message_view.msg_clear()

            def rightMenuShow(_point):
                menu = QtWidgets.QMenu(user)
                # showAction = QtWidgets.QAction('&Show', menu, triggered=lambda :print('s'))
                # hideAction = QtWidgets.QAction('&Hide', menu, triggered=lambda :print('h'))
                quitAction = QtWidgets.QAction('&Remove', menu, triggered=remove)
                # menu.addAction(showAction)
                # menu.addAction(hideAction)
                menu.addSeparator()
                menu.addAction(quitAction)
                point = QtGui.QCursor.pos()
                # print( point )
                menu.exec_(point)
            
            user.setContextMenuPolicy(Qt.CustomContextMenu)
            user.customContextMenuRequested[QtCore.QPoint].connect(rightMenuShow)
            item.setData(0, user)
            listWidget.addItem(item)
            listWidget.setItemWidget(item, user)

        search_bar = SearchWidget(appendUserItem, self)
        search_bar.setGeometry(32, 32, 215, 20)

        self.message_view = MessageViewWidget(self)
        self.message_view.setGeometry(255, 35, 750, 520)

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
                        channel = MessageItem(img_path, True, False)
                        self.message_view.msgStack.appendChannel(channel)
                    elif typ == 'txt':
                        msg = pkg.autoWrap(msg)
                        print( repr(msg) )
                        channel = MessageItem(msg, True, True)
                        self.message_view.msgStack.appendChannel(channel)
        """
        def handler_message( data: str ):
            
            if self.message_view.cfg.title:
                temp = data.strip("\n")
                if temp:
                    msg = pkg.autoWrap(data)
                    # print( msg.split("\n") )
                    channel = MessageItem(msg, True, True)
                    self.message_view.msgStack.appendChannel(channel)
                return True
            return False

        message_panel = MessagePanelWidget(handler_message)
        message_panel.setParent(self)
        message_panel.setGeometry(255, 560, 750, 200)
        
    def listItemCurrentChanged(self, currentItem, previousItem):
        self.message_view.msgStack.clear()
        # print( 'changed' )
        if currentItem:
            # print( currentItem, previousItem )
            currentItem.setSelected(True)
            username = currentItem.data(0).user_config["username"]
            print( 'connect to ', username)
            self.message_view.cfg.changeTitle(f"{username}")

class MWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.resize(1060, 820)
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
    titleChange = QtCore.pyqtSignal(str)
    def __init__(self, parent, title=''):
        QtCore.QObject.__init__(self)
        # self.parent = parent
        # self.modifyTitle.connect(self.changeTitle)
        self._title = title
    @QtCore.pyqtProperty(str, notify=titleChange)
    def title(self):
        return self._title

    @title.setter
    def title(self, title):
        if title != self._title:
            self._title = title
            self.modifyTitle.emit(title)
    
    @QtCore.pyqtSlot(str)
    def changeTitle(self, title: str):
        if title != self._title:
            self._title = title
            self.modifyTitle.emit(title)
    
class MessageItem(QtCore.QObject):
    msgChanged = QtCore.pyqtSignal()
    flagChanged = QtCore.pyqtSignal()
    typeChanged = QtCore.pyqtSignal()

    def __init__(self, msg='', selfSend=False, textType=True, *args, **kwargs):
        QtCore.QObject.__init__(self, *args, **kwargs)
        self._msg = msg
        self._selfSend = selfSend
        self._textType = textType
    @QtCore.pyqtProperty('QString', notify=msgChanged)
    def msg(self):
        return self._msg
    @msg.setter
    def msg(self, msg):
        if msg != self._msg:
            self._msg = msg
            self.msgChanged.emit()
    @QtCore.pyqtProperty(bool, notify=typeChanged)
    def textType(self):
        return self._textType
    @textType.setter
    def textType(self, textType: bool):
        if textType != self._textType:
            self._textType = textType
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
        self._items = []
        # MessageItem('hello', False, False),
        # MessageItem('hi', False, False)

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
    def clear(self):
        self._items = []
        self.itemsChanged.emit()
    def load_with_list(self, maps: [dict]):
        # {}
        for item in maps:
            msg = item["msg"]
            selfSend = item["self"]
            textType = item["textType"]
            
            MessageItem(msg, selfSend, textType)

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
    def msg_clear(self):
        self.cfg.changeTitle('')
        self.msgStack.clear()
    
if __name__=="__main__":
 
    mapp= QtWidgets.QApplication(sys.argv)
    # QtCore.QCoreApplication.setAttribute(Qt.AA_UseSoftwareOpenGL)
    window = MWindow()
    window.show()
    
    sys.exit(mapp.exec_())
