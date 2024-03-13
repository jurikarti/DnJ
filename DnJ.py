import sys
import json
from PySide6.QtCore import Qt

from PySide6.QtWidgets import (QApplication, QMainWindow, QPushButton, QHBoxLayout, QVBoxLayout, QWidget, QLineEdit,
                               QDialog, QLabel, QFileDialog, QDockWidget)

class FieldCreationDock(QDockWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(' ')
        self.widget = QWidget()
        self.setWidget(self.widget)
        self.layout = QVBoxLayout(self.widget)

        # Поле для ввода делителя при значении равно 20
        self.input_divider_20 = QLineEdit(self)
        self.input_divider_20.setPlaceholderText("Введите делитель для = 20")  # Устанавливаем текст-подсказку
        self.layout.addWidget(self.input_divider_20)

        # Поле для ввода делителя при значении >= 10
        self.input_divider_10 = QLineEdit(self)
        self.input_divider_10.setPlaceholderText("Введите делитель для >= 10")  # Устанавливаем текст-подсказку
        self.layout.addWidget(self.input_divider_10)

        # Поле для ввода делителя при значении >= 5
        self.input_divider_5 = QLineEdit(self)
        self.input_divider_5.setPlaceholderText("Введите делитель для >= 5")  # Устанавливаем текст-подсказку
        self.layout.addWidget(self.input_divider_5)

        # Поле для ввода делителя при значении равно 1
        self.input_divider_1 = QLineEdit(self)
        self.input_divider_1.setPlaceholderText("Введите делитель для = 1")  # Устанавливаем текст-подсказку
        self.layout.addWidget(self.input_divider_1)

        # Поле для ввода названия нового поля
        self.input_field_name = QLineEdit(self)
        self.input_field_name.setPlaceholderText("Введите название")  # Устанавливаем текст-подсказку
        self.layout.addWidget(self.input_field_name)

        # Кнопка для создания нового поля
        self.button_add_field = QPushButton(' ✅ Создать поле', self)
        self.button_add_field.clicked.connect(self.parent().add_input_field_from_dock)
        self.layout.addWidget(self.button_add_field)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('DnDTawerna')
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Словарь для хранения полей ввода и меток
        self.fields = {}
        self.field_count = 0

        # Инициализация основного компоновщика для центрального виджета
        self.main_layout = QVBoxLayout(self.central_widget)

        # Добавление растягивающего пространства в компоновщик после добавления кнопок
        self.main_layout.addStretch()

        # Кнопка для сохранения данных
        self.button_save = QPushButton('⚡ Сохранить', self)
        self.button_save.clicked.connect(self.save_data)
        self.main_layout.addWidget(self.button_save)

        # Кнопка для импорта сохраненных данных
        self.button_import = QPushButton('⬇ Импортировать сохранение', self)
        self.button_import.clicked.connect(self.import_data)
        self.main_layout.addWidget(self.button_import)

        # Пристань для создания новых полей
        self.field_creation_dock = FieldCreationDock(self)
        self.addDockWidget(Qt.RightDockWidgetArea, self.field_creation_dock)
        self.field_creation_dock.setStyleSheet("""
            QDockWidget::title {
                background: #44475a;
                text-align: center;
                height: 20px;
            }
        """)


        self.field_creation_dock.hide()  # Скрываем виджет по умолчанию

        # Кнопка для отображения или скрытия пристани создания новых полей
        self.button_toggle_dock = QPushButton('➕ Добавить Компонент', self)
        self.button_toggle_dock.clicked.connect(self.toggle_dock)
        self.main_layout.addWidget(self.button_toggle_dock)

        # Кнопка для выполнения логики "день"
        self.button_day = QPushButton('☑ Посчитать', self)
        self.button_day.clicked.connect(self.apply_day_logic)
        self.main_layout.addWidget(self.button_day)

    def toggle_dock(self):
        if self.field_creation_dock.isVisible():
            self.field_creation_dock.hide()
            self.button_toggle_dock.setText('➕ Добавить Компонент')
        else:
            self.field_creation_dock.show()
            self.button_toggle_dock.setText('Скрыть виджет')

    def add_input_field_from_dock(self):
        field_name = self.field_creation_dock.input_field_name.text()
        if field_name:
            # Создание горизонтального слоя для поля ввода, названия и метки
            horizontal_layout = QHBoxLayout()

            # Создание названия поля
            field_label = QLabel(field_name, self)
            field_label.setStyleSheet("color: white;")

            # Создание поля ввода
            input_field = QLineEdit(self)
            input_field.setPlaceholderText("Введите количество")  # Устанавливаем текст-подсказку

            # Создание стилизованной метки для результата рандома
            random_result_label = QLineEdit(self)  # Изменено на QLineEdit
            random_result_label.setPlaceholderText("1к20")  # Устанавливаем текст-подсказку
            random_result_label.setStyleSheet("""
                QLineEdit {  # Изменено на QLineEdit
                    background-color: #44475a;
                    color: #f8f8f2;
                    border: none;
                    padding: 10px;
                    margin: 5px;
                    border-radius: 5px;
                    min-width: 20px;
                    max-width: 20px;  /* Минимальная ширина */
                }
            """)

            # Добавление виджетов в горизонтальный слой
            horizontal_layout.addWidget(field_label)
            horizontal_layout.addWidget(input_field)
            horizontal_layout.addWidget(random_result_label)

            # Добавление горизонтального слоя в основной вертикальный слой
            self.main_layout.insertLayout(self.main_layout.count() - 1, horizontal_layout)

            # Сохранение ссылок на виджеты в словаре
            self.fields[self.field_count] = (input_field, random_result_label, field_name)
            self.field_count += 1

    def apply_day_logic(self):
        divider_20 = float(self.field_creation_dock.input_divider_20.text())
        divider_10 = float(self.field_creation_dock.input_divider_10.text())
        divider_5 = float(self.field_creation_dock.input_divider_5.text())
        divider_1 = float(self.field_creation_dock.input_divider_1.text())
        for _, (input_field, random_result_label, _) in self.fields.items():
            text = input_field.text().replace(',', '.')
            try:
                value = float(text)
                roll = float(random_result_label.text())  # Изменено на float(random_result_label.text())
                if roll == 20:
                    result = value / divider_20  # Изменено на divider_20
                elif roll >= 10:
                    result = value / divider_10  # Изменено на divider_10
                elif roll >= 5:
                    result = value / divider_5  # Изменено на divider_5
                elif roll == 1:
                    result = value / divider_1  # Изменено на divider_1
                else:
                    result = value  # Если число не попадает ни в один из диапазонов, оставляем его без изменений
                input_field.setText(str(result))
                random_result_label.setText(f'{roll}')
            except ValueError:
                input_field.clear()  # Очистка поля ввода
                input_field.setPlaceholderText('Ошибка! Введите число.')  # Установка текста-подсказки

    def import_data(self):
        file_name, _ = QFileDialog.getOpenFileName(self, 'Открыть файл сохранения', '', 'JSON Files (*.json)')
        if file_name:
            with open(file_name, 'r') as file:
                data = json.load(file)
                for field_name, value in data['fields'].items():
                    # Проверяем, существует ли поле с таким названием
                    if not any(field_name == existing_field_name for _, (_, _, existing_field_name) in
                               self.fields.items()):
                        # Если поля нет, создаем его
                        self.create_input_field(field_name)
                    # Заполняем поле значением из файла
                    for _, (input_field, _, existing_field_name) in self.fields.items():
                        if existing_field_name == field_name:
                            input_field.setText(value)
                # Загружаем значения делителей
                self.field_creation_dock.input_divider_20.setText(str(data['dividers']['20']))
                self.field_creation_dock.input_divider_10.setText(str(data['dividers']['10']))
                self.field_creation_dock.input_divider_5.setText(str(data['dividers']['5']))
                self.field_creation_dock.input_divider_1.setText(str(data['dividers']['1']))

    def create_input_field(self, field_name):
        # Создание горизонтального слоя для поля ввода, названия и метки
        horizontal_layout = QHBoxLayout()

        # Создание названия поля
        field_label = QLabel(field_name, self)
        field_label.setStyleSheet("color: white;")

        # Создание поля ввода
        input_field = QLineEdit(self)

        input_field.setText('')  # Устанавливаем пустое значение по умолчанию

        # Создание стилизованной метки для результата рандома
        random_result_label = QLineEdit(self)  # Изменено на QLineEdit
        random_result_label.setStyleSheet("""
            QLineEdit {  # Изменено на QLineEdit
                background-color: #44475a;
                color: #f8f8f2;
                border: none;
                padding: 10px;
                margin: 5px;
                border-radius: 5px;
                min-width: 20px;
                max-width: 20px;  /* Минимальная ширина */
            }
        """)

        # Добавление виджетов в горизонтальный слой
        horizontal_layout.addWidget(field_label)
        horizontal_layout.addWidget(input_field)
        horizontal_layout.addWidget(random_result_label)

        # Добавление горизонтального слоя в основной вертикальный слой
        self.main_layout.insertLayout(self.main_layout.count() - 1, horizontal_layout)

        # Сохранение ссылок на виджеты в словаре
        self.fields[self.field_count] = (input_field, random_result_label, field_name)
        self.field_count += 1

    def save_data(self):
        # Сохраняем значения полей
        field_data = {field_name: input_field.text() for _, (input_field, _, field_name) in self.fields.items()}
        # Сохраняем значения делителей
        divider_data = {
            '20': self.field_creation_dock.input_divider_20.text(),
            '10': self.field_creation_dock.input_divider_10.text(),
            '5': self.field_creation_dock.input_divider_5.text(),
            '1': self.field_creation_dock.input_divider_1.text()
        }
        # Объединяем данные полей и делителей в один словарь
        data = {'fields': field_data, 'dividers': divider_data}
        # Открываем диалоговое окно для сохранения файла
        file_name, _ = QFileDialog.getSaveFileName(self, 'Сохранить как', '', 'JSON Files (*.json)')
        if file_name:
            with open(file_name, 'w') as file:
                json.dump(data, file, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    # Устанавливаем тему Dracula
    app.setStyleSheet("""
        QMainWindow {
            background-color: #282a36;
        }
        QLineEdit {
            background-color: #44475a;
            color: #f8f8f2;
            border: none;
            padding: 10px;
            margin: 5px;
            border-radius: 5px;
            min-width: 180px;  /* Минимальная ширина */
            max-width: 200px;  /* Максимальная ширина */
        }
        QLabel {
            color: #f8f8f2;
            background-color: #44475a;
            border: none;
            padding: 10px;
            margin: 5px;
            border-radius: 5px;
            min-width: 100px;  /* Минимальная ширина */
            max-height: 20px;
        }
        QPushButton {
            background-color: #44475a;
            border: none;
            color: #f8f8f2;
            padding: 15px;
            margin: 5px;
            border-radius: 10px;
        }
        QPushButton:hover {
            background-color: #6272a4;
        }
    """)
    sys.exit(app.exec())
