import sys
from PyQt5.QtWidgets import QApplication
from windows.login import LoginWindow
from windows.home_page import HomePage


def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    login_window = LoginWindow()
    login_window.show()
    
    app.exec_()
    
    if login_window.token:
        main_window = HomePage(
            login_window.token, 
            login_window.user_data,
            login_window.refresh_token
        )
        main_window.show()
        sys.exit(app.exec_())
    else:
        sys.exit(0)


if __name__ == '__main__':
    main()