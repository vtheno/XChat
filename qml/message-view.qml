import QtQuick 2.12
import QtQuick.Controls 2.12
import QtQuick.Controls.Styles 1.4
import QtQuick.Layouts 1.12

import Message 1.0
// import ViewConfig 1.0
Item {
    id: root
    width: 750
    height: 620
    visible: true
    // property string cfg
    // cfg: qsTr(obj.title)
    Page {
	id: page
        anchors.fill: parent
        header: ToolBar {
            Label {
		id: page_title
		font.pixelSize: 20
		// anchors.centerIn: parent
		anchors.left: parent.left
		anchors.margins: 10
		anchors.verticalCenter: parent.verticalCenter
            }
	    /*
              ToolButton {
	      text: qsTr("close")
	      anchors.left: parent.left
	      anchors.leftMargin: 5
	      anchors.verticalCenter: parent.verticalCenter
	      onClicked: {
	      viewConfig.changeTitle("")
	      }
              }
	    */
	}
	ColumnLayout {
            anchors.fill: parent

            ListView {
		id: listView
		Layout.fillWidth: true
		Layout.fillHeight: true
		Layout.margins: 5
		displayMarginBeginning: 40
		displayMarginEnd: 40
		verticalLayoutDirection: ListView.TopToBottom
		spacing: 12
		model: msgStack.items
		delegate:
		Row {
		    id: messageRow
		    anchors.right: selfSend ? parent.right : undefined
		    spacing: 6

		    Image {
                        id: avatar
                        source: !selfSend ? "qrc:///img/profile.jpg" : ""
                    }
		    Rectangle {
			width: !textType ? image_msg.width : Math.min(messageText.implicitWidth + 24,
								    listView.width - 
								    (!selfSend ? avatar.width + messageRow.spacing : 0))
                        height: !textType ? image_msg.height : messageText.implicitHeight + 24
			color: !textType?"white":(selfSend ? "lightgrey" : "steelblue")
			Image {
                            id: image_msg
			    anchors.centerIn: parent
			    anchors.margins: 12
                            source: !textType ? msg : ""
			}
			TextEdit {
			    id: messageText
			    anchors.centerIn: parent
			    anchors.margins: 12
			    wrapMode: TextEdit.Wrap
			    text: textType ? msg : ""
			    color: selfSend ? "black" : "white"
			    readOnly: true
			    // selectByMouse: true
			    // selectable: true
			}
		    }
		    Image {
                        id: self_avatar
                        source: selfSend ? "qrc:///img/profile.jpg" : ""
                    }
		}
		ScrollBar.vertical: ScrollBar {}
		onCountChanged: {
                    var newIndex = count - 1 // last index
                    positionViewAtEnd()
                    currentIndex = newIndex
		}
            }
            
	}


    }
    Connections {
	target: viewConfig
	onModifyTitle: {
	    page_title.text = title
	}
    }
}
