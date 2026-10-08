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
</style>""",unsafe_allow_html=True)

def config_value(key, default=""):
    try:
        return st.secrets.get(key, os.environ.get(key, default))
    except Exception:
        return os.environ.get(key, default)

ADMIN_PASSWORD = config_value("ADMIN_PASSWORD", "mt1234")
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
LOCAL_DB = Path(__file__).with_name("mt_team_state.sqlite3")
SAVE_FIELDS = ("points", "investigated_clues", "final_submission_open", "final_submitted", "final_answers", "stage")

def default_team_data():
    return {"points": INITIAL_POINTS, "investigated_clues": [], "final_submission_open": False,
            "final_submitted": False, "final_answers": {"culprit":"", "weapon":"", "motive":""}, "stage":1}

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
        return rows[0]["data"] if rows else default_team_data()
    with sqlite3.connect(LOCAL_DB) as conn:
        conn.execute("CREATE TABLE IF NOT EXISTS mt_teams (team_no INTEGER PRIMARY KEY, data TEXT NOT NULL)")
        row = conn.execute("SELECT data FROM mt_teams WHERE team_no=?", (int(team),)).fetchone()
        return json.loads(row[0]) if row else default_team_data()

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
    try:
        write_team_data(team, data)
    except Exception as exc:
        st.error(f"진행 상황 저장 실패: {exc}. 네트워크를 확인하고 다시 시도하세요.")
        st.stop()

def restore_progress(team):
    data = load_team_data(team)
    for field in SAVE_FIELDS:
        st.session_state[field] = set(data.get(field, [])) if field == "investigated_clues" else data.get(field, default_team_data()[field])

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
    "trash": {"name":"물티슈가 들어있는 휴지통", "x":.929,"y":.111,"width":.055,"height":.103,"clue_ids":["bloody_tissue"]},
    "extinguisher": {"name":"소화기", "x":.514,"y":.047,"width":.052,"height":.125,"clue_ids":["extinguisher_dented_base"]},
    "body": {"name":"구성민의 시신", "x":.529,"y":.289,"width":.190,"height":.190,"clue_ids":["time_of_death","wound_report_1","wound_report_2"]},
    "footprint": {"name":"발자국", "x":.701,"y":.512,"width":.069,"height":.257,"clue_ids":["footprint_analysis"]},
    "phone": {"name":"구성민의 휴대전화", "x":.700,"y":.400,"width":.054,"height":.072,"clue_ids":["story_upload","story_viewers"]},
    "wrist": {"name":"구성민의 손목시계", "x":.644,"y":.477,"width":.050,"height":.056,"clue_ids":["stopped_watch"]},
    "case_file": {"name":"책상 위 사건 파일", "x":.277,"y":.282,"width":.070,"height":.080,"clue_ids":["extinguisher_position"]},
    "floor": {"name":"바닥", "x":.590,"y":.712,"width":.100,"height":.096,"clue_ids":["red_paint","short_hair"]},
}

JIAN_ROOM_HOTSPOTS = {
    "jian_bankbook":{"name":"통장","x":.815,"y":.677,"width":.095,"height":.095,"clue_ids":["jian_bank_record"]},
    "jian_phone":{"name":"핸드폰","x":.845,"y":.440,"width":.064,"height":.094,"clue_ids":["jian_dm","jian_event_alibi"]},
    "jian_id":{"name":"주민등록증","x":.076,"y":.114,"width":.064,"height":.063,"clue_ids":["jian_id_card"]},
    "jian_opinion":{"name":"책상 위 소견서","x":.750,"y":.324,"width":.101,"height":.118,"clue_ids":["jian_left_handed"]},
    "jian_prescription":{"name":"처방전","x":.786,"y":.563,"width":.074,"height":.111,"clue_ids":["jian_medicine_record"]},
    "jian_ticket":{"name":"항공권","x":.486,"y":.133,"width":.090,"height":.070,"clue_ids":["jian_thailand_ticket"]},
}

HYEJUN_ROOM_HOTSPOTS = {
    "hyejun_trash":{"name":"쓰레기통","x":.145,"y":.473,"width":.087,"height":.163,"clue_ids":["hyejun_couple_ring"]},
    "hyejun_phone":{"name":"핸드폰","x":.874,"y":.524,"width":.072,"height":.105,"clue_ids":["hyejun_dm","hyejun_saved_name","hyejun_missed_calls"]},
    "hyejun_letter":{"name":"책상 위 편지","x":.793,"y":.419,"width":.130,"height":.103,"clue_ids":["hyejun_love_letter"]},
    "hyejun_opinion":{"name":"소견서","x":.795,"y":.677,"width":.133,"height":.163,"clue_ids":["hyejun_right_handed"]},
}

PROF_ROOM_HOTSPOTS = {
    "prof_bank":{"name":"통장","x":.361,"y":.474,"width":.092,"height":.088,"clue_ids":["prof_bank_record"]},
    "prof_phone":{"name":"핸드폰","x":.751,"y":.511,"width":.083,"height":.093,"clue_ids":["prof_call_history","prof_eta_post"]},
    "prof_computer":{"name":"컴퓨터","x":.546,"y":.262,"width":.292,"height":.184,"clue_ids":["prof_chat_capture"]},
    "prof_receipt":{"name":"영수증","x":.766,"y":.620,"width":.109,"height":.096,"clue_ids":["prof_dinner_receipt"]},
    "prof_research":{"name":"책상 위 자료","x":.487,"y":.490,"width":.213,"height":.135,"clue_ids":["prof_research_log"]},
}

JINSEO_ROOM_HOTSPOTS = {
    "jinseo_opinion":{"name":"소견서","x":.287,"y":.436,"width":.112,"height":.105,"clue_ids":["jinseo_ambidextrous"]},
    "jinseo_material":{"name":"책상 위 자료","x":.077,"y":.547,"width":.162,"height":.137,"clue_ids":["jinseo_anatomy_material","jinseo_childhood_record"]},
    "jinseo_diary":{"name":"일기장","x":.278,"y":.539,"width":.099,"height":.088,"clue_ids":["jinseo_diary_1","jinseo_diary_2"]},
    "jinseo_computer":{"name":"컴퓨터","x":.150,"y":.325,"width":.092,"height":.145,"clue_ids":["jinseo_discovery_record"]},
    "jinseo_diagnosis":{"name":"진단서","x":.104,"y":.707,"width":.144,"height":.166,"clue_ids":["jinseo_medical_record"]},
}

GEONTAE_ROOM_HOTSPOTS = {
    "geontae_news":{"name":"신문","x":.349,"y":.610,"width":.165,"height":.128,"clue_ids":["geontae_aunt_article"]},
    "geontae_phone":{"name":"핸드폰","x":.519,"y":.674,"width":.082,"height":.114,"clue_ids":["geontae_lure_chat","geontae_extinguisher_search"]},
    "geontae_opinion":{"name":"소견서","x":.667,"y":.272,"width":.123,"height":.101,"clue_ids":["geontae_right_handed"]},
    "geontae_school":{"name":"책장의 학교폭력 조치결과 통지서","x":.881,"y":.206,"width":.119,"height":.192,"clue_ids":["geontae_school_record"]},
    "geontae_scrapbook":{"name":"스크랩북","x":.597,"y":.711,"width":.130,"height":.156,"clue_ids":["geontae_scrapbook"]},
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
    "extinguisher_dented_base": {
        "menu_name": '미확인 자료 01',
        "name": '증거 자료 01',
        "cost": 10,
        "location": "사건 현장 - 과방",
        "source": "소화기",
        "result": [],
        "image": find_clue_image("과방 단서 이미지", "fire_extinguisher_dented_base"),
    },
    "wound_report_1": {
        "menu_name": '미확인 자료 02',
        "name": '증거 자료 02',
        "cost": 10,
        "location": "사건 현장 - 과방",
        "source": "구성민의 시신",
        "result": [
            "둔기에 의한 타격으로 추정된다.",
        ],
        "image": find_clue_image('과방 단서 이미지', 'wound_report_1'),
    },
    "wound_report_2": {
        "menu_name": '미확인 자료 03',
        "name": '증거 자료 03',
        "cost": 10,
        "location": "사건 현장 - 과방",
        "source": "구성민의 시신",
        "result": [
            "상흔의 방향을 통해 공격자의 주손을 추리할 수 있다.",
        ],
        "image": find_clue_image('과방 단서 이미지', 'wound_report_2'),
    },
    "time_of_death": {
        "menu_name": '미확인 자료 04',
        "name": '증거 자료 04',
        "cost": 10,
        "location": "사건 현장 - 과방",
        "source": "구성민의 시신",
        "result": [
            "사망 시각과 관련된 감식 결과를 확인할 수 있다.",
        ],
        "image": find_clue_image('과방 단서 이미지', 'time_of_death_report'),
    },
    "stopped_watch": {
        "menu_name": '미확인 자료 05',
        "name": '증거 자료 05',
        "cost": 10,
        "location": "사건 현장 - 과방",
        "source": "구성민의 손목",
        "result": [
            "충격으로 멈춘 것으로 보이는 손목시계를 발견했다.",
            "표시된 시각은 사망 시각 추리에 활용할 수 있다.",
        ],
        "image": find_clue_image('과방 단서 이미지', 'stopped_watch_1718'),
    },
    "red_paint": {
        "menu_name": '미확인 자료 06',
        "name": '증거 자료 06',
        "cost": 10,
        "location": "사건 현장 - 과방",
        "source": "바닥",
        "result": [
            "바닥에서 붉은색 도료 조각을 발견했다.",
        ],
        "image": find_clue_image('과방 단서 이미지', 'red_paint_analysis'),
    },
    "short_hair": {
        "menu_name": '미확인 자료 07',
        "name": '증거 자료 07',
        "cost": 10,
        "location": "사건 현장 - 과방",
        "source": "바닥",
        "result": [
            "바닥에서 짧은 머리카락을 발견했다.",
        ],
        "image": find_clue_image('과방 단서 이미지', 'short_hair_evidence'),
    },
    "footprint_analysis": {
        "menu_name": '미확인 자료 08',
        "name": '증거 자료 08',
        "cost": 10,
        "location": "사건 현장 - 과방",
        "source": "신발 자국",
        "result": [
            "감식 결과 약 270mm 크기의 신발에서 남은 것으로 추정된다.",
        ],
        "image": find_clue_image('과방 단서 이미지', 'shoeprint_analysis'),
    },
    "extinguisher_position": {
        "menu_name": '미확인 자료 09',
        "name": '증거 자료 09',
        "cost": 10,
        "location": "사건 현장 - 과방",
        "source": "책상 위 사건 파일",
        "result": [
            "평소 소화기 보관 상태와 사건 발생 후 상태를 비교한 결과 소화기의 위치가 달라져 있다.",
        ],
        "image": find_clue_image('과방 단서 이미지', 'fire_extinguisher_before_after'),
    },
    "story_upload": {
        "menu_name": '미확인 자료 10',
        "name": '증거 자료 10',
        "cost": 10,
        "location": "사건 현장 - 과방",
        "source": "구성민의 휴대전화",
        "result": [
            "구성민이 16:00에 SNS 스토리를 업로드한 기록을 확인했다.",
        ],
        "image": find_clue_image('과방 단서 이미지', 'seongmin_instagram_story'),
    },
    "story_viewers": {
        "menu_name": '미확인 자료 11',
        "name": '증거 자료 11',
        "cost": 10,
        "location": "사건 현장 - 과방",
        "source": "구성민의 휴대전화",
        "result": [
            "구성민의 스토리를 확인한 계정 목록을 확인할 수 있다.",
        ],
        "image": find_clue_image('과방 단서 이미지', 'seongmin_story_viewers'),
    },
    "bloody_tissue": {
        "menu_name": '미확인 자료 12',
        "name": '증거 자료 12',
        "cost": 10,
        "location": "사건 현장 - 과방",
        "source": "피 묻은 물티슈",
        "result": [
            "피가 묻어 있지만 화장품이 묻어난 흔적은 확인되지 않는다.",
        ],
        "image": find_clue_image('과방 단서 이미지', 'bloody_wet_wipe'),
    },

    "jian_medicine_record": {
        "menu_name": '미확인 자료 01',
        "name": '증거 자료 01',
        "cost": 10,
        "location": "이지안의 방",
        "source": "처방약 봉투",
        "result": [
            "에스트라디올데포와 관련된 처방 기록을 확인했다.",
            "사건과 직접적인 연관성은 현재로서는 확인되지 않는다.",
        ],
        "image": find_clue_image('이지안 단서 이미지', 'jian_prescription'),
    },
    "jian_bank_record": {
        "menu_name": '미확인 자료 02',
        "name": '증거 자료 02',
        "cost": 10,
        "location": "이지안의 방",
        "source": "통장",
        "result": [
            "최근 입출금 내역에서 평소보다 눈에 띄는 거래 기록을 확인했다.",
            "거래의 의미는 다른 단서와 함께 판단할 필요가 있다.",
        ],
        "image": find_clue_image('이지안 단서 이미지', 'jian_bank_record'),
    },
    "jian_thailand_ticket": {
        "menu_name": '미확인 자료 03',
        "name": '증거 자료 03',
        "cost": 10,
        "location": "이지안의 방",
        "source": "비행기표",
        "result": [
            "이지안 명의의 태국행 항공권 예약 자료를 확인했다.",
        ],
        "image": find_clue_image('이지안 단서 이미지', 'jian_thailand_ticket'),
    },
    "jian_dm": {
        "menu_name": '미확인 자료 04',
        "name": '증거 자료 04',
        "cost": 10,
        "location": "이지안의 방",
        "source": "휴대전화",
        "result": [
            "휴대전화에서 구성민과 관련된 DM 기록을 확인했다.",
            "구성민과 주고받은 메시지 내용을 확인할 수 있다.",
        ],
        "image": find_clue_image('이지안 단서 이미지', 'jian_dm'),
    },
    "jian_event_alibi": {
        "menu_name": '미확인 자료 05',
        "name": '증거 자료 05',
        "cost": 10,
        "location": "이지안의 방",
        "source": "노트북",
        "result": [
            "17:30경 잠실에서 열린 행사에 이지안이 참석한 정황을 확인했다.",
            "주최 측 촬영 자료에서 같은 시각 이지안의 모습을 확인할 수 있다.",
        ],
        "image": find_clue_image('이지안 단서 이미지', 'jian_event_alibi'),
    },
    "jian_left_handed": {
        "menu_name": '미확인 자료 06',
        "name": '증거 자료 06',
        "cost": 10,
        "location": "이지안의 방",
        "source": "책상 위 필기 기록",
        "result": [
            "필기 습관과 개인 기록을 통해 이지안이 왼손잡이임을 확인할 수 있다.",
        ],
        "image": find_clue_image('이지안 단서 이미지', 'jian_left_handed'),
    },


    "hyejun_dm": {
        "menu_name": '미확인 자료 01',
        "name": '증거 자료 01',
        "cost": 10,
        "location": "전혜준의 방",
        "source": "휴대전화",
        "result": [
            "구성민에게 집착하는 듯한 내용의 DM 기록을 확인했다.",
            "두 사람의 관계가 평범하지 않았음을 짐작할 수 있다.",
        ],
        "image": find_clue_image('전혜준 단서 이미지', 'hyejun_dm'),
    },
    "hyejun_saved_name": {
        "menu_name": '미확인 자료 02',
        "name": '증거 자료 02',
        "cost": 10,
        "location": "전혜준의 방",
        "source": "휴대전화",
        "result": [
            "구성민의 연락처가 '성민이형♥'으로 저장되어 있다.",
        ],
        "image": find_clue_image('전혜준 단서 이미지', 'hyejun_saved_name'),
    },
    "hyejun_missed_calls": {
        "menu_name": '미확인 자료 03',
        "name": '증거 자료 03',
        "cost": 10,
        "location": "전혜준의 방",
        "source": "휴대전화",
        "result": [
            "16:30부터 17:30 사이 구성민에게 반복적으로 전화를 건 기록을 확인했다.",
            "총 170회의 부재중 전화가 남아 있다.",
        ],
        "image": find_clue_image('전혜준 단서 이미지', 'hyejun_missed_calls'),
    },
    "hyejun_couple_ring": {
        "menu_name": '미확인 자료 04',
        "name": '증거 자료 04',
        "cost": 10,
        "location": "전혜준의 방",
        "source": "쓰레기통",
        "result": [
            "쓰레기통 안에서 버려진 커플링을 발견했다.",
        ],
        "image": find_clue_image('전혜준 단서 이미지', 'hyejun_couple_ring'),
    },
    "hyejun_love_letter": {
        "menu_name": '미확인 자료 05',
        "name": '증거 자료 05',
        "cost": 10,
        "location": "전혜준의 방",
        "source": "열린 서랍",
        "result": [
            "서랍 안에서 구성민을 향해 작성한 것으로 보이는 러브레터를 발견했다.",
        ],
        "image": find_clue_image('전혜준 단서 이미지', 'hyejun_love_letter'),
    },
    "hyejun_right_handed": {
        "menu_name": '미확인 자료 06',
        "name": '증거 자료 06',
        "cost": 10,
        "location": "전혜준의 방",
        "source": "노트와 필기구",
        "result": [
            "필기 습관과 개인 기록을 통해 전혜준이 오른손잡이임을 확인할 수 있다.",
        ],
        "image": find_clue_image('전혜준 단서 이미지', 'hyejun_right_handed'),
    },

    "prof_eta_post": {
        "menu_name": '미확인 자료 01',
        "name": '증거 자료 01',
        "cost": 10,
        "location": "변상균 교수 연구실",
        "source": "노트북",
        "result": [
            "변상균 교수가 작성한 것으로 보이는 에브리타임 게시글을 확인했다.",
            "연구 성과 관련 뉴스를 두고 불쾌감을 드러낸 내용이 담겨 있다.",
        ],
        "image": find_clue_image('변상균 교수 단서 이미지', 'prof_eta_post'),
    },
    "prof_chat_capture": {
        "menu_name": '미확인 자료 02',
        "name": '증거 자료 02',
        "cost": 10,
        "location": "변상균 교수 연구실",
        "source": "휴대전화",
        "result": [
            "구성민과 고려대 교수 사이의 대화 캡처를 확인했다.",
            "연구 자료와 성과를 둘러싼 은어성 표현이 포함되어 있다.",
        ],
        "image": find_clue_image('변상균 교수 단서 이미지', 'prof_chat_capture'),
    },
    "prof_research_log": {
        "menu_name": '미확인 자료 03',
        "name": '증거 자료 03',
        "cost": 10,
        "location": "변상균 교수 연구실",
        "source": "연구 자료 더미",
        "result": [
            "연구 진행 상황과 구성민에 대한 불만이 기록된 연구일지를 확인했다.",
            "최근 연구 성과 문제로 두 사람 사이에 갈등이 있었던 정황이 보인다.",
        ],
        "image": find_clue_image('변상균 교수 단서 이미지', 'prof_research_log'),
    },
    "prof_bank_record": {
        "menu_name": '미확인 자료 04',
        "name": '증거 자료 04',
        "cost": 10,
        "location": "변상균 교수 연구실",
        "source": "서랍장",
        "result": [
            "최근 입출금 내역을 확인했다.",
            "일부 거래가 눈에 띄지만 사건과의 직접적인 관련성은 다른 단서와 함께 판단해야 한다.",
        ],
        "image": find_clue_image('변상균 교수 단서 이미지', 'prof_bank_record'),
    },
    "prof_dinner_receipt": {
        "menu_name": '미확인 자료 05',
        "name": '증거 자료 05',
        "cost": 10,
        "location": "변상균 교수 연구실",
        "source": "원형 테이블 위 개인 자료",
        "result": [
            "17:13에 연구실 조교들과 함께 저녁 식사를 하며 결제한 기록을 확인했다.",
            "사망 추정 시각과 비교하면 변상균 교수의 행적을 판단하는 데 중요한 자료가 된다.",
        ],
        "image": find_clue_image('변상균 교수 단서 이미지', 'prof_dinner_receipt'),
    },


    "jinseo_anatomy_material": {
        "menu_name": '미확인 자료 01',
        "name": '증거 자료 01',
        "cost": 10,
        "location": "박진서의 방",
        "source": "침대 위 검은 자료",
        "result": [
            "박진서가 소지한 인체해부학 관련 자료를 확인했다.",
            "인체 구조와 손상에 관한 내용이 포함되어 있다.",
        ],
        "image": find_clue_image('박진서 단서 이미지', 'jinseo_anatomy'),
    },
    "jinseo_diary_1": {
        "menu_name": '미확인 자료 02',
        "name": '증거 자료 02',
        "cost": 10,
        "location": "박진서의 방",
        "source": "책상 위 필기 자료",
        "result": [
            "구성민을 대상으로 한 살해 계획처럼 보이는 내용이 적혀 있다.",
            "구체적인 상황을 가정한 문장들이 있어 박진서를 강하게 의심하게 만드는 자료다.",
        ],
        "image": find_clue_image('박진서 단서 이미지', 'jinseo_diary1'),
    },
    "jinseo_diary_2": {
        "menu_name": '미확인 자료 03',
        "name": '증거 자료 03',
        "cost": 10,
        "location": "박진서의 방",
        "source": "책상 위 필기 자료",
        "result": [
            "이후 작성된 기록에서 '결국 못 죽였다'는 취지의 내용을 확인했다.",
            "앞서 발견한 계획이 실제 범행으로 이어졌는지는 다시 판단할 필요가 있다.",
        ],
        "image": find_clue_image('박진서 단서 이미지', 'jinseo_diary2'),
    },
    "jinseo_discovery_record": {
        "menu_name": '미확인 자료 04',
        "name": '증거 자료 04',
        "cost": 10,
        "location": "박진서의 방",
        "source": "휴대전화",
        "result": [
            "18:30경 박진서가 구성민의 시신을 발견한 뒤 신고한 기록을 확인했다.",
            "박진서가 시신의 최초 발견자였다는 사실을 확인할 수 있다.",
        ],
        "image": find_clue_image('박진서 단서 이미지', 'jinseo_discovery'),
    },
    "jinseo_ambidextrous": {
        "menu_name": '미확인 자료 05',
        "name": '증거 자료 05',
        "cost": 10,
        "location": "박진서의 방",
        "source": "중앙 테이블의 책",
        "result": [
            "개인 기록과 필기 흔적을 통해 박진서가 양손을 모두 사용하는 정황을 확인했다.",
        ],
        "image": find_clue_image('박진서 단서 이미지', 'jinseo_ambidextrous'),
    },


    "geontae_aunt_article": {
        "menu_name": '미확인 자료 01',
        "name": '증거 자료 01',
        "cost": 10,
        "location": "고건태의 방",
        "source": "책장과 파일",
        "result": [
            "고건태의 가족과 관련된 과거 자살 사건 기사를 보관하고 있는 것을 확인했다.",
            "해당 사건이 고건태에게 오래 남아 있는 것으로 보인다.",
        ],
        "image": find_clue_image('고건태 단서 이미지', 'geontae_brother_news'),
    },
    "geontae_scrapbook": {
        "menu_name": '미확인 자료 02',
        "name": '증거 자료 02',
        "cost": 10,
        "location": "고건태의 방",
        "source": "중앙 테이블 자료",
        "result": [
            "구성민과 관련된 기사와 기록을 장기간 모아 둔 스크랩 자료를 확인했다.",
            "일부 메모에는 구성민에 대한 강한 감정이 드러나 있다.",
        ],
        "image": find_clue_image('고건태 단서 이미지', 'geontae_scrapbook'),
    },
    "geontae_right_handed": {
        "menu_name": '미확인 자료 03',
        "name": '증거 자료 03',
        "cost": 10,
        "location": "고건태의 방",
        "source": "책상 위 필기 자료",
        "result": [
            "필기 흔적과 물품 사용 습관을 통해 고건태가 오른손잡이임을 확인할 수 있다.",
        ],
        "image": find_clue_image('고건태 단서 이미지', 'geontae_right_handed'),
    },
    "geontae_school_record": {
        "menu_name": '미확인 자료 04',
        "name": '증거 자료 04',
        "cost": 10,
        "location": "고건태의 방",
        "source": "책장과 파일",
        "result": [
            "구성민의 과거 학교생활 관련 기록 사본을 보관하고 있는 것을 확인했다.",
            "기록에는 경미한 처벌 이력이 포함되어 있다.",
        ],
        "image": find_clue_image('고건태 단서 이미지', 'geontae_school_record'),
    },


    "geontae_lure_chat": {
        "menu_name": '미확인 자료 05',
        "name": '증거 자료 05',
        "cost": 10,
        "location": "고건태의 방",
        "source": "휴대전화",
        "result": [
            "컴퓨터에 백업된 메신저 기록에서 고건태가 구성민에게 과방에서 만나자고 유도한 대화를 확인했다.",
            "대화 시각은 사건 발생 직전의 시간대와 겹친다.",
        ],
        "image": find_clue_image('고건태 단서 이미지', 'geontae_chat'),
    },
    "geontae_extinguisher_search": {
        "menu_name": '미확인 자료 06',
        "name": '증거 자료 06',
        "cost": 10,
        "location": "고건태의 방",
        "source": "필기 노트",
        "result": [
            "브라우저 기록에서 소화기를 이용해 사람에게 치명상을 입힐 수 있는지에 관한 검색 흔적을 확인했다.",
            "검색 시각은 사건 발생 이전이다.",
        ],
        "image": find_clue_image('고건태 단서 이미지', 'geontae_search_history'),
    },


    "jian_id_card": {
        "menu_name": '미확인 자료 07', "name": '증거 자료 07', "cost": 10,
        "location": "이지안의 방", "source": "개인 서류",
        "result": ["이지안의 신분증을 확인했다."],
        "image": find_clue_image("이지안 단서 이미지", "jian_id_card"),
    },
    "prof_call_history": {
        "menu_name": '미확인 자료 06', "name": '증거 자료 06', "cost": 10,
        "location": "변상균 교수 연구실", "source": "휴대전화",
        "result": ["구성민과 관련된 통화 기록을 확인했다."],
        "image": find_clue_image("변상균 교수 단서 이미지", "prof_call_history"),
    },
    "jinseo_childhood_record": {
        "menu_name": '미확인 자료 06', "name": '증거 자료 06', "cost": 10,
        "location": "박진서의 방", "source": "개인 서류",
        "result": ["박진서의 어린 시절 기록을 확인했다."],
        "image": find_clue_image("박진서 단서 이미지", "jinseo_childhood_record"),
    },
    "jinseo_medical_record": {
        "menu_name": '미확인 자료 07', "name": '증거 자료 07', "cost": 10,
        "location": "박진서의 방", "source": "개인 서류",
        "result": ["박진서의 진료 기록을 확인했다."],
        "image": find_clue_image("박진서 단서 이미지", "jinseo_medical_record"),
    },
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
    "final_answers": {
        "culprit": "",
        "weapon": "",
        "motive": "",
    },
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
    if stage == 2:
        return location_key != "사건 현장"
    return True


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
    st.session_state.points = INITIAL_POINTS
    st.session_state.investigated_clues = set()
    st.session_state.final_submission_open = False
    st.session_state.final_submitted = False
    st.session_state.final_answers = {
        "culprit": "",
        "weapon": "",
        "motive": "",
    }
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
        team_pw = st.text_input("조별 관리자 비밀번호", type="password", key="team_login_pw")
        if st.button("담당 조 입장", use_container_width=True):
            if team_pw == ADMIN_PASSWORD:
                try:
                    restore_progress(team_input)
                    st.session_state.team_no = team_input
                    st.session_state.admin_ok = True
                    st.rerun()
                except Exception as exc:
                    st.error(f"조별 데이터 연결 실패: {exc}")
            else:
                st.error("관리자 비밀번호가 틀렸습니다.")
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

    if not st.session_state.admin_ok:
        pw = st.text_input("관리자 비밀번호", type="password")
        if st.button("관리자 로그인"):
            if pw == ADMIN_PASSWORD:
                st.session_state.admin_ok = True
                st.rerun()
            else:
                st.error("비밀번호가 틀렸습니다.")
    else:
        st.success("관리자 로그인 상태")

        new_stage = st.radio(
            "조사 단계 변경",
            options=[1, 2, 3],
            index=st.session_state.stage - 1,
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

        with st.form("custom_points_form"):
            amount = st.number_input("직접 지급할 포인트", min_value=1, max_value=10000, value=50, step=10)
            if st.form_submit_button("입력한 포인트 지급", use_container_width=True):
                st.session_state.points += int(amount)
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
                st.write("**범인 및 근거**")
                st.write(st.session_state.final_answers["culprit"])
                st.write("**살해 도구 및 근거**")
                st.write(st.session_state.final_answers["weapon"])
                st.write("**살해 동기 및 사건 흐름**")
                st.write(st.session_state.final_answers["motive"])

            if st.button("현재 팀 제출 초기화", use_container_width=True):
                st.session_state.final_submitted = False
                save_progress()
                st.session_state.final_answers = {
                    "culprit": "",
                    "weapon": "",
                    "motive": "",
                }
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
    st.info("왼쪽 사이드바에서 담당 조를 선택하고 관리자 비밀번호로 입장해주세요.")
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
    show_optional_image(clue.get("image"))

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
        st.error(f"이미지를 찾을 수 없습니다: {CRIME_SCENE_IMAGE_PATH}")
        st.stop()

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
        st.error(f"이미지를 찾을 수 없습니다: {JIAN_ROOM_IMAGE_PATH}")
        st.info("images 폴더 안에 파일명이 정확히 jian_room.png인지 확인해주세요.")
        st.stop()

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
        st.error(f"이미지를 찾을 수 없습니다: {HYEJUN_ROOM_IMAGE_PATH}")
        st.info("images 폴더 안에 파일명이 정확히 hyejun_room.png인지 확인해주세요.")
        st.stop()

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
        st.error(f"이미지를 찾을 수 없습니다: {PROF_ROOM_IMAGE_PATH}")
        st.info("images 폴더 안에 파일명이 정확히 prof_room.png인지 확인해주세요.")
        st.stop()

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
        st.error(f"이미지를 찾을 수 없습니다: {JINSEO_ROOM_IMAGE_PATH}")
        st.info("images 폴더 안에 파일명이 정확히 jinseo_room.png인지 확인해주세요.")
        st.stop()

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
        st.error(f"이미지를 찾을 수 없습니다: {GEONTAE_ROOM_IMAGE_PATH}")
        st.info("images 폴더 안에 파일명이 정확히 gt_room.png인지 확인해주세요.")
        st.stop()

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
                    show_optional_image(clue.get("image"))
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
    st.caption(f"{st.session_state.team_no}팀")

    if st.session_state.final_submitted:
        st.success("최종 추리가 제출되었습니다. 제출 후에는 수정할 수 없습니다.")

        with st.container(border=True):
            st.subheader("1. 범인 및 근거")
            st.write(st.session_state.final_answers["culprit"])

        with st.container(border=True):
            st.subheader("2. 살해 도구 및 근거")
            st.write(st.session_state.final_answers["weapon"])

        with st.container(border=True):
            st.subheader("3. 살해 동기 및 사건 흐름")
            st.write(st.session_state.final_answers["motive"])

        if st.button("⬅ 메인 화면으로 돌아가기", use_container_width=True):
            clear_transient_states()
            st.session_state.current_view = None
            st.rerun()
        return

    if not st.session_state.final_submission_open:
        st.warning("아직 최종 추리 제출 시간이 아닙니다.")
        if st.button("⬅ 메인 화면으로 돌아가기", use_container_width=True):
            clear_transient_states()
            st.session_state.current_view = None
            st.rerun()
        return

    st.info(
        "단순히 정답만 적기보다 조사에서 확보한 단서를 근거로 작성해주세요. "
        "제출 후에는 참가자가 직접 수정할 수 없습니다."
    )

    with st.form("final_submission_form"):
        culprit = st.text_area(
            "1. 범인은 누구라고 생각하는가? 그 이유와 근거 단서를 함께 작성하세요.",
            height=150,
            placeholder="예: ○○가 범인이라고 생각한다. 그 이유는 ...",
        )

        weapon = st.text_area(
            "2. 살해 도구는 무엇이라고 생각하는가? 어떤 단서로 판단했는지 작성하세요.",
            height=150,
            placeholder="예: 살해 도구는 ○○라고 생각한다. 현장에서 ...",
        )

        motive = st.text_area(
            "3. 살해 동기는 무엇이라고 생각하는가? 사건의 흐름과 함께 설명하세요.",
            height=190,
            placeholder="예: ○○ 사건을 계기로 ...",
        )

        submitted = st.form_submit_button(
            "최종 추리 제출",
            type="primary",
            use_container_width=True,
        )

    if submitted:
        if not culprit.strip() or not weapon.strip() or not motive.strip():
            st.error("세 항목을 모두 작성한 뒤 제출해주세요.")
        else:
            st.session_state.final_answers = {
                "culprit": culprit.strip(),
                "weapon": weapon.strip(),
                "motive": motive.strip(),
            }
            st.session_state.final_submitted = True
            save_progress()
            st.rerun()

    if st.button("⬅ 메인 화면으로 돌아가기", use_container_width=True):
        clear_transient_states()
        st.session_state.current_view = None
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
