import tkinter as tk
from tkinter import ttk, messagebox
import serial.tools.list_ports
from obd_connector import OBDConnector
from obd_reader import OBDReader

class OBDApp:
    def __init__(self, root):
        self.root = root
        self.root.title("OBD2 Reader")
        self.root.geometry("1400x900")  # Увеличиваем размер стартового окна

        self.connector = OBDConnector()
        self.reader = OBDReader(self.connector)

        # Список доступных портов
        self.available_ports = self.get_available_ports()

        # Список поддерживаемых команд
        self.supported_commands = []

        # Список выбранных команд
        self.selected_commands = []

        # Статус мониторинга
        self.monitoring = False

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

        # Фрейм для отображения доступных и выбранных PID
        self.pid_frame = ttk.Frame(self.root)
        self.pid_frame.pack(fill=tk.BOTH, expand=True)

        # Список доступных PID
        self.available_pid_label = ttk.Label(self.pid_frame, text="Доступные PID:")
        self.available_pid_label.grid(row=0, column=0, padx=10, pady=10)

        self.available_pid_listbox = tk.Listbox(self.pid_frame, selectmode=tk.MULTIPLE, width=60, height=30)
        self.available_pid_listbox.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        # Кнопка для добавления выбранных PID
        self.add_button = ttk.Button(self.pid_frame, text="Добавить →", command=self.add_selected_pids)
        self.add_button.grid(row=1, column=1, padx=10, pady=10)

        # Список выбранных PID
        self.selected_pid_label = ttk.Label(self.pid_frame, text="Выбранные PID:")
        self.selected_pid_label.grid(row=0, column=2, padx=10, pady=10)

        self.selected_pid_listbox = tk.Listbox(self.pid_frame, width=60, height=30)
        self.selected_pid_listbox.grid(row=1, column=2, padx=10, pady=10, sticky="nsew")

        # Кнопка для удаления выбранных PID
        self.remove_button = ttk.Button(self.pid_frame, text="Убрать параметры", command=self.remove_selected_pids)
        self.remove_button.grid(row=2, column=2, padx=10, pady=10)

        # Кнопка для начала мониторинга
        self.start_button = ttk.Button(self.root, text="Начать мониторинг", command=self.start_monitoring)
        self.start_button.pack(pady=10)

        # Кнопка для остановки мониторинга
        self.stop_button = ttk.Button(self.root, text="Остановить мониторинг", command=self.stop_monitoring)
        self.stop_button.pack(pady=10)

        # Статус бар
        self.status_bar = ttk.Progressbar(self.root, orient=tk.HORIZONTAL, mode='indeterminate')
        self.status_bar.pack(fill=tk.X, padx=10, pady=10)

        # Постоянные данные в нижнем углу
        self.constant_data_frame = ttk.Frame(self.root)
        self.constant_data_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)

        self.vin_label = ttk.Label(self.constant_data_frame, text="VIN: Нет данных")
        self.vin_label.pack(side=tk.LEFT, padx=10)

        self.voltage_label = ttk.Label(self.constant_data_frame, text="Вольтаж: Нет данных")
        self.voltage_label.pack(side=tk.RIGHT, padx=10)

    def connect(self):
        """Подключение к адаптеру."""
        selected_port = self.port_combobox.get()
        if not selected_port:
            messagebox.showwarning("Ошибка", "Выберите COM-порт.")
            return

        if self.connector.connect(port=selected_port):
            # Получаем список поддерживаемых команд
            self.supported_commands = list(self.reader.get_supported_commands())
            if self.supported_commands:
                # Заполняем список доступных PID
                self.available_pid_listbox.delete(0, tk.END)
                for cmd in self.supported_commands:
                    self.available_pid_listbox.insert(tk.END, cmd.name)
            messagebox.showinfo("Успех", "Подключение установлено!")

            # Получаем VIN и вольтаж
            vin = self.connector.get_vin()
            self.vin_label.config(text=f"VIN: {vin}")

            voltage = self.reader.read_parameter(obd.commands.ELM_VOLTAGE)
            self.voltage_label.config(text=f"Вольтаж: {voltage if voltage else 'Нет данных'}")
        else:
            messagebox.showerror("Ошибка", "Не удалось подключиться к адаптеру.")

    def add_selected_pids(self):
        """Добавление выбранных PID в список для мониторинга."""
        selected_indices = self.available_pid_listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("Ошибка", "Выберите PID для добавления.")
            return

        # Добавляем выбранные команды
        for i in selected_indices:
            cmd = self.supported_commands[i]
            if cmd.name not in self.selected_commands:
                self.selected_commands.append(cmd.name)
                self.selected_pid_listbox.insert(tk.END, cmd.name)

    def remove_selected_pids(self):
        """Удаление выбранных PID из списка для мониторинга."""
        selected_indices = self.selected_pid_listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("Ошибка", "Выберите PID для удаления.")
            return

        # Удаляем выбранные команды
        for i in reversed(selected_indices):
            self.selected_commands.pop(i)
            self.selected_pid_listbox.delete(i)

    def start_monitoring(self):
        """Начать мониторинг выбранных PID."""
        if not self.selected_commands:
            messagebox.showwarning("Ошибка", "Выберите PID для мониторинга.")
            return

        self.monitoring = True
        self.status_bar.start()
        self.update_data()

    def stop_monitoring(self):
        """Остановить мониторинг."""
        self.monitoring = False
        self.status_bar.stop()

    def update_data(self):
        """Обновление данных OBD2."""
        if self.monitoring and self.connector.connection and self.selected_commands:
            data = {}
            for cmd_name in self.selected_commands:
                cmd = next((cmd for cmd in self.supported_commands if cmd.name == cmd_name), None)
                if cmd:
                    value = self.reader.read_parameter(cmd)
                    data[cmd_name] = value if value is not None else "N/A"

            # Отображаем данные в правом окне
            self.selected_pid_listbox.delete(0, tk.END)
            for name, value in data.items():
                self.selected_pid_listbox.insert(tk.END, f"{name} ----- {value}")

            # Планируем следующее обновление
            self.root.after(1000, self.update_data)  # Обновление каждую секунду
        else:
            self.status_bar.stop()