import tkinter as tk
from tkinter import ttk, messagebox
import serial.tools.list_ports
from obd_connector import OBDConnector
from obd_reader import OBDReader

class OBDApp:
    def __init__(self, root):
        self.root = root
        self.root.title("OBD2 Reader")
        self.root.geometry("400x300")

        self.connector = OBDConnector()
        self.reader = OBDReader(self.connector)

        # Список доступных портов
        self.available_ports = self.get_available_ports()

        self.create_widgets()

    def get_available_ports(self):
        """Получить список доступных COM-портов."""
        ports = serial.tools.list_ports.comports()
        return [port.device for port in ports]

    def create_widgets(self):
        """Создание элементов интерфейса."""
        # Выбор COM-порта
        self.port_label = ttk.Label(self.root, text="Выберите COM-порт:")
        self.port_label.pack(pady=10)

        self.port_combobox = ttk.Combobox(self.root, values=self.available_ports)
        self.port_combobox.pack(pady=10)
        if self.available_ports:
            self.port_combobox.current(0)  # Выбрать первый порт по умолчанию

        # Кнопка подключения
        self.connect_button = ttk.Button(self.root, text="Подключиться", command=self.connect)
        self.connect_button.pack(pady=10)

        # Поле для отображения VIN
        self.vin_label = ttk.Label(self.root, text="VIN: Не подключено")
        self.vin_label.pack(pady=10)

        # Поле для отображения RPM
        self.rpm_label = ttk.Label(self.root, text="RPM: -")
        self.rpm_label.pack(pady=10)

        # Поле для отображения скорости
        self.speed_label = ttk.Label(self.root, text="Скорость: -")
        self.speed_label.pack(pady=10)

        # Кнопка для обновления данных
        self.update_button = ttk.Button(self.root, text="Обновить данные", command=self.update_data)
        self.update_button.pack(pady=10)

    def connect(self):
        """Подключение к адаптеру."""
        selected_port = self.port_combobox.get()
        if not selected_port:
            messagebox.showwarning("Ошибка", "Выберите COM-порт.")
            return

        if self.connector.connect(port=selected_port):
            vin = self.connector.get_vin()
            self.vin_label.config(text=f"VIN: {vin}")
            messagebox.showinfo("Успех", "Подключение установлено!")
        else:
            messagebox.showerror("Ошибка", "Не удалось подключиться к адаптеру.")

    def update_data(self):
        """Обновление данных OBD2."""
        if self.connector.connection:
            data = self.reader.read_all_parameters()
            self.rpm_label.config(text=f"RPM: {data.get('RPM', '-')}")
            self.speed_label.config(text=f"Скорость: {data.get('SPEED', '-')}")
        else:
            messagebox.showwarning("Предупреждение", "Сначала подключитесь к адаптеру.")