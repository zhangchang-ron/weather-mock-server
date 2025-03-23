import socket
import json
import struct
import random
from datetime import datetime
from threading import Thread

class WeatherMock:
    def __init__(self):
        self.weather_conditions = [
            "晴天", "多云", "阴天", "小雨", "中雨", "大雨", 
            "雷阵雨", "小雪", "中雪", "大雪"
        ]
        
    def get_random_temperature(self, season="summer"):
        if season == "summer":
            return round(random.uniform(20, 35), 1)
        elif season == "winter":
            return round(random.uniform(-5, 15), 1)
        else:  # spring or autumn
            return round(random.uniform(10, 25), 1)
    
    def get_random_humidity(self):
        return random.randint(30, 95)
    
    def get_random_wind_speed(self):
        return round(random.uniform(0, 30), 1)
    
    def get_random_weather(self):
        return random.choice(self.weather_conditions)
    
    def get_weather_data(self, season="summer"):
        return {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "temperature": self.get_random_temperature(season),
            "weather": self.get_random_weather(),
            "humidity": self.get_random_humidity(),
            "wind_speed": self.get_random_wind_speed()
        }

class MCPServer:
    def __init__(self, host='0.0.0.0', port=8000):
        self.host = host
        self.port = port
        self.weather_mock = WeatherMock()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
    def start(self):
        self.sock.bind((self.host, self.port))
        self.sock.listen(5)
        print(f"MCP Weather Server running on {self.host}:{self.port}")
        
        while True:
            client, address = self.sock.accept()
            print(f"Client connected from {address}")
            client_thread = Thread(target=self.handle_client, args=(client,))
            client_thread.start()
            
    def handle_client(self, client_socket):
        try:
            # 接收消息头（4字节长度）
            header = client_socket.recv(4)
            if not header:
                return
                
            # 解析消息长度
            message_length = struct.unpack('!I', header)[0]
            
            # 接收消息体
            message = b''
            while len(message) < message_length:
                chunk = client_socket.recv(min(message_length - len(message), 1024))
                if not chunk:
                    break
                message += chunk
                
            if message:
                # 解析请求
                request = json.loads(message.decode())
                season = request.get('season', 'summer')
                
                # 获取天气数据
                weather_data = self.weather_mock.get_weather_data(season)
                
                # 编码响应
                response_json = json.dumps(weather_data)
                response_bytes = response_json.encode()
                
                # 发送响应（长度 + 数据）
                response_length = struct.pack('!I', len(response_bytes))
                client_socket.sendall(response_length + response_bytes)
                
        except Exception as e:
            print(f"Error handling client: {e}")
        finally:
            client_socket.close()
            
def main():
    server = MCPServer()
    try:
        server.start()
    except KeyboardInterrupt:
        print("\nServer shutting down...")
    except Exception as e:
        print(f"Server error: {e}")

if __name__ == '__main__':
    main() 