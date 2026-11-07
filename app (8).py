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
        'menu_name': '가방',
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


# ── 텍스트 테스트 모드용 상세 조사 카드 ──
TEXT_EVIDENCE = {'scene_extinguisher': '[현장 물품 조사 | ABC 분말소화기]\n'
                       '\n'
                       '출입문 가까운 벽면에 붉은색 소화기 1대가 세워져 있다. 몸통과 검은 호스에 눈에 띄는 먼지층은 없으며, 바닥에 닿는 하단부에는 긁힌 자국이 '
                       '여러 개 있다. 긁힌 부분 일부에서는 붉은 코팅이 벗겨져 회색 금속 면이 드러난다.\n'
                       '\n'
                       '본체 라벨의 외장 코팅 사양(작은 글씨):\n'
                       '• 도막 수지: 폴리에스터계\n'
                       '• 색상 안료: 산화철계(Fe₂O₃)\n'
                       '• 도막 두께: 약 60~80μm\n'
                       '\n'
                       '소화기 압력계 바늘은 녹색 정상 범위에 위치한다.',
 'scene_bat': '[현장 물품 조사 | 야구방망이]\n'
              '\n'
              '출입문 옆 우산꽂이에 나무 야구방망이 한 자루가 비스듬히 기대어 있다. 몸통 표면에는 가느다란 긁힘이 있지만 눈에 띄는 파손은 없다.\n'
              '\n'
              '방망이의 넓은 타격 부분부터 손잡이의 홈 사이까지 옅은 회색 먼지가 얇고 고르게 쌓여 있다. 손잡이 부분에도 손으로 쥐었을 때 흔히 남는 뚜렷한 깨끗한 자국은 '
              '보이지 않는다.',
 'scene_wrench': '[현장 물품 조사 | 몽키스패너]\n'
                 '\n'
                 '과방 한쪽 작은 나무 탁자 위에 몽키스패너가 놓여 있다. 은회색 금속 턱과 조절 나사, 붉은색으로 도장된 손잡이로 구성되어 있다. 손잡이는 탁자 바깥쪽을 '
                 '향한다.\n'
                 '\n'
                 '손잡이의 붉은 표면에서 소량의 코팅 시료를 채취해 분석했다.\n'
                 '• 결합재: 에폭시계\n'
                 '• 적색 안료: 유기 적색 안료계\n'
                 '• 금속 턱: 일반 철계 합금\n'
                 '\n'
                 '손잡이 끝부분에는 사용하면서 생긴 듯한 잔긁힘이 보인다.',
 'scene_red_paint': '[현장 미세물 감식 | 붉은 도료 조각]\n'
                    '\n'
                    '시신 가까운 작은 핏방울들 사이에서 얇고 단단한 붉은 조각 여러 개가 발견되었다. 조각들은 불규칙한 형태이며 크기는 약 2~5mm다. 한쪽 표면은 '
                    '광택이 나는 붉은색, 반대쪽에는 옅은 회색 바탕층이 남아 있다.\n'
                    '\n'
                    '[채취 시료 분석 결과]\n'
                    '• 수지 성분: 폴리에스터계\n'
                    '• 색상 안료: 산화철계(Fe₂O₃)\n'
                    '• 도막 두께: 약 65~75μm\n'
                    '• 관찰 특징: 붉은 상도 아래 얇은 회색층',
 'scene_wound1': '[두부 손상 감식서 ① | 외상 형태]\n'
                 '\n'
                 '피해자: 구성민\n'
                 '사건일: 2026년 9월 15일\n'
                 '\n'
                 '머리 오른쪽 측두·두정 부위에 둔한 충격에 의한 손상이 집중되어 있다. 피부 표면의 찢김과 주변 연부조직의 손상은 뾰족하거나 날카로운 물체보다 넓고 '
                 '단단한 물체가 강하게 접촉했을 때의 양상과 가깝다.\n'
                 '\n'
                 '손상의 윤곽은 좁은 날이나 날카로운 모서리에 의한 선형 절창과 뚜렷하게 다르다. 주요 타격 부위 주변에서도 압박성 손상과 출혈이 확인된다.',
 'scene_wound2': '[두부 손상 감식서 ② | 충격 위치와 방향]\n'
                 '\n'
                 '피해자: 구성민\n'
                 '사건일: 2026년 9월 15일\n'
                 '\n'
                 '주요 손상은 머리 오른쪽 측면에 집중된다. 손상 분포를 검토한 결과, 피해자의 오른쪽 방향에서 둔한 외력이 가해졌을 가능성이 높은 것으로 평가된다.\n'
                 '\n'
                 '[감식 소견]\n'
                 '손상이 집중된 면: 우측 측두·두정 부위\n'
                 '추정 충격 방향: 피해자 기준 우측에서 안쪽 방향\n'
                 '현장 확인 사항: 정확한 공격 자세와 공격자 위치는 영상으로 확인되지 않음',
 'scene_tod': '[법의학 감정서 | 사망 시각 추정]\n'
              '\n'
              '피해자: 구성민\n'
              '사건일: 2026년 9월 15일\n'
              '\n'
              '현장 발견 당시의 체온, 시반, 사후 경직 및 주변 환경에 대한 감정을 종합한 결과, 사망 추정 시각은 다음과 같다.\n'
              '\n'
              '**2026년 9월 15일 16:00~18:30**\n'
              '\n'
              '감정 담당자는 위 시각을 오차 범위를 포함하는 추정 구간으로 기재했다.',
 'scene_watch': '[현장 물품 조사 | 손목시계]\n'
                '\n'
                '피해자 구성민의 손목에 아날로그 시계가 차여 있다. 유리는 금이 갔고 시곗바늘 일부가 손상되어 있다.\n'
                '\n'
                '• 시침: 부러져 현재 위치 확인 불가\n'
                '• 분침: 숫자 4 방향, 즉 **20분** 위치에서 정지\n'
                '• 초침: 파손되어 판독 불가\n'
                '\n'
                '시계 뒷면에는 외부에서 긁힌 흔적이 남아 있다.',
 'scene_cctv': '[현장 설비 확인 | CCTV]\n'
               '\n'
               '과방 오른쪽 높은 캐비닛 위, 벽면 구석에 CCTV가 설치되어 있다. CCTV 렌즈 바로 앞쪽에 갈색 종이상자가 놓여 있어 카메라의 과방 내부 시야를 대부분 '
               '가리고 있다.\n'
               '\n'
               '확보된 영상에는 일정 시점부터 상자의 갈색 면이 화면의 큰 부분을 차지하는 모습이 나타난다. 카메라 본체와 전원 연결에는 눈에 띄는 파손이 없다.',
 'scene_bacchus': '[현장 물품 및 성분 감식 | 박카스]\n'
                  '\n'
                  '원형 탁자에 개봉된 박카스 병 한 개가 놓여 있다. 병뚜껑은 옆에 놓여 있고 안에는 음료가 일부 남아 있다.\n'
                  '\n'
                  '[잔여액 검사]\n'
                  '• 음료 성분: 박카스 계열 음료와 부합\n'
                  '• 추가 검출 성분: 수면제 계열 약물\n'
                  '\n'
                  '병 입구와 뚜껑은 별도로 수거해 보관했다.',
 'scene_story': '[구성민 휴대전화 | SNS 스토리]\n'
                '\n'
                '2026년 9월 15일 오후 **4:00**에 업로드된 SNS 스토리 한 건이 저장되어 있다.\n'
                '\n'
                "사진에는 과방 특유의 화이트보드와 소파, 원형 탁자가 함께 보인다. 화이트보드의 '생명공학과 화이팅!' 문구가 식별되며, 사진 한쪽에는 과방 내부의 "
                '가구들이 담겨 있다.\n'
                '\n'
                '게시 계정: 구성민',
 'scene_cash': '[현장 물품 조사 | 검은 운동가방]\n'
               '\n'
               '과방 소파 위에 놓인 커다란 검은색 운동가방이다. 지퍼가 닫혀 있으며 안이 빽빽하게 채워져 있다.\n'
               '\n'
               '지퍼를 열자 띠지로 묶은 5만 원권 지폐 다발이 여러 묶음 들어 있다. 현금을 세어 확인한 총액은 **20,000,000원**이다. 함께 들어 있는 물건은 '
               '없다.',
 'jian_cash': '[통장 거래 내역]\n'
              '\n'
              '예금주: 이지안\n'
              '\n'
              '2026.09.15  / 현금 인출  / **20,000,000원**\n'
              '\n'
              "통장에는 위 거래 직전까지 일반적인 생활비 입출금 내역이 이어져 있다. 이 거래의 적요에는 '현금 인출'로 표시되어 있다.",
 'jian_threat': '[휴대전화 | 구성민과의 DM]\n'
                '\n'
                '구성민: 너 이거 사람들한테 알려져도 상관없어?\n'
                '이지안: 제발 그 얘기만은 하지 마.\n'
                '구성민: 네가 지금까지 쌓아 온 거 다 날아갈 수도 있겠네.\n'
                '이지안: 나한테 왜 이러는 건데.\n'
                '구성민: **2천만 원**. 그 정도면 조용히 넘어가 줄게.\n'
                '이지안: 그 돈을 갑자기 어떻게 마련해.\n'
                '구성민: 15일까지 준비해. 그때 과방에서 보자.\n'
                '이지안: 돈 주면 정말 끝나는 거지?\n'
                '\n'
                '메시지 대화창에는 추가 첨부파일이 보이지 않는다.',
 'jian_event': '[SNS 게시물 | 행사 참석 사진]\n'
               '\n'
               '계정: 이지안\n'
               '게시일: 2026년 9월 15일\n'
               '게시 시각: **18:30**\n'
               '\n'
               '잠실의 인플루언서 행사장 포토월 앞에서 찍힌 이지안의 사진이 게시되어 있다. 사진 배경의 행사 로고가 안내문에 인쇄된 로고와 일치한다.\n'
               '\n'
               '함께 저장된 행사 안내문:\n'
               '• 입장 마감: **18:00**\n'
               '• 행사 시작: **18:30**',
 'jian_id': '[개인 신분증]\n'
            '\n'
            '성명: 이지안\n'
            '사진: 신분증용 상반신 사진\n'
            '법적 성별 표기: **남성**\n'
            '\n'
            '신분증 표면에는 사용에 따른 작은 흠집이 있지만 이름과 성별 표기는 선명하게 판독된다.',
 'jian_sleep': '[진료·처방 내역 ①]\n'
               '\n'
               '처방 대상: 이지안\n'
               '기록 종류: 수면 관련 약물 처방전\n'
               '\n'
               '수면을 돕는 약제가 다량 처방된 기록이 확인된다. 처방전에는 복용 횟수와 하루 권장량, 의료기관의 확인 표시가 기재되어 있다.',
 'jian_diary': '[개인 일기 | 2026년 9월 13일]\n'
               '\n'
               '요즘 정말 미칠 것 같다.\n'
               '여기까지 오려고 얼마나 노력했는데. 이제 겨우 모든 게 잘 풀리기 시작했는데, 그 사람이 모든 걸 망쳐 버릴 수도 있다는 생각에 잠도 제대로 못 자겠다.\n'
               '\n'
               '돈을 주면 정말 끝날까? 한 번 요구를 들어주면 앞으로도 계속 협박하는 건 아닐까.\n'
               '\n'
               '이 일이 알려지면 지금까지 쌓아 온 이미지도, 커리어도 한순간에 무너질 것 같다. 앞으로 사람들 얼굴을 어떻게 봐야 할지도 모르겠다.\n'
               '\n'
               '어떻게든 그 사람이 가지고 있는 증거를 없애야 할 것 같은데, 대체 어떻게 해야 하지.\n'
               '\n'
               '정말 너무 무섭다.',
 'jian_estradiol': '[진료·처방 내역 ②]\n'
                   '\n'
                   '처방 대상: 이지안\n'
                   '약제명: **에스트라디올 데포(Estradiol depot)**\n'
                   '기록 종류: 주사제 처방 내역\n'
                   '\n'
                   '의료기관 발급 처방전이며, 투여 일정과 용량이 의료 기록 형식으로 기재되어 있다.',
 'hyejun_letter': '[손편지 | 구성민에게]\n'
                  '\n'
                  '성민이 형.\n'
                  '\n'
                  '형한테 이런 얘기를 직접 하면 또 피할 것 같아서 편지로 써. 나는 형이 정말 좋았어. 사람들이 뭐라고 하든 상관없을 만큼.\n'
                  '\n'
                  '그런데 형은 내가 무슨 말을 해도 대충 웃고 넘기잖아. 나 혼자만 진심이었던 건가 싶어서 미칠 것 같아. 형이 내 마음을 받아주지 않으면, **차라리 '
                  '죽여 버리고 싶을 만큼** 화가 날 것 같아.\n'
                  '\n'
                  '이 편지를 읽고는 제발 피하지 말고 대답해 줘.\n'
                  '\n'
                  '— 혜준',
 'hyejun_xphoto': '[책상 위 사진]\n'
                  '\n'
                  '사진 표면에 비친 강한 빛 때문에 멀리서 내용이 보이지 않았으나, 꺼내서 살펴보니 **이지안의 얼굴이 찍힌 사진**이었다.\n'
                  '\n'
                  '이지안의 얼굴 위에는 붉은 펜으로 여러 번 그은 큰 **X 표시**가 있다. 사진 뒷면에는 글씨가 적혀 있지 않다.',
 'hyejun_dm': '[휴대전화 | 구성민에게 보낸 DM 일부]\n'
              '\n'
              '전혜준: 형 지금 뭐 해?\n'
              '전혜준: 답장 좀 해 줘.\n'
              '전혜준: 어디야?\n'
              '전혜준: 나랑 얘기 좀 하자.\n'
              '전혜준: 지금 과방이야?\n'
              '전혜준: 읽었으면 뭐라도 말해 줘.\n'
              '\n'
              '여러 메시지는 읽음 표시 없이 연속으로 발송되어 있다.',
 'hyejun_ring': '[중앙 탁자 | 작은 상자]\n'
                '\n'
                '닫혀 있던 검은 보석 상자를 열었다. 안에는 디자인이 같은 은색 반지 **두 개**가 나란히 놓여 있다. 크기는 서로 조금 다르며, 반지 안쪽에는 같은 '
                '기념 문구가 새겨져 있다.\n'
                '\n'
                "상자 바닥에는 반지 케이스 구매 영수증이 접혀 있다. 전혜준의 메모에는 짧게 '버려진 걸 다시 주웠다'라고 적혀 있다.",
 'hyejun_knife': '[침대 옆 백팩]\n'
                 '\n'
                 '검은 백팩 안쪽 지퍼 수납칸에서 접이식 칼 한 자루가 나왔다. 손잡이는 어두운 색이며 칼날에는 약한 사용 흔적이 있다.\n'
                 '\n'
                 '칼은 접힌 상태로 보관되어 있었고, 백팩의 다른 칸에는 충전기와 필기구가 들어 있다.',
 'hyejun_contact': '[휴대전화 | 저장된 연락처]\n'
                   '\n'
                   '이름: **성민이형♡**\n'
                   '연락처: 구성민\n'
                   '\n'
                   '최근 통화 목록에는 이 연락처로 여러 번 전화를 건 기록이 표시되어 있다.',
 'hyejun_left': '[손 사용 습관 소견서]\n'
                '\n'
                '대상자: 전혜준\n'
                '\n'
                '일상생활에서 주로 사용하는 손: **왼손**\n'
                '관찰 항목: 필기, 도구 쥐기, 물체를 던지는 동작\n'
                '\n'
                '평가 의견: 세 항목에서 왼손 사용이 우세하게 관찰됨.',
 'hyejun_chat': '[카카오톡 | 2026년 9월 15일]\n'
                '\n'
                '14:18 전혜준: **반지 버린 거 봤어. 지금 어디야?**\n'
                '14:20 구성민: **왜 그러는데?**\n'
                '14:24 전혜준: **과방이지? 지금 갈게. 직접 얘기해.**',
 'prof_cctv': '[연구실 컴퓨터 | CCTV 영상]\n'
              '\n'
              '파일명: LAB_CAM_20260915.mp4\n'
              '\n'
              '영상에는 구성민이 연구실 문을 열고 혼자 들어오는 모습이 담겨 있다. 당시 연구실 안에는 다른 사람이 보이지 않는다. 구성민은 실험대와 컴퓨터가 있는 방향으로 '
              '걸어간다.\n'
              '\n'
              '연구실 출입 기록에는 해당 시간대 구성민에게 허가된 공식 출입 신청이 없다.',
 'prof_kakao': '[휴대전화 | 구성민과의 카카오톡]\n'
               '\n'
               '변상균: 성민 학생, 오늘 학교에 있습니까?\n'
               '구성민: 네 교수님.\n'
               '변상균: 확인할 일이 있으니 오후 2시에 과방에서 봅시다.\n'
               '구성민: 어떤 일 때문이신가요?\n'
               '변상균: 만나서 이야기합시다.\n'
               '구성민: 네, 알겠습니다.',
 'prof_korea': '[연구실 컴퓨터 | 조교 이메일]\n'
               '\n'
               '보낸 사람: 연구실 조교\n'
               '받는 사람: 변상균 교수\n'
               '제목: 요청하신 메시지 캡처 전달드립니다\n'
               '\n'
               '교수님, 말씀하신 자료를 확보해 첨부합니다. 구성민 학생과 고려대학교 소속 교수 사이에 주고받은 메시지입니다.\n'
               '\n'
               '[첨부된 대화 일부]\n'
               '구성민: 지난번 말씀드린 연구 관련 자료입니다.\n'
               '고려대 교수: 확인했습니다. 특히 분석 결과 부분이 흥미롭군요.\n'
               '구성민: 추가 내용도 정리되는 대로 보내드리겠습니다.\n'
               '\n'
               '첨부파일: messenger_capture_01.png',
 'prof_receipt': '[영수증 | 식사 결제]\n'
                 '\n'
                 '결제일: **2026.09.15**\n'
                 '결제 시각: **17:13**\n'
                 '업종: 음식점\n'
                 '결제 내역: 식사 및 음료\n'
                 '결제 상태: 승인 완료\n'
                 '\n'
                 '영수증 하단에는 카드 승인번호와 음식점 정보가 인쇄되어 있다.',
 'prof_award': '[신문기사 | 연구 성과 수상]\n'
               '\n'
               '**고려대학교 연구진, 획기적 성과로 대형 학술상 수상**\n'
               '\n'
               '고려대학교 소속 연구자가 새로운 분석 방법과 연구 결과를 발표해 올해 주요 학술상 수상자로 선정됐다. 학계는 해당 연구가 기존 연구의 한계를 넘어서는 성과를 '
               '제시했다고 평가했다.\n'
               '\n'
               '기사에는 핵심 분석 방법과 실험 접근법이 요약되어 있다.',
 'prof_research': '[변상균 교수 연구 일지]\n'
                  '\n'
                  "장기간의 실험 날짜, 가설, 반복 측정 결과가 정리된 두꺼운 연구 일지다. 후반부에는 데이터 분석 도표와 함께 '발표 원고 최종 정리'라는 메모가 남아 "
                  '있다.\n'
                  '\n'
                  '일지의 핵심 도표와 실험 설계에는 최근 경쟁 대학에서 발표된 연구 기사에 등장하는 방법과 유사한 대목이 여러 곳 있다. 마지막 장에는 수정한 원고의 '
                  '제출 예정 일정이 적혀 있다.',
 'prof_golf': '[책장 위 액자 | 골프 사진]\n'
              '\n'
              '빛을 비껴 액자를 살펴보니 변상균 교수가 야외 골프장에서 스윙하는 모습이 담겨 있다. 사진 속 교수는 오른손잡이 골퍼가 일반적으로 취하는 자세로 클럽을 잡고 '
              '있다.\n'
              '\n'
              '사진 아래쪽에는 동료 교수들과 함께 찍은 날짜가 손글씨로 적혀 있다.',
 'jinseo_checklist': '[벽면 체크리스트 | 2026년 9월 14일]\n'
                     '\n'
                     '□ 과방 사람 없는 시간 확인\n'
                     '☑ CCTV 시야 확인\n'
                     '☑ 캐비닛 위 상자\n'
                     '□ 9/15 저녁 일정 확인\n'
                     '□ 준비물 확인\n'
                     '\n'
                     '검은 볼펜으로 적은 글씨이며 일부 획 끝에서 잉크가 종이 오른쪽으로 번져 있다.',
 'jinseo_diary': '[박진서 일기 | 2026년 9월 15일]\n'
                 '\n'
                 '과방에 갔을 때 성민 오빠는 이미 바닥에 쓰러져 있었다. 처음엔 무슨 상황인지 이해가 되지 않았다. 가까이 갔는데도 아무 반응이 없었다.\n'
                 '\n'
                 '그 모습을 보고 한동안 아무것도 하지 못했다. 무서운 건지, 이상하게 궁금한 건지 나도 잘 모르겠다. 결국 신고했다.\n'
                 '\n'
                 '지금도 그 장면이 눈앞에서 사라지지 않는다.\n'
                 '\n'
                 '일기장 오른쪽 여백에 볼펜 잉크가 번진 흔적이 있다.',
 'jinseo_bodyphoto': '[휴대전화 | 사진첩]\n'
                     '\n'
                     '파일명: **IMG_0915_1828.jpg**\n'
                     '촬영일: **2026.09.15**\n'
                     '촬영 시각: **18:28**\n'
                     '\n'
                     '사진에는 과방 바닥에 쓰러진 구성민과 주변의 가구들이 담겨 있다. 사진은 흔들림이 적고 시신의 주변 상황이 한눈에 보이도록 찍혀 있다.',
 'jinseo_child': '[어린 시절 상담 기록 | 발췌]\n'
                 '\n'
                 '대상자: 박진서\n'
                 '주요 상담 내용: 또래와의 관계 형성에서 반복적인 어려움을 보임. 감정 표현이 제한적이며, 타인의 고통이나 반응에 대해 독특한 호기심을 드러낸 적이 '
                 '있음.\n'
                 '\n'
                 '보호자 진술: 어린 시절 동물에게 위해를 가하는 행동이 관찰되어 상담을 신청함.\n'
                 '\n'
                 '담당 상담자의 서명과 상담일자가 문서 하단에 남아 있다.',
 'jinseo_childdiary': '[책장 속 오래된 일기장 | 어린 시절]\n'
                      '\n'
                      '애들은 왜 내가 이상하다고 하는 걸까. 그냥 왜 그런 반응을 하는지가 궁금했을 뿐인데.\n'
                      '\n'
                      '사람들은 다들 비슷한 말을 한다. 무섭다, 이상하다, 그러지 마라. 나는 아직도 무엇이 그렇게 잘못됐는지 모르겠다.\n'
                      '\n'
                      '일기장 글씨의 일부는 종이 오른쪽으로 잉크가 살짝 끌린 흔적이 있다.',
 'jinseo_search': '[컴퓨터 | 최근 검색 기록]\n'
                  '\n'
                  '• 둔기로 머리를 맞으면 어떤 손상이 생기나\n'
                  '• 무거운 금속 물체 두부 충격\n'
                  '• 머리에 강한 충격을 받았을 때 외상 형태\n'
                  '• 둔기 외상 관련 법의학 자료\n'
                  '\n'
                  '여러 검색 페이지의 열람 기록이 최근 날짜에 집중되어 있다.',
 'jinseo_calendar': '[휴대전화 | 2026년 9월 15일 일정]\n'
                    '\n'
                    '**16:00 — 준비물 확인**\n'
                    '**18:00 — 과방, 성민 오빠**\n'
                    '\n'
                    '두 일정 모두 개인 캘린더에 직접 등록된 항목이며, 별도의 참석자 초대나 확인 표시는 없다.',
 'geontae_news': '[보관된 신문기사 | 고교생 사망 사건]\n'
                 '\n'
                 '**학교폭력 피해 호소하던 고교생 숨져…유족, 학교 대응 비판**\n'
                 '\n'
                 '한 고등학교에 재학 중이던 **고○○ 군**이 지속적인 학교폭력 피해를 겪은 끝에 숨진 사실이 알려졌다. 유족에 따르면 피해학생은 장기간 언어폭력과 '
                 '괴롭힘을 호소해 왔다.\n'
                 '\n'
                 '유족은 학교 측에 수차례 도움을 요청했으나 충분한 보호 조치가 이루어지지 않았다고 주장했다. 교육 당국은 관련 경위를 조사하고 있다고 밝혔다.',
 'geontae_chat': '[카카오톡 | 2026년 9월 15일]\n'
                 '\n'
                 '16:43 고건태: **형 오늘 학교야?**\n'
                 '16:44 구성민: **ㅇㅇ**\n'
                 '16:45 고건태: **지금 과방에 있어?**\n'
                 '16:46 구성민: **응 있어. 무슨 일이야?**\n'
                 '16:46 고건태: **할 얘기 좀 있는데 잠깐 얼굴 보고 얘기하면 좋을 것 같아서**\n'
                 '16:47 구성민: **그래 지금 과방이니까 와**\n'
                 '16:49 고건태: **ㅇㅋ 지금 갈게**\n'
                 '16:49 구성민: **ㅇㅇ**',
 'geontae_album': '[책장 속 앨범 | 고등학교 졸업 기념 사진]\n'
                  '\n'
                  '학급 학생들의 사진과 이름이 작은 글씨로 배열된 페이지다. 이름순 명단에서 **고선태**와 **구성민**이 가까운 위치에 나란히 실려 있다.\n'
                  '\n'
                  '사진 촬영은 두 학생이 학교에 함께 다니던 시기에 이루어졌다. 페이지 아래쪽에는 학급 단체사진도 함께 수록되어 있다.',
 'geontae_petition': '[보관된 탄원서 | 학교폭력 조치 결과에 대한 재검토 요청]\n'
                     '\n'
                     '저는 학교폭력 피해학생의 어머니입니다.\n'
                     '\n'
                     '아이는 오랫동안 반복된 괴롭힘 때문에 학교에 가는 것조차 두려워했습니다. 밤마다 울고, 사람을 만나는 것도 어려워했습니다. 그런데 가해학생에게 '
                     '내려진 조치는 아이가 받은 고통에 비해 너무 가볍습니다.\n'
                     '\n'
                     '이대로 아무 일 없었다는 듯 넘어갈 수는 없습니다. 아이가 다시 안심하고 학교생활을 할 수 있도록 조치 결과를 재검토해 주시기를 간절히 '
                     '부탁드립니다.\n'
                     '\n'
                     '피해학생 보호자 올림\n'
                     '\n'
                     '문서에는 접수 날짜와 학교의 접수 도장이 찍혀 있다.',
 'geontae_keepsakes': '[방 구석 | 오래된 상자]\n'
                      '\n'
                      '상자를 열자 색이 바랜 사진 여러 장, 손때 묻은 열쇠고리 하나, 오래된 생일 카드가 들어 있다.\n'
                      '\n'
                      "사진 한 장에는 어린 남자아이 둘이 어깨를 맞대고 웃고 있다. 사진 뒷면에는 '선태·건태'라는 메모가 적혀 있다.\n"
                      '\n'
                      "생일 카드: '건태야, 생일 축하해! 무슨 일이 있어도 형이 네 편인 거 알지? — 선태 형'",
 'geontae_airpods': '[가방 내부 | 무선 이어폰 케이스]\n'
                    '\n'
                    '가방 안쪽 주머니에 흰색 무선 이어폰 충전 케이스가 있다. 뚜껑을 열자 **오른쪽 유닛만 들어 있고 왼쪽은 비어 있다.**\n'
                    '\n'
                    '케이스에는 작은 긁힘이 몇 개 있으며 충전 단자와 오른쪽 이어폰은 정상적으로 보인다.',
 'geontae_findmy': '[휴대전화 | 나의 찾기 활동 기록]\n'
                   '\n'
                   '기기: **왼쪽 AirPod Pro**\n'
                   '날짜: **2026년 9월 15일**\n'
                   '\n'
                   '• 마지막 확인 위치: **연세대학교 생명공학관 인근**\n'
                   '• **17:28 — 근거리 연결 감지**\n'
                   '• 감지 당시 기기 간 거리: **약 0.8m**\n'
                   '• **17:28 — 사운드 재생**\n'
                   '\n'
                   '화면 하단에는 작은 캠퍼스 지도와 감지 위치를 나타내는 표시가 남아 있다.'}
