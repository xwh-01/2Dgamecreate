# AI 2D 游戏素材生成工具 - 素材生成工作流

## 1. 工作流总览

素材生成是一个标准化的多步骤工作流，**不是** prompt → image 的单步调用。完整链路如下：

```
用户请求 (API)
     │
     ▼
创建 GenerationTask (status=pending)
     │
     ▼
[Step 1] 需求解析 ─── 自然语言 → 结构化参数
     │
     ▼
[Step 2] Prompt 构造 ─── 结构化参数 + 风格规则 → 最终 Prompt
     │
     ▼
[Step 3] 图像生成 ─── Prompt → 调用 AI 模型 → 原始图像
     │
     ▼
[Step 4] 后处理 ─── 裁剪 / 缩放 / 透明背景 / 格式统一
     │
     ▼
[Step 5] 质量检查 ─── 尺寸 / 透明度 / 文件完整性
     │
     ▼
[Step 6] 文件保存 ─── 写入磁盘，按项目分类目录
     │
     ▼
[Step 7] 元数据保存 ─── Asset 记录写入数据库
     │
     ▼
[Step 8] 状态更新 ─── GenerationTask → succeeded
     │
     ▼
返回结果 (API Response / 轮询通知)
```

每个步骤独立封装为一个 Step 对象，由 `AssetGenerationWorkflow` 统一编排调用。步骤之间通过上下文对象传递数据，新增或删除步骤不影响其他步骤。

## 2. 创建生成任务

API 收到用户生成请求后，**不直接开始生成图片**，而是先创建一条 `GenerationTask` 记录：

1. 校验请求参数（project_id 是否存在、asset_type 是否合法、尺寸是否在支持范围内）。
2. 创建任务记录，状态为 `pending`。
3. 保存用户原始输入 (`user_input`) 和请求参数。
4. 返回任务 ID 给前端，前端通过轮询或 WebSocket 获取任务进度。

**为什么不直接同步生成？**

- 图像生成耗时不可控（数秒到数十秒），HTTP 请求不宜长时间挂起。
- 前端需要展示进度（"需求解析中..."、"图像生成中..."、"后处理中..."）。
- 失败需要支持重试，而非每次重新提交完整请求。

## 3. 需求解析 (Step 1: parse_requirement_step)

`RequirementParser` 将用户的自然语言输入和 `extra_params` 转换为结构化需求对象。

**输入示例**：

```
user_input: "生成一个像素风骑士角色，32×32，面朝右边，白色背景"
extra_params: { asset_type: "character", size: "32x32" }
```

**输出 - 结构化需求**：

| 字段 | 值 | 来源 |
|------|------|------|
| `asset_type` | `character` | extra_params 直接指定 |
| `subject` | `"骑士"` | 从 user_input 提取 |
| `style_hint` | `"像素风"` | 从 user_input 提取 |
| `size` | `"32x32"` | extra_params 直接指定 |
| `direction` | `"right"` | 从 user_input 提取（"面朝右边"） |
| `background` | `"white"` | 从 user_input 提取，用于后处理背景移除 |
| `usage` | `"game_sprite"` | 默认，表示用于游戏 Sprite |

**设计原则**：

- `RequirementParser` 是接口抽象，不绑定具体实现。MVP 阶段可用 LLM 调用实现（将自然语言转为 JSON），后续可替换为规则匹配或更轻量的模型。
- 解析逻辑应遵循"先取 extra_params 的显式值，再从自然语言中补全缺失字段"的优先级。
- 解析结果应包含所有下游步骤所需的信息，避免后续步骤再解析原始文本。

## 4. Prompt 构造 (Step 2: build_prompt_step)

`PromptBuilder` 将多个来源的信息组合为发送给图像模型的最终 Prompt。

**组合来源**：

```
Base Prompt          ←  用户描述（subject + 修饰词）
+ Asset Type Rules   ←  素材类型专用规则（如角色需要四朝向、道具需要物品展示角度）
+ Style Profile Rules ←  项目风格约束（art_style、color_palette、outline_style）
+ Technical Rules    ←  技术约束（像素尺寸、透明背景要求、边缘干净）
+ Engine Compatibility ←  引擎兼容性规则（锚点居中、无需阴影、纯色填充）
+ Negative Prompt    ←  反向提示词（排除项：blurry、realistic、gradient、3D 等）
```

**Prompt 结构（逻辑分组，非实际拼接顺序）**：

| 分组 | 内容示例 | 来源 |
|------|----------|------|
| Base | `"a pixel art knight character, front view, facing right"` | 需求解析结果 |
| Asset Type | `"full body character sprite, game asset, suitable for RPG"` | asset_type 规则映射 |
| Style | `"pixel art style, 32x32 resolution, clean edges, solid color fill, limited palette"` | StyleProfile |
| Technical | `"transparent background, centered, 32x32 canvas, no anti-aliasing"` | 尺寸 + 格式规则 |
| Engine | `"pixel perfect, no shadow, no outline bleeding, isolated sprite"` | 引擎兼容规则 |
| Negative | `"blurry, realistic, 3D render, shading, gradient, photo, complex background, watermark"` | StyleProfile + 全局规则 |

