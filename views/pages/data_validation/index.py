from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton

from views.pages.data_validation.variance_Inflation_factor import VIFWindow


class AdditionalWindows(QWidget):
    """包含 6 个按钮的页面，其中一个用于打开 VIF 分析窗口。"""

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        vif = QPushButton("VIF因子独立性检验")
        vif.clicked.connect(self.open_vif_window)
        layout.addWidget(vif)

        self.setLayout(layout)

    def open_vif_window(self):
        self.vif_window = VIFWindow()
        self.vif_window.show()
