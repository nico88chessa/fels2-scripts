import QtQuick 2.12
import QtQuick.Window 2.12
import QtQuick.Controls 2.12
import QtQuick.Layouts 1.11
import QtQuick.Dialogs 1.3

import com.dv.CoreController 1.0
import com.dv.CoreBean 1.0

Window {

    CoreController {
        id: coreController
    }

    CoreBean {
        id: coreBean
    }

    Component.onCompleted: {
        coreController.pBean = coreBean
    }

    id: windowApp
    visible: true
    width: 1024
    height: 768
    minimumHeight: 768
    minimumWidth: 1024
    onClosing: {
        coreController.stopProcess()
    }

    GridLayout {
        id: gridLayout
        anchors.margins: 5
        anchors.fill: parent

        ListView {
            id: menuList
            width: 200
            spacing: 2
            interactive: false
            boundsBehavior: Flickable.StopAtBounds
            Layout.fillHeight: true
            highlight: highlightBar
            highlightFollowsCurrentItem: false

            MouseArea {
                anchors.fill: parent
                propagateComposedEvents: true
            }

            model: ListModel {

                ListElement {
                    name: "REGISTERS"
                }

                ListElement {
                    name: "CONTROL"
                }

                ListElement {
                    name: "OUTPUT"
                }

                ListElement {
                    name: "STATUS"
                }

                ListElement {
                    name: "DATA TRANSFER"
                }

                ListElement {
                    name: "UTILS"
                }
            }

            Component {
                id: highlightBar

                Rectangle {
                    z: 2
                    width: 200
                    height: 40
                    color: "#803e59db"
                    y: menuList.currentItem.y
                }
            }

            delegate: Rectangle {
                id: rectTest
                height: 40
                width: parent.width
                clip: true
                Layout.fillWidth: true
                color: "lightblue"
                border.width: 1
                border.color: "#003300"

                MouseArea {
                    id: delMouseArea
                    hoverEnabled: true
                    anchors.fill: parent
                    onClicked: menuList.currentIndex = index
                    onEntered: rectTest.color = "#cc3e59db"
                    onExited: parent.color = "lightblue"
                }

                Text {
                    x: 10
                    height: parent.height
                    text: name
                    verticalAlignment: Text.AlignVCenter
                    font.bold: rectTest.ListView.isCurrentItem ? true : false;
                    color: "#001122"
                }
            }
        }

        StackLayout {
            id: stackLayout
            currentIndex: menuList.currentIndex
            Layout.fillHeight: true
            Layout.fillWidth: true

            Item {
                id: itemRegisters

                GridLayout {
                    id: glRegisters
                    anchors.fill: parent
                    visible: true
                    rows: 3
                    columns: 2

                    Item {
                        id: itemRegistersWriteRequest
                        Layout.minimumHeight: 600
                        Layout.fillWidth: true

                        TextArea {
                            id: taRegistersWriteRequest
                            font.pointSize: 10
                            font.family: "Ubuntu Mono"
                            selectionColor: "#0B6FAD"
                            selectedTextColor: "#FFFFFF"
                            selectByMouse: true
                            anchors.fill: parent
                            color: "#FFFFFF"
                            background: Rectangle {
                                color: "#000000"
                            }

                            onEditingFinished: coreBean.pRegistersWriteRequest = text
                            Component.onCompleted: text = coreBean.pRegistersWriteRequest
                        }
                    }

                    Item {
                        id: itemRegistersReadResponse
                        Layout.rowSpan: 2
                        Layout.fillHeight: true
                        Layout.fillWidth: true

                        TextArea {
                            id: taRegistersReadResponse
                            readOnly: true
                            font.pointSize: 10
                            font.family: "Ubuntu Mono"
                            selectionColor: "#0B6FAD"
                            selectedTextColor: "#FFFFFF"
                            selectByMouse: true
                            anchors.fill: parent
                            color: "#FFFFFF"
                            background: Rectangle {
                                color: "#000000"
                            }
                        }

                        Connections {
                            target: coreBean
                            function onRegistersReadResponseChanged() {
                                taRegistersReadResponse.text = coreBean.pRegistersReadResponse
                            }
                        }
                    }

                    Item {
                        id: itemRegistersWriteResponse
                        Layout.fillHeight: true
                        Layout.fillWidth: true

                        TextArea {
                            id: taRegistersWriteResponse
                            readOnly: true
                            font.pointSize: 10
                            font.family: "Ubuntu Mono"
                            anchors.fill: parent
                            color: "#FFFFFF"
                            background: Rectangle {
                                color: "#000000"
                            }
                        }

                        Connections {
                            target: coreBean
                            function onRegistersWriteResponseChanged() {
                                taRegistersWriteResponse.text = coreBean.pRegistersWriteResponse
                            }
                        }
                    }

                    Item {
                        id: itemRegistersButtonArea
                        height: bSendRegistersWrite.height + 4
                        Layout.fillWidth: true

                        Button {
                            id: bSendRegistersWrite
                            height: 40
                            anchors.right: itemRegistersButtonArea.right
                            text: qsTr("Send registers")
                            anchors.verticalCenter: parent.verticalCenter
                            onClicked: coreController.writeRegisters()
                        }

                        Rectangle {
                            color: "#00450010"
                            anchors.fill: parent

                        }
                    }
                }
            }

            Item {
                id: itemControl

                GridLayout {
                    id: glControl
                    anchors.fill: parent
                    visible: true
                    rows: 2
                    columns: 2

                    Item {
                        id: itemControlWriteRequest
                        Layout.minimumHeight: 600
                        Layout.fillWidth: true

                        TextArea {
                            id: taControlWriteRequest
                            font.pointSize: 10
                            font.family: "Ubuntu Mono"
                            selectionColor: "#0B6FAD"
                            selectedTextColor: "#FFFFFF"
                            selectByMouse: true
                            anchors.fill: parent
                            color: "#FFFFFF"
                            background: Rectangle {
                                color: "#000000"
                            }
                            onEditingFinished: coreBean.pControlWriteRequest = text
                            Component.onCompleted: text = coreBean.pControlWriteRequest
                        }
                    }

                    Item {
                        id: itemControlReadResponse
                        Layout.rowSpan: 2
                        Layout.fillHeight: true
                        Layout.fillWidth: true

                        TextArea {
                            id: taControlReadResponse
                            readOnly: true
                            font.pointSize: 10
                            font.family: "Ubuntu Mono"
                            selectionColor: "#0B6FAD"
                            selectedTextColor: "#FFFFFF"
                            selectByMouse: true
                            anchors.fill: parent
                            color: "#FFFFFF"
                            background: Rectangle {
                                color: "#000000"
                            }
                        }

                        Connections {
                            target: coreBean
                            function onControlReadResponseChanged() {
                                taControlReadResponse.text = coreBean.pControlReadResponse
                            }
                        }
                    }

                    Item {
                        id: itemControlWriteResponse
                        Layout.fillHeight: true
                        Layout.fillWidth: true

                        TextArea {
                            id: taControlWriteResponse
                            readOnly: true
                            font.pointSize: 10
                            font.family: "Ubuntu Mono"
                            anchors.fill: parent
                            color: "#FFFFFF"
                            background: Rectangle {
                                color: "#000000"
                            }
                        }

                        Connections {
                            target: coreBean
                            function onControlWriteResponseChanged() {
                                taControlWriteResponse.text = coreBean.pControlWriteResponse
                            }
                        }
                    }

                    Item {
                        id: itemControlButtonArea
                        height: bSendControlWrite.height + 4
                        Layout.fillWidth: true

                        Button {
                            id: bSendControlWrite
                            height: 40
                            anchors.right: itemControlButtonArea.right
                            text: qsTr("Send control")
                            anchors.verticalCenter: parent.verticalCenter
                            onClicked: coreController.writeControl()
                        }

                        Rectangle {
                            color: "#00450010"
                            anchors.fill: parent
                        }
                    }
                }
            }

            Item {
                id: itemOutput

                GridLayout {
                    id: glOutput
                    anchors.fill: parent
                    visible: true
                    rows: 3
                    columns: 2

                    Item {
                        id: itemOutputWriteRequest
                        Layout.minimumHeight: 600
                        Layout.fillWidth: true

                        TextArea {
                            id: taOutputWriteRequest
                            font.pointSize: 10
                            font.family: "Ubuntu Mono"
                            selectionColor: "#0B6FAD"
                            selectedTextColor: "#FFFFFF"
                            selectByMouse: true
                            anchors.fill: parent
                            color: "#FFFFFF"
                            background: Rectangle {
                                color: "#000000"
                            }

                            onEditingFinished: coreBean.pOutputWriteRequest = text
                            Component.onCompleted: text = coreBean.pOutputWriteRequest
                        }
                    }

                    Item {
                        id: itemOutputReadResponse
                        Layout.rowSpan: 2
                        Layout.fillHeight: true
                        Layout.fillWidth: true

                        TextArea {
                            id: taOutputReadResponse
                            readOnly: true
                            font.pointSize: 10
                            font.family: "Ubuntu Mono"
                            selectionColor: "#0B6FAD"
                            selectedTextColor: "#FFFFFF"
                            selectByMouse: true
                            anchors.fill: parent
                            color: "#FFFFFF"
                            background: Rectangle {
                                color: "#000000"
                            }
                        }

                        Connections {
                            target: coreBean
                            function onOutputReadResponseChanged() {
                                taOutputReadResponse.text = coreBean.pOutputReadResponse
                            }
                        }
                    }

                    Item {
                        id: itemOutputWriteResponse
                        Layout.fillHeight: true
                        Layout.fillWidth: true

                        TextArea {
                            id: taOutputWriteResponse
                            readOnly: true
                            font.pointSize: 10
                            font.family: "Ubuntu Mono"
                            anchors.fill: parent
                            color: "#FFFFFF"
                            background: Rectangle {
                                color: "#000000"
                            }
                        }

                        Connections {
                            target: coreBean
                            function onOutputWriteResponseChanged() {
                                taOutputWriteResponse.text = coreBean.pOutputWriteResponse
                            }
                        }
                    }

                    Item {
                        id: itemOutputButtonArea
                        height: bSendOutputWrite.height + 4
                        Layout.fillWidth: true

                        Button {
                            id: bSendOutputWrite
                            height: 40
                            anchors.right: itemOutputButtonArea.right
                            text: qsTr("Send output")
                            anchors.verticalCenter: parent.verticalCenter
                            onClicked: coreController.writeOutput()
                        }
                        Rectangle {
                            color: "#00450010"
                            anchors.fill: parent

                        }
                    }
                }
            }

            Item {
                id: itemStatus

                GridLayout {
                    id: glStatus
                    anchors.fill: parent
                    visible: true
                    rows: 1
                    columns: 1

                    Item {
                        id: itemStatusResponse
                        Layout.rowSpan: 1
                        Layout.fillHeight: true
                        Layout.fillWidth: true

                        TextArea {
                            id: taStatusResponse
                            readOnly: true
                            font.pointSize: 10
                            font.family: "Ubuntu Mono"
                            selectionColor: "#0B6FAD"
                            selectedTextColor: "#FFFFFF"
                            selectByMouse: true
                            anchors.fill: parent
                            color: "#FFFFFF"
                            background: Rectangle {
                                color: "#000000"
                            }
                        }

                        Connections {
                            target: coreBean
                            function onStatusResponseChanged() {
                                taStatusResponse.text = coreBean.pStatusResponse
                            }
                        }
                    }
                }
            }

            Item {
                id: itemData

                ColumnLayout {
                    id: glData
                    anchors.fill: parent

                    Item {
                        id: itemEncoder
                        Layout.rightMargin: 10
                        Layout.leftMargin: 10
                        Layout.fillWidth: true
                        Layout.minimumHeight: 50

                        RowLayout {
                            id: rlEncoder
                            height: 50
                            anchors.left: parent.left
                            anchors.leftMargin: 0
                            anchors.right: parent.right
                            anchors.rightMargin: 0

                            TextField {
                                id: tfEncoder
                                font.family: "Ubuntu Mono Regular"
                                placeholderText: "Insert map filepath"
                                Layout.fillWidth: true
                                selectByMouse: true
                                selectionColor: "#0B6FAD"
                                selectedTextColor: "#FFFFFF"
                                KeyNavigation.tab: tfModulationTable
                                //                                onEditingFinished: coreBean.pMapFilepath = text
                                onTextChanged: coreBean.pMapFilepath = text
                            }

                            FileDialog {
                                id: fdEncoder
                                title: "Selezione mappa encoder"
                                selectMultiple: false
                                modality: Qt.ApplicationModal
                                onAccepted: {
                                    console.log("You chose: " + fileUrl)
                                    tfEncoder.text = fileUrl.toString().replace("file://", "")
                                }
                            }

                            Button {
                                id: bEncoderChoose
                                Layout.minimumWidth: 30
                                Layout.maximumWidth: 30
                                text: qsTr("...")
                                onClicked: {
                                    var path = Qt.resolvedUrl("./../../data-generators")
                                    console.log(path)
                                    fdEncoder.folder = Qt.resolvedUrl(path)
                                    fdEncoder.open()
                                }
                            }

                            Button {
                                id: bEncoder
                                Layout.minimumWidth: 200
                                text: qsTr("SEND ENCODER MAP")
                                onClicked: coreController.sendEncoderMap()
                            }
                        }
                    }

                    Item {
                        id: itemModulationTable
                        Layout.rightMargin: 10
                        Layout.leftMargin: 10
                        Layout.fillWidth: true
                        Layout.minimumHeight: 50

                        RowLayout {
                            id: rlModulationTable
                            height: 50
                            anchors.left: parent.left
                            anchors.leftMargin: 0
                            anchors.right: parent.right
                            anchors.rightMargin: 0

                            TextField {
                                id: tfModulationTable
                                font.family: "Ubuntu Mono Regular"
                                placeholderText: "Insert modulation table filepath"
                                Layout.fillWidth: true
                                selectByMouse: true
                                selectionColor: "#0B6FAD"
                                selectedTextColor: "#FFFFFF"
                                KeyNavigation.tab: tfImage
                                //                                onEditingFinished: coreBean.pModulationTableFilepath = text
                                onTextChanged: coreBean.pModulationTableFilepath = text
                            }

                            FileDialog {
                                id: fdModulationTable
                                title: "Selezione tabella modulazione"
                                selectMultiple: false
                                modality: Qt.ApplicationModal
                                onAccepted: {
                                    console.log("You chose: " + fileUrl)
                                    tfModulationTable.text = fileUrl.toString().replace("file://", "")
                                }
                            }

                            Button {
                                id: bModulationTableChoose
                                Layout.minimumWidth: 30
                                Layout.maximumWidth: 30
                                text: qsTr("...")
                                onClicked: {
                                    var path = Qt.resolvedUrl("./../../data-generators")
                                    console.log(path)
                                    fdModulationTable.folder = Qt.resolvedUrl(path)
                                    fdModulationTable.open()
                                }
                            }

                            Button {
                                id: bModulationTable
                                Layout.minimumWidth: 200
                                text: qsTr("SEND MODULATION TABLE")
                                onClicked: coreController.sendModulationTableMap()
                            }
                        }
                    }

                    Item {
                        id: itemImage
                        Layout.rightMargin: 10
                        Layout.leftMargin: 10
                        Layout.fillWidth: true
                        Layout.minimumHeight: 50

                        RowLayout {
                            id: rlImage
                            height: 50
                            anchors.left: parent.left
                            anchors.leftMargin: 0
                            anchors.right: parent.right
                            anchors.rightMargin: 0

                            TextField {
                                id: tfImage
                                font.family: "Ubuntu Mono Regular"
                                placeholderText: "Insert image filepath"
                                Layout.fillWidth: true
                                selectByMouse: true
                                selectionColor: "#0B6FAD"
                                selectedTextColor: "#FFFFFF"
                                KeyNavigation.tab: tfEncoder
                                //                                onEditingFinished: coreBean.pImageFilepath = text
                                onTextChanged: coreBean.pImageFilepath = text
                            }

                            FileDialog {
                                id: fdImage
                                title: "Selezione immagine"
                                selectMultiple: false
                                modality: Qt.ApplicationModal
                                onAccepted: {
                                    console.log("You chose: " + fileUrl)
                                    tfImage.text = fileUrl.toString().replace("file://", "")
                                }
                            }

                            Button {
                                id: bImageChoose
                                Layout.minimumWidth: 30
                                Layout.maximumWidth: 30
                                text: qsTr("...")
                                onClicked: {
                                    var path = Qt.resolvedUrl("./../../data-generators")
                                    console.log(path)
                                    fdImage.folder = Qt.resolvedUrl(path)
                                    fdImage.open()
                                }
                            }

                            Button {
                                id: bImage
                                Layout.minimumWidth: 200
                                text: qsTr("SEND IMAGE")
                                onClicked: coreController.sendImage()
                            }
                        }
                    }

                    Item {
                        id: test
                        Layout.fillWidth: true
                        Layout.fillHeight: true

                        RowLayout {
                            id: rowLayoutTest
                            anchors.fill: parent

                            Item {
                                id: itemDataResponse
                                Layout.fillHeight: true
                                Layout.fillWidth: true

                                ScrollView {
                                    id: svDataResponse
                                    anchors.fill: parent
                                    Layout.fillHeight: true
                                    Layout.fillWidth: true

                                    TextArea {
                                        id: taDataResponse
                                        readOnly: false
                                        font.pointSize: 10
                                        font.family: "Ubuntu Mono"
                                        selectionColor: "#0B6FAD"
                                        selectedTextColor: "#FFFFFF"
                                        selectByMouse: true
                                        color: "#FFFFFF"

                                        background: Rectangle {
                                            color: "#000000"
                                        }

                                        Connections {
                                            target: coreController
                                            function onUpdateTransferConsole(outputData) {
                                                if (taDataResponse.lineCount > 200) {
                                                    taDataResponse.clear();
                                                }
                                                taDataResponse.append(outputData)
                                            }
                                        }
                                    }
                                }
                            }


                            Item {
                                id: itemDataTransferRead
                                Layout.fillHeight: true
                                Layout.fillWidth: true

                                ScrollView {
                                    id: svDataTransferRead
                                    anchors.fill: parent
                                    Layout.fillHeight: true
                                    Layout.fillWidth: true

                                    TextArea {
                                        id: taDataTransferRead
                                        readOnly: false
                                        font.pointSize: 10
                                        font.family: "Ubuntu Mono"
                                        selectionColor: "#0B6FAD"
                                        selectedTextColor: "#FFFFFF"
                                        selectByMouse: true
                                        color: "#FFFFFF"

                                        background: Rectangle {
                                            color: "#000000"
                                        }

                                        Connections {
                                            target: coreBean
                                            function onDataTransferReadResponseChanged() {
                                                taDataTransferRead.clear();
                                                taDataTransferRead.text = coreBean.pDataTransferReadResponse
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }

                }
            }


            Item {
                id: itemUtils

                GridLayout {
                    id: glUtils
                    anchors.rightMargin: 10
                    anchors.leftMargin: 10
                    anchors.bottomMargin: 10
                    anchors.topMargin: 10
                    anchors.fill: parent

                    GridLayout {
                        id: glUtilsEdit
                        columnSpacing: 10
                        columns: 2
                        Layout.fillWidth: true
                        Layout.fillHeight: true

                        Text {
                            id: tEncoderPulses
                            text: qsTr("Impulsi encoder")
                            font.pixelSize: 12
                        }

                        TextField {
                            id: tfEncoderPulses
                            text: qsTr("")
                            font.family: "Ubuntu Mono Regular"
                            selectByMouse: true
                            selectionColor: "#0B6FAD"
                            selectedTextColor: "#FFFFFF"
                            horizontalAlignment: Text.AlignRight
                            validator: IntValidator {
                                bottom: 0
                                top: 8388608
                            }
                            onEditingFinished: coreBean.pEncoderPulses = text
                        }

                        Text {
                            id: tFileChunkSize
                            text: qsTr("Chunk file size [MB]")
                            font.pixelSize: 12
                        }

                        TextField {
                            id: tfFileChunkSize
                            text: qsTr("")
                            font.family: "Ubuntu Mono Regular"
                            selectByMouse: true
                            selectionColor: "#0B6FAD"
                            selectedTextColor: "#FFFFFF"
                            horizontalAlignment: Text.AlignRight
                            validator: IntValidator {
                                bottom: 0
                            }
                            onEditingFinished: coreBean.pFileChunkSize = text
                        }

                        Item {
                            id: element1
                            width: 200
                            height: 200
                            Layout.fillWidth: true
                            Layout.fillHeight: true
                            Layout.columnSpan: 2
                        }

                    }

                    GridLayout {
                        id: glUtilsReadOnly
                        columnSpacing: 10
                        columns: 2
                        Layout.fillHeight: true
                        Layout.fillWidth: true

                        Text {
                            id: tPeriodTestTime
                            text: qsTr("Period test time [ns]")
                            font.pixelSize: 12
                        }

                        TextField {
                            id: tfPeriodTestTime
                            text: coreBean.pPeriodTestTime
                            font.family: "Ubuntu Mono Regular"
                            selectByMouse: true
                            selectionColor: "#0B6FAD"
                            selectedTextColor: "#FFFFFF"
                            horizontalAlignment: Text.AlignRight
                            readOnly: true
                        }

                        Text {
                            id: tNumPeriodChannel
                            text: qsTr("Number periods channel")
                            font.pixelSize: 12
                        }

                        TextField {
                            id: tfNumPeriodChannel
                            text: Number(coreBean.pNumPeriodChannel).toLocaleString(Qt.locale(), "f", 3)
                            font.family: "Ubuntu Mono Regular"
                            selectByMouse: true
                            selectionColor: "#0B6FAD"
                            selectedTextColor: "#FFFFFF"
                            horizontalAlignment: Text.AlignRight
                            readOnly: true
                        }

                        Text {
                            id: tRotationTestTime
                            text: qsTr("Rotation test time [us]")
                            font.pixelSize: 12
                        }

                        TextField {
                            id: tfRotationTestTime
                            text: (Number(coreBean.pRotationTestTime)/1000).toLocaleString(Qt.locale(), "f", 3)
                            font.family: "Ubuntu Mono Regular"
                            selectByMouse: true
                            selectionColor:  "#0B6FAD"
                            selectedTextColor: "#FFFFFF"
                            horizontalAlignment: Text.AlignRight
                            readOnly: true
                        }

                        Text {
                            id: tDDRBlockSize
                            text: qsTr("DDR block size [elem]")
                            font.pixelSize: 12
                        }

                        TextField {
                            id: tfDDRBlockSize
                            text: coreBean.pDDRBlockSize
                            font.family: "Ubuntu Mono Regular"
                            selectByMouse: true
                            selectionColor: "#0B6FAD"
                            selectedTextColor: "#FFFFFF"
                            horizontalAlignment: Text.AlignRight
                            readOnly: true
                        }

                        Item {
                            id: element3
                            width: 200
                            height: 200
                            Layout.fillHeight: true
                            Layout.fillWidth: true
                            Layout.columnSpan: 2
                        }

                    }
                }
            }

        }
    }
}




