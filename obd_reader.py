import time

class OBDReader:
    def __init__(self, connector):
        self.connector = connector

    def read_parameter(self, command):
        """Чтение одного параметра."""
        if self.connector.connection:
            response = self.connector.connection.query(command)
            if not response.is_null():
                return response.value.magnitude if hasattr(response.value, 'magnitude') else response.value
        return None

    def read_all_parameters(self):
        """Чтение всех доступных параметров."""
        parameters = {
            "RPM": obd.commands.RPM,
            "SPEED": obd.commands.SPEED,
            "COOLANT_TEMP": obd.commands.COOLANT_TEMP,
            "FUEL_PRESSURE": obd.commands.FUEL_PRESSURE,
            "O2_SENSOR": obd.commands.O2_B1S1,
            "IGNITION_TIMING": obd.commands.TIMING_ADVANCE,
        }

        data = {}
        for name, cmd in parameters.items():
            data[name] = self.read_parameter(cmd)
        return data