import streamlit as st


def apply_custom_style():
    st.markdown(
        """
        <style>
        .stApp {
            background:
                radial-gradient(circle at top left, rgba(20, 184, 166, 0.14), transparent 30%),
                radial-gradient(circle at top right, rgba(59, 130, 246, 0.12), transparent 28%),
                linear-gradient(135deg, #07111f 0%, #0b1220 45%, #111827 100%);
            color: #e5e7eb;
        }

        .block-container {
            padding-top: 2rem;
            padding-bottom: 3rem;
            max-width: 1180px;
        }

        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #0b1220 0%, #111827 100%);
            border-right: 1px solid rgba(148, 163, 184, 0.18);
        }

        h1, h2, h3 {
            color: #f8fafc;
            letter-spacing: -0.03em;
        }

        p, li {
            color: #cbd5e1;
            font-size: 1.02rem;
            line-height: 1.65;
        }

        .hero-box {
            padding: 2.2rem;
            border-radius: 26px;
            background: linear-gradient(135deg, rgba(15, 23, 42, 0.96), rgba(30, 41, 59, 0.86));
            border: 1px solid rgba(45, 212, 191, 0.28);
            box-shadow: 0 24px 60px rgba(0, 0, 0, 0.35);
            margin-bottom: 1.4rem;
        }

        .hero-badge {
            display: inline-block;
            padding: 0.42rem 0.8rem;
            border-radius: 999px;
            background: rgba(20, 184, 166, 0.14);
            color: #5eead4;
            border: 1px solid rgba(94, 234, 212, 0.24);
            font-weight: 700;
            font-size: 0.82rem;
            margin-bottom: 0.9rem;
        }

        .hero-title {
            font-size: 2.45rem;
            font-weight: 850;
            color: #f8fafc;
            margin-bottom: 0.65rem;
            line-height: 1.1;
        }

        .hero-subtitle {
            font-size: 1.08rem;
            color: #cbd5e1;
            max-width: 900px;
        }

        .feature-card {
            padding: 1.25rem;
            border-radius: 20px;
            background: rgba(15, 23, 42, 0.78);
            border: 1px solid rgba(148, 163, 184, 0.18);
            box-shadow: 0 18px 45px rgba(0, 0, 0, 0.22);
            min-height: 175px;
        }

        .card-icon {
            font-size: 1.8rem;
            margin-bottom: 0.65rem;
        }

        .card-title {
            color: #f8fafc;
            font-size: 1.08rem;
            font-weight: 800;
            margin-bottom: 0.45rem;
        }

        .card-text {
            color: #cbd5e1;
            font-size: 0.95rem;
            line-height: 1.55;
        }

        div[data-testid="stMetric"] {
            background: rgba(15, 23, 42, 0.82);
            border: 1px solid rgba(148, 163, 184, 0.18);
            border-radius: 18px;
            padding: 1rem;
            box-shadow: 0 14px 35px rgba(0, 0, 0, 0.24);
        }

        .stButton > button {
            border-radius: 14px;
            border: 1px solid rgba(45, 212, 191, 0.45);
            background: linear-gradient(135deg, #0f766e, #0891b2);
            color: white;
            font-weight: 800;
            padding: 0.65rem 1.25rem;
        }

        .stButton > button:hover {
            border-color: #67e8f9;
            background: linear-gradient(135deg, #0d9488, #0284c7);
            color: white;
        }

        div[data-testid="stAlert"] {
            border-radius: 16px;
        }

        div[data-testid="stDataFrame"] {
            border-radius: 16px;
            overflow: hidden;
        }
        </style>
        """,
        unsafe_allow_html=True
    )


def page_header(title, subtitle, badge):
    st.markdown(
        f"""
        <div class="hero-box">
            <div class="hero-badge">{badge}</div>
            <div class="hero-title">{title}</div>
            <div class="hero-subtitle">{subtitle}</div>
        </div>
        """,
        unsafe_allow_html=True
    )