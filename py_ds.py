# -*- coding: utf-8 -*-

import sys
import os
import requests
from datetime import datetime
from threading import Thread
from PySide6 import QtCore, QtGui, QtWidgets, QtWebEngineWidgets
from PySide6.QtCore import QTimer, QUrl, QMetaObject, Qt, Slot
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import QFileDialog, QMessageBox, QInputDialog

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        # 增大窗口尺寸
        Dialog.resize(1200, 800)
        Dialog.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #cccccc;
                border-radius: 5px;
                margin-top: 1ex;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
            QPushButton {
                background-color: #4CAF50;
                border: none;
                color: white;
                padding: 5px 10px;
                border-radius: 3px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
            QLineEdit, QTextEdit {
                border: 1px solid #cccccc;
                border-radius: 3px;
                padding: 5px;
                font-size: 12px;
            }
            QProgressBar {
                border: 1px solid #cccccc;
                border-radius: 3px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #4CAF50;
            }
        """)
        
        # 地址栏和搜索按钮
        self.lineEdit = QtWidgets.QLineEdit(Dialog)
        self.lineEdit.setGeometry(QtCore.QRect(10, 10, 800, 35))
        self.lineEdit.setObjectName("lineEdit")
        
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(820, 10, 80, 35))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        
        # 浏览器显示区域
        self.groupBox = QtWidgets.QGroupBox(Dialog)
        self.groupBox.setGeometry(QtCore.QRect(10, 60, 900, 600))
        self.groupBox.setObjectName("groupBox")
        
        self.webEngineView = QtWebEngineWidgets.QWebEngineView(self.groupBox)
        self.webEngineView.setGeometry(QtCore.QRect(10, 20, 880, 570))
        self.webEngineView.setStyleSheet("QWebEngineView { background: white; }")
        self.webEngineView.setUrl(QtCore.QUrl("about:blank"))
        self.webEngineView.setObjectName("webEngineView")
        
        # 进度条
        self.groupBox_2 = QtWidgets.QGroupBox(Dialog)
        self.groupBox_2.setGeometry(QtCore.QRect(10, 670, 900, 50))
        self.groupBox_2.setObjectName("groupBox_2")
        
        self.progressBar = QtWidgets.QProgressBar(self.groupBox_2)
        self.progressBar.setGeometry(QtCore.QRect(10, 15, 880, 25))
        self.progressBar.setProperty("value", 100)
        self.progressBar.setObjectName("progressBar")
        
        # 右侧功能区
        # 时间显示
        self.groupBox_3 = QtWidgets.QGroupBox(Dialog)
        self.groupBox_3.setGeometry(QtCore.QRect(920, 10, 270, 80))
        self.groupBox_3.setObjectName("groupBox_3")
        
        self.lcdNumber = QtWidgets.QLCDNumber(self.groupBox_3)
        self.lcdNumber.setGeometry(QtCore.QRect(20, 40, 70, 31))
        self.lcdNumber.setObjectName("lcdNumber")
        
        self.label = QtWidgets.QLabel(self.groupBox_3)
        self.label.setGeometry(QtCore.QRect(40, 20, 41, 16))
        self.label.setObjectName("label")
        
        self.lcdNumber_2 = QtWidgets.QLCDNumber(self.groupBox_3)
        self.lcdNumber_2.setGeometry(QtCore.QRect(100, 40, 70, 31))
        self.lcdNumber_2.setObjectName("lcdNumber_2")
        
        self.label_2 = QtWidgets.QLabel(self.groupBox_3)
        self.label_2.setGeometry(QtCore.QRect(120, 20, 41, 16))
        self.label_2.setObjectName("label_2")
        
        self.lcdNumber_3 = QtWidgets.QLCDNumber(self.groupBox_3)
        self.lcdNumber_3.setGeometry(QtCore.QRect(180, 40, 70, 31))
        self.lcdNumber_3.setObjectName("lcdNumber_3")
        
        self.label_3 = QtWidgets.QLabel(self.groupBox_3)
        self.label_3.setGeometry(QtCore.QRect(200, 20, 41, 16))
        self.label_3.setObjectName("label_3")
        
        # 计算器
        self.groupBox_4 = QtWidgets.QGroupBox(Dialog)
        self.groupBox_4.setGeometry(QtCore.QRect(920, 100, 270, 250))
        self.groupBox_4.setObjectName("groupBox_4")
        
        self.lineEdit_2 = QtWidgets.QLineEdit(self.groupBox_4)
        self.lineEdit_2.setGeometry(QtCore.QRect(10, 20, 250, 35))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_2.setReadOnly(True)
        
        # 计算器按钮布局
        calc_buttons = [
            ('7', 10, 60), ('8', 60, 60), ('9', 110, 60), ('/', 160, 60), ('C', 210, 60),
            ('4', 10, 100), ('5', 60, 100), ('6', 110, 100), ('*', 160, 100), ('(', 210, 100),
            ('1', 10, 140), ('2', 60, 140), ('3', 110, 140), ('-', 160, 140), (')', 210, 140),
            ('0', 10, 180), ('.', 60, 180), ('=', 110, 180), ('+', 160, 180), ('⌫', 210, 180)
        ]
        
        self.calc_buttons = {}
        for text, x, y in calc_buttons:
            btn = QtWidgets.QPushButton(self.groupBox_4)
            btn.setGeometry(QtCore.QRect(x, y, 45, 35))
            btn.setText(text)
            btn.setObjectName(f"calc_btn_{text}")
            self.calc_buttons[text] = btn
        
        # 笔记功能
        self.groupBox_5 = QtWidgets.QGroupBox(Dialog)
        self.groupBox_5.setGeometry(QtCore.QRect(920, 360, 270, 250))
        self.groupBox_5.setObjectName("groupBox_5")
        
        self.textEdit = QtWidgets.QTextEdit(self.groupBox_5)
        self.textEdit.setGeometry(QtCore.QRect(10, 20, 250, 180))
        self.textEdit.setObjectName("textEdit")
        
        self.pushButton_17 = QtWidgets.QPushButton(self.groupBox_5)
        self.pushButton_17.setGeometry(QtCore.QRect(10, 210, 80, 30))
        self.pushButton_17.setObjectName("pushButton_17")
        
        self.pushButton_18 = QtWidgets.QPushButton(self.groupBox_5)
        self.pushButton_18.setGeometry(QtCore.QRect(95, 210, 80, 30))
        self.pushButton_18.setObjectName("pushButton_18")
        
        self.pushButton_19 = QtWidgets.QPushButton(self.groupBox_5)
        self.pushButton_19.setGeometry(QtCore.QRect(180, 210, 80, 30))
        self.pushButton_19.setObjectName("pushButton_19")
        
        # 网站工具
        self.groupBox_7 = QtWidgets.QGroupBox(Dialog)
        self.groupBox_7.setGeometry(QtCore.QRect(920, 620, 270, 100))
        self.groupBox_7.setObjectName("groupBox_7")
        
        self.pushButton_21 = QtWidgets.QPushButton(self.groupBox_7)
        self.pushButton_21.setGeometry(QtCore.QRect(10, 20, 80, 30))
        self.pushButton_21.setObjectName("pushButton_21")
        
        self.pushButton_22 = QtWidgets.QPushButton(self.groupBox_7)
        self.pushButton_22.setGeometry(QtCore.QRect(95, 20, 80, 30))
        self.pushButton_22.setObjectName("pushButton_22")
        
        self.pushButton_23 = QtWidgets.QPushButton(self.groupBox_7)
        self.pushButton_23.setGeometry(QtCore.QRect(180, 20, 80, 30))
        self.pushButton_23.setObjectName("pushButton_23")
        
        self.pushButton_24 = QtWidgets.QPushButton(self.groupBox_7)
        self.pushButton_24.setGeometry(QtCore.QRect(10, 55, 120, 30))
        self.pushButton_24.setObjectName("pushButton_24")
        
        self.pushButton_25 = QtWidgets.QPushButton(self.groupBox_7)
        self.pushButton_25.setGeometry(QtCore.QRect(140, 55, 120, 30))
        self.pushButton_25.setObjectName("pushButton_25")
        
        # 检查更新
        self.groupBox_6 = QtWidgets.QGroupBox(Dialog)
        self.groupBox_6.setGeometry(QtCore.QRect(920, 730, 270, 60))
        self.groupBox_6.setObjectName("groupBox_6")
        
        self.pushButton_20 = QtWidgets.QPushButton(self.groupBox_6)
        self.pushButton_20.setGeometry(QtCore.QRect(10, 20, 250, 30))
        self.pushButton_20.setObjectName("pushButton_20")
        
        # 状态栏
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(10, 730, 1180, 20))
        self.label_4.setObjectName("label_4")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        
        # 初始化变量
        self.calc_expression = ""
        self.home_page = "https://www.bing.com"
        self.save_directory = os.path.expanduser("~")
        self.note_file = os.path.join(self.save_directory, "notes.txt")
        
        # 连接信号和槽
        self.connectSlots()
        
        # 启动定时器更新时间
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)
        self.update_time()
        
        # 加载主页
        self.load_url(self.home_page)

    def connectSlots(self):
        """连接所有信号和槽"""
        # 浏览器相关
        self.pushButton.clicked.connect(self.search_url)
        self.lineEdit.returnPressed.connect(self.search_url)
        self.webEngineView.loadProgress.connect(self.progressBar.setValue)
        self.webEngineView.loadFinished.connect(self.on_load_finished)
        
        # 计算器按钮
        calc_functions = {
            '0': '0', '1': '1', '2': '2', '3': '3', '4': '4',
            '5': '5', '6': '6', '7': '7', '8': '8', '9': '9',
            '+': '+', '-': '-', '*': '*', '/': '/',
            '(': '(', ')': ')', '.': '.'
        }
        
        for text, value in calc_functions.items():
            self.calc_buttons[text].clicked.connect(lambda checked, v=value: self.calc_button_clicked(v))
        
        self.calc_buttons['='].clicked.connect(self.calculate_result)
        self.calc_buttons['C'].clicked.connect(self.clear_calculator)
        self.calc_buttons['⌫'].clicked.connect(self.backspace_calculator)
        
        # 笔记功能
        self.pushButton_17.clicked.connect(self.save_note)
        self.pushButton_18.clicked.connect(self.share_note)
        self.pushButton_19.clicked.connect(self.clear_note)
        
        # 其他功能
        self.pushButton_20.clicked.connect(self.check_update)
        self.pushButton_21.clicked.connect(self.force_refresh)
        self.pushButton_22.clicked.connect(self.force_quit)
        self.pushButton_23.clicked.connect(self.manage_cookies)
        self.pushButton_24.clicked.connect(self.home_settings)
        self.pushButton_25.clicked.connect(self.show_history)

    def update_time(self):
        """更新时间显示"""
        now = datetime.now()
        self.lcdNumber.display(now.year)
        self.lcdNumber_2.display(now.month)
        self.lcdNumber_3.display(now.day)

    def search_url(self):
        """搜索或打开URL"""
        url = self.lineEdit.text().strip()
        if not url:
            return
            
        if not url.startswith(('http://', 'https://')):
            # 如果不是完整的URL，使用Bing搜索
            url = f"https://www.bing.com/search?q={url}"
        self.load_url(url)

    def load_url(self, url):
        """加载URL"""
        self.webEngineView.setUrl(QUrl(url))
        self.lineEdit.setText(url)

    def on_load_finished(self, ok):
        """页面加载完成"""
        if ok:
            self.progressBar.setValue(100)
            current_url = self.webEngineView.url().toString()
            self.lineEdit.setText(current_url)
        else:
            self.progressBar.setValue(0)
            QMessageBox.warning(None, "加载失败", "网页加载失败，请检查URL是否正确")

    def calc_button_clicked(self, value):
        """计算器按钮点击"""
        self.calc_expression += value
        self.lineEdit_2.setText(self.calc_expression)

    def clear_calculator(self):
        """清空计算器"""
        self.calc_expression = ""
        self.lineEdit_2.setText("")

    def backspace_calculator(self):
        """计算器退格"""
        self.calc_expression = self.calc_expression[:-1]
        self.lineEdit_2.setText(self.calc_expression)

    def calculate_result(self):
        """计算表达式结果"""
        try:
            # 安全地计算表达式
            result = eval(self.calc_expression)
            self.lineEdit_2.setText(str(result))
            self.calc_expression = str(result)
        except Exception as e:
            self.lineEdit_2.setText("Error")
            self.calc_expression = ""

    def save_note(self):
        """保存笔记"""
        try:
            with open(self.note_file, 'w', encoding='utf-8') as f:
                f.write(self.textEdit.toPlainText())
            QMessageBox.information(None, "成功", f"笔记已保存到: {self.note_file}")
        except Exception as e:
            QMessageBox.critical(None, "错误", f"保存失败: {str(e)}")

    def share_note(self):
        """打包分享笔记"""
        try:
            file_path, _ = QFileDialog.getSaveFileName(
                None, "保存笔记文件", 
                os.path.join(self.save_directory, "my_notes.txt"),
                "Text Files (*.txt)"
            )
            if file_path:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(self.textEdit.toPlainText())
                QMessageBox.information(None, "成功", f"笔记已导出到: {file_path}")
        except Exception as e:
            QMessageBox.critical(None, "错误", f"导出失败: {str(e)}")

    def clear_note(self):
        """清空笔记"""
        reply = QMessageBox.question(None, "确认清空", "确定要清空笔记吗？",
                                   QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.textEdit.clear()

    def check_update(self):
        """检查更新 - 通过GitHub文件"""
        # 显示检查中状态
        self.pushButton_20.setText("检查中...")
        self.pushButton_20.setEnabled(False)
        
        # 在新线程中检查更新
        thread = Thread(target=self._check_update_thread)
        thread.daemon = True
        thread.start()

    def _check_update_thread(self):
        """在后台线程中检查更新"""
        try:
            # GitHub raw文件URL
            version_url = "https://raw.githubusercontent.com/VaheStudio/DeepLora_Browser/main/version"
            
            # 发送HTTP请求获取版本文件
            response = requests.get(version_url, timeout=10)
            
            if response.status_code == 200:
                version_content = response.text.strip()
                # 解析版本信息
                latest_version = self._parse_version(version_content)
                
                # 回到主线程更新UI
                QMetaObject.invokeMethod(self, "_show_update_result", 
                                       QtCore.Qt.QueuedConnection,
                                       QtCore.Q_ARG(str, latest_version),
                                       QtCore.Q_ARG(str, version_content))
            else:
                QMetaObject.invokeMethod(self, "_show_network_error", 
                                       QtCore.Qt.QueuedConnection)
                
        except Exception as e:
            print(f"检查更新错误: {e}")
            QMetaObject.invokeMethod(self, "_show_network_error", 
                                   QtCore.Qt.QueuedConnection)

    def _parse_version(self, version_content):
        """解析版本文件内容"""
        # 处理不同的版本格式
        if version_content.startswith("Version:"):
            # 格式: "Version: Alpha1.0.1"
            return version_content.split(":", 1)[1].strip()
        elif version_content.startswith("v") or version_content.startswith("Alpha"):
            # 格式: "Alpha1.0.1" 或 "v1.0.1"
            return version_content
        else:
            # 其他格式，直接返回
            return version_content

    @Slot(str, str)
    def _show_update_result(self, latest_version, version_content):
        """显示更新结果"""
        # 恢复按钮状态
        self.pushButton_20.setText("检查更新(Official Website)")
        self.pushButton_20.setEnabled(True)
        
        current_version = "Alpha 1.0.1"
        download_url = "https://github.com/VaheStudio/DeepLora_Browser"
        
        # 标准化版本字符串进行比较
        current_clean = self._clean_version_string(current_version)
        latest_clean = self._clean_version_string(latest_version)
        
        print(f"当前版本: {current_version}, 最新版本: {latest_version}")
        
        if latest_clean != current_clean:
            reply = QMessageBox.question(
                None, 
                "发现新版本", 
                f"当前版本: {current_version}\n最新版本: {latest_version}\n\n是否前往下载页面？",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.Yes
            )
            if reply == QMessageBox.Yes:
                self.load_url(download_url)
        else:
            QMessageBox.information(None, "检查更新", "当前已是最新版本！")

    def _clean_version_string(self, version_str):
        """清理版本字符串用于比较"""
        # 移除空格和特殊字符，只保留版本号部分
        cleaned = version_str.replace(' ', '').replace('Alpha', '').replace('alpha', '')
        return cleaned

    @Slot()
    def _show_network_error(self):
        """显示网络错误"""
        self.pushButton_20.setText("检查更新(Official Website)")
        self.pushButton_20.setEnabled(True)
        QMessageBox.warning(None, "检查更新", "网络连接失败，请检查网络后重试")

    def force_refresh(self):
        """强制刷新页面"""
        self.webEngineView.reload()

    def force_quit(self):
        """强制退出"""
        reply = QMessageBox.question(None, "确认退出", "确定要退出程序吗？",
                                   QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            sys.exit()

    def manage_cookies(self):
        """管理cookies"""
        QMessageBox.information(None, "Cookie管理", "Cookie管理功能正在开发中...")

    def home_settings(self):
        """主页设置"""
        new_home, ok = QInputDialog.getText(
            None, "主页设置", "请输入主页URL:", text=self.home_page
        )
        if ok and new_home:
            self.home_page = new_home
            QMessageBox.information(None, "成功", f"主页已设置为: {new_home}")

    def show_history(self):
        """显示历史记录"""
        QMessageBox.information(None, "历史记录", "历史记录功能正在开发中...")

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "DeepLora Browser - 增强版"))
        self.lineEdit.setText(_translate("Dialog", "https://www.bing.com"))
        self.pushButton.setText(_translate("Dialog", "🔍 搜索"))
        self.groupBox.setTitle(_translate("Dialog", "浏览器"))
        self.groupBox_2.setTitle(_translate("Dialog", "加载进度"))
        self.groupBox_3.setTitle(_translate("Dialog", "时间"))
        self.label.setText(_translate("Dialog", "年"))
        self.label_2.setText(_translate("Dialog", "月"))
        self.label_3.setText(_translate("Dialog", "日"))
        self.groupBox_4.setTitle(_translate("Dialog", "计算器"))
        self.groupBox_5.setTitle(_translate("Dialog", "笔记"))
        self.pushButton_17.setText(_translate("Dialog", "保存"))
        self.pushButton_18.setText(_translate("Dialog", "导出"))
        self.pushButton_19.setText(_translate("Dialog", "清空"))
        self.groupBox_7.setTitle(_translate("Dialog", "工具"))
        self.pushButton_21.setText(_translate("Dialog", "刷新"))
        self.pushButton_22.setText(_translate("Dialog", "退出"))
        self.pushButton_23.setText(_translate("Dialog", "Cookies"))
        self.pushButton_24.setText(_translate("Dialog", "主页设置"))
        self.pushButton_25.setText(_translate("Dialog", "历史记录"))
        self.groupBox_6.setTitle(_translate("Dialog", "更新"))
        self.pushButton_20.setText(_translate("Dialog", "检查更新"))
        self.label_4.setText(_translate("Dialog", "2025 DeepLora™版权所有  VaheStudio汉化支持  Github: github.com/vahestudio DeepLora联系方式: LanJusuntar@markline.dpdns.org  软件版本: Alpha 1.0.1"))


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
