import obd

class OBDReader:
    def __init__(self, connector):
        self.connector = connector

    def get_supported_commands(self):
        """Возвращает список поддерживаемых команд."""
        if self.connector.connection:
            return self.connector.connection.supported_commands
        return []

    def read_parameter(self, command):
        """Чтение одного параметра."""
        if self.connector.connection:
            response = self.connector.connection.query(command)
            if not response.is_null():
                return response.value.magnitude if hasattr(response.value, 'magnitude') else response.value
        return None

    def read_all_parameters(self, commands):
        """Чтение выбранных параметров."""
        data = {}
        for cmd in commands:
            value = self.read_parameter(cmd)
            data[cmd.name] = value if value is not None else "N/A"
        return data