import sys
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QTableWidgetItem,
    QMessageBox,
    QInputDialog,
    QHeaderView
)

from kasir import Ui_Form


class KasirApp(QWidget):
    def __init__(self):
        super().__init__()

        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.total_bayar = 0

        # ── STYLESHEET UTAMA ──────────────────────────────────
        self.setStyleSheet("""
    QWidget {
        background-color: #1e1e2e;
        color: #cdd6f4;
        font-family: 'Segoe UI';
    }

    QLabel {
        color: #89b4fa;
        font-weight: bold;
    }

    QLineEdit {
        background-color: #313244;
        color: #cdd6f4;
        border: 2px solid #89b4fa;
        border-radius: 4px;
        padding: 2px 4px;
    }

    QSpinBox {
        background-color: #313244;
        color: #cdd6f4;
        border: 2px solid #89b4fa;
        border-radius: 4px;
    }

    QPushButton {
        background-color: #89b4fa;
        color: #1e1e2e;
        border: none;
        border-radius: 4px;
        font-weight: bold;
    }
    QPushButton:hover {
        background-color: #b4befe;
    }
    QPushButton:pressed {
        background-color: #cba6f7;
    }

    QPushButton#pushButton_3,
    QPushButton#pushButton_5,
    QPushButton#pushButton_7,
    QPushButton#pushButton_8 {
        background-color: #f38ba8;
        color: #1e1e2e;
    }

    QPushButton#pushButton_10 {
        background-color: #a6e3a1;
        color: #1e1e2e;
    }

    QPushButton#pushButton_2 {
        background-color: #f9e2af;
        color: #1e1e2e;
    }

    QTableWidget {
        background-color: #181825;
        color: #cdd6f4;
        gridline-color: #45475a;
        border: 1px solid #45475a;
    }
    QTableWidget::item:selected {
        background-color: #89b4fa;
        color: #1e1e2e;
    }
    QTableWidget::item:alternate {
        background-color: #1e1e2e;
    }
    QHeaderView::section {
        background-color: #313244;
        color: #89dceb;
        font-weight: bold;
        border: 1px solid #45475a;
    }
""")
        # ─────────────────────────────────────────────────────

        # Setup tabel
        self.ui.tableWidget.setRowCount(0)
        self.ui.tableWidget.setColumnCount(4)
        self.ui.tableWidget.setHorizontalHeaderLabels(
            ["Nama Barang", "Harga", "Jumlah", "Subtotal"]
        )

        header = self.ui.tableWidget.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        self.ui.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.ui.tableWidget.verticalHeader().setVisible(False)
        self.ui.tableWidget.verticalHeader().setDefaultSectionSize(35)
        self.ui.tableWidget.setAlternatingRowColors(True)
        self.ui.tableWidget.setShowGrid(True)

        # Tombol Tambah
        self.ui.pushButton.clicked.connect(
            lambda: self.tambah_barang(self.ui.lineEdit.text(), 17000, self.ui.spinBox.value())
        )
        self.ui.pushButton_4.clicked.connect(
            lambda: self.tambah_barang(self.ui.lineEdit_3.text(), 75000, self.ui.spinBox_2.value())
        )
        self.ui.pushButton_6.clicked.connect(
            lambda: self.tambah_barang(self.ui.lineEdit_6.text(), 34000, self.ui.spinBox_3.value())
        )
        self.ui.pushButton_9.clicked.connect(
            lambda: self.tambah_barang(self.ui.lineEdit_7.text(), 45000, self.ui.spinBox_4.value())
        )

        # Tombol Hapus
        self.ui.pushButton_5.clicked.connect(self.hapus_barang)
        self.ui.pushButton_3.clicked.connect(self.hapus_barang)
        self.ui.pushButton_7.clicked.connect(self.hapus_barang)
        self.ui.pushButton_8.clicked.connect(self.hapus_barang)

        # Tombol Total & Kembalian
        self.ui.pushButton_10.clicked.connect(self.hitung_total)
        self.ui.pushButton_2.clicked.connect(self.hitung_kembalian)

    def tambah_barang(self, nama, harga, jumlah):
        if jumlah <= 0:
            QMessageBox.warning(self, "Peringatan", "Jumlah barang harus lebih dari 0")
            return
        subtotal = harga * jumlah
        row = self.ui.tableWidget.rowCount()
        self.ui.tableWidget.insertRow(row)
        self.ui.tableWidget.setItem(row, 0, QTableWidgetItem(nama))
        self.ui.tableWidget.setItem(row, 1, QTableWidgetItem(f"Rp {harga:,}"))
        self.ui.tableWidget.setItem(row, 2, QTableWidgetItem(str(jumlah)))
        self.ui.tableWidget.setItem(row, 3, QTableWidgetItem(f"Rp {subtotal:,}"))

    def hapus_barang(self):
        row = self.ui.tableWidget.currentRow()
        if row >= 0:
            self.ui.tableWidget.removeRow(row)
        else:
            QMessageBox.warning(self, "Peringatan", "Pilih data yang akan dihapus!")

    def hitung_total(self):
        self.total_bayar = 0
        for row in range(self.ui.tableWidget.rowCount()):
            subtotal_text = self.ui.tableWidget.item(row, 3).text()
            subtotal = int(subtotal_text.replace("Rp", "").replace(",", "").replace(" ", ""))
            self.total_bayar += subtotal
        QMessageBox.information(self, "Total Bayar", f"Total Belanja = Rp {self.total_bayar:,}")

    def hitung_kembalian(self):
        if self.total_bayar == 0:
            QMessageBox.warning(self, "Peringatan", "Klik TOTAL BAYAR terlebih dahulu!")
            return
        uang_dibayar, ok = QInputDialog.getInt(
            self, "Pembayaran", "Masukkan jumlah uang yang dibayarkan:", min=0
        )
        if ok:
            if uang_dibayar < self.total_bayar:
                QMessageBox.warning(self, "Peringatan", f"Uang kurang Rp {self.total_bayar - uang_dibayar:,}")
            else:
                kembalian = uang_dibayar - self.total_bayar
                QMessageBox.information(
                    self, "Struk Pembayaran",
                    f"Total Belanja : Rp {self.total_bayar:,}\n\n"
                    f"Uang Dibayar : Rp {uang_dibayar:,}\n\n"
                    f"Kembalian    : Rp {kembalian:,}"
                )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = KasirApp()
    window.show()
    sys.exit(app.exec())