import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QLabel, QCheckBox, QLineEdit, QDialog, QTextBrowser, QComboBox, QMessageBox
import time
from PyQt5.QtCore import QCoreApplication, Qt, QTimer,QDateTime ,QEvent
from PyQt5.QtGui import QIcon

import pyautogui as pyauto

import keyboard
from datetime import datetime


import mim_tool
import mimmim_sys

class CustomDialog(QDialog):
    def __init__(self,parent=None):
        super().__init__(parent)
        #System Variable
        self.loop_option=None
        self.loop_num=None

        self.loop_index_list=[] # Loop를 돌리는 Index List
        self.one_index_list=[] # 한번만 실행시키는 Index List
        self.mouse_click_num_list=[] # number of mouse click

        # Dialog Variable
        self.location_list=[]
        self.label_list=[]
        self.CheckBox_list1=[]
        self.CheckBox_list2=[]
        self.CheckBox_list3=[]
        self.CheckBox_list4=[]
        self.CheckBox_list5=[]
        
        self.Text_list=[]

        # Time Info
        self.startTime=None
        self.checkTime=None
        self.checkPoint=0

        # Auto Timer for automation
        self.atTimer=QTimer()
        self.atTimer.setInterval(mimmim_sys.MOUSE_AUTO_INTERVAL)
        self.atTimer.timeout.connect(self.auto_start)
        
        self.counted_loop_num=0

        # Option1 - Function Start Timer
        self.timer_on=False
        self.timer_input=None
        self.timer_info={}
        self.timer_start=False 

        self.timer_label_cnt=0 # for label change

        # Option2 - Alarm
        self.Alarm_on=False
         
        # Dialog Setting
        self.setWindowTitle('Auto Run')
        self.setWindowIcon(QIcon('mim_favicon.png'))
        self.setGeometry(300, 300, 300, 300)
        #asd
        # Telegram Info
        self.telegram_API=None
        self.telegram_UserID=None


        # Component
        self.info_textBrowser=QTextBrowser()
        self.info_textBrowser.setAcceptRichText(True)
        self.info_textBrowser.setOpenExternalLinks(True)


        # Layout1 - State Show
        self.mode_label = QLabel('[Mode]', self)
        self.mode_label.setStyleSheet("font-weight: bold")
        self.mode_label_val = QLabel(self)
        
        self.mode_label_val.setText("Ready")

        self.state_label = QLabel('[State]', self)
        self.state_label.setStyleSheet("font-weight: bold")
        self.state_label_val = QLabel(self)
   

        self.Dia_Hbox_state = QHBoxLayout()
        self.Dia_Hbox_state.addWidget(self.mode_label) 
        self.Dia_Hbox_state.addWidget(self.mode_label_val) 
        self.Dia_Hbox_state.addWidget(self.state_label) 
        self.Dia_Hbox_state.addWidget(self.state_label_val) 


        # Layout2 - Start & Stop Button
        self.auto_start_Btn = QPushButton('Start', self)
        self.auto_start_Btn.setCheckable(True)
        self.auto_start_Btn.clicked.connect(self.auto_Start_btn_click)

        self.cancel_Btn = QPushButton('Cancel', self)
        self.cancel_Btn.setCheckable(True)
        self.cancel_Btn.clicked.connect(self.cancel_btn_click)
    
        self.Dia_Hbox_Button = QHBoxLayout()

        self.Dia_Hbox_Button.addWidget(self.auto_start_Btn) 
        self.Dia_Hbox_Button.addWidget(self.cancel_Btn) 
    
        self.Dia_vbox = QVBoxLayout()


        # Layout3 - Automation Info
        self.Dia_Hbox_autoInfo = QHBoxLayout()
        self.Dia_Hbox_autoInfo.addWidget(self.info_textBrowser)

        # Total Layout Setting
        self.Dia_vbox.addLayout( self.Dia_Hbox_state)
        self.Dia_vbox.addLayout( self.Dia_Hbox_Button)
        self.Dia_vbox.addLayout( self.Dia_Hbox_autoInfo)


        self.setLayout(self.Dia_vbox)

    def event(self, event): 
        if event.type() == QEvent.EnterWhatsThisMode:
        #    print ("click")
            QMessageBox.information(self,'MIMMIM','Mikung is Cute KingKing Princess!')
            return True
        #return True
        return QDialog.event(self, event)

    def cancel_btn_click(self):
        sys.exit(0)


    def get_mouse_funcType(self,idx):
        if self.mouse_click_num_list[idx]==1: 
            return "One Click"
        elif self.mouse_click_num_list[idx]==2:
            return "Double Click" 
        else:                                 
            if self.CheckBox_list4[idx].isChecked()==True and self.CheckBox_list5[idx].isChecked()==False:                  
                return "Scroll Up"
            elif self.CheckBox_list4[idx].isChecked()==False and self.CheckBox_list5[idx].isChecked()==True:  
                return "Scroll Down"


    def auto_Start_btn_click(self):
        # Check Auto Start Available
        if self.location_list!=[]: # there is no mouse location input

            self.counted_loop_num=0 # count reset
            self.info_textBrowser.clear()
            
            if self.timer_on==True:
                self.mode_label_val.setText("Timer Waiting")
            else:
                self.mode_label_val.setText("Auto Run")

            # Divide list
            for idx in range(len(self.location_list)):
                # (1) Divide Work by two (Loop Work, One Work)
                if self.CheckBox_list3[idx].isChecked()==True:
                    self.one_index_list.append(idx)
                else:
                    self.loop_index_list.append(idx)

                # (2) Make Mouse Click Num List
                if self.CheckBox_list1[idx].isChecked()==True and self.CheckBox_list2[idx].isChecked()!=True:
                    self.mouse_click_num_list.append(1)
                elif self.CheckBox_list1[idx].isChecked()!=True and self.CheckBox_list2[idx].isChecked()==True:
                    self.mouse_click_num_list.append(2)
                
                elif self.CheckBox_list4[idx].isChecked()==True or self.CheckBox_list5[idx].isChecked()==True:
                    self.mouse_click_num_list.append(0)
                    

            # SYSTEM INFO
            self.info_textBrowser.append("[SYSYEM INFO]")
            self.info_textBrowser.append("- Version : V0(Auto Mouse)\n")

            # WORK INFO
            self.info_textBrowser.append("[WORK INFO]")

            self.startTime=datetime.now()
            self.info_textBrowser.append("- Start Time : {}".format(self.startTime))
            self.info_textBrowser.append("- Setting : {}".format(self.loop_option))
            
            self.info_textBrowser.append("- Total Work Number: {}".format(len(self.location_list)))
            
            self.info_textBrowser.append("- One Time Work : {}".format(len(self.one_index_list)))

            for idx in self.one_index_list:
                self.info_textBrowser.append("- ({0}) : {1}".format(idx, self.get_mouse_funcType(idx)))
            
            self.info_textBrowser.append("- Loop Work : {}".format(len(self.loop_index_list)))

            for idx in self.loop_index_list:
                self.info_textBrowser.append("- ({0}) : {1}".format(idx, self.get_mouse_funcType(idx)))

            # Timer
            if self.timer_on==True:
                self.info_textBrowser.append("- Timer : ON")
                self.info_textBrowser.append("- Setting Time : {}".format(self.timer_input))
            else:
                self.info_textBrowser.append("- Timer : OFF")
            
        
            # Alarm 
            if self.Alarm_on==True:
                alarm_info="Use"
                mim_tool.call_teleBot(sending_message="Start! "+str(datetime.now()), api_key=self.telegram_API, user_id=self.telegram_UserID)

            else:
                alarm_info="Not Use"
            
            self.info_textBrowser.append("- Alarm : {}".format(alarm_info))

        
           
            # Timer for auto start
            self.atTimer.start()
            

    def update_option(self,is_timer_On,timer_input, alarm_opt):
        # Option1 - Timer
        self.timer_on=is_timer_On
        
        if self.timer_on==True:
            self.timer_input=timer_input
            
            # Create Timer Info From timer input
            user_input=self.timer_input.strip()
            
            time_input_temp=user_input.split()
            
            date_info=time_input_temp[0].split('-')
            time_info=time_input_temp[1].split(':')
            
            self.timer_info["date_YY"]=int("20"+date_info[0]) # 20~ year
            self.timer_info["date_MM"]=int(date_info[1])
            self.timer_info["date_DD"]=int(date_info[2])

            self.timer_info["time_HH"]=int(time_info[0])
            self.timer_info["time_MM"]=int(time_info[1])
            self.timer_info["time_SS"]=int(time_info[2])
        
        # Option2 - Timer
        self.Alarm_on=alarm_opt
        
        

    def update_SysInfo(self,loop_option,loop_num):
        self.loop_option=loop_option
        self.loop_num=loop_num
    
    def update_userInfo(self,location_list,label_list, CheckBox_list1, CheckBox_list2, CheckBox_list3, CheckBox_list4, CheckBox_list5, Text_list):
        self.location_list=location_list
        self.label_list=label_list
        self.CheckBox_list1=CheckBox_list1 
        self.CheckBox_list2=CheckBox_list2
        
        self.CheckBox_list3=CheckBox_list3  # Mouse Function Indicate

        self.CheckBox_list4=CheckBox_list4  # Scroll Up
        self.CheckBox_list5=CheckBox_list5  # Scroll Down

        self.Text_list=Text_list

    def update_telegramInfo(self,tele_API, tele_userID):
        self.telegram_API=tele_API
        self.telegram_UserID=tele_userID

    def clear_TextBrowser(self):
        self.info_textBrowser.clear()

    def dia_run(self):
        pass


    def run_mouse_func(self,idx):
        screen_height =pyauto.size().height

        if self.mouse_click_num_list[idx]!=0: # -> Click Function
            pyauto.click(self.location_list[idx],clicks=self.mouse_click_num_list[idx])
        else:                                 # -> Scroll Function
            if self.CheckBox_list4[idx].isChecked()==True and self.CheckBox_list5[idx].isChecked()==False:                  
                pyauto.scroll(screen_height * mimmim_sys.MOUSE_SCROLL_LENGH_RATIO)
            elif self.CheckBox_list4[idx].isChecked()==False and self.CheckBox_list5[idx].isChecked()==True:  
                pyauto.scroll(-1 * screen_height * mimmim_sys.MOUSE_SCROLL_LENGH_RATIO)


    def auto_function(self):
        
        # One Function
        if self.counted_loop_num==0: 
            if self.one_index_list!=[]:
                for idx in self.one_index_list:
                    self.run_mouse_func(idx)


        # Loop Function 
        if self.loop_index_list!=[]:
            for idx in self.loop_index_list:
                self.run_mouse_func(idx)
       

        self.counted_loop_num=self.counted_loop_num+1
            
        
        # Loop Stop Condition1 : Finite Loop
        if self.loop_option=="Finite Loop":
            if self.counted_loop_num>=self.loop_num:
                self.atTimer.stop()


        # Loop Stop Condition2 : Reservation Success
        if self.Alarm_on==True:
            if self.counted_loop_num % mimmim_sys.CHECKING_LOOP_NUM==0:
                if mim_tool.check_success(check_msg=mimmim_sys.RESERVATION_CHECK_MESSAGE)==True:
                    mim_tool.call_teleBot(sending_message="성공"+str(datetime.now()), api_key=self.telegram_API, user_id=self.telegram_UserID)
                    self.atTimer.stop()
    

        # Loop Stop Condition3 - keyboard input
        if keyboard.is_pressed("esc"):
            self.atTimer.stop()

            self.checkPoint=self.checkPoint+1

            self.info_textBrowser.append("- Check Point #{0} : {1}".format(self.checkPoint,datetime.now()-self.startTime))
            self.mode_label_val.setText("Ready")    
            self.state_label_val.setText("Stop") 

        # Display Effect
        mim_tool.show_prog_state(self.state_label_val,self.counted_loop_num%8,"Running")

        if self.loop_option=="Infinite Loop" and self.counted_loop_num>=1000:
            self.counted_loop_num=0

    def auto_start(self):
        
        if self.timer_on==True:
            if self.timer_start==True:
                self.auto_function()
            else:
                # Time Monitoring
                now=datetime.now()
   
                if(now.year==self.timer_info["date_YY"] and now.month==self.timer_info["date_MM"] and now.day==self.timer_info["date_DD"]):
                    if(now.hour>=self.timer_info["time_HH"] and now.minute>=self.timer_info["time_MM"]):
                        self.timer_start=True
                       
                        self.mode_label_val.setText("Auto Start")
                        self.state_label_val.setText("Auto Run")
                        
                        self.auto_function()


                # Display Effect
                self.timer_label_cnt=self.timer_label_cnt+1

                mim_tool.show_prog_state(self.state_label_val,self.timer_label_cnt%8,"Waiting")
                if self.timer_label_cnt>=1000:
                    self.timer_label_cnt=0
                
        else:
            self.auto_function()
            
    