for _cid, _body in TEXT_EVIDENCE.items():
    CLUES[_cid]["result"] = [_body]

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
    if clue_id not in st.session_state.investigated_clues:
        st.warning("아직 구매하지 않은 자료입니다. 조사 비용을 지불한 뒤 열람할 수 있습니다.")
        return
    st.markdown('<div class="game-section">▌ EVIDENCE ACQUIRED / 증거 확보</div>', unsafe_allow_html=True)
    st.subheader(clue["name"])
    st.caption(f"발견 장소: {clue['location']} · 조사 대상: {clue['source']} · 확보 완료")
    for line in clue.get("result", []):
        st.markdown(line.replace("\n", "  \n"))
    st.caption("※ 본 자료는 추리게임을 위한 가상 문서·현장 관찰 기록입니다. 의혹과 확정 사실을 구분해 판단하세요.")
    st.divider()
    if st.button("↶ 이전 조사 화면으로 돌아가기", key="reveal_return", use_container_width=True):
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
                    for line in clue.get("result", []):
                        st.markdown(line.replace("\n", "  \n"))
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
<div class="game-sub">단서 상세 텍스트 테스트 · 현장 사진을 조사해 사건을 재구성하라.</div>
<div class="game-status">● UNSOLVED / 수사 진행 중</div>
</div>""",unsafe_allow_html=True)

m1,m2,m3=st.columns(3)
with m1: st.metric("INVESTIGATION TEAM",f"{st.session_state.team_no}팀")
with m2: st.metric("REMAINING POINTS",f"{st.session_state.points} P")
with m3: st.metric("INVESTIGATION PHASE",f"{st.session_state.stage:02d} / 03")

st.markdown('<div class="game-section">▌ 조사 구역 선택 &nbsp; / &nbsp; SELECT LOCATION</div>',unsafe_allow_html=True)
st.markdown('<div class="game-caption">잠금 해제된 장소의 사진에서 빨간 네모로 표시된 물건을 클릭하세요. 조사 후 상세 자료는 텍스트로 제공됩니다.</div>',unsafe_allow_html=True)
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
