# ///////////////////////////////////////////////////////////////
#
# BY: WANDERSON M.PIMENTA
# PROJECT MADE WITH: Qt Designer and PySide6
# V: 1.0.0
#
# This project can be used freely for all uses, as long as they maintain the
# respective credits only in the Python scripts, any information in the visual
# interface (GUI) can be modified without any implication.
#
# There are limitations on Qt licenses if you want to use your products
# commercially, I recommend reading them on the official website:
# https://doc.qt.io/qtforpython/licenses.html
#
# ///////////////////////////////////////////////////////////////

# IMPORT PACKAGES AND MODULES
# ///////////////////////////////////////////////////////////////
from gui.uis.windows.main_window.functions_main_window import *
import sys
import os
from gui.uis.windows.main_window.llm_function import save_api_key, handle_llm_query
from data.data import province_list, city_dict, region_dict, code_dict, city_code_dict
from ManipulateRoadPOI import *


# IMPORT QT CORE
# ///////////////////////////////////////////////////////////////
from qt_core import *

# IMPORT SETTINGS
# ///////////////////////////////////////////////////////////////
from gui.core.json_settings import Settings

# IMPORT PY ONE DARK WINDOWS
# ///////////////////////////////////////////////////////////////
# MAIN WINDOW
from gui.uis.windows.main_window import *

# IMPORT PY ONE DARK WIDGETS
# ///////////////////////////////////////////////////////////////
from gui.widgets import *

# ADJUST QT FONT DPI FOR HIGHT SCALE AN 4K MONITOR
# ///////////////////////////////////////////////////////////////
os.environ["QT_FONT_DPI"] = "96"
# IF IS 4K MONITOR ENABLE 'os.environ["QT_SCALE_FACTOR"] = "2"'

