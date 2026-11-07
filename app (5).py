import os
import json
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
</style>""",unsafe_allow_html=True)

def config_value(key, default=""):
    try:
        return st.secrets.get(key, os.environ.get(key, default))
    except Exception:
        return os.environ.get(key, default)

ADMIN_PASSWORD = "mt1234"  # MT 진행자용 고정 관리자 비밀번호
INITIAL_POINTS = 100
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
CURRENT_SCHEMA = 2
INTERROGATION_COST = 20
MAX_INTERROGATIONS = 4

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
    if not isinstance(data, dict) or data.get("schema_version") != CURRENT_SCHEMA:
        return default_team_data()
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
CRIME_SCENE_HOTSPOTS = {
    # 좌표는 최종 과방 이미지(images/crime_scene.png)의 전체 너비/높이 대비 비율.
    # 박스별 위치가 겹칠 때는 면적이 작은 박스(손목시계 등)를 우선 인식합니다.
    'extinguisher': {
        "name": '소화기', "x": 0.715, "y": 0.165, "width": 0.043, "height": 0.09,
        "clue_ids": ['scene_extinguisher'],
    },
    'bat': {
        "name": '야구방망이', "x": 0.548, "y": 0.131, "width": 0.026, "height": 0.146,
        "clue_ids": ['scene_bat'],
    },
    'wrench': {
        "name": '몽키스패너', "x": 0.123, "y": 0.623, "width": 0.066, "height": 0.071,
        "clue_ids": ['scene_wrench'],
    },
    'body': {
        "name": '구성민의 시신', "x": 0.541, "y": 0.458, "width": 0.183, "height": 0.304,
        "clue_ids": ['scene_tod', 'scene_wound1', 'scene_wound2'],
    },
    'floor': {
        "name": '시신 옆 붉은 조각', "x": 0.763, "y": 0.737, "width": 0.061, "height": 0.057,
        "clue_ids": ['scene_red_paint'],
    },
    'watch': {
        "name": '구성민의 손목시계', "x": 0.675, "y": 0.520, "width": 0.027, "height": 0.048,
        "clue_ids": ['scene_watch'],
    },
    'cctv': {
        "name": '캐비닛 위 CCTV와 상자', "x": 0.878, "y": 0.005, "width": 0.069, "height": 0.118,
        "clue_ids": ['scene_cctv'],
    },
    'drink': {
        "name": '원형 탁자의 박카스', "x": 0.284, "y": 0.309, "width": 0.032, "height": 0.062,
        "clue_ids": ['scene_bacchus'],
    },
    'phone': {
        "name": '원형 탁자의 휴대전화', "x": 0.339, "y": 0.319, "width": 0.033, "height": 0.051,
        "clue_ids": ['scene_story'],
    },
    'cash': {
        "name": '소파의 운동가방', "x": 0.147, "y": 0.172, "width": 0.12, "height": 0.113,
        "clue_ids": ['scene_cash'],
    },
}

JIAN_ROOM_HOTSPOTS = {
    'id': {"name": '신분증', "x": 0.07597, "y": 0.1105, "width": 0.06077, "height": 0.06446, "clue_ids": ['jian_id']},
    'phone': {"name": '휴대전화', "x": 0.16298, "y": 0.37385, "width": 0.06699, "height": 0.08379, "clue_ids": ['jian_threat', 'jian_event']},
    'diary': {"name": '서랍 속 일기장', "x": 0.65401, "y": 0.32413, "width": 0.08494, "height": 0.09945, "clue_ids": ['jian_diary']},
    'medicine': {"name": '처방전', "x": 0.79627, "y": 0.5488, "width": 0.09669, "height": 0.11694, "clue_ids": ['jian_sleep', 'jian_estradiol']},
    'bankbook': {"name": '통장', "x": 0.81354, "y": 0.67219, "width": 0.08287, "height": 0.0709, "clue_ids": ['jian_cash']},
}
HYEJUN_ROOM_HOTSPOTS = {
    'letter': {"name": '편지', "x": 0.25552, "y": 0.31952, "width": 0.08356, "height": 0.06538, "clue_ids": ['hyejun_letter']},
    'bag': {"name": '백팩', "x": 0.37293, "y": 0.24862, "width": 0.10773, "height": 0.12891, "clue_ids": ['hyejun_knife']},
    'ring': {"name": '작은 상자', "x": 0.51865, "y": 0.44199, "width": 0.07251, "height": 0.07366, "clue_ids": ['hyejun_ring']},
    'laptop': {"name": '노트북', "x": 0.76657, "y": 0.407, "width": 0.14019, "height": 0.15009, "clue_ids": ['hyejun_chat']},
    'photo': {"name": '사진', "x": 0.75, "y": 0.56077, "width": 0.08425, "height": 0.08287, "clue_ids": ['hyejun_xphoto']},
    'handed': {"name": '소견서', "x": 0.72997, "y": 0.65101, "width": 0.1326, "height": 0.15193, "clue_ids": ['hyejun_left']},
    'phone': {"name": '휴대전화', "x": 0.86671, "y": 0.66483, "width": 0.07251, "height": 0.12339, "clue_ids": ['hyejun_dm', 'hyejun_contact']},
}
PROF_ROOM_HOTSPOTS = {
    'pc': {"name": '컴퓨터', "x": 0.5297, "y": 0.25414, "width": 0.3529, "height": 0.17956, "clue_ids": ['prof_cctv', 'prof_korea']},
    'golf': {"name": '액자', "x": 0.8011, "y": 0.08379, "width": 0.06906, "height": 0.08195, "clue_ids": ['prof_golf']},
    'news': {"name": '신문기사', "x": 0.30663, "y": 0.45764, "width": 0.14503, "height": 0.09116, "clue_ids": ['prof_award']},
    'research': {"name": '연구 일지', "x": 0.52279, "y": 0.49171, "width": 0.18025, "height": 0.11602, "clue_ids": ['prof_research']},
    'phone': {"name": '휴대전화', "x": 0.73066, "y": 0.51197, "width": 0.0739, "height": 0.0884, "clue_ids": ['prof_kakao']},
    'receipt': {"name": '영수증', "x": 0.7797, "y": 0.60313, "width": 0.07182, "height": 0.10129, "clue_ids": ['prof_receipt']},
}
JINSEO_ROOM_HOTSPOTS = {
    'checklist': {"name": '벽면 체크리스트', "x": 0.84669, "y": 0.10773, "width": 0.06699, "height": 0.13168, "clue_ids": ['jinseo_checklist']},
    'childdiary': {"name": '책장 속 오래된 일기장', "x": 0.24309, "y": 0.18785, "width": 0.05594, "height": 0.10037, "clue_ids": ['jinseo_childdiary']},
    'pc': {"name": '컴퓨터', "x": 0.1326, "y": 0.31308, "width": 0.12293, "height": 0.14917, "clue_ids": ['jinseo_search']},
    'phone': {"name": '휴대전화', "x": 0.29075, "y": 0.51197, "width": 0.06146, "height": 0.07827, "clue_ids": ['jinseo_bodyphoto', 'jinseo_calendar']},
    'diary': {"name": '9월 15일 일기장', "x": 0.1105, "y": 0.58287, "width": 0.19751, "height": 0.12063, "clue_ids": ['jinseo_diary']},
    'counseling': {"name": '상담 기록', "x": 0.08978, "y": 0.71363, "width": 0.17265, "height": 0.19797, "clue_ids": ['jinseo_child']},
}
GEONTAE_ROOM_HOTSPOTS = {
    'news': {"name": '신문기사', "x": 0.24862, "y": 0.72284, "width": 0.21478, "height": 0.13812, "clue_ids": ['geontae_news']},
    'phone': {"name": '휴대전화', "x": 0.11257, "y": 0.41252, "width": 0.06837, "height": 0.06722, "clue_ids": ['geontae_chat', 'geontae_findmy']},
    'keepsakes': {"name": '구석의 상자', "x": 0.39917, "y": 0.27164, "width": 0.09323, "height": 0.093, "clue_ids": ['geontae_keepsakes']},
    'petition': {"name": '책상 위 탄원서', "x": 0.64986, "y": 0.35912, "width": 0.13674, "height": 0.08564, "clue_ids": ['geontae_petition']},
    'backpack': {"name": '가방', "x": 0.6471, "y": 0.53499, "width": 0.13743, "height": 0.21823, "clue_ids": ['geontae_airpods']},
    'album': {"name": '책장의 앨범', "x": 0.84669, "y": 0.13444, "width": 0.11395, "height": 0.15562, "clue_ids": ['geontae_album']},
}
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


CLUES = {
    # 사건 현장 - 과방: 12개
    'scene_extinguisher': {
        'menu_name': '소화기',
        'name': '붉은 소화기',
        'cost': 10,
        'location': '사건 현장 - 과방',
        'source': '소화기',
        'result': ['깨끗한 붉은 소화기. 주변 물건보다 먼지가 적으며 표면에 붉은 금속용 도료가 칠해져 있다.'],
        "image": find_clue_image('과방 단서 이미지', 'fire_extinguisher_clean'),
    },
    'scene_bat': {
        'menu_name': '야구방망이',
        'name': '먼지가 쌓인 야구방망이',
        'cost': 10,
        'location': '사건 현장 - 과방',
        'source': '야구방망이',
        'result': ['손잡이까지 오래 쌓인 미세 먼지가 보인다. 최근 사용 여부는 다른 증거와 비교해야 한다.'],
        "image": find_clue_image('과방 단서 이미지', 'baseball_bat'),
    },
    'scene_wrench': {
        'menu_name': '몽키스패너',
        'name': '몽키스패너',
        'cost': 10,
        'location': '사건 현장 - 과방',
        'source': '몽키스패너',
        'result': ['손잡이가 바깥쪽을 향한 몽키스패너가 놓여 있다. 손잡이는 붉은 고무 재질이다.'],
        "image": find_clue_image('과방 단서 이미지', 'monkey_wrench'),
    },
    'scene_red_paint': {
        'menu_name': '붉은 조각',
        'name': '붉은 도료 조각',
        'cost': 10,
        'location': '사건 현장 - 과방',
        'source': '바닥',
        'result': ['시신 주변에서 떨어진 붉은색 조각. 금속 표면 보호용 코팅 계열로 분석된다.'],
        "image": find_clue_image('과방 단서 이미지', 'red_paint_analysis'),
    },
    'scene_wound1': {
        'menu_name': '상처 감식서 ①',
        'name': '상처 감식 결과 ①',
        'cost': 10,
        'location': '사건 현장 - 과방',
        'source': '구성민의 시신',
        'result': ['머리의 손상은 비교적 넓은 접촉면을 가진 둔기 충격에 부합한다. 정확한 무기는 추가 비교가 필요하다.'],
        "image": find_clue_image('과방 단서 이미지', 'wound_report_1'),
    },
    'scene_wound2': {
        'menu_name': '상처 감식서 ②',
        'name': '상처 감식 결과 ②',
        'cost': 10,
        'location': '사건 현장 - 과방',
        'source': '구성민의 시신',
        'result': ['머리 오른쪽 측면에 주요 손상이 있고 오른쪽 방향에서 가격했을 가능성이 있다. 상처만으로 공격자의 주사용 손을 특정할 수 없다.'],
        "image": find_clue_image('과방 단서 이미지', 'wound_report_2'),
    },
    'scene_tod': {
        'menu_name': '사망 시각 감정서',
        'name': '법의학적 사망 추정 시간',
        'cost': 10,
        'location': '사건 현장 - 과방',
        'source': '구성민의 시신',
        'result': ['사망 추정 시간 범위는 2026년 9월 15일 16:00~18:30이다.'],
        "image": find_clue_image('과방 단서 이미지', 'time_of_death_report'),
    },
    'scene_watch': {
        'menu_name': '손목시계',
        'name': '파손된 손목시계',
        'cost': 10,
        'location': '사건 현장 - 과방',
        'source': '구성민의 손목',
        'result': ['시침은 파손되어 있고 분침은 20분을 가리키고 있다. 이것만으로 사망 시각이 확정되지는 않는다.'],
        "image": find_clue_image('과방 단서 이미지', 'stopped_watch_1720'),
    },
    'scene_cctv': {
        'menu_name': 'CCTV',
        'name': '상자로 가려진 CCTV',
        'cost': 10,
        'location': '사건 현장 - 과방',
        'source': '캐비닛 위 상자',
        'result': ['캐비닛 위 상자가 과방 CCTV의 시야를 가리고 있다. 상자를 놓은 사람과 시각은 아직 확인되지 않았다.'],
        "image": find_clue_image('과방 단서 이미지', 'cctv_blocked'),
    },
    'scene_bacchus': {
        'menu_name': '박카스',
        'name': '개봉된 박카스',
        'cost': 10,
        'location': '사건 현장 - 과방',
        'source': '책상 위 박카스',
        'result': ['개봉된 박카스에서 수면제 성분이 검출되었다. 피해자가 실제로 마셨는지는 확인되지 않는다.'],
        "image": find_clue_image('과방 단서 이미지', 'bacchus_drugged'),
    },
    'scene_story': {
        'menu_name': 'SNS 스토리',
        'name': '16:00 SNS 스토리',
        'cost': 10,
        'location': '사건 현장 - 과방',
        'source': '구성민의 휴대전화',
        'result': ['9월 15일 16:00에 구성민이 올린 SNS 스토리. 사진 속 배경을 통해 당시 과방에 있었음을 알 수 있다. 열람자 정보는 제공되지 않는다.'],
        "image": find_clue_image('과방 단서 이미지', 'seongmin_instagram_story'),
    },
    'scene_cash': {
        'menu_name': '가방',
        'name': '현금 2,000만 원 가방',
        'cost': 10,
        'location': '사건 현장 - 과방',
        'source': '가방',
        'result': ['과방에 남아 있는 가방에서 현금 2,000만 원이 발견되었다.'],
        "image": find_clue_image('과방 단서 이미지', 'cash_bag_20m'),
    },
    # 이지안의 방: 7개
    'jian_cash': {
        'menu_name': '통장',
        'name': '현금 2,000만 원 인출 기록',
        'cost': 10,
        'location': '이지안의 방',
        'source': '통장',
        'result': ['이지안 명의 계좌에서 거액의 현금이 인출된 기록.'],
        "image": find_clue_image('이지안 단서 이미지', 'jian_bank_record'),
    },
    'jian_threat': {
        'menu_name': 'DM',
        'name': '구성민의 협박 DM',
        'cost': 10,
        'location': '이지안의 방',
        'source': '휴대전화',
        'result': ['구성민이 개인적인 정보를 공개하겠다고 협박하며 돈을 요구한 메시지.'],
        "image": find_clue_image('이지안 단서 이미지', 'jian_dm'),
    },
    'jian_event': {
        'menu_name': 'SNS 게시물',
        'name': '잠실 행사 SNS 사진',
        'cost': 10,
        'location': '이지안의 방',
        'source': '휴대전화',
        'result': ['9월 15일 18:30에 게시된 인플루언서 행사 사진. 행사 입장 마감은 18:00, 시작은 18:30이다. 게시 시각만으로 실제 입장 시각이 증명되지는 않는다.'],
        "image": find_clue_image('이지안 단서 이미지', 'jian_event_photo'),
    },
    'jian_id': {
        'menu_name': '신분증',
        'name': '이지안의 신분증',
        'cost': 10,
        'location': '이지안의 방',
        'source': '개인 서류',
        'result': ['신분증에 기록된 법적 성별이 남성이다. 다른 단서 없이 이 사람의 개인적인 의료 이력을 추측할 수는 없다.'],
        "image": find_clue_image('이지안 단서 이미지', 'jian_id_card'),
    },
    'jian_sleep': {
        'menu_name': '처방전 ①',
        'name': '수면제 처방 기록',
        'cost': 10,
        'location': '이지안의 방',
        'source': '처방전',
        'result': ['이지안의 수면제 처방 기록을 확인했다.'],
        "image": find_clue_image('이지안 단서 이미지', 'jian_sleep_prescription'),
    },
    'jian_diary': {
        'menu_name': '일기장',
        'name': '9월 13일 일기',
        'cost': 10,
        'location': '이지안의 방',
        'source': '일기장',
        'result': ['협박이 반복될지 모른다는 두려움, 커리어를 잃을 수 있다는 불안, 구성민이 가진 증거를 없애고 싶다는 생각을 적어 놓았다.'],
        "image": find_clue_image('이지안 단서 이미지', 'jian_diary_0913'),
    },
    'jian_estradiol': {
        'menu_name': '처방전 ②',
        'name': '에스트라디올 데포 처방 기록',
        'cost': 10,
        'location': '이지안의 방',
        'source': '처방전',
        'result': ['에스트라디올 데포 관련 처방 기록. 기록 하나만으로 의료 이력이나 정체성을 단정할 수는 없다.'],
        "image": find_clue_image('이지안 단서 이미지', 'jian_prescription'),
    },
    # 전혜준의 방: 8개
    'hyejun_letter': {
        'menu_name': '편지',
        'name': '위협적인 고백 편지',
        'cost': 10,
        'location': '전혜준의 방',
        'source': '편지',
        'result': ['구성민에게 마음을 고백하면서 거절당하면 죽이겠다는 식의 위협적인 말이 적힌 편지.'],
        "image": find_clue_image('전혜준 단서 이미지', 'hyejun_love_letter'),
    },
    'hyejun_xphoto': {
        'menu_name': '사진',
        'name': '이지안 얼굴에 X 표시한 사진',
        'cost': 10,
        'location': '전혜준의 방',
        'source': '사진',
        'result': ['이지안 얼굴 위에 붉은 X 표시가 그어진 사진.'],
        "image": find_clue_image('전혜준 단서 이미지', 'hyejun_x_photo'),
    },
    'hyejun_dm': {
        'menu_name': 'DM',
        'name': '반복적인 DM',
        'cost': 10,
        'location': '전혜준의 방',
        'source': '휴대전화',
        'result': ['구성민에게 답장을 요구하며 위치를 반복해서 묻는 메시지.'],
        "image": find_clue_image('전혜준 단서 이미지', 'hyejun_dm'),
    },
    'hyejun_ring': {
        'menu_name': '작은 상자',
        'name': '작은 상자 속 커플링',
        'cost': 10,
        'location': '전혜준의 방',
        'source': '작은 상자',
        'result': ['닫혀 있던 작은 상자를 열자 커플링 반지 두 개가 들어 있다. 구성민에게 줬던 반지는 과방 근처 쓰레기통에서 버려진 것을 확인하고 전혜준이 회수했다.'],
        "image": find_clue_image('전혜준 단서 이미지', 'hyejun_couple_ring'),
    },
    'hyejun_knife': {
        'menu_name': '가방',
        'name': '가방 속 칼',
        'cost': 10,
        'location': '전혜준의 방',
        'source': '가방',
        'result': ['전혜준의 가방에 칼이 들어 있다.'],
        "image": find_clue_image('전혜준 단서 이미지', 'hyejun_knife'),
    },
    'hyejun_contact': {
        'menu_name': '연락처',
        'name': '성민이형♡ 저장 연락처',
        'cost': 10,
        'location': '전혜준의 방',
        'source': '휴대전화',
        'result': ['구성민의 연락처가 ‘성민이형♡’으로 저장되어 있다.'],
        "image": find_clue_image('전혜준 단서 이미지', 'hyejun_saved_name'),
    },
    'hyejun_left': {
        'menu_name': '소견서',
        'name': '왼손잡이 소견서',
        'cost': 10,
        'location': '전혜준의 방',
        'source': '소견서',
        'result': ['전혜준이 주로 왼손을 사용한다는 기록. 이 정보만으로 범행을 배제하거나 확정할 수 없다.'],
        "image": find_clue_image('전혜준 단서 이미지', 'hyejun_left_handed'),
    },
    'hyejun_chat': {
        'menu_name': '카카오톡',
        'name': '9월 15일 과방 방문 카카오톡',
        'cost': 10,
        'location': '전혜준의 방',
        'source': '휴대전화',
        'result': ['14:18 전혜준: “반지 버린 거 봤어. 지금 어디야?” / 14:20 구성민: “왜 그러는데?” / 14:24 전혜준: “과방이지? 지금 갈게. 직접 얘기해.”'],
        "image": find_clue_image('전혜준 단서 이미지', 'hyejun_chat_0915'),
    },
    # 변상균 교수 연구실: 7개
    'prof_cctv': {
        'menu_name': 'CCTV 영상',
        'name': '연구실 무단 출입 CCTV',
        'cost': 10,
        'location': '변상균 교수 연구실',
        'source': '컴퓨터',
        'result': ['구성민이 허가 없이 연구실에 들어오는 모습이 촬영된 영상.'],
        "image": find_clue_image('변상균 교수 단서 이미지', 'prof_lab_cctv'),
    },
    'prof_kakao': {
        'menu_name': '카카오톡',
        'name': '9월 15일 약속 카카오톡',
        'cost': 10,
        'location': '변상균 교수 연구실',
        'source': '휴대전화',
        'result': ['변상균 교수와 구성민이 9월 15일 만나기로 한 메시지.'],
        "image": find_clue_image('변상균 교수 단서 이미지', 'prof_meeting_kakao'),
    },
    'prof_korea': {
        'menu_name': '메신저 기록',
        'name': '고려대 교수와 구성민의 메시지',
        'cost': 10,
        'location': '변상균 교수 연구실',
        'source': '컴퓨터',
        'result': ['구성민과 다른 대학 교수의 연구 관련 메시지. 변상균 교수의 조교가 확보했다.'],
        "image": find_clue_image('변상균 교수 단서 이미지', 'prof_chat_capture'),
    },
    'prof_receipt': {
        'menu_name': '영수증',
        'name': '17:13 저녁 결제 영수증',
        'cost': 10,
        'location': '변상균 교수 연구실',
        'source': '영수증',
        'result': ['9월 15일 17:13 결제 영수증. 결제 시각의 알리바이 자료이나 그 후의 연속 동선까지 보장하지 않는다.'],
        "image": find_clue_image('변상균 교수 단서 이미지', 'prof_dinner_receipt'),
    },
    'prof_award': {
        'menu_name': '신문기사',
        'name': '고려대 교수 연구 수상 기사',
        'cost': 10,
        'location': '변상균 교수 연구실',
        'source': '신문기사',
        'result': ['경쟁 대학 교수가 획기적인 연구 성과로 큰 상을 받았다는 기사.'],
        "image": find_clue_image('변상균 교수 단서 이미지', 'prof_award_news'),
    },
    'prof_research': {
        'menu_name': '연구 일지',
        'name': '변상균 교수 연구 일지',
        'cost': 10,
        'location': '변상균 교수 연구실',
        'source': '연구 일지',
        'result': ['거의 완성 단계였던 연구 내용이 적힌 연구 일지. 외부에 알려진 성과와 관련이 있다.'],
        "image": find_clue_image('변상균 교수 단서 이미지', 'prof_research_log'),
    },
    'prof_golf': {
        'menu_name': '골프 사진',
        'name': '오른손 사용 골프 사진',
        'cost': 10,
        'location': '변상균 교수 연구실',
        'source': '사진',
        'result': ['변상균 교수가 오른손잡이인 것으로 추정되는 골프 자세 사진.'],
        "image": find_clue_image('변상균 교수 단서 이미지', 'prof_golf_photo'),
    },
    # 박진서의 방: 7개
    'jinseo_checklist': {
        'menu_name': '체크리스트',
        'name': '9월 14일 준비 체크리스트',
        'cost': 10,
        'location': '박진서의 방',
        'source': '체크리스트',
        'result': ['과방 사람이 없는 시간, CCTV 시야, 캐비닛 위 상자, 9월 15일 저녁 일정, 준비물 등을 점검한 손글씨 목록.'],
        "image": find_clue_image('박진서 단서 이미지', 'jinseo_checklist_0914'),
    },
    'jinseo_diary': {
        'menu_name': '일기장',
        'name': '9월 15일 일기',
        'cost': 10,
        'location': '박진서의 방',
        'source': '일기장',
        'result': ['이미 쓰러져 있던 ‘성민 오빠’를 발견했을 때의 당혹감과 이상한 호기심이 담긴 일기.'],
        "image": find_clue_image('박진서 단서 이미지', 'jinseo_diary_0915'),
    },
    'jinseo_bodyphoto': {
        'menu_name': '사진첩',
        'name': '18:28 시신 사진',
        'cost': 10,
        'location': '박진서의 방',
        'source': '휴대전화',
        'result': ['9월 15일 18:28에 촬영한 구성민 시신 사진(IMG_0915_1828.jpg). 사진 촬영 시각은 주장하는 최초 발견 시각과 별개의 자료다.'],
        "image": find_clue_image('박진서 단서 이미지', 'jinseo_body_photo_1828'),
    },
    'jinseo_child': {
        'menu_name': '상담 기록',
        'name': '어린 시절 상담 기록',
        'cost': 10,
        'location': '박진서의 방',
        'source': '상담 기록',
        'result': ['어린 시절 동물에 위해를 가한 행동 등이 기록된 상담 자료. 이 기록만으로 범행 여부를 판단할 수는 없다.'],
        "image": find_clue_image('박진서 단서 이미지', 'jinseo_childhood_record'),
    },
    'jinseo_childdiary': {
        'menu_name': '오래된 일기장',
        'name': '어린 시절 일기',
        'cost': 10,
        'location': '박진서의 방',
        'source': '일기장',
        'result': ['어린 시절 소외감과 불편한 생각이 드러난 손글씨 일기.'],
        "image": find_clue_image('박진서 단서 이미지', 'jinseo_childhood_diary'),
    },
    'jinseo_search': {
        'menu_name': '검색 기록',
        'name': '둔기 손상 관련 검색 기록',
        'cost': 10,
        'location': '박진서의 방',
        'source': '검색 기록',
        'result': ['무거운 둔기에 의한 머리 부상 등에 관한 검색 내역.'],
        "image": find_clue_image('박진서 단서 이미지', 'jinseo_search_history'),
    },
    'jinseo_calendar': {
        'menu_name': '캘린더',
        'name': '9월 15일 휴대전화 캘린더',
        'cost': 10,
        'location': '박진서의 방',
        'source': '휴대전화',
        'result': ['9월 15일 16:00 ‘준비물 확인’, 18:00 ‘과방 — 성민 오빠’ 일정이 기록되어 있다.'],
        "image": find_clue_image('박진서 단서 이미지', 'jinseo_calendar'),
    },
    # 고건태의 방: 7개
    'geontae_news': {
        'menu_name': '신문기사',
        'name': '과거 학교폭력 관련 신문기사',
        'cost': 10,
        'location': '고건태의 방',
        'source': '신문',
        'result': ['고○○ 학생이 지속적인 학교폭력 끝에 사망했다는 기사. 가해학생 이름과 구성민에 관한 정보는 없다.'],
        "image": find_clue_image('고건태 단서 이미지', 'geontae_brother_news'),
    },
    'geontae_chat': {
        'menu_name': '카카오톡',
        'name': '구성민과의 16:43~16:49 카카오톡',
        'cost': 10,
        'location': '고건태의 방',
        'source': '휴대전화',
        'result': ['9월 15일 16:43~16:49 고건태가 구성민에게 과방에 있는지 묻고 방문하겠다고 한 카카오톡.'],
        "image": find_clue_image('고건태 단서 이미지', 'geontae_chat'),
    },
    'geontae_album': {
        'menu_name': '앨범',
        'name': '고선태·구성민 졸업앨범',
        'cost': 10,
        'location': '고건태의 방',
        'source': '졸업앨범',
        'result': ['두 학생 고선태와 구성민의 사진 및 이름이 가까이 나란히 실린 고등학교 앨범. 사진 촬영은 고선태 사망 이전에 이루어졌다는 설정.'],
        "image": find_clue_image('고건태 단서 이미지', 'geontae_yearbook'),
    },
    'geontae_petition': {
        'menu_name': '탄원서',
        'name': '피해학생 어머니의 탄원서',
        'cost': 10,
        'location': '고건태의 방',
        'source': '탄원서',
        'result': ['학교폭력 피해와 가벼운 조치에 항의하는 어머니의 탄원서. 피해학생과 가해학생 실명은 모두 없다. 사망 전 작성된 문서다.'],
        "image": find_clue_image('고건태 단서 이미지', 'geontae_mother_petition'),
    },
    'geontae_keepsakes': {
        'menu_name': '상자',
        'name': '형의 유품 상자',
        'cost': 10,
        'location': '고건태의 방',
        'source': '유품 상자',
        'result': ['어린 시절 형제 사진, 형이 쓴 생일 카드, 형의 낡은 열쇠고리가 들어 있다.'],
        "image": find_clue_image('고건태 단서 이미지', 'geontae_keepsake_box'),
    },
    'geontae_airpods': {
        'menu_name': '에어팟 케이스',
        'name': '한쪽이 비어 있는 에어팟 케이스',
        'cost': 10,
        'location': '고건태의 방',
        'source': '에어팟 케이스',
        'result': ['오른쪽 유닛만 남아 있고 왼쪽 에어팟은 없다.'],
        "image": find_clue_image('고건태 단서 이미지', 'geontae_airpods_case'),
    },
    'geontae_findmy': {
        'menu_name': '나의 찾기',
        'name': '17:28 에어팟 나의 찾기 기록',
        'cost': 10,
        'location': '고건태의 방',
        'source': '휴대전화',
        'result': ['왼쪽 AirPod Pro 마지막 위치: 생명공학관 인근. 근거리 연결 17:28, 약 0.8m, 사운드 재생 17:28. 게임 속 가상 활동 기록이다.'],
        "image": find_clue_image('고건태 단서 이미지', 'geontae_findmy'),
    },
}

INTERROGATIONS = {
    'jian_q1': {"suspect":'이지안', "number":1, "question":'사건 당일 오후에 무엇을 하고 있었나요?', "answer":'그날 오후 4시 반쯤 성민 오빠를 만나러 과방에 갔어요. 개인적으로 해결해야 할 일이 있었거든요. 오래 있지는 않았어요. 한 20분 정도 있다가 나왔던 것 같아요. 그날 저녁에 잠실에서 열리는 인플루언서 행사에 참석해야 해서 늦어도 5시쯤에는 학교를 떠나야 했거든요. 행사장에는 6시 전에 도착했고, 실제로 행사에 참석한 사진도 남아 있어요.'},
    'jian_q2': {"suspect":'이지안', "number":2, "question":'구성민과는 어떤 관계였고, 최근 어떤 일이 있었나요?', "answer":'성민 오빠랑은 예전부터 알고 지냈어요. 그런데 최근에 저에 대해 남들에게 알려지고 싶지 않은 개인적인 정보를 가지고 협박하기 시작했어요. 처음에는 그냥 무시하려고 했는데, 점점 요구가 심해졌어요. 결국 돈까지 요구했고요. 제가 얼마나 힘들었는지 아무도 모를 거예요. 그렇다고 사람을 죽일 생각까지 한 건 아니에요.'},
    'jian_q3': {"suspect":'이지안', "number":3, "question":'사건과 관련해 수사에 도움이 될 만한 사실을 알고 있나요?', "answer":'사실… 제가 성민 오빠한테 박카스를 하나 건넨 건 맞아요. 거기에 수면제를 넣었어요. 오빠가 잠들면 휴대전화에서 저를 협박할 때 쓰던 증거를 없애려고 했거든요. 그런데 오빠는 박카스를 마시지 않았어요. 제가 나올 때도 그대로 책상 위에 있었고요. 제가 잘못한 건 알아요. 하지만 정말로 죽일 생각은 없었어요.'},
    'hyejun_q1': {"suspect":'전혜준', "number":1, "question":'사건 당일 오후에 무엇을 하고 있었나요?', "answer":'그날 2시 반쯤 성민이 형을 만나러 과방에 갔어요. 형한테 꼭 확인하고 싶은 게 있었거든요. 그런데 과방 앞에 도착했을 때 안에서 누가 크게 말하는 소리가 들렸어요. 분위기가 너무 안 좋아 보여서 들어가지는 않았어요. 그냥 돌아왔습니다. 성민이 형이랑 직접 이야기하지는 못했어요.'},
    'hyejun_q2': {"suspect":'전혜준', "number":2, "question":'구성민과는 어떤 관계였고, 최근 어떤 일이 있었나요?', "answer":'저는 성민이 형을 많이 좋아했어요. 그냥 친한 선후배 이상으로요. 그런데 형은 제 마음을 받아주지 않았어요. 제가 선물한 반지도 버렸고요. 그걸 보고 정말 화가 났어요. 제가 그동안 형한테 어떤 마음이었는데 그렇게 쉽게 버릴 수 있나 싶어서요. 편지에 심한 말을 쓴 것도 사실이에요. 하지만 진심으로 해치려고 한 말은 아니었어요.'},
    'hyejun_q3': {"suspect":'전혜준', "number":3, "question":'사건과 관련해 수사에 도움이 될 만한 사실을 알고 있나요?', "answer":'과방 앞에서 들었던 목소리 중 하나는 변상균 교수님이었던 것 같아요. 교수님이 성민이 형한테 상당히 화가 나 계셨어요. 목소리도 평소보다 훨씬 컸고요. 정확히 무슨 내용으로 싸우는지는 듣지 못했어요. 괜히 끼어들기 싫어서 바로 자리를 떠났거든요. 제가 아는 건 그게 전부예요.'},
    'prof_q1': {"suspect":'변상균 교수', "number":1, "question":'사건 당일 오후에 무엇을 하고 있었나요?', "answer":'오후에는 학교에서 업무를 보고 있었습니다. 구성민 학생과 잠깐 이야기를 나눈 것도 사실입니다. 다만 저녁에는 외부 일정이 있었습니다. 다른 분들과 식사 약속이 있었고, 그 자리에서 결제한 영수증도 남아 있습니다. 영수증에 찍힌 시간이 오후 5시 13분이니, 그 시간에는 제가 과방이 아닌 다른 장소에 있었다는 점은 확인하실 수 있을 겁니다.'},
    'prof_q2': {"suspect":'변상균 교수', "number":2, "question":'구성민과는 어떤 관계였고, 최근 어떤 일이 있었나요?', "answer":'구성민 학생은 제 연구실과 관련이 있는 학생이었습니다. 그런데 최근 제 연구 내용이 외부로 유출된 정황이 발견됐습니다. 확인 과정에서 구성민 학생이 허가 없이 연구실에 출입한 기록도 확인됐고요. 당연히 본인에게 설명을 요구했습니다. 하지만 학생은 관련 사실을 부인했습니다. 화가 난 것은 사실입니다. 오랫동안 진행한 연구가 그런 식으로 외부에 알려지는 일은 결코 가볍게 볼 수 없으니까요.'},
    'prof_q3': {"suspect":'변상균 교수', "number":3, "question":'사건과 관련해 수사에 도움이 될 만한 사실을 알고 있나요?', "answer":'그날 오후 2시쯤 구성민 학생과 과방에서 언쟁이 있었습니다. 제가 연구실 CCTV에 남아 있는 출입 기록을 보여주며 물었지만, 학생은 끝까지 자신은 모르는 일이라고 했습니다. 언성이 높아진 건 인정합니다. 그렇지만 저는 더 이야기해 봐야 소용이 없다고 판단해 대화를 마치고 나왔습니다. 구성민 학생이 이후 누구를 만났는지는 알지 못합니다.'},
    'jinseo_q1': {"suspect":'박진서', "number":1, "question":'사건 당일 오후에 무엇을 하고 있었나요?', "answer":'그날 오후 6시 25분쯤 과방에 갔어요. 성민 오빠가 바닥에 쓰러져 있었는데, 처음에는 무슨 상황인지 잘 이해가 안 됐어요. 가까이 가서 보니까 움직이지도 않고 반응도 없더라고요. 너무 당황해서 한동안 어떻게 해야 할지 몰랐어요. 결국 6시 40분에 신고했어요. 제가 발견했을 때는 이미 그렇게 되어 있었어요.'},
    'jinseo_q2': {"suspect":'박진서', "number":2, "question":'구성민과는 어떤 관계였고, 최근 어떤 일이 있었나요?', "answer":'성민 오빠랑은 같은 과에서 알고 지내는 사이였어요. 아주 친한 건 아니었고요. 저는 원래 사람이 극단적인 상황에서 어떻게 행동하는지 그런 게 조금 궁금했어요. 오빠한테 특별히 개인적인 원한이 있었던 건 아니에요. 그런데 막상 그런 상황을 직접 보니까 생각했던 것과는 많이 다르더라고요. 제가 좀 이상하게 보일 수는 있겠지만, 그렇다고 제가 오빠를 죽였다는 건 아니잖아요.'},
    'jinseo_q3': {"suspect":'박진서', "number":3, "question":'사건과 관련해 수사에 도움이 될 만한 사실을 알고 있나요?', "answer":'제가 들어갔을 때 과방은 조용했어요. 성민 오빠 말고 다른 사람은 보이지 않았고요. 물건들도 크게 흐트러져 있는 것 같지는 않았어요. 캐비닛에 놓아둔 몽키스패너도 그대로 있었던 것 같고… 아, 제가 거기에 뒀다는 뜻은 아니에요. 그냥 평소에 과방에 있던 물건이라 그렇게 말한 거예요. 그리고… 시신 사진을 찍은 건 맞아요. 나중에 뭔가 확인할 일이 있을지도 모른다고 생각했어요.'},
    'geontae_q1': {"suspect":'고건태', "number":1, "question":'사건 당일 오후에 무엇을 하고 있었나요?', "answer":'그날 오후 5시쯤 성민이 형을 만나러 과방에 갔어요. 예전부터 꼭 물어보고 싶었던 게 있어서요. 그런데 막상 만나니까 별로 얘기가 잘 안 되더라고요. 형도 더 이상 그 얘기는 하고 싶지 않다고 했고요. 저도 더 얘기해 봐야 소용없겠다 싶어서 그냥 나왔어요. 5시 10분쯤이었던 것 같아요. 그 뒤로는 바로 집으로 갔고, 과방 근처에는 다시 가지 않았습니다.'},
    'geontae_q2': {"suspect":'고건태', "number":2, "question":'구성민과는 어떤 관계였고, 최근 어떤 일이 있었나요?', "answer":'성민이 형은 예전에 저희 형이랑 같은 고등학교에 다녔어요. 형이 학교 다닐 때 많이 힘들어했거든요. 그때 무슨 일이 있었는지 직접 듣고 싶었어요. 저는 아직도 그때 일을 잊을 수가 없는데, 성민이 형은 이미 다 지나간 일이라는 식으로 말하더라고요. 화가 났던 건 사실이에요. 하지만 화가 난다고 해서 사람을 죽이는 건 아니잖아요.'},
    'geontae_q3': {"suspect":'고건태', "number":3, "question":'사건과 관련해 수사에 도움이 될 만한 사실을 알고 있나요?', "answer":'제가 갔을 때 성민이 형은 혼자 있었어요. 다른 사람이랑 약속이 있었는지는 모르겠고요. 예전 일로 잠깐 말이 오가긴 했지만, 크게 싸운 건 아니었어요. 제가 나올 때도 형은 멀쩡했어요. 그 뒤에 누가 왔는지는 저도 모릅니다. 저도 형이 그렇게 됐다는 소식을 듣고 놀랐어요.'},
}

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
with st.sidebar:
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
                st.rerun()
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
            if st.button("+30P", use_container_width=True):
                st.session_state.points += 30
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
        st.subheader("개발/테스트")
        st.checkbox("디버그 모드", key="debug_mode")
        if st.session_state.debug_mode:
            st.caption("사건 현장 이미지에 hotspot 영역과 디버그 버튼이 표시됩니다.")

        st.divider()
        st.subheader("조사 진행상태 초기화")

        if not st.session_state.reset_confirm:
            if st.button("조사상태 초기화", use_container_width=True):
                st.session_state.reset_confirm = True
                st.rerun()
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
                    st.rerun()

        if st.button("관리자 로그아웃", use_container_width=True):
            st.session_state.admin_ok = False
            st.session_state.debug_mode = False
            st.session_state.reset_confirm = False
            st.rerun()


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
        st.subheader(clue["name"])
        for line in clue.get("result", []):
            st.write(line)
        st.caption("실제 단서 이미지가 등록되면 이 설명 대신 이미지가 표시됩니다.")

    st.divider()

    if st.button("↶ 이전 조사 화면으로 돌아가기", key="reveal_return", use_container_width=True):
        # 사건 현장 또는 용의자의 방을 그대로 유지하고, 증거 화면만 닫습니다.
        st.session_state.last_revealed_clue_id = None
        st.session_state.pending_clue_id = None
        st.session_state.selected_hotspot_id = None
        refresh_image_click_component()
        st.rerun()


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
                st.rerun()
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
                    st.rerun()

            with c2:
                if st.button(
                    "취소",
                    key=f"cancel_investigate_{clue_id}",
                    use_container_width=True,
                ):
                    st.session_state.pending_clue_id = None
                    refresh_image_click_component()
                    st.rerun()


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

                st.rerun()

        if st.button(
            "선택 닫기",
            key=f"close_hotspot_{hotspot_id}",
            use_container_width=True,
        ):
            st.session_state.selected_hotspot_id = None
            st.session_state.pending_clue_id = None
            refresh_image_click_component()
            st.rerun()

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

                st.rerun()

        if st.button(
            "선택 닫기",
            key=f"room_close_{hotspot_id}",
            use_container_width=True,
        ):
            st.session_state.selected_hotspot_id = None
            st.session_state.pending_clue_id = None
            refresh_image_click_component()
            st.rerun()

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
                st.rerun()

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
            st.rerun()
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
            st.rerun()

    st.info("조사할 지점을 선택하세요. 사진 속 물건을 직접 눌러보세요.")

    st.divider()

    try:
        base_image = Image.open(CRIME_SCENE_IMAGE_PATH)
    except FileNotFoundError:
        render_no_image_clue_menu('사건 현장 - 과방')
        return

    display_image = (
        draw_debug_overlay(base_image)
        if st.session_state.debug_mode
        else base_image
    )

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

                st.rerun()

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
            st.rerun()

    st.info("방 안에서 조사하고 싶은 물건을 직접 눌러보세요.")

    try:
        base_image = Image.open(JIAN_ROOM_IMAGE_PATH)
    except FileNotFoundError:
        render_no_image_clue_menu('이지안의 방')
        return

    display_image = (
        draw_jian_debug_overlay(base_image)
        if st.session_state.debug_mode
        else base_image
    )

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

                st.rerun()

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

                    st.rerun()


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
            st.rerun()

    st.info("방 안에서 조사하고 싶은 물건을 직접 눌러보세요.")

    try:
        base_image = Image.open(HYEJUN_ROOM_IMAGE_PATH)
    except FileNotFoundError:
        render_no_image_clue_menu('전혜준의 방')
        return

    display_image = draw_hyejun_debug_overlay(base_image) if st.session_state.debug_mode else base_image
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
                st.rerun()

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
                    st.rerun()


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
            st.rerun()

    st.info("연구실 안에서 조사하고 싶은 물건을 직접 눌러보세요.")

    try:
        base_image = Image.open(PROF_ROOM_IMAGE_PATH)
    except FileNotFoundError:
        render_no_image_clue_menu('변상균 교수 연구실')
        return

    display_image = (
        draw_prof_debug_overlay(base_image)
        if st.session_state.debug_mode
        else base_image
    )

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

                st.rerun()

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

                    st.rerun()



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
            st.rerun()

    st.info("방 안에서 조사하고 싶은 물건을 직접 눌러보세요.")

    try:
        base_image = Image.open(JINSEO_ROOM_IMAGE_PATH)
    except FileNotFoundError:
        render_no_image_clue_menu('박진서의 방')
        return

    display_image = (
        draw_jinseo_debug_overlay(base_image)
        if st.session_state.debug_mode
        else base_image
    )

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

                st.rerun()

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

                    st.rerun()



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
            st.rerun()

    st.info("방 안에서 조사하고 싶은 물건을 직접 눌러보세요.")

    if st.session_state.stage == 3:
        st.success("3차 자유 조사: 이전 조사에서 확인하지 못한 장소와 자료를 자유롭게 다시 조사할 수 있습니다.")

    try:
        base_image = Image.open(GEONTAE_ROOM_IMAGE_PATH)
    except FileNotFoundError:
        render_no_image_clue_menu('고건태의 방')
        return

    display_image = (
        draw_geontae_debug_overlay(base_image)
        if st.session_state.debug_mode
        else base_image
    )

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

                st.rerun()

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

                    st.rerun()


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
                with st.expander(f"📄 {clue['name']}"):
                    if clue.get("image") and os.path.isfile(clue["image"]):
                        show_optional_image(clue["image"])
                    else:
                        for line in clue.get("result", []): st.write(line)
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
        st.success("최종 추리가 제출되었습니다. 제출 후에는 수정할 수 없습니다.")
        for key,label in labels.items():
            with st.container(border=True):
                st.write(f"**{label}**")
                st.write(st.session_state.final_answers.get(key, ""))
        if st.button("⬅ 메인 화면으로 돌아가기", use_container_width=True):
            clear_transient_states()
            st.session_state.current_view = None
            st.rerun()
        return
    if not st.session_state.final_submission_open or st.session_state.stage < 3:
        st.warning("아직 최종 추리 제출 시간이 아닙니다.")
        if st.button("⬅ 메인 화면으로 돌아가기", use_container_width=True):
            st.session_state.current_view = None
            st.rerun()
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
            st.rerun()
    if st.button("⬅ 메인 화면으로 돌아가기", use_container_width=True):
        clear_transient_states()
        st.session_state.current_view = None
        st.rerun()


def render_interrogation():
    """3차 조사 전용. 질문별 20P, 누적 최대 4개, 동일 질문 재열람 무료."""
    if st.session_state.stage < 3:
        st.warning("용의자 심문은 3차 조사에서만 가능합니다.")
        return
    st.title("🗣️ 용의자 심문")
    count = len(st.session_state.interrogated_questions)
    c1,c2,c3 = st.columns(3)
    c1.metric("남은 심문", f"{MAX_INTERROGATIONS-count} / {MAX_INTERROGATIONS}")
    c2.metric("질문당 비용", f"{INTERROGATION_COST} P")
    c3.metric("현재 포인트", f"{st.session_state.points} P")
    st.caption("팀당 최대 4개의 질문을 구매할 수 있습니다. 구매한 질문은 무료로 다시 볼 수 있습니다.")
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
                    st.rerun()
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
        st.rerun()


# ─────────────────────────────────────
# 장소 라우팅
# ─────────────────────────────────────
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
        st.rerun()

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
            st.rerun()

if st.session_state.stage >= 3:
    st.markdown('<div class="game-section">▌ 용의자 심문 &nbsp; / &nbsp; INTERROGATION</div>',unsafe_allow_html=True)
    if st.button(f"🗣 용의자 심문 · 남은 {MAX_INTERROGATIONS - len(st.session_state.interrogated_questions)}회 / {MAX_INTERROGATIONS}", key="home_interview", use_container_width=True):
        clear_transient_states()
        st.session_state.current_view = "용의자 심문"
        st.rerun()

st.markdown('<div class="game-section">▌ 수사 기록 &nbsp; / &nbsp; CASE ARCHIVE</div>',unsafe_allow_html=True)
c1,c2=st.columns(2)
with c1:
    if st.button("▣ 확보한 증거 열람",key="home_archive",use_container_width=True):
        clear_transient_states()
        refresh_image_click_component()
        st.session_state.current_view="확보한 단서"
        st.rerun()
with c2:
    if st.session_state.final_submission_open or st.session_state.final_submitted:
        if st.button("✎ 최종 추리 제출",key="home_final",use_container_width=True,type="primary"):
            clear_transient_states()
            st.session_state.current_view="최종 추리 제출"
            st.rerun()
    else:
        st.button("🔒 최종 추리 · LOCKED",key="home_final_locked",disabled=True,use_container_width=True)