'''------------------------------------------------------------------------------------------------------

------------------------------------------------------------------------------------------------------'''
        

class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        # 시스템 함수
        self.sys_setting={
            "loop_option":None, # Fininte, Infinite
            "loop_num":None, #Only in Finite
            "alarm":None, # Not Use
        }

        self.Mouse_Point_List=[]
        self.auto_line_num=0

        self.auto_line_label_list=[]

        self.auto_line_CheckBox_list1=[]
        self.auto_line_CheckBox_list2=[]
        self.auto_line_CheckBox_list3=[]

        self.auto_line_CheckBox_list4=[]
        self.auto_line_CheckBox_list5=[]

        self.auto_line_Text_list=[]

        # UI Component
        self.timer=QTimer()
        self.timer.setInterval(50)
        self.timer.timeout.connect(self.set_point)

        # Dialog
        self.make_dialog = CustomDialog()


        self.is_Timer_ON=False

        self.timer_input=QLineEdit(self)
        self.timer_input.setEnabled(False)
  

        # Layout Setting
        self.vbox = QVBoxLayout()


        # [Layout1]: Mouse & Timer Setting
        
        # Mouse Location Button
        self.mouse_label = QLabel('Setting Point', self)
        self.mouse_label.setAlignment(Qt.AlignCenter)

        self.mouse_loc_Btn = QPushButton('Coordinate Input', self)
        self.mouse_loc_Btn.setCheckable(True)
        self.mouse_loc_Btn.clicked.connect(self.set_btn_click)

        self.hbox_mouse= QHBoxLayout()

        self.hbox_mouse.addWidget(self.mouse_label)
        self.hbox_mouse.addWidget(self.mouse_loc_Btn)

        self.vbox.addLayout(self.hbox_mouse)


        # Timer Button
        self.Timer_Btn = QPushButton('Timer', self)
        self.Timer_Btn.setCheckable(True)
        self.Timer_Btn.clicked.connect(self.set_timer)
        self.timer_label = QLabel('Format : YY-MM-DD HH:MM:SS', self)

        self.hbox_timer= QHBoxLayout()

        self.hbox_timer.addWidget(self.Timer_Btn)
        self.hbox_timer.addWidget(self.timer_input)

        self.vbox.addLayout(self.hbox_timer)
        self.vbox.addWidget(self.timer_label)
        
        self.vbox.addStretch(3)



        # Layout2 : Auto Make Button
        self.make_Button = QPushButton('Make')
        self.make_Button.clicked.connect(self.make_auto)

        self.cancelButton = QPushButton('Cancel')
        self.cancelButton.clicked.connect(self.close_mimmim)

        self.hbox = QHBoxLayout()
        self.hbox.addStretch(1)
        self.hbox.addWidget(self.make_Button)
        self.hbox.addWidget(self.cancelButton)

        self.hbox.addStretch(1)
        self.vbox.addLayout(self.hbox)
        self.vbox.addStretch(1)


        # Layout3 : System Setting(Loop/Alarm)
        self.sys_label = QLabel('System Setting', self)
        
        self.sys_combo= QComboBox(self)
        self.sys_combo.addItem("Infinite Loop")
        self.sys_combo.addItem("Finite Loop")
        self.sys_combo.currentIndexChanged.connect(self.change_combo)

        self.sys_input=QLineEdit(self)
        self.sys_input.setEnabled(False)

        self.sys_alarm=QCheckBox("Alarm",self)

        self.hbox_system=QHBoxLayout()
        self.hbox_system.addWidget(self.sys_label)
        self.hbox_system.addWidget(self.sys_combo)
        self.hbox_system.addWidget(self.sys_input)
        self.hbox_system.addWidget(self.sys_alarm)
        
        
        self.vbox.addLayout(self.hbox_system)

        # Layout4 - Telegram
        self.Telegram_API_label=QLabel('Telegram API : ', self)
        self.Telegram_API_input=QLineEdit(self)
        
        self.Telegram_ID_label=QLabel('User ID : ', self)
        self.Telegram_ID_input=QLineEdit(self)
        

        self.hbox_tele_API=QHBoxLayout()
        self.hbox_tele_API.addWidget(self.Telegram_API_label)
        self.hbox_tele_API.addWidget(self.Telegram_API_input)

        self.hbox_tele_ID=QHBoxLayout()
        self.hbox_tele_ID.addWidget(self.Telegram_ID_label)
        self.hbox_tele_ID.addWidget(self.Telegram_ID_input)

        self.vbox.addLayout(self.hbox_tele_API)
        self.vbox.addLayout(self.hbox_tele_ID)

        # Total Layout Setting
        self.setLayout(self.vbox)

        # Window Setting
        self.setWindowTitle('MIMMIM Auto')
        self.setWindowIcon(QIcon('mim_favicon.png'))
        self.move(300, 300)
        self.resize(400, 200)
        self.show()

    def close_mimmim(self):
        self.close()

    def set_timer(self):
        if self.is_Timer_ON==True:
            self.timer_input.setEnabled(False)
            self.timer_label.setEnabled(False)

            self.is_Timer_ON=False
        else:
            self.timer_input.setEnabled(True)
            self.timer_label.setEnabled(True)

            self.is_Timer_ON=True

    def change_combo(self):
        selected_option=self.sys_combo.currentText()
        
        if selected_option=="Infinite Loop":
            self.sys_input.setEnabled(False)
        elif selected_option=="Finite Loop":
            self.sys_input.setEnabled(True)
        else:
            print("combo error!")



    def set_btn_click(self):
        if self.mouse_loc_Btn.isChecked()==True:
            self.timer.start()
            #self.auto_detect_Btn.setEnabled(False)
        else:
            self.timer.stop()
            #self.auto_detect_Btn.setEnabled(True)

    def change_layout(self,mouse_position):

        # Create Component
        self.auto_line_label_list.append(QLabel(str(self.auto_line_num)+". "+str(mouse_position)))
    
        self.auto_line_CheckBox_list1.append(QCheckBox("C1"))  # click one
        self.auto_line_CheckBox_list2.append(QCheckBox("C2"))  # click two
        self.auto_line_CheckBox_list3.append(QCheckBox("One")) # one-time worki
                
        self.auto_line_CheckBox_list4.append(QCheckBox("SC_U")) # Scroll Up
        self.auto_line_CheckBox_list5.append(QCheckBox("SC_D")) # Scroll Down
        

        self.auto_line_Text_list.append(QLineEdit())

        temp_Hbox = QHBoxLayout()

        temp_Hbox.addWidget(self.auto_line_label_list[self.auto_line_num-1])

        # Click Check Box 
        temp_Hbox.addWidget(self.auto_line_CheckBox_list1[self.auto_line_num-1])
        temp_Hbox.addWidget(self.auto_line_CheckBox_list2[self.auto_line_num-1])
        
        # Scroll Check Box
        temp_Hbox.addWidget(self.auto_line_CheckBox_list4[self.auto_line_num-1])
        temp_Hbox.addWidget(self.auto_line_CheckBox_list5[self.auto_line_num-1])
        
        # One Time Check Box
        temp_Hbox.addWidget(self.auto_line_CheckBox_list3[self.auto_line_num-1])
        
        # Text Input
        temp_Hbox.addWidget(self.auto_line_Text_list[self.auto_line_num-1])

        self.vbox.addLayout(temp_Hbox)
        self.setLayout(temp_Hbox)


    def set_point(self):
        mouse_position=pyauto.position()

        self.mouse_label.setText("Current Mouse Position : ({0},{1})".format(str(mouse_position.x),str(mouse_position.y) ))

        if keyboard.is_pressed("enter"):
            
            if (len(self.Mouse_Point_List)==0):
                self.Mouse_Point_List.append(mouse_position)
                self.auto_line_num=self.auto_line_num+1
                print("Enter!  -  "+str(len(self.Mouse_Point_List)))
                
                self.change_layout(mouse_position)

            else:
                if (abs(self.Mouse_Point_List[-1].x-mouse_position.x)>abs(self.Mouse_Point_List[-1].x/mimmim_sys.MOUSE_LOCATION_PRECISION) 
                or abs(self.Mouse_Point_List[-1].y-mouse_position.y)>abs(self.Mouse_Point_List[-1].y/mimmim_sys.MOUSE_LOCATION_PRECISION)):
                    self.Mouse_Point_List.append(mouse_position)
                    self.auto_line_num=self.auto_line_num+1
                    print("Enter!  -  "+str(len(self.Mouse_Point_List)))
                    
                    self.change_layout(mouse_position)



    def make_auto(self):
        # [0] Empty Data Check
        if self.Mouse_Point_List==[]: 
            QMessageBox.critical(self,'MIMMIM ERROR',"Empty Data Error!")
            sys.exit(0)
        
        check_timer=True
        check_click_chkbox=True

        # [1] Mouse Click Selection Check
        for idx in range(self.auto_line_num):
            # Check : (1) Duplicate Choose, (2) Notihing Choose 
            # Case1 : True / True => Duplication Case
            # Case2 : False / False => Nothing Case
            if self.auto_line_CheckBox_list1[idx].isChecked()==True and self.auto_line_CheckBox_list2[idx].isChecked()==True :
                QMessageBox.critical(self,'MIMMIM ERROR','Please choose only one click option! (Line : {})'.format(idx+1))
                check_click_chkbox=False
                break

            if self.auto_line_CheckBox_list4[idx].isChecked()==True and self.auto_line_CheckBox_list5[idx].isChecked()==True:
                QMessageBox.critical(self,'MIMMIM ERROR','Please choose only one scroll option! (Line : {})'.format(idx+1))
                check_click_chkbox=False
                break

            if ((self.auto_line_CheckBox_list1[idx].isChecked()==True or self.auto_line_CheckBox_list2[idx].isChecked()==True) and (self.auto_line_CheckBox_list4[idx].isChecked()==True or self.auto_line_CheckBox_list5[idx].isChecked()==True)):
                QMessageBox.critical(self,'MIMMIM ERROR','Please choose only one option! (Line : {})'.format(idx+1))
                check_click_chkbox=False
                break

            if (self.auto_line_CheckBox_list1[idx].isChecked()==False and self.auto_line_CheckBox_list2[idx].isChecked()==False and self.auto_line_CheckBox_list4[idx].isChecked()==False and self.auto_line_CheckBox_list5[idx].isChecked()==False):
                QMessageBox.critical(self,'MIMMIM ERROR','Please choose only one option! (Line : {})'.format(idx+1))
                check_click_chkbox=False
                break
        # [2] Timer Check
        if self.is_Timer_ON==True:
            # Timer Check
            if "-" in self.timer_input.text() and ":" in self.timer_input.text():
                check_timer=True
            else:
                check_timer=False
                QMessageBox.critical(self,'MIMMIM ERROR','Invalid Timer Format')

        # All Condition Check
        if check_timer==True and check_click_chkbox==True:
            # System Setting
            self.sys_setting["loop_option"]=self.sys_combo.currentText()
            
            if self.sys_setting["loop_option"]=="Finite Loop":
                self.sys_setting["loop_num"]=int(self.sys_input.text())
            else:
                self.sys_setting["loop_num"]=self.sys_input.text()

            self.sys_setting["alarm"]=self.sys_alarm.isChecked()

            # sys update
            self.make_dialog.update_SysInfo(self.sys_setting["loop_option"],self.sys_setting["loop_num"])
            
            # Option Update        
            self.make_dialog.update_option(self.is_Timer_ON,self.timer_input.text(),self.sys_alarm.isChecked())

            # work update
            self.make_dialog.update_userInfo(self.Mouse_Point_List,
                                            self.auto_line_label_list,
                                            self.auto_line_CheckBox_list1,
                                            self.auto_line_CheckBox_list2,
                                            self.auto_line_CheckBox_list3,
                                            self.auto_line_CheckBox_list4,
                                            self.auto_line_CheckBox_list5,
                                            self.auto_line_Text_list)
            
            # Telegram Update
            self.make_dialog.update_telegramInfo(self.Telegram_API_input.text(), self.Telegram_ID_input.text())


            # Timer Stop & Dialog Open
            self.timer.stop()
            self.make_dialog.show()

            

if __name__ == '__main__':
   app = QApplication(sys.argv)
   ex = MyApp()
   sys.exit(app.exec_())