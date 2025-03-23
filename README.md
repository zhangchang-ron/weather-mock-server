# Weather Mock MCP Server

一个基于 MCP (Message Control Protocol) 协议的模拟天气数据服务器。该服务器提供实时模拟的天气数据，支持不同季节的天气信息查询。

## 功能特点

- 基于 MCP 协议的二进制通信
- 支持多客户端并发连接
- 提供真实的天气数据模拟
- 支持四季温度范围调整
- 包含完整的天气信息（温度、天气状况、湿度、风速等）
- 简单易用的客户端 API

## 技术规格

### MCP 协议说明

消息格式：
1. 消息头：4 字节的消息长度（网络字节序）
2. 消息体：JSON 格式的数据

### 数据范围

温度范围（°C）：
- 夏季：20 ~ 35
- 冬季：-5 ~ 15
- 春秋：10 ~ 25

其他数据范围：
- 湿度：30% ~ 95%
- 风速：0 ~ 30 km/h
- 天气状况：晴天、多云、阴天、小雨、中雨、大雨、雷阵雨、小雪、中雪、大雪

## 安装

1. 克隆仓库：
```bash
git clone https://github.com/yourusername/weather-mock-server.git
cd weather-mock-server
```

2. 创建虚拟环境：
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
.\venv\Scripts\activate  # Windows
```

3. 安装依赖：
```bash
pip install -r requirements.txt
```

## 使用方法

### 启动服务器

```bash
python mcp_server.py
```

服务器将在 0.0.0.0:8000 启动，等待客户端连接。

### 使用客户端

```python
from mcp_client import MCPClient

# 创建客户端实例
client = MCPClient(host='localhost', port=8000)

# 获取天气数据
weather_data = client.get_weather(season='summer')

# 打印天气信息
print(f"温度: {weather_data['temperature']}°C")
print(f"天气: {weather_data['weather']}")
print(f"湿度: {weather_data['humidity']}%")
print(f"风速: {weather_data['wind_speed']} km/h")
```

### 示例响应

```json
{
    "date": "2024-03-23",
    "temperature": 32.1,
    "weather": "多云",
    "humidity": 77,
    "wind_speed": 24.4
}
```

## API 参数

season 参数支持以下值：
- summer：夏季
- winter：冬季
- spring：春季
- autumn：秋季

## 开发说明

### 项目结构

```
weather-mock-server/
├── mcp_server.py    # 服务器实现
├── mcp_client.py    # 客户端实现
├── requirements.txt # 项目依赖
└── README.md       # 项目文档
```

### 扩展建议

1. 添加更多天气参数（气压、能见度等）
2. 实现数据持久化
3. 添加地理位置支持
4. 增加天气预警功能
5. 实现更复杂的天气模型

## 贡献

欢迎提交 Issue 和 Pull Request 来帮助改进项目。

## 许可证

MIT License 