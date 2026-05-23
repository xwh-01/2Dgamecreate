# AI 2D 游戏素材生成工具 - 架构设计

## 1. 整体架构

系统采用分层架构设计，自上而下分为六层：

```
[  API 层  ]   FastAPI Router → Request Validation → Response
     │
[ Service 层 ]   业务规则、事务协调
     │
[ Workflow 层 ]  素材生成全流程编排
     │
[  AI 层  ]   需求解析、Prompt 构建、模型调用、质量检查
     │
[ Storage 层 ]   图片文件存储、导出包管理
     │
[ Repository 层 ]  数据库 CRUD 抽象
```

各层之间通过依赖注入（FastAPI Depends）解耦，上层依赖接口而非具体实现，确保后续可替换任意一层而不影响其他层。

## 2. 分层设计

| 层 | 职责 | 不应做的事 |
|----|------|-----------|
| **API 层** (`api/`) | 接收 HTTP 请求，参数校验，调用 Service 层，构造 Response | 不应包含业务逻辑、不应直接操作数据库、不应调用 AI 模型 |
| **Service 层** (`services/`) | 处理业务规则，协调多个 Repository，触发 Workflow | 不应处理 HTTP 请求/响应细节、不应直接操作文件存储 |
| **Workflow 层** (`workflows/`) | 编排素材生成的完整步骤序列，管理步骤间数据传递 | 不应实现具体 AI 算法、不应直接读写数据库 |
| **AI 层** (`ai/`) | 自然语言需求解析、Prompt 构造与优化、图像模型客户端抽象、生成质量评估 | 不应管理任务状态、不应处理文件 I/O |
| **Storage 层** (`storage/`) | 图片文件的保存、读取、删除，导出包的生成，存储路径构造 | 不应管理数据库事务、不应包含业务规则 |
| **Repository 层** (`repositories/`) | 数据库的 CRUD 操作抽象，提供领域实体级别的查询接口 | 不应包含复杂业务逻辑、不应调用外部 AI 服务 |

层级间调用方向严格自上而下：API → Service → Workflow → AI / Repository。Storage 层可被 Workflow 和 Service 调用。不允许跨层调用（API 层不可直接调用 Repository 层）。

## 3. 核心模块职责

### Project 模块

管理游戏项目生命周期。一个项目包含名称、描述、创建时间，关联一组 StyleProfile 和一组 Asset。提供项目的创建、查询、更新、删除功能。

### StyleProfile 模块

管理项目级风格配置。定义画风（像素、扁平、手绘等）、视角（俯视、侧视、等距等）、色彩倾向、参考示例等全局约束。所有属于该项目的素材生成时都必须遵守此风格配置，确保视觉一致性。

### GenerationTask 模块

管理素材生成任务的生命周期。维护任务状态（待处理 → 处理中 → 成功/失败/取消），记录请求参数、生成结果引用、错误信息。支持重试和状态查询。

### Asset 模块

管理已生成的素材。记录素材的元数据（尺寸、格式、类型、文件路径、关联项目、关联生成任务），提供检索和下载能力。

### ExportPackage 模块

管理素材导出打包。支持将项目下部分或全部素材按指定格式打包导出，记录导出记录。

### AssetGenerationWorkflow

素材生成的工作流编排器。持有完整步骤链（需求解析 → Prompt 构造 → 图像生成 → 后处理 → 质量检查 → 文件保存），按序执行，处理步骤间数据传递和异常回退。

### PromptBuilder

将结构化生成参数（素材类型、风格约束、尺寸规格、内容描述）构造为高质量图像生成 Prompt。支持不同模型的 Prompt 格式适配。

### ImageGenerator

图像生成器，封装模型调用逻辑。通过 ImageGeneratorClient 接口与具体模型交互，处理重试、超时等异常。

### QualityChecker

对生成图像进行质量评估，包括：尺寸合规、背景透明度、风格一致性、视觉质量评分。评估不通过时触发重试或标记失败。

### FileStorage

物理文件存储。负责将图像数据写入磁盘、读取文件、删除过期素材。支持本地文件系统和对象存储两种后端。

## 4. 为什么使用任务制

图像生成具有以下特点，决定了不能设计为简单的同步 API（请求 → 等待 → 返回图片）：

