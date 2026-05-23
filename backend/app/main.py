# FastAPI application entry point
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
body{font-family:system-ui,-apple-system,sans-serif;background:#1a1a2e;color:#e0e0e0;min-height:100vh}
h1{text-align:center;padding:20px;color:#e94560;font-size:1.8rem}
h2{color:#e94560;margin-bottom:12px;font-size:1.2rem}
.container{max-width:1000px;margin:0 auto;padding:0 20px 40px}
.card{background:#16213e;border-radius:10px;padding:20px;margin-bottom:16px;border:1px solid #0f3460}
.row{display:flex;gap:12px;flex-wrap:wrap}
.col{flex:1;min-width:200px}
label{display:block;margin-bottom:4px;font-size:.8rem;color:#a0a0c0}
input,select,textarea{width:100%;padding:8px 12px;border-radius:6px;border:1px solid #0f3460;background:#1a1a2e;color:#e0e0e0;font-size:.9rem}
textarea{resize:vertical;min-height:60px}
button{padding:10px 24px;border-radius:6px;border:none;cursor:pointer;font-size:.9rem;font-weight:600;transition:background .2s}
.btn-primary{background:#e94560;color:#fff}
.btn-primary:hover{background:#c73552}
.btn-secondary{background:#0f3460;color:#e0e0e0}
.btn-secondary:hover{background:#1a4278}
.btn-danger{background:#c0392b;color:#fff}
.btn-danger:hover{background:#a93226}
.btn-sm{padding:6px 14px;font-size:.8rem}
.msg{padding:10px 14px;border-radius:6px;margin-bottom:12px;font-size:.85rem}
.msg-success{background:#0a3d0a;border:1px solid #27ae60;color:#2ecc71}
.msg-error{background:#3d0a0a;border:1px solid #e74c3c;color:#e74c3c}
.msg-info{background:#0a1a3d;border:1px solid #3498db;color:#3498db}
.result-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:12px;margin-top:12px}
.result-item{background:#0f3460;border-radius:8px;overflow:hidden;text-align:center;padding:10px}
.result-item img{max-width:100%;max-height:150px;object-fit:contain;background:repeating-conic-gradient(#1a1a2e 0 25%,#222244 0 50%) 50%/16px 16px}
.result-item .name{font-size:.8rem;margin-top:6px;color:#a0a0c0;word-break:break-all}
.result-item .actions{margin-top:6px;display:flex;gap:6px;justify-content:center}
.tab-bar{display:flex;gap:4px;margin-bottom:16px}
.tab-bar button{padding:8px 16px;border-radius:6px 6px 0 0;background:#16213e;color:#a0a0c0;border:1px solid #0f3460;border-bottom:none;font-size:.85rem}
.tab-bar button.active{background:#0f3460;color:#e94560}
.tab-content{display:none}
.tab-content.active{display:block}
.status-badge{display:inline-block;padding:2px 8px;border-radius:4px;font-size:.75rem;margin-left:8px}
.status-succeeded{background:#0a3d0a;color:#2ecc71}
.status-failed{background:#3d0a0a;color:#e74c3c}
.status-running{background:#3d3a00;color:#f1c40f}
.status-pending{background:#0a1a3d;color:#3498db}
.loading{display:inline-block;width:14px;height:14px;border:2px solid #e94560;border-top-color:transparent;border-radius:50%;animation:spin .6s linear infinite;margin-left:8px;vertical-align:middle}
@keyframes spin{to{transform:rotate(360deg)}}
pre{background:#1a1a2e;padding:10px;border-radius:6px;overflow-x:auto;font-size:.8rem}
</style>
</head>
<body>
<h1>AI 2D Game Asset Generator</h1>
<div class="container">

  <div id="msg-container"></div>

  <div class="tab-bar">
    <button class="active" onclick="switchTab('create')">1. 创建项目</button>
    <button onclick="switchTab('style')">2. 画风配置</button>
    <button onclick="switchTab('generate')">3. 生成素材</button>
    <button onclick="switchTab('assets')">4. 素材管理</button>
  </div>

  <div id="tab-create" class="tab-content active">
    <div class="card">
      <h2>创建项目</h2>
      <div class="row">
        <div class="col">
          <label>项目名称</label>
          <input id="project-name" placeholder="地牢像素RPG" value="我的游戏">
        </div>
        <div class="col">
          <label>项目ID</label>
          <input id="project-id" placeholder="project_default" value="project_default" readonly style="opacity:.6">
        </div>
      </div>
      <div style="margin-top:10px">
        <label>项目描述</label>
        <input id="project-desc" placeholder="一款俯视角像素风地牢游戏">
      </div>
      <div style="margin-top:14px">
        <button class="btn-primary" onclick="createProject()">创建项目</button>
      </div>
    </div>
  </div>

  <div id="tab-style" class="tab-content">
    <div class="card">
      <h2>项目画风配置</h2>
      <div class="row">
        <div class="col">
          <label>画风</label>
          <select id="style-art">
            <option value="pixel_art">像素风</option>
            <option value="cartoon">卡通风</option>
            <option value="hand_drawn">手绘风</option>
          </select>
        </div>
        <div class="col">
          <label>视角类型</label>
          <select id="style-view">
            <option value="top_down">俯视角</option>
            <option value="side_view">侧视角</option>
            <option value="isometric">等角视角</option>
          </select>
        </div>
        <div class="col">
          <label>配色方案</label>
          <select id="style-palette">
            <option value="dark_dungeon">暗黑地牢</option>
            <option value="bright_forest">明亮森林</option>
            <option value="cyberpunk">赛博朋克</option>
            <option value="custom">自定义</option>
          </select>
        </div>
        <div class="col">
          <label>默认尺寸</label>
          <select id="style-size">
            <option value="32x32">32x32</option>
            <option value="64x64" selected>64x64</option>
            <option value="128x128">128x128</option>
          </select>
        </div>
      </div>
      <div class="row" style="margin-top:10px">
        <div class="col">
          <label>提示词规则（每次生成自动附加）</label>
          <textarea id="style-prompt-rules" placeholder="居中的精灵图，清晰的轮廓">centered sprite, clean silhouette</textarea>
        </div>
        <div class="col">
          <label>反向提示词规则</label>
          <textarea id="style-neg-rules" placeholder="无文字，无水印，无杂乱背景">no text, no watermark, no background clutter</textarea>
        </div>
      </div>
      <div style="margin-top:14px">
        <button class="btn-primary" onclick="saveStyle()">保存画风配置</button>
      </div>
    </div>
  </div>

  <div id="tab-generate" class="tab-content">
    <div class="card">
      <h2>生成素材</h2>
      <div class="row">
        <div class="col">
          <label>素材类型</label>
          <select id="gen-type">
            <option value="character">角色</option>
            <option value="item">物品</option>
            <option value="tile">地形/瓦片</option>
            <option value="ui_icon">UI图标</option>
          </select>
        </div>
        <div class="col">
          <label>尺寸</label>
          <select id="gen-size">
            <option value="32x32">32x32</option>
            <option value="64x64" selected>64x64</option>
            <option value="128x128">128x128</option>
          </select>
        </div>
        <div class="col">
          <label>数量</label>
          <select id="gen-quantity">
            <option value="1">1</option>
          </select>
        </div>
      </div>
      <div style="margin-top:10px">
        <label>描述（描述你想生成的内容）</label>
        <textarea id="gen-desc" placeholder="手持木杖的蓝袍法师" rows="3">blue robe mage holding a wooden staff</textarea>
      </div>
      <div class="row" style="margin-top:10px">
        <div class="col">
          <label>朝向</label>
          <select id="gen-direction">
            <option value="right">右</option>
            <option value="left">左</option>
            <option value="front">前</option>
            <option value="back">后</option>
          </select>
        </div>
        <div class="col">
          <label>背景</label>
          <select id="gen-bg">
            <option value="transparent">透明</option>
            <option value="white">白色</option>
            <option value="black">黑色</option>
          </select>
        </div>
        <div class="col">
          <label>用途</label>
          <select id="gen-usage">
            <option value="player_sprite">玩家精灵</option>
            <option value="enemy_sprite">敌人精灵</option>
            <option value="npc_sprite">NPC精灵</option>
            <option value="ui_element">UI元素</option>
            <option value="environment">环境</option>
            <option value="prop">道具</option>
          </select>
        </div>
      </div>
      <div style="margin-top:14px">
        <button class="btn-primary" id="btn-generate" onclick="generateAsset()">生成素材</button>
        <span id="gen-loading" style="display:none;margin-left:12px;color:#e94560">正在生成... <span class="loading"></span></span>
      </div>
      <div id="gen-result" style="margin-top:16px"></div>
    </div>
  </div>

  <div id="tab-assets" class="tab-content">
    <div class="card">
      <h2>已生成素材 <button class="btn-secondary btn-sm" style="float:right" onclick="loadAssets()">刷新</button></h2>
      <div id="asset-list" class="result-grid"></div>
    </div>
  </div>

</div>

<script>
const API = '/api';

function msg(text, type) {
  const c = document.getElementById('msg-container');
  c.innerHTML = `<div class="msg msg-${type}">${text}</div>`;
  setTimeout(() => c.innerHTML = '', 5000);
}

function switchTab(name) {
  document.querySelectorAll('.tab-content').forEach(e => e.classList.remove('active'));
  document.querySelectorAll('.tab-bar button').forEach(e => e.classList.remove('active'));
  document.getElementById('tab-' + name).classList.add('active');
  event.target.classList.add('active');
  if (name === 'assets') loadAssets();
}

async function api(url, opts = {}) {
  const res = await fetch(url, { headers: {'Content-Type':'application/json'}, ...opts });
  return res.json();
}

function getProjectId() {
  return document.getElementById('project-id').value || 'project_default';
}

async function createProject() {
  const name = document.getElementById('project-name').value || '我的游戏';
  const desc = document.getElementById('project-desc').value || '';
  const data = await api(`${API}/projects`, {method:'POST', body:JSON.stringify({name, description:desc})});
  if (data.success) {
    document.getElementById('project-id').value = data.project.id;
    msg('项目已创建：' + data.project.id, 'success');
  } else {
    msg('失败：' + (data.error || JSON.stringify(data)), 'error');
  }
}

async function saveStyle() {
  const pid = getProjectId();
  const body = {
    art_style: document.getElementById('style-art').value,
    view_type: document.getElementById('style-view').value,
    color_palette: document.getElementById('style-palette').value,
    default_size: document.getElementById('style-size').value,
    prompt_rules: document.getElementById('style-prompt-rules').value,
    negative_prompt_rules: document.getElementById('style-neg-rules').value
  };
  const data = await api(`${API}/projects/${pid}/style`, {method:'POST', body:JSON.stringify(body)});
  if (data.success) {
    msg('画风配置已保存！', 'success');
  } else {
    msg('失败：' + (data.error || JSON.stringify(data)), 'error');
  }
}

async function generateAsset() {
  const pid = getProjectId();
  const btn = document.getElementById('btn-generate');
  const load = document.getElementById('gen-loading');
  btn.disabled = true;
  load.style.display = 'inline';

  const body = {
    project_id: pid,
    asset_type: document.getElementById('gen-type').value,
    description: document.getElementById('gen-desc').value,
    size: document.getElementById('gen-size').value,
    quantity: parseInt(document.getElementById('gen-quantity').value),
    extra_params: {
      direction: document.getElementById('gen-direction').value,
      background: document.getElementById('gen-bg').value,
      usage: document.getElementById('gen-usage').value
    }
  };

  try {
    const data = await api(`${API}/generations`, {method:'POST', body:JSON.stringify(body)});
    const r = document.getElementById('gen-result');

    if (data.success && data.task.status === 'succeeded') {
      r.innerHTML = `
        <div class="msg msg-success">素材生成成功！</div>
        <div style="text-align:center;margin-top:10px">
          <img src="${data.task.preview_url}" style="max-width:300px;max-height:300px;background:repeating-conic-gradient(#1a1a2e 0 25%,#222244 0 50%) 50%/16px 16px" onerror="this.style.display='none'">
          <div style="margin-top:8px">
            <a href="${data.task.download_url}" class="btn-primary btn-sm" style="text-decoration:none;display:inline-block">下载</a>
            <button class="btn-secondary btn-sm" onclick="switchTab('assets');loadAssets()">查看素材</button>
          </div>
        </div>`;
    } else {
      r.innerHTML = `<div class="msg msg-error">生成失败：${data.task?.error_message || data.error || '未知错误'}</div>`;
    }
  } catch(e) {
    document.getElementById('gen-result').innerHTML = `<div class="msg msg-error">错误：${e.message}</div>`;
  }

  btn.disabled = false;
  load.style.display = 'none';
}

async function loadAssets() {
  const pid = getProjectId();
  const container = document.getElementById('asset-list');
  try {
    const data = await api(`${API}/projects/${pid}/assets`);
    if (!data.success) {
      container.innerHTML = `<div class="msg msg-info">暂无素材，请先配置画风并生成。</div>`;
      return;
    }
    if (!data.assets || data.assets.length === 0) {
      container.innerHTML = `<div class="msg msg-info">还没有生成任何素材。</div>`;
      return;
    }
    container.innerHTML = data.assets.map(a => `
      <div class="result-item">
        <img src="${a.preview_url || ''}" onerror="this.src=''" alt="${a.name}">
        <div class="name">${a.name}</div>
        <div style="font-size:.7rem;color:#888">${a.asset_type} ${a.width}x${a.height}</div>
        <div class="actions">
          <a href="${a.download_url}" class="btn-primary btn-sm" style="text-decoration:none">下载</a>
        </div>
      </div>
    `).join('');
  } catch(e) {
    container.innerHTML = `<div class="msg msg-error">加载失败：${e.message}</div>`;
  }
}

loadAssets();
</script>
</body>
</html>"""


@app.get("/", response_class=HTMLResponse)
def index():
    return HTMLResponse(content=INDEX_HTML)
