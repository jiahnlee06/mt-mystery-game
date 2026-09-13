import os

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

ADMIN_PASSWORD = "mt1234"
INITIAL_POINTS = 100
CRIME_SCENE_IMAGE_PATH = "images/crime_scene.png"
JIAN_ROOM_IMAGE_PATH = "images/jian_room.png"


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
CRIME_SCENE_HOTSPOTS = {
    "body": {
        "name": "구성민의 시신",
        "x": 0.52,
        "y": 0.28,
        "width": 0.17,
        "height": 0.34,
        "clue_ids": [
            "wound_report_1",
            "wound_report_2",
            "time_of_death",
        ],
    },
    "wrist": {
        "name": "구성민의 손목",
        "x": 0.65,
        "y": 0.43,
        "width": 0.06,
        "height": 0.08,
        "clue_ids": ["stopped_watch"],
    },
    "floor": {
        "name": "바닥",
        "x": 0.60,
        "y": 0.70,
        "width": 0.09,
        "height": 0.10,
        "clue_ids": [
            "red_paint",
            "short_hair",
        ],
    },
    "footprint": {
        "name": "신발 자국",
        "x": 0.67,
        "y": 0.49,
        "width": 0.11,
        "height": 0.25,
        "clue_ids": ["footprint_analysis"],
    },
    "extinguisher": {
        "name": "소화기",
        "x": 0.52,
        "y": 0.04,
        "width": 0.06,
        "height": 0.13,
        "clue_ids": ["extinguisher_bottom"],
    },
    "extinguisher_case": {
        "name": "소화기 보관함",
        "x": 0.57,
        "y": 0.01,
        "width": 0.10,
        "height": 0.16,
        "clue_ids": ["extinguisher_position"],
    },
    "phone": {
        "name": "구성민의 휴대전화",
        "x": 0.69,
        "y": 0.39,
        "width": 0.06,
        "height": 0.08,
        "clue_ids": [
            "story_upload",
            "story_viewers",
        ],
    },
    "tissue": {
        "name": "피 묻은 물티슈",
        "x": 0.75,
        "y": 0.63,
        "width": 0.07,
        "height": 0.09,
        "clue_ids": ["bloody_tissue"],
    },
    "door": {
        "name": "과방 출입문 / 키 보관함",
        "x": 0.71,
        "y": 0.00,
        "width": 0.23,
        "height": 0.15,
        "clue_ids": ["key_return_log"],
    },
}


# ─────────────────────────────────────
# 이지안의 방 hotspot
# 방금 만든 jian_room.png 기준 비율 좌표입니다.
# 관리자 디버그 모드에서 빨간 상자를 켜고 실제 위치를 확인할 수 있습니다.
# ─────────────────────────────────────
JIAN_ROOM_HOTSPOTS = {
    # 아래 좌표는 사용자가 디버그 모드에서 실측한 물체 중심(center)을 기준으로
    # x = center_x - width/2, y = center_y - height/2 로 계산했습니다.
    # medicine center ≈ (0.365, 0.253) / bankbook ≈ (0.474, 0.335)
    # ticket ≈ (0.550, 0.300) / phone ≈ (0.620, 0.249)
    # laptop ≈ (0.489, 0.090) / notebook ≈ (0.481, 0.810)
    "jian_medicine": {
        "name": "처방약 봉투",
        "x": 0.328, "y": 0.206, "width": 0.075, "height": 0.095,
        "clue_ids": ["jian_medicine_record"],
    },
    "jian_bankbook": {
        "name": "통장",
        "x": 0.439, "y": 0.293, "width": 0.070, "height": 0.085,
        "clue_ids": ["jian_bank_record"],
    },
    "jian_ticket": {
        "name": "비행기표",
        "x": 0.515, "y": 0.258, "width": 0.070, "height": 0.085,
        "clue_ids": ["jian_thailand_ticket"],
    },
    "jian_phone": {
        "name": "휴대전화",
        "x": 0.588, "y": 0.197, "width": 0.065, "height": 0.105,
        "clue_ids": ["jian_dm"],
    },
    "jian_laptop": {
        "name": "노트북",
        "x": 0.429, "y": 0.025, "width": 0.120, "height": 0.130,
        "clue_ids": ["jian_event_alibi"],
    },
    "jian_notebook": {
        "name": "노트",
        "x": 0.434, "y": 0.753, "width": 0.095, "height": 0.115,
        "clue_ids": ["jian_left_handed"],
    },
}

