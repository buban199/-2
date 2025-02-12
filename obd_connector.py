import obd

class OBDConnector:
    def __init__(self):
        self.connection = None

    def connect(self, port=None, baudrate=38400, timeout=30):
        """Подключение к адаптеру ELM327."""
        try:
            self.connection = obd.OBD(port, baudrate=baudrate, timeout=timeout)
            if self.connection.is_connected():
                print("Подключение к ELM327 установлено.")
                return True
            else:
                print("Не удалось подключиться к ELM327.")
                return False
        except Exception as e:
            print(f"Ошибка при подключении: {e}")
            return False

    def disconnect(self):
        """Отключение от адаптера."""
        if self.connection:
            self.connection.close()
            print("Подключение к ELM327 закрыто.")

    def get_vin(self):
        """Чтение VIN автомобиля."""
        if self.connection:
            response = self.connection.query(obd.commands.VIN)
            if not response.is_null():
                return response.value
        return None