# MAIN WINDOW
# ///////////////////////////////////////////////////////////////
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # SETUP MAIN WINDOw
        # Load widgets from "gui\uis\main_window\ui_main.py"
        # ///////////////////////////////////////////////////////////////
        self.ui = UI_MainWindow()
        self.ui.setup_ui(self)

        # LOAD SETTINGS
        # ///////////////////////////////////////////////////////////////
        settings = Settings()
        self.settings = settings.items

        # SETUP MAIN WINDOW
        # ///////////////////////////////////////////////////////////////
        self.hide_grips = True # Show/Hide resize grips
        SetupMainWindow.setup_gui(self)

        # SHOW MAIN WINDOW
        # ///////////////////////////////////////////////////////////////
        self.show()

    # LEFT MENU BTN IS CLICKED
    # Run function when btn is clicked
    # Check funtion by object name / btn_id
    # ///////////////////////////////////////////////////////////////
    def btn_clicked(self):
        # GET BT CLICKED
        btn = SetupMainWindow.setup_btns(self)

        # Remove Selection If Clicked By "btn_close_left_column"
        if btn.objectName() != "btn_settings":
            self.ui.left_menu.deselect_all_tab()

        # Get Title Bar Btn And Reset Active         
        top_settings = MainFunctions.get_title_bar_btn(self, "btn_top_settings")
        top_settings.set_active(False)

        # LEFT MENU
        # ///////////////////////////////////////////////////////////////
        
        # HOME BTN
        if btn.objectName() == "btn_home":
            # Select Menu
            self.ui.left_menu.select_only_one(btn.objectName())

            # Load Page 1
            MainFunctions.set_page(self, self.ui.load_pages.page_1)

        # WIDGETS BTN
        if btn.objectName() == "btn_widgets":
            # Select Menu
            self.ui.left_menu.select_only_one(btn.objectName())

            # Load Page 2
            MainFunctions.set_page(self, self.ui.load_pages.page_2)

        # LOAD USER PAGE
        if btn.objectName() == "btn_modelscope":
            # Select Menu
            self.ui.left_menu.select_only_one(btn.objectName())

            # Load Page 3 
            MainFunctions.set_page(self, self.ui.load_pages.page_llm)

        # BOTTOM INFORMATION
        if btn.objectName() == "btn_info":
            # CHECK IF LEFT COLUMN IS VISIBLE
            if not MainFunctions.left_column_is_visible(self):
                self.ui.left_menu.select_only_one_tab(btn.objectName())

                # Show / Hide
                MainFunctions.toggle_left_column(self)
                self.ui.left_menu.select_only_one_tab(btn.objectName())
            else:
                if btn.objectName() == "btn_close_left_column":
                    self.ui.left_menu.deselect_all_tab()
                    # Show / Hide
                    MainFunctions.toggle_left_column(self)
                
                self.ui.left_menu.select_only_one_tab(btn.objectName())

            # Change Left Column Menu
            if btn.objectName() != "btn_close_left_column":
                MainFunctions.set_left_column_menu(
                    self, 
                    menu = self.ui.left_column.menus.menu_2,
                    title = "Info tab",
                    icon_path = Functions.set_svg_icon("icon_info.svg")
                )

        # SETTINGS LEFT
        if btn.objectName() == "btn_settings" or btn.objectName() == "btn_close_left_column":
            # CHECK IF LEFT COLUMN IS VISIBLE
            if not MainFunctions.left_column_is_visible(self):
                # Show / Hide
                MainFunctions.toggle_left_column(self)
                self.ui.left_menu.select_only_one_tab(btn.objectName())
            else:
                if btn.objectName() == "btn_close_left_column":
                    self.ui.left_menu.deselect_all_tab()
                    # Show / Hide
                    MainFunctions.toggle_left_column(self)
                self.ui.left_menu.select_only_one_tab(btn.objectName())

            # Change Left Column Menu
            if btn.objectName() != "btn_close_left_column":
                MainFunctions.set_left_column_menu(
                    self, 
                    menu = self.ui.left_column.menus.menu_1,
                    title = "Settings Left Column",
                    icon_path = Functions.set_svg_icon("icon_settings.svg")
                )
        
        # TITLE BAR MENU
        # ///////////////////////////////////////////////////////////////
        
        # SETTINGS TITLE BAR
        if btn.objectName() == "btn_top_settings":
            # Toogle Active
            if not MainFunctions.right_column_is_visible(self):
                btn.set_active(True)

                # Show / Hide
                MainFunctions.toggle_right_column(self)
            else:
                btn.set_active(False)

                # Show / Hide
                MainFunctions.toggle_right_column(self)

            # Get Left Menu Btn            
            top_settings = MainFunctions.get_left_menu_btn(self, "btn_settings")
            top_settings.set_active_tab(False)            

        # DEBUG
        print(f"Button {btn.objectName()}, clicked!")

    # LEFT MENU BTN IS RELEASED
    # Run function when btn is released
    # Check funtion by object name / btn_id
    # ///////////////////////////////////////////////////////////////
    def btn_released(self):
        # GET BT CLICKED
        btn = SetupMainWindow.setup_btns(self)

        # DEBUG
        print(f"Button {btn.objectName()}, released!")

    # RESIZE EVENT
    # ///////////////////////////////////////////////////////////////
    def resizeEvent(self, event):
        SetupMainWindow.resize_grips(self)

    # MOUSE CLICK EVENTS
    # ///////////////////////////////////////////////////////////////
    def mousePressEvent(self, event):
        # SET DRAG POS WINDOW
        self.dragPos = event.globalPos()

    def on_send_clicked(self):
        # 从界面获取输入
        api_key = self.ui.load_pages.api_input.text().strip()
        user_input = self.ui.load_pages.chat_input.text().strip()

        if not user_input:
            return

        # 显示用户输入
        self.ui.load_pages.chat_display.append(f"<b>你：</b> {user_input}")
        self.ui.load_pages.chat_input.clear()

        # 调用封装方法处理模型请求
        prompt_prefix = self.ui.load_pages.prompt_hint.currentText().strip()
        reply = handle_llm_query(api_key, user_input, prompt_prefix=prompt_prefix)

        # 显示模型回复
        self.ui.load_pages.chat_display.append(f"<b>模型：</b> {reply}")

    def on_save_api_key(self):
        key = self.ui.load_pages.api_input.text()
        if key:
            save_api_key(key)

            # 弹出样式美化后的提示窗口
            msg = QMessageBox(self)
            msg.setWindowTitle("提示")
            msg.setText("✅ API Key 已成功保存！")
            msg.setIcon(QMessageBox.Information)
            msg.setStyleSheet("""
                QMessageBox {
                    background-color: #f5f6f9;
                    color: #ffffff;
                    font-size: 16px;
                    min-width: 300px;
                }
                QPushButton {
                    min-width: 80px;
                    padding: 6px;
                    font-size: 14px;
                }
            """)
            msg.exec_()
    def init_privince_combo(self):
        self.province_combo.addItem("选择省份")
        for prov in province_list:
            self.province_combo.addItem(prov)
    
    def init_city_combo(self, province):
        # print('update city combo')
        self.city_combo.clear()
        self.city_combo.addItem("全部")
        if province == "选择省份" or province == " ":
            # self.city_combo.addItem("选择城市")
            return
        if '市' in province or '行政区' in province:
            self.city_combo.addItem(province)
            # self.init_region_combo(province)
            # print('from province to region')
            return 
        city_list = city_dict[province]
        for city in city_list:
            self.city_combo.addItem(city)
    
    def init_region_combo(self, city):
        # print('update region combo, city  is ' + city)
        self.region_combo.clear()
        self.region_combo.addItem("全部")
        if city == "全部" or city == "":
            # self.region_combo.clear()
            # self.region_combo.addItem("选择区县")
            return
        region_list = region_dict[city]
        for region in region_list:
            self.region_combo.addItem(region)

    def pass_data(self, data):
        province_data = self.province_combo.currentText()
        city_data = self.city_combo.currentText()
        region_data = self.region_combo.currentText()
        # print('data1 passed' + province_data)
        self.data = (province_data, city_data, region_data)

    def select_and_filter_data(self):
        province = self.province_combo.currentText()
        city = self.city_combo.currentText()
        region = self.region_combo.currentText()
        data_list = self.filtered_data(province, city, region)
        self.table_widget.set_data(data_list)
        # print(province, city, region)

    def filtered_data(self, province, city, region):
        df = os.listdir('./data')
        df = [i for i in df if 'DF' in i]
        data_list = []
        if city == '':
            city = '全部'
        # 选择指定城市
        if city != '全部':
            print('getdata:' + city + '.')
            df_info_name = 'DF_Road_Info#' + str(code_dict[city]) + '.csv'
            dir = 'DF_' + str(code_dict[city])
            df_info = os.path.join('data',dir, df_info_name) # Data_Info#440300\DF_Road_Info#440300.csv
            if not os.path.exists(df_info):
                # 文件不存在则返回空list
                print(df_info)
                print("file not exists")
                return []
            # print(1)
            df = load_df_csv(file=df_info)
            df_road_info = load_df_csv(file=df_info)    
            df_filtered = filter_df_column(df=df_road_info,columns=['name_road','name_district'])   # 仅选用道路信息和城市信息
            # 选择指定区县 
            if region != '全部':
                df_filtered = filter_df_keyword(df=df_filtered,column='name_district', keyword=region)

            temp_list = df_filtered.to_numpy().tolist()
            data_list.append(temp_list)
            for i in temp_list:
                i.append(city)
                i.append(province)
            data_list = data_list[0]
            return data_list

        # 偷个懒，由于没有收集到全部省份的道路信息，所以只写简化的处理逻辑
        # 所有城市的道路信息
        else:
            # print('province:'+province)
            for dir in df:
                if 'DF' in dir:
                    adcode = dir[-6:]
                    city = city_code_dict[int(adcode)]
                    # print(adcode)
                    file_name = 'DF_Road_Info#' + adcode +'.csv'
                    df_info = os.path.join('data' , dir, file_name)
                    # print(df_info)
                    df_road_info = load_df_csv(file=df_info)
                    # print(df_road_info) # 有内容
                    df_filtered = filter_df_column(df=df_road_info,columns=['name_road','name_district'])
                    # df_filtered = filter_df_keyword(df=df_filtered,column='name_district', keyword=region)
                    
                    temp_list = df_filtered.to_numpy().tolist()
                    for i in temp_list:
                        i.append(city)
                        i.append(province)
                    data_list.append(temp_list)
            data_list = data_list[0]
            return data_list
    
# SETTINGS WHEN TO START
# Set the initial class and also additional parameters of the "QApplication" class
# ///////////////////////////////////////////////////////////////
if __name__ == "__main__":
    # APPLICATION
    # ///////////////////////////////////////////////////////////////
    # print(city_code_dict['440300'])
    # print(city_code_dict[440300])
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("icon.ico"))
    window = MainWindow()

    # EXEC APP
    # ///////////////////////////////////////////////////////////////
    sys.exit(app.exec_())