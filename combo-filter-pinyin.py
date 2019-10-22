# from https://stackoverflow.com/questions/4827207/how-do-i-filter-the-pyqt-qcombobox-items-based-on-the-text-input?answertab=active#tab-top
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QSortFilterProxyModel, QRegExp
from PyQt5.QtWidgets import QCompleter, QComboBox, QApplication
from PyQt5.QtGui import QStandardItem, QStandardItemModel
from getPinYin import vagueOrderedSearch, getPinyinStr

class MySortFilterProxyModel(QSortFilterProxyModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.searchitem = None
        self.invalidatetime = 0

    def myfilter(self, text):
        # self.setFilterRegExp(QRegExp(text))
        self.searchitem = getPinyinStr(text)
        # print(self.searchitem)
        self.invalidateFilter()

    def filterAcceptsRow(self, sourceRow, sourceParent):
        search = self.searchitem
        index = self.sourceModel().index(sourceRow, 0, sourceParent)
        data_str = getPinyinStr(self.sourceModel().data(index))

        if self.searchitem:
            if not vagueOrderedSearch(search, data_str):
                # print("{} : {} : {}".format(False, search , data_str))
                return False
            else:
                # print('True for seach {} in {}'.format(search, data_str))
                return True
        else:
            return True

class ExtendedCombo( QComboBox ):
    def __init__( self,  parent = None):
        super( ExtendedCombo, self ).__init__( parent )

        self.setFocusPolicy( Qt.StrongFocus )
        self.setEditable( True )
        self.completer = QCompleter( self )

        # always show all completions
        self.completer.setCompletionMode( QCompleter.UnfilteredPopupCompletion )
        self.pFilterModel = MySortFilterProxyModel( self )
        self.pFilterModel.setFilterCaseSensitivity( Qt.CaseInsensitive )



        self.completer.setPopup( self.view() )


        self.setCompleter( self.completer )


        self.lineEdit().textEdited[str].connect( self.pFilterModel.myfilter )
        self.completer.activated.connect(self.setTextIfCompleterIsClicked)

    def setModel( self, model ):
        super(ExtendedCombo, self).setModel( model )
        self.pFilterModel.setSourceModel( model )
        self.completer.setModel(self.pFilterModel)

    def setModelColumn( self, column ):
        self.completer.setCompletionColumn( column )
        self.pFilterModel.setFilterKeyColumn( column )
        super(ExtendedCombo, self).setModelColumn( column )


    def view( self ):
        return self.completer.popup()

    def index( self ):
        return self.currentIndex()

    def setTextIfCompleterIsClicked(self, text):
      if text:
        index = self.findText(text)
        self.setCurrentIndex(index)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    model = QStandardItemModel()

    for i,word in enumerate( ['hola muchachos', 'adios amigos', 'hello world', 'good bye', 'listen', 'powerful', 'plant', 'plain', '汉子', '牛逼','中华人民共和国'] ):
        item = QStandardItem(word)
        model.setItem(i, 0, item)



    combo = ExtendedCombo()
    combo.setModel(model)
    combo.setModelColumn(0)
    combo.resize(300, 40)
    combo.setCurrentIndex(combo.model().rowCount()-1)

    combo.show()

    sys.exit(app.exec_())