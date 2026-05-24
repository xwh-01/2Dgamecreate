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
body{font-family:system-ui,-apple-system,sans-serif;background:#0d1117;color:#c9d1d9;min-height:100vh}
h1{text-align:center;padding:24px 20px 2px;color:#e94560;font-size:1.5rem;font-weight:700}
.subtitle{text-align:center;color:#8b949e;font-size:.75rem;margin-bottom:12px}
.user-guide{max-width:1200px;margin:0 auto 16px;padding:0 20px}
.guide-steps{display:flex;gap:6px;flex-wrap:wrap;background:#161b22;border:1px solid #21262d;border-radius:8px;padding:10px 16px}
.guide-step{display:flex;align-items:center;gap:4px;font-size:.7rem;color:#484f58;padding:4px 8px;border-radius:4px;white-space:nowrap}
.guide-step .gs-num{display:inline-flex;align-items:center;justify-content:center;width:18px;height:18px;border-radius:50%;background:#21262d;color:#8b949e;font-size:.65rem;font-weight:700;flex-shrink:0}
.guide-arrow{color:#30363d;font-size:.7rem}
.main-layout{max-width:1200px;margin:0 auto;padding:0 20px 40px;display:grid;grid-template-columns:260px 1fr 300px;gap:14px;align-items:start}
@media(max-width:900px){.main-layout{grid-template-columns:1fr}}
.panel{background:#161b22;border-radius:8px;border:1px solid #21262d;overflow:hidden}
.panel-header{font-size:.8rem;font-weight:700;color:#e94560;padding:10px 14px;border-bottom:1px solid #21262d;background:#0d1117}
.panel-body{padding:12px 14px}
.panel-body.compact{padding:8px 12px}
label{display:block;margin-bottom:2px;font-size:.68rem;color:#8b949e;font-weight:500}
.field-hint{font-size:.62rem;color:#484f58;margin-bottom:4px;line-height:1.3}
input,select,textarea{width:100%;padding:6px 10px;border-radius:5px;border:1px solid #30363d;background:#0d1117;color:#c9d1d9;font-size:.78rem;font-family:inherit;transition:border-color .15s}
input:focus,select:focus,textarea:focus{outline:none;border-color:#e94560}
textarea{resize:vertical;min-height:48px}
button{padding:7px 16px;border-radius:5px;border:none;cursor:pointer;font-size:.75rem;font-weight:600;transition:all .15s;font-family:inherit}
button:disabled{opacity:.4;cursor:not-allowed}
.btn-primary{background:#e94560;color:#fff}.btn-primary:hover:not(:disabled){background:#c73552}
.btn-secondary{background:#21262d;color:#c9d1d9;border:1px solid #30363d}.btn-secondary:hover:not(:disabled){background:#30363d}
.btn-success{background:#238636;color:#fff}.btn-success:hover:not(:disabled){background:#2ea043}
.btn-danger{background:#da3633;color:#fff}.btn-danger:hover:not(:disabled){background:#f85149}
.btn-outline{background:transparent;color:#8b949e;border:1px solid #30363d}.btn-outline:hover:not(:disabled){background:#21262d;color:#c9d1d9}
.btn-ghost{background:transparent;color:#58a6ff;border:none;padding:3px 6px;font-size:.65rem;cursor:pointer}.btn-ghost:hover{text-decoration:underline}
.btn-sm{padding:5px 10px;font-size:.7rem}
.btn-xs{padding:2px 7px;font-size:.65rem}
.msg{padding:8px 12px;border-radius:5px;margin-bottom:8px;font-size:.72rem;line-height:1.4;word-break:break-word}
.msg-success{background:#0d2818;border:1px solid #238636;color:#3fb950}
.msg-error{background:#2d1111;border:1px solid #da3633;color:#f85149}
.msg-info{background:#0d1b2d;border:1px solid #1f6feb;color:#58a6ff}
.msg-warning{background:#2d2300;border:1px solid #d29922;color:#d29922}
.progress-bar{margin:8px 0}
.progress-step{display:flex;align-items:center;gap:6px;padding:3px 0;font-size:.68rem;color:#484f58;border-left:2px solid #21262d;padding-left:8px;transition:all .3s}
.progress-step.active{color:#58a6ff;border-left-color:#58a6ff;font-weight:600}
.progress-step.done{color:#3fb950;border-left-color:#238636}
.progress-step .step-spinner{width:12px;height:12px;border:2px solid #58a6ff;border-top-color:transparent;border-radius:50%;animation:spin .6s linear infinite;flex-shrink:0}
@keyframes spin{to{transform:rotate(360deg)}}
.preview-img{max-width:100%;max-height:220px;object-fit:contain;background-image:repeating-conic-gradient(#0d1117 0 25%,#161b22 0 50%);background-size:16px 16px;border-radius:6px;border:1px solid #30363d}
.filter-bar{display:flex;gap:4px;align-items:center;flex-wrap:wrap;margin-bottom:8px}
.filter-types{display:flex;gap:2px;flex-wrap:wrap}
.filter-btn{padding:2px 8px;border-radius:10px;border:1px solid #30363d;background:transparent;color:#8b949e;font-size:.62rem;cursor:pointer;transition:all .15s}
.filter-btn:hover{color:#c9d1d9;border-color:#58a6ff}
.filter-btn.active{background:#1f6feb;color:#fff;border-color:#1f6feb}
.search-input{flex:1;min-width:100px;padding:4px 8px;font-size:.7rem}
.asset-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(130px,1fr));gap:8px}
.asset-card{background:#0d1117;border-radius:6px;overflow:hidden;border:1px solid #21262d;transition:border-color .15s}
.asset-card:hover{border-color:#58a6ff}
.asset-card-img{width:100%;aspect-ratio:1;display:flex;align-items:center;justify-content:center;background-image:repeating-conic-gradient(#0d1117 0 25%,#161b22 0 50%);background-size:10px 10px;padding:6px;cursor:pointer}
.asset-card-img img{max-width:100%;max-height:100%;object-fit:contain}
.asset-card-body{padding:6px 8px}
.asset-card-name{font-size:.65rem;font-weight:600;color:#c9d1d9;margin-bottom:2px;word-break:break-all;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.asset-card-type{font-size:.58rem;padding:1px 5px;border-radius:8px;background:#e94560;color:#fff;display:inline-block;margin-bottom:3px}
.asset-card-date{font-size:.58rem;color:#484f58;display:block;margin-bottom:4px}
.asset-card-actions{display:flex;gap:2px;flex-wrap:wrap}
.empty-state{text-align:center;padding:30px 16px;color:#484f58;font-size:.72rem}
.empty-state .empty-title{color:#8b949e;font-weight:600;margin-bottom:4px}
.btn-row{display:flex;gap:6px;margin-top:10px;flex-wrap:wrap}
.example-bar{display:flex;gap:4px;flex-wrap:wrap;margin-top:4px;margin-bottom:8px}
.example-btn{padding:2px 8px;font-size:.6rem;background:#0d1b2d;border:1px solid #1f6feb;color:#58a6ff;border-radius:10px;cursor:pointer;transition:all .15s}
.example-btn:hover{background:#1f6feb;color:#fff}
.inline-tag{display:inline-block;padding:1px 5px;border-radius:3px;font-size:.58rem;background:#21262d;color:#8b949e}
.stats-text{font-size:.65rem;color:#8b949e;margin-bottom:6px}
.stats-text strong{color:#c9d1d9}
.modal-overlay{display:none;position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,.85);z-index:999;justify-content:center;align-items:center}
.modal-overlay.active{display:flex}
.modal-content{max-width:90vw;max-height:90vh;position:relative}
.modal-content img{max-width:100%;max-height:85vh;object-fit:contain;background-image:repeating-conic-gradient(#0d1117 0 25%,#161b22 0 50%);background-size:16px 16px;border-radius:6px}
.modal-close{position:absolute;top:-30px;right:0;background:none;border:none;color:#8b949e;font-size:1.1rem;cursor:pointer}
.modal-close:hover{color:#c9d1d9}
.toast{position:fixed;bottom:20px;right:20px;padding:8px 16px;border-radius:6px;font-size:.72rem;z-index:1000;animation:toastIn .3s ease;color:#fff}
.toast-success{background:#238636}.toast-error{background:#da3633}
@keyframes toastIn{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:translateY(0)}}
.no-project-banner{padding:8px 12px;background:#2d2300;border:1px solid #d29922;border-radius:5px;color:#d29922;font-size:.7rem;margin-bottom:8px;text-align:center}
</style>
</head>
<body>
<h1>AI 2D Game Asset Generator</h1>
<div class="subtitle">2D 游戏素材智能生成工作台 - 为 Unity / Godot 开发者设计</div>

<div class="user-guide">
  <div class="guide-steps">
    <div class="guide-step"><span class="gs-num">1</span> 创建项目</div><span class="guide-arrow">&rarr;</span>
    <div class="guide-step"><span class="gs-num">2</span> 设置画风</div><span class="guide-arrow">&rarr;</span>
    <div class="guide-step"><span class="gs-num">3</span> 选择素材类型</div><span class="guide-arrow">&rarr;</span>
    <div class="guide-step"><span class="gs-num">4</span> 填写素材信息</div><span class="guide-arrow">&rarr;</span>
    <div class="guide-step"><span class="gs-num">5</span> 点击生成</div><span class="guide-arrow">&rarr;</span>
    <div class="guide-step"><span class="gs-num">6</span> 在素材库下载</div>
  </div>
</div>

<div class="main-layout">

  <!-- ===== LEFT: Project & Style ===== -->
  <div class="panel">
    <div class="panel-header">项目与画风</div>
    <div class="panel-body compact">
      <div id="no-project-warn" class="no-project-banner">请先创建项目或确认项目 ID</div>
      <label>项目名称</label>
      <input id="project-name" placeholder="地牢像素RPG" value="我的游戏" style="margin-bottom:6px">
      <label>项目 ID</label>
      <input id="project-id" value="project_default" readonly style="opacity:.5;font-size:.7rem;margin-bottom:6px">
      <label>项目描述</label>
      <input id="project-desc" placeholder="一款俯视角像素风地牢游戏" style="margin-bottom:8px">
      <button class="btn-primary btn-sm" style="width:100%" onclick="createProject()">创建 / 更新项目</button>
      <span style="display:block;font-size:.65rem;color:#484f58;margin-top:4px" id="project-status"></span>

      <hr style="border-color:#21262d;margin:12px 0 10px">

      <div style="display:grid;grid-template-columns:1fr 1fr;gap:6px">
        <div><label>画风</label><select id="style-art"><option value="pixel_art">像素风</option><option value="cartoon">卡通风</option><option value="hand_drawn">手绘风</option></select></div>
        <div><label>视角</label><select id="style-view"><option value="top_down">俯视</option><option value="side_view">侧视</option><option value="isometric">等角</option></select></div>
      </div>
      <label style="margin-top:6px">配色方案</label>
      <select id="style-palette"><option value="dark_dungeon">暗黑地牢</option><option value="bright_forest">明亮森林</option><option value="cyberpunk">赛博朋克</option><option value="custom">自定义</option></select>
      <label style="margin-top:4px">默认尺寸</label>
      <select id="style-size"><option value="32x32">32x32</option><option value="64x64" selected>64x64</option><option value="128x128">128x128</option></select>
      <label style="margin-top:4px">提示词规则</label>
      <textarea id="style-prompt-rules" rows="2" style="font-size:.7rem">centered sprite, clean silhouette</textarea>
      <label style="margin-top:4px">反向提示词</label>
      <textarea id="style-neg-rules" rows="2" style="font-size:.7rem">no text, no watermark, no background clutter</textarea>
      <button class="btn-primary btn-sm" style="width:100%;margin-top:8px" onclick="saveStyle()">保存画风配置</button>
      <span style="display:block;font-size:.65rem;color:#484f58;margin-top:4px" id="style-status"></span>
    </div>
  </div>

  <!-- ===== CENTER: Asset Library ===== -->
  <div class="panel">
    <div class="panel-header">素材库 <button class="btn-ghost" style="float:right" onclick="loadAssets()">刷新</button></div>
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

  <!-- ===== RIGHT: Generate Asset ===== -->
  <div class="panel" style="position:sticky;top:10px">
    <div class="panel-header">生成素材</div>
    <div class="panel-body compact">
      <label>素材类型</label>
      <div class="field-hint">选择你要生成的游戏素材类别</div>
      <select id="gen-type" onchange="onTypeChange()" style="margin-bottom:10px"><option value="character">角色 (Character)</option><option value="enemy">敌人 (Enemy)</option><option value="item">道具 (Item)</option><option value="tile">地图瓦片 (Tile)</option><option value="ui_icon">UI 图标 (UI Icon)</option><option value="effect">技能特效 (Effect)</option></select>
      <div id="gen-fields"></div>
      <div class="btn-row">
        <button class="btn-primary" id="btn-generate" onclick="generateAsset()" style="flex:1">生成素材</button>
        <button class="btn-secondary btn-sm" id="btn-regenerate" style="display:none" onclick="regenerateAsset()">重新生成</button>
      </div>
      <div class="field-hint" style="margin-top:6px">系统会根据素材类型自动补全游戏素材 Prompt</div>
      <div id="gen-progress"></div>
      <div id="gen-error"></div>
      <div id="gen-result"></div>
    </div>
  </div>

</div>

<div class="modal-overlay" id="preview-modal" onclick="closePreview()">
  <div class="modal-content" onclick="event.stopPropagation()">
    <button class="modal-close" onclick="closePreview()">&#10005;</button>
    <img id="preview-modal-img" src="" alt="">
  </div>
</div>

<script>
var API = '/api';
var lastGenParams = null;
var cachedAssets = [];
var currentFilter = 'all';
var progressTimer = null;
var progressStepIndex = 0;
var progressSteps = ['正在理解你的描述...','正在构造游戏素材 Prompt...','正在调用图片生成模型...','正在处理图片...','正在保存到素材库...'];

function msg(text, type) {
  var c = document.getElementById('msg-container');
  c.innerHTML = '<div class="msg msg-' + type + '">' + text + '</div>';
  if (c.innerHTML) setTimeout(function(){ c.innerHTML = ''; }, 6000);
}

function toast(text, type) {
  var t = document.getElementById('toast-el');
  if (!t) { t = document.createElement('div'); t.id = 'toast-el'; document.body.appendChild(t); }
  t.className = 'toast toast-' + (type || 'success');
  t.textContent = text;
  t.style.display = 'block';
  clearTimeout(t._timer);
  t._timer = setTimeout(function(){ t.style.display = 'none'; }, 2500);
}

function getProjectId() {
  return document.getElementById('project-id').value || 'project_default';
}

function isProjectReady() {
  var pid = getProjectId();
  return pid && pid !== 'project_default';
}

function updateNoProjectWarn() {
  var w = document.getElementById('no-project-warn');
  w.style.display = isProjectReady() ? 'none' : 'block';
}

async function api(url, opts) {
  var res = await fetch(url, Object.assign({ headers: {'Content-Type':'application/json'} }, opts || {}));
  if (!res.ok) throw new Error('HTTP ' + res.status + ': ' + res.statusText);
  return res.json();
}

function translateError(errMsg) {
  if (!errMsg) return '未知错误，请稍后重试';
  var msg = String(errMsg).toLowerCase();
  if (msg.indexOf('image provider is not configured') >= 0 || msg.indexOf('not configured') >= 0)
    return '图片生成服务还没有配置，请检查 IMAGE_API_KEY';
  if (msg.indexOf('tongyi wanxiang') >= 0 || (msg.indexOf('dashscope') >= 0 && msg.indexOf('error') >= 0))
    return '通义万象图片生成服务调用失败，请检查 API Key 是否正确';
  if (msg.indexOf('openai') >= 0 && (msg.indexOf('api') >= 0 || msg.indexOf('key') >= 0 || msg.indexOf('auth') >= 0))
    return 'OpenAI 服务认证失败，请检查 API Key 是否正确';
  if (msg.indexOf('image generation failed') >= 0 || msg.indexOf('generation failed') >= 0)
    return '图片生成服务调用失败，请稍后重试';
  if (msg.indexOf('task not found') >= 0) return '生成任务不存在';
  if (msg.indexOf('project not found') >= 0) return '项目不存在，请先创建项目';
  if (msg.indexOf('style profile') >= 0 || msg.indexOf('style_profile') >= 0)
    return '当前项目还没有配置画风，请先保存画风配置';
  if (msg.indexOf('network') >= 0 || msg.indexOf('fetch') >= 0 || msg.indexOf('timeout') >= 0 || msg.indexOf('connection') >= 0 || msg.indexOf('econnrefused') >= 0)
    return '请求失败，请检查后端服务是否运行';
  if (msg.indexOf('http') >= 0) return '服务器响应异常，请稍后重试';
  if (msg.indexOf('rate') >= 0 || msg.indexOf('quota') >= 0 || msg.indexOf('billing') >= 0)
    return 'API 额度不足或已达速率限制，请稍后重试';
  if (msg.indexOf('content') >= 0 || msg.indexOf('safety') >= 0 || msg.indexOf('policy') >= 0)
    return '内容被安全策略拦截，请修改描述后重试';
  if (msg.indexOf('unsupported') >= 0) return '不支持的图片生成服务商，请检查 IMAGE_PROVIDER 配置';
  return errMsg.length > 120 ? errMsg.substring(0, 120) + '...' : errMsg;
}

function getAssetTypeName(type) {
  var map = { character:'角色', enemy:'敌人', prop:'道具', tile:'瓦片', ui_icon:'UI图标', item:'物品', effect:'特效' };
  return map[type] || type;
}

function formatDate(isoStr) {
  if (!isoStr) return '';
  try {
    var d = new Date(isoStr);
    var p = function(n){ var s = String(n); return s.length < 2 ? '0' + s : s; };
    return d.getMonth()+1 + '/' + p(d.getDate()) + ' ' + p(d.getHours()) + ':' + p(d.getMinutes());
  } catch(e) { return isoStr; }
}

function escapeHtml(text) {
  if (!text) return '';
  return String(text).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;').replace(/'/g,'&#39;');
}

// ---- Project ----
async function createProject() {
  var name = document.getElementById('project-name').value || '我的游戏';
  var desc = document.getElementById('project-desc').value || '';
  var s = document.getElementById('project-status');
  s.textContent = '...';
  try {
    var data = await api(API + '/projects', {method:'POST', body:JSON.stringify({name:name, description:desc})});
    if (data.success) {
      document.getElementById('project-id').value = data.project.id;
      s.textContent = 'OK';
      s.style.color = '#3fb950';
      updateNoProjectWarn();
      msg('项目已创建', 'success');
    } else {
      s.textContent = 'fail';
      s.style.color = '#f85149';
    }
  } catch(e) {
    s.textContent = 'fail';
    s.style.color = '#f85149';
  }
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
  var s = document.getElementById('style-status');
  s.textContent = '...';
  try {
    var data = await api(API + '/projects/' + pid + '/style', {method:'POST', body:JSON.stringify(body)});
    if (data.success) {
      s.textContent = 'OK';
      s.style.color = '#3fb950';
      msg('画风配置已保存', 'success');
    } else {
      s.textContent = 'fail';
      s.style.color = '#f85149';
    }
  } catch(e) {
    s.textContent = 'fail';
    s.style.color = '#f85149';
  }
}

// ---- Example fill ----
var EXAMPLES = {
  character: [
    {label:'骑士战士', fill:{name:'Knight Warrior',view:'top_down',action:'idle',appearance:'wearing plate armor, iron helmet',weapon:'iron sword',size:'64x64'}},
    {label:'蓝袍法师', fill:{name:'Blue Mage',view:'front',action:'attack',appearance:'wearing blue robe, casting spell',weapon:'wooden staff',size:'64x64'}},
    {label:'精灵弓箭手', fill:{name:'Elf Archer',view:'side_view',action:'walk',appearance:'green cloak, holding bow',weapon:'bow and arrow',size:'128x128'}}
  ],
  enemy: [
    {label:'骷髅兵', fill:{name:'Skeleton Soldier',view:'top_down',action:'idle',appearance:'bone body, red glowing eyes',weapon:'bone sword',size:'64x64'}},
    {label:'史莱姆', fill:{name:'Green Slime',view:'front',action:'walk',appearance:'green translucent blob, two eyes',weapon:'',size:'64x64'}},
    {label:'暗黑法师', fill:{name:'Dark Mage',view:'front',action:'attack',appearance:'black hooded robe, purple energy',weapon:'dark staff',size:'128x128'}}
  ],
  item: [
    {label:'生命药水', fill:{name:'Health Potion',item_category:'potion',appearance:'red liquid in round glass bottle with cork',size:'64x64'}},
    {label:'金币', fill:{name:'Gold Coin',item_category:'coin',appearance:'golden coin with star emblem, shiny',size:'64x64'}},
    {label:'铁剑', fill:{name:'Iron Sword',item_category:'weapon',appearance:'silver blade with brown leather handle',size:'128x128'}}
  ],
  tile: [
    {label:'石砖地板', fill:{name:'Stone Floor',tile_type:'floor',material:'gray stone bricks with moss texture',seamless:'true',size:'32x32'}},
    {label:'草地', fill:{name:'Grass Ground',tile_type:'grass',material:'green grass with small flowers',seamless:'true',size:'32x32'}},
    {label:'岩浆', fill:{name:'Lava Surface',tile_type:'lava',material:'cracked dark rock with glowing orange lava',seamless:'true',size:'32x32'}}
  ],
  ui_icon: [
    {label:'红心图标', fill:{name:'Health Heart',icon_purpose:'health',shape:'circle',appearance:'red heart on white circular background',size:'64x64'}},
    {label:'金币图标', fill:{name:'Coin Icon',icon_purpose:'coin',shape:'no_frame',appearance:'golden coin icon, simple flat design',size:'64x64'}},
    {label:'齿轮设置', fill:{name:'Settings Gear',icon_purpose:'settings',shape:'circle',appearance:'silver gear icon on dark circle background',size:'64x64'}}
  ],
  effect: [
    {label:'火球爆炸', fill:{name:'Fireball Explosion',effect_type:'fire',motion_feeling:'burst',size:'64x64'}},
    {label:'冰霜光环', fill:{name:'Frost Aura',effect_type:'ice',motion_feeling:'aura',size:'64x64'}},
    {label:'雷电斩击', fill:{name:'Lightning Slash',effect_type:'lightning',motion_feeling:'slash',size:'128x128'}}
  ]
};

function fillExample(type, ex) {
  document.getElementById('gen-type').value = type;
  renderTypeFields(type);
  var f = ex.fill;
  var map = {name:'genf-name',view:'genf-view',action:'genf-action',appearance:'genf-appearance',weapon:'genf-weapon',item_category:'genf-item_category',tile_type:'genf-tile_type',material:'genf-material',seamless:'genf-seamless',icon_purpose:'genf-icon_purpose',shape:'genf-shape',effect_type:'genf-effect_type',motion_feeling:'genf-motion_feeling',size:'genf-size'};
  for (var k in f) {
    var el = document.getElementById(map[k]);
    if (el) el.value = f[k];
  }
}

// ---- FIELD_DEFS ----
var FIELD_DEFS = {
  character: [
    {id:'genf-name',label:'名称',hint:'角色叫什么？例如"骑士战士"',type:'text',placeholder:'骑士战士',value:'Knight Warrior'},
    {id:'genf-view',label:'视角',hint:'游戏中的观察角度',type:'select',opts:[{v:'top_down',t:'俯视'},{v:'side_view',t:'侧视'},{v:'front',t:'正面'}],value:'top_down'},
    {id:'genf-action',label:'动作',hint:'角色当前正在做什么',type:'select',opts:[{v:'idle',t:'待机'},{v:'walk',t:'行走'},{v:'attack',t:'攻击'},{v:'hurt',t:'受伤'},{v:'dead',t:'死亡'}],value:'idle'},
    {id:'genf-appearance',label:'外观',hint:'服装、体型、颜色等视觉特征',type:'textarea',placeholder:'穿着板甲，戴着铁盔',value:'wearing plate armor, iron helmet'},
    {id:'genf-weapon',label:'武器（可选）',hint:'留空则不生成武器',type:'text',placeholder:'铁剑',value:''},
    {id:'genf-size',label:'尺寸',hint:'生成的图片像素大小',type:'select',opts:[{v:'64x64',t:'64x64'},{v:'128x128',t:'128x128'}],value:'64x64'}
  ],
  enemy: [
    {id:'genf-name',label:'名称',hint:'敌人叫什么？例如"骷髅兵"',type:'text',placeholder:'骷髅兵',value:'Skeleton Soldier'},
    {id:'genf-view',label:'视角',hint:'游戏中的观察角度',type:'select',opts:[{v:'top_down',t:'俯视'},{v:'side_view',t:'侧视'},{v:'front',t:'正面'}],value:'top_down'},
    {id:'genf-action',label:'动作',hint:'敌人当前正在做什么',type:'select',opts:[{v:'idle',t:'待机'},{v:'walk',t:'行走'},{v:'attack',t:'攻击'},{v:'hurt',t:'受伤'},{v:'dead',t:'死亡'}],value:'idle'},
    {id:'genf-appearance',label:'外观',hint:'体型、颜色、特征等视觉描述',type:'textarea',placeholder:'白骨战士，手持骨盾',value:'skeleton with bone shield, red glowing eyes'},
    {id:'genf-weapon',label:'武器（可选）',hint:'留空则不生成武器',type:'text',placeholder:'骨刀',value:''},
    {id:'genf-size',label:'尺寸',hint:'生成的图片像素大小',type:'select',opts:[{v:'64x64',t:'64x64'},{v:'128x128',t:'128x128'}],value:'64x64'}
  ],
  item: [
    {id:'genf-name',label:'名称',hint:'道具叫什么？例如"生命药水"',type:'text',placeholder:'生命药水',value:'Health Potion'},
    {id:'genf-item_category',label:'道具类型',hint:'在游戏中的分类',type:'select',opts:[{v:'weapon',t:'武器'},{v:'potion',t:'药水'},{v:'coin',t:'钱币'},{v:'key',t:'钥匙'},{v:'food',t:'食物'}],value:'potion'},
    {id:'genf-appearance',label:'外观',hint:'形状、颜色、材质等',type:'textarea',placeholder:'红色液体装在圆形玻璃瓶中',value:'red liquid in a round glass bottle'},
    {id:'genf-size',label:'尺寸',hint:'生成的图片像素大小',type:'select',opts:[{v:'64x64',t:'64x64'},{v:'128x128',t:'128x128'}],value:'64x64'}
  ],
  tile: [
    {id:'genf-name',label:'名称',hint:'瓦片叫什么？例如"石砖地板"',type:'text',placeholder:'石砖地板',value:'Stone Floor'},
    {id:'genf-tile_type',label:'瓦片类型',hint:'在地图中的功能类型',type:'select',opts:[{v:'floor',t:'地板'},{v:'wall',t:'墙壁'},{v:'grass',t:'草地'},{v:'water',t:'水面'},{v:'lava',t:'岩浆'},{v:'road',t:'道路'}],value:'floor'},
    {id:'genf-material',label:'材质描述',hint:'视觉材质和纹理特征',type:'text',placeholder:'灰色石砖，有青苔纹理',value:'gray stone bricks with moss texture'},
    {id:'genf-seamless',label:'无缝平铺',hint:'是否可以无缝重复拼接',type:'select',opts:[{v:'true',t:'是 (Seamless)'},{v:'false',t:'否 (Single)'}],value:'true'},
    {id:'genf-size',label:'尺寸',hint:'生成的图片像素大小',type:'select',opts:[{v:'32x32',t:'32x32'},{v:'64x64',t:'64x64'}],value:'32x32'}
  ],
  ui_icon: [
    {id:'genf-name',label:'名称',hint:'图标叫什么？例如"生命值图标"',type:'text',placeholder:'生命值图标',value:'Health Icon'},
    {id:'genf-icon_purpose',label:'用途',hint:'这个图标在游戏中的功能',type:'select',opts:[{v:'health',t:'生命'},{v:'coin',t:'货币'},{v:'skill',t:'技能'},{v:'inventory',t:'背包'},{v:'settings',t:'设置'}],value:'health'},
    {id:'genf-shape',label:'形状',hint:'图标的外框形状',type:'select',opts:[{v:'circle',t:'圆形'},{v:'square',t:'方形'},{v:'no_frame',t:'无边框'}],value:'circle'},
    {id:'genf-appearance',label:'外观',hint:'颜色、图案等视觉描述',type:'textarea',placeholder:'红色十字，白色背景',value:'red cross on white background'},
    {id:'genf-size',label:'尺寸',hint:'生成的图片像素大小',type:'select',opts:[{v:'64x64',t:'64x64'},{v:'128x128',t:'128x128'}],value:'64x64'}
  ],
  effect: [
    {id:'genf-name',label:'名称',hint:'特效叫什么？例如"火球爆炸"',type:'text',placeholder:'火球爆炸',value:'Fireball Explosion'},
    {id:'genf-effect_type',label:'特效类型',hint:'特效的元素类型',type:'select',opts:[{v:'fire',t:'火焰'},{v:'ice',t:'冰霜'},{v:'lightning',t:'雷电'},{v:'healing',t:'治疗'},{v:'explosion',t:'爆炸'}],value:'fire'},
    {id:'genf-motion_feeling',label:'动势',hint:'特效的运动形态',type:'select',opts:[{v:'burst',t:'爆发'},{v:'spiral',t:'螺旋'},{v:'slash',t:'斩击'},{v:'aura',t:'光环'}],value:'burst'},
    {id:'genf-size',label:'尺寸',hint:'生成的图片像素大小',type:'select',opts:[{v:'64x64',t:'64x64'},{v:'128x128',t:'128x128'}],value:'64x64'}
  ]
};

function onTypeChange() {
  var type = document.getElementById('gen-type').value;
  renderTypeFields(type);
}

function renderTypeFields(type) {
  var container = document.getElementById('gen-fields');
  var fields = FIELD_DEFS[type] || FIELD_DEFS.character;
  var examples = EXAMPLES[type] || [];

  var html = '';
  if (examples.length > 0) {
    html += '<div class="example-bar">';
    html += '<span style="font-size:.62rem;color:#484f58;margin-right:2px">示例:</span>';
    for (var e = 0; e < examples.length; e++) {
      html += '<button class="example-btn" onclick="fillExample(\'' + type + '\',EXAMPLES[\'' + type + '\'][' + e + '])">' + examples[e].label + '</button>';
    }
    html += '</div>';
  }

  for (var i = 0; i < fields.length; i++) {
    var f = fields[i];
    html += '<div style="margin-bottom:8px">';
    html += '<label>' + f.label + '</label>';
    if (f.hint) html += '<div class="field-hint">' + f.hint + '</div>';
    if (f.type === 'select') {
      html += '<select id="' + f.id + '">';
      for (var j = 0; j < f.opts.length; j++) {
        var sel = f.opts[j].v === f.value ? ' selected' : '';
        html += '<option value="' + f.opts[j].v + '"' + sel + '>' + f.opts[j].t + '</option>';
      }
      html += '</select>';
    } else if (f.type === 'textarea') {
      html += '<textarea id="' + f.id + '" placeholder="' + (f.placeholder || '') + '" rows="2">' + (f.value || '') + '</textarea>';
    } else {
      html += '<input id="' + f.id + '" placeholder="' + (f.placeholder || '') + '" value="' + (f.value || '') + '">';
    }
    html += '</div>';
  }
  container.innerHTML = html;
}

function getFieldVal(id) {
  var el = document.getElementById(id);
  return el ? el.value : '';
}

function composeDescription(type) {
  var name = getFieldVal('genf-name');
  var appearance = getFieldVal('genf-appearance');
  if (type === 'character' || type === 'enemy') {
    var view = getFieldVal('genf-view');
    var action = getFieldVal('genf-action');
    var weapon = getFieldVal('genf-weapon');
    var parts = [name, '2D game sprite', view + ' view', action + ' pose'];
    if (appearance) parts.push(appearance);
    if (weapon) parts.push('holding ' + weapon);
    return parts.join(', ');
  }
  if (type === 'item') {
    var cat = getFieldVal('genf-item_category');
    return [cat, name, 'game item', appearance].filter(Boolean).join(', ');
  }
  if (type === 'tile') {
    var tileType = getFieldVal('genf-tile_type');
    var material = getFieldVal('genf-material');
    var seamless = getFieldVal('genf-seamless');
    var parts = [tileType, 'tile', material];
    if (seamless === 'true') parts.push('seamless repeatable');
    return parts.filter(Boolean).join(', ');
  }
  if (type === 'ui_icon') {
    var purpose = getFieldVal('genf-icon_purpose');
    var shape = getFieldVal('genf-shape');
    return [purpose, 'icon', name, shape + ' shape', appearance].filter(Boolean).join(', ');
  }
  if (type === 'effect') {
    var etype = getFieldVal('genf-effect_type');
    var motion = getFieldVal('genf-motion_feeling');
    return [etype, 'effect', name, motion, appearance].filter(Boolean).join(', ');
  }
  return appearance || name || '';
}

function getGenParams() {
  var pid = getProjectId();
  var type = document.getElementById('gen-type').value;
  var description = composeDescription(type);
  var size = getFieldVal('genf-size');
  return {
    project_id: pid,
    asset_type: type,
    description: description,
    size: size || '64x64',
    quantity: 1,
    extra_params: {
      direction: getFieldVal('genf-view') || '',
      background: 'transparent',
      usage: type === 'enemy' ? 'enemy_sprite' : (type === 'character' ? 'player_sprite' : ''),
      name: getFieldVal('genf-name'), view: getFieldVal('genf-view'),
      action: getFieldVal('genf-action'), appearance: getFieldVal('genf-appearance'),
      weapon: getFieldVal('genf-weapon'), item_category: getFieldVal('genf-item_category'),
      tile_type: getFieldVal('genf-tile_type'), material: getFieldVal('genf-material'),
      seamless: getFieldVal('genf-seamless'), icon_purpose: getFieldVal('genf-icon_purpose'),
      shape: getFieldVal('genf-shape'), effect_type: getFieldVal('genf-effect_type'),
      motion_feeling: getFieldVal('genf-motion_feeling')
    }
  };
}

function startProgressSteps() {
  progressStepIndex = 0;
  renderProgress();
  progressTimer = setInterval(function() {
    progressStepIndex++;
    if (progressStepIndex > progressSteps.length) progressStepIndex = progressSteps.length;
    renderProgress();
  }, 2000);
}

function stopProgressSteps() {
  if (progressTimer) { clearInterval(progressTimer); progressTimer = null; }
}

function renderProgress() {
  var p = document.getElementById('gen-progress');
  var html = '<div class="progress-bar">';
  for (var i = 0; i < progressSteps.length; i++) {
    var cls = 'pending';
    var icon = '<span style="width:12px;display:inline-block;text-align:center;font-size:.6rem;color:#484f58">' + (i+1) + '</span>';
    if (i < progressStepIndex) { cls = 'done'; icon = '<span style="color:#3fb950;font-weight:700">&#10003;</span>'; }
    else if (i === progressStepIndex) { cls = 'active'; icon = '<span class="step-spinner"></span>'; }
    html += '<div class="progress-step ' + cls + '">' + icon + progressSteps[i] + '</div>';
  }
  html += '</div>';
  p.innerHTML = html;
}

function markAllProgressDone() {
  progressStepIndex = progressSteps.length;
  renderProgress();
}

async function generateAsset() {
  var params = getGenParams();
  lastGenParams = params;

  var btn = document.getElementById('btn-generate');
  var regenBtn = document.getElementById('btn-regenerate');
  var progress = document.getElementById('gen-progress');
  var result = document.getElementById('gen-result');
  var errArea = document.getElementById('gen-error');

  result.style.display = 'none'; result.innerHTML = '';
  errArea.style.display = 'none'; errArea.innerHTML = '';
  regenBtn.style.display = 'none'; progress.innerHTML = '';

  btn.textContent = '生成中...'; btn.disabled = true;
  startProgressSteps();

  try {
    var data = await api(API + '/generations', {method:'POST', body:JSON.stringify(params)});
    markAllProgressDone();

    if (data.success && data.task && data.task.status === 'succeeded') {
      var previewUrl = data.task.preview_url || '';
      var downloadUrl = data.task.download_url || '';
      result.style.display = 'block';
      result.innerHTML =
        '<div class="msg msg-success">生成成功！</div>' +
        '<div style="text-align:center"><img class="preview-img" src="' + previewUrl + '" onerror="this.style.display=\'none\'"></div>' +
        '<div class="btn-row" style="justify-content:center">' +
          '<a href="' + downloadUrl + '" class="btn-success btn-xs" style="text-decoration:none">下载</a>' +
          '<button class="btn-outline btn-xs" onclick="copyText(' + JSON.stringify(params.description) + ')">复制 Prompt</button>' +
        '</div>';
      regenBtn.style.display = 'inline-block';
      msg('素材生成成功', 'success');
      loadAssets();
    } else {
      var errMsg = (data.task && data.task.error_message) ? data.task.error_message : (data.error || '未知错误');
      showGenError(errMsg);
    }
  } catch(e) {
    stopProgressSteps();
    showGenError(e.message);
  }
  btn.textContent = '生成素材'; btn.disabled = false;
}

function showGenError(errMsg) {
  var errArea = document.getElementById('gen-error');
  var result = document.getElementById('gen-result');
  var regenBtn = document.getElementById('btn-regenerate');
  result.style.display = 'none';
  errArea.style.display = 'block';
  var friendly = translateError(errMsg);
  errArea.innerHTML = '<div class="msg msg-error" style="margin-top:8px"><strong>生成失败</strong><br>' + friendly + '</div>';
  regenBtn.style.display = 'inline-block';
}

function restoreFieldsFromParams(params) {
  if (!params) return;
  var type = params.asset_type || 'character';
  document.getElementById('gen-type').value = type;
  renderTypeFields(type);
  var p = params.extra_params || {};
  var fieldMap = {
    name:'genf-name', view:'genf-view', action:'genf-action',
    appearance:'genf-appearance', weapon:'genf-weapon',
    item_category:'genf-item_category', tile_type:'genf-tile_type',
    material:'genf-material', seamless:'genf-seamless',
    icon_purpose:'genf-icon_purpose', shape:'genf-shape',
    effect_type:'genf-effect_type', motion_feeling:'genf-motion_feeling'
  };
  for (var key in fieldMap) {
    if (p[key] !== undefined && p[key] !== null) {
      var el = document.getElementById(fieldMap[key]);
      if (el) el.value = p[key];
    }
  }
}

async function regenerateAsset() {
  if (!lastGenParams) { msg('请先生成一次素材', 'info'); return; }
  restoreFieldsFromParams(lastGenParams);
  await generateAsset();
}

// ---- Image preview ----
function openPreview(url) {
  document.getElementById('preview-modal-img').src = url;
  document.getElementById('preview-modal').classList.add('active');
}
function closePreview() {
  document.getElementById('preview-modal').classList.remove('active');
}

// ---- Copy ----
function copyText(text) {
  if (navigator.clipboard && navigator.clipboard.writeText) {
    navigator.clipboard.writeText(text).then(function(){ toast('已复制', 'success'); }).catch(function(){ fallbackCopy(text); });
  } else { fallbackCopy(text); }
}
function fallbackCopy(text) {
  var ta = document.createElement('textarea'); ta.value = text;
  ta.style.position = 'fixed'; ta.style.left = '-9999px';
  document.body.appendChild(ta); ta.select();
  try { document.execCommand('copy'); toast('已复制', 'success'); } catch(e) { toast('复制失败', 'error'); }
  document.body.removeChild(ta);
}

// ---- Asset Library ----
function setFilter(type, btn) {
  currentFilter = type;
  document.querySelectorAll('#filter-types .filter-btn').forEach(function(b){ b.classList.remove('active'); });
  if (btn) btn.classList.add('active');
  renderAssets();
}

async function loadAssets() {
  var pid = getProjectId();
  var container = document.getElementById('asset-list');
  container.innerHTML = '<div style="text-align:center;padding:20px;color:#484f58;font-size:.7rem">加载中...</div>';
  try {
    var data = await api(API + '/projects/' + pid + '/assets');
    if (!data.success || !data.assets || data.assets.length === 0) {
      cachedAssets = [];
      container.innerHTML = '<div class="empty-state"><div class="empty-title">暂无素材</div><div class="empty-hint">请先在右侧面板生成素材</div></div>';
      document.getElementById('stats-bar').innerHTML = '';
      return;
    }
    cachedAssets = data.assets;
    renderAssets();
  } catch(e) {
    container.innerHTML = '<div class="msg msg-error">加载失败：' + translateError(e.message) + '</div>';
  }
}

function renderAssets() {
  var container = document.getElementById('asset-list');
  var searchText = (document.getElementById('search-input').value || '').toLowerCase();
  var filtered = cachedAssets.filter(function(a) {
    if (currentFilter !== 'all' && a.asset_type !== currentFilter) return false;
    if (searchText) {
      var name = (a.name || '').toLowerCase();
      var desc = (a.metadata && a.metadata.description || '').toLowerCase();
      var prompt = (a.metadata && a.metadata.final_prompt || '').toLowerCase();
      if (name.indexOf(searchText) < 0 && desc.indexOf(searchText) < 0 && prompt.indexOf(searchText) < 0) return false;
    }
    return true;
  });
  document.getElementById('stats-bar').innerHTML = '共 <strong>' + cachedAssets.length + '</strong> 个' + (filtered.length !== cachedAssets.length ? '，显示 <strong>' + filtered.length + '</strong> 个' : '');
  if (filtered.length === 0) {
    container.innerHTML = '<div class="empty-state"><div class="empty-title">' + (cachedAssets.length === 0 ? '暂无素材' : '无匹配') + '</div><div class="empty-hint">' + (cachedAssets.length === 0 ? '请在右侧面板生成素材' : '试试调整筛选条件') + '</div></div>';
    return;
  }
  container.innerHTML = '<div class="asset-grid">' + filtered.map(function(a) {
    var meta = a.metadata || {};
    var desc = meta.description || '';
    var prompt = meta.final_prompt || '';
    var pd = prompt.length > 80 ? prompt.substring(0, 80) + '...' : prompt;
    var h = '<div class="asset-card">';
    h += '<div class="asset-card-img" onclick="openPreview(\'' + escapeHtml(a.preview_url || '') + '\')"><img src="' + escapeHtml(a.preview_url || '') + '" loading="lazy" onerror="this.parentElement.innerHTML=\'<span style=font-size:.6rem;color:#484f58>加载失败</span>\'"></div>';
    h += '<div class="asset-card-body">';
    h += '<div class="asset-card-name" title="' + escapeHtml(a.name) + '">' + escapeHtml(a.name) + '</div>';
    h += '<span class="asset-card-type">' + getAssetTypeName(a.asset_type) + '</span>';
    h += '<span class="asset-card-date">' + formatDate(a.created_at) + '</span>';
    h += '<div class="asset-card-actions">';
    h += '<a href="' + escapeHtml(a.download_url || '') + '" class="btn-success btn-xs" style="text-decoration:none">下载</a>';
    h += '<button class="btn-outline btn-xs" onclick="copyText(' + JSON.stringify(prompt || desc) + ')">复制</button>';
    h += '<button class="btn-secondary btn-xs" onclick="regenerateFromAsset(' + JSON.stringify(a.asset_type) + ',' + JSON.stringify(desc) + ',' + JSON.stringify(meta.size || '') + ')">重生成</button>';
    h += '<button class="btn-danger btn-xs" onclick="deleteAsset(' + JSON.stringify(a.id) + ')">删</button>';
    h += '</div></div></div>';
    return h;
  }).join('') + '</div>';
}

function regenerateFromAsset(assetType, desc, size) {
  document.getElementById('gen-type').value = assetType || 'character';
  renderTypeFields(assetType || 'character');
  var szEl = document.getElementById('genf-size');
  if (szEl && size) szEl.value = size;
  var appEl = document.getElementById('genf-appearance');
  if (appEl && desc) appEl.value = desc;
  var nameEl = document.getElementById('genf-name');
  if (nameEl && desc) nameEl.value = desc.split(',')[0] || desc;
  generateAsset();
}

async function deleteAsset(assetId) {
  if (!confirm('确定删除该素材吗？此操作不可撤销。')) return;
  try {
    var data = await api(API + '/assets/' + assetId, {method:'DELETE'});
    if (data.success) { msg('已删除', 'success'); loadAssets(); }
    else { msg('删除失败', 'error'); }
  } catch(e) { msg('删除失败：' + translateError(e.message), 'error'); }
}

document.addEventListener('keydown', function(e) { if (e.key === 'Escape') closePreview(); });
updateNoProjectWarn();
onTypeChange();
loadAssets();
</script>
</body>
</html>"""


@app.get("/", response_class=HTMLResponse)
def index():
    return HTMLResponse(content=INDEX_HTML)
