
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve, fminbound

st.set_page_config(page_title="케이블 구조물 최적 설계 도우미", layout="centered")

# 다리 이모지 대신 이미지 로고 삽입
st.image("bridge_icon.png", width=60)
st.title("케이블 구조물 최적 설계 도우미")
st.markdown("입력한 거리(D)와 처짐 깊이(H)를 바탕으로 최적 a값, 곡선 그래프, 장력 방향, 퍼텐셜 에너지, 자재 길이를 시각화합니다.")

# 입력
D = st.number_input("📏 거리 D (단위: m)", min_value=1.0, value=120.0, step=1.0)
H = st.number_input("📐 처짐 깊이 H (단위: m)", min_value=0.1, value=12.0, step=1.0)

if st.button("계산하기"):
    g = 9.8
    rho = 1
    x0 = D / 2

    def equation(a):
        return a * np.cosh(x0 / a) - a - H

    try:
        a_opt = fsolve(equation, x0)[0]
        st.success(f"✅ 계산된 최적 a값: {a_opt:.2f} m")

        y = lambda x: a_opt * np.cosh(x / a_opt)
        dy = lambda x: np.sinh(x / a_opt)
        integrand_energy = lambda x: rho * g * y(x) * np.sqrt(1 + (dy(x))**2)
        U = np.round(np.trapz(integrand_energy(np.linspace(-x0, x0, 1000)), np.linspace(-x0, x0, 1000)), 2)

        arc_length_integrand = lambda x: np.sqrt(1 + (dy(x))**2)
        arc_len = np.round(np.trapz(arc_length_integrand(np.linspace(-x0, x0, 1000)), np.linspace(-x0, x0, 1000)), 2)

        st.write(f"💠 퍼텐셜 에너지: {U:,.2f} J")
        st.write(f"🧱 예상 자재 길이: {arc_len:.2f} m")

        # 그래프
        x = np.linspace(-x0, x0, 300)
        fig, ax = plt.subplots()
        ax.plot(x, y(x), label="현수선 곡선")
        ax.quiver(x[::20], y(x)[::20], 1, dy(x)[::20], angles='xy', scale_units='xy', scale=5, color='r', width=0.003)
        ax.set_xlabel("x (m)")
        ax.set_ylabel("y (m)")
        ax.set_title("현수선 형태 및 장력 방향")
        ax.legend()
        ax.grid(True)
        st.pyplot(fig)

    except Exception as e:
        st.error("❌ 계산에 실패했습니다. 입력값을 다시 확인해주세요.")
