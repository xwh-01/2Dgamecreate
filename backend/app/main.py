# FastAPI application entry point
import os

for key in ("HTTP_PROXY", "HTTPS_PROXY", "http_proxy", "https_proxy", "ALL_PROXY", "all_proxy"):
    os.environ.pop(key, None)
os.environ.setdefault("NO_PROXY", "*")

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from .api.router import router as api_router

app = FastAPI(title="Game Asset Generator", version="0.1.0")
app.include_router(api_router)

INDEX_HTML = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AI 2D Game Asset Generator</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:system-ui,-apple-system,sans-serif;background:#0b1120;color:#e2e8f0;min-height:100vh;-webkit-font-smoothing:antialiased}
h1{text-align:center;padding:32px 20px 2px;color:#e94560;font-size:1.5rem;font-weight:800;letter-spacing:-.3px}
.subtitle{text-align:center;color:#94a3b8;font-size:.75rem;margin-bottom:6px}
.guide-bar{max-width:1280px;margin:0 auto 18px;padding:0 24px;display:flex;justify-content:center}
.guide-steps{display:flex;gap:2px;align-items:center;font-size:.65rem;color:#64748b}
.guide-step{padding:3px 10px;border-radius:12px;background:#111827;white-space:nowrap}
.guide-arrow{color:#334155;margin:0 2px}
.main-layout{max-width:1280px;margin:0 auto;padding:0 24px 60px;display:grid;grid-template-columns:300px 1fr;gap:16px;align-items:start}
@media(max-width:860px){.main-layout{grid-template-columns:1fr}}

.panel{background:#111827;border-radius:10px;border:1px solid #1e293b;overflow:hidden}
.panel-header{font-size:.82rem;font-weight:700;color:#f1f5f9;padding:12px 16px;border-bottom:1px solid #1e293b;background:#0f172a;display:flex;align-items:center;gap:8px}
.panel-body{padding:14px 16px}
.panel-body.sm{padding:8px 12px}

label{display:block;margin-bottom:3px;font-size:.7rem;color:#94a3b8;font-weight:500}
.field-hint{font-size:.62rem;color:#64748b;margin-bottom:5px;line-height:1.4}
input,select,textarea{width:100%;padding:8px 12px;border-radius:7px;border:1px solid #1e293b;background:#0f172a;color:#e2e8f0;font-size:.78rem;font-family:inherit;transition:border-color .15s}
input:focus,select:focus,textarea:focus{outline:none;border-color:#e94560;box-shadow:0 0 0 3px rgba(233,69,96,.1)}
textarea{resize:vertical;min-height:52px}
button{padding:8px 18px;border-radius:7px;border:none;cursor:pointer;font-size:.78rem;font-weight:600;transition:all .12s;font-family:inherit}
button:disabled{opacity:.4;cursor:not-allowed;pointer-events:none}
.btn-primary{background:#e94560;color:#fff}.btn-primary:hover:not(:disabled){background:#d63850}
.btn-secondary{background:#1e293b;color:#cbd5e1;border:1px solid #334155}.btn-secondary:hover:not(:disabled){background:#334155}
.btn-success{background:#16a34a;color:#fff}.btn-success:hover:not(:disabled){background:#15803d}
.btn-danger{background:#dc2626;color:#fff}.btn-danger:hover:not(:disabled){background:#b91c1c}
.btn-outline{background:transparent;color:#94a3b8;border:1px solid #334155}.btn-outline:hover:not(:disabled){background:#1e293b;color:#e2e8f0}
.btn-ghost{background:transparent;color:#60a5fa;border:none;padding:3px 6px;font-size:.65rem;cursor:pointer}.btn-ghost:hover{text-decoration:underline}
.btn-sm{padding:5px 12px;font-size:.7rem}
.btn-xs{padding:3px 8px;font-size:.65rem}
.btn-xl{padding:12px 24px;font-size:.82rem;width:100%}

.msg{padding:10px 14px;border-radius:7px;margin-bottom:8px;font-size:.72rem;line-height:1.5;word-break:break-word}
.msg-success{background:#052e16;border:1px solid #166534;color:#4ade80}
.msg-error{background:#2d1111;border:1px solid #7f1d1d;color:#fca5a5}
.msg-info{background:#0c1929;border:1px solid #1e3a5f;color:#93c5fd}
.msg-warning{background:#2d2300;border:1px solid #713f12;color:#fbbf24}

.type-bar{display:flex;gap:6px;flex-wrap:wrap;margin-bottom:14px}
.type-btn{padding:6px 14px;border-radius:8px;font-size:.7rem;font-weight:600;cursor:pointer;border:2px solid #1e293b;background:#0f172a;color:#94a3b8;transition:all .12s}
.type-btn:hover{border-color:#475569;color:#e2e8f0}
.type-btn.active{background:#e94560;color:#fff;border-color:#e94560}

.prompt-detail{margin-top:10px;border:1px solid #1e293b;border-radius:8px;overflow:hidden}
.prompt-detail-header{display:flex;align-items:center;gap:6px;padding:8px 12px;background:#0f172a;cursor:pointer;font-size:.67rem;color:#94a3b8;user-select:none;border-bottom:1px solid #1e293b}
.prompt-detail-header:hover{color:#e2e8f0}
.prompt-detail-header .pd-arrow{transition:transform .2s;font-size:.6rem}
.prompt-detail-header.collapsed .pd-arrow{transform:rotate(-90deg)}
.prompt-detail-body{padding:8px 12px;font-size:.62rem;line-height:1.6}
.pd-section{margin-bottom:8px}
.pd-section-title{font-size:.6rem;color:#e94560;font-weight:600;margin-bottom:3px;text-transform:uppercase;letter-spacing:.5px}
.pd-item{display:inline-block;padding:2px 6px;margin:1px 3px;border-radius:4px;font-size:.57rem;background:#0f172a;border:1px solid #1e293b;color:#94a3b8}
.pd-item.active{background:#0f172a;border-color:#334155;color:#e2e8f0}
.pd-item.warn{background:#2d2300;border-color:#713f12;color:#fbbf24}
.pd-text{color:#e2e8f0;font-size:.6rem;word-break:break-all}
.pd-muted{color:#64748b;font-size:.58rem;font-style:italic}
.pd-manual-toggle{display:flex;align-items:center;gap:6px;padding:6px 12px;font-size:.63rem;color:#94a3b8;border-top:1px solid #1e293b}
.pd-manual-area{display:none;padding:6px 12px}
.pd-manual-area textarea{width:100%;min-height:60px;font-size:.63rem;font-family:monospace}

.progress-bar{margin:8px 0}
.progress-step{display:flex;align-items:center;gap:8px;padding:4px 0;font-size:.68rem;color:#475569;border-left:2px solid #1e293b;padding-left:10px;transition:all .3s}
.progress-step.active{color:#60a5fa;border-left-color:#60a5fa;font-weight:600}
.progress-step.done{color:#4ade80;border-left-color:#16a34a}
.progress-step .step-spinner{width:12px;height:12px;border:2px solid #60a5fa;border-top-color:transparent;border-radius:50%;animation:spin .6s linear infinite;flex-shrink:0}
@keyframes spin{to{transform:rotate(360deg)}}

.preview-img{max-width:100%;max-height:220px;object-fit:contain;background-image:repeating-conic-gradient(#0b1120 0 25%,#111827 0 50%);background-size:16px 16px;border-radius:7px;border:1px solid #1e293b}

.filter-bar{display:flex;gap:6px;align-items:center;flex-wrap:wrap;margin-bottom:12px}
.filter-types{display:flex;gap:3px;flex-wrap:wrap}
.filter-btn{padding:3px 10px;border-radius:12px;border:1px solid #1e293b;background:transparent;color:#94a3b8;font-size:.63rem;cursor:pointer;transition:all .12s}
.filter-btn:hover{color:#e2e8f0;border-color:#475569}
.filter-btn.active{background:#3b82f6;color:#fff;border-color:#3b82f6}
.search-input{flex:1;min-width:120px;max-width:220px}

.asset-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(145px,1fr));gap:10px;margin-top:6px}
.asset-card{background:#0f172a;border-radius:8px;overflow:hidden;border:1px solid #1e293b;transition:border-color .15s,transform .12s}
.asset-card:hover{border-color:#475569;transform:translateY(-2px)}
.asset-card-img{width:100%;aspect-ratio:1;display:flex;align-items:center;justify-content:center;background-image:repeating-conic-gradient(#0b1120 0 25%,#111827 0 50%);background-size:10px 10px;padding:8px;cursor:pointer}
.asset-card-img img{max-width:100%;max-height:100%;object-fit:contain}
.asset-card-body{padding:7px 9px}
.asset-card-name{font-size:.65rem;font-weight:600;color:#e2e8f0;margin-bottom:3px;word-break:break-all;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.asset-card-type{font-size:.58rem;padding:2px 6px;border-radius:8px;background:#1e293b;color:#94a3b8;display:inline-block;margin-bottom:3px}.asset-card-type.enemy{background:#3b1f1f;color:#fca5a5}
.asset-card-date{font-size:.58rem;color:#64748b;display:block;margin-bottom:5px}
.asset-card-actions{display:flex;gap:2px;flex-wrap:wrap}

.empty-state{text-align:center;padding:40px 20px}
.empty-state .empty-icon{font-size:2.5rem;margin-bottom:10px;opacity:.2}
.empty-state .empty-title{font-size:.85rem;color:#94a3b8;font-weight:600;margin-bottom:4px}
.empty-state .empty-hint{font-size:.7rem;color:#64748b;margin-bottom:14px;line-height:1.4}
.empty-state .empty-actions{display:flex;gap:6px;justify-content:center;flex-wrap:wrap}

.chip-group{margin-bottom:5px}
.chip-group-header{font-size:.6rem;color:#94a3b8;cursor:pointer;padding:3px 0;display:flex;align-items:center;gap:4px;user-select:none}
.chip-group-header:hover{color:#e2e8f0}
.chip-group-header .arrow{transition:transform .2s;display:inline-block}
.chip-group-header.collapsed .arrow{transform:rotate(-90deg)}
.chip-group-body{display:flex;flex-wrap:wrap;gap:3px;padding:4px 0 4px 8px;border-left:2px solid #1e293b;margin-left:2px}
.chip-group-header.collapsed+.chip-group-body{display:none}
.chip{display:inline-block;padding:3px 9px;border-radius:12px;font-size:.6rem;cursor:pointer;border:1px solid #334155;background:#0f172a;color:#94a3b8;transition:all .1s;white-space:nowrap}
.chip:hover{border-color:#60a5fa;color:#e2e8f0}
.chip.active{background:#3b82f6;color:#fff;border-color:#3b82f6}

.template-grid{display:flex;flex-wrap:wrap;gap:5px;margin-top:6px}
.tpl-btn{padding:5px 12px;border-radius:8px;font-size:.65rem;cursor:pointer;border:1px solid #1e293b;background:#0f172a;color:#cbd5e1;transition:all .1s;text-align:left;display:flex;align-items:center;gap:4px}
.tpl-btn:hover{border-color:#e94560;color:#fff;background:#1a1120}
.tpl-btn .tpl-dot{width:6px;height:6px;border-radius:50%;flex-shrink:0}
.tpl-btn.character .tpl-dot{background:#e94560}
.tpl-btn.enemy .tpl-dot{background:#ef4444}
.tpl-btn.item .tpl-dot{background:#f59e0b}
.tpl-btn.tile .tpl-dot{background:#22c55e}
.tpl-btn.ui_icon .tpl-dot{background:#3b82f6}
.tpl-btn.effect .tpl-dot{background:#a855f7}

.example-bar{margin:4px 0 10px;display:flex;gap:4px;flex-wrap:wrap}
.example-btn{padding:3px 10px;font-size:.6rem;background:#0f172a;border:1px solid #334155;color:#94a3b8;border-radius:12px;cursor:pointer;transition:all .1s}
.example-btn:hover{background:#1e293b;color:#e2e8f0;border-color:#475569}

.btn-row{display:flex;gap:8px;margin-top:12px;flex-wrap:wrap}

.stats-text{font-size:.67rem;color:#94a3b8;margin-bottom:6px}
.stats-text strong{color:#e2e8f0}

.inline-tag{display:inline-block;padding:2px 6px;border-radius:4px;font-size:.58rem;background:#1e293b;color:#94a3b8}

.toast{position:fixed;bottom:24px;right:24px;padding:10px 18px;border-radius:8px;font-size:.72rem;z-index:1000;animation:toastIn .3s ease;color:#fff;box-shadow:0 4px 12px rgba(0,0,0,.3)}
.toast-success{background:#16a34a}.toast-error{background:#dc2626}
@keyframes toastIn{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:translateY(0)}}

.no-project-banner{padding:8px 12px;background:rgba(251,191,36,.1);border:1px solid rgba(251,191,36,.3);border-radius:7px;color:#fbbf24;font-size:.7rem;margin-bottom:10px;text-align:center}

.collapse-box{border:1px solid #1e293b;border-radius:7px;overflow:hidden;margin-top:8px}
.collapse-box-header{display:flex;align-items:center;gap:6px;padding:7px 12px;background:#0f172a;cursor:pointer;font-size:.67rem;color:#94a3b8;user-select:none}
.collapse-box-header:hover{color:#e2e8f0}
.collapse-box-header .cb-arrow{transition:transform .2s;font-size:.6rem}
.collapse-box-header.collapsed .cb-arrow{transform:rotate(-90deg)}
.collapse-box-body{padding:8px 12px}
.collapse-box-header.collapsed+.collapse-box-body{display:none}

.result-panel{margin-top:10px}
.result-panel .rp-img{text-align:center;padding:10px;background-image:repeating-conic-gradient(#0b1120 0 25%,#111827 0 50%);background-size:12px 12px;border-radius:7px;margin-bottom:8px}
.result-panel .rp-img img{max-width:100%;max-height:200px;object-fit:contain;border-radius:4px}
.result-panel .rp-meta{display:flex;flex-wrap:wrap;gap:4px;margin-bottom:8px}
.result-panel .rp-tag{display:inline-block;padding:2px 7px;border-radius:4px;font-size:.6rem;background:#1e293b;color:#94a3b8}
.result-panel .rp-section{margin-bottom:8px}
.result-panel .rp-section .rp-label{font-size:.6rem;color:#94a3b8;margin-bottom:2px}
.result-panel .rp-section .rp-text{font-size:.63rem;color:#e2e8f0;word-break:break-all;background:#0f172a;padding:5px 9px;border-radius:5px;line-height:1.4}
.result-panel .rp-section .rp-text.mono{font-family:monospace;font-size:.58rem;max-height:80px;overflow-y:auto}
.result-panel .rp-actions{display:flex;gap:5px;flex-wrap:wrap;margin-top:10px}

.modal-overlay,.detail-overlay{display:none;position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,.85);z-index:999;justify-content:center;align-items:center;padding:20px}
.modal-overlay.active,.detail-overlay.active{display:flex}
.detail-panel{background:#111827;border:1px solid #1e293b;border-radius:10px;max-width:560px;width:100%;max-height:90vh;overflow-y:auto;position:relative}
.detail-close-btn{position:sticky;top:8px;float:right;margin:8px 12px;background:rgba(0,0,0,.6);border:none;color:#94a3b8;font-size:1rem;cursor:pointer;z-index:2;padding:4px 8px;border-radius:4px}.detail-close-btn:hover{color:#e2e8f0}
.detail-img-area{padding:16px;text-align:center;background-image:repeating-conic-gradient(#0b1120 0 25%,#111827 0 50%);background-size:14px 14px;border-bottom:1px solid #1e293b}
.detail-img-area img{max-width:100%;max-height:240px;object-fit:contain;border-radius:4px}
.detail-body{padding:14px 18px}
.detail-body h3{color:#f1f5f9;font-size:.85rem;margin-bottom:10px}
.detail-row{display:flex;justify-content:space-between;padding:5px 0;font-size:.7rem;border-bottom:1px solid #0f172a}
.detail-row .dl{color:#94a3b8;flex-shrink:0;margin-right:12px}
.detail-row .dv{color:#e2e8f0;text-align:right;word-break:break-all;max-width:70%}
.detail-row .dv.mono{font-family:monospace;font-size:.63rem;max-height:100px;overflow-y:auto;background:#0f172a;padding:5px 8px;border-radius:4px;text-align:left}
.detail-actions{display:flex;gap:5px;flex-wrap:wrap;margin-top:14px;padding-top:10px;border-top:1px solid #1e293b}
.detail-modify-area{margin-top:14px;padding-top:10px;border-top:1px solid #1e293b}
.result-modify-area{margin-top:10px;padding-top:8px;border-top:1px solid #1e293b}
.result-modify-area .rm-row,.detail-modify-area .modify-row{display:flex;gap:5px;margin-top:4px}
.result-modify-area .rm-row input,.detail-modify-area .modify-row input{flex:1;font-size:.68rem}
.result-modify-area .rm-row button,.detail-modify-area .modify-row button{flex-shrink:0;font-size:.68rem}
.modify-examples{display:flex;gap:4px;flex-wrap:wrap;margin-top:6px}
.modify-examples button{padding:3px 9px;font-size:.6rem;background:#0f172a;border:1px solid #334155;color:#94a3b8;border-radius:12px;cursor:pointer}.modify-examples button:hover{background:#1e293b;color:#e2e8f0}

.gen-retry-btn{margin-left:4px;font-size:.65rem;color:#60a5fa;cursor:pointer;background:none;border:none;padding:2px 4px}.gen-retry-btn:hover{text-decoration:underline}

hr{border:none;border-top:1px solid #1e293b;margin:12px 0}

.gen-layout{display:grid;grid-template-columns:1fr 320px;gap:16px;align-items:start}
.gen-form-panel{min-width:0}
.gen-preview-panel{position:sticky;top:16px}
.preview-placeholder{display:flex;flex-direction:column;align-items:center;justify-content:center;min-height:220px;background-image:repeating-conic-gradient(#0b1120 0 25%,#111827 0 50%);background-size:16px 16px;border-radius:7px;border:1px solid #1e293b;color:#64748b;font-size:.68rem;text-align:center;padding:20px}
.preview-placeholder .ph-icon{font-size:2rem;opacity:.15;margin-bottom:8px}
.preview-img-lg{max-width:100%;max-height:320px;object-fit:contain;border-radius:7px;display:block;margin:0 auto}
.quality-check-list{list-style:none;padding:0;margin:8px 0 0}
.quality-check-list li{display:flex;align-items:center;gap:6px;padding:4px 8px;border-radius:4px;font-size:.62rem;margin-bottom:3px;background:#0f172a}
.quality-check-list li.pass{color:#4ade80}
.quality-check-list li.warn{color:#fbbf24;background:#2d2300}
.quality-check-list li .qc-icon{flex-shrink:0;font-size:.65rem}
.structured-field{margin-bottom:10px}
.structured-field label{display:block;margin-bottom:2px;font-size:.68rem;color:#94a3b8;font-weight:500}
.structured-field .sf-hint{font-size:.6rem;color:#64748b;margin-bottom:3px;line-height:1.3}
.structured-field select,.structured-field input{width:100%;padding:6px 10px;border-radius:6px;border:1px solid #1e293b;background:#0f172a;color:#e2e8f0;font-size:.7rem;font-family:inherit}
.structured-field select:focus,.structured-field input:focus{outline:none;border-color:#e94560;box-shadow:0 0 0 2px rgba(233,69,96,.1)}
.sf-row{display:grid;grid-template-columns:1fr 1fr;gap:8px}

@media(max-width:860px){
  .gen-layout{grid-template-columns:1fr}
  .gen-preview-panel{position:static;margin-top:12px}
}
  .main-layout{grid-template-columns:1fr}
  .type-bar{justify-content:center}
}
</style>
</head>
<body>
<h1>AI 2D Game Asset Generator</h1>
<div class="subtitle">为 Unity / Godot 快速生成统一风格的 2D 游戏素材</div>

<div class="guide-bar">
  <div class="guide-steps">
    <span class="guide-step">创建项目</span><span class="guide-arrow">&rarr;</span>
    <span class="guide-step">设置画风</span><span class="guide-arrow">&rarr;</span>
    <span class="guide-step">选择类型</span><span class="guide-arrow">&rarr;</span>
    <span class="guide-step">填写描述</span><span class="guide-arrow">&rarr;</span>
    <span class="guide-step">生成素材</span><span class="guide-arrow">&rarr;</span>
    <span class="guide-step">下载使用</span>
  </div>
</div>

<div class="main-layout">

  <!-- ===== LEFT: Project & Style ===== -->
  <div>
    <div class="panel" style="margin-bottom:14px">
      <div class="panel-header">项目</div>
      <div class="panel-body sm">
        <div id="no-project-warn" class="no-project-banner">请先创建项目或确认项目 ID</div>
        <label>项目名称</label>
        <input id="project-name" placeholder="地牢像素RPG" value="我的游戏" style="margin-bottom:8px">
        <label>项目描述</label>
        <input id="project-desc" placeholder="一款俯视角像素风地牢游戏" style="margin-bottom:8px">
        <label>项目 ID</label>
        <input id="project-id" value="project_default" readonly style="opacity:.4;font-size:.7rem;margin-bottom:10px">
        <button class="btn-primary btn-sm" style="width:100%" onclick="createProject()">创建 / 更新项目</button>
        <span style="display:block;font-size:.65rem;color:#64748b;margin-top:4px" id="project-status"></span>
      </div>
    </div>

    <div class="panel">
      <div class="panel-header">画风</div>
      <div class="panel-body sm">
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px">
          <div><label>画风</label><select id="style-art"><option value="pixel_art">像素风</option><option value="cartoon">卡通风</option><option value="hand_drawn">手绘风</option></select></div>
          <div><label>视角</label><select id="style-view"><option value="top_down">俯视</option><option value="side_view">侧视</option><option value="isometric">等角</option></select></div>
        </div>
        <label style="margin-top:8px">配色方案</label>
        <select id="style-palette"><option value="dark_dungeon">暗黑地牢</option><option value="bright_forest">明亮森林</option><option value="cyberpunk">赛博朋克</option><option value="custom">自定义</option></select>
        <label style="margin-top:8px">默认尺寸</label>
        <select id="style-size"><option value="32x32">32x32</option><option value="64x64" selected>64x64</option><option value="128x128">128x128</option></select>

        <div class="collapse-box" style="margin-top:10px">
          <div class="collapse-box-header collapsed" onclick="this.classList.toggle('collapsed')"><span class="cb-arrow">&#9662;</span> 高级画风设置</div>
          <div class="collapse-box-body">
            <label>提示词规则</label>
            <textarea id="style-prompt-rules" rows="2" style="font-size:.7rem">centered sprite, clean silhouette</textarea>
            <label style="margin-top:6px">反向提示词</label>
            <textarea id="style-neg-rules" rows="2" style="font-size:.7rem">no text, no watermark, no background clutter</textarea>
          </div>
        </div>

        <button class="btn-primary btn-sm" style="width:100%;margin-top:10px" onclick="saveStyle()">保存画风</button>
        <span style="display:block;font-size:.65rem;color:#64748b;margin-top:4px" id="style-status"></span>
      </div>
    </div>
  </div>

  <!-- ===== RIGHT: Generate + Library ===== -->
  <div>

    <!-- Generate -->
    <div class="panel" style="margin-bottom:16px">
      <div class="panel-header">生成新素材</div>
      <div class="panel-body">
        <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:10px">
          <span style="font-size:.65rem;color:#64748b">快速模板</span>
          <span style="font-size:.6rem;color:#60a5fa;cursor:pointer" id="template-more-toggle" onclick="toggleMoreTemplates()">更多模板</span>
        </div>
        <div class="template-grid" id="template-grid"></div>

        <div class="type-bar" id="type-bar">
          <button class="type-btn active" data-type="character" onclick="selectType('character',this)">角色</button>
          <button class="type-btn" data-type="enemy" onclick="selectType('enemy',this)">敌人</button>
          <button class="type-btn" data-type="item" onclick="selectType('item',this)">道具</button>
          <button class="type-btn" data-type="tile" onclick="selectType('tile',this)">瓦片</button>
          <button class="type-btn" data-type="ui_icon" onclick="selectType('ui_icon',this)">UI</button>
          <button class="type-btn" data-type="effect" onclick="selectType('effect',this)">特效</button>
        </div>

        <select id="gen-type" onchange="onTypeChange()" style="display:none"><option value="character">角色</option><option value="enemy">敌人</option><option value="item">道具</option><option value="tile">瓦片</option><option value="ui_icon">UI</option><option value="effect">特效</option></select>

        <div class="gen-layout">
          <div class="gen-form-panel">
            <div id="gen-fields"></div>
            <div id="completeness-hint" style="margin-top:8px;font-size:.62rem"></div>
            <div class="btn-row" style="margin-top:8px">
              <button class="btn-outline btn-xs" id="btn-random" onclick="randomCharacter()" style="display:none">随机完整角色</button>
              <button class="btn-outline btn-xs" id="btn-clear-chips" onclick="clearAllChips()" style="display:none">清空选择</button>
            </div>
            <div class="btn-row">
              <button class="btn-primary btn-xl" id="btn-generate" onclick="generateAsset()">生成素材</button>
              <button class="btn-secondary btn-sm" id="btn-regenerate" style="display:none" onclick="regenerateAsset()">重新生成</button>
            </div>
            <div class="prompt-detail" id="prompt-detail">
              <div class="prompt-detail-header" onclick="var h=this;h.classList.toggle('collapsed');var b=document.getElementById('pd-body');b.style.display=b.style.display==='none'?'block':'none'">
                <span class="pd-arrow">&#9662;</span> Prompt 预览
              </div>
              <div class="prompt-detail-body" id="pd-body" style="display:none">
                <div class="pd-section" id="pd-user"></div>
                <div class="pd-section" id="pd-style"></div>
                <div class="pd-section" id="pd-system"></div>
                <div class="pd-section" id="pd-negative"></div>
              </div>
              <div class="pd-manual-toggle">
                <input type="checkbox" id="manual-edit-toggle" onchange="toggleManualEdit()">
                <label for="manual-edit-toggle" style="display:inline;color:#94a3b8;font-size:.63rem">手动编辑 Prompt</label>
              </div>
              <div class="pd-manual-area" id="pd-manual-area">
                <textarea id="pd-manual-text" placeholder="在这里编辑最终发送给 AI 的 Prompt..." oninput="refreshPromptPreview()"></textarea>
              </div>
            </div>
          </div>
          <div class="gen-preview-panel">
            <div class="panel" style="margin-bottom:0">
              <div class="panel-header">预览</div>
              <div class="panel-body">
                <div id="gen-preview-img-area">
                  <div class="preview-placeholder" id="preview-placeholder">
                    <div class="ph-icon">&#9635;</div>
                    <span>选择参数后点击生成</span>
                  </div>
                </div>
                <div id="gen-progress" style="margin-top:8px"></div>
                <div id="gen-error"></div>
                <div id="gen-qc-results"></div>
                <div id="gen-result"></div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Asset Library -->
    <div class="panel">
      <div class="panel-header">素材库 <button class="btn-ghost" style="margin-left:auto" onclick="loadAssets()">刷新</button></div>
      <div class="panel-body">
        <div id="msg-container"></div>
        <div class="filter-bar">
          <div class="filter-types" id="filter-types">
            <button class="filter-btn active" data-type="all" onclick="setFilter('all',this)">全部</button>
            <button class="filter-btn" data-type="character" onclick="setFilter('character',this)">角色</button>
            <button class="filter-btn" data-type="enemy" onclick="setFilter('enemy',this)">敌人</button>
            <button class="filter-btn" data-type="prop" onclick="setFilter('prop',this)">道具</button>
            <button class="filter-btn" data-type="tile" onclick="setFilter('tile',this)">瓦片</button>
            <button class="filter-btn" data-type="ui_icon" onclick="setFilter('ui_icon',this)">UI</button>
            <button class="filter-btn" data-type="effect" onclick="setFilter('effect',this)">特效</button>
          </div>
          <input type="text" class="search-input" id="search-input" placeholder="搜索..." oninput="renderAssets()">
        </div>
        <div class="stats-text" id="stats-bar"></div>
        <div id="asset-list"></div>
      </div>
    </div>

  </div>
</div>

<div class="detail-overlay" id="detail-modal" onclick="closeDetail()">
  <div class="detail-panel" onclick="event.stopPropagation()">
    <button class="detail-close-btn" onclick="closeDetail()">&#10005;</button>
    <div class="detail-img-area"><img id="detail-img" src="" alt=""></div>
    <div class="detail-body">
      <h3><span id="detail-name"></span></h3>
      <div id="detail-rows"></div>
      <div class="detail-actions" id="detail-actions"></div>
      <div class="detail-modify-area">
        <label style="font-size:.7rem">基于当前素材修改</label>
        <div class="modify-examples" id="modify-examples"></div>
        <div class="modify-row">
          <input id="modify-input" placeholder="例如：改成红色、更像像素风...">
          <button class="btn-primary btn-sm" id="btn-modify" onclick="modifyCurrentAsset()">生成修改版</button>
        </div>
        <div id="modify-progress" style="margin-top:5px"></div>
      </div>
    </div>
  </div>
</div>

<script>
var API = '/api';
var lastGenParams = null;
var cachedAssets = [];
var currentFilter = 'all';
var progressTimer = null;
var progressStepIndex = 0;
var showAllTemplates = false;
var progressSteps = ['正在理解描述...','正在构造 Prompt...','正在生成图片...','正在处理...','正在保存...'];

function msg(text, type) {
  var c = document.getElementById('msg-container');
  c.innerHTML = '<div class="msg msg-' + type + '">' + text + '</div>';
  setTimeout(function(){ c.innerHTML = ''; }, 6000);
}
function toast(text, type) {
  var t = document.getElementById('toast-el');
  if (!t) { t = document.createElement('div'); t.id = 'toast-el'; document.body.appendChild(t); }
  t.className = 'toast toast-' + (type || 'success'); t.textContent = text; t.style.display = 'block';
  clearTimeout(t._timer); t._timer = setTimeout(function(){ t.style.display = 'none'; }, 2500);
}
function getProjectId() { return document.getElementById('project-id').value || 'project_default'; }
function isProjectReady() { var p = getProjectId(); return p && p !== 'project_default'; }

async function api(url, opts) {
  var res = await fetch(url, Object.assign({ headers: {'Content-Type':'application/json'} }, opts || {}));
  if (!res.ok) throw new Error('HTTP ' + res.status);
  return res.json();
}

function translateError(errMsg) {
  if (!errMsg) return '未知错误';
  var msg = String(errMsg).toLowerCase();
  if (msg.indexOf('not configured')>=0) return '图片生成服务还没有配置，请检查 IMAGE_API_KEY';
  if (msg.indexOf('tongyi')>=0||msg.indexOf('dashscope')>=0) return '通义万象图片生成服务调用失败';
  if (msg.indexOf('project not found')>=0) return '项目不存在，请先创建项目';
  if (msg.indexOf('style profile')>=0||msg.indexOf('style_profile')>=0) return '请先保存画风配置';
  if (msg.indexOf('network')>=0||msg.indexOf('fetch')>=0||msg.indexOf('econnrefused')>=0) return '请求失败，请检查后端服务是否运行';
  if (msg.indexOf('rate')>=0||msg.indexOf('quota')>=0) return 'API 额度不足，请稍后重试';
  if (msg.indexOf('unsupported')>=0) return '不支持的图片生成服务商';
  return errMsg.length > 120 ? errMsg.substring(0,120)+'...' : errMsg;
}
function getAssetTypeName(type) {
  var map = { character:'角色',enemy:'敌人',prop:'道具',tile:'瓦片',ui_icon:'UI',item:'物品',effect:'特效' };
  return map[type]||type;
}
function formatDate(iso) {
  if (!iso) return '';
  try { var d=new Date(iso); var p=function(n){return String(n).padStart(2,'0');}; return (d.getMonth()+1)+'/'+p(d.getDate())+' '+p(d.getHours())+':'+p(d.getMinutes()); } catch(e){return iso;}
}
function escapeHtml(t) {
  if (!t) return '';
  return String(t).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
}
function getFieldVal(id) { var el=document.getElementById(id); return el?el.value:''; }

// ---- Type selection ----
function selectType(type, btn) {
  document.getElementById('gen-type').value = type;
  document.querySelectorAll('#type-bar .type-btn').forEach(function(b){ b.classList.remove('active'); });
  if (btn) btn.classList.add('active');
  onTypeChange();
}

// ---- Project ----
async function createProject() {
  var name = document.getElementById('project-name').value || '我的游戏';
  var desc = document.getElementById('project-desc').value || '';
  var s = document.getElementById('project-status'); s.textContent = '...';
  try {
    var data = await api(API+'/projects',{method:'POST',body:JSON.stringify({name:name,description:desc})});
    if (data.success) {
      document.getElementById('project-id').value = data.project.id;
      s.textContent = 'ok'; s.style.color = '#4ade80';
      msg('项目已创建','success');
    } else { s.textContent = 'fail'; s.style.color = '#fca5a5'; }
  } catch(e) { s.textContent = 'fail'; s.style.color = '#fca5a5'; }
}

// ---- Style ----
async function saveStyle() {
  var pid = getProjectId();
  var body = {
    art_style: document.getElementById('style-art').value,
    view_type: document.getElementById('style-view').value,
    color_palette: document.getElementById('style-palette').value,
    default_size: document.getElementById('style-size').value,
    prompt_rules: document.getElementById('style-prompt-rules').value,
    negative_prompt_rules: document.getElementById('style-neg-rules').value
  };
  var s = document.getElementById('style-status'); s.textContent = '...';
  try {
    var data = await api(API+'/projects/'+pid+'/style',{method:'POST',body:JSON.stringify(body)});
    if (data.success) { s.textContent = 'ok'; s.style.color = '#4ade80'; msg('画风已保存','success'); }
    else { s.textContent = 'fail'; s.style.color = '#fca5a5'; }
  } catch(e) { s.textContent = 'fail'; s.style.color = '#fca5a5'; }
}

// ---- Quick Templates ----
var QUICK_TEMPLATES = [
  {label:'像素恶魔',type:'enemy',desc:'像素风红色恶魔敌人',fill:{name:'红色恶魔',view:'front',action:'attacking',appearance:'像素风、红色皮肤、黑色角、尖牙、凶恶',emotion:'angry',pose:'attacking','canvas-fill':'85%',complexity:'simple','outline-style':'pixel','color-palette':'红、黑',size:'64x64',background:'transparent'}},
  {label:'Q版法师',type:'character',desc:'Q版蓝色法师角色',fill:{name:'蓝色小法师',view:'front',action:'idle',appearance:'Q版头大身小、蓝色长袍、法师帽、可爱大眼睛',emotion:'cute',pose:'idle','canvas-fill':'85%',complexity:'simple','outline-style':'clean','color-palette':'蓝、白、金',size:'64x64',background:'transparent'}},
  {label:'金币',type:'item',desc:'金币道具图标',fill:{name:'金币',item_category:'coin',appearance:'金色圆币、星纹、闪亮、扁平',complexity:'medium','canvas-fill':'75%','color-palette':'金、黄',size:'64x64'}},
  {label:'草地',type:'tile',desc:'草地无缝瓦片',fill:{name:'森林草地',tile_type:'grass',material:'绿草地、小花、自然',seamless:'true',complexity:'medium','color-palette':'绿色自然',size:'32x32'}},
  {label:'火球',type:'effect',desc:'火焰技能特效',fill:{name:'火球爆炸',effect_type:'fire',motion_feeling:'burst',appearance:'橙红火焰、高亮、爆发',complexity:'medium','canvas-fill':'85%','color-palette':'橙红、亮黄',size:'64x64'}},
  {label:'蓝袍法师',type:'character',desc:'像素俯视蓝袍法师',fill:{name:'蓝袍月光法师',view:'top_down',action:'attack',appearance:'像素风、蓝白配色、白发、冷静、蓝色长袍、月光特效',weapon:'法杖',size:'64x64'}},
  {label:'红甲剑士',type:'character',desc:'日式RPG红甲战士',fill:{name:'红甲剑士',view:'side_view',action:'attack',appearance:'日式RPG、红黑配色、金发、自信、轻甲、披风飘动',weapon:'长剑',size:'64x64'}},
  {label:'绿史莱姆',type:'enemy',desc:'Q版绿色史莱姆',fill:{name:'绿色史莱姆',view:'front',action:'walk',appearance:'Q版、绿色主色、呆萌圆眼、圆滚滚、身体半透明、黏液质感',weapon:'',size:'64x64'}},
  {label:'冰霜女巫',type:'character',desc:'暗黑冰系施法者',fill:{name:'冰霜女巫',view:'front',action:'attack',appearance:'暗黑幻想、冰蓝色、白发、神秘、黑色斗篷、冰霜气息',weapon:'冰晶',size:'64x64'}},
  {label:'机械守卫',type:'enemy',desc:'科幻金属机械守卫',fill:{name:'机械守卫',view:'front',action:'attack',appearance:'科幻机械、机械银灰、发光眼睛、严肃、机械装甲、能量核心',weapon:'能量炮',size:'128x128'}},
  {label:'地牢骷髅',type:'enemy',desc:'暗黑骨头短剑骷髅',fill:{name:'地牢骷髅兵',view:'side_view',action:'attack',appearance:'暗黑幻想、白银配色、凶狠、破旧盔甲、骨头结构',weapon:'短剑',size:'64x64'}},
  {label:'猫耳盗贼',type:'character',desc:'Q版猫耳轻甲盗贼',fill:{name:'猫耳盗贼',view:'side_view',action:'walk',appearance:'Q版、黑紫配色、猫耳、狡黠、轻甲',weapon:'匕首',size:'64x64'}},
  {label:'圣光牧师',type:'character',desc:'白金配色神圣牧师',fill:{name:'圣光牧师',view:'front',action:'attack',appearance:'中世纪幻想、白金配色、神圣、华丽长袍、背后光环',weapon:'治疗权杖',size:'64x64'}},
  {label:'Q版弓手',type:'character',desc:'Q版正面绿装弓手',fill:{name:'弓箭手',view:'front',action:'idle',appearance:'Q版头大身小、绿披风、小短腿、可爱',weapon:'弓箭',size:'64x64'}},
  {label:'暗黑法师',type:'enemy',desc:'暗黑兜帽紫袍法师',fill:{name:'暗黑法师',view:'front',action:'attack',appearance:'暗黑幻想、暗紫色、兜帽遮脸、邪恶、黑色斗篷',weapon:'暗黑法杖',size:'128x128'}},
  {label:'药水',type:'item',desc:'红色玻璃瓶',fill:{name:'生命药水',item_category:'potion',appearance:'红色液体、玻璃瓶、软木塞',size:'64x64'}},
  {label:'魔法书',type:'item',desc:'皮质发光符文',fill:{name:'魔法书',item_category:'weapon',appearance:'皮质封面、发光符文、神秘',size:'64x64'}},
  {label:'石砖',type:'tile',desc:'地牢石砖无缝',fill:{name:'石砖地板',tile_type:'floor',material:'灰色石砖、青苔',seamless:'true',size:'32x32'}},
  {label:'岩浆',type:'tile',desc:'火山岩浆裂纹',fill:{name:'岩浆地面',tile_type:'lava',material:'黑裂岩、橙岩浆',seamless:'true',size:'32x32'}},
  {label:'血量',type:'ui_icon',desc:'红色心形UI',fill:{name:'生命值图标',icon_purpose:'health',shape:'no_frame',appearance:'红色心形、高对比、简洁',size:'64x64'}},
  {label:'金币图标',type:'ui_icon',desc:'金色圆形像素',fill:{name:'金币图标',icon_purpose:'coin',shape:'circle',appearance:'金色硬币、圆形、像素风',size:'64x64'}},
  {label:'技能图标',type:'ui_icon',desc:'蓝光魔法徽章',fill:{name:'技能图标',icon_purpose:'skill',shape:'no_frame',appearance:'蓝色发光徽章、能量感',size:'64x64'}},
  {label:'冰霜',type:'effect',desc:'冰霜环绕光环',fill:{name:'冰霜光环',effect_type:'ice',motion_feeling:'aura',appearance:'蓝冰晶、透明、柔和',size:'64x64'}},
  {label:'雷电',type:'effect',desc:'雷电横向斩击',fill:{name:'雷电斩击',effect_type:'lightning',motion_feeling:'slash',appearance:'黄闪电、锐利、能量',size:'128x128'}}
];
var VISIBLE_TEMPLATE_COUNT = 8;

function toggleMoreTemplates() {
  showAllTemplates = !showAllTemplates;
  document.getElementById('template-more-toggle').textContent = showAllTemplates ? '收起模板' : '更多模板';
  renderTemplates();
}
function renderTemplates() {
  var grid = document.getElementById('template-grid');
  if (!grid) return;
  var count = showAllTemplates ? QUICK_TEMPLATES.length : VISIBLE_TEMPLATE_COUNT;
  var html = '';
  for (var i = 0; i < QUICK_TEMPLATES.length && i < count; i++) {
    var t = QUICK_TEMPLATES[i];
    html += '<button class="tpl-btn ' + t.type + '" onclick="applyTemplate(QUICK_TEMPLATES[' + i + '])" title="' + t.desc + '"><span class="tpl-dot"></span>' + t.label + '</button>';
  }
  grid.innerHTML = html;
}
function applyTemplate(tpl) {
  selectType(tpl.type);
  renderTypeFields(tpl.type);
  var f = tpl.fill;
  var map = {name:'genf-name',view:'genf-view',action:'genf-action',pose:'genf-pose',appearance:'genf-appearance',weapon:'genf-weapon','canvas-fill':'genf-canvas-fill',complexity:'genf-complexity','outline-style':'genf-outline-style','color-palette':'genf-color-palette',emotion:'genf-emotion',background:'genf-background',item_category:'genf-item_category',tile_type:'genf-tile_type',material:'genf-material',seamless:'genf-seamless',icon_purpose:'genf-icon_purpose',shape:'genf-shape',effect_type:'genf-effect_type',motion_feeling:'genf-motion_feeling',size:'genf-size'};
  for (var k in f) { var el = document.getElementById(map[k]); if (el) el.value = f[k]; }
  refreshPromptPreview();
}

// ---- EXAMPLES ----
var EXAMPLES = {
  character: [{label:'骑士战士',fill:{name:'骑士战士',view:'top_down',action:'idle',appearance:'铁盔、板甲、坚定',weapon:'铁剑',size:'64x64'}},{label:'蓝袍法师',fill:{name:'蓝袍法师',view:'front',action:'attack',appearance:'蓝长袍、兜帽、冷静',weapon:'法杖',size:'64x64'}},{label:'精灵弓手',fill:{name:'精灵弓手',view:'side_view',action:'walk',appearance:'绿披风、金发、轻盈',weapon:'弓箭',size:'128x128'}}],
  enemy: [{label:'骷髅兵',fill:{name:'骷髅兵',view:'top_down',action:'idle',appearance:'白骨、红眼、暗黑',weapon:'骨刀',size:'64x64'}},{label:'史莱姆',fill:{name:'绿史莱姆',view:'front',action:'walk',appearance:'绿半透明、圆滚',weapon:'',size:'64x64'}},{label:'暗黑法师',fill:{name:'暗黑法师',view:'front',action:'attack',appearance:'黑兜帽袍、紫能量',weapon:'暗法杖',size:'128x128'}}],
  item: [{label:'生命药水',fill:{name:'生命药水',item_category:'potion',appearance:'红液、玻璃瓶、软木塞',size:'64x64'}},{label:'金币',fill:{name:'金币',item_category:'coin',appearance:'金圆币、星纹、闪亮',size:'64x64'}},{label:'铁剑',fill:{name:'铁剑',item_category:'weapon',appearance:'银刃、棕皮柄',size:'128x128'}}],
  tile: [{label:'石砖',fill:{name:'石砖地板',tile_type:'floor',material:'灰石砖、青苔',seamless:'true',size:'32x32'}},{label:'草地',fill:{name:'草地',tile_type:'grass',material:'绿草、小花',seamless:'true',size:'32x32'}},{label:'岩浆',fill:{name:'岩浆',tile_type:'lava',material:'黑裂岩、橙岩浆',seamless:'true',size:'32x32'}}],
  ui_icon: [{label:'红心图标',fill:{name:'生命值图标',icon_purpose:'health',shape:'circle',appearance:'红心、白圆底',size:'64x64'}},{label:'金币图标',fill:{name:'金币图标',icon_purpose:'coin',shape:'no_frame',appearance:'金硬币、扁平',size:'64x64'}},{label:'齿轮',fill:{name:'设置图标',icon_purpose:'settings',shape:'circle',appearance:'银齿轮、深色圆底',size:'64x64'}}],
  effect: [{label:'火球',fill:{name:'火球爆炸',effect_type:'fire',motion_feeling:'burst',appearance:'橙火焰、爆发、发光',size:'64x64'}},{label:'冰霜',fill:{name:'冰霜光环',effect_type:'ice',motion_feeling:'aura',appearance:'蓝冰晶、环绕、透明',size:'64x64'}},{label:'雷电',fill:{name:'雷电斩击',effect_type:'lightning',motion_feeling:'slash',appearance:'黄闪电、横斩、锐利',size:'128x128'}}]
};
function fillExample(type, ex) {
  selectType(type);
  renderTypeFields(type);
  var f = ex.fill;
  var map = {name:'genf-name',view:'genf-view',action:'genf-action',pose:'genf-pose',appearance:'genf-appearance',weapon:'genf-weapon','canvas-fill':'genf-canvas-fill',complexity:'genf-complexity','outline-style':'genf-outline-style','color-palette':'genf-color-palette',emotion:'genf-emotion',item_category:'genf-item_category',tile_type:'genf-tile_type',material:'genf-material',seamless:'genf-seamless',icon_purpose:'genf-icon_purpose',shape:'genf-shape',effect_type:'genf-effect_type',motion_feeling:'genf-motion_feeling',size:'genf-size'};
  for (var k in f) { var el = document.getElementById(map[k]); if (el) el.value = f[k]; }
}

// ---- CHIP_DEFS ----
var CHIP_DEFS = {
  character: {
    role:{label:'角色定位',open:true,target:'genf-appearance',chips:['主角','敌人','Boss','NPC','伙伴','召唤物','宠物','精英怪','远程单位','近战单位','辅助单位','治疗单位','坦克单位']},
    style:{label:'美术风格',open:true,target:'genf-appearance',chips:['像素风','Q版','卡通','日式RPG','暗黑幻想','中世纪幻想','科幻机械','蒸汽朋克','赛博朋克','复古街机','手绘风','低饱和','高对比','简洁轮廓','厚描边','扁平化','明亮可爱','阴郁压抑','魔法幻想']},
    genre:{label:'游戏题材',open:false,target:'genf-appearance',chips:['地牢冒险','魔法学院','森林探险','雪地世界','火山洞窟','沙漠遗迹','天空岛','海盗冒险','机械工厂','末日废土','赛博都市','东方幻想','西方奇幻','勇者冒险','塔防游戏','横版动作','俯视角RPG','Roguelike']},
    roleClass:{label:'职业身份',open:true,target:'genf-name',chips:['法师','战士','骑士','弓箭手','刺客','牧师','盗贼','召唤师','炼金术士','机械师','枪手','忍者','武士','女巫','祭司','德鲁伊','死灵法师','圣骑士','狂战士','魔剑士','冰霜法师','火焰法师','雷电术士','机械守卫','地牢守卫','史莱姆','骷髅兵','哥布林','恶魔','龙人']},
    body:{label:'体型比例',open:false,target:'genf-appearance',chips:['Q版头大身小','小短腿','正常比例','高瘦','魁梧','娇小','圆滚滚','修长','强壮','胖乎乎','轻盈','笨重','小型怪物','巨大型Boss','人形','非人形','兽人型','机械体','史莱姆身体','幽灵身体']},
    color:{label:'主色配色',open:true,target:'genf-appearance',chips:['蓝色主色','红色主色','绿色主色','紫色主色','金色点缀','黑金配色','白银配色','蓝白配色','红黑配色','绿色自然系','冰蓝色','火焰橙红','毒绿色','暗紫色','机械银灰','棕色皮革','冷色调','暖色调','低饱和','高饱和','暗色调','明亮色调']},
    hair:{label:'发型脸部',open:false,target:'genf-appearance',chips:['短发','长发','白发','金发','黑发','蓝发','红发','双马尾','兜帽遮脸','面具','发光眼睛','单眼','两只大眼睛','眯眯眼','尖耳朵','猫耳','恶魔角','机械眼','脸上伤疤','凶狠眼神','呆萌圆眼','无脸幽灵']},
    expression:{label:'表情气质',open:false,target:'genf-appearance',chips:['冷静','严肃','凶狠','可爱','呆萌','开心','愤怒','神秘','自信','邪恶','坚定','忧郁','高傲','慵懒','疯狂','阴险','忠诚','神圣','危险','活泼','沉稳','压迫感','亲和力']},
    clothing:{label:'服装装备',open:false,target:'genf-appearance',chips:['蓝色长袍','红色披风','黑色斗篷','魔法袍','轻甲','重甲','皮甲','骑士盔甲','忍者服','机械装甲','破旧布衣','华丽礼服','战斗短袍','兜帽','护肩','腰带','长靴','手套','围巾','披肩','胸甲','金属护腕','魔法纹章','发光宝石','小翅膀','尾巴']},
    weapon_chip:{label:'武器道具',open:true,target:'genf-weapon',chips:['法杖','长剑','短剑','双刀','弓箭','盾牌','长枪','匕首','锤子','斧头','镰刀','魔法书','火球','冰晶','雷电法球','药瓶','炸弹','灯笼','魔法水晶','机械枪','能量剑','回旋镖','十字弩','治疗权杖']},
    action_chip:{label:'动作姿态',open:true,target:'genf-action',chips:['待机','站立','行走','奔跑','攻击','施法','防御','举盾','挥剑','拉弓','跳跃','受伤','死亡','冲刺','瞄准','召唤','胜利姿势']},
    detail:{label:'细节特征',open:false,target:'genf-appearance',chips:['发光眼睛','发光轮廓','背后光环','火焰特效','冰霜气息','雷电环绕','毒雾','魔法阵','机械手臂','破损盔甲','脸上伤疤','小翅膀','恶魔角','猫耳','尾巴','披风飘动','武器发光','身体半透明','圆滚滚身体','黏液质感','骨头结构','金属关节','能量核心','宝石镶嵌']},
    output:{label:'输出规范',open:false,target:'genf-appearance',chips:['透明背景','居中显示','单个角色','全身角色','干净轮廓','适合64x64','适合128x128','适合Unity Sprite','俯视角','侧视角','正面展示','无复杂背景','无文字','无水印','强轮廓','小尺寸可读']}
  },
  enemy: {
    role:{label:'角色定位',open:true,target:'genf-appearance',chips:['主角','敌人','Boss','NPC','精英怪','小怪','远程单位','近战单位','召唤物']},
    style:{label:'美术风格',open:true,target:'genf-appearance',chips:['像素风','Q版','卡通','暗黑幻想','中世纪幻想','科幻机械','赛博朋克','复古街机','低饱和','高对比','厚描边','阴郁压抑']},
    genre:{label:'游戏题材',open:false,target:'genf-appearance',chips:['地牢冒险','魔法学院','森林探险','雪地世界','火山洞窟','机械工厂','末日废土','横版动作','俯视角RPG','Roguelike']},
    roleClass:{label:'职业身份',open:true,target:'genf-name',chips:['史莱姆','骷髅兵','哥布林','恶魔','机械守卫','暗黑法师','死神','吸血鬼','幽灵','龙','Boss','精英怪','小怪']},
    body:{label:'体型比例',open:false,target:'genf-appearance',chips:['Q版头大身小','小短腿','魁梧','圆滚滚','修长','强壮','笨重','小型怪物','巨大型Boss','人形','非人形','兽人型','机械体','史莱姆身体','幽灵身体']},
    color:{label:'主色配色',open:true,target:'genf-appearance',chips:['蓝色主色','红色主色','绿色主色','紫色主色','暗色调','暗紫色','毒绿色','火焰橙红','冰蓝色','冷色调','暗色调','高饱和']},
    hair:{label:'发型脸部',open:false,target:'genf-appearance',chips:['发光眼睛','单眼','恶魔角','机械眼','脸上伤疤','凶狠眼神','无脸幽灵','面具','尖耳朵','骨头结构']},
    expression:{label:'表情气质',open:true,target:'genf-appearance',chips:['凶狠','邪恶','愤怒','神秘','疯狂','冷漠','恐怖','阴险','危险','呆萌','压迫感']},
    clothing:{label:'外观特征',open:false,target:'genf-appearance',chips:['暗影','触手','尖刺','火焰环绕','冰霜覆盖','破旧盔甲','破烂长袍','骨甲','金属装甲']},
    weapon_chip:{label:'武器道具',open:true,target:'genf-weapon',chips:['骨刀','暗黑法杖','毒爪','巨锤','火焰剑','冰霜弓','雷电矛','触手','尖牙','能量炮']},
    action_chip:{label:'动作姿态',open:true,target:'genf-action',chips:['待机','弹跳','扑击','咆哮','悬浮','巡逻','蓄力','撞击','攻击','防御','受伤','死亡','张牙舞爪']},
    detail:{label:'细节特征',open:false,target:'genf-appearance',chips:['发光眼睛','发光轮廓','背后光环','火焰特效','冰霜气息','雷电环绕','毒雾','破损盔甲','恶魔角','尾巴','武器发光','身体半透明','圆滚滚身体','黏液质感','骨头结构','金属关节','能量核心']},
    output:{label:'输出规范',open:false,target:'genf-appearance',chips:['透明背景','居中显示','单个角色','全身角色','干净轮廓','适合64x64','适合128x128','适合Unity Sprite','侧视角','正面展示','无复杂背景','强轮廓','小尺寸可读']}
  },
  item: {
    type_chip:{label:'类型',open:true,target:'genf-item_category',chips:['药水','金币','钥匙','卷轴','宝石','食物','武器']},
    material_chip:{label:'材质',open:true,target:'genf-appearance',chips:['木质','金属','水晶','玻璃','皮革','黄金','银色']},
    feel:{label:'感觉',open:false,target:'genf-appearance',chips:['闪亮','破旧','神秘','可爱','稀有','魔法感','复古']}
  },
  tile: {
    type_chip:{label:'类型',open:true,target:'genf-tile_type',chips:['地板','墙壁','草地','道路','水面','岩浆','沙地']},
    material_chip:{label:'材质',open:true,target:'genf-material',chips:['石砖','泥土','青苔','木头','雪','沙子','熔岩']},
    feature:{label:'特性',open:false,target:'genf-seamless',chips:['无缝平铺','俯视角','适合Tilemap']}
  },
  ui_icon: {
    purpose_chip:{label:'用途',open:true,target:'genf-icon_purpose',chips:['血量','金币','技能','背包','设置','地图','任务']},
    shape_chip:{label:'形状',open:true,target:'genf-shape',chips:['圆形','方形','无边框','徽章式','菱形']},
    style_chip:{label:'风格',open:false,target:'genf-appearance',chips:['简洁','高对比','发光','卡通','像素风','扁平']}
  },
  effect: {
    type_chip:{label:'类型',open:true,target:'genf-effect_type',chips:['火焰','冰霜','雷电','治疗','爆炸','毒气','护盾']},
    motion_chip:{label:'动势',open:true,target:'genf-motion_feeling',chips:['爆发','旋转','聚集','扩散','拖尾','闪烁','环绕']},
    feel:{label:'感觉',open:false,target:'genf-appearance',chips:['高亮','透明','发光','强对比','柔和','锐利','危险','神圣']}
  }
};
var VIEW_MAP = {'正面':'front','侧面':'side_view','背面':'back','俯视':'top_down','顶视角':'top_down','俯视角':'top_down','正面展示':'front','侧视角':'side_view','top-down':'top_down','side-view':'side_view','front-view':'front','isometric':'isometric'};
var ACTION_MAP = {'站立':'idle','待机':'idle','行走':'walk','奔跑':'run','攻击':'attack','施法':'attack','跳跃':'jump','受伤':'hurt','死亡':'dead','防御':'defend','举盾':'defend','挥剑':'attack','拉弓':'attack','冲刺':'run','瞄准':'attack','召唤':'attack','胜利姿势':'idle','咆哮':'attack','弹跳':'walk','扑击':'attack','悬浮':'idle','巡逻':'walk','蓄力':'attack','撞击':'attack','张牙舞爪':'attack'};

function toggleChipGroup(key) {
  var el = document.getElementById('chip-group-'+key);
  if (!el) return;
  var h = el.querySelector('.chip-group-header');
  if (h) h.classList.toggle('collapsed');
}
function toggleChip(groupKey, chipText) {
  var defs = CHIP_DEFS[document.getElementById('gen-type').value] || CHIP_DEFS.character;
  var group = defs[groupKey]; if (!group) return;
  var el = document.getElementById(group.target); if (!el) return;
  var current = el.value || '';
  var words = current.split(/[,，\\s]+/).filter(function(w){return w.length>0;});

  if (group.target === 'genf-view' && VIEW_MAP[chipText]) { el.value = VIEW_MAP[chipText]; updateChipStates(groupKey,chipText); refreshPromptPreview(); return; }
  if (group.target === 'genf-action' && ACTION_MAP[chipText]) { el.value = ACTION_MAP[chipText]; updateChipStates(groupKey,chipText); refreshPromptPreview(); return; }
  if (group.target === 'genf-seamless') { el.value = (el.value==='true')?'false':'true'; updateChipStates(groupKey,chipText); refreshPromptPreview(); return; }
  if (['genf-item_category','genf-tile_type','genf-icon_purpose','genf-effect_type','genf-shape','genf-motion_feeling'].indexOf(group.target)>=0) { el.value = chipText; updateChipStates(groupKey,chipText); refreshPromptPreview(); return; }

  var idx = -1;
  for (var i=0;i<words.length;i++) { if (words[i].toLowerCase()===chipText.toLowerCase()){idx=i;break;} }
  if (idx>=0) words.splice(idx,1); else words.push(chipText);
  el.value = words.join(', ');
  updateChipStates(groupKey,null);
  refreshPromptPreview();
}
function updateChipStates(groupKey, activeText) {
  var defs = CHIP_DEFS[document.getElementById('gen-type').value] || CHIP_DEFS.character;
  var group = defs[groupKey]; if (!group) return;
  var el = document.getElementById(group.target);
  var current = el ? (el.value||'').toLowerCase() : '';
  var chips = document.querySelectorAll('#chip-group-'+groupKey+' .chip');
  for (var i=0;i<chips.length;i++) {
    var t = (chips[i].textContent||'').toLowerCase();
    if (activeText && t===activeText.toLowerCase()) chips[i].classList.add('active');
    else if (activeText===null && current.indexOf(t)>=0) chips[i].classList.add('active');
    else chips[i].classList.remove('active');
  }
}

function randomCharacter() {
  var type = document.getElementById('gen-type').value;
  var defs = CHIP_DEFS[type];
  if (!defs) return;
  var picks = [];
  var pickFrom = function(gk) {
    var g = defs[gk]; if (!g || !g.chips) return;
    var c = g.chips[Math.floor(Math.random() * g.chips.length)];
    picks.push(c);
    toggleChip(gk, c);
  };
  if (type === 'character' || type === 'enemy') {
    pickFrom('style'); pickFrom('genre'); pickFrom('roleClass'); pickFrom('color');
    pickFrom('expression'); pickFrom('clothing'); pickFrom('weapon_chip'); pickFrom('action_chip');
    pickFrom('detail'); var d2 = defs.detail.chips[Math.floor(Math.random()*defs.detail.chips.length)];
    picks.push(d2); toggleChip('detail', d2);
    var n = defs.roleClass.chips[Math.floor(Math.random()*defs.roleClass.chips.length)];
    document.getElementById('genf-name').value = n;
  }
  updateCompletenessHint();
  refreshPromptPreview();
}

function clearAllChips() {
  var type = document.getElementById('gen-type').value;
  var defs = CHIP_DEFS[type];
  var cleared = {};
  if (!defs) return;
  for (var key in defs) {
    var g = defs[key]; if (!g || !g.target) continue;
    if (cleared[g.target]) continue;
    cleared[g.target] = true;
    var el = document.getElementById(g.target);
    if (!el) continue;
    if (['genf-view','genf-action','genf-item_category','genf-tile_type','genf-icon_purpose','genf-effect_type','genf-shape','genf-motion_feeling','genf-seamless'].indexOf(g.target) >= 0) continue;
    el.value = '';
  }
  document.querySelectorAll('.chip').forEach(function(c){ c.classList.remove('active'); });
  updateCompletenessHint();
  refreshPromptPreview();
}

function updateCompletenessHint() {
  var type = document.getElementById('gen-type').value;
  var el = document.getElementById('completeness-hint');
  if (!el) return;
  if (type !== 'character' && type !== 'enemy') { el.innerHTML = ''; return; }
  var missing = [];
  var app = (getFieldVal('genf-appearance')||'').toLowerCase();
  var name = (getFieldVal('genf-name')||'').toLowerCase();
  var pose = getFieldVal('genf-pose');
  var cf = getFieldVal('genf-canvas-fill');
  var cp = getFieldVal('genf-color-palette');
  var em = getFieldVal('genf-emotion');
  if (!app || app.length < 10) missing.push('外观特征');
  if (!name || name.length < 2) missing.push('角色名称');
  if (!pose || pose === 'idle') missing.push('动作姿态');
  if (!cp) missing.push('配色');
  if (!em) missing.push('表情');
  if (missing.length === 0) {
    el.innerHTML = '<span style="color:#4ade80">参数设置完整，可以生成</span>';
  } else if (missing.length <= 2) {
    el.innerHTML = '<span style="color:#fbbf24">建议补充：' + missing.join('、') + '</span>';
  } else {
    el.innerHTML = '<span style="color:#fca5a5">缺少关键信息：' + missing.join('、') + '。建议用下方标签快速填充</span>';
  }
}

// ---- FIELD_DEFS ----
var FIELD_DEFS = {
  character: [
    {id:'genf-name',label:'名称',hint:'角色叫什么？如"骑士战士"',type:'text',placeholder:'骑士战士',value:'骑士战士'},
    {id:'genf-view',label:'视角',hint:'游戏的观察角度',type:'select',opts:[{v:'top_down',t:'俯视'},{v:'side_view',t:'侧视'},{v:'front',t:'正面'},{v:'back',t:'背面'},{v:'three-quarter',t:'3/4侧面'}],value:'top_down'},
    {id:'genf-pose',label:'姿态',hint:'角色的动作姿态',type:'select',opts:[{v:'idle',t:'待机'},{v:'walking',t:'行走'},{v:'attacking',t:'攻击'},{v:'casting',t:'施法'},{v:'hurt',t:'受伤'},{v:'dead',t:'死亡'}],value:'idle'},
    {id:'genf-emotion',label:'表情',hint:'角色的情绪表达',type:'select',opts:[{v:'cute',t:'可爱'},{v:'angry',t:'愤怒'},{v:'serious',t:'严肃'},{v:'crazy',t:'疯狂'},{v:'happy',t:'开心'},{v:'sad',t:'悲伤'}],value:'serious'},
    {id:'genf-appearance',label:'外观',hint:'服装、体型、颜色、特征。如"铁盔、板甲"',type:'textarea',placeholder:'铁盔、板甲、坚定',value:'铁盔、板甲、坚定'},
    {id:'genf-weapon',label:'武器',hint:'留空不生成武器',type:'text',placeholder:'铁剑',value:''},
    {id:'genf-canvas-fill',label:'主体占比',hint:'控制主体占画布比例，85% 更饱满',type:'select',opts:[{v:'60%',t:'60% 较小'},{v:'75%',t:'75% 适中'},{v:'85%',t:'85% 饱满'}],value:'75%'},
    {id:'genf-complexity',label:'复杂度',hint:'控制细节精细程度',type:'select',opts:[{v:'simple',t:'简洁'},{v:'medium',t:'中等'},{v:'detailed',t:'丰富'}],value:'medium'},
    {id:'genf-color-palette',label:'配色',hint:'主色调方案',type:'text',placeholder:'红、黑、金',value:''},
    {id:'genf-outline-style',label:'描边',hint:'轮廓线风格',type:'select',opts:[{v:'clean',t:'清晰描边'},{v:'bold',t:'粗描边'},{v:'thin',t:'细描边'},{v:'pixel',t:'像素描边'},{v:'none',t:'无描边'}],value:'clean'},
    {id:'genf-background',label:'背景',hint:'图片背景类型',type:'select',opts:[{v:'transparent',t:'透明'},{v:'solid',t:'固定底色'}],value:'transparent'},
    {id:'genf-size',label:'尺寸',hint:'图片像素大小',type:'select',opts:[{v:'64x64',t:'64x64'},{v:'128x128',t:'128x128'},{v:'256x256',t:'256x256'},{v:'512x512',t:'512x512'}],value:'64x64'}
  ],
  enemy: [
    {id:'genf-name',label:'名称',hint:'敌人叫什么？如"骷髅兵"',type:'text',placeholder:'骷髅兵',value:'骷髅兵'},
    {id:'genf-view',label:'视角',hint:'观察角度',type:'select',opts:[{v:'top_down',t:'俯视'},{v:'side_view',t:'侧视'},{v:'front',t:'正面'},{v:'back',t:'背面'},{v:'three-quarter',t:'3/4侧面'}],value:'front'},
    {id:'genf-pose',label:'姿态',hint:'敌人的动作姿态',type:'select',opts:[{v:'idle',t:'待机'},{v:'walking',t:'行走'},{v:'attacking',t:'攻击'},{v:'casting',t:'施法'},{v:'hurt',t:'受伤'},{v:'dead',t:'死亡'}],value:'idle'},
    {id:'genf-emotion',label:'表情',hint:'敌人的情绪表达',type:'select',opts:[{v:'angry',t:'愤怒'},{v:'crazy',t:'疯狂'},{v:'serious',t:'严肃'},{v:'cute',t:'呆萌'},{v:'happy',t:'开心'}],value:'angry'},
    {id:'genf-appearance',label:'外观',hint:'体型、颜色、特征。如"白骨、红眼"',type:'textarea',placeholder:'白骨、红眼、暗黑',value:'白骨、红眼、暗黑'},
    {id:'genf-weapon',label:'武器',hint:'留空不生成武器',type:'text',placeholder:'骨刀',value:''},
    {id:'genf-canvas-fill',label:'主体占比',hint:'控制主体占画布比例，85% 更饱满',type:'select',opts:[{v:'60%',t:'60% 较小'},{v:'75%',t:'75% 适中'},{v:'85%',t:'85% 饱满'}],value:'75%'},
    {id:'genf-complexity',label:'复杂度',hint:'控制细节精细程度',type:'select',opts:[{v:'simple',t:'简洁'},{v:'medium',t:'中等'},{v:'detailed',t:'丰富'}],value:'medium'},
    {id:'genf-color-palette',label:'配色',hint:'主色调方案',type:'text',placeholder:'暗紫、红、黑',value:''},
    {id:'genf-outline-style',label:'描边',hint:'轮廓线风格',type:'select',opts:[{v:'clean',t:'清晰描边'},{v:'bold',t:'粗描边'},{v:'thin',t:'细描边'},{v:'pixel',t:'像素描边'},{v:'none',t:'无描边'}],value:'clean'},
    {id:'genf-background',label:'背景',hint:'图片背景类型',type:'select',opts:[{v:'transparent',t:'透明'},{v:'solid',t:'固定底色'}],value:'transparent'},
    {id:'genf-size',label:'尺寸',hint:'图片像素大小',type:'select',opts:[{v:'64x64',t:'64x64'},{v:'128x128',t:'128x128'},{v:'256x256',t:'256x256'},{v:'512x512',t:'512x512'}],value:'64x64'}
  ],
  item: [
    {id:'genf-name',label:'名称',hint:'道具叫什么？如"生命药水"',type:'text',placeholder:'生命药水',value:'生命药水'},
    {id:'genf-item_category',label:'类别',hint:'游戏分类',type:'select',opts:[{v:'weapon',t:'武器'},{v:'potion',t:'药水'},{v:'coin',t:'钱币'},{v:'key',t:'钥匙'},{v:'food',t:'食物'},{v:'gem',t:'宝石'}],value:'potion'},
    {id:'genf-appearance',label:'外观',hint:'形状、颜色、材质。如"红液、玻璃瓶"',type:'textarea',placeholder:'红液、玻璃瓶',value:'红液、玻璃瓶'},
    {id:'genf-canvas-fill',label:'主体占比',hint:'道具占画布比例',type:'select',opts:[{v:'60%',t:'60%'},{v:'75%',t:'75%'},{v:'85%',t:'85%'}],value:'75%'},
    {id:'genf-complexity',label:'复杂度',hint:'细节精细程度',type:'select',opts:[{v:'simple',t:'简洁'},{v:'medium',t:'中等'},{v:'detailed',t:'丰富'}],value:'medium'},
    {id:'genf-color-palette',label:'配色',hint:'主色调',type:'text',placeholder:'金、闪光',value:''},
    {id:'genf-outline-style',label:'描边',hint:'轮廓线风格',type:'select',opts:[{v:'clean',t:'清晰'},{v:'bold',t:'粗'},{v:'thin',t:'细'},{v:'pixel',t:'像素'},{v:'none',t:'无'}],value:'clean'},
    {id:'genf-size',label:'尺寸',hint:'图片像素大小',type:'select',opts:[{v:'64x64',t:'64x64'},{v:'128x128',t:'128x128'},{v:'256x256',t:'256x256'}],value:'64x64'}
  ],
  tile: [
    {id:'genf-name',label:'名称',hint:'瓦片叫什么？如"石砖地板"',type:'text',placeholder:'石砖地板',value:'石砖地板'},
    {id:'genf-tile_type',label:'类型',hint:'地图功能类型',type:'select',opts:[{v:'floor',t:'地板'},{v:'wall',t:'墙壁'},{v:'grass',t:'草地'},{v:'water',t:'水面'},{v:'lava',t:'岩浆'},{v:'road',t:'道路'}],value:'floor'},
    {id:'genf-material',label:'材质',hint:'视觉材质和纹理。如"灰石砖、青苔"',type:'text',placeholder:'灰石砖、青苔',value:'灰石砖、青苔'},
    {id:'genf-seamless',label:'无缝',hint:'是否可无缝重复',type:'select',opts:[{v:'true',t:'是（用于Tilemap平铺）'},{v:'false',t:'否'}],value:'true'},
    {id:'genf-complexity',label:'复杂度',hint:'细节精细程度',type:'select',opts:[{v:'simple',t:'简洁'},{v:'medium',t:'中等'},{v:'detailed',t:'丰富'}],value:'simple'},
    {id:'genf-color-palette',label:'配色',hint:'主色调',type:'text',placeholder:'灰、绿苔',value:''},
    {id:'genf-size',label:'尺寸',hint:'图片像素大小（建议32或64）',type:'select',opts:[{v:'32x32',t:'32x32'},{v:'64x64',t:'64x64'},{v:'128x128',t:'128x128'}],value:'32x32'}
  ],
  ui_icon: [
    {id:'genf-name',label:'名称',hint:'图标叫什么？如"生命值"',type:'text',placeholder:'生命值图标',value:'生命值图标'},
    {id:'genf-icon_purpose',label:'用途',hint:'游戏中的功能',type:'select',opts:[{v:'health',t:'生命'},{v:'coin',t:'货币'},{v:'skill',t:'技能'},{v:'inventory',t:'背包'},{v:'settings',t:'设置'},{v:'map',t:'地图'}],value:'health'},
    {id:'genf-shape',label:'形状',hint:'外框形状',type:'select',opts:[{v:'circle',t:'圆形'},{v:'square',t:'方形'},{v:'diamond',t:'菱形'},{v:'no_frame',t:'无边框'}],value:'circle'},
    {id:'genf-appearance',label:'外观',hint:'颜色、图案。如"红心、白底"',type:'textarea',placeholder:'红心、白底、简洁',value:'红心、白底、简洁'},
    {id:'genf-canvas-fill',label:'主体占比',hint:'图标占画布比例',type:'select',opts:[{v:'60%',t:'60%'},{v:'75%',t:'75%'},{v:'85%',t:'85%'}],value:'75%'},
    {id:'genf-color-palette',label:'配色',hint:'主色调',type:'text',placeholder:'红、白',value:''},
    {id:'genf-size',label:'尺寸',hint:'图片像素大小',type:'select',opts:[{v:'64x64',t:'64x64'},{v:'128x128',t:'128x128'},{v:'256x256',t:'256x256'}],value:'64x64'}
  ],
  effect: [
    {id:'genf-name',label:'名称',hint:'特效叫什么？如"火球爆炸"',type:'text',placeholder:'火球爆炸',value:'火球爆炸'},
    {id:'genf-effect_type',label:'类型',hint:'元素类型',type:'select',opts:[{v:'fire',t:'火焰'},{v:'ice',t:'冰霜'},{v:'lightning',t:'雷电'},{v:'healing',t:'治疗'},{v:'explosion',t:'爆炸'},{v:'poison',t:'毒气'},{v:'shield',t:'护盾'}],value:'fire'},
    {id:'genf-motion_feeling',label:'动势',hint:'运动形态',type:'select',opts:[{v:'burst',t:'爆发'},{v:'spiral',t:'螺旋'},{v:'slash',t:'斩击'},{v:'aura',t:'光环'},{v:'trail',t:'拖尾'},{v:'flicker',t:'闪烁'}],value:'burst'},
    {id:'genf-canvas-fill',label:'主体占比',hint:'特效占画布比例',type:'select',opts:[{v:'60%',t:'60%'},{v:'75%',t:'75%'},{v:'85%',t:'85%'}],value:'75%'},
    {id:'genf-complexity',label:'复杂度',hint:'特效细节程度',type:'select',opts:[{v:'simple',t:'简洁'},{v:'medium',t:'中等'},{v:'detailed',t:'丰富'}],value:'medium'},
    {id:'genf-color-palette',label:'配色',hint:'主色调',type:'text',placeholder:'橙红、亮黄',value:''},
    {id:'genf-size',label:'尺寸',hint:'图片像素大小',type:'select',opts:[{v:'64x64',t:'64x64'},{v:'128x128',t:'128x128'},{v:'256x256',t:'256x256'}],value:'64x64'}
  ]
};

function onTypeChange() {
  var type = document.getElementById('gen-type').value;
  document.querySelectorAll('#type-bar .type-btn').forEach(function(b){ b.classList.remove('active'); });
  var tb = document.querySelector('#type-bar .type-btn[data-type="'+type+'"]');
  if (tb) tb.classList.add('active');
  renderTypeFields(type);
}
function renderTypeFields(type) {
  var container = document.getElementById('gen-fields');
  var fields = FIELD_DEFS[type] || FIELD_DEFS.character;
  var examples = EXAMPLES[type] || [];
  var html = '';
  if (examples.length > 0) {
    html += '<div class="example-bar"><span style="font-size:.6rem;color:#64748b;margin-right:2px">示例:</span>';
    for (var e=0;e<examples.length;e++) html += '<button class="example-btn" onclick="fillExample('+JSON.stringify(type)+',EXAMPLES['+JSON.stringify(type)+']['+e+'])">'+examples[e].label+'</button>';
    html += '</div>';
  }
  for (var i=0;i<fields.length;i++) {
    var f = fields[i];
    html += '<div style="margin-bottom:12px"><label>'+f.label+'</label>';
    if (f.hint) html += '<div class="field-hint">'+f.hint+'</div>';
    if (f.type==='select') {
      html += '<select id="'+f.id+'" onchange="refreshPromptPreview()">';
      for (var j=0;j<f.opts.length;j++) html += '<option value="'+f.opts[j].v+'"'+(f.opts[j].v===f.value?' selected':'')+'>'+f.opts[j].t+'</option>';
      html += '</select>';
    } else if (f.type==='textarea') {
      html += '<textarea id="'+f.id+'" placeholder="'+(f.placeholder||'')+'" rows="3" oninput="refreshPromptPreview()">'+(f.value||'')+'</textarea>';
    } else {
      html += '<input id="'+f.id+'" placeholder="'+(f.placeholder||'')+'" value="'+(f.value||'')+'" oninput="refreshPromptPreview()">';
    }
    html += '</div>';
  }
  html += '<div style="font-size:.62rem;color:#64748b;margin:12px 0 4px">提示词标签</div>';
  html += renderChips(type);
  container.innerHTML = html;
  slimeActionHint(type);
  var isCh = (type === 'character' || type === 'enemy');
  document.getElementById('btn-random').style.display = isCh ? 'inline-block' : 'none';
  document.getElementById('btn-clear-chips').style.display = 'inline-block';
  updateCompletenessHint();
  setTimeout(refreshPromptPreview, 50);
}

function renderChips(type) {
  var defs = CHIP_DEFS[type]; if (!defs) return '';
  var html = '';
  for (var key in defs) {
    var g = defs[key];
    html += '<div class="chip-group" id="chip-group-'+key+'">';
    html += '<div class="chip-group-header'+(g.open?'':' collapsed')+'" onclick="toggleChipGroup(&quot;'+key+'&quot;)"><span class="arrow">&#9662;</span> '+g.label+'</div>';
    html += '<div class="chip-group-body">';
    for (var c=0;c<g.chips.length;c++) html += '<span class="chip" onclick="toggleChip(&quot;'+key+'&quot;,&quot;'+g.chips[c].replace(/"/g,'&quot;')+'&quot;)">'+g.chips[c]+'</span>';
    html += '</div></div>';
  }
  return html;
}

function slimeActionHint(type) {
  if (type !== 'enemy') return;
  var name = (getFieldVal('genf-name')||'').toLowerCase();
  var app = (getFieldVal('genf-appearance')||'').toLowerCase();
  var isSl = name.indexOf('slime')>=0||name.indexOf('史莱姆')>=0||name.indexOf('圆滚滚')>=0||app.indexOf('slime')>=0||app.indexOf('史莱姆')>=0||app.indexOf('圆滚滚')>=0;
  var el = document.getElementById('genf-slime-hint');
  if (el) el.remove();
  if (!isSl) return;
  var actionEl = document.getElementById('genf-action');
  if (!actionEl || !actionEl.parentElement) return;
  var hint = document.createElement('div');
  hint.id = 'genf-slime-hint';
  hint.style.cssText = 'font-size:.6rem;color:#fbbf24;margin-top:3px;line-height:1.3';
  hint.textContent = '史莱姆类敌人更适合待机/弹跳/攻击；如选行走，系统自动转弹跳姿态';
  actionEl.parentElement.appendChild(hint);
}

function composeDescription(type) {
  var parts=[];
  var an=getFieldVal('genf-name'),ap=getFieldVal('genf-appearance');
  var av=getFieldVal('genf-view'),pos=getFieldVal('genf-pose'),em=getFieldVal('genf-emotion');
  var cf=getFieldVal('genf-canvas-fill'),cx=getFieldVal('genf-complexity'),cp=getFieldVal('genf-color-palette'),os=getFieldVal('genf-outline-style'),bg=getFieldVal('genf-background');

  var typeMap={character:'Character',enemy:'Enemy',item:'Item',tile:'Tile',ui_icon:'UI Icon',effect:'Effect'};
  parts.push('Asset type: '+(typeMap[type]||type));

  if(an)parts.push('Subject: '+an);
  if(av){var vm={top_down:'top-down',side_view:'side',front:'front',back:'back','three-quarter':'three-quarter'};parts.push('View: '+(vm[av]||av));}
  if(pos){var pm={idle:'idle',walking:'walking',attacking:'attacking',casting:'casting',hurt:'hurt',dead:'dead'};parts.push('Pose: '+(pm[pos]||pos));}
  if(em){var emm={cute:'cute',angry:'angry',serious:'serious',crazy:'crazy',happy:'happy',sad:'sad'};parts.push('Emotion: '+(emm[em]||em));}
  if(cp)parts.push('Main colors: '+cp);
  if(cf)parts.push('Canvas fill: '+cf);
  if(bg)parts.push('Background: '+bg);
  if(cx){var cxm={simple:'simple',medium:'medium',detailed:'detailed'};parts.push('Complexity: '+(cxm[cx]||cx));}
  if(os)parts.push('Outline: '+os);

  if(ap)parts.push('Appearance: '+ap);
  if(type==='character'||type==='enemy'){
    var w=getFieldVal('genf-weapon');if(w)parts.push('Weapon: '+w);
  }
  if(type==='item'){var ic=getFieldVal('genf-item_category');if(ic)parts.push('Category: '+ic);}
  if(type==='tile'){var tt=getFieldVal('genf-tile_type'),tm=getFieldVal('genf-material'),ts=getFieldVal('genf-seamless');if(tt)parts.push('Tile type: '+tt);if(tm)parts.push('Material: '+tm);if(ts==='true')parts.push('Seamless repeatable');}
  if(type==='ui_icon'){var ip=getFieldVal('genf-icon_purpose'),sh=getFieldVal('genf-shape');if(ip)parts.push('Purpose: '+ip);if(sh)parts.push('Shape: '+sh);}
  if(type==='effect'){var et=getFieldVal('genf-effect_type'),mf=getFieldVal('genf-motion_feeling');if(et)parts.push('Effect type: '+et);if(mf)parts.push('Motion: '+mf);}

  return parts.join('; ');
}
function getGenParams() {
  var pid=getProjectId(),type=document.getElementById('gen-type').value;
  var manualOn=document.getElementById('manual-edit-toggle').checked;
  var manualText=document.getElementById('pd-manual-text').value.trim();
  var desc=(manualOn&&manualText)?manualText:composeDescription(type);
  return {
    project_id:pid,asset_type:type,description:desc,size:getFieldVal('genf-size')||'64x64',quantity:1,
    extra_params:{
      direction:getFieldVal('genf-view')||'',background:getFieldVal('genf-background')||'transparent',
      usage:type==='enemy'?'enemy_sprite':(type==='character'?'player_sprite':''),
      name:getFieldVal('genf-name'),view:getFieldVal('genf-view'),
      action:getFieldVal('genf-pose'),
      appearance:getFieldVal('genf-appearance'),weapon:getFieldVal('genf-weapon'),
      item_category:getFieldVal('genf-item_category'),tile_type:getFieldVal('genf-tile_type'),
      material:getFieldVal('genf-material'),seamless:getFieldVal('genf-seamless'),
      icon_purpose:getFieldVal('genf-icon_purpose'),shape:getFieldVal('genf-shape'),
      effect_type:getFieldVal('genf-effect_type'),motion_feeling:getFieldVal('genf-motion_feeling'),
      pose:getFieldVal('genf-pose'),camera_angle:getFieldVal('genf-view'),
      body_ratio:'',canvas_fill:getFieldVal('genf-canvas-fill'),
      outline_style:getFieldVal('genf-outline-style'),color_palette:getFieldVal('genf-color-palette'),
      emotion:getFieldVal('genf-emotion'),complexity:getFieldVal('genf-complexity'),
      animation_frame:'',forbidden_elements:['text','watermark','white background','frame','border']
    }
  };
}

function refreshPromptPreview() {
  var type=document.getElementById('gen-type').value,manualOn=document.getElementById('manual-edit-toggle').checked;
  var userParts=[];
  userParts.push({l:'类型',v:getAssetTypeName(type)});
  var fn=getFieldVal('genf-name'); if(fn)userParts.push({l:'名称',v:fn});
  var fv=getFieldVal('genf-view'); if(fv){var vm={top_down:'俯视',side_view:'侧视',front:'正面',back:'背面','three-quarter':'3/4侧'};userParts.push({l:'视角',v:vm[fv]||fv});}
  var fp=getFieldVal('genf-pose'); if(fp){var pm={idle:'待机',walking:'行走',attacking:'攻击',casting:'施法',hurt:'受伤',dead:'死亡'};userParts.push({l:'姿态',v:pm[fp]||fp});}
  var fe=getFieldVal('genf-emotion'); if(fe){var emm={cute:'可爱',angry:'愤怒',serious:'严肃',crazy:'疯狂',happy:'开心',sad:'悲伤'};userParts.push({l:'表情',v:emm[fe]||fe});}
  var fap=getFieldVal('genf-appearance'); if(fap)userParts.push({l:'外观',v:fap});
  var fw=getFieldVal('genf-weapon'); if(fw)userParts.push({l:'武器',v:fw});
  var fcf=getFieldVal('genf-canvas-fill'); if(fcf)userParts.push({l:'占比',v:fcf});
  var fcx=getFieldVal('genf-complexity'); if(fcx)userParts.push({l:'复杂度',v:fcx});
  var fcp=getFieldVal('genf-color-palette'); if(fcp)userParts.push({l:'配色',v:fcp});
  var fos=getFieldVal('genf-outline-style'); if(fos)userParts.push({l:'描边',v:fos});
  var fbg=getFieldVal('genf-background'); if(fbg)userParts.push({l:'背景',v:fbg==='transparent'?'透明':'固定底色'});
  var fc=getFieldVal('genf-item_category'); if(fc)userParts.push({l:'类别',v:fc});
  var ft=getFieldVal('genf-tile_type'); if(ft)userParts.push({l:'瓦片',v:ft});
  var fm=getFieldVal('genf-material'); if(fm)userParts.push({l:'材质',v:fm});
  var fs=getFieldVal('genf-seamless'); if(fs)userParts.push({l:'无缝',v:fs==='true'?'是':'否'});
  var fip=getFieldVal('genf-icon_purpose'); if(fip)userParts.push({l:'用途',v:fip});
  var fsh=getFieldVal('genf-shape'); if(fsh)userParts.push({l:'形状',v:fsh});
  var fet=getFieldVal('genf-effect_type'); if(fet)userParts.push({l:'特效',v:fet});
  var fmf=getFieldVal('genf-motion_feeling'); if(fmf)userParts.push({l:'动势',v:fmf});
  var fsz=getFieldVal('genf-size'); if(fsz)userParts.push({l:'尺寸',v:fsz});
  var uh='<div class="pd-section-title">用户输入</div>';
  if(userParts.length===0)uh+='<span class="pd-muted">未填写任何字段</span>';else for(var i=0;i<userParts.length;i++)uh+='<span class="pd-item">'+userParts[i].l+':'+userParts[i].v+'</span>';
  document.getElementById('pd-user').innerHTML=uh;
  var sh='<div class="pd-section-title">画风配置</div>';
  var art=document.getElementById('style-art').value,pal=document.getElementById('style-palette').value;
  if(art)sh+='<span class="pd-item active">画风:'+art+'</span>';if(pal)sh+='<span class="pd-item active">配色:'+pal+'</span>';
  if(!art&&!pal)sh+='<span class="pd-muted">未设置画风配置</span>';
  document.getElementById('pd-style').innerHTML=sh;
  var rules=getSystemRules(type),sysH='<div class="pd-section-title">系统规范</div>';
  for(var r=0;r<rules.length;r++)sysH+='<span class="pd-item active">'+rules[r]+'</span>';
  var isSl=type==='enemy'&&((getFieldVal('genf-name')||'').toLowerCase().indexOf('slime')>=0||(getFieldVal('genf-name')||'').toLowerCase().indexOf('史莱姆')>=0||(getFieldVal('genf-appearance')||'').toLowerCase().indexOf('slime')>=0);
  if(isSl){sysH+='<span class="pd-item warn">slime: walk auto-to-bouncing</span>';sysH+='<span class="pd-item active">round blob, simple face</span>';}
  if(art==='pixel_art')sysH+='<span class="pd-item active">hard edges, limited palette, no 3D</span>';
  var fcf2=getFieldVal('genf-canvas-fill');if(fcf2)sysH+='<span class="pd-item active">canvas fill: '+fcf2+'</span>';
  var fcp2=getFieldVal('genf-complexity');if(fcp2)sysH+='<span class="pd-item active">complexity: '+fcp2+'</span>';
  document.getElementById('pd-system').innerHTML=sysH;
  document.getElementById('pd-negative').innerHTML='<div class="pd-section-title">Negative</div><span class="pd-text">3d render, plastic toy, smooth gradient, soft lighting, text, watermark, white background, white rectangle, border, frame, cropped body, tiny character, multiple characters, complex scene, realistic photo</span>';
  if(manualOn){var mt=document.getElementById('pd-manual-text');if(!mt.value)mt.value=composeDescription(type);document.getElementById('pd-manual-area').style.display='block';}
}
var SYSTEM_RULES={character:['2D sprite','full body','centered','transparent bg','clean silhouette','Unity ready'],enemy:['2D sprite','full body','centered','transparent bg','clean silhouette','Unity ready'],item:['item icon','centered','transparent bg','simple silhouette'],tile:['2D tile','top-down','edge-matchable','Unity Tilemap'],ui_icon:['UI icon','centered','transparent bg','high contrast','no text'],effect:['VFX sprite','centered','transparent bg','high contrast','no scene']};
function getSystemRules(t){return SYSTEM_RULES[t]||SYSTEM_RULES.character;}
function toggleManualEdit(){var on=document.getElementById('manual-edit-toggle').checked;document.getElementById('pd-manual-area').style.display=on?'block':'none';refreshPromptPreview();}

function startProgressSteps(){progressStepIndex=0;renderProgress();progressTimer=setInterval(function(){progressStepIndex++;if(progressStepIndex>progressSteps.length)progressStepIndex=progressSteps.length;renderProgress();},2000);}
function stopProgressSteps(){if(progressTimer){clearInterval(progressTimer);progressTimer=null;}}
function renderProgress(){var p=document.getElementById('gen-progress'),h='<div class="progress-bar">';for(var i=0;i<progressSteps.length;i++){var c='pending',ic='<span style="width:12px;display:inline-block;text-align:center;font-size:.6rem;color:#475569">'+(i+1)+'</span>';if(i<progressStepIndex){c='done';ic='<span style="color:#4ade80;font-weight:700">&#10003;</span>';}else if(i===progressStepIndex){c='active';ic='<span class="step-spinner"></span>';}h+='<div class="progress-step '+c+'">'+ic+progressSteps[i]+'</div>';}h+='</div>';p.innerHTML=h;}
function markAllProgressDone(){progressStepIndex=progressSteps.length;renderProgress();}

async function generateAsset() {
  var params=getGenParams();lastGenParams=params;
  var btn=document.getElementById('btn-generate'),regenBtn=document.getElementById('btn-regenerate'),
      progress=document.getElementById('gen-progress'),result=document.getElementById('gen-result'),errArea=document.getElementById('gen-error');
  result.style.display='none';result.innerHTML='';errArea.style.display='none';errArea.innerHTML='';regenBtn.style.display='none';progress.innerHTML='';
  btn.textContent='生成中...';btn.disabled=true;startProgressSteps();
  try {
    var data=await api(API+'/generations',{method:'POST',body:JSON.stringify(params)});markAllProgressDone();
    if(data.success&&data.task&&data.task.status==='succeeded'){showResultPanel(params,data.task);regenBtn.style.display='inline-block';loadAssets();}else showGenError((data.task&&data.task.error_message)||data.error||'Unknown');
  }catch(e){stopProgressSteps();showGenError(e.message);}
  btn.textContent='生成素材';btn.disabled=false;
}
function showResultPanel(params,task){
  var p=params.extra_params||{},pu=task.preview_url||'',du=task.download_url||'',desc=params.description;
  var tags=[];if(p.name)tags.push(p.name);if(p.view)tags.push(p.view);if(p.pose)tags.push(p.pose);if(p.emotion)tags.push(p.emotion);if(p.canvas_fill)tags.push('fill:'+p.canvas_fill);
  var ph=document.getElementById('preview-placeholder');if(ph)ph.style.display='none';
  var imgArea=document.getElementById('gen-preview-img-area');
  if(pu)imgArea.innerHTML='<div style="text-align:center;background-image:repeating-conic-gradient(#0b1120 0 25%,#111827 0 50%);background-size:14px 14px;border-radius:7px;padding:12px"><img class="preview-img-lg" src="'+pu+'" onerror="this.style.display=\\x27none\\x27;this.parentElement.innerHTML=\\x27<div class=preview-placeholder><span>预览加载失败</span></div>\\x27"></div>';
  var tagH='';for(var t=0;t<tags.length;t++)tagH+='<span class="rp-tag">'+tags[t]+'</span>';
  var h='<div class="rp-meta">'+tagH+'</div>';
  if(desc)h+='<div class="rp-section"><div class="rp-label">Prompt</div><div class="rp-text mono" style="max-height:60px;overflow-y:auto">'+escapeHtml(desc)+'</div></div>';
  h+='<div class="rp-actions"><a href="'+du+'" class="btn-success btn-sm" style="text-decoration:none">下载</a><button class="btn-outline btn-sm" onclick="copyText('+JSON.stringify(desc)+')">复制</button><button class="btn-secondary btn-sm" onclick="regenerateWithSameParams()">重生成</button><button class="btn-outline btn-sm" onclick="toggleResultModify()">修改</button></div>';
  h+='<div class="rp-section" style="margin-top:8px;padding-top:6px;border-top:1px solid #1e293b"><div class="rp-label">快捷优化</div><div style="display:flex;gap:4px;flex-wrap:wrap;margin-top:4px">';
  h+='<button class="example-btn" onclick="quickOptimize('+JSON.stringify('make it stricter pixel art, hard pixel edges, limited palette')+')">更像像素风</button>';
  h+='<button class="example-btn" onclick="quickOptimize('+JSON.stringify('add stronger dark outline, clearer silhouette')+')">增强轮廓</button>';
  h+='<button class="example-btn" onclick="quickOptimize('+JSON.stringify('avoid 3D toy-like rendering, flat 2D sprite style')+')">减少3D感</button>';
  h+='<button class="example-btn" onclick="quickOptimize('+JSON.stringify('simplify details, readable at 64x64')+')">适合64x64</button>';
  h+='</div></div><div id="result-optimize-progress" style="margin-top:4px"></div>';
  h+='<div class="result-modify-area" id="result-modify-area" style="display:none"><label style="font-size:.6rem;color:#94a3b8">修改意见</label><div class="rm-row"><input id="result-modify-input" placeholder="如：改成红色 / 更可爱 / 武器更明显"><button class="btn-primary btn-sm" onclick="modifyFromResult()">生成修改版</button></div><div id="result-modify-progress" style="margin-top:4px"></div></div>';

  if(task.checks||task.quality_result){
    var checks=task.checks||(task.quality_result&&task.quality_result.checks)||[];
    if(checks.length>0){
      h+='<div style="margin-top:8px;padding-top:6px;border-top:1px solid #1e293b"><div class="rp-label" style="font-size:.6rem;color:#94a3b8;margin-bottom:4px">质量检查</div><ul class="quality-check-list">';
      for(var c=0;c<checks.length;c++){
        var ch=checks[c],cls=ch.passed?'pass':'warn',icon=ch.passed?'\u2713':'\u26A0';
        h+='<li class="'+cls+'"><span class="qc-icon">'+icon+'</span> '+escapeHtml(ch.name)+': '+escapeHtml(ch.message||(ch.passed?'OK':'Warning'))+'</li>';
      }
      h+='</ul></div>';
    }
  }

  document.getElementById('gen-result').innerHTML=h;document.getElementById('gen-result').style.display='block';
  renderQualityCheckResults(task);
  renderQualityCheckResults(task);
}
function renderQualityCheckResults(task) {
  var qc=document.getElementById('gen-qc-results');if(!qc)return;
  var checks=task.checks||(task.quality_result&&task.quality_result.checks)||[];
  if(checks.length===0){qc.innerHTML='';return;}
  var h='<div style="margin-top:8px"><div style="font-size:.62rem;color:#94a3b8;margin-bottom:4px;font-weight:600">质量检测</div><ul class="quality-check-list">';
  var labelMap={image_exists:'文件存在',is_png:'PNG格式',file_size:'文件大小',size_match:'尺寸匹配',alpha_channel:'Alpha通道',transparent_background:'透明背景',subject_fill_ratio:'主体占比',centered_subject:'居中',near_white_background:'白底残留',white_background_removed:'白底清除'};
  for(var c=0;c<checks.length;c++){
    var ch=checks[c],cls=ch.passed?'pass':'warn',icon=ch.passed?'\u2713':'\u26A0';
    var name=ch.name||'check',label=labelMap[name]||name;
    h+='<li class="'+cls+'"><span class="qc-icon">'+icon+'</span> '+label+': '+escapeHtml(ch.message||(ch.passed?'通过':'注意'))+'</li>';
  }
  h+='</ul></div>';
  qc.innerHTML=h;
}
function toggleResultModify(){var a=document.getElementById('result-modify-area');a.style.display=a.style.display==='none'?'block':'none';}
async function quickOptimize(inst){
  if(!lastGenParams)return;var pg=document.getElementById('result-optimize-progress');pg.innerHTML='<div style="padding:5px 9px;background:rgba(59,130,246,.15);border:1px solid rgba(59,130,246,.3);border-radius:5px;font-size:.6rem;color:#60a5fa;display:flex;align-items:center;gap:5px"><span class="step-spinner" style="width:10px;height:10px"></span>优化中...</div>';
  var np=JSON.parse(JSON.stringify(lastGenParams));np.description=(lastGenParams.description||'')+', '+inst;
  try{var d=await api(API+'/generations',{method:'POST',body:JSON.stringify(np)});if(d.success&&d.task&&d.task.status==='succeeded'){pg.innerHTML='<div class="msg msg-success" style="font-size:.6rem">优化成功</div>';showResultPanel(np,d.task);loadAssets();}else pg.innerHTML='<div class="msg msg-error" style="font-size:.6rem">'+translateError((d.task&&d.task.error_message)||d.error||'')+'</div>';}catch(e){pg.innerHTML='<div class="msg msg-error" style="font-size:.6rem">'+translateError(e.message)+'</div>';}
}
async function modifyFromResult(){
  var inst=document.getElementById('result-modify-input').value.trim();if(!inst){msg('请输入修改意见','info');return;}if(!lastGenParams)return;
  var pg=document.getElementById('result-modify-progress');pg.innerHTML='<div style="padding:5px 9px;background:rgba(59,130,246,.15);border:1px solid rgba(59,130,246,.3);border-radius:5px;font-size:.6rem;color:#60a5fa;display:flex;align-items:center;gap:5px"><span class="step-spinner" style="width:10px;height:10px"></span>生成中...</div>';
  var np=JSON.parse(JSON.stringify(lastGenParams));np.description=(lastGenParams.description||'')+', '+inst;
  try{var d=await api(API+'/generations',{method:'POST',body:JSON.stringify(np)});if(d.success&&d.task&&d.task.status==='succeeded'){pg.innerHTML='<div class="msg msg-success" style="font-size:.6rem">修改版成功</div>';showResultPanel(np,d.task);loadAssets();}else pg.innerHTML='<div class="msg msg-error" style="font-size:.6rem">'+translateError((d.task&&d.task.error_message)||d.error||'')+'</div>';}catch(e){pg.innerHTML='<div class="msg msg-error" style="font-size:.6rem">'+translateError(e.message)+'</div>';}
}
async function regenerateWithSameParams(){if(!lastGenParams){msg('无参数','info');return;}await generateAsset();}
function showGenError(errMsg){
  var errArea=document.getElementById('gen-error'),result=document.getElementById('gen-result'),regenBtn=document.getElementById('btn-regenerate');
  result.style.display='none';errArea.style.display='block';
  errArea.innerHTML='<div class="msg msg-error" style="margin-top:8px"><strong>生成失败</strong><br>'+translateError(errMsg)+'<br><button class="gen-retry-btn" onclick="retryGenerate()">再试一次</button></div>';
  regenBtn.style.display='inline-block';
}
function retryGenerate(){document.getElementById('gen-error').style.display='none';generateAsset();}
function restoreFieldsFromParams(params){
  if(!params)return;var t=params.asset_type||'character';selectType(t);renderTypeFields(t);
  var p=params.extra_params||{},fm={name:'genf-name',view:'genf-view',action:'genf-action',pose:'genf-pose',appearance:'genf-appearance',weapon:'genf-weapon','canvas-fill':'genf-canvas-fill',complexity:'genf-complexity','outline-style':'genf-outline-style','color-palette':'genf-color-palette',emotion:'genf-emotion',background:'genf-background',item_category:'genf-item_category',tile_type:'genf-tile_type',material:'genf-material',seamless:'genf-seamless',icon_purpose:'genf-icon_purpose',shape:'genf-shape',effect_type:'genf-effect_type',motion_feeling:'genf-motion_feeling'};
  for(var k in fm){if(p[k]!==undefined&&p[k]!==null){var el=document.getElementById(fm[k]);if(el)el.value=p[k];}}
}
async function regenerateAsset(){if(!lastGenParams){msg('请先生成','info');return;}restoreFieldsFromParams(lastGenParams);await generateAsset();}
function copyText(text){if(navigator.clipboard&&navigator.clipboard.writeText)navigator.clipboard.writeText(text).then(function(){toast('已复制','success');}).catch(function(){fallbackCopy(text);});else fallbackCopy(text);}
function fallbackCopy(text){var ta=document.createElement('textarea');ta.value=text;ta.style.position='fixed';ta.style.left='-9999px';document.body.appendChild(ta);ta.select();try{document.execCommand('copy');toast('已复制','success');}catch(e){toast('复制失败','error');}document.body.removeChild(ta);}

// ---- Detail Modal ----
var currentDetailAsset=null;
function setModifyInput(t){document.getElementById('modify-input').value=t;}
function findAssetById(id){for(var i=0;i<cachedAssets.length;i++)if(cachedAssets[i].id===id)return cachedAssets[i];return null;}
function openDetail(aid){
  var a=findAssetById(aid);if(!a){msg('素材未找到','error');return;}currentDetailAsset=a;
  var meta=a.metadata||{},desc=meta.description||'',prompt=meta.final_prompt||'';
  document.getElementById('detail-img').src=a.preview_url||'';document.getElementById('detail-name').textContent=a.name||'';
  var rows='';rows+='<div class="detail-row"><span class="dl">类型</span><span class="dv">'+getAssetTypeName(a.asset_type)+'</span></div>';
  if(a.width&&a.height)rows+='<div class="detail-row"><span class="dl">尺寸</span><span class="dv">'+a.width+' x '+a.height+'</span></div>';
  rows+='<div class="detail-row"><span class="dl">时间</span><span class="dv">'+formatDate(a.created_at)+'</span></div>';
  if(desc)rows+='<div class="detail-row"><span class="dl">描述</span><span class="dv">'+escapeHtml(desc)+'</span></div>';
  if(prompt)rows+='<div class="detail-row"><span class="dl">Prompt</span><span class="dv mono">'+escapeHtml(prompt)+'</span></div>';
  document.getElementById('detail-rows').innerHTML=rows;
  var act='<a href="'+escapeHtml(a.download_url||'')+'" class="btn-success btn-sm" style="text-decoration:none">下载</a><button class="btn-outline btn-sm" onclick="copyText('+JSON.stringify(prompt||desc)+')">复制 Prompt</button><button class="btn-secondary btn-sm" onclick="regenerateFromAsset('+JSON.stringify(a.asset_type)+','+JSON.stringify(desc)+','+JSON.stringify(meta.size||'')+');closeDetail()">重生成</button><button class="btn-danger btn-sm" onclick="deleteFromDetail('+JSON.stringify(a.id)+')">删除</button>';
  document.getElementById('detail-actions').innerHTML=act;
  var ex='<button onclick="setModifyInput(\u6539\u6210\u7ea2\u8272)">改成红色</button><button onclick="setModifyInput(\u66f4\u50cf\u50cf\u7d20\u98ce)">更像像素风</button><button onclick="setModifyInput(\u6b66\u5668\u66f4\u660e\u663e)">武器更明显</button><button onclick="setModifyInput(\u53bb\u6389\u80cc\u666f\u6742\u7269)">去掉背景杂物</button>';
  document.getElementById('modify-examples').innerHTML=ex;document.getElementById('modify-input').value='';document.getElementById('modify-progress').innerHTML='';
  document.getElementById('detail-modal').classList.add('active');
}
function closeDetail(){document.getElementById('detail-modal').classList.remove('active');currentDetailAsset=null;}
async function modifyCurrentAsset(){
  if(!currentDetailAsset)return;var inst=document.getElementById('modify-input').value.trim();if(!inst){msg('请输入修改意见','info');return;}
  var a=currentDetailAsset,meta=a.metadata||{},bd=meta.description||a.name||'',t=a.asset_type,sz=meta.size||(a.width&&a.height?a.width+'x'+a.height:'64x64');
  var btn=document.getElementById('btn-modify'),pg=document.getElementById('modify-progress');btn.textContent='生成中...';btn.disabled=true;
  pg.innerHTML='<div style="padding:5px 9px;background:rgba(59,130,246,.15);border:1px solid rgba(59,130,246,.3);border-radius:5px;font-size:.6rem;color:#60a5fa;display:flex;align-items:center;gap:5px"><span class="step-spinner"></span>生成中...</div>';
  var np={project_id:getProjectId(),asset_type:t,description:bd+', '+inst,size:sz,quantity:1,extra_params:{name:meta.name||a.name,appearance:inst,background:'transparent',direction:'',usage:t==='enemy'?'enemy_sprite':(t==='character'?'player_sprite':''),view:meta.view||'',action:meta.action||'',pose:meta.pose||'',emotion:meta.emotion||'',canvas_fill:meta.canvas_fill||'75%',complexity:meta.complexity||'medium',color_palette:meta.color_palette||'',outline_style:meta.outline_style||'clean',weapon:meta.weapon||'',item_category:meta.item_category||'',tile_type:meta.tile_type||'',material:meta.material||'',seamless:meta.seamless||'',icon_purpose:meta.icon_purpose||'',shape:meta.shape||'',effect_type:meta.effect_type||'',motion_feeling:meta.motion_feeling||'',forbidden_elements:['text','watermark','white background','frame','border']}};
  try{var d=await api(API+'/generations',{method:'POST',body:JSON.stringify(np)});if(d.success&&d.task&&d.task.status==='succeeded'){pg.innerHTML='<div class="msg msg-success" style="font-size:.6rem">修改版成功</div>';closeDetail();loadAssets();}else pg.innerHTML='<div class="msg msg-error" style="font-size:.6rem">'+translateError((d.task&&d.task.error_message)||d.error||'')+'</div>';}catch(e){pg.innerHTML='<div class="msg msg-error" style="font-size:.6rem">'+translateError(e.message)+'</div>';}
  btn.textContent='生成修改版';btn.disabled=false;
}
async function deleteFromDetail(aid){if(!confirm('确定删除？'))return;try{var d=await api(API+'/assets/'+aid,{method:'DELETE'});if(d.success){closeDetail();loadAssets();}else msg('删除失败','error');}catch(e){msg('删除失败:'+translateError(e.message),'error');}}

// ---- Asset Library ----
function setFilter(type,btn){currentFilter=type;document.querySelectorAll('#filter-types .filter-btn').forEach(function(b){b.classList.remove('active');});if(btn)btn.classList.add('active');renderAssets();}
async function loadAssets(){
  var pid=getProjectId(),container=document.getElementById('asset-list');container.innerHTML='<div style="text-align:center;padding:24px;color:#64748b;font-size:.7rem">加载中...</div>';
  try{
    var data=await api(API+'/projects/'+pid+'/assets');
    if(!data.success||!data.assets||data.assets.length===0){
      cachedAssets=[];container.innerHTML='<div class="empty-state"><div class="empty-icon" style="font-size:2.5rem;opacity:.2">&#9635;</div><div class="empty-title">还没有素材</div><div class="empty-hint">选择一个模板或填写描述，生成你的第一个游戏素材</div><div class="empty-actions"><button class="btn-primary btn-sm" onclick="applyTemplate(QUICK_TEMPLATES[0])">像素恶魔</button><button class="btn-primary btn-sm" onclick="applyTemplate(QUICK_TEMPLATES[2])">金币</button></div></div>';
      document.getElementById('stats-bar').innerHTML='';return;
    }
    cachedAssets=data.assets;renderAssets();
  }catch(e){container.innerHTML='<div class="msg msg-error">素材库加载失败<br><span style="font-size:.65rem;color:#fca5a5">可能是后端服务未启动或项目 ID 不存在</span><br><button class="btn-outline btn-xs" onclick="loadAssets()" style="margin-top:6px">重试</button></div>';}
}
function renderAssets(){
  var container=document.getElementById('asset-list'),searchText=(document.getElementById('search-input').value||'').toLowerCase();
  var filtered=cachedAssets.filter(function(a){if(currentFilter!=='all'&&a.asset_type!==currentFilter)return false;if(searchText){var n=(a.name||'').toLowerCase(),d=(a.metadata&&a.metadata.description||'').toLowerCase(),p=(a.metadata&&a.metadata.final_prompt||'').toLowerCase();if(n.indexOf(searchText)<0&&d.indexOf(searchText)<0&&p.indexOf(searchText)<0)return false;}return true;});
  document.getElementById('stats-bar').innerHTML='共 <strong>'+cachedAssets.length+'</strong> 个'+(filtered.length!==cachedAssets.length?'，显示 <strong>'+filtered.length+'</strong> 个':'');
  if(filtered.length===0){container.innerHTML='<div class="empty-state"><div class="empty-icon" style="font-size:2.5rem;opacity:.2">&#9635;</div><div class="empty-title">'+(cachedAssets.length===0?'还没有素材':'无匹配')+'</div><div class="empty-hint">'+(cachedAssets.length===0?'选择模板或填写描述，生成第一个素材':'试试调整筛选条件')+'</div></div>';return;}
  container.innerHTML='<div class="asset-grid">'+filtered.map(function(a){var meta=a.metadata||{},desc=meta.description||'',prompt=meta.final_prompt||'',pd=prompt.length>60?prompt.substring(0,60)+'...':prompt,h='<div class="asset-card">';h+='<div class="asset-card-img" onclick="openDetail('+JSON.stringify(a.id)+')"><img src="'+escapeHtml(a.preview_url||'')+'" loading="lazy" onerror="this.parentElement.innerHTML=\\x27<span style=font-size:.6rem;color:#64748b>加载失败</span>\\x27"></div>';h+='<div class="asset-card-body"><div class="asset-card-name" title="'+escapeHtml(a.name)+'">'+escapeHtml(a.name)+'</div>';h+='<span class="asset-card-type '+(a.asset_type==='enemy'?'enemy':'')+'">'+getAssetTypeName(a.asset_type)+'</span><span class="asset-card-date">'+formatDate(a.created_at)+'</span>';h+='<div class="asset-card-actions"><a href="'+escapeHtml(a.download_url||'')+'" class="btn-success btn-xs" style="text-decoration:none">下载</a><button class="btn-outline btn-xs" onclick="openDetail('+JSON.stringify(a.id)+')">详情</button></div></div></div>';return h;}).join('')+'</div>';
}
function regenerateFromAsset(at,desc,sz){selectType(at||'character');renderTypeFields(at||'character');var se=document.getElementById('genf-size');if(se&&sz)se.value=sz;var ae=document.getElementById('genf-appearance');if(ae&&desc)ae.value=desc;var ne=document.getElementById('genf-name');if(ne&&desc)ne.value=desc.split(',')[0]||desc;generateAsset();}
async function deleteAsset(aid){if(!confirm('确定删除？'))return;try{var d=await api(API+'/assets/'+aid,{method:'DELETE'});if(d.success){loadAssets();msg('已删除','success');}else msg('删除失败','error');}catch(e){msg('删除失败:'+translateError(e.message),'error');}}
document.addEventListener('keydown',function(e){if(e.key==='Escape')closeDetail();});
renderTemplates();onTypeChange();loadAssets();
</script>
</body>
</html>"""


@app.get("/", response_class=HTMLResponse)
def index():
    return HTMLResponse(content=INDEX_HTML)