**设计原则**：

- `PromptBuilder` 不关心下游用的是什么模型，只负责产出文本。模型客户端接收到 Prompt 后自行适配格式。
- 各组规则独立管理，新增素材类型或画风时只需追加对应的规则模板，无需修改 PromptBuilder 核心逻辑。
- Negative Prompt 由 StyleProfile 的 `negative_prompt_rules` 和全局默认禁用词合并而成，用户不可跳过。

## 5. 图像生成 (Step 3: generate_image_step)

`generate_image_step` 不直接依赖任何具体模型 SDK。它依赖 `ImageGenerator` 接口，而 `ImageGenerator` 内部通过 `ImageGeneratorClient` 抽象与具体模型交互。

```
generate_image_step
        │
        ▼
   ImageGenerator  (编排：选模型、调客户端、处理重试)
        │
        ▼
   ImageGeneratorClient  (抽象接口)
        │
   ┌────┼────────────┬──────────────┐
   │    │            │              │
   ▼    ▼            ▼              ▼
 DALL·E  Stability  ComfyUI    Local SD
 Client  Client     Client     Client
```

**ImageGeneratorClient 接口职责**：

- 接收标准化 Prompt（文本）
- 调用具体模型 API
- 返回原始图像字节流
- 处理模型级错误（认证失败、内容过滤、配额耗尽）

**ImageGenerator 职责**：

- 根据任务参数选择模型（MVP 阶段直接使用配置指定的默认模型）。
- 调用 `ImageGeneratorClient` 生成图像。
- 实现重试策略（网络超时 → 重试；内容过滤 → 重试并换种子；配额耗尽 → 抛出明确错误）。
- 将原始图像字节流传给下一步。

**设计原则**：

- 新增模型只需实现 `ImageGeneratorClient` 接口并注册到 `ModelProvider`，无需修改工作流或 Step 代码。
- 模型选择和路由逻辑集中在 `ModelProvider`，后续可扩展为按 asset_type、风格、成本等维度自动选模型。

## 6. 后处理 (Step 4: post_process_step)

后处理步骤将 AI 生成的原始图像转换为符合游戏引擎规范的标准化素材。

| 处理项 | 说明 | 实现方式 |
|--------|------|----------|
| 尺寸调整 | 将图像缩放到目标尺寸（如 `32x32`），保持宽高比，不足部分自动填充 | Pillow / OpenCV |
| 透明背景处理 | 检测并移除背景色（如白色/黑色背景转为透明），保留主体内容 | 颜色阈值 + Alpha 通道写入 |
| 居中裁剪 | 确保主体位于画布中心，避免 Sprite 在引擎中偏移 | 边界检测 + 中心对齐 |
| 格式统一 | 统一输出为 PNG 格式，保留 Alpha 通道 | Pillow 格式转换 |
| 边缘清理 | 移除 AI 常产的边缘杂色 / 噪声像素 | 边缘平滑算法 |

**关键约束**：

- 后处理必须保证图像的 `transparent` 属性可被准确判断。如果背景移除失败或素材本身就不需要透明背景，应如实标记。
- 后处理步骤应返回处理后的图像字节流和一组成处理指标（原始尺寸、裁剪边界、是否成功透明化等），供下一步质量检查参考。

## 7. 质量检查 (Step 5: quality_check_step)

`QualityChecker` 对后处理完成的图像进行质量评估。MVP 阶段至少检查以下维度：

| 检查项 | 规则 | 失败处理 |
|--------|------|----------|
| 图片是否存在 | 图像字节流不为空，可解析为有效图像 | 标记失败，无重试意义 |
| 是否为 PNG | 文件头校验，格式为 PNG | 标记失败，回退到后处理重试格式转换 |
| 尺寸是否符合 | 图像像素宽高与请求的目标尺寸一致（允许 ±2px 容差） | 标记失败，回退到后处理重试缩放 |
| 是否有 Alpha 通道 | 检查图像模式是否包含 Alpha（RGBA 模式） | 若素材类型要求透明则标记失败；若不要求透明则警告通过 |
| 文件大小是否合理 | 文件大小在合理范围内（不宜为 0 字节，不宜超过上限如 10MB） | 文件为 0 → 失败；文件过大 → 通过但有日志告警 |

**扩展性**：

后续可接入更复杂的质量检查维度：CLIP 评分（Prompt 与图像匹配度）、风格一致性评分（与项目已有素材对比）、分辨率自动提升建议等。新增检查维度只需在 `QualityChecker` 中追加检查规则，不影响其他步骤。

**质量检查结果**：

- **全部通过** → 流程继续。
- **部分失败但有重试价值** → 抛出特定异常，由 Workflow 判定是否回退到后处理步骤重试。
- **彻底失败** → 抛出不可重试异常，任务标记 `failed`。