# ─────────────────────────────────────
# 실제로 포인트를 사용해 얻는 단서
# image에 파일 경로를 넣으면 결과 화면에서 자동 표시됩니다.
# 예: "images/clues/wound_report_1.png"
# ─────────────────────────────────────
CLUES = {
    "wound_report_1": {
        "menu_name": "외상 정밀 조사 A",
        "name": "상흔 소견서 1",
        "cost": 15,
        "location": "사건 현장 - 과방",
        "source": "구성민의 시신",
        "result": [
            "둔기에 의한 타격으로 추정된다.",
        ],
        "image": None,
    },
    "wound_report_2": {
        "menu_name": "외상 정밀 조사 B",
        "name": "상흔 소견서 2",
        "cost": 15,
        "location": "사건 현장 - 과방",
        "source": "구성민의 시신",
        "result": [
            "상흔의 방향을 통해 공격자의 주손을 추리할 수 있다.",
        ],
        "image": None,
    },
    "time_of_death": {
        "menu_name": "법의학적 감식",
        "name": "사망 시각 소견",
        "cost": 10,
        "location": "사건 현장 - 과방",
        "source": "구성민의 시신",
        "result": [
            "사망 시각과 관련된 감식 결과를 확인할 수 있다.",
        ],
        "image": None,
    },
    "stopped_watch": {
        "menu_name": "손목 주변 조사",
        "name": "멈춘 손목시계",
        "cost": 10,
        "location": "사건 현장 - 과방",
        "source": "구성민의 손목",
        "result": [
            "충격으로 멈춘 것으로 보이는 손목시계를 발견했다.",
            "표시된 시각은 사망 시각 추리에 활용할 수 있다.",
        ],
        "image": None,
    },
    "red_paint": {
        "menu_name": "바닥 흔적 조사 A",
        "name": "붉은 도료 조각",
        "cost": 10,
        "location": "사건 현장 - 과방",
        "source": "바닥",
        "result": [
            "바닥에서 붉은색 도료 조각을 발견했다.",
        ],
        "image": None,
    },
    "short_hair": {
        "menu_name": "바닥 흔적 조사 B",
        "name": "짧은 머리카락",
        "cost": 10,
        "location": "사건 현장 - 과방",
        "source": "바닥",
        "result": [
            "바닥에서 짧은 머리카락을 발견했다.",
        ],
        "image": None,
    },
    "footprint_analysis": {
        "menu_name": "바닥 흔적 감식",
        "name": "신발 자국 감식",
        "cost": 20,
        "location": "사건 현장 - 과방",
        "source": "신발 자국",
        "result": [
            "감식 결과 약 270mm 크기의 신발에서 남은 것으로 추정된다.",
        ],
        "image": None,
    },
    "extinguisher_bottom": {
        "menu_name": "소화기 정밀 조사",
        "name": "소화기 바닥 정밀 조사",
        "cost": 20,
        "location": "사건 현장 - 과방",
        "source": "소화기",
        "result": [
            "소화기 바닥 부분에서 도료가 벗겨진 흔적을 발견했다.",
        ],
        "image": None,
    },
    "extinguisher_position": {
        "menu_name": "보관 상태 조사",
        "name": "소화기 보관 상태 비교",
        "cost": 10,
        "location": "사건 현장 - 과방",
        "source": "소화기 보관함",
        "result": [
            "평소 소화기 보관 상태와 사건 발생 후 상태를 비교한 결과 소화기의 위치가 달라져 있다.",
        ],
        "image": None,
    },
    "story_upload": {
        "menu_name": "휴대전화 기록 조사 A",
        "name": "SNS 스토리 업로드 기록",
        "cost": 10,
        "location": "사건 현장 - 과방",
        "source": "구성민의 휴대전화",
        "result": [
            "구성민이 16:00에 SNS 스토리를 업로드한 기록을 확인했다.",
        ],
        "image": None,
    },
    "story_viewers": {
        "menu_name": "휴대전화 기록 조사 B",
        "name": "스토리 확인 목록",
        "cost": 10,
        "location": "사건 현장 - 과방",
        "source": "구성민의 휴대전화",
        "result": [
            "구성민의 스토리를 확인한 계정 목록을 확인할 수 있다.",
        ],
        "image": None,
    },
    "bloody_tissue": {
        "menu_name": "물티슈 정밀 조사",
        "name": "물티슈 감식",
        "cost": 10,
        "location": "사건 현장 - 과방",
        "source": "피 묻은 물티슈",
        "result": [
            "피가 묻어 있지만 화장품이 묻어난 흔적은 확인되지 않는다.",
        ],
        "image": None,
    },
    "key_return_log": {
        "menu_name": "출입 기록 조사",
        "name": "키 반납 기록",
        "cost": 10,
        "location": "사건 현장 - 과방",
        "source": "과방 출입문 / 키 보관함",
        "result": [
            "과방 키 반납 기록을 확인할 수 있다.",
        ],
        "image": None,
    },

    "jian_medicine_record": {
        "menu_name": "처방약 봉투 조사",
        "name": "처방약 기록",
        "cost": 10,
        "location": "이지안의 방",
        "source": "처방약 봉투",
        "result": [
            "에스트라디올데포와 관련된 처방 기록을 확인했다.",
            "사건과 직접적인 연관성은 현재로서는 확인되지 않는다.",
        ],
        "image": None,
    },
    "jian_bank_record": {
        "menu_name": "통장 내역 확인",
        "name": "입출금 기록",
        "cost": 10,
        "location": "이지안의 방",
        "source": "통장",
        "result": [
            "최근 입출금 내역에서 평소보다 눈에 띄는 거래 기록을 확인했다.",
            "거래의 의미는 다른 단서와 함께 판단할 필요가 있다.",
        ],
        "image": None,
    },
    "jian_thailand_ticket": {
        "menu_name": "항공권 확인",
        "name": "태국행 항공권",
        "cost": 10,
        "location": "이지안의 방",
        "source": "비행기표",
        "result": [
            "이지안 명의의 태국행 항공권 예약 자료를 확인했다.",
        ],
        "image": None,
    },
    "jian_dm": {
        "menu_name": "휴대전화 메시지 확인",
        "name": "DM 기록",
        "cost": 10,
        "location": "이지안의 방",
        "source": "휴대전화",
        "result": [
            "휴대전화에서 구성민과 관련된 DM 기록을 확인했다.",
            "구성민과 주고받은 메시지 내용을 확인할 수 있다.",
        ],
        "image": None,
    },
    "jian_event_alibi": {
        "menu_name": "노트북 파일 확인",
        "name": "17:30 잠실 행사 기록",
        "cost": 20,
        "location": "이지안의 방",
        "source": "노트북",
        "result": [
            "17:30경 잠실에서 열린 행사에 이지안이 참석한 정황을 확인했다.",
            "주최 측 촬영 자료에서 같은 시각 이지안의 모습을 확인할 수 있다.",
        ],
        "image": None,
    },
    "jian_left_handed": {
        "menu_name": "필기 기록 확인",
        "name": "왼손 사용 정황",
        "cost": 15,
        "location": "이지안의 방",
        "source": "노트와 필기구",
        "result": [
            "필기 습관과 개인 기록을 통해 이지안이 왼손잡이임을 확인할 수 있다.",
        ],
        "image": None,
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
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value.copy() if isinstance(value, set) else value


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


def refresh_image_click_component():
    """이전 이미지 클릭값이 다음 화면에서 재사용되는 것을 막습니다."""
    st.session_state.image_click_nonce += 1
    st.session_state.last_click_xy = None
    st.session_state.last_click_ratio = None


def reset_investigation():
    st.session_state.points = INITIAL_POINTS
    st.session_state.investigated_clues = set()
    clear_transient_states()
    st.session_state.reset_confirm = False


def show_optional_image(path):
    if path and os.path.exists(path):
        st.image(path, use_container_width=True)


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
        draw.text((x0 + 4, y0 + 4), hotspot_id, fill="red")

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
        draw.text((x0 + 4, y0 + 4), hotspot_id, fill="red")

    return image

# ─────────────────────────────────────
# 사이드바
# ─────────────────────────────────────
with st.sidebar:
    st.header("팀 설정")

    if st.session_state.team_no is None:
        team_input = st.text_input("우리 팀 번호를 입력하세요 (예: 1)")
        if st.button("팀 번호 확정"):
            if team_input.strip():
                st.session_state.team_no = team_input.strip()
                st.rerun()
    else:
        st.write(f"현재 팀 번호: **{st.session_state.team_no}**")
        if st.button("팀 번호 다시 설정"):
            st.session_state.team_no = None
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
            clear_transient_states()
            st.rerun()

        st.divider()
        st.subheader("조사 포인트 조정")
        st.write(f"현재 조사 포인트: **{st.session_state.points}P**")

        p1, p2 = st.columns(2)
        with p1:
            if st.button("+10P", use_container_width=True):
                st.session_state.points += 10
                st.rerun()
            if st.button("+30P", use_container_width=True):
                st.session_state.points += 30
                st.rerun()

        with p2:
            if st.button("+20P", use_container_width=True):
                st.session_state.points += 20
                st.rerun()
            if st.button("-10P", use_container_width=True):
                st.session_state.points = max(0, st.session_state.points - 10)
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
    st.info("왼쪽 사이드바에서 먼저 팀 번호를 입력해주세요.")
    st.stop()


# ─────────────────────────────────────
# 단서 결과 화면
# ─────────────────────────────────────
def render_clue_reveal_screen(clue_id: str):
    clue = CLUES[clue_id]

    st.title("✅ 조사 완료")
    st.subheader(clue["name"])
    st.caption(f"발견 장소: {clue['location']} · 조사 위치: {clue['source']}")

    show_optional_image(clue.get("image"))

    for line in clue["result"]:
        st.write(f"→ {line}")

    st.divider()

    if st.button("⬅ 이전 조사 화면으로 돌아가기", use_container_width=True):
        st.session_state.last_revealed_clue_id = None
        refresh_image_click_component()
        st.rerun()


# ─────────────────────────────────────
# 단서 구매 확인
# ─────────────────────────────────────
def render_confirm_box(clue_id: str):
    clue = CLUES[clue_id]
    already_done = clue_id in st.session_state.investigated_clues
    # 조사 전에는 menu_name(중립적인 이름)을, 이미 조사한 단서는 실제 name을 보여줍니다.
    display_name = clue["name"] if already_done else clue.get("menu_name", clue["name"])

    st.divider()
    with st.container(border=True):
        st.subheader(display_name)

        if already_done:
            st.info("이미 조사한 단서입니다.")
            if st.button("결과 다시 보기", key="already_done_reveal", use_container_width=True):
                st.session_state.pending_clue_id = None
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
                    key="confirm_investigate_btn",
                    disabled=not enough_points,
                    use_container_width=True,
                ):
                    st.session_state.points -= clue["cost"]
                    st.session_state.investigated_clues.add(clue_id)
                    st.session_state.pending_clue_id = None
                    st.session_state.last_revealed_clue_id = clue_id
                    st.session_state.last_click_xy = None
                    st.rerun()

            with c2:
                if st.button("취소", key="cancel_investigate_btn", use_container_width=True):
                    st.session_state.pending_clue_id = None
                    refresh_image_click_component()
                    st.rerun()


# ─────────────────────────────────────
# 여러 단서가 있는 hotspot의 세부 조사 메뉴
# ─────────────────────────────────────
def render_hotspot_menu(hotspot_id: str):
    hotspot = CRIME_SCENE_HOTSPOTS[hotspot_id]

    st.title(f"🔎 {hotspot['name']}")
    st.write("조사할 항목을 선택하세요.")

    for clue_id in hotspot["clue_ids"]:
        clue = CLUES[clue_id]
        done = clue_id in st.session_state.investigated_clues

        if done:
            label = f"✅ {clue['name']} - 조사 완료"
        else:
            # 조사 전에는 menu_name(중립적인 이름)만 노출합니다.
            menu_label = clue.get("menu_name", clue["name"])
            label = f"{menu_label} - {clue['cost']}P"

        if st.button(label, key=f"subclue_{clue_id}", use_container_width=True):
            if done:
                st.session_state.last_revealed_clue_id = clue_id
            else:
                st.session_state.pending_clue_id = clue_id
            st.session_state.last_click_xy = None
            st.rerun()

    if st.session_state.pending_clue_id is not None:
        render_confirm_box(st.session_state.pending_clue_id)

    st.divider()

    if st.button("⬅ 사건 현장으로 돌아가기", use_container_width=True):
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
    hotspot = hotspots[hotspot_id]

    st.title(f"🔎 {hotspot['name']}")
    st.write("조사할 항목을 선택하세요.")

    for clue_id in hotspot["clue_ids"]:
        clue = CLUES[clue_id]
        done = clue_id in st.session_state.investigated_clues

        if done:
            label = f"✅ {clue['name']} - 조사 완료"
        else:
            # 조사 전에는 menu_name(중립적인 이름)만 노출합니다.
            menu_label = clue.get("menu_name", clue["name"])
            label = f"{menu_label} - {clue['cost']}P"

        if st.button(
            label,
            key=f"room_subclue_{hotspot_id}_{clue_id}",
            use_container_width=True,
        ):
            if done:
                st.session_state.last_revealed_clue_id = clue_id
            else:
                st.session_state.pending_clue_id = clue_id
            st.session_state.last_click_xy = None
            st.rerun()

    if st.session_state.pending_clue_id is not None:
        render_confirm_box(st.session_state.pending_clue_id)

    st.divider()

    if st.button(
        f"⬅ {room_label}으로 돌아가기",
        key=f"room_back_{hotspot_id}",
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

    if st.session_state.selected_hotspot_id is not None:
        render_hotspot_menu(st.session_state.selected_hotspot_id)
        return

    st.title("📍 사건 현장 - 과방")

    top1, top2 = st.columns(2)

    with top1:
        st.metric("현재 조사 포인트", f"{st.session_state.points} P")

    with top2:
        if st.button("⬅ 메인 화면으로 돌아가기", use_container_width=True):
            clear_transient_states()
            st.session_state.current_view = None
            st.rerun()

    st.info("조사할 지점을 선택하세요. 사진 속 물건을 직접 눌러보세요.")

    with st.expander("🗺 과방 평면도 보기"):
        material = FREE_MATERIALS["floorplan"]
        if material["image"]:
            show_optional_image(material["image"])
        else:
            st.write("자료 준비 중입니다.")

    with st.expander("📋 과방 비품 목록 보기"):
        material = FREE_MATERIALS["inventory"]
        if material["image"]:
            show_optional_image(material["image"])
        else:
            st.write("자료 준비 중입니다.")

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
                clue_ids = CRIME_SCENE_HOTSPOTS[hotspot_id]["clue_ids"]

                if len(clue_ids) == 1:
                    clue_id = clue_ids[0]

                    if clue_id in st.session_state.investigated_clues:
                        st.session_state.last_revealed_clue_id = clue_id
                    else:
                        st.session_state.pending_clue_id = clue_id

                else:
                    st.session_state.selected_hotspot_id = hotspot_id

                st.rerun()

    if st.session_state.debug_mode and st.session_state.last_click_ratio:
        rx, ry = st.session_state.last_click_ratio
        st.caption(f"🧭 방금 클릭한 비율 좌표 → x={rx}, y={ry}")

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

    if st.session_state.selected_hotspot_id is not None:
        render_room_hotspot_menu(
            JIAN_ROOM_HOTSPOTS,
            st.session_state.selected_hotspot_id,
            "이지안의 방",
        )
        return

    st.title("📍 이지안의 방")

    top1, top2 = st.columns(2)

    with top1:
        st.metric("현재 조사 포인트", f"{st.session_state.points} P")

    with top2:
        if st.button("⬅ 메인 화면으로 돌아가기", use_container_width=True):
            clear_transient_states()
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
                clue_ids = JIAN_ROOM_HOTSPOTS[hotspot_id]["clue_ids"]

                if len(clue_ids) == 1:
                    clue_id = clue_ids[0]

                    if clue_id in st.session_state.investigated_clues:
                        st.session_state.last_revealed_clue_id = clue_id
                    else:
                        st.session_state.pending_clue_id = clue_id

                else:
                    st.session_state.selected_hotspot_id = hotspot_id

                st.session_state.last_click_xy = None
                st.rerun()

    if st.session_state.debug_mode and st.session_state.last_click_ratio:
        rx, ry = st.session_state.last_click_ratio
        st.caption(f"🧭 방금 클릭한 비율 좌표 → x={rx}, y={ry}")

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
                    clue_id = hotspot["clue_ids"][0]
                    if clue_id in st.session_state.investigated_clues:
                        st.session_state.last_revealed_clue_id = clue_id
                    else:
                        st.session_state.pending_clue_id = clue_id
                    st.rerun()


# ─────────────────────────────────────
# 확보한 단서
# ─────────────────────────────────────
def render_clue_list():
    st.title("🧾 확보한 단서")

    if not st.session_state.investigated_clues:
        st.info("아직 확보한 단서가 없습니다.")
    else:
        for clue_id in CLUES:
            if clue_id not in st.session_state.investigated_clues:
                continue

            clue = CLUES[clue_id]

            with st.container(border=True):
                st.subheader(clue["name"])
                st.caption(
                    f"발견 장소: {clue['location']} · 조사 위치: {clue['source']}"
                )

                show_optional_image(clue.get("image"))

                for line in clue["result"]:
                    st.write(f"→ {line}")

                if st.button(
                    "단서 다시 보기",
                    key=f"notebook_{clue_id}",
                    use_container_width=True,
                ):
                    st.session_state.last_revealed_clue_id = clue_id
                    st.session_state.current_view = "사건 현장"
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

    if st.session_state.current_view == "이지안":
        render_jian_room()
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
# 메인 화면
# ─────────────────────────────────────
st.title("🔍 학생회장 살인사건")

m1, m2, m3 = st.columns(3)

with m1:
    st.metric("팀 번호", st.session_state.team_no)

with m2:
    st.metric("조사 포인트", f"{st.session_state.points} P")

with m3:
    st.metric("현재 조사 단계", f"{st.session_state.stage}차 조사")

st.divider()
st.subheader("조사 장소 선택")

location_keys = list(LOCATIONS.keys())
cols = st.columns(3)

for i, key in enumerate(location_keys):
    unlocked = is_unlocked(key)
    display_name = LOCATIONS[key]

    with cols[i % 3]:
        if unlocked:
            label = f"🔓 {display_name}"
        else:
            label = f"🔒 {display_name} (다른 단계에서 개방)"

        if st.button(
            label,
            key=f"location_{key}",
            disabled=not unlocked,
            use_container_width=True,
        ):
            clear_transient_states()
            st.session_state.current_view = key
            st.rerun()

st.divider()

if st.button("🧾 확보한 단서 보기", use_container_width=True):
    clear_transient_states()
    st.session_state.current_view = "확보한 단서"
    st.rerun()
