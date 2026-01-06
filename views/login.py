import os.path
import re
import os

import joblib
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel, QLineEdit, QCheckBox, QPushButton, QMessageBox

from constant.const import APP_NAME, OUTPUT_DIR, HIDDEN_EYE, UNHIDDEN_EYE
from controllers.core import AppController
from views.custom import ClickableLabel
from utilities.utils import BinarySerializer
from views.core import MainApp
from views.style import GENERAL_QLabel_STYLESHEET, GENERAL_QLineEdit_STYLESHEET, SMALLER_QLabel_STYLESHEET, \
    GENERAL_QPushButton_STYLESHEET

import time
import secrets

RESET_TOKEN_FILE = "reset_tokens"   # سيُحفظ كـ reset_tokens.jl
TOKEN_TTL_SECONDS = 15 * 60         # 15 دقيقة

class ForgetPasswordForm(QWidget):
    def __init__(self,parent=None):
        super(ForgetPasswordForm,self).__init__()
        self.__init_ui()
        self._parent=parent
        layout=QGridLayout()



        username_label_forget_password=QLabel("Email")
        username_label_forget_password.setStyleSheet(GENERAL_QLabel_STYLESHEET)
        self.username_lineEdit_forget_password=QLineEdit()
        self.username_lineEdit_forget_password.setPlaceholderText("enter your email...")
        self.username_lineEdit_forget_password.setStyleSheet(GENERAL_QLineEdit_STYLESHEET)
        layout.addWidget(username_label_forget_password,0,0)
        layout.addWidget(self.username_lineEdit_forget_password,0,1,1,4)

        back_button = QPushButton("← Back")
        back_button.setStyleSheet(GENERAL_QPushButton_STYLESHEET)
        back_button.clicked.connect(self.home_page)
        layout.addWidget(back_button,1 ,0)

        confirm_button=QPushButton("confirm")
        confirm_button.setStyleSheet(GENERAL_QPushButton_STYLESHEET)
        confirm_button.clicked.connect(self.send_reset_email)
        layout.addWidget(confirm_button,1, 1, 1, 4 )

        self.setLayout(layout)





    def __init_ui(self):

        self.setWindowTitle(APP_NAME + ' -- Forget Password Form')
        height = 150  # consts.FORGET_PASSWORD_SCREEN_HEIGHT
        width = 400  # consts.FORGET_PASSWORD_WIDTH
        self.resize(width, height)
        self.setMinimumHeight(height)
        self.setMaximumHeight(height)

        self.setMinimumWidth(width)
        self.setMaximumWidth(width)

    # def send_reset_email(self):
    #     email=self.username_lineEdit_forget_password.text().strip().lower()
    #
    #     if not email:
    #         QMessageBox.information(self, "Error", "Please enter an email.")
    #         return
    #
    #     if not self.is_valid_email(email):
    #         QMessageBox.information(self, "Error", "Email format is invalid.")
    #         return
    #
    #     body = (
    #         f"Hello,\n\n"
    #         f"You requested a password reset.\n\n"
    #         f"Use this token to reset your password (valid for 15 minutes):\n"
    #         f"If you did not request this, please ignore this email.\n"
    #     )
    #     AppController.send_email(
    #         subject="Reset Password",
    #         body=body,
    #         receivers=[email],
    #         attachments=None,
    #         inline_attachments=None
    #     )
    #     QMessageBox.information(
    #         self,
    #         "Success",
    #         f"If this account exists, a reset token has been sent to:\n{email}"
    #     )
    def send_reset_email(self):
        email = self.username_lineEdit_forget_password.text().strip().lower()

        if not email:
            QMessageBox.information(self, "Error", "Please enter an email.")
            return

        if not self.is_valid_email(email):
            QMessageBox.information(self, "Error", "Email format is invalid.")
            return

        # 1) توليد توكن قوي
        token = self._generate_token()

        # 2) تخزين التوكن مع وقت الانتهاء
        # self._save_reset_token(email=email, token=token)

        # 3) إرسال الإيميل (يفضل HTML أو نص واضح)
        body = f"""
          <h3>Password Reset</h3>
          <p>Hello,</p>
          <p>You requested a password reset.</p>
          <p><b>Your reset token (valid for 15 minutes):</b></p>
          <h2>{token}</h2>
          <p>If you did not request this, please ignore this email.</p>
          """

        AppController.send_email(
            subject="Reset Password",
            body=body,
            receivers=[email],
            attachments=None,
            inline_attachments=None
        )

        QMessageBox.information(
            self,
            "Success",
            f"If this account exists, a reset token has been sent to:\n{email}"
        )

    def _generate_token(self) -> str:
        # توكن قوي: 6 أرقام أو نص
        # خيار 1: 6 أرقام:
        # return f"{secrets.randbelow(10**6):06d}"

        # خيار 2: نص أقوى
        return secrets.token_urlsafe(6)

    # def _save_reset_token(self, email: str, token: str):
    #     """
    #     تخزين التوكن في ملف joblib كـ dict:
    #     {
    #       "email@example.com": {"token": "...", "expires_at": 1234567890}
    #     }
    #     """
    #     serializer = BinarySerializer()
    #
    #     path = os.path.join(OUTPUT_DIR, RESET_TOKEN_FILE + ".jl")
    #
    #     data = {}
    #     if os.path.exists(path):
    #         try:
    #             data = joblib.load(path)
    #             if not isinstance(data, dict):
    #                 data = {}
    #         except Exception:
    #             data = {}
    #
    #     expires_at = int(time.time()) + TOKEN_TTL_SECONDS
    #     data[email] = {"token": token, "expires_at": expires_at}
    #
    #     serializer.write_jl(data, OUTPUT_DIR, RESET_TOKEN_FILE)

    def is_valid_email(self,email: str) -> bool:
        EMAIL_REGEX = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

        if not email:
            return False
        return re.fullmatch(EMAIL_REGEX, email) is not None
    def home_page(self):
        self._parent.show()
        self.hide()
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



