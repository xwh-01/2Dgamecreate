# AI 2D 游戏素材生成工具 - 数据模型设计

本文档描述系统的核心实体及其关系，属于概念模型层，不涉及具体数据库实现。

---

## 1. Project

Project 表示一个游戏项目空间。同一项目下的所有素材共享风格配置，确保视觉一致性。

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `id` | UUID / int | 是 | 项目唯一标识，主键 |
| `name` | string | 是 | 项目名称，用户设定，用于界面展示和素材默认命名前缀 |
| `description` | string | 否 | 项目简要描述，记录游戏类型、世界观等上下文信息，辅助 AI 理解素材需求 |
| `style_profile_id` | FK → StyleProfile | 否 | 关联的风格配置，一对多关系（一个 StyleProfile 可被多个 Project 使用） |
| `created_at` | datetime | 是 | 项目创建时间 |
| `updated_at` | datetime | 是 | 最后修改时间 |

**设计说明**：

- `name` 和 `description` 共同为 AI 提供项目上下文。例如"像素风地牢探险游戏"的描述会影响 Prompt 生成策略。
- `style_profile_id` 允许跨项目共享同一风格（如开发系列作品时），也允许项目暂不绑定风格（后续再配置）。
- `created_at` / `updated_at` 用于排序、过滤和审计。

---

## 2. StyleProfile

StyleProfile 保存项目级视觉风格约束。所有素材生成时必须遵守此配置，从根源上解决"多次生成素材风格不统一"的问题。

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `id` | UUID / int | 是 | 风格配置唯一标识 |
| `project_id` | FK → Project | 是 | 所属项目，一对多（一个项目可有多版风格草稿，当前绑定一个启用版本） |
| `art_style` | enum | 是 | 画风枚举值：`pixel` / `flat` / `hand_drawn` / `vector` / `realistic` 等。强制约束生成模型输出风格 |
| `view_type` | enum | 是 | 视角枚举值：`top_down` / `side_scroller` / `isometric` / `first_person` 等。约束素材朝向和透视 |
| `color_palette` | string / JSON | 否 | 色彩方案，可存储色板 HEX 列表或色系描述文本。用于引导模型输出目标色调 |
| `outline_style` | string | 否 | 描边风格描述，如"黑色硬边 2px"、"无边线"、"柔和内阴影"。影响素材边界的视觉表现 |
| `default_size` | string | 否 | 项目默认素材尺寸，如 `"32x32"`、`"64x64"`。当生成请求未指定尺寸时以此为默认值 |
| `prompt_rules` | string / JSON | 是 | 正向 Prompt 约束规则。自动追加到每次生成的 Prompt 中，如 `"pixel art, clean edges, solid color fill, no gradient"` |
| `negative_prompt_rules` | string / JSON | 是 | 反向 Prompt 约束规则。自动追加到每次生成的反向词中，如 `"blurry, realistic, 3D render, shading, gradient"` |
| `created_at` | datetime | 是 | 创建时间 |
| `updated_at` | datetime | 是 | 最后修改时间 |

**设计说明**：

- `prompt_rules` 和 `negative_prompt_rules` 是保证风格一致性的核心字段。无论用户提交什么素材需求，这些规则都会自动注入到 Prompt 中，无需用户每次手动添加。例如用户只需描述"骑士"，系统自动追加 `"pixel art, 64x64, clean edges"`。
- `art_style` 和 `view_type` 使用枚举约束，避免用户自由输入造成风格漂移，也为模型路由提供依据（不同风格走不同模型或参数）。
- `color_palette` 和 `outline_style` 是选填的高级约束，MVP 阶段可暂不强制，但数据结构预留以支持后续精细化控制。
- `default_size` 减少用户重复输入尺寸参数，提升生成效率。

---

## 3. GenerationTask

