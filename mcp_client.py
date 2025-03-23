import socket
import json
import struct

class MCPClient:
    def __init__(self, host='localhost', port=8000):
        self.host = host
        self.port = port
        
    def get_weather(self, season='summer'):
        try:
            # 创建 socket 连接
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((self.host, self.port))
                
                # 准备请求数据
                request = json.dumps({'season': season})
                request_bytes = request.encode()
                
                # 发送请求（长度 + 数据）
                request_length = struct.pack('!I', len(request_bytes))
                s.sendall(request_length + request_bytes)
                
                # 接收响应头（4字节长度）
                header = s.recv(4)
                if not header:
                    return None
                    
                # 解析响应长度
                response_length = struct.unpack('!I', header)[0]
                
                # 接收响应数据
                response = b''
                while len(response) < response_length:
                    chunk = s.recv(min(response_length - len(response), 1024))
                    if not chunk:
                        break
                    response += chunk
                    
                # 解析响应数据
                if response:
                    return json.loads(response.decode())
                    
        except Exception as e:
            print(f"Error: {e}")
            return None

def main():
    client = MCPClient()
    
    # 获取今天的天气数据
    weather_data = client.get_weather(season='summer')
    
    if weather_data:
        print("\n今日天气信息:")
        print(f"日期: {weather_data['date']}")
        print(f"温度: {weather_data['temperature']}°C")
        print(f"天气: {weather_data['weather']}")
        print(f"湿度: {weather_data['humidity']}%")
        print(f"风速: {weather_data['wind_speed']} km/h")
    else:
        print("获取天气数据失败")

if __name__ == '__main__':
    main() 