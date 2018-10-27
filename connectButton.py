from PyQt5 import QtWidgets
import networkx as nx

from globalUsed import msgDuration

class connectButton(QtWidgets.QPushButton):
    def __init__(self, parent, **kwargs):
        super().__init__(**kwargs)

        self.parent = parent
        self.colToConnect = []

        self.setText(self.tr("建立聯結"))
        self.setAcceptDrops(True)
        self.pressed.connect(self.on_pressed)


    ####################
    #    Overloadeds
    ####################
    
    # DragEnter: check if is plain text

    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat("text/plain"):
            # TODO: add a regExpress check condition
            event.acceptProposedAction()


    # Drop: parse text to store tuple temporarily

    def dropEvent(self, event):
        # Take out the info
        text = event.mimeData().text()
        pos1 = text.find(",")
        pos2 = text.rfind(",")
        fileName = text[:pos1]
        sheetName = text[pos1+1:pos2]
        colName = text[pos2+1:]

        # Store and show hint
        t = (fileName, sheetName, colName)
        self.colToConnect.append(t)

        n = str(len(self.colToConnect))
        self.setText(self.tr("建立聯結\n+" + n))

        event.acceptProposedAction()



    ####################
    #      Slots
    ####################

    # With colNames loaded, press button will connect them

    def on_pressed(self):
        # Consider failed conditions
        if len(self.colToConnect) != 2:
            self.colToConnect.clear()
            self.setText(self.tr("建立聯結"))
            self.parent.statusBar().showMessage(
                "項目連結失敗，連結項目之數目必須為兩個", msgDuration)
            return

        infoTup1 = self.colToConnect[0]
        infoTup2 = self.colToConnect[1]

        if infoTup1[0] == infoTup2[0] and infoTup1[1] == infoTup2[1]:
            self.colToConnect.clear()
            self.setText(self.tr("建立聯結"))
            self.parent.statusBar().showMessage(
                "項目連結失敗，兩個連結項目必須來自不同的工作表", msgDuration)
            return

        # Add relationship to graph
        nodeTup1 = infoTup1[0:2]
        nodeTup2 = infoTup2[0:2]
        edgeTup1to2 = (infoTup1[2], infoTup2[2])
        edgeTup2to1 = (infoTup2[2], infoTup1[2])

        g = self.parent.relatedGraph
        g.add_node(nodeTup1)
        g.add_node(nodeTup2)
        g.add_edge(nodeTup1, nodeTup2, common=edgeTup1to2)
        g.add_edge(nodeTup2, nodeTup1, common=edgeTup2to1)

        # Set hint to normal
        self.setText(self.tr("建立聯結"))
        self.colToConnect.clear()
        self.parent.statusBar().showMessage("項目連結成功", msgDuration)
        #print("Graph becomes:")
        #print("nodes x{0}".format(g.number_of_nodes()))
        #print("edges x{0}".format(g.number_of_edges()))
        #print(g[nodeTup1][nodeTup2]['common'])
        #print(g[nodeTup2][nodeTup1]['common'])
        