## 8. 素材保存 (Step 6: save_asset_step)

素材文件按项目、类型分类存储，**禁止将所有图片直接扔到 `generated_assets/` 根目录**。

**目录结构规范**：

```
generated_assets/
  project_{project_id}/
    characters/          ← 角色素材
    props/               ← 道具素材
    tiles/               ← 地图 Tile
    ui_icons/            ← UI 图标
    exports/             ← 导出包文件
```

每个素材文件的命名规范：

```
{asset_name}_{asset_type}_{size}_{timestamp}.png
```

例如：`knight_character_32x32_20260523140000.png`

**保存流程**：

1. `PathBuilder` 根据 project_id 和 asset_type 构造完整存储路径。
2. `FileStorage` 检查目录是否存在，不存在则创建。
3. 将图像字节流写入目标路径。
4. 可选：生成缩略图（如 128×128），存储在同目录 `thumbnails/` 下。
5. 返回文件相对路径，传递给元数据保存步骤。

**依赖抽象**：

`save_asset_step` 依赖 `FileStorage` 接口而非具体实现。MVP 阶段使用本地磁盘存储，后续切换到 MinIO / S3 只需替换 `FileStorage` 实现，无需修改 Step 代码。

## 9. 元数据保存 (Step 7: 附加操作)

文件保存成功后，创建 `Asset` 数据库记录，记录以下信息：

| 字段 | 来源 |
|------|------|
| `project_id` | 从 GenerationTask 获取 |
| `task_id` | 当前 GenerationTask ID |
| `name` | 命名工具 (`Naming`) 生成 |
| `asset_type` | 从需求解析结果获取 |
| `file_path` | 从 save_asset_step 返回 |
| `preview_url` | 缩略图路径（如有） |
| `width` | 从后处理后的图像属性获取 |
| `height` | 从后处理后的图像属性获取 |
| `format` | 固定 `"png"` |
| `transparent` | 从后处理结果/质量检查结果获取 |
| `metadata` | JSON，包含原始 prompt、模型名称、后处理参数等 |

此步骤通过 `AssetService` → `AssetRepository` 完成数据库写入，不与文件存储逻辑耦合。

## 10. 任务状态更新 (Step 8: 流程收尾)

所有步骤成功执行完毕后，将 `GenerationTask` 状态更新为 `succeeded`，并回写 `result_asset_id`。

**完整状态流转**：

```
        创建任务
           │
           ▼
       ┌───────┐
       │pending│──── 用户取消 ────► ┌─────────┐
       └───┬───┘                    │cancelled│ (终态)
           │                        └─────────┘
     工作流启动
           │
           ▼
       ┌───────┐
       │running│── 全部步骤成功 ──► ┌──────────┐
       └───┬───┘                    │succeeded │ (终态，关联 Asset)
           │                        └──────────┘
      任一步骤失败
           │
           ▼
       ┌──────┐
       │failed│── 用户重试 ──► pending
       └──────┘
```

**状态更新时机**：

- `pending` → `running`：Workflow 开始执行 Step 1 时更新。
- `running` → `succeeded`：全部步骤完成且 Asset 记录已创建时更新。
- `running` → `failed`：任一步骤抛出不可重试异常时更新。
- `pending` → `cancelled`：用户通过 API 取消时更新。

## 11. 异常处理

工作流中的每个步骤都可能失败。统一的异常处理机制确保系统不会进入不一致状态。

**异常分类**：

| 异常类型 | 含义 | 处理策略 |
|----------|------|----------|
| 可重试异常 | 临时性问题（网络超时、模型服务暂时不可用） | 记录日志 → 等待后重试当前步骤（最多 N 次） |
| 不可重试异常 | 永久性问题（Prompt 被永久拒绝、解析结果格式错误） | 记录 `error_message` → 任务标记 `failed` |
| 业务校验异常 | 质量检查不通过 | 回退到后处理步骤重试（最多 M 次），耗尽后标记 `failed` |

**失败记录**：

任务失败时，`GenerationTask` 必须记录：

1. `status` 更新为 `failed`。
2. `error_message` 写入人类可读的错误描述（如 `"Quality check failed: output size 30x28 does not match requested 32x32"`）。
3. `updated_at` 更新为当前时间。

**失败后的恢复路径**：

- 用户查看失败原因 → 修改 `user_input` → 触发重试（创建新任务或重置当前任务）。
- Workflow 保持幂等性：重试时从断点步骤继续（需各 Step 支持基于上下文的恢复），或从 Step 1 重新执行（MVP 策略，简单可靠）。

**全局约束**：

- 任何步骤抛出的异常必须被 Workflow 层捕获，不允许未处理的异常导致任务永远卡在 `running` 状态。
- 异常信息不应直接暴露给前端用户（如堆栈跟踪），应转换为用户可理解的提示。
- 所有异常应写日志（含 task_id、step_name、timestamp），便于排查。
