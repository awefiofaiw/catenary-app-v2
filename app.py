
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from scipy.optimize import fsolve
from scipy.integrate import quad

# 한글 폰트 등록
font_path = "NanumGothic-Regular.ttf"
font_prop = fm.FontProperties(fname=font_path)
plt.rcParams['font.family'] = font_prop.get_name()

st.set_page_config(page_title="케이블 구조물 최적 설계 도우미")

# 타이틀
st.markdown("### 🏗️ 케이블 구조물 최적 설계 도우미")
st.write("입력한 거리(D)와 처짐 깊이(H)를 바탕으로 최적 a값, 곡선 그래프, 처짐 방향(장력), 퍼텐셜 에너지, 자재 길이를 시각화합니다.")

# 사용자 입력
D = st.number_input("📐 거리 D (단위: m)", min_value=1.0, step=1.0, format="%.2f")
H = st.number_input("📐 처짐 깊이 H (단위: m)", min_value=0.1, step=0.1, format="%.2f")

def equation(a, D, H):
    return a * np.cosh(D / (2 * a)) - a - H

def catenary_y(x, a):
    return a * np.cosh(x / a)

def arc_length_integrand(x, a):
    return np.sqrt(1 + (np.sinh(x / a))**2)

def potential_energy_integrand(x, a, g=9.8, rho=1):
    y = catenary_y(x, a)
    return rho * g * y * arc_length_integrand(x, a)

if st.button("계산하기"):
    try:
        a_initial = D / 2
        a_sol = fsolve(equation, a_initial, args=(D, H))[0]

        if a_sol <= 0 or np.isnan(a_sol):
            raise ValueError("올바르지 않은 a값입니다.")

        L, _ = quad(arc_length_integrand, -D/2, D/2, args=(a_sol,))
        U, _ = quad(potential_energy_integrand, -D/2, D/2, args=(a_sol,))

        st.success(f"✅ 계산된 최적 a값: {a_sol:.2f} m")
        st.info(f"🔷 퍼텐셜 에너지: {U:,.2f} J")
        st.info(f"🧱 예상 자재 길이: {L:.2f} m")

        # 시각화
        x_vals = np.linspace(-D/2, D/2, 200)
        y_vals = catenary_y(x_vals, a_sol)

        # 수직 아래 방향 화살표
        ux = np.zeros_like(x_vals)
        uy = np.ones_like(x_vals)

        fig, ax = plt.subplots()
        ax.plot(x_vals, y_vals, label="현수선 곡선", color='royalblue', linewidth=2)
        ax.quiver(x_vals, y_vals, ux, uy, angles='xy', scale_units='xy', scale=10, color='darkred', width=0.003, label="처짐 방향")
        ax.set_title("현수선 곡선 및 장력 방향", fontproperties=font_prop)
        ax.set_xlabel("x (m)", fontproperties=font_prop)
        ax.set_ylabel("y (m)", fontproperties=font_prop)
        ax.legend(prop=font_prop)
        ax.grid(True)

        st.pyplot(fig)

    except Exception as e:
        st.error(f"❌ 계산에 실패했습니다: {str(e)}")
