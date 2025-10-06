import sys
import os
import pandas as pd
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
                             QWidget, QMessageBox, QCheckBox, QGroupBox)
from PyQt5.QtChart import QChart, QChartView, QLineSeries, QCategoryAxis
from PyQt5.QtGui import QPainter
from PyQt5.QtCore import Qt

def resource_path(relative_path):
    """取得資源的絕對路徑,適用於開發和打包後的環境"""
    try:
        # PyInstaller 打包後的臨時資料夾路徑
        base_path = sys._MEIPASS
    except Exception:
        # 開發環境中使用當前目錄
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)

class SimpleChart(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("2018-2024 食品銷售趨勢")
        self.resize(1000, 600)

        # 讀取 CSV 檔案
        file_path = resource_path("cleaned_forpyqt.csv")
        self.df = pd.read_csv(file_path)

        # 儲存資料
        self.x_values = self.df.iloc[:, 0].astype(str).tolist()
        self.data_columns = self.df.columns[1:6].tolist()  # 選第 2 到第 6 欄
        
        # 建立主要容器
        container = QWidget()
        main_layout = QVBoxLayout(container)
        
        # 建立複選框區域
        checkbox_group = QGroupBox("選擇要顯示的資料")
        checkbox_layout = QHBoxLayout()
        
        self.checkboxes = {}
        for col in self.data_columns:
            checkbox = QCheckBox(col)
            checkbox.setChecked(True)  # 預設全部勾選
            checkbox.stateChanged.connect(self.update_chart)
            self.checkboxes[col] = checkbox
            checkbox_layout.addWidget(checkbox)
        
        checkbox_group.setLayout(checkbox_layout)
        main_layout.addWidget(checkbox_group)
        
        # 建立圖表
        self.chart = QChart()
        self.chart.setTitle("2018-2024 食品銷售趨勢_波動最大的五項")
        
        self.chart_view = QChartView(self.chart)
        self.chart_view.setRenderHint(QPainter.Antialiasing)
        
        main_layout.addWidget(self.chart_view)
        self.setCentralWidget(container)
        
        # 初始繪製圖表
        self.update_chart()

    def update_chart(self):
        """更新圖表顯示"""
        # 清除現有的系列
        self.chart.removeAllSeries()
        
        # 根據勾選狀態添加折線
        for col in self.data_columns:
            if self.checkboxes[col].isChecked():
                series = QLineSeries()
                series.setName(col)
                y_values = self.df[col].tolist()
                for i, y in enumerate(y_values):
                    series.append(i, y)
                self.chart.addSeries(series)
        
        # 重新建立座標軸
        self.chart.createDefaultAxes()
        
        # 設定 Y 軸標題
        axis_y = self.chart.axisY()
        if axis_y:
            axis_y.setTitleText("銷售指數")
        
        # 設定 X 軸
        axis_x = QCategoryAxis()
        axis_x.setTitleText("時間")
        for i, label in enumerate(self.x_values):
            if i % 5 == 0:  # 每五格顯示一次標籤以避免重疊
                axis_x.append(label, i)
        axis_x.setLabelsAngle(45)  # 文字旋轉 45 度
        
        # 將座標軸應用到所有系列
        if self.chart.series():
            self.chart.setAxisX(axis_x, self.chart.series()[0])
            for s in self.chart.series():
                s.attachAxis(axis_x)
                s.attachAxis(axis_y)

def main():
    app = QApplication(sys.argv)
    window = SimpleChart()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()