class LoginForm(QWidget):
    def __init__(self):
        super(LoginForm,self).__init__()
        self.__init_ui()
        self.screen=None
        self._serializer=BinarySerializer()

        layout=QGridLayout()

        #username
        user_name_lable=QLabel("Username")
        user_name_lable.setStyleSheet(GENERAL_QLabel_STYLESHEET)
        self.user_name_LineEdit=QLineEdit()
        self.user_name_LineEdit.setPlaceholderText('username')
        self.user_name_LineEdit.setStyleSheet(GENERAL_QLineEdit_STYLESHEET)
        layout.addWidget(user_name_lable,0,0)
        layout.addWidget(self.user_name_LineEdit,0, 1, 1, 3, )


        #password
        password_lable = QLabel("Password")
        password_lable.setStyleSheet(GENERAL_QLabel_STYLESHEET)
        self.password_line_edit = QLineEdit()
        self.password_line_edit.setPlaceholderText('enter a password')
        self.password_line_edit.setStyleSheet(GENERAL_QLineEdit_STYLESHEET)
        layout.addWidget(password_lable, 1, 0)
        layout.addWidget(self.password_line_edit,1, 1,1,3)

        #show password

        self._show_pass_action=QAction(QIcon(HIDDEN_EYE), 'Show Password', self)
        self._show_pass_action.setCheckable(True)
        self.password_line_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_line_edit.addAction(self._show_pass_action,QLineEdit.ActionPosition.TrailingPosition)
        self._show_pass_action.toggled.connect(self.show_Password)



        #remember me
        self.remember_me=QCheckBox("remember me")
        self.remember_me.setStyleSheet(SMALLER_QLabel_STYLESHEET)
        # self.remember_me.clicked.connect(self.check_email)
        layout.addWidget(self.remember_me,2,0)


        #forget password
        forget_password=ClickableLabel(self.forget_form,"forget password?",)
        forget_password.setStyleSheet(GENERAL_QLabel_STYLESHEET)
        layout.addWidget(forget_password,2,3)

        #login putton
        login_button=QPushButton("login")
        login_button.setStyleSheet(GENERAL_QPushButton_STYLESHEET)
        login_button.clicked.connect(self.check_email)
        layout.addWidget(login_button,3, 0, 1, 4, )




        self.setLayout(layout)
        self._attempt_remember_me_fill()
    def forget_form(self,event):
        AppController.LOGGER.info('forget password clicked')
        self.screen=ForgetPasswordForm(parent=self)
        self.screen.show()
        self.hide()

    def __init_ui(self):
        self.setWindowTitle(APP_NAME + ' -- Login')
        height = 200  # consts.LOGIN_SCREEN_HEIGHT
        width = 400  # consts.LOGIN_SCREEN_WIDTH
        self.resize(width, height)
        self.setMinimumHeight(height)
        self.setMaximumHeight(height)

        self.setMinimumWidth(width)
        self.setMaximumWidth(width)

    def show_Password(self, checked: bool):
        if checked:
            self.password_line_edit.setEchoMode(QLineEdit.EchoMode.Normal)
            self._show_pass_action.setIcon(QIcon(UNHIDDEN_EYE))
        else:
            self.password_line_edit.setEchoMode(QLineEdit.EchoMode.Password)
            self._show_pass_action.setIcon(QIcon(HIDDEN_EYE))

    def check_email(self):
        email=self.user_name_LineEdit.text().lower()
        password=self.password_line_edit.text()
        msg=QMessageBox()

        if not email:
            msg.setText('Please enter an email')
            msg.exec()
            return
        if not password:
            msg.setText('Please enter an password')
            msg.exec()
            return
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if not re.fullmatch(regex,email):
            msg.setText('invalid email formate')
            msg.exec()
            return

        user=self.__load_user_data(email,password)
        if user is None:
            msg.setText('User is not registered in the system.')
            msg.exec()
            return
        if self.remember_me.isChecked():
            AppController.LOGGER.info('remember me is checked')
            self._serializer.write_jl(
                obj={
                    'email': email,
                    'password': password,
                },
                path=OUTPUT_DIR,
                name='remember_me',
            )
        self.next_screen(user)

    def next_screen(self,user):
        self.screen=MainApp(user=user,parent=self)
        self.screen.show()
        self.destroy()
        self.close()

    def _attempt_remember_me_fill(self):
        path=os.path.join(OUTPUT_DIR,'remember_me.jl')
        data=None
        if os.path.exists(path):
            try:
                data=joblib.load(path)
                if not isinstance(data,dict):
                    print("بيانات remember_me ليست من نوع dict")
                    data = None
                elif 'email' not in data :
                    print("بيانات remember_me تفتقد email أو password")
                    data = None
            except Exception as e:
                print("فشل تحميل بيانات remember_me:", e)
                data = None
        if data is not None:
            self.user_name_LineEdit.setText(data['email'])
            # self.password_line_edit.setText(data['password'])
        else:
            print("لا توجد بيانات remember_me صالحة")


    def __load_user_data(self,email,password):
        from models.models import User
        user=AppController.factory.session.query(User).filter(
            User.email==email,
            User.removed_at.is_(None),
        ).first()
        if user is None:
            return None

        if user.password != password:
            return None

        return user

    #
    # def next_screen(self, user):
    #     self.screen = MainApp(
    #         user=user,
    #     )
    #     self.screen.show()
    #
    #     self.hide()
    #     self.destroy()
    #     self.close()
    #     pass
    #

