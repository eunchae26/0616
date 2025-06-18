import streamlit as st
import random
import time

# 게임판 크기 설정
WIDTH, HEIGHT = 20, 10
EMPTY = " "
SNAKE_CHAR = "🟩"
STAR_CHAR = "⭐"

# 세션 상태 초기화
if "snake" not in st.session_state:
    st.session_state.snake = [(WIDTH // 2, HEIGHT // 2)]
    st.session_state.direction = (1, 0)  # 오른쪽
    st.session_state.star = (random.randint(0, WIDTH - 1), random.randint(0, HEIGHT - 1))
    st.session_state.score = 0
    st.session_state.game_over = False
    st.session_state.running = False

# 스네이크 이동 처리
def move_snake():
    head_x, head_y = st.session_state.snake[0]
    dx, dy = st.session_state.direction
    new_head = (head_x + dx, head_y + dy)

    # 충돌 검사
    if (
        not (0 <= new_head[0] < WIDTH)
        or not (0 <= new_head[1] < HEIGHT)
        or new_head in st.session_state.snake
    ):
        st.session_state.game_over = True
        st.session_state.running = False
        return

    st.session_state.snake.insert(0, new_head)

    # 별 먹은 경우
    if new_head == st.session_state.star:
        st.session_state.score += 1
        while True:
            st.session_state.star = (
                random.randint(0, WIDTH - 1),
                random.randint(0, HEIGHT - 1),
            )
            if st.session_state.star not in st.session_state.snake:
                break
    else:
        st.session_state.snake.pop()

# 게임판 출력
def render_board():
    board = ""
    for y in range(HEIGHT):
        for x in range(WIDTH):
            pos = (x, y)
            if pos == st.session_state.star:
                board += STAR_CHAR
            elif pos in st.session_state.snake:
                board += SNAKE_CHAR
            else:
                board += EMPTY
        board += "\n"
    return board

# UI 구성
st.title("🐍 Snake Game")
st.markdown("화살표 버튼을 눌러 뱀을 조종하세요.")

# 방향 버튼 UI
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("⬅️ Left"):
        if st.session_state.direction != (1, 0):
            st.session_state.direction = (-1, 0)
with col2:
    if st.button("⬆️ Up"):
        if st.session_state.direction != (0, 1):
            st.session_state.direction = (0, -1)
    if st.button("⬇️ Down"):
        if st.session_state.direction != (0, -1):
            st.session_state.direction = (0, 1)
with col3:
    if st.button("➡️ Right"):
        if st.session_state.direction != (-1, 0):
            st.session_state.direction = (1, 0)

# 게임판, 점수 출력
st.text(render_board())
st.write(f"Score: {st.session_state.score}")

# 게임 오버 처리
if st.session_state.game_over:
    st.error("💀 Game Over!")
    if st.button("🔄 Restart"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

# 게임 시작 버튼
if not st.session_state.running and not st.session_state.game_over:
    if st.button("▶️ Start"):
        st.session_state.running = True
        st.rerun()

# 프레임 반복 처리
if st.session_state.running:
    time.sleep(0.25)
    move_snake()
    st.rerun()
