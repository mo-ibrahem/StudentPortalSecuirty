screen_helper = """
ScreenManager:
    id: scr_mng
    LoginPage:
    HomePage:
    OTPScreen:
    studentCredentials:
    showStudentCredentials:

<LoginPage>:
    name: 'login'
    Screen:
        MDCard:
            size_hint: None, None
            size: 600,800
            pos_hint: {"center_x": 0.5, "center_y": 0.5}
            elevation: 10
            padding: 50
            spacing: 50
            orientation: 'vertical'

            MDLabel:
                id: Welcome_label
                text: "Login form"
                font_size: 65
                halign: 'center'
                size_hint_y: None 
                height: self.texture_size[1]
                padding_y: 30


            MDTextField:
                id: username
                hint_text: "Enter username"
                helper_text: "or click on forgot username"
                helper_text_mode: "on_focus"
                icon_right: "account"
                icon_right_color: app.theme_cls.primary_color
                pos_hint:{'center_x': 0.5, 'center_y': 0.5}
                size_hint_x:None
                width:450
            
            MDTextField:
                id: phonenumber
                hint_text: "Number"
                helper_text: "Enter Phone Number"
                helper_text_mode: "on_focus"
                icon_right: "cellphone-text"
                icon_right_color: app.theme_cls.primary_color
                pos_hint:{'center_x': 0.5, 'center_y': 0.5}
                size_hint_x:None
                width:450


            MDRectangleFlatButton:
                text: '     Login     '
                right_pad: True
                font_size: 30
                width: dp(350) 
                pos_hint: {"center_x": 0.5}
                on_release: app.logger()


            MDRectangleFlatButton:
                text: "     Clear     "
                width: dp(350)
                font_size: 30
                size_hint: None, None
                pos_hint: {"center_x": 0.5}
                on_press: app.clear()
            
            

           

<HomePage>:
    name: 'home'
    MDLabel:
        id: homepage_label
        text: ""
        halign: "center"
    MDRectangleFlatButton:
        text: 'Check Credentials'
        pos_hint: {'center_x':0.5,'center_y':0.35}
        on_release: root.manager.current = 'stcredentials'
    MDRectangleFlatButton:
        text: '         Sign out         '
        pos_hint: {'center_x':0.5,'center_y':0.25}
        on_release: root.manager.current = 'login'


<OTPScreen>:
    name: 'otpscreen'
    MDLabel:
        id: otp_label
        text: ""
        font_size: 65
        pos_hint:{'center_x': 0.5, 'center_y': 0.7}

    MDTextField:
        id: otp_user
        hint_text: "Enter otp"
        helper_text: "Check your phone"
        helper_text_mode: "on_focus"
        icon_right: "lock-off-outline"
        icon_right_color: app.theme_cls.primary_color
        pos_hint:{'center_x': 0.5, 'center_y': 0.5}
        size_hint_x:None
        width:450
    MDRectangleFlatButton:
        text: 'Submit'
        pos_hint: {'center_x':0.5,'center_y':0.2}
        on_release: app.verifyOtp()

<studentCredentials>:
    name: 'stcredentials'
    MDLabel:
        text: "Please Enter The Student number to show your credentials"
        font_size: 40
        halign: 'center'
        pos_hint:{'center_x': 0.5, 'center_y': 0.65}
    MDTextField:
        id: id_entered
        hint_text: "Type SNumber"
        helper_text: "Your student number was displayed"
        helper_text_mode: "on_focus"
        icon_right: "lock-off-outline"
        icon_right_color: app.theme_cls.primary_color
        pos_hint:{'center_x': 0.5, 'center_y': 0.45}
        size_hint_x:None
        width:450
    MDRectangleFlatButton:
        text: 'Submit'
        pos_hint: {'center_x':0.5,'center_y':0.25}
        on_release: app.checkCredentials()

<showStudentCredentials>:
    name: 'showCredentials'
    MDLabel:
        id: change
        text: ""
        font_size: 40
        halign: 'center'
        pos_hint:{'center_x': 0.5, 'center_y': 0.65}
    
"""