# 🍳 HowToCook-py-MCP 🥘 -- 炫一周好饭，拒绝拼好饭

[English](./README_EN.md) | 简体中文

> 让 AI 助手变身私人大厨，为你的一日三餐出谋划策！

这是一个Python版的菜谱助手MCP服务，使用FastMCP库实现。基于[Anduin2017/HowToCook](https://github.com/Anduin2017/HowToCook)打造，让 AI 助手能够为你推荐菜谱、规划膳食，解决"今天吃什么"的世纪难题！

特别感谢[worryzyy/HowToCook-mcp](https://github.com/worryzyy/HowToCook-mcp)，这个Python版本是从那边模仿过来的😄！

## 📸 效果预览

![功能预览1](img/01.png)

## 🔌 支持的 MCP 客户端

本服务器已在以下客户端测试通过:

- 📝 Cursor

## ✨ 美味功能

该 MCP 服务器提供以下美食工具:

1. **📚 获取所有菜谱** (`get_all_recipes`) - 返回所有可用菜谱的简化版数据 -- 慎用这个--上下文太大
2. **🔍 按分类获取菜谱** (`get_recipes_by_category`) - 根据指定的分类查询菜谱，想吃水产？早餐？荤菜？主食？一键搞定！
3. **🎲 不知道吃什么** (`what_to_eat`) - 选择困难症福音！根据人数直接推荐今日菜单，再也不用纠结了
4. **🧩 推荐膳食计划** (`recommend_meals`) - 根据你的忌口、过敏原和用餐人数，为你规划整整一周的美味佳肴

## 🚀 快速上手

### 📋 先决条件

- Python 3.12.9+ 🐍
- 必要的Python依赖包 📦

### 💻 安装步骤

1. 克隆美食仓库

```bash
git clone https://github.com/DusKing1/howtocook-py-mcp.git
cd howtocook-py-mcp
```

2. 安装依赖（就像准备食材一样简单！）

```bash
pip install -r requirements.txt
```

### ❓ 为什么不用uv

你每天都忘记上千件事，为什么不把这件也忘了？

## 🍽️ 开始使用

### 🔥 启动服务器

```bash
# 确保在项目根目录下运行
python -m src.app
```

服务将在9000端口通过SSE传输协议运行。

### 🔧 配置 MCP 客户端

#### 使用 Cursor 快速体验

在 Cursor 设置中添加 MCP 服务器配置：

```json
{
  "mcpServers": {
    "how to cook": {
      "url": "http://localhost:9000/sse"
    }
  }
}
```

#### 其他 MCP 客户端

对于其他支持 MCP 协议的客户端，请参考各自的文档进行配置。

## 🧙‍♂️ 菜单魔法使用指南

以下是在各种 MCP 客户端中使用的示例提示语：

### 1. 📚 获取所有菜谱

无需参数，直接召唤美食全书！

```
请使用howtocook-py-mcp的MCP服务查询所有菜谱
```

### 2. 🔍 按分类获取菜谱

```
请使用howtocook-py-mcp的MCP服务查询水产类的菜谱
```

参数:

- `category`: 菜谱分类（水产、早餐、荤菜、主食等）

### 3. 🎲 不知道吃什么？

```
请使用howtocook-py-mcp的MCP服务为4人晚餐推荐菜单
```

参数:

- `people_count`: 用餐人数 (1-10)

### 4. 🧩 推荐膳食计划

```
请使用howtocook-py-mcp的MCP服务为3人推荐一周菜谱，我们家不吃香菜，对虾过敏
```

参数:

- `allergies`: 过敏原列表，如 ["大蒜", "虾"]
- `avoid_items`: 忌口食材，如 ["葱", "姜"]
- `people_count`: 用餐人数 (1-10)

## 📝 小贴士

- 本服务兼容所有支持 MCP 协议的 AI 助手和应用
- 首次使用时，AI 可能需要一点时间来熟悉如何使用这些工具（就像烧热锅一样）

## 📄 数据来源

菜谱数据来自远程JSON文件，URL：
`https://mp-bc8d1f0a-3356-4a4e-8592-f73a3371baa2.cdn.bspapp.com/all_recipes.json`

## 🤝 贡献

欢迎 Fork 和 Pull Request，让我们一起完善这个美食助手！

## 📄 许可

MIT License - 随意使用，就像分享美食配方一样慷慨！

---

> 🍴 美食即将开始，胃口准备好了吗？