GenerationTask 表示一次素材生成请求的完整生命周期记录。它承载从用户提交到素材产出的全部中间状态和数据。

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `id` | UUID / int | 是 | 任务唯一标识 |
| `project_id` | FK → Project | 是 | 所属项目 |
| `asset_type` | enum | 是 | 请求生成的素材类型：`character` / `prop` / `tile` / `ui_icon` 等 |
| `status` | enum | 是 | 任务状态，枚举值见下方状态表 |
| `user_input` | string | 是 | 用户原始自然语言输入，保留用于调试和重试 |
| `parsed_requirement` | JSON | 否 | 需求解析结果，结构化描述（关键词、对应元素、数量等），由需求解析步骤填充 |
| `final_prompt` | string | 否 | 最终发送给图像模型的完整 Prompt（含风格规则注入后的），由 Prompt 构造步骤填充 |
| `model_name` | string | 否 | 实际调用的模型名称（如 `"stable-diffusion-xl"`、`"dall-e-3"`），便于问题追溯和成本统计 |
| `size` | string | 否 | 请求的目标尺寸，如 `"128x128"` |
| `error_message` | string | 否 | 失败时的错误信息（模型拒绝、超时、内容不安全等），用于用户提示和调试 |
| `result_asset_id` | FK → Asset | 否 | 生成成功后的产出 Asset，一对多（未来支持一次任务生成多张变体） |
| `created_at` | datetime | 是 | 任务创建时间（用户提交时刻） |
| `updated_at` | datetime | 是 | 最后状态变更时间 |

**任务状态枚举**：

| 状态值 | 含义 |
|--------|------|
| `pending` | 任务已创建，等待处理 |
| `running` | 工作流正在执行（需求解析 → 图像生成中） |
| `succeeded` | 生成成功，Asset 已创建 |
| `failed` | 生成失败，`error_message` 中记录原因 |
| `cancelled` | 用户或系统取消了任务 |

**设计说明**：

- `user_input` 保留原始输入是关键的：当生成结果不理想时，用户可以修改原始输入并重新提交，而非从零开始。同时也为后续的 Prompt 优化和 A/B 测试提供数据基础。
- `parsed_requirement` 和 `final_prompt` 分别记录工作流中间产物和最终产物。两者分开存储，便于定位问题是出在需求解析阶段还是 Prompt 构造阶段。
- `model_name` 记录实际调用的模型，是后续实现成本统计和多模型路由的基础数据。
- `error_message` 存储人类可读的错误描述，而非原始异常堆栈，避免泄露内部细节给用户。
- `result_asset_id` 在 MVP 阶段为单素材关联，但设计为一对多预留，后续一次任务生成多个变体时无需改动表结构。

---

## 4. Asset

Asset 表示已经生成并持久化保存的游戏素材。它是系统的核心产出物，不是临时图片。

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `id` | UUID / int | 是 | 素材唯一标识 |
| `project_id` | FK → Project | 是 | 所属项目 |
| `task_id` | FK → GenerationTask | 是 | 关联的生成任务，用于追溯生成来源 |
| `name` | string | 是 | 素材显示名称，如 `"knight_idle_01"`，由系统按命名规范自动生成或用户自定义 |
| `asset_type` | enum | 是 | 素材类型：`character` / `prop` / `tile` / `ui_icon` |
| `file_path` | string | 是 | 素材文件在存储中的相对路径，如 `"projects/abc123/assets/knight_idle_01.png"`，用于文件读取和下载 |
| `preview_url` | string | 否 | 缩略图或预览图 URL，供列表展示使用，可指向更低分辨率的缓存版本 |
| `width` | int | 是 | 图像像素宽度，元数据供引擎导入时参考 |
| `height` | int | 是 | 图像像素高度 |
| `format` | string | 是 | 文件格式，默认 `"png"`，可为 `"webp"` 等 |
| `transparent` | bool | 是 | 是否包含透明通道，影响游戏引擎中的渲染设置（如 Sprite 的 Alpha 模式） |
| `metadata` | JSON | 否 | 扩展元数据，可存储 anchor_point、frame_count、tags 等引擎和工具所需信息 |
| `created_at` | datetime | 是 | 素材生成时间 |
| `updated_at` | datetime | 是 | 最后修改时间 |

**设计说明**：

- `transparent` 是游戏素材的核心标志之一。普通 AI 生成图通常不带透明背景，本系统的后处理步骤会去除背景并设置此字段为 `true`。引擎导入工具可据此自动配置正确的 Alpha 模式。
- `width` 和 `height` 独立于文件本身而显式存储，避免每次读取文件头获取尺寸，提升列表加载性能。
- `file_path` 使用相对路径而非绝对路径，便于后续从本地存储迁移到对象存储（只需更换路径解析逻辑）。
- `metadata` 是 JSON 扩展字段，避免频繁修改核心表结构。后续新增引擎相关属性（如 Sprite Pivot、Pixels Per Unit）可直接写入此字段。
- `task_id` 关联回 GenerationTask，用户可查看"这个素材是哪个请求生成的，当时用的什么 Prompt"，形成可追溯链条。