# from PyQt6.QtWidgets import (
#     QWidget, QLabel, QLineEdit, QCheckBox, QPushButton,
#     QHBoxLayout, QVBoxLayout, QFrame, QSizePolicy
# )
# from PyQt6.QtCore import Qt
# from PyQt6.QtGui import QFont
#
# from constant.const import APP_NAME
# from custom import ClickableLabel
#
#
# class LoginForm(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.screen = None
#         self.__init_ui()
#         self._build_ui()
#
#     def __init_ui(self):
#         self.setWindowTitle(APP_NAME + " - تسجيل الدخول")
#         self.setFixedSize(980, 520)   # ✅ نفس ستايل الصورة (أفقي واسع)
#         self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)  # ✅ RTL
#
#         self.setStyleSheet("""
#             QWidget { background: #f6f6f6; font-family: Arial; }
#             QLabel#title { font-size: 20px; font-weight: 700; color: #333; }
#             QLabel#label { font-size: 12px; color: #555; }
#             QLabel#hint { font-size: 11px; color: #f28c28; }
#             QLineEdit {
#                 background: #ffffff;
#                 border: 1px solid #dcdcdc;
#                 border-radius: 18px;
#                 padding: 10px 14px;
#                 font-size: 12px;
#             }
#             QLineEdit:focus { border: 1px solid #f28c28; }
#
#             QPushButton#primaryBtn {
#                 background: #f28c28;
#                 color: white;
#                 border: none;
#                 border-radius: 18px;
#                 padding: 10px 18px;
#                 font-size: 12px;
#                 font-weight: 700;
#             }
#             QPushButton#primaryBtn:hover { background: #e57f1d; }
#
#             QPushButton#secondaryBtn {
#                 background: transparent;
#                 color: #f28c28;
#                 border: 1px solid #f28c28;
#                 border-radius: 18px;
#                 padding: 10px 18px;
#                 font-size: 12px;
#                 font-weight: 700;
#             }
#             QPushButton#secondaryBtn:hover { background: rgba(242,140,40,0.08); }
#
#             QCheckBox { font-size: 11px; color: #666; }
#         """)
#
#     def _build_ui(self):
#         # ===== Root split layout =====
#         root = QHBoxLayout(self)
#         root.setContentsMargins(18, 18, 18, 18)
#         root.setSpacing(0)
#
#         # ===== Left orange panel =====
#         left_panel = QFrame()
#         left_panel.setObjectName("leftPanel")
#         left_panel.setFixedWidth(560)
#
#         left_panel.setStyleSheet("""
#             QFrame#leftPanel {
#                 background: #f28c28;
#                 border-top-right-radius: 24px;
#                 border-bottom-right-radius: 24px;
#             }
#             QLabel#brand { color: white; font-size: 34px; font-weight: 800; }
#             QLabel#brandSub { color: white; font-size: 16px; font-weight: 600; }
#             QLabel#brandDesc { color: rgba(255,255,255,0.9); font-size: 13px; }
#         """)
#
#         left_layout = QVBoxLayout(left_panel)
#         left_layout.setContentsMargins(40, 40, 40, 40)
#         left_layout.setSpacing(10)
#         left_layout.addStretch(1)
#
#         brand = QLabel("مواسم\nmwasm")
#         brand.setObjectName("brand")
#         brand.setAlignment(Qt.AlignmentFlag.AlignHCenter)
#
#         brand_sub = QLabel("مرحبًا بكم في منصة مواسم المختصة في بيع\nأروع المنتجات المنزلية")
#         brand_sub.setObjectName("brandSub")
#         brand_sub.setAlignment(Qt.AlignmentFlag.AlignHCenter)
#
#         brand_desc = QLabel("")  # إذا بدك سطر إضافي
#         brand_desc.setObjectName("brandDesc")
#         brand_desc.setAlignment(Qt.AlignmentFlag.AlignHCenter)
#
#         left_layout.addWidget(brand)
#         left_layout.addSpacing(8)
#         left_layout.addWidget(brand_sub)
#         left_layout.addWidget(brand_desc)
#         left_layout.addStretch(2)
#
#         # ===== Right white card =====
#         right_card = QFrame()
#         right_card.setObjectName("rightCard")
#         right_card.setStyleSheet("""
#             QFrame#rightCard {
#                 background: white;
#                 border-top-left-radius: 24px;
#                 border-bottom-left-radius: 24px;
#             }
#         """)
#
#         right_layout = QVBoxLayout(right_card)
#         right_layout.setContentsMargins(44, 44, 44, 44)
#         right_layout.setSpacing(14)
#
#         title = QLabel("تسجيل الدخول")
#         title.setObjectName("title")
#         title.setAlignment(Qt.AlignmentFlag.AlignRight)
#
#         # Email
#         email_lbl = QLabel("الإيميل")
#         email_lbl.setObjectName("label")
#         self.email_edit = QLineEdit()
#         self.email_edit.setPlaceholderText("بريدك الإلكتروني")
#
#         # Password
#         pass_lbl = QLabel("كلمة المرور")
#         pass_lbl.setObjectName("label")
#         self.pass_edit = QLineEdit()
#         self.pass_edit.setPlaceholderText("هنا كلمة المرور")
#         self.pass_edit.setEchoMode(QLineEdit.EchoMode.Password)
#
#         # forgot
#         forgot = ClickableLabel(self.forget_form, "نسيت كلمة المرور")
#         forgot.setObjectName("hint")
#         forgot.setAlignment(Qt.AlignmentFlag.AlignRight)
#         forgot.setStyleSheet("color:#f28c28;")  # فوق الـ stylesheet العام
#
#         # buttons row
#         btn_row = QHBoxLayout()
#         btn_row.setSpacing(12)
#
#         signup_btn = QPushButton("التسجيل")
#         signup_btn.setObjectName("secondaryBtn")
#
#         login_btn = QPushButton("تسجيل الدخول")
#         login_btn.setObjectName("primaryBtn")
#
#         btn_row.addWidget(login_btn)
#         btn_row.addWidget(signup_btn)
#
#         # social row (اختياري)
#         social_lbl = QLabel("أو باستخدام")
#         social_lbl.setAlignment(Qt.AlignmentFlag.AlignHCenter)
#         social_lbl.setStyleSheet("color:#777; font-size:11px;")
#
#         socials = QHBoxLayout()
#         socials.setSpacing(18)
#         socials.setAlignment(Qt.AlignmentFlag.AlignHCenter)
#
#         g = QLabel("G")
#         t = QLabel("T")
#         f = QLabel("f")
#         for x in (g, t, f):
#             x.setFixedSize(34, 34)
#             x.setAlignment(Qt.AlignmentFlag.AlignCenter)
#             x.setStyleSheet("""
#                 background:#f3f3f3;
#                 border-radius:17px;
#                 color:#555;
#                 font-weight:700;
#             """)
#             socials.addWidget(x)
#
#         right_layout.addWidget(title)
#         right_layout.addSpacing(10)
#
#         right_layout.addWidget(email_lbl)
#         right_layout.addWidget(self.email_edit)
#
#         right_layout.addWidget(pass_lbl)
#         right_layout.addWidget(self.pass_edit)
#
#         right_layout.addWidget(forgot)
#
#         right_layout.addSpacing(6)
#         right_layout.addLayout(btn_row)
#
#         right_layout.addStretch(1)
#         right_layout.addWidget(social_lbl)
#         right_layout.addLayout(socials)
#
#         # ===== Add panels to root =====
#         root.addWidget(right_card)
#         root.addWidget(left_panel)
#
#         # stretch so card keeps nice size
#         right_card.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
#
#     def forget_form(self, event):
#         from your_module import ForgetPasswordForm  # عدّل الاستيراد حسب مشروعك
#         self.screen = ForgetPasswordForm(parent=self)
#         self.screen.show()
#         self.hide()


