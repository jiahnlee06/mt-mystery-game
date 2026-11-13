import os
import json
import csv
import io
import sqlite3
import urllib.request
import urllib.error
from pathlib import Path

import streamlit as st
from PIL import Image, ImageDraw
from streamlit_image_coordinates import streamlit_image_coordinates


# ─────────────────────────────────────
# 기본 설정
# ─────────────────────────────────────
st.set_page_config(
    page_title="학생회장 살인사건",
    layout="wide",
)


# ── 몰입형 사건 조사 게임 UI ──
st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700;900&family=Black+Han+Sans&display=swap');
:root{--blood:#b52b32;--ink:#08090d;--line:#493037;--paper:#e7ded7}
.stApp{background:linear-gradient(115deg,rgba(7,8,11,.96),rgba(15,14,18,.92)),repeating-linear-gradient(0deg,#121014 0px,#121014 3px,#08090c 4px);color:#ddd2ce;font-family:'Noto Sans KR',sans-serif}
[data-testid="stHeader"]{background:transparent}
[data-testid="stSidebar"]{background:#0b0c10;border-right:1px solid #4a252b}
[data-testid="stSidebar"] h2,[data-testid="stSidebar"] h3{color:#d3b7b4!important}
.block-container{max-width:1160px;padding-top:2.2rem;padding-bottom:4rem}
h1,h2,h3{font-family:'Noto Sans KR',sans-serif!important;font-weight:900!important;letter-spacing:-.04em;color:#e9ddda!important}
h1{border-left:4px solid #a22d34;padding-left:16px;text-shadow:0 0 20px #5c131b66}
.stButton>button{background:linear-gradient(145deg,#211a1e,#111216)!important;border:1px solid #654148!important;color:#f1e3df!important;border-radius:3px!important;min-height:54px;font-weight:700!important;letter-spacing:.02em;box-shadow:inset 0 1px 0 #ffffff10,0 6px 15px #0006;transition:transform .15s,border-color .15s,box-shadow .15s}
.stButton>button:hover{transform:translateY(-2px);border-color:#d2474f!important;box-shadow:0 0 22px #b32a3744!important}
.stButton>button:disabled{opacity:.36;filter:grayscale(1)}
.stButton>button[kind="primary"]{background:linear-gradient(110deg,#741b27,#3b141b)!important;border-color:#bb5056!important}
[data-testid="stMetric"]{background:linear-gradient(145deg,#20171c,#101115);border:1px solid #51343b;border-radius:2px;padding:15px 20px}
[data-testid="stMetricLabel"]{color:#b7a3a4!important}
[data-testid="stMetricValue"]{color:#e9d8d4!important}
[data-testid="stAlert"]{background:#1b171c;border:1px solid #49343a;border-radius:3px}
[data-testid="stExpander"]{background:#151317;border:1px solid #4d333a;border-radius:2px}
[data-testid="stTabs"] button{color:#c8b8b5}
hr{border-color:#503038!important}
.game-hero{position:relative;overflow:hidden;min-height:300px;padding:45px 50px;background:radial-gradient(ellipse at 75% 50%,#6d1d2860,transparent 44%),linear-gradient(115deg,#151318,#08090c);border:1px solid #6a353e;box-shadow:0 18px 55px #0009,inset 0 0 80px #0009;margin-bottom:24px}
.game-hero:after{content:'CASE 001';position:absolute;right:-20px;bottom:-44px;font-weight:900;font-size:145px;letter-spacing:-10px;color:#ffffff06;pointer-events:none}
.game-eyebrow{color:#e05d66;font-size:12px;font-weight:900;letter-spacing:.28em;margin-bottom:18px}
.game-title{font-family:'Black Han Sans','Noto Sans KR',sans-serif;font-size:clamp(37px,6vw,69px);color:#f1e7e1;line-height:1.2;text-shadow:0 4px 25px #000;letter-spacing:-.06em}
.game-sub{font-size:15px;color:#b7a6a5;letter-spacing:.15em;margin-top:17px}
.game-status{display:inline-block;border:1px solid #9b333b;background:#4b1a2359;color:#f2a2a7;font-size:11px;font-weight:900;letter-spacing:.18em;padding:7px 13px;margin-top:26px}
.game-section{color:#f0ded8;font-weight:900;letter-spacing:.16em;font-size:15px;border-bottom:1px solid #60353d;padding:12px 0;margin:14px 0 18px}
.game-caption{font-size:12px;letter-spacing:.15em;color:#aa8d90;margin:4px 0 18px}
@media(max-width:650px){.game-hero{padding:30px 22px;min-height:250px}.game-hero:after{font-size:75px;bottom:-20px}.block-container{padding-top:1rem}}

/* Cinematic game HUD / minimize dashboard appearance */
#MainMenu,footer,[data-testid="stDecoration"],[data-testid="stStatusWidget"]{visibility:hidden!important}
[data-testid="stHeader"]{height:1.5rem!important}
.stApp{background:radial-gradient(ellipse at 50% -15%,#3b1720 0%,transparent 46%),radial-gradient(ellipse at 110% 80%,#28171b 0%,transparent 48%),#08090b!important}
.stApp:before{content:"";position:fixed;inset:0;pointer-events:none;z-index:0;background:repeating-linear-gradient(0deg,transparent 0px,transparent 3px,#00000010 4px);opacity:.65}
.block-container{max-width:1220px!important;padding-top:1.2rem!important}
.game-hero{min-height:375px!important;display:flex;flex-direction:column;justify-content:center;background:linear-gradient(90deg,#08090cdd 0%,#101014c4 55%,#210b16b5 100%),radial-gradient(circle at 85% 50%,#9b243d 0%,#160d13 42%,#08090c 82%)!important;border:1px solid #7c3543!important;box-shadow:0 30px 85px #000c,inset 0 0 100px #000b!important}
.game-hero:before{content:"◉  CLASSIFIED  /  CASE 001";position:absolute;top:16px;right:20px;font:700 11px monospace;letter-spacing:.2em;color:#d37983;opacity:.75}
.game-title{font-size:clamp(46px,7vw,86px)!important;text-shadow:0 3px 2px #000,0 0 40px #991d314d!important}
.game-section{background:linear-gradient(90deg,#321a22b0,transparent 85%);border-left:3px solid #bd4250!important;padding:15px 20px!important;text-transform:uppercase;letter-spacing:.14em!important}
.stButton>button{border-radius:0!important;min-height:62px!important;clip-path:polygon(0 0,calc(100% - 10px) 0,100% 10px,100% 100%,10px 100%,0 calc(100% - 10px));background:linear-gradient(120deg,#261c23,#100f14)!important;border:1px solid #78404a!important;text-transform:none;letter-spacing:.08em!important;box-shadow:inset 3px 0 #a73e4a,0 12px 24px #0007!important}
.stButton>button:hover{background:linear-gradient(120deg,#56242e,#1a1118)!important;box-shadow:inset 4px 0 #e65b69,0 0 25px #b52b324d!important}
[data-testid="stImage"] img{border:1px solid #65414b;box-shadow:0 18px 65px #000a,0 0 35px #701e2c30}
[data-testid="stExpander"]{border-radius:0!important;border-left:3px solid #813743!important}
[data-testid="stTabs"] button{font-family:monospace!important;letter-spacing:.07em}
[data-testid="stSidebar"]{background:linear-gradient(180deg,#120e14,#090a0d)!important}
[data-testid="stSidebar"] [data-testid="stButton"] button{min-height:46px!important}

/* Readable typography and controls on the dark game UI */
.stApp, [data-testid="stSidebar"],
[data-testid="stSidebar"] p, [data-testid="stSidebar"] label,
[data-testid="stSidebar"] span, [data-testid="stSidebar"] small,
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"],
[data-testid="stWidgetLabel"], [data-testid="stCaptionContainer"],
[data-testid="stMetricLabel"], [data-testid="stMetricValue"],
[data-testid="stAlert"] p, [data-testid="stAlert"] span {
    color: #f1e9e6 !important;
}
[data-testid="stSidebar"] [data-baseweb="input"],
[data-testid="stSidebar"] [data-baseweb="select"] > div,
[data-testid="stSidebar"] [data-baseweb="base-input"],
[data-testid="stSidebar"] input,
[data-testid="stSidebar"] textarea,
[data-testid="stSidebar"] [role="combobox"] {
    background-color: #211b23 !important;
    color: #fff6f2 !important;
    -webkit-text-fill-color: #fff6f2 !important;
    border-color: #77515b !important;
}
[data-testid="stSidebar"] input::placeholder {color:#d0bec3 !important;}
[data-testid="stSidebar"] [data-baseweb="select"] svg,
[data-testid="stSidebar"] [data-baseweb="input"] svg {fill:#f1e9e6 !important;color:#f1e9e6 !important;}
[data-testid="stSidebar"] button {color:#fff4f0 !important;}
[data-testid="stSidebar"] [data-baseweb="select"] [role="option"] {color:#f1e9e6 !important;}
[data-baseweb="popover"] [role="listbox"],
[data-baseweb="popover"] [role="option"] {background:#211b23 !important;color:#f1e9e6 !important;}
/* Text entry throughout the main investigation view */
[data-testid="stMain"] input, [data-testid="stMain"] textarea {
    background-color:#211b23 !important;
    color:#fff6f2 !important;
    -webkit-text-fill-color:#fff6f2 !important;
}
[data-testid="stMain"] input::placeholder, [data-testid="stMain"] textarea::placeholder {color:#d0bec3 !important;}

/* Accessibility: readable alert messages across Streamlit themes */
[data-testid="stAlert"], div[data-testid="stAlert"] {
  background: #25222a !important;
  border: 1px solid #b28090 !important;
  color: #fff3ee !important;
}
[data-testid="stAlert"] *, [data-testid="stAlert"] p,
[data-testid="stAlert"] span, [data-testid="stAlert"] svg,
[data-testid="stAlert"] [data-testid="stMarkdownContainer"] * {
  color: #fff3ee !important;
  -webkit-text-fill-color: #fff3ee !important;
  fill: currentColor;
}
/* Sidebar must stand apart from the page and its collapsed chevron must be visible */
section[data-testid="stSidebar"], [data-testid="stSidebarContent"] {
  background: #25212d !important;
  border-right: 2px solid #b85465 !important;
}
[data-testid="stSidebar"] p, [data-testid="stSidebar"] small,
[data-testid="stSidebar"] label, [data-testid="stSidebar"] span,
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] * {
  color: #f7edeb !important;
  -webkit-text-fill-color: #f7edeb !important;
}
[data-testid="stSidebarCollapsedControl"],
[data-testid="stSidebarCollapseButton"],
[data-testid="stSidebarCollapsedControl"] button,
[data-testid="stSidebarCollapseButton"] button {
  background: #963949 !important;
  border: 1px solid #e7a7b0 !important;
  border-radius: 8px !important;
  box-shadow: 0 2px 16px #000a !important;
  color: #ffffff !important;
}
[data-testid="stSidebarCollapsedControl"] svg,
[data-testid="stSidebarCollapseButton"] svg,
[data-testid="stSidebar"] button svg {
  color: #ffffff !important;
  stroke: #ffffff !important;
}
[data-testid="stSidebar"] [data-testid="stButton"] button {
  background: #4a303e !important;
  border: 1px solid #9e6576 !important;
  color: #ffffff !important;
}
[data-testid="stSidebar"] [data-testid="stButton"] button:hover {
  background: #6b3b4d !important;
  border-color: #e29fac !important;
}
/* White/very pale status cards must never inherit pale text */
[data-testid="stNotification"] {background: #25222a !important;color: #fff !important;}
[data-testid="stNotification"] * {color: #fff !important;-webkit-text-fill-color: #fff !important;}

/* Final readability fix: keep Streamlit pale alert backgrounds, use dark text. */
div[data-testid="stAlert"],
section[data-testid="stSidebar"] div[data-testid="stAlert"] {
  color: #303039 !important;
}
div[data-testid="stAlert"] *,
section[data-testid="stSidebar"] div[data-testid="stAlert"] *,
div[data-testid="stNotification"] *,
section[data-testid="stSidebar"] div[data-testid="stNotification"] * {
  color: #303039 !important;
  -webkit-text-fill-color: #303039 !important;
}
div[data-testid="stAlert"] svg,
div[data-testid="stAlert"] svg *,
div[data-testid="stNotification"] svg,
div[data-testid="stNotification"] svg * {
  color: #303039 !important;
  fill: currentColor !important;
  stroke: currentColor !important;
}
/* Override earlier custom dark alert background only for message boxes. */
div[data-testid="stAlert"] {
  background: #f1f5fa !important;
  border: 1px solid #9eabba !important;
}
div[data-testid="stAlert"][data-baseweb="notification"] { background: #f1f5fa !important; }
div[data-testid="stNotification"] {background: #f1f5fa !important; color: #303039 !important;}

/* Closed sidebar opener: high contrast against the black main screen */
[data-testid="stSidebarCollapsedControl"],
[data-testid="stSidebarCollapsedControl"] > button,
[data-testid="stSidebarCollapseButton"],
[data-testid="stSidebarCollapseButton"] > button,
[data-testid="stSidebarHeader"] button {
  background-color: #b83750 !important;
  color: #fff !important;
  border: 2px solid #ffd6dc !important;
  border-radius: 7px !important;
  opacity: 1 !important;
  box-shadow: 0 0 0 2px #21141a, 0 0 14px #d84c6a88 !important;
}
[data-testid="stSidebarCollapsedControl"] svg,
[data-testid="stSidebarCollapsedControl"] svg *,
[data-testid="stSidebarCollapseButton"] svg,
[data-testid="stSidebarCollapseButton"] svg *,
[data-testid="stSidebarHeader"] button svg,
[data-testid="stSidebarHeader"] button svg * {
  color: white !important;
  stroke: white !important;
  fill: none !important;
  opacity: 1 !important;
}
[data-testid="stSidebarCollapsedControl"]:hover,
[data-testid="stSidebarCollapsedControl"] button:hover,
[data-testid="stSidebarHeader"] button:hover {
  background: #dc526c !important;
}

/* 2026-11-14 FINAL UI: dark, legible notice cards across Streamlit variants */
.stApp div[data-testid="stAlert"],
.stApp div[data-testid="stAlertContainer"],
.stApp div[data-testid="stNotification"],
.stApp div[data-baseweb="notification"],
.stApp [role="alert"] {
    background: #29242e !important;
    background-color: #29242e !important;
    border: 1px solid #977482 !important;
    border-radius: 7px !important;
    color: #fff7f3 !important;
    opacity: 1 !important;
}
.stApp div[data-testid="stAlert"] *,
.stApp div[data-testid="stAlertContainer"] *,
.stApp div[data-testid="stNotification"] *,
.stApp div[data-baseweb="notification"] *,
.stApp [role="alert"] * {
    color: #fff7f3 !important;
    -webkit-text-fill-color: #fff7f3 !important;
    opacity: 1 !important;
}
.stApp div[data-testid="stAlert"] svg,
.stApp div[data-testid="stAlertContainer"] svg,
.stApp [role="alert"] svg {
    stroke: #ffb2c0 !important;
    color: #ffb2c0 !important;
}
/* Actual collapsed-sidebar opener: separate from buttons within the open sidebar */
[data-testid="stSidebarCollapsedControl"],
[data-testid="stSidebarCollapsedControl"] button,
[data-testid="stSidebarCollapseButton"],
[data-testid="stSidebarCollapseButton"] button,
[data-testid="collapsedControl"],
[data-testid="collapsedControl"] button,
button[aria-label="Open sidebar"],
button[aria-label="Expand sidebar"],
button[title="Open sidebar"] {
    background: #d42d4c !important;
    background-color: #d42d4c !important;
    border: 2px solid #ffc7d1 !important;
    border-radius: 9px !important;
    color: #ffffff !important;
    opacity: 1 !important;
    box-shadow: 0 0 12px #e53c668c !important;
}
[data-testid="stSidebarCollapsedControl"] svg,
[data-testid="stSidebarCollapsedControl"] svg *,
[data-testid="collapsedControl"] svg,
[data-testid="collapsedControl"] svg *,
button[aria-label="Open sidebar"] svg,
button[aria-label="Open sidebar"] svg * {
    color: #fff !important;
    stroke: #fff !important;
    stroke-width: 2.8px !important;
    opacity: 1 !important;
}
</style>""",unsafe_allow_html=True)

def config_value(key, default=""):
    try:
        return st.secrets.get(key, os.environ.get(key, default))
    except Exception:
        return os.environ.get(key, default)

ADMIN_PASSWORD = "mt1234"  # MT 진행자용 고정 관리자 비밀번호
INITIAL_POINTS = 0
CRIME_SCENE_IMAGE_PATH = "images/crime_scene.png"
JIAN_ROOM_IMAGE_PATH = "images/jian_room.png"
HYEJUN_ROOM_IMAGE_PATH = "images/hyejun_room.png"
PROF_ROOM_IMAGE_PATH = "images/prof_room.png"
JINSEO_ROOM_IMAGE_PATH = "images/jinseo_room.png"
GEONTAE_ROOM_IMAGE_PATH = "images/gt_room.png"


# ── 8개 조의 진행 기록 저장 ──
# Streamlit Cloud 배포에서는 Supabase 연결이 필수입니다.
SUPABASE_URL = str(config_value("SUPABASE_URL")).rstrip("/")
SUPABASE_KEY = str(config_value("SUPABASE_SERVICE_ROLE_KEY"))
REMOTE_STORAGE = bool(SUPABASE_URL and SUPABASE_KEY)
LOCAL_DB = Path(__file__).with_name("mt_team_state_v2.sqlite3")
SAVE_FIELDS = ("points", "investigated_clues", "interrogated_questions", "final_submission_open", "final_submitted", "final_answers", "stage", "schema_version")
CURRENT_SCHEMA = 3
INTERROGATION_COST = 20
MAX_INTERROGATIONS = 5

def default_team_data():
    return {
        "points": INITIAL_POINTS,
        "investigated_clues": [],
        "interrogated_questions": [],
        "final_submission_open": False,
        "final_submitted": False,
        "final_answers": {"culprit":"", "weapon":"", "time":"", "reason":""},
        "stage": 1,
        "schema_version": CURRENT_SCHEMA,
    }


def normalize_team_data(data):
    """기존 사건의 구매기록을 새 단서에 잘못 매칭하지 않도록 스키마 분리."""
    if not isinstance(data, dict):
        return default_team_data()
    if data.get("schema_version") != CURRENT_SCHEMA:
        # Keep independently submitted final answers across schema revisions.
        # Investigation purchases still reset to avoid mixing clue catalogs.
        migrated = default_team_data()
        submitted = bool(data.get("final_submitted"))
        answers = data.get("final_answers")
        if submitted and isinstance(answers, dict):
            migrated["final_submitted"] = True
            migrated["final_answers"].update({
                key: str(answers.get(key) or "")
                for key in ("culprit", "weapon", "time", "reason")
            })
        return migrated
    base = default_team_data()
    base.update({key: data[key] for key in base if key in data})
    if not isinstance(base.get("final_answers"), dict):
        base["final_answers"] = default_team_data()["final_answers"]
    base["final_answers"] = {
        **default_team_data()["final_answers"], **base["final_answers"]
    }
    base["investigated_clues"] = [k for k in base["investigated_clues"] if k in CLUES]
    base["interrogated_questions"] = [k for k in base["interrogated_questions"] if k in INTERROGATIONS]
    return base


def remote_request(method, team, payload=None):
    url = f"{SUPABASE_URL}/rest/v1/mt_teams"
    if method == "GET":
        url += f"?team_no=eq.{int(team)}&select=data"
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8") if payload is not None else None
    headers = {"apikey": SUPABASE_KEY, "Authorization": f"Bearer {SUPABASE_KEY}",
               "Content-Type":"application/json", "Prefer":"resolution=merge-duplicates,return=minimal"}
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    with urllib.request.urlopen(req, timeout=12) as response:
        raw = response.read().decode("utf-8")
    return json.loads(raw) if raw else None

def load_team_data(team):
    if REMOTE_STORAGE:
        rows = remote_request("GET", team)
        return normalize_team_data(rows[0]["data"]) if rows else default_team_data()
    with sqlite3.connect(LOCAL_DB) as conn:
        conn.execute("CREATE TABLE IF NOT EXISTS mt_teams (team_no INTEGER PRIMARY KEY, data TEXT NOT NULL)")
        row = conn.execute("SELECT data FROM mt_teams WHERE team_no=?", (int(team),)).fetchone()
        return normalize_team_data(json.loads(row[0])) if row else default_team_data()

def write_team_data(team, data):
    if REMOTE_STORAGE:
        remote_request("POST", team, {"team_no":int(team), "data":data})
    else:
        with sqlite3.connect(LOCAL_DB) as conn:
            conn.execute("CREATE TABLE IF NOT EXISTS mt_teams (team_no INTEGER PRIMARY KEY, data TEXT NOT NULL)")
            conn.execute("INSERT OR REPLACE INTO mt_teams (team_no, data) VALUES (?,?)", (int(team), json.dumps(data, ensure_ascii=False)))

def save_progress():
    team = st.session_state.team_no
    if team is None: return
    data = {field: st.session_state[field] for field in SAVE_FIELDS}
    data["investigated_clues"] = sorted(data["investigated_clues"])
    data["interrogated_questions"] = sorted(data["interrogated_questions"])
    try:
        write_team_data(team, data)
    except Exception as exc:
        st.error(f"진행 상황 저장 실패: {exc}. 네트워크를 확인하고 다시 시도하세요.")
        st.stop()

def restore_progress(team):
    data = load_team_data(team)
    for field in SAVE_FIELDS:
        st.session_state[field] = set(data.get(field, [])) if field in ("investigated_clues", "interrogated_questions") else data.get(field, default_team_data()[field])

# ─────────────────────────────────────
# 장소 목록
# ─────────────────────────────────────
LOCATIONS = {
    "사건 현장": "사건 현장 - 과방",
    "이지안": "이지안의 방",
    "전혜준": "전혜준의 방",
    "변상균 교수": "변상균 교수 연구실",
    "박진서": "박진서의 방",
    "고건태": "고건태의 방",
}


# ─────────────────────────────────────
# 사건 현장 hotspot
# x, y, width, height는 전체 이미지 대비 비율(0~1)
# 한 hotspot에 여러 clue_id를 연결할 수 있습니다.
# ─────────────────────────────────────
# 새로 확정한 방 이미지의 빨간 박스에 대응하는 클릭 좌표 (0~1)
# 같은 물건에 단서가 여러 개 있으면 세부 조사 메뉴를 표시합니다.
CRIME_SCENE_HOTSPOTS = {'extinguisher': {'name': '소화기',
                  'x': 0.70925,
                  'y': 0.16851,
                  'width': 0.0366,
                  'height': 0.09392,
                  'clue_ids': ['scene_extinguisher']},
 'bat': {'name': '야구방망이',
         'x': 0.534,
         'y': 0.124,
         'width': 0.042,
         'height': 0.154,
         'clue_ids': ['scene_bat']},
 'wrench': {'name': '몽키스패너',
            'x': 0.12155,
            'y': 0.61326,
            'width': 0.06768,
            'height': 0.07551,
            'clue_ids': ['scene_wrench']},
 'body': {'name': '시신',
          'x': 0.52348,
          'y': 0.4512,
          'width': 0.20166,
          'height': 0.30847,
          'clue_ids': ['scene_wound1']},
 'report': {'name': '서류',
            'x': 0.284,
            'y': 0.658,
            'width': 0.067,
            'height': 0.067,
            'clue_ids': ['scene_wound2']},
 'floor': {'name': '바닥',
           'x': 0.76174,
           'y': 0.73481,
           'width': 0.05801,
           'height': 0.05801,
           'clue_ids': ['scene_red_paint']},
 'watch': {'name': '시계',
           'x': 0.67196,
           'y': 0.52578,
           'width': 0.0297,
           'height': 0.06169,
           'clue_ids': ['scene_watch']},
 'cctv': {'name': '상자',
          'x': 0.87155,
          'y': 0.0221,
          'width': 0.07528,
          'height': 0.09484,
          'clue_ids': ['scene_cctv']},
 'drink': {'name': '박카스',
           'x': 0.283,
           'y': 0.303,
           'width': 0.031,
           'height': 0.081,
           'clue_ids': ['scene_bacchus']},
 'phone': {'name': '휴대전화',
           'x': 0.336,
           'y': 0.319,
           'width': 0.038,
           'height': 0.065,
           'clue_ids': ['scene_story']},
 'cash': {'name': '운동가방',
          'x': 0.1471,
          'y': 0.17035,
          'width': 0.11878,
          'height': 0.10497,
          'clue_ids': ['scene_cash']},
 'tablet': {'name': '태블릿',
            'x': 0.848,
            'y': 0.466,
            'width': 0.065,
            'height': 0.065,
            'clue_ids': ['scene_tod']}}
JIAN_ROOM_HOTSPOTS = {'id': {'name': '신분증', 'x': 0.054, 'y': 0.098, 'width': 0.095, 'height': 0.092, 'clue_ids': ['jian_id']}, 'phone': {'name': '휴대전화', 'x': 0.16713, 'y': 0.38398, 'width': 0.06906, 'height': 0.08656, 'clue_ids': ['jian_threat', 'jian_event', 'jian_search']}, 'diary': {'name': '일기장', 'x': 0.67196, 'y': 0.33425, 'width': 0.08771, 'height': 0.09853, 'clue_ids': ['jian_diary']}, 'medicine': {'name': '처방전', 'x': 0.82113, 'y': 0.56814, 'width': 0.09669, 'height': 0.11326, 'clue_ids': ['jian_sleep']}, 'bankbook': {'name': '통장', 'x': 0.8384, 'y': 0.69337, 'width': 0.08356, 'height': 0.06906, 'clue_ids': ['jian_cash']}}
HYEJUN_ROOM_HOTSPOTS = {'letter': {'name': '편지', 'x': 0.25, 'y': 0.32781, 'width': 0.09945, 'height': 0.0663, 'clue_ids': ['hyejun_letter']}, 'bag': {'name': '가방', 'x': 0.38398, 'y': 0.25783, 'width': 0.10843, 'height': 0.12891, 'clue_ids': ['hyejun_knife']}, 'ring': {'name': '반지 상자', 'x': 0.53315, 'y': 0.4558, 'width': 0.07459, 'height': 0.07182, 'clue_ids': ['hyejun_ring']}, 'bin': {'name': '쓰레기통', 'x': 0.14572, 'y': 0.49355, 'width': 0.08011, 'height': 0.1418, 'clue_ids': ['hyejun_receipt', 'hyejun_xphoto']}, 'phone': {'name': '휴대전화', 'x': 0.89641, 'y': 0.68508, 'width': 0.0663, 'height': 0.12155, 'clue_ids': ['hyejun_chat']}, 'handed': {'name': '진료기록지', 'x': 0.75691, 'y': 0.65101, 'width': 0.12362, 'height': 0.16667, 'clue_ids': ['hyejun_left']}}
PROF_ROOM_HOTSPOTS = {'pc': {'name': '모니터', 'x': 0.746, 'y': 0.27, 'width': 0.202, 'height': 0.228, 'clue_ids': ['prof_cctv']},
 'phone': {'name': '휴대전화',
           'x': 0.75483,
           'y': 0.52302,
           'width': 0.07113,
           'height': 0.09024,
           'clue_ids': ['prof_kakao']},
 'receipt': {'name': '가방',
             'x': 0.04627,
             'y': 0.34162,
             'width': 0.11671,
             'height': 0.11418,
             'clue_ids': ['prof_receipt']},
 'research': {'name': '연구일지',
              'x': 0.53936,
              'y': 0.50552,
              'width': 0.18163,
              'height': 0.10958,
              'clue_ids': ['prof_research']},
 'news': {'name': '신문기사',
          'x': 0.31837,
          'y': 0.46869,
          'width': 0.14572,
          'height': 0.09116,
          'clue_ids': ['prof_award']},
 'shoes': {'name': '운동화',
           'x': 0.23204,
           'y': 0.75506,
           'width': 0.12569,
           'height': 0.12339,
           'clue_ids': ['prof_shoes']},
 'pc_left': {'name': '모니터',
             'x': 0.545,
             'y': 0.262,
             'width': 0.202,
             'height': 0.235,
             'clue_ids': ['prof_korea']}}
JINSEO_ROOM_HOTSPOTS = {'pc': {'name': '컴퓨터', 'x': 0.066, 'y': 0.205, 'width': 0.21, 'height': 0.163, 'clue_ids': ['jinseo_post']}, 'phone': {'name': '휴대전화', 'x': 0.63398, 'y': 0.33886, 'width': 0.09116, 'height': 0.10497, 'clue_ids': ['jinseo_bodyphoto', 'jinseo_search']}, 'counsel': {'name': '서류', 'x': 0.87086, 'y': 0.19982, 'width': 0.10014, 'height': 0.15746, 'clue_ids': ['jinseo_child']}, 'gloves': {'name': '장갑 상자', 'x': 0.85635, 'y': 0.38029, 'width': 0.12224, 'height': 0.13352, 'clue_ids': ['jinseo_gloves']}, 'diary': {'name': '일기장', 'x': 0.34323, 'y': 0.58287, 'width': 0.13191, 'height': 0.17403, 'clue_ids': ['jinseo_diary']}, 'sketch': {'name': '손글씨 메모', 'x': 0.50829, 'y': 0.62247, 'width': 0.08978, 'height': 0.10037, 'clue_ids': ['jinseo_sketch']}}
GEONTAE_ROOM_HOTSPOTS = {'newspaper': {'name': '신문기사', 'x': 0.25829, 'y': 0.73665, 'width': 0.21616, 'height': 0.14825, 'clue_ids': ['geontae_news']}, 'phone': {'name': '휴대전화', 'x': 0.11809, 'y': 0.42541, 'width': 0.06492, 'height': 0.06538, 'clue_ids': ['geontae_help', 'geontae_chat']}, 'album': {'name': '앨범', 'x': 0.87569, 'y': 0.13904, 'width': 0.10981, 'height': 0.14641, 'clue_ids': ['geontae_album']}, 'documents': {'name': '서류', 'x': 0.66782, 'y': 0.37109, 'width': 0.14019, 'height': 0.08287, 'clue_ids': ['geontae_supplies']}, 'keepsakes': {'name': '상자', 'x': 0.4116, 'y': 0.27993, 'width': 0.09461, 'height': 0.093, 'clue_ids': ['geontae_keepsakes']}, 'laptop': {'name': '맥북', 'x': 0.66782, 'y': 0.27993, 'width': 0.14019, 'height': 0.093, 'clue_ids': ['geontae_findmy']}}


# ─────────────────────────────────────
# 실제로 포인트를 사용해 얻는 단서
# image에 파일 경로를 넣으면 결과 화면에서 자동 표시됩니다.
# 예: "images/clues/wound_report_1.png"
# ─────────────────────────────────────
def find_clue_image(folder, filename):
    """파일 확장자가 PNG/JPG/JPEG여도 자동으로 연결합니다."""
    for extension in (".png", ".jpg", ".jpeg", ".webp", ".PNG", ".JPG", ".JPEG"):
        path = os.path.join(folder, filename + extension)
        if os.path.isfile(path):
            return path
    return os.path.join(folder, filename + ".png")


CLUES = {'scene_extinguisher': {'menu_name': '소화기',
                        'name': '붉은 소화기',
                        'cost': 10,
                        'location': '사건 현장 - 과방',
                        'source': '소화기',
                        'result': ['붉은 ABC 소화기의 하단 도막이 벗겨져 회색 금속 표면이 드러나 있다.',
                                   '표면 시료에서 폴리에스터계 수지와 산화철계 적색 안료(Fe₂O₃)가 확인된다.'],
                        'image': 'images/clues/scene_extinguisher.png',
                        'clue_no': 1},
 'scene_bat': {'menu_name': '방망이',
               'name': '야구방망이',
               'cost': 10,
               'location': '사건 현장 - 과방',
               'source': '야구방망이',
               'result': ['목재 야구방망이의 손잡이와 표면에 오래 쌓인 먼지가 보인다.'],
               'image': 'images/clues/baseball_bat.png',
               'clue_no': 2},
 'scene_wrench': {'menu_name': '스패너',
                  'name': '붉은 손잡이 몽키스패너',
                  'cost': 10,
                  'location': '사건 현장 - 과방',
                  'source': '몽키스패너',
                  'result': ['은색 몽키스패너의 손잡이는 붉은 고무 재질이며 일부가 벗겨져 있다.', '손잡이 재료에서는 합성고무계 고분자와 유기 적색 안료가 확인된다.'],
                  'image': 'images/clues/scene_wrench.png',
                  'clue_no': 3},
 'scene_red_paint': {'menu_name': '조각',
                     'name': '붉은 도료 조각 감식',
                     'cost': 10,
                     'location': '사건 현장 - 과방',
                     'source': '바닥',
                     'result': ['혈흔 주변에 비교적 굵은 붉은 도료 조각들이 흩어져 있다.', '시료에서 폴리에스터계 수지와 산화철계 적색 안료(Fe₂O₃)가 확인된다.'],
                     'image': 'images/clues/red_paint_analysis.png',
                     'clue_no': 4},
 'scene_wound1': {'menu_name': '시신',
                  'name': '시신의 상처 사진',
                  'cost': 10,
                  'location': '사건 현장 - 과방',
                  'source': '시신',
                  'result': ['머리 오른쪽 주요 외상'],
                  'image': 'images/clues/scene_wound1.png',
                  'clue_no': 5},
 'scene_wound2': {'menu_name': '서류',
                  'name': '두부 손상 감식 보고서',
                  'cost': 10,
                  'location': '사건 현장 - 과방',
                  'source': '감식자료',
                  'result': [],
                  'image': 'images/clues/scene_wound2.png',
                  'clue_no': 6},
 'scene_tod': {'menu_name': '태블릿',
               'name': '사망 추정 시각 전문가 메일',
               'cost': 10,
               'location': '사건 현장 - 과방',
               'source': '감정 메일',
               'result': [],
               'image': 'images/clues/scene_deathtime_mail.png',
               'clue_no': 7},
 'scene_watch': {'menu_name': '시계',
                 'name': '파손된 손목시계',
                 'cost': 10,
                 'location': '사건 현장 - 과방',
                 'source': '손목시계',
                 'result': [],
                 'image': 'images/clues/scene_watch.png',
                 'clue_no': 8},
 'scene_cctv': {'menu_name': '상자',
                'name': '상자와 CCTV',
                'cost': 10,
                'location': '사건 현장 - 과방',
                'source': '캐비닛 위',
                'result': ['과방 캐비닛 위의 CCTV 렌즈 앞에 상자가 놓여 있다.', '카메라 시야가 일부 가려지는 배치다.'],
                'image': 'images/clues/scene_cctv.png',
                'clue_no': 9},
 'scene_bacchus': {'menu_name': '음료',
                   'name': '개봉된 박카스',
                   'cost': 10,
                   'location': '사건 현장 - 과방',
                   'source': '탁자',
                   'result': ['원형 탁자에 개봉된 박카스가 거의 남아 있다.', '수면 유도 성분이 검출되었지만 피해자가 이를 마셨다는 근거는 확인되지 않는다.'],
                   'image': 'images/clues/scene_bacchus.png',
                   'clue_no': 10},
 'scene_story': {'menu_name': '휴대전화',
                 'name': '구성민 SNS 스토리',
                 'cost': 10,
                 'location': '사건 현장 - 과방',
                 'source': '휴대전화',
                 'result': [],
                 'image': 'images/clues/scene_sns_story.png',
                 'clue_no': 11},
 'scene_cash': {'menu_name': '가방',
                'name': '현금 2,000만 원',
                'cost': 10,
                'location': '사건 현장 - 과방',
                'source': '운동가방',
                'result': [],
                'image': 'images/clues/scene_cash_bag.png',
                'clue_no': 12},
 'jian_cash': {'menu_name': '통장',
               'name': '2,000만 원 금융기록',
               'cost': 10,
               'location': '이지안의 방',
               'source': '통장',
               'result': [],
               'image': 'images/clues/jian_bank_record.png',
               'clue_no': 1},
 'jian_threat': {'menu_name': '메시지',
                 'name': '구성민의 협박 DM',
                 'cost': 10,
                 'location': '이지안의 방',
                 'source': '휴대전화',
                 'result': [],
                 'image': 'images/clues/jian_dm.png',
                 'clue_no': 2},
 'jian_event': {'menu_name': '사진',
                'name': '잠실 행사 사진',
                'cost': 10,
                'location': '이지안의 방',
                'source': '휴대전화',
                'result': [],
                'image': 'images/clues/jian_event_alibi.png',
                'clue_no': 3},
 'jian_id': {'menu_name': '신분증',
             'name': '이지안 신분증',
             'cost': 10,
             'location': '이지안의 방',
             'source': '신분증',
             'result': [],
             'image': 'images/clues/jian_id_card.png',
             'clue_no': 4},
 'jian_sleep': {'menu_name': '처방전',
                'name': '수면제 처방 기록',
                'cost': 10,
                'location': '이지안의 방',
                'source': '처방전',
                'result': [],
                'image': 'images/clues/jian_sleep_prescription.png',
                'clue_no': 5},
 'jian_diary': {'menu_name': '일기장',
                'name': '9월 13일 일기',
                'cost': 10,
                'location': '이지안의 방',
                'source': '일기장',
                'result': [],
                'image': 'images/clues/jian_diary_0913.png',
                'clue_no': 6},
 'jian_search': {'menu_name': '검색',
                 'name': '최근 검색 기록',
                 'cost': 10,
                 'location': '이지안의 방',
                 'source': '휴대전화',
                 'result': [],
                 'image': 'images/clues/jian_search_history.png',
                 'clue_no': 7},
 'hyejun_letter': {'menu_name': '편지',
                   'name': '고백 편지',
                   'cost': 10,
                   'location': '전혜준의 방',
                   'source': '편지',
                   'result': [],
                   'image': 'images/clues/hyejun_love_letter.png',
                   'clue_no': 1},
 'hyejun_receipt': {'menu_name': '영수증',
                    'name': '마호가니 카페 영수증',
                    'cost': 10,
                    'location': '전혜준의 방',
                    'source': '쓰레기통',
                    'result': [],
                    'image': 'images/clues/hyejun_mahogany_receipt.png',
                    'clue_no': 2},
 'hyejun_left': {'menu_name': '진료기록',
                 'name': '왼손 타박상 기록',
                 'cost': 10,
                 'location': '전혜준의 방',
                 'source': '진료기록지',
                 'result': [],
                 'image': 'images/clues/hyejun_left_hand_record.png',
                 'clue_no': 3},
 'hyejun_ring': {'menu_name': '반지',
                 'name': '커플링 두 개',
                 'cost': 10,
                 'location': '전혜준의 방',
                 'source': '반지 상자',
                 'result': [],
                 'image': 'images/clues/hyejun_ring_box.png',
                 'clue_no': 4},
 'hyejun_knife': {'menu_name': '가방',
                  'name': '가방 속 칼',
                  'cost': 10,
                  'location': '전혜준의 방',
                  'source': '가방',
                  'result': [],
                  'image': 'images/clues/hyejun_bag_knife.png',
                  'clue_no': 5},
 'hyejun_xphoto': {'menu_name': '사진',
                   'name': '찢어진 사진',
                   'cost': 10,
                   'location': '전혜준의 방',
                   'source': '쓰레기통',
                   'result': [],
                   'image': 'images/clues/hyejun_torn_photo.png',
                   'clue_no': 6},
 'hyejun_chat': {'menu_name': '메시지',
                 'name': '9월 15일 카카오톡',
                 'cost': 10,
                 'location': '전혜준의 방',
                 'source': '휴대전화',
                 'result': [],
                 'image': 'images/clues/hyejun_kakaotalk_0915.png',
                 'clue_no': 7},
 'prof_cctv': {'menu_name': '모니터',
               'name': '연구실 CCTV',
               'cost': 10,
               'location': '변상균 교수 연구실',
               'source': '컴퓨터',
               'result': [],
               'image': 'images/clues/prof_cctv_june.png',
               'clue_no': 1},
 'prof_kakao': {'menu_name': '메시지',
                'name': '구성민과 약속 카카오톡',
                'cost': 10,
                'location': '변상균 교수 연구실',
                'source': '휴대전화',
                'result': [],
                'image': 'images/clues/prof_meeting_kakaotalk.png',
                'clue_no': 2},
 'prof_korea': {'menu_name': '이메일',
                'name': '조교가 보낸 RED-17 이메일',
                'cost': 10,
                'location': '변상균 교수 연구실',
                'source': '컴퓨터',
                'result': [],
                'image': 'images/clues/prof_red17_email.png',
                'clue_no': 3},
 'prof_receipt': {'menu_name': '영수증',
                  'name': '17:13 고깃집 영수증',
                  'cost': 10,
                  'location': '변상균 교수 연구실',
                  'source': '가방',
                  'result': [],
                  'image': 'images/clues/prof_bbq_receipt.png',
                  'clue_no': 4},
 'prof_award': {'menu_name': '신문',
                'name': 'RED-17 노벨상 기사',
                'cost': 10,
                'location': '변상균 교수 연구실',
                'source': '신문기사',
                'result': [],
                'image': 'images/clues/prof_red17_nobel_newspaper.png',
                'clue_no': 5},
 'prof_research': {'menu_name': '일지',
                   'name': 'RED-17 연구일지',
                   'cost': 10,
                   'location': '변상균 교수 연구실',
                   'source': '연구일지',
                   'result': [],
                   'image': 'images/clues/prof_red17_research_log.png',
                   'clue_no': 6},
 'prof_shoes': {'menu_name': '운동화',
                'name': '붉은 흔적이 묻은 운동화',
                'cost': 10,
                'location': '변상균 교수 연구실',
                'source': '운동화',
                'result': ['연구실 바닥의 흰 운동화 앞코에 붉은 도료 흔적이 있다.', '검출된 입자 성분은 폴리에스터계 수지와 산화철계 적색 안료(Fe₂O₃)다.'],
                'image': 'images/clues/prof_shoes_red_paint.png',
                'clue_no': 7},
 'jinseo_sketch': {'menu_name': '메모',
                   'name': 'CCTV 위치 스케치',
                   'cost': 10,
                   'location': '박진서의 방',
                   'source': '손글씨 메모',
                   'result': [],
                   'image': 'images/clues/jinseo_cctv_sketch.png',
                   'clue_no': 1},
 'jinseo_diary': {'menu_name': '일기장',
                  'name': '9월 15일 일기',
                  'cost': 10,
                  'location': '박진서의 방',
                  'source': '일기장',
                  'result': [],
                  'image': 'images/clues/jinseo_diary_0915.png',
                  'clue_no': 2},
 'jinseo_bodyphoto': {'menu_name': '사진',
                      'name': '18:28 시신 사진',
                      'cost': 10,
                      'location': '박진서의 방',
                      'source': '휴대전화',
                      'result': [],
                      'image': 'images/clues/jinseo_corpse_photo_1828.png',
                      'clue_no': 3},
 'jinseo_child': {'menu_name': '기록지',
                  'name': '어린 시절 정신과 상담 기록',
                  'cost': 10,
                  'location': '박진서의 방',
                  'source': '상담 기록',
                  'result': [],
                  'image': 'images/clues/jinseo_child_psychiatry_record.png',
                  'clue_no': 4},
 'jinseo_gloves': {'menu_name': '장갑',
                   'name': '붉은 도료가 묻은 목장갑',
                   'cost': 10,
                   'location': '박진서의 방',
                   'source': '장갑 상자',
                   'result': [],
                   'image': 'images/clues/jinseo_stained_gloves.png',
                   'clue_no': 5},
 'jinseo_search': {'menu_name': '검색',
                   'name': '둔기 손상 관련 검색',
                   'cost': 10,
                   'location': '박진서의 방',
                   'source': '휴대전화',
                   'result': [],
                   'image': 'images/clues/jinseo_blunt_force_search.png',
                   'clue_no': 6},
 'jinseo_post': {'menu_name': '게시글',
                 'name': '익명 게시글',
                 'cost': 10,
                 'location': '박진서의 방',
                 'source': '컴퓨터',
                 'result': [],
                 'image': 'images/clues/jinseo_anonymous_post.png',
                 'clue_no': 7},
 'geontae_news': {'menu_name': '신문',
                  'name': '고등학생 학교폭력 사망 기사',
                  'cost': 10,
                  'location': '고건태의 방',
                  'source': '신문기사',
                  'result': [],
                  'image': 'images/clues/gt_bullying_article.png',
                  'clue_no': 1},
 'geontae_help': {'menu_name': '대화 1',
                  'name': '9월 12일 도움 요청 카카오톡',
                  'cost': 10,
                  'location': '고건태의 방',
                  'source': '휴대전화',
                  'result': [],
                  'image': 'images/clues/gt_kakaotalk_help_0912.png',
                  'clue_no': 2},
 'geontae_album': {'menu_name': '앨범',
                   'name': '고선태·구성민 졸업앨범',
                   'cost': 10,
                   'location': '고건태의 방',
                   'source': '졸업앨범',
                   'result': [],
                   'image': 'images/clues/gt_graduation_yearbook.png',
                   'clue_no': 3},
 'geontae_chat': {'menu_name': '대화 2',
                  'name': '9월 15일 방문 카카오톡',
                  'cost': 10,
                  'location': '고건태의 방',
                  'source': '휴대전화',
                  'result': [],
                  'image': 'images/clues/gt_kakaotalk_visit_0915.png',
                  'clue_no': 4},
 'geontae_keepsakes': {'menu_name': '상자',
                       'name': '형의 유품 상자',
                       'cost': 10,
                       'location': '고건태의 방',
                       'source': '상자',
                       'result': [],
                       'image': 'images/clues/gt_brother_keepsake_box.png',
                       'clue_no': 5},
 'geontae_supplies': {'menu_name': '서류',
                      'name': '학과 물품 수량 확인 요청',
                      'cost': 10,
                      'location': '고건태의 방',
                      'source': '학과 자료',
                      'result': [],
                      'image': 'images/clues/gt_missing_supplies.png',
                      'clue_no': 6},
 'geontae_findmy': {'menu_name': '맥북',
                    'name': '왼쪽 AirPod 사운드 재생 기록',
                    'cost': 10,
                    'location': '고건태의 방',
                    'source': '맥북',
                    'result': [],
                    'image': 'images/clues/gt_findmy_airpods_1728.png',
                    'clue_no': 7}}
# ── 이미지 경로 호환성: 기존 GitHub 폴더 / 새 images 폴더 모두 지원 ──
# 테스트 모드가 아닌 실제 클릭형 이미지 조사 화면을 사용합니다.
GAME_ROOT = Path(__file__).resolve().parent
_IMAGE_LOOKUP = {}

def resolve_game_image(original_path):
    if not original_path:
        return original_path
    original = Path(original_path)
    direct_candidates = [
        GAME_ROOT / original,
        GAME_ROOT / "총엠_추리게임" / original,
        GAME_ROOT / "총엠 레크 게임 수정본" / original,
    ]
    for candidate in direct_candidates:
        if candidate.is_file():
            return str(candidate)
    # GitHub에 이미지를 '과방 단서', '고건태 방' 등 원래 폴더에 업로드한 경우
    filename = original.name.lower()
    if filename not in _IMAGE_LOOKUP:
        matches = sorted(
            (p for p in GAME_ROOT.rglob('*')
             if p.is_file() and p.name.lower() == filename and '.git' not in p.parts),
            key=lambda p: (len(p.parts), str(p)),
        )
        _IMAGE_LOOKUP[filename] = str(matches[0]) if matches else str(GAME_ROOT / original)
    return _IMAGE_LOOKUP[filename]

CRIME_SCENE_IMAGE_PATH = resolve_game_image(CRIME_SCENE_IMAGE_PATH)
JIAN_ROOM_IMAGE_PATH = resolve_game_image(JIAN_ROOM_IMAGE_PATH)
HYEJUN_ROOM_IMAGE_PATH = resolve_game_image(HYEJUN_ROOM_IMAGE_PATH)
PROF_ROOM_IMAGE_PATH = resolve_game_image(PROF_ROOM_IMAGE_PATH)
JINSEO_ROOM_IMAGE_PATH = resolve_game_image(JINSEO_ROOM_IMAGE_PATH)
GEONTAE_ROOM_IMAGE_PATH = resolve_game_image(GEONTAE_ROOM_IMAGE_PATH)
for _clue in CLUES.values():
    if _clue.get("image"):
        _clue["image"] = resolve_game_image(_clue["image"])



INTERROGATIONS = {'jian_q1': {'suspect': '이지안',
             'number': 1,
             'question': '사건 당일 오후에는 무엇을 하고 계셨나요?',
             'answer': '“그날 오후 4시 반쯤 성민 오빠를 만나러 과방에 갔어요. 개인적으로 해결해야 할 일이 있었거든요. 오래 있지는 않았고, 5시쯤에는 학교에서 나왔어요. '
                       '저녁에 잠실에서 열리는 행사가 있었는데, 행사는 6시 반에 시작해도 6시까지는 입장을 마쳐야 했거든요. 그래서 시간이 좀 빠듯했어요. 실제로 행사장에도 '
                       '6시 전에 도착했고요.”'},
 'jian_q2': {'suspect': '이지안',
             'number': 2,
             'question': '구성민과는 어떤 관계였나요? 최근 특별한 일은 없었나요?',
             'answer': '“같은 과 선후배 사이였어요. 원래는 별문제 없었는데, 최근에는 정말 얼굴도 보기 싫을 정도였어요. 성민 오빠가 저에 대해 남들에게 알려지고 싶지 않은 '
                       '사실을 알고 있었거든요. 그걸 가지고 계속 협박했어요. 처음에는 부탁하는 척하더니 나중에는 돈까지 요구하더라고요. 그게 알려지면 제가 지금까지 쌓아 온 '
                       '것들이 다 무너질 수도 있었어요. 솔직히 그때는 성민 오빠가 제 인생에서 그냥 사라져 버렸으면 좋겠다고 생각하기도 했어요. 하지만 그런 생각을 했다고 '
                       '해서 제가 진짜 사람을 죽였다는 건 아니잖아요.”'},
 'jian_q3': {'suspect': '이지안',
             'number': 3,
             'question': '사건과 관련해서 알고 계신 다른 이야기가 있나요?',
             'answer': '“성민 오빠가 저한테만 그런 식으로 행동한 건 아닌 것 같아요. 다른 사람한테도 사람 마음을 가지고 장난치는 것처럼 보일 때가 있었거든요. 특히 '
                       '전혜준이 성민 오빠랑 가까워지고 싶어 했는데, 둘 사이가 좀 복잡했던 것 같아요. 자세한 사정까지 제가 말씀드리기는 그렇지만, 혜준이도 성민 오빠 '
                       '때문에 많이 힘들어했던 걸로 알아요.”'},
 'jian_q4': {'suspect': '이지안',
             'number': 4,
             'question': '지금까지 말씀하신 것 외에 추가로 이야기할 부분이 있을까요?',
             'answer': '“그날 돈을 가져간 건 맞아요. 정말 어쩔 수 없다고 생각했거든요. 그리고 성민 오빠한테 박카스를 하나 건넨 것도 맞아요. 사실... 그냥 평범한 '
                       '박카스는 아니었어요. 오빠가 잠들면 휴대전화에 있는 제 자료를 없애려고 했거든요. 그런데 오빠는 그걸 마시지 않았어요. 제가 나올 때도 그대로 '
                       '있었고요. 제가 잘못한 건 인정해요. 그렇지만 정말 죽일 생각은 없었어요.”'},
 'hyejun_q1': {'suspect': '전혜준',
               'number': 1,
               'question': '사건 당일 오후에는 무엇을 하고 계셨나요?',
               'answer': '“2시 반쯤 성민이 형을 만나러 과방에 갔어요. 근데 안에서 누가 엄청 크게 싸우는 소리가 나더라고요. 분위기가 너무 안 좋아 보여서 들어가지는 '
                         '않았어요. 그렇다고 바로 집에 간 건 아니에요. 마호가니에 앉아서 형이 나오기를 기다렸어요. 혹시라도 형이 나오면 다시 얘기해 보려고요. 꽤 오래 '
                         '기다렸는데 결국 못 만났어요. 정확히 몇 시에 나왔는지는 잘 기억 안 나요.”'},
 'hyejun_q2': {'suspect': '전혜준',
               'number': 2,
               'question': '구성민과는 어떤 관계였나요? 최근 특별한 일은 없었나요?',
               'answer': '“제가 성민이 형을 좋아했던 건 맞아요. 그냥 친한 선후배 이상의 감정이었어요. 근데 형은 제 마음을 받아주지 않았고, 제가 줬던 반지도 버렸어요. '
                         '저는 그게 정말 이해가 안 됐어요. 그렇게 쉽게 버릴 거면 처음부터 왜 받아줬는지도 모르겠고요. 그 일 때문에 크게 다퉜어요. 제가 좀 심한 말도 '
                         '했고요. 근데 좋아했던 사람한테 거절당해서 화났다는 이유로 제가 범인이 되는 건 아니잖아요.”'},
 'hyejun_q3': {'suspect': '전혜준',
               'number': 3,
               'question': '사건과 관련해서 알고 계신 다른 이야기가 있나요?',
               'answer': '“과방 앞에 갔을 때 들었던 목소리 중 하나가 변상균 교수님이었던 것 같아요. 교수님이 성민이 형한테 엄청 화를 내고 계셨어요. 정확히 무슨 '
                         '얘기인지는 모르겠는데, 중간에 갑자기 ‘쾅’ 하는 소리도 들렸어요. 그냥 책상 같은 걸 세게 친 건가 싶었는데, 분위기가 정말 험악했어요. 저는 '
                         '괜히 끼어들기 싫어서 그냥 돌아섰어요.”'},
 'hyejun_q4': {'suspect': '전혜준',
               'number': 4,
               'question': '지금까지 말씀하신 것 외에 추가로 이야기할 부분이 있을까요?',
               'answer': '“제가 형한테 화가 나서 좀 이상한 행동을 했던 건 맞아요. 사진을 찢거나 얼굴 부분을 훼손한 것도 사실이고, 편지에 심한 말을 쓴 것도 인정해요. '
                         '그때는 정말 형이 저만큼 괴로웠으면 좋겠다고 생각했거든요. 하지만 그걸 실제로 행동에 옮길 생각은 없었어요. 그리고 왼손에 난 상처는 며칠 전에 '
                         '물건을 옮기다가 생긴 거예요. 사건 당일에 누굴 때리거나 해서 다친 건 아니에요. 제가 형을 많이 좋아했던 건 사실이지만, 그렇다고 죽일 생각까지 '
                         '했던 건 아니에요.”'},
 'prof_q1': {'suspect': '변상균 교수',
             'number': 1,
             'question': '사건 당일 오후에는 무엇을 하고 계셨나요?',
             'answer': '“오후 2시경 구성민 학생을 만나러 과방에 갔습니다. 최근 연구와 관련해 확인해야 할 문제가 있었거든요. 이후에는 제 업무를 봤고, 저녁에는 외부 '
                       '일정이 있었습니다. 다른 사람들과 식사 약속이 있었죠. 그날 결제한 기록도 남아 있을 겁니다. 오후 5시... 그쯤이었던 것 같은데 정확한 시간까지는 '
                       '기억나지 않습니다.”'},
 'prof_q2': {'suspect': '변상균 교수',
             'number': 2,
             'question': '구성민과는 어떤 관계였나요? 최근 특별한 일은 없었나요?',
             'answer': '“구성민 학생은 제 연구와 관련된 학생이었습니다. 그런데 최근 제 연구 내용이 외부로 유출된 정황을 확인했습니다. 상당한 시간과 노력을 들인 연구였고, '
                       '아직 공개되지 않은 내용도 포함되어 있었죠. 확인해 보니 구성민 학생이 허가 없이 연구실에 출입한 기록까지 있었습니다. 당연히 본인에게 설명을 '
                       '요구했지만, 끝까지 제대로 답하지 않았습니다. 지도하는 입장에서 실망이 컸고, 화가 났던 것도 사실입니다. 하지만 연구 문제로 다퉜다는 것과 사람을 '
                       '살해했다는 것은 전혀 다른 이야기입니다.”'},
 'prof_q3': {'suspect': '변상균 교수',
             'number': 3,
             'question': '사건과 관련해서 알고 계신 다른 이야기가 있나요?',
             'answer': '“그날 과방에서 구성민 학생과 이야기를 나누다가, 오후에 이지안 학생과 만나기로 했다는 말을 들었습니다. 개인적인 약속인 것 같아서 자세한 이유까지 '
                       '묻지는 않았습니다. 두 학생 사이에 어떤 일이 있었는지는 저도 모릅니다. 다만 그날 구성민 학생이 저 말고도 만날 사람이 있었다는 건 말씀드릴 수 '
                       '있겠네요.”'},
 'prof_q4': {'suspect': '변상균 교수',
             'number': 4,
             'question': '지금까지 말씀하신 것 외에 추가로 이야기할 부분이 있을까요?',
             'answer': '“그날 구성민 학생과 언쟁이 상당히 격해졌던 건 인정합니다. 저도 평소보다 화가 많이 나 있었고, 대화를 마치고 나가려다가 출입문 근처에 있던 소화기를 '
                       '발로 찼습니다. 감정적으로 행동한 건 사실이죠. 하지만 그것뿐입니다. 구성민 학생에게 직접 손을 대거나 때린 적은 없습니다. 제가 화를 냈다는 '
                       '사실만으로 살인까지 저질렀다고 생각하신다면 그건 지나친 추측입니다.”'},
 'jinseo_q1': {'suspect': '박진서',
               'number': 1,
               'question': '사건 당일 오후에는 무엇을 하고 계셨나요?',
               'answer': '“오후에는 개인적인 일을 하고 있었어요. 과방에 간 건 저녁 6시 25분쯤이었고요. 들어가니까 성민 오빠가 바닥에 쓰러져 있더라고요. 처음에는 그냥 '
                         '자는 건가 싶었는데, 가까이 가 보니까 아무 반응도 없었어요. 그런데 좀 이상하더라고요. 평소에는 그렇게 말도 많고 잘난 척하던 사람이 그렇게 '
                         '조용히 있으니까요. 사진이요? 네, 찍었어요. 나중에 상황을 다시 확인할 수도 있으니까요. 그 순간에는 당황하기보다 일단 눈앞에 있는 걸 '
                         '남겨둬야겠다는 생각이 먼저 들었던 것 같아요. 신고는 6시 40분에 했어요. 왜 바로 하지 않았냐고요? 글쎄요. 그때는 그렇게 시간이 많이 지난 줄 '
                         '몰랐어요.”'},
 'jinseo_q2': {'suspect': '박진서',
               'number': 2,
               'question': '구성민과는 어떤 관계였나요? 최근 특별한 일은 없었나요?',
               'answer': '“같은 과 선배였어요. 친하지는 않았고, 솔직히 좋아하지도 않았어요. 성민 오빠는 사람들 앞에서는 좋은 사람인 척하면서 뒤에서는 다른 사람을 '
                         '무시하는 일이 많았거든요. 저는 그런 사람들이 좀 우스워요. 자기가 남한테 상처 주는 건 아무렇지도 않아 하면서, 정작 자기가 조금만 불편해져도 '
                         '세상이 무너진 것처럼 굴잖아요. 가끔 궁금하긴 했어요. 그런 사람이 정말 감당하기 힘든 상황에 놓이면 어떻게 행동할지. 평소처럼 잘난 척할 수 '
                         '있을지, 아니면 다른 사람들처럼 무너질지요. ...왜 그렇게 보세요? 궁금할 수도 있는 거 아닌가요?”'},
 'jinseo_q3': {'suspect': '박진서',
               'number': 3,
               'question': '사건과 관련해서 알고 계신 다른 이야기가 있나요?',
               'answer': '“직접 본 건 없어요. 제가 갔을 때는 이미 성민 오빠가 쓰러져 있었으니까요. 그런데 혜준이한테 들은 얘기가 있어요. 성민 오빠랑 변상균 교수님 '
                         '사이가 꽤 안 좋았다고 하더라고요. 그날도 교수님이 성민 오빠한테 크게 화를 냈다는 얘기를 들었어요. 연구 때문에 무슨 문제가 있었다던데요. 사람이 '
                         '그렇게까지 화를 내는 데는 이유가 있겠죠. 물론 화가 났다고 반드시 사람을 죽이는 건 아니지만요.”'},
 'jinseo_q4': {'suspect': '박진서',
               'number': 4,
               'question': '지금까지 말씀하신 것 외에 추가로 이야기할 부분이 있을까요?',
               'answer': '“제가 원래 남들이 별로 관심 갖지 않는 것들을 궁금해하는 편이긴 해요. 사람이 크게 다치면 몸에 어떤 변화가 생기는지, 그런 것도 찾아본 적 '
                         '있어요. 직접 겪어본 적 없는 상황이니까 궁금할 수도 있잖아요. 작업용 장갑이요? 아, 그거요. 과방에서 물건 정리할 때 쓰던 거예요. 공구 같은 '
                         '걸 만진 적도 있고요. CCTV요? 제가 그걸 왜 가렸겠어요. 오히려 그런 게 있으면 누가 무슨 짓을 했는지 알아내기 쉽지 않나요? 물론 누군가는 '
                         '카메라를 가리고 싶었겠죠. 안 찍히고 싶은 일이 있었다면요. 그런데 제가 그랬다는 증거라도 있나요?”'},
 'geontae_q1': {'suspect': '고건태',
                'number': 1,
                'question': '사건 당일 오후에는 무엇을 하고 계셨나요?',
                'answer': '“그날 오후 5시쯤 성민이 형을 만나러 과방에 갔어요. 며칠 전부터 형한테 물어보고 싶은 게 있었거든요. 카톡으로 얘기하기에는 좀 복잡한 문제라 '
                          '직접 만나서 얘기하려고 했어요. 그런데 막상 만나니까 생각했던 것처럼 대화가 잘 풀리지는 않았어요. 형도 좀 불편해하는 것 같았고요. 그래서 더 '
                          '얘기해 봐야 소용없겠다 싶어서 5시 10분쯤 나왔어요. 그 후에는 바로 집으로 갔습니다. 과방에 다시 돌아갈 이유도 없었고, 실제로 돌아간 적도 '
                          '없어요. 그건 분명히 말씀드릴 수 있습니다.”'},
 'geontae_q2': {'suspect': '고건태',
                'number': 2,
                'question': '구성민과는 어떤 관계였나요? 최근 특별한 일은 없었나요?',
                'answer': '“성민이 형은 평소에 알고 지내던 형이에요. 저한테도 잘해 주셨고요. 사실 얼마 전에 저희 형 물건을 정리하다가 예전에 다니던 학교 졸업앨범을 '
                          '봤어요. 그러다가 성민이 형 이름을 발견했어요. 예전에 저희 형을 괴롭혔던 사람 중에 구성민이라는 이름이 있었다는 건 알고 있었어요. 그런데 설마 '
                          '제가 아는 성민이 형일 거라고는 생각도 못 했어요. 그냥 이름이 같은 다른 사람일 거라고 생각했거든요. 그래서 좀 혼란스러웠어요. 제가 알고 '
                          '지내던 성민이 형은 그런 사람이 아니라고 생각했으니까요. 형한테 직접 예전 일에 대해 물어보고 싶었어요. 당시 무슨 일이 있었는지 알고 있을 수도 '
                          '있고, 다른 사람들에게 사과를 받는 데 도움을 줄 수도 있다고 생각했거든요. 저는 성민이 형을 믿고 있었어요. 적어도 저한테는 제대로 이야기해 줄 '
                          '거라고 생각했어요.”'},
 'geontae_q3': {'suspect': '고건태',
                'number': 3,
                'question': '사건과 관련해서 알고 계신 다른 이야기가 있나요?',
                'answer': '“직접 수상한 사람을 본 건 없어요. 근데 예전에 성민이 형이 변상균 교수님 연구실로 불려간 적이 있었다고 들었어요. 그때도 분위기가 별로 안 '
                          '좋았다고 하더라고요. 정확히 무슨 문제였는지는 저도 잘 몰라요. 그냥 연구 관련해서 교수님이 성민이 형한테 화가 났다는 얘기를 들은 정도예요. '
                          '그날도 두 분이 만났다는 이야기가 있던데, 혹시 그 문제와 관련된 건 아닌가요?”'},
 'geontae_q4': {'suspect': '고건태',
                'number': 4,
                'question': '지금까지 말씀하신 것 외에 추가로 이야기할 부분이 있을까요?',
                'answer': '“제가 성민이 형을 만나러 간 건 정말 도움을 부탁하기 위해서였어요. 저희 형과 관련해서 예전에 무슨 일이 있었는지 알고 싶었고, 성민이 형이라면 '
                          '조금이라도 도와줄 수 있을 거라고 생각했거든요. 근데 생각했던 것만큼 쉬운 얘기는 아니더라고요. 저도 좀 실망했던 건 사실이에요. 그래도 제가 '
                          '형을 해치려고 찾아간 건 아니에요. 애초에 그럴 생각이었으면 도움을 부탁하지도 않았겠죠. 그날 과방에 갔던 건 맞지만, 제가 말씀드릴 수 있는 건 '
                          '그게 전부예요.”'}}


# ─────────────────────────────────────
# 무료 기본 자료
# 나중에 image 경로를 넣으면 자동으로 이미지가 표시됩니다.
# ─────────────────────────────────────
FREE_MATERIALS = {
    "floorplan": {
        "name": "과방 평면도",
        "image": None,
    },
    "inventory": {
        "name": "과방 비품 목록",
        "image": None,
    },
}


# ─────────────────────────────────────
# session_state 초기화
# ─────────────────────────────────────
defaults = {
    "stage": 1,
    "team_no": None,
    "points": INITIAL_POINTS,
    "current_view": None,
    "admin_ok": False,
    "investigated_clues": set(),
    "interrogated_questions": set(),
    "schema_version": CURRENT_SCHEMA,
    "pending_clue_id": None,
    "selected_hotspot_id": None,
    "last_click_xy": None,
    "last_click_ratio": None,
    "last_revealed_clue_id": None,
    "debug_mode": False,
    "reset_confirm": False,
    "image_click_nonce": 0,
    "evidence_return_view": None,
    "final_submission_open": False,
    "final_submitted": False,
    "final_answers": {"culprit":"", "weapon":"", "time":"", "reason":""},
}

for key, value in defaults.items():
    if key not in st.session_state:
        if isinstance(value, (set, dict)):
            st.session_state[key] = value.copy()
        else:
            st.session_state[key] = value


# ─────────────────────────────────────
# 유틸리티
# ─────────────────────────────────────
def is_unlocked(location_key: str) -> bool:
    stage = st.session_state.stage
    if stage == 1:
        return location_key == "사건 현장"
    return True  # 2·3차 조사에는 과방과 모든 용의자 방 개방


def clear_transient_states():
    st.session_state.pending_clue_id = None
    st.session_state.selected_hotspot_id = None
    st.session_state.last_click_xy = None
    st.session_state.last_click_ratio = None
    st.session_state.last_revealed_clue_id = None


def clue_is_available(clue_id: str) -> bool:
    """현재 조사 단계에서 해당 단서를 볼 수 있는지 확인합니다."""
    clue = CLUES[clue_id]
    # 조사 가능 여부는 장소의 잠금 상태로만 결정합니다.
    # 동일 장소 내 모든 단서는 선행 단서 없이 조사할 수 있습니다.
    return True


def available_clue_ids(hotspot: dict):
    """hotspot에 연결된 단서 중 현재 단계에서 열려 있는 것만 반환합니다."""
    return [
        clue_id
        for clue_id in hotspot["clue_ids"]
        if clue_is_available(clue_id)
    ]


def refresh_image_click_component():
    """이전 이미지 클릭값이 다음 화면에서 재사용되는 것을 막습니다."""
    st.session_state.image_click_nonce += 1
    st.session_state.last_click_xy = None
    st.session_state.last_click_ratio = None


def reset_investigation():
    st.session_state.stage = 1
    st.session_state.points = INITIAL_POINTS
    st.session_state.investigated_clues = set()
    st.session_state.interrogated_questions = set()
    st.session_state.schema_version = CURRENT_SCHEMA
    st.session_state.final_submission_open = False
    st.session_state.final_submitted = False
    st.session_state.final_answers = default_team_data()["final_answers"].copy()
    clear_transient_states()
    st.session_state.reset_confirm = False
    save_progress()


# 방 사진은 여러 번 클릭할 때마다 다시 디코딩하지 않도록 서버 메모리에 보관합니다.
# 방 전체 이미지에 한해서 화면용 크기로 조절하며, 단서 원본 이미지는 수정하지 않습니다.
@st.cache_resource(show_spinner=False, max_entries=12)
def _cached_room_image(path, file_mtime_ns):
    with Image.open(path) as source:
        image = source.convert("RGB")
        image.thumbnail((1400, 1400), Image.Resampling.LANCZOS)
        return image


def load_room_image(path):
    return _cached_room_image(path, os.stat(path).st_mtime_ns)



# 클릭형 위젯에 큰 PIL 이미지를 매번 직렬화하지 않고 가벼운 JPEG 파일 경로를 전달합니다.
# 이미지의 가로세로 비율은 유지하므로 기존 상대좌표 핫스팟은 변경하지 않습니다.
@st.cache_resource(show_spinner=False, max_entries=12)
def _fast_room_preview(path, modified_ns):
    import hashlib
    import tempfile
    digest = hashlib.sha256(f"{path}:{modified_ns}".encode()).hexdigest()[:20]
    cache_dir = Path(tempfile.gettempdir()) / "mt_mystery_room_previews"
    cache_dir.mkdir(parents=True, exist_ok=True)
    preview_file = cache_dir / f"{digest}.jpg"
    if not preview_file.is_file():
        with Image.open(path) as src:
            preview = src.convert("RGB")
            preview.thumbnail((1200, 1200), Image.Resampling.LANCZOS)
            preview.save(preview_file, format="JPEG", quality=78, optimize=True)
    return str(preview_file)


def fast_room_image(path, debug_mode, overlay_func):
    if debug_mode:
        return overlay_func(load_room_image(path))
    # 경로를 넘기면 image-coordinates가 파일을 바로 사용합니다.
    return _fast_room_preview(path, os.stat(path).st_mtime_ns)

def show_optional_image(path):
    if path and os.path.exists(path):
        st.image(path, use_container_width=True)
    elif path:
        st.warning(f"단서 이미지 파일을 찾지 못했습니다: {path}")


def find_hotspot(x_ratio: float, y_ratio: float):
    matches = []

    for hotspot_id, hotspot in CRIME_SCENE_HOTSPOTS.items():
        x0 = hotspot["x"]
        y0 = hotspot["y"]
        x1 = x0 + hotspot["width"]
        y1 = y0 + hotspot["height"]

        if x0 <= x_ratio <= x1 and y0 <= y_ratio <= y1:
            area = hotspot["width"] * hotspot["height"]
            matches.append((area, hotspot_id))

    if not matches:
        return None

    matches.sort(key=lambda item: item[0])
    return matches[0][1]

def find_jian_hotspot(x_ratio: float, y_ratio: float):
    matches = []

    for hotspot_id, hotspot in JIAN_ROOM_HOTSPOTS.items():
        x0 = hotspot["x"]
        y0 = hotspot["y"]
        x1 = x0 + hotspot["width"]
        y1 = y0 + hotspot["height"]

        if x0 <= x_ratio <= x1 and y0 <= y_ratio <= y1:
            area = hotspot["width"] * hotspot["height"]
            matches.append((area, hotspot_id))

    if not matches:
        return None

    matches.sort(key=lambda item: item[0])
    return matches[0][1]

def draw_debug_overlay(base_image: Image.Image) -> Image.Image:
    image = base_image.copy().convert("RGB")
    draw = ImageDraw.Draw(image)
    width, height = image.size

    for hotspot_id, hotspot in CRIME_SCENE_HOTSPOTS.items():
        x0 = hotspot["x"] * width
        y0 = hotspot["y"] * height
        x1 = (hotspot["x"] + hotspot["width"]) * width
        y1 = (hotspot["y"] + hotspot["height"]) * height

        draw.rectangle([x0, y0, x1, y1], outline="red", width=3)
        

    return image

def draw_jian_debug_overlay(base_image: Image.Image) -> Image.Image:
    image = base_image.copy().convert("RGB")
    draw = ImageDraw.Draw(image)
    width, height = image.size

    for hotspot_id, hotspot in JIAN_ROOM_HOTSPOTS.items():
        x0 = hotspot["x"] * width
        y0 = hotspot["y"] * height
        x1 = (hotspot["x"] + hotspot["width"]) * width
        y1 = (hotspot["y"] + hotspot["height"]) * height

        draw.rectangle([x0, y0, x1, y1], outline="red", width=3)
        

    return image


def find_hyejun_hotspot(x_ratio: float, y_ratio: float):
    # 노트북은 조사 대상에서 제외: 클릭해도 단서 및 구매창을 열지 않음.
    if 0.75 <= x_ratio <= 0.94 and 0.39 <= y_ratio <= 0.59:
        return None
    matches = []
    for hotspot_id, hotspot in HYEJUN_ROOM_HOTSPOTS.items():
        x0, y0 = hotspot["x"], hotspot["y"]
        x1 = x0 + hotspot["width"]
        y1 = y0 + hotspot["height"]
        if x0 <= x_ratio <= x1 and y0 <= y_ratio <= y1:
            matches.append((hotspot["width"] * hotspot["height"], hotspot_id))
    if not matches:
        return None
    matches.sort(key=lambda item: item[0])
    return matches[0][1]

def draw_hyejun_debug_overlay(base_image: Image.Image) -> Image.Image:
    image = base_image.copy().convert("RGB")
    draw = ImageDraw.Draw(image)
    width, height = image.size
    for hotspot_id, hotspot in HYEJUN_ROOM_HOTSPOTS.items():
        x0 = hotspot["x"] * width
        y0 = hotspot["y"] * height
        x1 = (hotspot["x"] + hotspot["width"]) * width
        y1 = (hotspot["y"] + hotspot["height"]) * height
        draw.rectangle([x0, y0, x1, y1], outline="red", width=3)
        
    return image


def find_prof_hotspot(x_ratio: float, y_ratio: float):
    matches = []
    for hotspot_id, hotspot in PROF_ROOM_HOTSPOTS.items():
        x0, y0 = hotspot["x"], hotspot["y"]
        x1 = x0 + hotspot["width"]
        y1 = y0 + hotspot["height"]

        if x0 <= x_ratio <= x1 and y0 <= y_ratio <= y1:
            matches.append((hotspot["width"] * hotspot["height"], hotspot_id))

    if not matches:
        return None

    matches.sort(key=lambda item: item[0])
    return matches[0][1]


def draw_prof_debug_overlay(base_image: Image.Image) -> Image.Image:
    image = base_image.copy().convert("RGB")
    draw = ImageDraw.Draw(image)
    width, height = image.size

    for hotspot_id, hotspot in PROF_ROOM_HOTSPOTS.items():
        x0 = hotspot["x"] * width
        y0 = hotspot["y"] * height
        x1 = (hotspot["x"] + hotspot["width"]) * width
        y1 = (hotspot["y"] + hotspot["height"]) * height

        draw.rectangle([x0, y0, x1, y1], outline="red", width=3)
        

    return image



def find_jinseo_hotspot(x_ratio: float, y_ratio: float):
    matches = []
    for hotspot_id, hotspot in JINSEO_ROOM_HOTSPOTS.items():
        x0, y0 = hotspot["x"], hotspot["y"]
        x1 = x0 + hotspot["width"]
        y1 = y0 + hotspot["height"]

        if x0 <= x_ratio <= x1 and y0 <= y_ratio <= y1:
            matches.append((hotspot["width"] * hotspot["height"], hotspot_id))

    if not matches:
        return None

    matches.sort(key=lambda item: item[0])
    return matches[0][1]


def draw_jinseo_debug_overlay(base_image: Image.Image) -> Image.Image:
    image = base_image.copy().convert("RGB")
    draw = ImageDraw.Draw(image)
    width, height = image.size

    for hotspot_id, hotspot in JINSEO_ROOM_HOTSPOTS.items():
        x0 = hotspot["x"] * width
        y0 = hotspot["y"] * height
        x1 = (hotspot["x"] + hotspot["width"]) * width
        y1 = (hotspot["y"] + hotspot["height"]) * height

        draw.rectangle([x0, y0, x1, y1], outline="red", width=3)
        

    return image



def find_geontae_hotspot(x_ratio: float, y_ratio: float):
    matches = []
    for hotspot_id, hotspot in GEONTAE_ROOM_HOTSPOTS.items():
        x0, y0 = hotspot["x"], hotspot["y"]
        x1 = x0 + hotspot["width"]
        y1 = y0 + hotspot["height"]

        if x0 <= x_ratio <= x1 and y0 <= y_ratio <= y1:
            matches.append((hotspot["width"] * hotspot["height"], hotspot_id))

    if not matches:
        return None

    matches.sort(key=lambda item: item[0])
    return matches[0][1]


def draw_geontae_debug_overlay(base_image: Image.Image) -> Image.Image:
    image = base_image.copy().convert("RGB")
    draw = ImageDraw.Draw(image)
    width, height = image.size

    for hotspot_id, hotspot in GEONTAE_ROOM_HOTSPOTS.items():
        x0 = hotspot["x"] * width
        y0 = hotspot["y"] * height
        x1 = (hotspot["x"] + hotspot["width"]) * width
        y1 = (hotspot["y"] + hotspot["height"]) * height

        draw.rectangle([x0, y0, x1, y1], outline="red", width=3)
        

    return image


# ─────────────────────────────────────
# 사이드바
# ─────────────────────────────────────
@st.fragment
def render_sidebar_controls():
    st.markdown("**◈ INVESTIGATION TERMINAL**")
    st.caption("CASE FILE 001 · ACCESS CONTROL")
    st.header("팀 설정")

    if st.session_state.team_no is None:
        team_input = st.selectbox("담당 조 선택", list(range(1, 9)), format_func=lambda x: f"{x}조")
        if st.button("게임 시작", use_container_width=True):
            try:
                restore_progress(team_input)
                st.session_state.team_no = team_input
                st.session_state.admin_ok = False
                st.rerun()
            except Exception as exc:
                st.error(f"조별 데이터 연결 실패: {exc}")
    else:
        st.write(f"현재 담당 조: **{st.session_state.team_no}조**")
        if st.button("담당 조에서 나가기"):
            save_progress()
            st.session_state.team_no = None
            st.session_state.admin_ok = False
            st.session_state.current_view = None
            st.rerun()

    st.divider()
    st.header("관리자 전용")
    if not ADMIN_PASSWORD:
        st.caption("관리자 비밀번호가 설정되지 않았습니다. .streamlit/secrets.toml에 ADMIN_PASSWORD를 지정하세요.")

    if not st.session_state.admin_ok:
        pw = st.text_input("관리자 비밀번호", type="password")
        if st.button("관리자 로그인"):
            if ADMIN_PASSWORD and pw == ADMIN_PASSWORD:
                st.session_state.admin_ok = True
                st.rerun(scope="fragment")
            else:
                st.error("비밀번호가 틀렸습니다.")
    else:
        st.success("관리자 로그인 상태")

        new_stage = st.radio(
            "조사 단계 변경",
            options=[1, 2, 3],
            index=max(0,min(2,st.session_state.stage - 1)),
            format_func=lambda x: f"{x}차 조사",
        )
        if st.button("이 단계로 적용", use_container_width=True):
            st.session_state.stage = new_stage
            save_progress()
            clear_transient_states()
            refresh_image_click_component()
            st.rerun()

        st.divider()
        st.subheader("조사 포인트 조정")
        st.write(f"현재 조사 포인트: **{st.session_state.points}P**")

        p1, p2 = st.columns(2)
        with p1:
            if st.button("+10P", use_container_width=True):
                st.session_state.points += 10
                save_progress()
                st.rerun()
            if st.button("+5P", use_container_width=True):
                st.session_state.points += 5
                save_progress()
                st.rerun()

        with p2:
            if st.button("+20P", use_container_width=True):
                st.session_state.points += 20
                save_progress()
                st.rerun()
            if st.button("-10P", use_container_width=True):
                st.session_state.points = max(0, st.session_state.points - 10)
                save_progress()
                st.rerun()

        st.divider()
        st.subheader("최종 추리 제출")

        if st.session_state.stage < 3:
            st.caption("최종 추리 제출은 3차 조사에서 오픈하는 것을 권장합니다.")

        if not st.session_state.final_submission_open:
            if st.button("최종 추리 제출 오픈", use_container_width=True):
                st.session_state.final_submission_open = True
                save_progress()
                st.rerun()
        else:
            st.success("최종 추리 제출이 열려 있습니다.")
            if st.button("최종 추리 제출 마감", use_container_width=True):
                st.session_state.final_submission_open = False
                save_progress()
                st.rerun()

        if st.session_state.final_submitted:
            with st.expander("현재 팀 제출 내용 확인"):
                labels = {"culprit":"범인", "weapon":"범행도구", "time":"범행 추정 시각", "reason":"동기 및 추리 근거"}
                for field, label in labels.items():
                    st.write(f"**{label}**")
                    st.write(st.session_state.final_answers.get(field, ""))
            if st.button("현재 팀 제출 초기화", use_container_width=True):
                st.session_state.final_submitted = False
                st.session_state.final_answers = default_team_data()["final_answers"].copy()
                save_progress()
                st.rerun()

        st.divider()
        st.subheader("전체 팀 최종 답안 수합")
        st.caption("8개 팀의 제출 결과를 저장소에서 직접 불러옵니다. 제출 내용을 다운로드해 채점할 수 있습니다.")
        if not REMOTE_STORAGE:
            st.error("⚠ 공유 저장소 연결 없음: 현재 제출은 서버의 임시 SQLite에 저장됩니다. 서버가 재시작되면 기록이 사라질 수 있고, 다른 실행 서버의 제출을 수합할 수 없습니다. 8개 팀의 최종 제출을 실제로 수합하려면 Streamlit Cloud의 Secrets에 SUPABASE_URL과 SUPABASE_SERVICE_ROLE_KEY를 설정해야 합니다.")
        else:
            st.caption("● 제출 수합 저장소: Supabase 연결됨")
        if st.button("8개 팀 제출 현황 불러오기", key="admin_collect_final", use_container_width=True):
            try:
                submissions = []
                for team_number in range(1, 9):
                    record = load_team_data(team_number)
                    answers = record.get("final_answers") or {}
                    submissions.append({
                        "조": f"{team_number}조",
                        "제출 여부": "제출 완료" if record.get("final_submitted") else "미제출",
                        "범인": answers.get("culprit", "") if record.get("final_submitted") else "",
                        "범행도구": answers.get("weapon", "") if record.get("final_submitted") else "",
                        "범행 추정 시각": answers.get("time", "") if record.get("final_submitted") else "",
                        "동기 및 추리 근거": answers.get("reason", "") if record.get("final_submitted") else "",
                    })
                st.session_state["admin_final_submissions"] = submissions
            except Exception as exc:
                st.error(f"제출 현황 조회 실패: {exc}")
        if "admin_final_submissions" in st.session_state:
            submissions = st.session_state["admin_final_submissions"]
            finished = sum(x["제출 여부"] == "제출 완료" for x in submissions)
            st.write(f"**제출 완료: {finished} / 8팀**")
            st.dataframe(submissions, hide_index=True, use_container_width=True)
            out = io.StringIO()
            csv_writer = csv.DictWriter(out, fieldnames=list(submissions[0].keys()))
            csv_writer.writeheader()
            csv_writer.writerows(submissions)
            st.download_button(
                "최종 추리 결과 CSV 다운로드",
                data=out.getvalue().encode("utf-8-sig"),
                file_name="MT_최종추리_8개팀_제출결과.csv",
                mime="text/csv",
                key="admin_final_csv",
                use_container_width=True,
            )
            st.caption("목록을 최신으로 갱신하려면 '8개 팀 제출 현황 불러오기'를 다시 누르세요.")

        st.divider()
        st.subheader("개발/테스트")
        st.checkbox("디버그 모드", key="debug_mode")
        if st.session_state.debug_mode:
            st.caption("사건 현장 이미지에 hotspot 영역과 디버그 버튼이 표시됩니다.")

        st.divider()
        st.subheader("조사 진행상태 초기화")

        if not st.session_state.reset_confirm:
            if st.button("조사상태 초기화", use_container_width=True):
                st.session_state.reset_confirm = True
                st.rerun(scope="fragment")
        else:
            st.warning("정말 현재 팀의 조사 진행상태를 초기화하시겠습니까?")
            r1, r2 = st.columns(2)

            with r1:
                if st.button("초기화 실행", type="primary", use_container_width=True):
                    reset_investigation()
                    st.success("초기화했습니다.")
                    st.rerun()

            with r2:
                if st.button("취소", key="reset_cancel", use_container_width=True):
                    st.session_state.reset_confirm = False
                    st.rerun(scope="fragment")

        if st.button("관리자 로그아웃", use_container_width=True):
            st.session_state.admin_ok = False
            st.session_state.debug_mode = False
            st.session_state.reset_confirm = False
            st.rerun(scope="fragment")

with st.sidebar:
    render_sidebar_controls()

# ─────────────────────────────────────
# 팀 번호 입력 전
# ─────────────────────────────────────
if st.session_state.team_no is None:
    st.title("🔍 학생회장 살인사건")
    st.info("왼쪽 사이드바에서 담당 조를 선택한 뒤 게임 시작을 눌러주세요. 관리자 로그인 없이도 조사할 수 있습니다.")
    st.stop()


if not REMOTE_STORAGE:
    st.sidebar.warning("현재 로컬 SQLite 저장 방식입니다. Streamlit Cloud에서는 서버 재시작 시 기록이 사라질 수 있으므로 Supabase 설정 후 행사에 사용하세요.")

# 모든 조사 화면에서 증거 보관함으로 이동하는 고정 메뉴
with st.sidebar:
    st.divider()
    if st.button("📁 증거 보관함", key="global_evidence_vault", use_container_width=True):
        clear_transient_states()
        refresh_image_click_component()
        if st.session_state.current_view != "확보한 단서":
            st.session_state.evidence_return_view = st.session_state.current_view
        st.session_state.current_view = "확보한 단서"
        st.rerun()
    if st.session_state.current_view is not None:
        if st.button("⌂ 메인 화면", key="global_home", use_container_width=True):
            clear_transient_states()
            refresh_image_click_component()
            st.session_state.current_view = None
            st.rerun()

# ─────────────────────────────────────
# 단서 결과 화면
# ─────────────────────────────────────
def render_clue_reveal_screen(clue_id: str):
    clue = CLUES[clue_id]

    st.markdown('<div class="game-section">▌ EVIDENCE ACQUIRED / 증거 확보</div>',unsafe_allow_html=True)
    if clue.get("image") and os.path.isfile(clue["image"]):
        show_optional_image(clue["image"])
    else:
        st.warning("단서 이미지 파일을 찾을 수 없습니다.")
    st.subheader(clue["name"])
    for line in clue.get("result", []):
        st.write(line)

    st.divider()

    if st.button("↶ 이전 조사 화면으로 돌아가기", key="reveal_return", use_container_width=True):
        # 사건 현장 또는 용의자의 방을 그대로 유지하고, 증거 화면만 닫습니다.
        st.session_state.last_revealed_clue_id = None
        st.session_state.pending_clue_id = None
        st.session_state.selected_hotspot_id = None
        refresh_image_click_component()
        st.rerun(scope="fragment")


# ─────────────────────────────────────
# 단서 구매 확인
# ─────────────────────────────────────
def render_confirm_box(clue_id: str):
    clue = CLUES[clue_id]
    already_done = clue_id in st.session_state.investigated_clues
    display_name = clue["name"] if already_done else clue.get("menu_name", clue["name"])

    st.divider()
    with st.container(border=True):
        st.subheader(display_name)

        if already_done:
            st.info("이미 조사한 단서입니다.")
            if st.button(
                "결과 다시 보기",
                key=f"already_done_reveal_{clue_id}",
                use_container_width=True,
            ):
                st.session_state.pending_clue_id = None
                st.session_state.selected_hotspot_id = None
                refresh_image_click_component()
                st.session_state.last_revealed_clue_id = clue_id
                st.rerun(scope="fragment")
        else:
            st.write(f"조사 비용: **{clue['cost']}P**")
            st.write(f"현재 조사 포인트: **{st.session_state.points}P**")

            enough_points = st.session_state.points >= clue["cost"]
            if not enough_points:
                st.warning("조사 포인트가 부족합니다.")

            st.write(f"**{display_name}**을(를) 조사하시겠습니까?")

            c1, c2 = st.columns(2)

            with c1:
                if st.button(
                    "조사하기",
                    key=f"confirm_investigate_{clue_id}",
                    disabled=not enough_points,
                    use_container_width=True,
                ):
                    st.session_state.points -= clue["cost"]
                    st.session_state.investigated_clues.add(clue_id)
                    save_progress()

                    # 이전 hotspot/pending 상태를 완전히 비운 뒤 결과 화면으로 이동
                    st.session_state.pending_clue_id = None
                    st.session_state.selected_hotspot_id = None
                    refresh_image_click_component()
                    st.session_state.last_revealed_clue_id = clue_id
                    st.rerun(scope="fragment")

            with c2:
                if st.button(
                    "취소",
                    key=f"cancel_investigate_{clue_id}",
                    use_container_width=True,
                ):
                    st.session_state.pending_clue_id = None
                    refresh_image_click_component()
                    st.rerun(scope="fragment")


# ─────────────────────────────────────
# 여러 단서가 있는 hotspot의 세부 조사 메뉴
# ─────────────────────────────────────
def render_hotspot_menu(hotspot_id: str):
    """사건 현장 사진 아래에 표시되는 다중 단서 선택 패널."""
    hotspot = CRIME_SCENE_HOTSPOTS[hotspot_id]

    st.divider()
    with st.container(border=True):
        st.subheader(f"🔎 {hotspot['name']}")
        st.write("조사할 항목을 선택하세요.")

        visible_clue_ids = available_clue_ids(hotspot)

        if not visible_clue_ids:
            st.info("현재 조사 단계에서는 추가로 확인할 수 있는 자료가 없습니다.")

        for clue_id in visible_clue_ids:
            clue = CLUES[clue_id]
            done = clue_id in st.session_state.investigated_clues

            if done:
                label = f"✅ {clue['name']} - 조사 완료"
            else:
                menu_label = clue.get("menu_name", clue["name"])
                label = f"{menu_label} - {clue['cost']}P"

            if st.button(
                label,
                key=f"subclue_{hotspot_id}_{clue_id}",
                use_container_width=True,
            ):
                # 다른 단서의 확인창이 남지 않도록 먼저 비움
                st.session_state.pending_clue_id = None

                if done:
                    st.session_state.selected_hotspot_id = None
                    refresh_image_click_component()
                    st.session_state.last_revealed_clue_id = clue_id
                else:
                    st.session_state.pending_clue_id = clue_id

                st.rerun(scope="fragment")

        if st.button(
            "선택 닫기",
            key=f"close_hotspot_{hotspot_id}",
            use_container_width=True,
        ):
            st.session_state.selected_hotspot_id = None
            st.session_state.pending_clue_id = None
            refresh_image_click_component()
            st.rerun(scope="fragment")

# ─────────────────────────────────────
# 용의자 방(이지안 방 등) 공용 다중 단서 메뉴
#
# 사건 현장의 render_hotspot_menu()는 절대 수정하지 않고 그대로 둡니다.
# 이 함수는 이지안의 방을 비롯해 앞으로 추가될 용의자 공간에서
# "한 hotspot에 단서가 여러 개인 경우"를 안전하게 처리하기 위해
# 새로 추가한 별도 함수입니다. 기존 코드 경로에는 영향이 없습니다.
# ─────────────────────────────────────
def render_room_hotspot_menu(hotspots: dict, hotspot_id: str, room_label: str):
    """용의자 방 사진 아래에 표시되는 다중 단서 선택 패널."""
    hotspot = hotspots[hotspot_id]

    st.divider()
    with st.container(border=True):
        st.subheader(f"🔎 {hotspot['name']}")
        st.write("조사할 항목을 선택하세요.")

        for clue_id in hotspot["clue_ids"]:
            clue = CLUES[clue_id]
            done = clue_id in st.session_state.investigated_clues

            if done:
                label = f"✅ {clue['name']} - 조사 완료"
            else:
                menu_label = clue.get("menu_name", clue["name"])
                label = f"{menu_label} - {clue['cost']}P"

            if st.button(
                label,
                key=f"room_subclue_{hotspot_id}_{clue_id}",
                use_container_width=True,
            ):
                st.session_state.pending_clue_id = None

                if done:
                    st.session_state.selected_hotspot_id = None
                    refresh_image_click_component()
                    st.session_state.last_revealed_clue_id = clue_id
                else:
                    st.session_state.pending_clue_id = clue_id

                st.rerun(scope="fragment")

        if st.button(
            "선택 닫기",
            key=f"room_close_{hotspot_id}",
            use_container_width=True,
        ):
            st.session_state.selected_hotspot_id = None
            st.session_state.pending_clue_id = None
            refresh_image_click_component()
            st.rerun(scope="fragment")

# ─────────────────────────────────────
# 디버그용 단서 버튼
# ─────────────────────────────────────

def render_debug_button_list():
    st.divider()
    st.caption("🛠 디버그 모드: 아래 버튼으로 모든 단서를 직접 테스트할 수 있습니다.")

    clue_ids = list(CLUES.keys())
    cols = st.columns(3)

    for i, clue_id in enumerate(clue_ids):
        clue = CLUES[clue_id]
        done = clue_id in st.session_state.investigated_clues

        with cols[i % 3]:
            label = (
                f"✅ {clue['name']} - 다시 보기"
                if done
                else f"{clue['name']} - {clue['cost']}P"
            )

            if st.button(label, key=f"debug_{clue_id}", use_container_width=True):
                if done:
                    st.session_state.last_revealed_clue_id = clue_id
                else:
                    st.session_state.pending_clue_id = clue_id
                st.rerun(scope="fragment")

    if st.session_state.pending_clue_id is not None:
        render_confirm_box(st.session_state.pending_clue_id)



def render_no_image_clue_menu(location_name):
    """방 이미지 제작 전에도 48개 단서를 포인트를 지불해 테스트할 수 있게 함."""
    st.warning("방 이미지가 아직 등록되지 않았습니다. 아래 임시 조사 메뉴에서 기능을 테스트할 수 있습니다.")
    st.caption("이미지 파일을 지정하면 물건 클릭 조사 화면으로 전환됩니다.")
    for cid,clue in CLUES.items():
        if clue["location"] != location_name:
            continue
        acquired = cid in st.session_state.investigated_clues
        label = f"✅ {clue['name']} (재열람)" if acquired else f"{clue['menu_name']} · {clue['cost']}P"
        if st.button(label, key=f"fallback_{cid}", use_container_width=True):
            st.session_state.selected_hotspot_id = None
            st.session_state.pending_clue_id = None
            if acquired:
                st.session_state.last_revealed_clue_id = cid
            else:
                st.session_state.pending_clue_id = cid
            st.rerun(scope="fragment")
    if st.session_state.pending_clue_id:
        render_confirm_box(st.session_state.pending_clue_id)


# ─────────────────────────────────────
# 사건 현장 화면
# ─────────────────────────────────────
def render_crime_scene():
    if st.session_state.last_revealed_clue_id is not None:
        render_clue_reveal_screen(st.session_state.last_revealed_clue_id)
        return

    st.title("📍 사건 현장 - 과방")

    top1, top2 = st.columns(2)

    with top1:
        st.metric("현재 조사 포인트", f"{st.session_state.points} P")

    with top2:
        if st.button("⬅ 메인 화면으로 돌아가기", use_container_width=True):
            clear_transient_states()
            refresh_image_click_component()
            st.session_state.current_view = None
            st.rerun(scope="fragment")

    st.info("조사할 지점을 선택하세요. 사진 속 물건을 직접 눌러보세요.")

    st.divider()

    try:
        display_image = fast_room_image(CRIME_SCENE_IMAGE_PATH, st.session_state.debug_mode, draw_debug_overlay)
    except FileNotFoundError:
        render_no_image_clue_menu('사건 현장 - 과방')
        return


    value = streamlit_image_coordinates(
        display_image,
        key=f"crime_scene_image_{st.session_state.image_click_nonce}",
        use_column_width="always",
    )

    if value is not None:
        click_xy = (value["x"], value["y"])

        if click_xy != st.session_state.last_click_xy:
            st.session_state.last_click_xy = click_xy

            rendered_width = value["width"]
            rendered_height = value["height"]

            x_ratio = value["x"] / rendered_width
            y_ratio = value["y"] / rendered_height

            st.session_state.last_click_ratio = (
                round(x_ratio, 3),
                round(y_ratio, 3),
            )

            hotspot_id = find_hotspot(x_ratio, y_ratio)

            if hotspot_id is not None:
                # 새 hotspot을 누르는 순간 이전 단서 확인 상태는 반드시 제거
                st.session_state.pending_clue_id = None
                st.session_state.selected_hotspot_id = None

                clue_ids = CRIME_SCENE_HOTSPOTS[hotspot_id]["clue_ids"]

                if len(clue_ids) == 1:
                    clue_id = clue_ids[0]
                    if clue_id in st.session_state.investigated_clues:
                        refresh_image_click_component()
                        st.session_state.last_revealed_clue_id = clue_id
                    else:
                        st.session_state.pending_clue_id = clue_id
                else:
                    st.session_state.selected_hotspot_id = hotspot_id

                # Image clicks already cause a Streamlit script rerun.
                # Show a new clue menu/confirmation in this pass without forcing a second rerun.
                if st.session_state.last_revealed_clue_id is not None:
                    st.rerun(scope="fragment")

    if st.session_state.debug_mode and st.session_state.last_click_ratio:
        rx, ry = st.session_state.last_click_ratio
        st.caption(f"🧭 방금 클릭한 비율 좌표 → x={rx}, y={ry}")

    # 다중 단서 hotspot도 사진을 유지한 채 아래에 표시
    if st.session_state.selected_hotspot_id is not None:
        render_hotspot_menu(st.session_state.selected_hotspot_id)

    # 확인창은 항상 한 곳에서만 렌더링
    if st.session_state.pending_clue_id is not None:
        render_confirm_box(st.session_state.pending_clue_id)

    if st.session_state.debug_mode:
        render_debug_button_list()


# ─────────────────────────────────────
# 이지안의 방
# ─────────────────────────────────────
def render_jian_room():
    if st.session_state.last_revealed_clue_id is not None:
        render_clue_reveal_screen(st.session_state.last_revealed_clue_id)
        return

    st.title("📍 이지안의 방")

    top1, top2 = st.columns(2)

    with top1:
        st.metric("현재 조사 포인트", f"{st.session_state.points} P")

    with top2:
        if st.button("⬅ 메인 화면으로 돌아가기", use_container_width=True):
            clear_transient_states()
            refresh_image_click_component()
            st.session_state.current_view = None
            st.rerun(scope="fragment")

    st.info("방 안에서 조사하고 싶은 물건을 직접 눌러보세요.")

    try:
        display_image = fast_room_image(JIAN_ROOM_IMAGE_PATH, st.session_state.debug_mode, draw_jian_debug_overlay)
    except FileNotFoundError:
        render_no_image_clue_menu('이지안의 방')
        return


    value = streamlit_image_coordinates(
        display_image,
        key=f"jian_room_image_{st.session_state.image_click_nonce}",
        use_column_width="always",
    )

    if value is not None:
        click_xy = (value["x"], value["y"])

        if click_xy != st.session_state.last_click_xy:
            st.session_state.last_click_xy = click_xy

            rendered_width = value["width"]
            rendered_height = value["height"]

            x_ratio = value["x"] / rendered_width
            y_ratio = value["y"] / rendered_height

            st.session_state.last_click_ratio = (
                round(x_ratio, 3),
                round(y_ratio, 3),
            )

            hotspot_id = find_jian_hotspot(x_ratio, y_ratio)

            if hotspot_id is not None:
                # 다른 물건의 pending/menu 상태가 남지 않게 먼저 완전 초기화
                st.session_state.pending_clue_id = None
                st.session_state.selected_hotspot_id = None

                clue_ids = JIAN_ROOM_HOTSPOTS[hotspot_id]["clue_ids"]

                if len(clue_ids) == 1:
                    clue_id = clue_ids[0]
                    if clue_id in st.session_state.investigated_clues:
                        refresh_image_click_component()
                        st.session_state.last_revealed_clue_id = clue_id
                    else:
                        st.session_state.pending_clue_id = clue_id
                else:
                    st.session_state.selected_hotspot_id = hotspot_id

                # Image clicks already cause a Streamlit script rerun.
                # Show a new clue menu/confirmation in this pass without forcing a second rerun.
                if st.session_state.last_revealed_clue_id is not None:
                    st.rerun(scope="fragment")

    if st.session_state.debug_mode and st.session_state.last_click_ratio:
        rx, ry = st.session_state.last_click_ratio
        st.caption(f"🧭 방금 클릭한 비율 좌표 → x={rx}, y={ry}")

    if st.session_state.selected_hotspot_id is not None:
        render_room_hotspot_menu(
            JIAN_ROOM_HOTSPOTS,
            st.session_state.selected_hotspot_id,
            "이지안의 방",
        )

    if st.session_state.pending_clue_id is not None:
        render_confirm_box(st.session_state.pending_clue_id)

    if st.session_state.debug_mode:
        st.divider()
        st.caption("🛠 이지안의 방 hotspot 테스트")
        cols = st.columns(3)

        for i, (hotspot_id, hotspot) in enumerate(JIAN_ROOM_HOTSPOTS.items()):
            with cols[i % 3]:
                if st.button(
                    hotspot["name"],
                    key=f"jian_debug_{hotspot_id}",
                    use_container_width=True,
                ):
                    st.session_state.pending_clue_id = None
                    st.session_state.selected_hotspot_id = None

                    clue_id = hotspot["clue_ids"][0]
                    if clue_id in st.session_state.investigated_clues:
                        refresh_image_click_component()
                        st.session_state.last_revealed_clue_id = clue_id
                    else:
                        st.session_state.pending_clue_id = clue_id

                    st.rerun(scope="fragment")


# ─────────────────────────────────────
# 전혜준의 방
# ─────────────────────────────────────
def render_hyejun_room():
    if st.session_state.last_revealed_clue_id is not None:
        render_clue_reveal_screen(st.session_state.last_revealed_clue_id)
        return

    st.title("📍 전혜준의 방")
    top1, top2 = st.columns(2)
    with top1:
        st.metric("현재 조사 포인트", f"{st.session_state.points} P")
    with top2:
        if st.button("⬅ 메인 화면으로 돌아가기", key="hyejun_back", use_container_width=True):
            clear_transient_states()
            refresh_image_click_component()
            st.session_state.current_view = None
            st.rerun(scope="fragment")

    st.info("방 안에서 조사하고 싶은 물건을 직접 눌러보세요.")

    try:
        display_image = fast_room_image(HYEJUN_ROOM_IMAGE_PATH, st.session_state.debug_mode, draw_hyejun_debug_overlay)
    except FileNotFoundError:
        render_no_image_clue_menu('전혜준의 방')
        return

    value = streamlit_image_coordinates(
        display_image,
        key=f"hyejun_room_image_{st.session_state.image_click_nonce}",
        use_column_width="always",
    )

    if value is not None:
        click_xy = (value["x"], value["y"])
        if click_xy != st.session_state.last_click_xy:
            st.session_state.last_click_xy = click_xy
            x_ratio = value["x"] / value["width"]
            y_ratio = value["y"] / value["height"]
            st.session_state.last_click_ratio = (round(x_ratio, 3), round(y_ratio, 3))
            hotspot_id = find_hyejun_hotspot(x_ratio, y_ratio)

            if hotspot_id is not None:
                st.session_state.pending_clue_id = None
                st.session_state.selected_hotspot_id = None
                clue_ids = HYEJUN_ROOM_HOTSPOTS[hotspot_id]["clue_ids"]
                if len(clue_ids) == 1:
                    clue_id = clue_ids[0]
                    if clue_id in st.session_state.investigated_clues:
                        refresh_image_click_component()
                        st.session_state.last_revealed_clue_id = clue_id
                    else:
                        st.session_state.pending_clue_id = clue_id
                else:
                    st.session_state.selected_hotspot_id = hotspot_id
                # Image clicks already cause a Streamlit script rerun.
                # Show a new clue menu/confirmation in this pass without forcing a second rerun.
                if st.session_state.last_revealed_clue_id is not None:
                    st.rerun(scope="fragment")

    if st.session_state.debug_mode and st.session_state.last_click_ratio:
        rx, ry = st.session_state.last_click_ratio
        st.caption(f"🧭 방금 클릭한 비율 좌표 → x={rx}, y={ry}")

    if st.session_state.selected_hotspot_id is not None:
        render_room_hotspot_menu(HYEJUN_ROOM_HOTSPOTS, st.session_state.selected_hotspot_id, "전혜준의 방")

    if st.session_state.pending_clue_id is not None:
        render_confirm_box(st.session_state.pending_clue_id)

    if st.session_state.debug_mode:
        st.divider()
        st.caption("🛠 전혜준의 방 hotspot 테스트")
        cols = st.columns(4)
        for i, (hotspot_id, hotspot) in enumerate(HYEJUN_ROOM_HOTSPOTS.items()):
            with cols[i % 4]:
                if st.button(hotspot["name"], key=f"hyejun_debug_{hotspot_id}", use_container_width=True):
                    st.session_state.pending_clue_id = None
                    st.session_state.selected_hotspot_id = None
                    clue_ids = hotspot["clue_ids"]
                    if len(clue_ids) == 1:
                        clue_id = clue_ids[0]
                        if clue_id in st.session_state.investigated_clues:
                            refresh_image_click_component()
                            st.session_state.last_revealed_clue_id = clue_id
                        else:
                            st.session_state.pending_clue_id = clue_id
                    else:
                        st.session_state.selected_hotspot_id = hotspot_id
                    st.rerun(scope="fragment")


# ─────────────────────────────────────
# 변상균 교수 연구실
# ─────────────────────────────────────
def render_prof_room():
    if st.session_state.last_revealed_clue_id is not None:
        render_clue_reveal_screen(st.session_state.last_revealed_clue_id)
        return

    st.title("📍 변상균 교수 연구실")

    top1, top2 = st.columns(2)
    with top1:
        st.metric("현재 조사 포인트", f"{st.session_state.points} P")

    with top2:
        if st.button("⬅ 메인 화면으로 돌아가기", key="prof_back", use_container_width=True):
            clear_transient_states()
            refresh_image_click_component()
            st.session_state.current_view = None
            st.rerun(scope="fragment")

    st.info("연구실 안에서 조사하고 싶은 물건을 직접 눌러보세요.")

    try:
        display_image = fast_room_image(PROF_ROOM_IMAGE_PATH, st.session_state.debug_mode, draw_prof_debug_overlay)
    except FileNotFoundError:
        render_no_image_clue_menu('변상균 교수 연구실')
        return


    value = streamlit_image_coordinates(
        display_image,
        key=f"prof_room_image_{st.session_state.image_click_nonce}",
        use_column_width="always",
    )

    if value is not None:
        click_xy = (value["x"], value["y"])

        if click_xy != st.session_state.last_click_xy:
            st.session_state.last_click_xy = click_xy

            x_ratio = value["x"] / value["width"]
            y_ratio = value["y"] / value["height"]

            st.session_state.last_click_ratio = (
                round(x_ratio, 3),
                round(y_ratio, 3),
            )

            hotspot_id = find_prof_hotspot(x_ratio, y_ratio)

            if hotspot_id is not None:
                st.session_state.pending_clue_id = None
                st.session_state.selected_hotspot_id = None

                clue_ids = PROF_ROOM_HOTSPOTS[hotspot_id]["clue_ids"]

                if len(clue_ids) == 1:
                    clue_id = clue_ids[0]

                    if clue_id in st.session_state.investigated_clues:
                        refresh_image_click_component()
                        st.session_state.last_revealed_clue_id = clue_id
                    else:
                        st.session_state.pending_clue_id = clue_id
                else:
                    st.session_state.selected_hotspot_id = hotspot_id

                # Image clicks already cause a Streamlit script rerun.
                # Show a new clue menu/confirmation in this pass without forcing a second rerun.
                if st.session_state.last_revealed_clue_id is not None:
                    st.rerun(scope="fragment")

    if st.session_state.debug_mode and st.session_state.last_click_ratio:
        rx, ry = st.session_state.last_click_ratio
        st.caption(f"🧭 방금 클릭한 비율 좌표 → x={rx}, y={ry}")

    if st.session_state.selected_hotspot_id is not None:
        render_room_hotspot_menu(
            PROF_ROOM_HOTSPOTS,
            st.session_state.selected_hotspot_id,
            "변상균 교수 연구실",
        )

    if st.session_state.pending_clue_id is not None:
        render_confirm_box(st.session_state.pending_clue_id)

    if st.session_state.debug_mode:
        st.divider()
        st.caption("🛠 변상균 교수 연구실 hotspot 테스트")

        cols = st.columns(5)

        for i, (hotspot_id, hotspot) in enumerate(PROF_ROOM_HOTSPOTS.items()):
            with cols[i % 5]:
                if st.button(
                    hotspot["name"],
                    key=f"prof_debug_{hotspot_id}",
                    use_container_width=True,
                ):
                    st.session_state.pending_clue_id = None
                    st.session_state.selected_hotspot_id = None

                    clue_ids = hotspot["clue_ids"]

                    if len(clue_ids) == 1:
                        clue_id = clue_ids[0]

                        if clue_id in st.session_state.investigated_clues:
                            refresh_image_click_component()
                            st.session_state.last_revealed_clue_id = clue_id
                        else:
                            st.session_state.pending_clue_id = clue_id
                    else:
                        st.session_state.selected_hotspot_id = hotspot_id

                    st.rerun(scope="fragment")



# ─────────────────────────────────────
# 박진서의 방
# ─────────────────────────────────────
def render_jinseo_room():
    if st.session_state.last_revealed_clue_id is not None:
        render_clue_reveal_screen(st.session_state.last_revealed_clue_id)
        return

    st.title("📍 박진서의 방")

    top1, top2 = st.columns(2)
    with top1:
        st.metric("현재 조사 포인트", f"{st.session_state.points} P")

    with top2:
        if st.button("⬅ 메인 화면으로 돌아가기", key="jinseo_back", use_container_width=True):
            clear_transient_states()
            refresh_image_click_component()
            st.session_state.current_view = None
            st.rerun(scope="fragment")

    st.info("방 안에서 조사하고 싶은 물건을 직접 눌러보세요.")

    try:
        display_image = fast_room_image(JINSEO_ROOM_IMAGE_PATH, st.session_state.debug_mode, draw_jinseo_debug_overlay)
    except FileNotFoundError:
        render_no_image_clue_menu('박진서의 방')
        return


    value = streamlit_image_coordinates(
        display_image,
        key=f"jinseo_room_image_{st.session_state.image_click_nonce}",
        use_column_width="always",
    )

    if value is not None:
        click_xy = (value["x"], value["y"])

        if click_xy != st.session_state.last_click_xy:
            st.session_state.last_click_xy = click_xy

            x_ratio = value["x"] / value["width"]
            y_ratio = value["y"] / value["height"]

            st.session_state.last_click_ratio = (
                round(x_ratio, 3),
                round(y_ratio, 3),
            )

            hotspot_id = find_jinseo_hotspot(x_ratio, y_ratio)

            if hotspot_id is not None:
                st.session_state.pending_clue_id = None
                st.session_state.selected_hotspot_id = None

                clue_ids = JINSEO_ROOM_HOTSPOTS[hotspot_id]["clue_ids"]

                if len(clue_ids) == 1:
                    clue_id = clue_ids[0]

                    if clue_id in st.session_state.investigated_clues:
                        refresh_image_click_component()
                        st.session_state.last_revealed_clue_id = clue_id
                    else:
                        st.session_state.pending_clue_id = clue_id
                else:
                    st.session_state.selected_hotspot_id = hotspot_id

                # Image clicks already cause a Streamlit script rerun.
                # Show a new clue menu/confirmation in this pass without forcing a second rerun.
                if st.session_state.last_revealed_clue_id is not None:
                    st.rerun(scope="fragment")

    if st.session_state.debug_mode and st.session_state.last_click_ratio:
        rx, ry = st.session_state.last_click_ratio
        st.caption(f"🧭 방금 클릭한 비율 좌표 → x={rx}, y={ry}")

    if st.session_state.selected_hotspot_id is not None:
        render_room_hotspot_menu(
            JINSEO_ROOM_HOTSPOTS,
            st.session_state.selected_hotspot_id,
            "박진서의 방",
        )

    if st.session_state.pending_clue_id is not None:
        render_confirm_box(st.session_state.pending_clue_id)

    if st.session_state.debug_mode:
        st.divider()
        st.caption("🛠 박진서의 방 hotspot 테스트")

        cols = st.columns(5)

        for i, (hotspot_id, hotspot) in enumerate(JINSEO_ROOM_HOTSPOTS.items()):
            with cols[i % 5]:
                if st.button(
                    hotspot["name"],
                    key=f"jinseo_debug_{hotspot_id}",
                    use_container_width=True,
                ):
                    st.session_state.pending_clue_id = None
                    st.session_state.selected_hotspot_id = None

                    clue_ids = hotspot["clue_ids"]

                    if len(clue_ids) == 1:
                        clue_id = clue_ids[0]

                        if clue_id in st.session_state.investigated_clues:
                            refresh_image_click_component()
                            st.session_state.last_revealed_clue_id = clue_id
                        else:
                            st.session_state.pending_clue_id = clue_id
                    else:
                        st.session_state.selected_hotspot_id = hotspot_id

                    st.rerun(scope="fragment")



# ─────────────────────────────────────
# 고건태의 방
# ─────────────────────────────────────
def render_geontae_room():
    if st.session_state.last_revealed_clue_id is not None:
        render_clue_reveal_screen(st.session_state.last_revealed_clue_id)
        return

    st.title("📍 고건태의 방")

    top1, top2 = st.columns(2)
    with top1:
        st.metric("현재 조사 포인트", f"{st.session_state.points} P")

    with top2:
        if st.button("⬅ 메인 화면으로 돌아가기", key="geontae_back", use_container_width=True):
            clear_transient_states()
            refresh_image_click_component()
            st.session_state.current_view = None
            st.rerun(scope="fragment")

    st.info("방 안에서 조사하고 싶은 물건을 직접 눌러보세요.")

    if st.session_state.stage == 3:
        st.success("3차 자유 조사: 이전 조사에서 확인하지 못한 장소와 자료를 자유롭게 다시 조사할 수 있습니다.")

    try:
        display_image = fast_room_image(GEONTAE_ROOM_IMAGE_PATH, st.session_state.debug_mode, draw_geontae_debug_overlay)
    except FileNotFoundError:
        render_no_image_clue_menu('고건태의 방')
        return


    value = streamlit_image_coordinates(
        display_image,
        key=f"geontae_room_image_{st.session_state.image_click_nonce}",
        use_column_width="always",
    )

    if value is not None:
        click_xy = (value["x"], value["y"])

        if click_xy != st.session_state.last_click_xy:
            st.session_state.last_click_xy = click_xy

            x_ratio = value["x"] / value["width"]
            y_ratio = value["y"] / value["height"]

            st.session_state.last_click_ratio = (
                round(x_ratio, 3),
                round(y_ratio, 3),
            )

            hotspot_id = find_geontae_hotspot(x_ratio, y_ratio)

            if hotspot_id is not None:
                st.session_state.pending_clue_id = None
                st.session_state.selected_hotspot_id = None

                hotspot = GEONTAE_ROOM_HOTSPOTS[hotspot_id]
                clue_ids = available_clue_ids(hotspot)

                if not clue_ids:
                    st.session_state.selected_hotspot_id = None
                    st.session_state.pending_clue_id = None
                elif len(clue_ids) == 1:
                    clue_id = clue_ids[0]

                    if clue_id in st.session_state.investigated_clues:
                        refresh_image_click_component()
                        st.session_state.last_revealed_clue_id = clue_id
                    else:
                        st.session_state.pending_clue_id = clue_id
                else:
                    st.session_state.selected_hotspot_id = hotspot_id

                # Image clicks already cause a Streamlit script rerun.
                # Show a new clue menu/confirmation in this pass without forcing a second rerun.
                if st.session_state.last_revealed_clue_id is not None:
                    st.rerun(scope="fragment")

    if st.session_state.debug_mode and st.session_state.last_click_ratio:
        rx, ry = st.session_state.last_click_ratio
        st.caption(f"🧭 방금 클릭한 비율 좌표 → x={rx}, y={ry}")

    if st.session_state.selected_hotspot_id is not None:
        render_room_hotspot_menu(
            GEONTAE_ROOM_HOTSPOTS,
            st.session_state.selected_hotspot_id,
            "고건태의 방",
        )

    if st.session_state.pending_clue_id is not None:
        render_confirm_box(st.session_state.pending_clue_id)

    if st.session_state.debug_mode:
        st.divider()
        st.caption("🛠 고건태의 방 hotspot 테스트")

        cols = st.columns(5)

        for i, (hotspot_id, hotspot) in enumerate(GEONTAE_ROOM_HOTSPOTS.items()):
            with cols[i % 5]:
                if st.button(
                    hotspot["name"],
                    key=f"geontae_debug_{hotspot_id}",
                    use_container_width=True,
                ):
                    st.session_state.pending_clue_id = None
                    st.session_state.selected_hotspot_id = None

                    clue_ids = available_clue_ids(hotspot)

                    if not clue_ids:
                        st.session_state.selected_hotspot_id = None
                        st.session_state.pending_clue_id = None
                    elif len(clue_ids) == 1:
                        clue_id = clue_ids[0]

                        if clue_id in st.session_state.investigated_clues:
                            refresh_image_click_component()
                            st.session_state.last_revealed_clue_id = clue_id
                        else:
                            st.session_state.pending_clue_id = clue_id
                    else:
                        st.session_state.selected_hotspot_id = hotspot_id

                    st.rerun(scope="fragment")


# ─────────────────────────────────────
# 확보한 단서
# ─────────────────────────────────────
def render_clue_list():
    st.markdown('<div class="game-section">▌ EVIDENCE ARCHIVE / 증거 보관함</div>',unsafe_allow_html=True)
    st.caption("조사 중 확보한 증거를 장소별로 다시 확인할 수 있습니다. 재열람은 무료입니다.")
    groups = ["사건 현장 - 과방", "이지안", "전혜준", "변상균 교수", "박진서", "고건태"]
    labels = ["과방", "이지안의 방", "전혜준의 방", "변상균 교수 연구실", "박진서의 방", "고건태의 방"]
    acquired = [cid for cid in CLUES if cid in st.session_state.investigated_clues]
    tabs = st.tabs([f"{label} ({sum(1 for cid in acquired if (CLUES[cid]['location'] == group or (group != '사건 현장 - 과방' and group in CLUES[cid]['location'])) )})" for label, group in zip(labels, groups)])
    for tab, group in zip(tabs, groups):
        with tab:
            ids = [cid for cid in acquired if CLUES[cid]['location'] == group or (group != "사건 현장 - 과방" and group in CLUES[cid]['location'])]
            if not ids:
                st.info("아직 확보한 증거가 없습니다.")
            for cid in ids:
                clue = CLUES[cid]
                if st.button(f"📄 {clue['name']} · 열람", key=f"archive_view_{cid}", use_container_width=True):
                    st.session_state.archive_open_key = None if st.session_state.get("archive_open_key") == cid else cid
                if st.session_state.get("archive_open_key") == cid:
                    if clue.get("image") and os.path.isfile(clue["image"]):
                        show_optional_image(clue["image"])
                    else:
                        st.warning("단서 이미지를 찾을 수 없습니다.")
                    for line in clue.get("result", []):
                        st.write(line)
    if st.button("↶ 이전 화면으로 돌아가기", key="archive_return", use_container_width=True):
        clear_transient_states()
        st.session_state.current_view = st.session_state.evidence_return_view
        st.session_state.evidence_return_view = None
        refresh_image_click_component()
        st.rerun()


# ─────────────────────────────────────
# 최종 추리 제출
# ─────────────────────────────────────
def render_final_submission():
    st.title("📝 최종 추리 제출")
    st.caption(f"{st.session_state.team_no}조 · 객관식 3문항 + 서술형 1문항")
    labels = {"culprit":"범인", "weapon":"범행도구", "time":"범행 추정 시각", "reason":"범행 동기 및 추리 근거"}
    if st.session_state.final_submitted:
        if REMOTE_STORAGE:
            st.success("최종 추리가 공유 저장소에 제출되었습니다. 제출 후에는 수정할 수 없습니다.")
        else:
            st.warning("최종 답안이 현재 서버에 임시 저장되었습니다. 공유 저장소가 연결되지 않아 다른 서버의 관리자 화면에서 확인되지 않을 수 있습니다. 관리자에게 제출 여부를 확인해주세요.")
        for key,label in labels.items():
            with st.container(border=True):
                st.write(f"**{label}**")
                st.write(st.session_state.final_answers.get(key, ""))
        if st.button("⬅ 메인 화면으로 돌아가기", use_container_width=True):
            clear_transient_states()
            st.session_state.current_view = None
            st.rerun(scope="fragment")
        return
    if not st.session_state.final_submission_open or st.session_state.stage < 3:
        st.warning("아직 최종 추리 제출 시간이 아닙니다.")
        if st.button("⬅ 메인 화면으로 돌아가기", use_container_width=True):
            st.session_state.current_view = None
            st.rerun(scope="fragment")
        return
    st.info("범인, 범행도구, 추정 시각을 선택하고 확보한 증거를 근거로 설명하세요. 제출 후 수정할 수 없습니다.")
    with st.form("final_submission_form"):
        culprit = st.radio("1. 범인은 누구인가?", ["선택해주세요", "이지안", "전혜준", "변상균 교수", "박진서", "고건태"])
        weapon = st.radio("2. 실제 범행도구는 무엇인가?", ["선택해주세요", "소화기", "야구방망이", "몽키스패너", "칼"])
        time = st.radio("3. 범행 추정 시각은 언제인가?", ["선택해주세요", "14:30경", "16:30경", "17:20경", "18:25경"])
        reason = st.text_area("4. 범행 동기와 가장 중요한 증거 2개 이상을 연결해 설명하세요.", height=180)
        submitted = st.form_submit_button("최종 추리 제출", type="primary", use_container_width=True)
    if submitted:
        if "선택해주세요" in (culprit,weapon,time) or not reason.strip():
            st.error("모든 문항에 답한 뒤 제출해주세요.")
        else:
            st.session_state.final_answers = {"culprit":culprit, "weapon":weapon, "time":time, "reason":reason.strip()}
            st.session_state.final_submitted = True
            save_progress()
            # Verify persistence on the same storage used by the administrator.
            try:
                persisted = load_team_data(st.session_state.team_no)
                if not persisted.get("final_submitted") or persisted.get("final_answers", {}).get("reason") != reason.strip():
                    st.error("답안 저장 확인에 실패했습니다. 관리자에게 문의하고 다시 확인해주세요.")
                    return
            except Exception as exc:
                st.error(f"답안 저장 여부를 확인하지 못했습니다: {exc}")
                return
            st.rerun(scope="fragment")
    if st.button("⬅ 메인 화면으로 돌아가기", use_container_width=True):
        clear_transient_states()
        st.session_state.current_view = None
        st.rerun(scope="fragment")


def render_interrogation():
    """3차 조사 전용. 질문별 20P, 누적 최대 5개, 동일 질문 재열람 무료."""
    if st.session_state.stage < 3:
        st.warning("용의자 심문은 3차 조사에서만 가능합니다.")
        return
    st.title("🗣️ 용의자 심문")
    count = len(st.session_state.interrogated_questions)
    c1,c2,c3 = st.columns(3)
    c1.metric("남은 심문", f"{MAX_INTERROGATIONS-count} / {MAX_INTERROGATIONS}")
    c2.metric("질문당 비용", f"{INTERROGATION_COST} P")
    c3.metric("현재 포인트", f"{st.session_state.points} P")
    st.caption("팀당 최대 5개의 질문을 구매할 수 있습니다. 구매한 질문은 무료로 다시 볼 수 있습니다.")
    suspect = st.selectbox("심문 대상", ["이지안", "전혜준", "변상균 교수", "박진서", "고건태"])
    options=[(key,info) for key,info in INTERROGATIONS.items() if info["suspect"]==suspect]
    for key,info in options:
        acquired = key in st.session_state.interrogated_questions
        with st.container(border=True):
            st.markdown(f"**Q{info['number']}. {info['question']}**")
            if acquired:
                st.success("심문 완료 · 무료 재열람")
                st.write(info["answer"])
            else:
                can_buy=(count<MAX_INTERROGATIONS and st.session_state.points>=INTERROGATION_COST)
                if not can_buy:
                    st.caption("심문 횟수를 모두 사용했거나 포인트가 부족합니다.")
                if st.button(f"Q{info['number']} 심문하기 · {INTERROGATION_COST}P", key=f"buy_interview_{key}", disabled=not can_buy, use_container_width=True):
                    # 상태를 재검사하여 반복 구매 및 초과 구매 방지
                    if key not in st.session_state.interrogated_questions and len(st.session_state.interrogated_questions)<MAX_INTERROGATIONS and st.session_state.points>=INTERROGATION_COST:
                        st.session_state.points -= INTERROGATION_COST
                        st.session_state.interrogated_questions.add(key)
                        save_progress()
                    st.rerun(scope="fragment")
    st.divider()
    with st.expander("구매한 심문 다시 보기"):
        acquired_keys=[k for k in INTERROGATIONS if k in st.session_state.interrogated_questions]
        if not acquired_keys:
            st.info("아직 구매한 심문이 없습니다.")
        for k in acquired_keys:
            info=INTERROGATIONS[k]
            st.markdown(f"**{info['suspect']} Q{info['number']}. {info['question']}**")
            st.write(info["answer"])
    if st.button("⬅ 메인 화면으로 돌아가기", key="interview_back",use_container_width=True):
        st.session_state.current_view=None
        st.rerun(scope="fragment")


# ─────────────────────────────────────
# 장소 라우팅
# ─────────────────────────────────────
@st.fragment
def render_main_workspace():
    if st.session_state.current_view is not None:
        if st.session_state.current_view == "사건 현장":
            render_crime_scene()
            st.stop()

        if st.session_state.current_view == "확보한 단서":
            render_clue_list()
            st.stop()

        if st.session_state.current_view == "최종 추리 제출":
            render_final_submission()
            st.stop()

        if st.session_state.current_view == "용의자 심문":
            render_interrogation()
            st.stop()

        if st.session_state.current_view == "이지안":
            render_jian_room()
            st.stop()

        if st.session_state.current_view == "전혜준":
            render_hyejun_room()
            st.stop()

        if st.session_state.current_view == "변상균 교수":
            render_prof_room()
            st.stop()

        if st.session_state.current_view == "박진서":
            render_jinseo_room()
            st.stop()

        if st.session_state.current_view == "고건태":
            render_geontae_room()
            st.stop()

        location_key = st.session_state.current_view
        location_name = LOCATIONS[location_key]

        st.title(f"📍 {location_name}")
        st.info("현재는 용의자 공간 내부 조사 기능을 준비 중입니다.")

        if st.button("⬅ 메인 화면으로 돌아가기"):
            clear_transient_states()
            st.session_state.current_view = None
            st.rerun(scope="fragment")

        st.stop()


    # ─────────────────────────────────────
    # 메인 화면 · 사건 파일 선택
    # ─────────────────────────────────────
    st.markdown("""<div class="game-hero">
    <div class="game-eyebrow">YONSEI UNIVERSITY · INVESTIGATION FILE 001</div>
    <div class="game-title">학생회장<br>살인사건</div>
    <div class="game-sub">모든 증거는 현장에 남아 있다.</div>
    <div class="game-status">● UNSOLVED / 수사 진행 중</div>
    </div>""",unsafe_allow_html=True)

    m1,m2,m3=st.columns(3)
    with m1: st.metric("INVESTIGATION TEAM",f"{st.session_state.team_no}팀")
    with m2: st.metric("REMAINING POINTS",f"{st.session_state.points} P")
    with m3: st.metric("INVESTIGATION PHASE",f"{st.session_state.stage:02d} / 03")

    st.markdown('<div class="game-section">▌ 조사 구역 선택 &nbsp; / &nbsp; SELECT LOCATION</div>',unsafe_allow_html=True)
    st.markdown('<div class="game-caption">잠금 해제된 장소를 선택해 사건을 조사하십시오.</div>',unsafe_allow_html=True)
    location_keys=list(LOCATIONS.keys())
    cols=st.columns(3)
    for i,key in enumerate(location_keys):
        unlocked=is_unlocked(key)
        with cols[i%3]:
            label=("◈ " if unlocked else "🔒 ")+LOCATIONS[key]+("" if unlocked else " · LOCKED")
            if st.button(label,key=f"location_{key}",disabled=not unlocked,use_container_width=True):
                clear_transient_states()
                refresh_image_click_component()
                st.session_state.current_view=key
                st.rerun(scope="fragment")

    if st.session_state.stage >= 3:
        st.markdown('<div class="game-section">▌ 용의자 심문 &nbsp; / &nbsp; INTERROGATION</div>',unsafe_allow_html=True)
        if st.button(f"🗣 용의자 심문 · 남은 {MAX_INTERROGATIONS - len(st.session_state.interrogated_questions)}회 / {MAX_INTERROGATIONS}", key="home_interview", use_container_width=True):
            clear_transient_states()
            st.session_state.current_view = "용의자 심문"
            st.rerun(scope="fragment")

    st.markdown('<div class="game-section">▌ 수사 기록 &nbsp; / &nbsp; CASE ARCHIVE</div>',unsafe_allow_html=True)
    c1,c2=st.columns(2)
    with c1:
        if st.button("▣ 확보한 증거 열람",key="home_archive",use_container_width=True):
            clear_transient_states()
            refresh_image_click_component()
            st.session_state.current_view="확보한 단서"
            st.rerun(scope="fragment")
    with c2:
        if st.session_state.final_submission_open or st.session_state.final_submitted:
            if st.button("✎ 최종 추리 제출",key="home_final",use_container_width=True,type="primary"):
                clear_transient_states()
                st.session_state.current_view="최종 추리 제출"
                st.rerun(scope="fragment")
        else:
            st.button("🔒 최종 추리 · LOCKED",key="home_final_locked",disabled=True,use_container_width=True)


render_main_workspace()