---

## 5. ExportPackage

ExportPackage 表示一次素材导出打包操作的结果。

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `id` | UUID / int | 是 | 导出包唯一标识 |
| `project_id` | FK → Project | 是 | 所属项目 |
| `status` | enum | 是 | 导出状态：`pending` / `processing` / `succeeded` / `failed` |
| `file_path` | string | 否 | 导出后的 ZIP 包或目录路径，成功后填充 |
| `engine_type` | string | 否 | 目标引擎类型：`"unity"` / `"godot"` / `"generic"`。不同引擎导出目录结构不同 |
| `created_at` | datetime | 是 | 导出任务创建时间 |
| `updated_at` | datetime | 是 | 最后状态更新时间 |

**设计说明**：

- `engine_type` 预留了后续对接不同游戏引擎的扩展点。`"generic"` 表示标准目录结构导出。
- MVP 阶段导出操作可能为同步完成，但字段设计为异步（含 `status` 枚举）以支持后续大批量导出的后台处理。
- `file_path` 在导出完成后填充，用户通过此路径下载。

---

## 6. 实体关系

```
Project (1) ──────── (0..1) StyleProfile
   │
   ├─ (1) ──────── (N) ──── GenerationTask
   │                            │
   │                            └─ (1) ──── (1..N) ──── Asset
   │
   ├─ (1) ──────── (N) ──── Asset
   │
   └─ (1) ──────── (N) ──── ExportPackage
```

关系说明：

| 关系 | 基数 | 说明 |
|------|------|------|
| Project → StyleProfile | 1 : 0..1 | 一个项目绑定一个启用的风格配置（可选）。StyleProfile 可被多个 Project 引用（如系列游戏共享风格） |
| Project → GenerationTask | 1 : N | 一个项目包含多次生成请求 |
| GenerationTask → Asset | 1 : 1..N | 一次成功的生成任务产出一个 Asset（MVP），未来可产出多个变体 |
| Project → Asset | 1 : N | 一个项目包含多个素材，提供快速按项目查询素材列表的能力 |
| Project → ExportPackage | 1 : N | 一个项目可多次导出打包 |

**为什么 Asset 同时关联 Project 和 GenerationTask**：同时持有两个外键是为了查询效率。按项目查询素材列表（Project → Asset）是最常用的操作，直接关联避免通过 GenerationTask 做 JOIN，提升查询性能。

---

## 7. 状态流转

GenerationTask 的完整状态流转：

```
       ┌──────────┐
       │  pending │  初始状态，用户刚提交生成请求
       └────┬─────┘
            │
     ┌──────┼──────────┐
     │      │           │
     ▼      ▼           ▼
┌────────┐    ┌──────────┐
│running │    │cancelled │  用户在 pending 状态可直接取消
└───┬────┘    └──────────┘
    │
    ├─────────┐
    │         │
    ▼         ▼
┌──────────┐ ┌────────┐
│succeeded │ │ failed │
│          │ │        │──── 用户可重试 → pending
└──────────┘ └────────┘
```

合法状态转换：

| 当前状态 | 可转换为 | 触发条件 |
|----------|----------|----------|
| `pending` | `running` | 工作流拾取任务开始处理 |
| `pending` | `cancelled` | 用户主动取消 |
| `running` | `succeeded` | 所有工作流步骤执行成功 |
| `running` | `failed` | 任一步骤失败且重试耗尽 |
| `failed` | `pending` | 用户触发重试，重置为待处理状态 |
| `failed` | `cancelled` | 用户放弃该任务 |
| `cancelled` | — | 终态，不可恢复 |

**不允许**的状态转换（由业务层逻辑保证）：

- `pending` → `succeeded`（必须经过 `running`）
- `succeeded` → 任何状态（终态，不可更改）
- `running` → `pending`（不可回退，只能失败后重建）
- `cancelled` → 任何状态（终态，不可恢复）