# from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel, QLineEdit, QCheckBox, QPushButton, QHBoxLayout, QVBoxLayout, \
#     QSpacerItem, QSizePolicy
# from PyQt6.QtCore import Qt, pyqtSignal
# from PyQt6.QtGui import QFont, QPixmap, QIcon, QColor, QPalette, QPainter, QLinearGradient, QBrush
#
# from constant.const import APP_NAME
# from custom import ClickableLabel
#
#
# class ForgetPasswordForm(QWidget):
#     def __init__(self, parent=None):
#         super(ForgetPasswordForm, self).__init__()
#         self._parent = parent
#         self.setFixedSize(380, 400)
#
#         # تعيين خلفية بيضاء
#         self.setStyleSheet("background-color: white;")
#
#         layout = QVBoxLayout()
#         layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
#         layout.setSpacing(20)
#         layout.setContentsMargins(40, 40, 40, 40)
#
#         # زر العودة (أصغر حجمًا وأقل بروزًا)
#         back_button = QPushButton("←")
#         back_button.clicked.connect(self.go_back)
#         back_button.setFixedSize(30, 30)
#         back_button.setStyleSheet("""
#             QPushButton {
#                 background-color: transparent;
#                 color: #777;
#                 border: none;
#                 font-size: 16px;
#                 padding: 0;
#             }
#             QPushButton:hover {
#                 color: #4CAF50;
#             }
#         """)
#         layout.addWidget(back_button, alignment=Qt.AlignmentFlag.AlignLeft)
#
#         # عنوان الصفحة
#         title = QLabel("استعادة كلمة المرور")
#         title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
#         title.setStyleSheet("color: #333;")
#         layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignCenter)
#
#         # البريد الإلكتروني
#         email_label = QLabel("البريد الإلكتروني")
#         email_label.setStyleSheet("color: #555; font-weight: bold;")
#         self.email_input = QLineEdit()
#         self.email_input.setPlaceholderText("أدخل بريدك الإلكتروني...")
#         self.email_input.setFixedHeight(40)
#         self.email_input.setStyleSheet("""
#             QLineEdit {
#                 padding: 10px;
#                 border: 1px solid #ddd;
#                 border-radius: 20px;
#                 font-size: 14px;
#                 background-color: #f9f9f9;
#             }
#             QLineEdit:focus {
#                 border: 1px solid #4CAF50;
#                 background-color: white;
#             }
#         """)
#         layout.addWidget(email_label)
#         layout.addWidget(self.email_input)
#
#         # زر التأكيد (بنفس تصميم زر تسجيل الدخول في الصفحة الرئيسية)
#         confirm_button = QPushButton("تأكيد")
#         confirm_button.setFixedHeight(45)
#         confirm_button.setStyleSheet("""
#             QPushButton {
#                 background-color: #FF9800;
#                 color: white;
#                 font-weight: bold;
#                 border-radius: 22px;
#                 font-size: 14px;
#             }
#             QPushButton:hover {
#                 background-color: #F57C00;
#             }
#         """)
#         layout.addWidget(confirm_button)
#
#         self.setLayout(layout)
#
#     def go_back(self):
#         if self._parent:
#             self._parent.show()
#         self.close()
#
#
# class LoginForm(QWidget):
#     def __init__(self):
#         super(LoginForm, self).__init__()
#         self.__init_ui()
#         self.screen = None
#
#         # التخطيط الرئيسي (أفقى لتقسيم الشاشة)
#         main_layout = QHBoxLayout()
#         main_layout.setContentsMargins(0, 0, 0, 0)
#         main_layout.setSpacing(0)
#
#         # القسم الأيسر (الصورة/الشعار والترحيب)
#         left_widget = QWidget()
#         left_widget.setStyleSheet("background-color: #F57F17;")  # برتقالي فاتح
#
#         left_layout = QVBoxLayout()
#         left_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
#         left_layout.setSpacing(20)
#         left_layout.setContentsMargins(60, 60, 60, 60)
#
#         # شعار/اسم التطبيق (بديل للصورة)
#         logo_label = QLabel("مِدراك")
#         logo_label.setFont(QFont("Arial", 24, QFont.Weight.Bold))
#         logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
#         logo_label.setStyleSheet("color: white; margin-bottom: 20px;")
#         left_layout.addWidget(logo_label)
#
#         # رسالة الترحيب
#         welcome_label = QLabel("لأن المعرفة تبدأ بكتاب")
#         welcome_label.setFont(QFont("Arial", 14))
#         welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
#         welcome_label.setStyleSheet("color: white; line-height: 1.5;")
#         left_layout.addWidget(welcome_label)
#
#         # صورة (يمكن استبدالها بـ QLabel يحتوي على صورة أو رسم توضيحي)
#         # هنا سنستخدم مساحة فارغة كمثال، يمكنك استبدالها بصورتك الفعلية
#         placeholder_image = QLabel()
#         placeholder_image.setFixedSize(300, 200)
#         placeholder_image.setStyleSheet("background-color: rgba(255, 255, 255, 0.1); border-radius: 10px;")
#         placeholder_image.setAlignment(Qt.AlignmentFlag.AlignCenter)
#         placeholder_image.setText("صورة المنتجات المنزلية")
#         placeholder_image.setStyleSheet("color: white; font-size: 12px;")
#         left_layout.addWidget(placeholder_image)
#
#         left_widget.setLayout(left_layout)
#         main_layout.addWidget(left_widget)
#
#         # القسم الأيمن (نموذج تسجيل الدخول)
#         right_widget = QWidget()
#         right_widget.setStyleSheet("background-color: white;")
#
#         right_layout = QVBoxLayout()
#         right_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
#         right_layout.setSpacing(20)
#         right_layout.setContentsMargins(60, 60, 60, 60)
#
#         # عنوان تسجيل الدخول
#         login_title = QLabel("تسجيل الدخول")
#         login_title.setFont(QFont("Arial", 18, QFont.Weight.Bold))
#         login_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
#         login_title.setStyleSheet("color: #333;")
#         right_layout.addWidget(login_title)
#
#         # تخطيط حقول الإدخال
#         form_layout = QGridLayout()
#         form_layout.setSpacing(15)
#         form_layout.setColumnStretch(0, 1)
#         form_layout.setColumnStretch(1, 2)
#
#         # البريد الإلكتروني
#         email_label = QLabel("الايميل")
#         email_label.setStyleSheet("color: #555; font-weight: bold;")
#         self.email_LineEdit = QLineEdit()
#         self.email_LineEdit.setPlaceholderText("بريدك الإلكتروني")
#         self.email_LineEdit.setFixedHeight(40)
#         self.email_LineEdit.setStyleSheet("""
#             QLineEdit {
#                 padding: 10px;
#                 border: 1px solid #ddd;
#                 border-radius: 20px;
#                 font-size: 14px;
#                 background-color: #f9f9f9;
#             }
#             QLineEdit:focus {
#                 border: 1px solid #4CAF50;
#                 background-color: white;
#             }
#         """)
#         form_layout.addWidget(email_label, 0, 0)
#         form_layout.addWidget(self.email_LineEdit, 0, 1)
#
#         # كلمة المرور
#         password_label = QLabel("كلمة المرور")
#         password_label.setStyleSheet("color: #555; font-weight: bold;")
#         self.password_LineEdit = QLineEdit()
#         self.password_LineEdit.setPlaceholderText("هنا كلمة المرور")
#         self.password_LineEdit.setEchoMode(QLineEdit.EchoMode.Password)
#         self.password_LineEdit.setFixedHeight(40)
#         self.password_LineEdit.setStyleSheet("""
#             QLineEdit {
#                 padding: 10px;
#                 border: 1px solid #ddd;
#                 border-radius: 20px;
#                 font-size: 14px;
#                 background-color: #f9f9f9;
#             }
#             QLineEdit:focus {
#                 border: 1px solid #4CAF50;
#                 background-color: white;
#             }
#         """)
#         form_layout.addWidget(password_label, 1, 0)
#         form_layout.addWidget(self.password_LineEdit, 1, 1)
#
#         right_layout.addLayout(form_layout)
#
#         # رابط نسيت كلمة المرور؟
#         forget_password = ClickableLabel(self.forget_form, "نسيت كلمة المرور؟")
#         forget_password.setStyleSheet("color: #FF9800; text-decoration: underline; font-size: 12px;")
#         forget_password.setAlignment(Qt.AlignmentFlag.AlignRight)
#         right_layout.addWidget(forget_password)
#
#         # زر تسجيل الدخول وزر التسجيل
#         buttons_layout = QHBoxLayout()
#         buttons_layout.setSpacing(10)
#
#         register_button = QPushButton("التسجيل")
#         register_button.setFixedHeight(45)
#         register_button.setStyleSheet("""
#             QPushButton {
#                 background-color: transparent;
#                 color: #FF9800;
#                 border: 2px solid #FF9800;
#                 font-weight: bold;
#                 border-radius: 22px;
#                 font-size: 14px;
#             }
#             QPushButton:hover {
#                 background-color: #FFF3E0;
#             }
#         """)
#         buttons_layout.addWidget(register_button)
#
#         login_button = QPushButton("تسجيل الدخول")
#         login_button.setFixedHeight(45)
#         login_button.setStyleSheet("""
#             QPushButton {
#                 background-color: #FF9800;
#                 color: white;
#                 font-weight: bold;
#                 border-radius: 22px;
#                 font-size: 14px;
#             }
#             QPushButton:hover {
#                 background-color: #F57C00;
#             }
#         """)
#         buttons_layout.addWidget(login_button)
#
#         right_layout.addLayout(buttons_layout)
#
#         # فاصل
#         separator = QLabel("أو باستخدام")
#         separator.setAlignment(Qt.AlignmentFlag.AlignCenter)
#         separator.setStyleSheet("color: gray; font-size: 12px; margin-top: 20px;")
#         right_layout.addWidget(separator)
#
#         # أيقونات وسائل التواصل الاجتماعي
#         social_layout = QHBoxLayout()
#         social_layout.setSpacing(15)
#
#         # يمكن استبدال هذه الأيقونات بالصور الفعلية
#         google_btn = QPushButton()
#         google_btn.setFixedSize(40, 40)
#         google_btn.setStyleSheet("""
#             QPushButton {
#                 background-color: white;
#                 border: 1px solid #ddd;
#                 border-radius: 20px;
#             }
#             QPushButton:hover {
#                 background-color: #f0f0f0;
#             }
#         """)
#         google_btn.setIcon(QIcon("path/to/google_icon.png"))  # استبدل بالمسار الفعلي للصورة
#         social_layout.addWidget(google_btn)
#
#         twitter_btn = QPushButton()
#         twitter_btn.setFixedSize(40, 40)
#         twitter_btn.setStyleSheet("""
#             QPushButton {
#                 background-color: white;
#                 border: 1px solid #ddd;
#                 border-radius: 20px;
#             }
#             QPushButton:hover {
#                 background-color: #f0f0f0;
#             }
#         """)
#         twitter_btn.setIcon(QIcon("path/to/twitter_icon.png"))  # استبدل بالمسار الفعلي للصورة
#         social_layout.addWidget(twitter_btn)
#
#         facebook_btn = QPushButton()
#         facebook_btn.setFixedSize(40, 40)
#         facebook_btn.setStyleSheet("""
#             QPushButton {
#                 background-color: white;
#                 border: 1px solid #ddd;
#                 border-radius: 20px;
#             }
#             QPushButton:hover {
#                 background-color: #f0f0f0;
#             }
#         """)
#         facebook_btn.setIcon(QIcon("path/to/facebook_icon.png"))  # استبدل بالمسار الفعلي للصورة
#         social_layout.addWidget(facebook_btn)
#
#         right_layout.addLayout(social_layout)
#
#         right_widget.setLayout(right_layout)
#         main_layout.addWidget(right_widget)
#
#         self.setLayout(main_layout)
#
#     def forget_form(self, event):
#         self.screen = ForgetPasswordForm(parent=self)
#         self.screen.show()
#         self.hide()
#
#     def __init_ui(self):
#         self.setWindowTitle(APP_NAME + '__تسجيل الدخول')
#         # حجم الشاشة
#         width = 900
#         height = 550
#         self.resize(width, height)
#         self.setMinimumSize(width, height)
#         self.setMaximumSize(width, height)
#         # لا حاجة لـ setStyleSheet هنا لأننا نستخدم StyleSheet لكل Widget منفصل


