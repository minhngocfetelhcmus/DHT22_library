from machine import I2C
import time

class AHTSensor:
    def __init__(self, i2c, address=0x38):
        self._i2c = i2c
        self._address = address
        # Khởi tạo cảm biến
        self._setup()

    def _setup(self):
        # Đợi cảm biến ổn định
        time.sleep_ms(20)
        try:
            # Lệnh khởi tạo chuẩn cho dòng AHT
            self._i2c.writeto(self._address, b'\xbe\x08\x00')
        except:
            pass

    def read_data(self):
        try:
            # Gửi lệnh đo
            self._i2c.writeto(self._address, b'\xac\x33\x00')
            time.sleep_ms(80)
            
            # Đọc 6 byte
            data = self._i2c.readfrom(self._address, 6)
            
            # Kiểm tra trạng thái sẵn sàng (bit 7 của byte 0 phải bằng 0)
            if (data[0] & 0x80) == 0:
                # Tính toán độ ẩm
                raw_hum = ((data[1] << 12) | (data[2] << 4) | (data[3] >> 4))
                humidity = (raw_hum * 100) / 1048576
                
                # Tính toán nhiệt độ
                raw_temp = ((data[3] & 0x0F) << 16) | (data[4] << 8) | data[5]
                temperature = (raw_temp * 200 / 1048576) - 50
                
                return temperature, humidity
            else:
                return None, None
        except Exception:
            return None, None