# 🍻 约酒热力图项目 (Drink-Heatmap) 详细设计文档

## 1. 项目基本信息
* **项目名称**：约酒热力图 (Drink-Heatmap)
* **项目目标**：创建一个轻量级、直观的社交日历，展示好友约酒意向及热度。（*注：仅限信任的熟人/朋友圈使用，无身份验证机制*）
* **技术架构**：Vue 3 (Frontend) + FastAPI (Backend) + Redis (Storage)
* **管理工具**：uv (Python Package Manager)

---

## 2. 核心功能设计
| 功能模块 | 描述 |
| :--- | :--- |
| **热力日历** | 以日历形式展现，格子颜色深度代表当天“想喝酒”的人数，在日期下面增加火种图标，表示当日热度。 |
| **热度排行** | (可选) 展示本月最受期待的喝酒日期。 |

---

## 3. 技术规范

### 3.1 后端 (Python FastAPI)
* **Python版本**：3.12 (通过 uv 管理)
* **依赖库**：`fastapi`, `uvicorn`, `redis`
* **核心逻辑**：
    * 接收前端日期点击请求。
    * 通过 Redis 的 `HINCRBY` 命令实现热度原子自增。


### 3.2 存储 (Redis)
* **热度数据 (Hash)**：`drink:heat:calendar` -> `{ "2026-01-20": 5 }* **存储地址** 47.95.11.247:6379 密码：Asiainfo@2 


### 3.3 前端 (Vue 3)
* **框架**：Vite + Vue 3
* **UI组件库**：Element Plus
* **日历实现**：使用 `el-calendar` 组件，通过 `v-slot` 插入自定义渲染逻辑，根据后端 Heat Count 映射 CSS 颜色。

---

## 4. 接口协议 (API)

### [GET] /api/v1/calendar/summary
* **描述**：获取当前月份所有日期的热度分布。
* **返回格式**：`{ "YYYY-MM-DD": int, ... }`


---

## 5. 部署路径
1.  **后端**：阿里云服务器运行 `uv run uvicorn main:app`。
2.  **前端**：构建后由 Nginx 托管静态资源。
3.  **代理**：Nginx 将 `/api` 请求转发至后端 8099 端口。