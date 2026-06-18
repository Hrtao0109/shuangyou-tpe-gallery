#!/usr/bin/env python3
"""
车型图库 HTML 生成器
读取 车型图库数据.csv + 带标注/ 图片，生成 self-contained index.html
"""
import csv
import os
import json

BASE = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE, "车型图库数据.csv")
IMG_DIR = os.path.join(BASE, "带标注")
OUT_HTML = os.path.join(BASE, "index.html")

def parse_csv():
    items = []
    with open(CSV_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            brand = row["品牌"].strip()
            model = row["车型"].strip()
            year = row["年份款"].strip()
            desc = row["描述"].strip()
            fname = row["文件名"].strip()
            if not brand or not fname:
                continue
            # Check file exists
            fpath = os.path.join(IMG_DIR, fname)
            if not os.path.exists(fpath):
                print(f"⚠ 图片不存在: {fname}")
            items.append({
                "brand": brand,
                "model": model,
                "year": year,
                "desc": desc,
                "file": fname,
            })
    return items

def generate_html(items):
    data_json = json.dumps(items, ensure_ascii=False, indent=2)

    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>双优TPE脚垫 · 车型图库</title>
<style>
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ font-family: -apple-system,BlinkMacSystemFont,"PingFang SC","Microsoft YaHei",sans-serif; background:#f2f3f5; color:#222; }}

/* ── Header ── */
.header {{ background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); color:#fff; padding:20px 16px 14px; position:sticky; top:0; z-index:100; }}
.header-top {{ display:flex; align-items:center; gap:10px; margin-bottom:10px; }}
.logo {{ font-size:22px; font-weight:800; letter-spacing:1px; }}
.logo span {{ color:#07c160; }}
.subtitle {{ font-size:12px; color:rgba(255,255,255,.55); }}

.search-wrap {{ display:flex; gap:8px; }}
.search-input {{ flex:1; height:42px; border:none; border-radius:10px; padding:0 14px; font-size:15px; background:rgba(255,255,255,.12); color:#fff; outline:none; transition:background .2s; }}
.search-input::placeholder {{ color:rgba(255,255,255,.4); }}
.search-input:focus {{ background:rgba(255,255,255,.2); }}

.brand-chips {{ display:flex; flex-wrap:wrap; gap:6px; margin-top:10px; }}
.chip {{ padding:5px 14px; border-radius:16px; font-size:13px; background:rgba(255,255,255,.1); color:rgba(255,255,255,.7); cursor:pointer; user-select:none; transition:all .2s; border:none; white-space:nowrap; }}
.chip.active {{ background:#07c160; color:#fff; font-weight:600; }}

/* ── Stats ── */
.stats {{ padding:12px 16px 4px; font-size:13px; color:#999; display:flex; justify-content:space-between; }}

/* ── Brand Sections ── */
.brand-section {{ margin:0 12px 20px; }}
.brand-header {{ display:flex; align-items:center; gap:8px; padding:8px 0 6px; }}
.brand-header .brand-name {{ font-size:17px; font-weight:700; color:#1a1a2e; }}
.brand-header .brand-count {{ font-size:12px; color:#999; }}

/* ── Grid ── */
.gallery {{ display:grid; grid-template-columns:repeat(2,1fr); gap:8px; }}
@media (min-width:640px) {{ .gallery {{ grid-template-columns:repeat(3,1fr); }} }}
@media (min-width:900px) {{ .gallery {{ grid-template-columns:repeat(4,1fr); }} }}
@media (min-width:1200px) {{ .gallery {{ grid-template-columns:repeat(5,1fr); }} }}

.card {{ background:#fff; border-radius:10px; overflow:hidden; box-shadow:0 1px 3px rgba(0,0,0,.06); cursor:pointer; transition:transform .15s,box-shadow .15s; }}
.card:hover {{ transform:translateY(-2px); box-shadow:0 4px 12px rgba(0,0,0,.1); }}
.card:active {{ transform:scale(.97); }}

.card-img-wrap {{ width:100%; aspect-ratio:1; background:#fafafa; display:flex; align-items:center; justify-content:center; overflow:hidden; }}
.card-img {{ width:100%; height:100%; object-fit:contain; }}
.card-body {{ padding:8px 10px 10px; }}
.card-model {{ font-size:13px; font-weight:600; color:#1a1a2e; line-height:1.3; }}
.card-year {{ font-size:11px; color:#999; margin-top:2px; }}
.card-tag {{ display:inline-block; font-size:10px; background:#e8f4fd; color:#3a8fd4; padding:1px 6px; border-radius:3px; margin-top:4px; }}

/* ── Empty ── */
.empty {{ text-align:center; padding:60px 20px; color:#bbb; display:none; }}
.empty.show {{ display:block; }}
.empty .icon {{ font-size:48px; margin-bottom:10px; }}

/* ── Lightbox ── */
.lightbox {{ display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,.94); z-index:999; flex-direction:column; }}
.lightbox.show {{ display:flex; }}
.lb-top {{ display:flex; justify-content:space-between; align-items:center; padding:12px 16px; }}
.lb-counter {{ font-size:14px; color:rgba(255,255,255,.6); }}
.lb-actions {{ display:flex; gap:8px; }}
.lb-btn {{ width:36px; height:36px; border-radius:50%; border:none; background:rgba(255,255,255,.15); color:#fff; font-size:16px; cursor:pointer; display:flex; align-items:center; justify-content:center; transition:background .2s; }}
.lb-btn:hover {{ background:rgba(255,255,255,.25); }}
.lb-btn svg {{ width:18px; height:18px; fill:#fff; }}
.lb-img-wrap {{ flex:1; display:flex; align-items:center; justify-content:center; padding:16px; overflow:auto; }}
.lb-img {{ max-width:100%; max-height:65vh; object-fit:contain; border-radius:4px; }}
.lb-caption {{ padding:10px 16px 6px; text-align:center; color:#fff; }}
.lb-name {{ font-size:17px; font-weight:600; }}
.lb-detail {{ font-size:13px; color:rgba(255,255,255,.5); margin-top:3px; }}
.lb-nav {{ display:flex; justify-content:space-between; padding:10px 16px 20px; gap:10px; }}
.lb-nav button {{ flex:1; height:40px; border:1px solid rgba(255,255,255,.25); border-radius:10px; background:transparent; color:#fff; font-size:15px; cursor:pointer; transition:background .2s; }}
.lb-nav button:hover {{ background:rgba(255,255,255,.08); }}

/* ── Footer ── */
.footer {{ text-align:center; padding:24px 16px 40px; color:#bbb; font-size:12px; }}

/* ── Back to top ── */
.back-top {{ position:fixed; bottom:24px; right:20px; width:44px; height:44px; border-radius:50%; background:#07c160; color:#fff; border:none; font-size:20px; cursor:pointer; box-shadow:0 2px 10px rgba(7,193,96,.3); display:none; z-index:50; transition:transform .2s; }}
.back-top.show {{ display:flex; align-items:center; justify-content:center; }}
.back-top:active {{ transform:scale(.9); }}
</style>
</head>
<body>

<div class="header">
  <div class="header-top">
    <div class="logo">双优<span>TPE</span>脚垫</div>
    <div class="subtitle">车型图库 · 白底已标注</div>
  </div>
  <div class="search-wrap">
    <input class="search-input" id="search" type="text" placeholder="搜索车型… 如 Model Y、理想 L7" oninput="filter()">
  </div>
  <div class="brand-chips" id="chips"></div>
</div>

<div class="stats" id="stats"></div>
<div id="content"></div>
<div class="empty" id="empty"><div class="icon">📭</div><p>没有匹配的车型</p></div>

<div class="lightbox" id="lightbox">
  <div class="lb-top">
    <span class="lb-counter" id="lbCounter"></span>
    <div class="lb-actions">
      <button class="lb-btn" id="lbDownload" title="下载原图">
        <svg viewBox="0 0 24 24"><path d="M19 9h-4V3H9v6H5l7 7 7-7zM5 18v2h14v-2H5z"/></svg>
      </button>
      <button class="lb-btn" onclick="closeLB()" title="关闭">✕</button>
    </div>
  </div>
  <div class="lb-img-wrap">
    <img class="lb-img" id="lbImg" src="" alt="">
  </div>
  <div class="lb-caption">
    <div class="lb-name" id="lbName"></div>
    <div class="lb-detail" id="lbDetail"></div>
  </div>
  <div class="lb-nav">
    <button onclick="prevImg()">◀ 上一张</button>
    <button onclick="nextImg()">下一张 ▶</button>
  </div>
</div>

<button class="back-top" id="backTop" onclick="window.scrollTo({{top:0,behavior:'smooth'}})">↑</button>

<div class="footer">双优 TPE 汽车脚垫 · 广东揭阳 · 车型图库持续更新中</div>

<script>
const DATA = {data_json};

// ── State ──
let activeBrand = '';
let searchTerm = '';
let lbIdx = -1;
let filteredIds = [];

// ── Init ──
const brands = [...new Set(DATA.map(i => i.brand))];
renderChips();
filter();

// ── Render brand chips ──
function renderChips() {{
  document.getElementById('chips').innerHTML =
    '<button class="chip' + (!activeBrand?' active':'') + '" onclick="setBrand(\\'\\')">全部</button>' +
    brands.map(b => '<button class="chip' + (activeBrand===b?' active':'') + '" onclick="setBrand(\\'' + b + '\\')">' + b + '</button>').join('');
}}

function setBrand(b) {{
  activeBrand = activeBrand === b ? '' : b;
  renderChips();
  filter();
}}

// ── Filter ──
function filter() {{
  searchTerm = document.getElementById('search').value.trim().toLowerCase();
  let list = DATA;
  if (activeBrand) list = list.filter(i => i.brand === activeBrand);
  if (searchTerm) {{
    list = list.filter(i =>
      (i.brand + i.model + i.year + i.desc).toLowerCase().includes(searchTerm)
    );
  }}
  filteredIds = list.map(i => DATA.indexOf(i));

  const total = filteredIds.length;
  document.getElementById('stats').innerHTML =
    '<span>共 ' + total + ' 张图片</span>' +
    (!activeBrand && !searchTerm ? '<span>' + brands.length + ' 个品牌</span>' : '');

  if (total === 0) {{
    document.getElementById('content').innerHTML = '';
    document.getElementById('empty').classList.add('show');
    return;
  }}
  document.getElementById('empty').classList.remove('show');

  // Group by brand
  const groups = {{}};
  list.forEach((item, idx) => {{
    if (!groups[item.brand]) groups[item.brand] = [];
    groups[item.brand].push({{...item, _globalIdx: DATA.indexOf(item)}});
  }});

  let html = '';
  for (const [brand, items] of Object.entries(groups)) {{
    html += '<div class="brand-section">';
    html += '<div class="brand-header"><span class="brand-name">' + brand + '</span><span class="brand-count">' + items.length + '款</span></div>';
    html += '<div class="gallery">';
    items.forEach(item => {{
      const label = item.desc ? (item.brand + ' ' + item.model + ' · ' + item.desc) : (item.brand + ' ' + item.model);
      const tagHtml = item.desc ? '<span class="card-tag">' + item.desc + '</span>' : '';
      html += '<div class="card" onclick="openLB(' + item._globalIdx + ')">';
      html += '<div class="card-img-wrap"><img class="card-img" src="带标注/' + item.file + '" alt="' + label + '" loading="lazy"></div>';
      html += '<div class="card-body">';
      html += '<div class="card-model">' + label + '</div>';
      html += '<div class="card-year">' + item.year + '</div>';
      html += tagHtml;
      html += '</div></div>';
    }});
    html += '</div></div>';
  }}
  document.getElementById('content').innerHTML = html;
}}

// ── Lightbox ──
function openLB(idx) {{
  lbIdx = idx;
  const item = DATA[idx];
  document.getElementById('lbImg').src = '带标注/' + item.file;
  document.getElementById('lbName').textContent = (item.desc ? (item.brand + ' ' + item.model + ' · ' + item.desc) : (item.brand + ' ' + item.model));
  document.getElementById('lbDetail').textContent = item.year;
  document.getElementById('lbCounter').textContent = (idx+1) + ' / ' + DATA.length;
  document.getElementById('lbDownload').onclick = () => downloadImg(item);
  document.getElementById('lightbox').classList.add('show');
  document.body.style.overflow = 'hidden';
}}

function closeLB() {{
  document.getElementById('lightbox').classList.remove('show');
  document.body.style.overflow = '';
}}

function prevImg() {{ if (lbIdx > 0) openLB(lbIdx - 1); }}
function nextImg() {{ if (lbIdx < DATA.length - 1) openLB(lbIdx + 1); }}

function downloadImg(item) {{
  const a = document.createElement('a');
  a.href = '带标注/' + item.file;
  a.download = item.file;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
}}

// ── Keyboard ──
document.addEventListener('keydown', e => {{
  if (document.getElementById('lightbox').classList.contains('show')) {{
    if (e.key === 'Escape') closeLB();
    if (e.key === 'ArrowLeft') prevImg();
    if (e.key === 'ArrowRight') nextImg();
  }}
}});

// ── Back to top ──
window.addEventListener('scroll', () => {{
  document.getElementById('backTop').classList.toggle('show', window.scrollY > 400);
}});
</script>
</body>
</html>'''
    return html


def main():
    items = parse_csv()
    print(f"✓ 读取 {len(items)} 条车型数据")

    html = generate_html(items)
    with open(OUT_HTML, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"✓ 生成 {OUT_HTML}")
    print(f"✓ 可直接用浏览器打开，或部署到 GitHub Pages")


if __name__ == "__main__":
    main()