# from PyQt6.QtWidgets import (
#     QWidget, QGridLayout, QLabel, QLineEdit, QPushButton,
#     QHBoxLayout, QVBoxLayout, QSpacerItem, QSizePolicy
# )
# from PyQt6.QtCore import Qt, pyqtSignal
# from PyQt6.QtGui import QFont, QIcon, QPixmap, QPainter, QColor, QLinearGradient, QBrush
#
# from constant.const import APP_NAME
# from custom import ClickableLabel
#
#
# class ForgetPasswordForm(QWidget):
#     def __init__(self, parent=None):
#         super(ForgetPasswordForm, self).__init__()
#         self._parent = parent
#         self.setFixedSize(380, 400)
#         self.setStyleSheet("background-color: #F57F17;")  # خلفية برتقالية موحدة
#
#         layout = QVBoxLayout()
#         layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
#         layout.setSpacing(20)
#         layout.setContentsMargins(40, 40, 40, 40)
#
#         # زر العودة (أصغر)
#         back_button = QPushButton("←")
#         back_button.clicked.connect(self.go_back)
#         back_button.setFixedSize(30, 30)
#         back_button.setStyleSheet("""
#             QPushButton {
#                 background-color: transparent;
#                 color: white;
#                 border: none;
#                 font-size: 16px;
#                 padding: 0;
#             }
#             QPushButton:hover {
#                 color: #FFD54F;
#             }
#         """)
#         layout.addWidget(back_button, alignment=Qt.AlignmentFlag.AlignLeft)
#
#         # العنوان
#         title = QLabel("استعادة كلمة المرور")
#         title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
#         title.setStyleSheet("color: white;")
#         layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignCenter)
#
#         # البريد الإلكتروني
#         email_label = QLabel("البريد الإلكتروني")
#         email_label.setStyleSheet("color: white; font-weight: bold;")
#         self.email_input = QLineEdit()
#         self.email_input.setPlaceholderText("أدخل بريدك الإلكتروني...")
#         self.email_input.setFixedHeight(40)
#         self.email_input.setStyleSheet("""
#             QLineEdit {
#                 padding: 10px;
#                 border: 1px solid #ddd;
#                 border-radius: 20px;
#                 font-size: 14px;
#                 background-color: white;
#                 color: #333;
#             }
#             QLineEdit:focus {
#                 border: 1px solid #FF9800;
#                 background-color: #fff;
#             }
#         """)
#         layout.addWidget(email_label)
#         layout.addWidget(self.email_input)
#
#         # زر التأكيد
#         confirm_button = QPushButton("تأكيد")
#         confirm_button.setFixedHeight(45)
#         confirm_button.setStyleSheet("""
#             QPushButton {
#                 background-color: #FF9800;
#                 color: white;
#                 font-weight: bold;
#                 border-radius: 22px;
#                 font-size: 14px;
#             }
#             QPushButton:hover {
#                 background-color: #F57C00;
#             }
#         """)
#         layout.addWidget(confirm_button)
#
#         self.setLayout(layout)
#
#     def go_back(self):
#         if self._parent:
#             self._parent.show()
#         self.close()
#
#
# class LoginForm(QWidget):
#     def __init__(self):
#         super(LoginForm, self).__init__()
#         self.__init_ui()
#         self.screen = None
#
#         # التخطيط الرئيسي: قسمين أفقيين
#         main_layout = QHBoxLayout()
#         main_layout.setContentsMargins(0, 0, 0, 0)
#         main_layout.setSpacing(0)
#
#         # =====================
#         # القسم الأيسر (الخلفية البرتقالية + رف الكتب)
#         # =====================
#         left_widget = QWidget()
#         left_widget.setStyleSheet("background-color: #F57F17;")
#
#         left_layout = QVBoxLayout()
#         left_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
#         left_layout.setSpacing(20)
#         left_layout.setContentsMargins(60, 60, 60, 60)
#
#         # شعار/اسم التطبيق
#         logo_label = QLabel("مدراك")
#         logo_label.setFont(QFont("Arial", 28, QFont.Weight.Bold))
#         logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
#         logo_label.setStyleSheet("color: white; margin-bottom: 10px;")
#         left_layout.addWidget(logo_label)
#
#         # شعار صغير فوق الاسم (يمكن استبداله بصورة فعليّة)
#         logo_icon = QLabel()
#         logo_icon.setFixedSize(50, 50)
#         logo_icon.setStyleSheet("background-color: transparent; color: white; font-size: 30px;")
#         logo_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
#         logo_icon.setText("📚")  # رمز مؤقت — يمكنك استبداله بصورة
#         left_layout.addWidget(logo_icon)
#
#         # النص الترحيبي
#         welcome_label = QLabel("لأن المعرفة بدأً بكُنب")
#         welcome_label.setFont(QFont("Arial", 16))
#         welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
#         welcome_label.setStyleSheet("color: white; margin-top: 10px;")
#         left_layout.addWidget(welcome_label)
#
#         # رف الكتب (رسم توضيحي)
#         bookshelf = QLabel()
#         bookshelf.setFixedSize(250, 400)
#         bookshelf.setStyleSheet("""
#             background-color: #E6C79C;
#             border-radius: 10px;
#             padding: 10px;
#         """)
#
#         # رسم الكتب داخل الرف
#         pixmap = QPixmap(250, 400)
#         pixmap.fill(QColor("#E6C79C"))
#         painter = QPainter(pixmap)
#         painter.setFont(QFont("Arial", 8))
#
#         # رسم 3 أرفف
#         shelf_y_positions = [50, 170, 290]
#         for y in shelf_y_positions:
#             # رسم خط الرف
#             painter.setPen(QColor("#B38B6D"))
#             painter.drawLine(10, y, 240, y)
#             # رسم الكتب
#             x = 20
#             colors = ["#FF5722", "#FF9800", "#FFEB3B", "#8BC34A", "#2196F3", "#9C27B0", "#607D8B"]
#             for i in range(10):
#                 book_width = 15 + (i % 3) * 2
#                 book_height = 80 - (i % 4) * 5
#                 book_color = colors[i % len(colors)]
#                 painter.fillRect(x, y - book_height, book_width, book_height, QColor(book_color))
#                 painter.setPen(QColor("white"))
#                 painter.drawText(x, y - book_height + 10, book_width, 20, Qt.AlignmentFlag.AlignCenter, str(i+1))
#                 x += book_width + 3
#
#         painter.end()
#         bookshelf.setPixmap(pixmap)
#         left_layout.addWidget(bookshelf, alignment=Qt.AlignmentFlag.AlignCenter)
#
#         # نص أسفل الرف
#         footer_label = QLabel("صورة المنتجات المنزلية")
#         footer_label.setFont(QFont("Arial", 10))
#         footer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
#         footer_label.setStyleSheet("color: white; margin-top: 20px;")
#         left_layout.addWidget(footer_label)
#
#         left_widget.setLayout(left_layout)
#         main_layout.addWidget(left_widget)
#
#         # =====================
#         # القسم الأيمن (نموذج تسجيل الدخول)
#         # =====================
#         right_widget = QWidget()
#         right_widget.setStyleSheet("background-color: #F57F17;")
#
#         right_main_layout = QVBoxLayout()
#         right_main_layout.setContentsMargins(0, 0, 0, 0)
#         right_main_layout.setSpacing(0)
#
#         # --- أزرار التحكم (إغلاق وتصغير) ---
#         close_btn = QPushButton("×")
#         close_btn.setFixedSize(30, 30)
#         close_btn.setStyleSheet("""
#             QPushButton {
#                 background-color: #FF5722;
#                 color: white;
#                 border: none;
#                 font-size: 16px;
#                 font-weight: bold;
#                 border-radius: 15px;
#             }
#             QPushButton:hover {
#                 background-color: #E64A19;
#             }
#         """)
#         close_btn.clicked.connect(self.close)
#
#         minimize_btn = QPushButton("–")
#         minimize_btn.setFixedSize(30, 30)
#         minimize_btn.setStyleSheet("""
#             QPushButton {
#                 background-color: #9E9E9E;
#                 color: white;
#                 border: none;
#                 font-size: 16px;
#                 font-weight: bold;
#                 border-radius: 15px;
#             }
#             QPushButton:hover {
#                 background-color: #757575;
#             }
#         """)
#         minimize_btn.clicked.connect(self.showMinimized)
#
#         controls_layout = QHBoxLayout()
#         controls_layout.addStretch()
#         controls_layout.addWidget(minimize_btn)
#         controls_layout.addWidget(close_btn)
#         controls_layout.setSpacing(5)
#         controls_layout.setContentsMargins(10, 10, 10, 10)
#
#         right_main_layout.addLayout(controls_layout)
#
#         # --- محتوى النموذج ---
#         content_layout = QVBoxLayout()
#         content_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
#         content_layout.setSpacing(20)
#         content_layout.setContentsMargins(60, 20, 60, 60)
#
#         login_title = QLabel("تسجيل الدخول")
#         login_title.setFont(QFont("Arial", 20, QFont.Weight.Bold))
#         login_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
#         login_title.setStyleSheet("color: white;")
#         content_layout.addWidget(login_title)
#
#         # نموذج الإدخال
#         form_layout = QGridLayout()
#         form_layout.setSpacing(15)
#         form_layout.setColumnStretch(0, 1)
#         form_layout.setColumnStretch(1, 2)
#
#         email_label = QLabel("البريد")
#         email_label.setStyleSheet("color: white; font-weight: bold;")
#         self.email_LineEdit = QLineEdit()
#         self.email_LineEdit.setPlaceholderText("بريدك الإلكتروني")
#         self.email_LineEdit.setFixedHeight(40)
#         self.email_LineEdit.setStyleSheet("""
#             QLineEdit {
#                 padding: 10px;
#                 border: 1px solid #ddd;
#                 border-radius: 20px;
#                 font-size: 14px;
#                 background-color: white;
#                 color: #333;
#             }
#             QLineEdit:focus {
#                 border: 1px solid #FF9800;
#                 background-color: #fff;
#             }
#         """)
#         form_layout.addWidget(email_label, 0, 0)
#         form_layout.addWidget(self.email_LineEdit, 0, 1)
#
#         password_label = QLabel("كلمة المرور")
#         password_label.setStyleSheet("color: white; font-weight: bold;")
#         self.password_LineEdit = QLineEdit()
#         self.password_LineEdit.setPlaceholderText("هنا كلمة المرور")
#         self.password_LineEdit.setEchoMode(QLineEdit.EchoMode.Password)
#         self.password_LineEdit.setFixedHeight(40)
#         self.password_LineEdit.setStyleSheet("""
#             QLineEdit {
#                 padding: 10px;
#                 border: 1px solid #ddd;
#                 border-radius: 20px;
#                 font-size: 14px;
#                 background-color: white;
#                 color: #333;
#             }
#             QLineEdit:focus {
#                 border: 1px solid #FF9800;
#                 background-color: #fff;
#             }
#         """)
#         form_layout.addWidget(password_label, 1, 0)
#         form_layout.addWidget(self.password_LineEdit, 1, 1)
#
#         content_layout.addLayout(form_layout)
#
#         # رابط نسيت كلمة المرور
#         forget_password = ClickableLabel(self.forget_form, "نسيت كلمة المرور؟")
#         forget_password.setStyleSheet("color: #FFD54F; text-decoration: underline; font-size: 12px;")
#         forget_password.setAlignment(Qt.AlignmentFlag.AlignRight)
#         content_layout.addWidget(forget_password)
#
#         # أزرار التسجيل وتسجيل الدخول
#         buttons_layout = QHBoxLayout()
#         buttons_layout.setSpacing(10)
#
#         register_button = QPushButton("التسجيل")
#         register_button.setFixedHeight(45)
#         register_button.setStyleSheet("""
#             QPushButton {
#                 background-color: white;
#                 color: #FF9800;
#                 border: 2px solid #FF9800;
#                 font-weight: bold;
#                 border-radius: 22px;
#                 font-size: 14px;
#             }
#             QPushButton:hover {
#                 background-color: #FFF3E0;
#             }
#         """)
#         buttons_layout.addWidget(register_button)
#
#         login_button = QPushButton("تسجيل الدخول")
#         login_button.setFixedHeight(45)
#         login_button.setStyleSheet("""
#             QPushButton {
#                 background-color: #FF9800;
#                 color: white;
#                 font-weight: bold;
#                 border-radius: 22px;
#                 font-size: 14px;
#             }
#             QPushButton:hover {
#                 background-color: #F57C00;
#             }
#         """)
#         buttons_layout.addWidget(login_button)
#
#         content_layout.addLayout(buttons_layout)
#
#         # فاصل
#         separator = QLabel("أو باستخدام")
#         separator.setAlignment(Qt.AlignmentFlag.AlignCenter)
#         separator.setStyleSheet("color: white; font-size: 12px; margin-top: 20px;")
#         content_layout.addWidget(separator)
#
#         # أيقونات التواصل الاجتماعي (بدون صور حقيقية حالياً)
#         social_layout = QHBoxLayout()
#         social_layout.setSpacing(15)
#         social_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
#
#         for name in ["Google", "Twitter", "Facebook"]:
#             btn = QPushButton(name[0])  # أول حرف كرمز مؤقت
#             btn.setFixedSize(40, 40)
#             btn.setStyleSheet("""
#                 QPushButton {
#                     background-color: white;
#                     border: 1px solid #ddd;
#                     border-radius: 20px;
#                     font-weight: bold;
#                     color: #555;
#                 }
#                 QPushButton:hover {
#                     background-color: #f0f0f0;
#                 }
#             """)
#             social_layout.addWidget(btn)
#
#         content_layout.addLayout(social_layout)
#
#         right_main_layout.addLayout(content_layout)
#         right_widget.setLayout(right_main_layout)
#         main_layout.addWidget(right_widget)
#
#         self.setLayout(main_layout)
#
#     def forget_form(self, event):
#         self.screen = ForgetPasswordForm(parent=self)
#         self.screen.show()
#         self.hide()
#
#     def __init_ui(self):
#         self.setWindowTitle(APP_NAME + ' - تسجيل الدخول')
#         self.setWindowFlags(Qt.WindowType.FramelessWindowHint)  # ⬅️ إزالة الشريط العلوي
#         width, height = 1000, 600
#         self.setFixedSize(width, height)