1. **耗时长**：AI 模型生成图像通常需要数秒到数十秒，HTTP 请求不宜长时间挂起。
2. **可能失败**：模型服务不可用、Prompt 被拒绝、生成质量不达标等异常需要重试，而非直接抛出 500 错误。
3. **需要状态追踪**：用户提交生成请求后应能查询进度，而非陷入"提交后不知道在不在处理"的黑盒体验。
4. **支持重试**：失败的任务应能重新触发，而非要求用户重新提交完整请求。

因此，引入 **GenerationTask** 作为生成过程的载体：

```
用户提交需求 → 创建 GenerationTask (status=pending)
                   ↓
            Workflow 拾取任务 (status=running)
                   ↓
          ┌─ 生成成功 → (status=succeeded, 关联 Asset)
          │
          └─ 生成失败 → (status=failed, 记录错误, 支持重试)
```

任务状态枚举：`pending` → `running` → `succeeded` / `failed` / `cancelled`。前端通过轮询或 WebSocket 订阅任务状态变更。

## 5. 为什么使用工作流制

素材生成并非一次模型调用即可完成，而是包含多个独立步骤的流水线：

```
用户需求文本
   │
   ▼
[1] 需求解析 (parse_requirement_step)
   自然语言 → 结构化参数（素材类型、尺寸、内容关键词）
   │
   ▼
[2] Prompt 构造 (build_prompt_step)
   结构化参数 + 项目风格 → 图像模型 Prompt
   │
   ▼
[3] 图像生成 (generate_image_step)
   Prompt → 调用模型 → 原始图像数据
   │
   ▼
[4] 后处理 (post_process_step)
   裁剪、缩放、透明背景处理、格式统一
   │
   ▼
[5] 质量检查 (quality_check_step)
   尺寸校验、透明度校验、风格一致性评估
   │
   ▼
[6] 文件保存 (save_asset_step)
   写入磁盘、创建 Asset 数据库记录、更新 GenerationTask 状态
```

每步独立封装为一个 Step，由 Workflow 编排执行。优势：

- **可观测**：每个步骤的执行状态和耗时独立记录，便于定位瓶颈。
- **可替换**：任何步骤可独立更换实现（如将需求解析从 LLM 调用改为规则匹配）。
- **可跳过/可重试**：根据配置跳过某些步骤（如不需要后处理），或在某步骤失败时只重试该步骤。
- **可测试**：每个 Step 可独立单元测试，不依赖完整流程。

## 6. 后续扩展点

当前架构为后续扩展预留了清晰的接入点，以下扩展均无需大幅重构现有代码：

| 扩展内容 | 接入方式 | 影响范围 |
|----------|----------|----------|
| 真实图像生成模型 | 实现 `ImageGeneratorClient` 新子类，替换 `image_generator.py` 中的客户端注入 | 仅 AI 层 |
| Redis / Celery / RQ 异步队列 | 将 Workflow 触发改为入队操作，增加 Worker 进程消费队列 | Workflow 层 + 配置 |
| MySQL | 替换 SQLite 连接字符串，SQLAlchemy 自动适配 | 仅 config / 数据库连接 |
| MinIO / S3 对象存储 | 实现 `object_storage.py` 中的 S3 后端，通过依赖注入切换 | 仅 Storage 层 |
| LangGraph 工作流 | 将 `asset_generation_workflow.py` 中的步骤编排迁移至 LangGraph 图定义 | 仅 Workflow 层 |
| Unity / Godot 导出 | 在 `export_service.py` 和 `ExportPackage` 模块中增加引擎专用导出逻辑 | Service + Storage 层 |
| 批量生成 | 在 API/Service 层增加批量创建任务的接口，Workflow 层并行处理 | API + Service + Workflow |
| Sprite Sheet 拼接 | 在 `post_process_step.py` 增加 Sprite Sheet 拼接子步骤，不影响其他步骤 | Workflow/steps + AI 层 |

分层架构保证：每层的内部变化不破坏相邻层的接口契约，从而使系统在 MVP 阶段可以保持轻量（单机、同步、SQLite、本地文件系统），而后续向生产级架构演进时无需推倒重写。
