import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQml.Models
import QtQuick.Window

ApplicationWindow {
    id: mainWindow
    width: 900
    height: 700
    visible: true

    Image {
        anchors.fill: parent
        source: "../resources/pictures/k2-18b.png"
        fillMode: Image.PreserveAspectCrop
    }

    Connections {
        target: theplanet

        function onUpdate_planet_image() {
            imagePlanets.reload();
        }
    }

    GridLayout {
        id: laySelectPlanets
        width: 300
        anchors.left: parent.left
        anchors.leftMargin: 10
        anchors.top: parent.top
        anchors.topMargin: 15
        rows: 1
        columns: 3

        Label {
            id: label0
            text: qsTr("Planet")
            color: "white"
            font.bold: true
            font.pixelSize: 20
        }

        ComboBox {
            id: comboBoxSelectPlanets
            model: ["TOI-700 d", "ROSS-128 b", "TRAPPIST-1 e", "KEPLER-62 e"]
            Layout.fillWidth: true
        }

        Button {
            id: buttonGetInfo
            text: qsTr("Get Info")
            Layout.fillWidth: false

            onClicked: {
                textDisplayDiscoveryLog.text = textDisplayDiscoveryLog.text + "\n";
                textDisplayParams.text = textDisplayParams.text + "\n";

                var user_data = {
                    "planet": comboBoxSelectPlanets.currentText
                };

                planetparams.params_entry(user_data);
                theplanet.display_planets(user_data);
                mydiscovery.log_entry(user_data);

            }
        }
    }

    TextInput {
        id: textInputStellarParameters
        anchors.left: parent.left
        anchors.leftMargin: 10
        anchors.top: laySelectPlanets.bottom
        anchors.topMargin: 10
        text: qsTr("Parameters")
        color: "white"
        font.bold: true
        font.pixelSize: 20
        Layout.fillWidth: true
    }

    Rectangle {
        id: rectangleParameters
        anchors.left: parent.left
        anchors.leftMargin: 10
        anchors.right: laySelectPlanets.right
        anchors.rightMargin: 0
        anchors.top: textInputStellarParameters.bottom
        anchors.topMargin: 10
        anchors.bottom: rectangleImage.bottom
        anchors.bottomMargin: 0
        color: "#64000000"

        Text {
            id: textDisplayParams
            anchors.fill: parent
            color: "white"
            font.bold: true
            font.family: "Courier"
            verticalAlignment: Text.AlignVCenter
            wrapMode: Text.Wrap

            Connections {
                target: planetparams
                function onParams_log_changed(log) {
                    textDisplayParams.text = log + "\n";
                }
            }
        }
    }

    TextInput {
        id: textInputHypotheticalImage
        anchors.right: parent.right
        anchors.rightMargin: 10
        anchors.top: parent.top
        anchors.topMargin: 10
        text: qsTr("Hypothetical Image")
        color: "white"
        font.bold: true
        font.pixelSize: 15
        Layout.fillWidth: true
    }

    Rectangle {
        id: rectangleImage
        height: 450
        anchors.left: laySelectPlanets.right
        anchors.leftMargin: 5
        anchors.right: parent.right
        anchors.rightMargin: 10
        anchors.top: textInputHypotheticalImage.bottom
        anchors.topMargin: 10
        color: "#64000000"

        Flickable {
            anchors.fill: parent
            contentWidth: Math.max(imagePlanets.width * imagePlanets.scale, rectangleImage.width)
            contentHeight: Math.max(imagePlanets.height * imagePlanets.scale, rectangleImage.height)
            clip: true

            Image {
                id: imagePlanets

                    property real zoom: 0.0
                    property real zoomStep: 0.1

                    asynchronous: false
                    cache: false
                    smooth: true
                    antialiasing: true
                    mipmap: true

                    anchors.centerIn: parent
                    fillMode: Image.PreserveAspectFit
                    transformOrigin: Item.Center
                    scale: Math.min(rectangleImage.width / width, rectangleImage.height / height, 1) + zoom
                    
                    function reload() {
                        var tempSource = source;
                        source = "";
                        source = "image://provider/";
                    }
            }
        }

        MouseArea {
            acceptedButtons: Qt.NoButton
            anchors.fill: parent
            onWheel: wheel => {
                if (wheel.angleDelta.y > 0)
                    imagePlanets.zoom = Number((imagePlanets.zoom + imagePlanets.zoomStep).toFixed(1));
                else if (imagePlanets.zoom > 0)
                    imagePlanets.zoom = Number((imagePlanets.zoom - imagePlanets.zoomStep).toFixed(1));
                wheel.accepted = true;
            }
        }
    }

    Rectangle {
        id: rectangleDiscoveryMessage
        anchors.left: parent.left
        anchors.leftMargin: 10
        anchors.right: parent.right
        anchors.rightMargin: 10
        anchors.top: rectangleImage.bottom
        anchors.topMargin: 5
        anchors.bottom: parent.bottom
        anchors.bottomMargin: 10
        color: "#64000000"

        ScrollView {
            id: discoveryLog
            anchors.fill: parent
            ScrollBar.horizontal.policy: Qt.ScrollBarAlwaysOff
            ScrollBar.vertical.policy: Qt.ScrollBarAlwaysOff

            Text {
                id: textDisplayDiscoveryLog
                text: "Discovery Log"
                width: discoveryLog.width
                color: "white"
                font.pixelSize: 15
                font.bold: true
                verticalAlignment: Text.AlignTop
                wrapMode: Text.WordWrap
                font.family: "Courier"

                Connections {
                    target: mydiscovery
                    function onDiscovery_log_changed(log) {
                        textDisplayDiscoveryLog.text = log + "\n";
                    }
                }
            }
        }
    }
}