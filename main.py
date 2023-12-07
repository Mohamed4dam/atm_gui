from PyQt6.QtWidgets import QApplication
import logic



def main():
    app = QApplication([])
    window = logic.BankAppLogic()
    pin_dialog = logic.PinInputDialog()
    while True:
        if pin_dialog.exec() == logic.QDialog.DialogCode.Accepted:
            if logic.BankAppLogic.validate_pin(pin_dialog.get_pin()):
                break
    window.show()

    app.exec()




if __name__ == '__main__':
    main()

    