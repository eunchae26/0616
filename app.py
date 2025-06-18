import streamlit as st
import random
import time

WIDTH, HEIGHT = 20, 10
EMPTY = " "
SNAKE_CHAR = "🟩"
STAR_CHAR = "⭐"

# 초기화
if "snake" not in st.session_state:
    st.session_state.snake = [(WIDTH // 2, HEIGHT // 2)]
    st.session_state.direction = (1, 0)
    st.session_state.star = (random.randint(0, WIDTH - 1), random.randint(0, HEIGHT - 1))
    st.session_state.score = 0
    st.session_state.game_over = False
    st.session_state.running = False

def move_snake():
    head_x, head_y = st.session_state.snake[0]
    dx, dy = st.session_state.direction
    new_head = (head_x + dx, head_y + dy)

    if (
        not (0 <= new_head[0] < WIDTH)
        or not (0 <= new_head[1] < HEIGHT)
        or new_head in st.session_state.snake
    ):
        st.session_state.game_over = True
        st.session_state.running = False
        return

    st.session_state.snake.insert(0, new_head)

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

st.title("🐍 Snake Game")
st.markdown("Use the arrow buttons to control the snake.")

# 방향 조작 버튼
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

st.text(render_board())
st.write(f"Score: {st.session_state.score}")

# 게임 상태 처리
if st.session_state.game_over:
    st.error("💀 Game Over!")
    if st.button("🔄 Restart"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.experimental_rerun()

# 게임 시작
if not st.session_state.running and not st.session_state.game_over:
    if st.button("▶️ Start"):
        st.session_state.running = True
        st.experimental_rerun()

# 프레임 실행
if st.session_state.running:
    time.sleep(0.25)  # delay between frames
    move_snake()
    st.experimental_rerun()
