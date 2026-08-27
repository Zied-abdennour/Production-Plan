import streamlit as st

def apply_style():
    st.markdown("""
    <style>

    .block-container {
        padding-top: 2.5rem;
        padding-bottom: 3rem;
        max-width: 1400px;
    }

    section[data-testid="stSidebar"] {
        background: #111827;
    }

    section[data-testid="stSidebar"] * {
        color: #f8fafc;
    }

    section[data-testid="stSidebar"] [data-testid="stIconMaterial"] {
        color: #ffffff !important;
    }

    section[data-testid="stSidebar"] svg {
        color: #ffffff !important;
        fill: #ffffff !important;
    }

    section[data-testid="stSidebar"] button {
        background-color: #1e293b !important;
        color: #ffffff !important;
        border: 1px solid #334155 !important;
    }

    section[data-testid="stSidebar"] button p {
        color: #ffffff !important;
    }

    section[data-testid="stSidebar"] button span {
        color: #ffffff !important;
    }

    section[data-testid="stSidebar"] button:hover {
        background-color: #334155 !important;
        color: #ffffff !important;
        border-color: #475569 !important;
    }

    section[data-testid="stSidebar"] button:hover p {
        color: #ffffff !important;
    }

    section[data-testid="stSidebar"] button:hover span {
        color: #ffffff !important;
    }

    .page-title {
        font-size: 2.3rem;
        font-weight: 700;
        color: #172033;
        margin-bottom: 0.35rem;
    }

    .page-subtitle {
        color: #64748b;
        font-size: 1rem;
        margin-bottom: 2rem;
    }

    .metric-box {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 1.2rem 1.4rem;
        min-height: 110px;
    }

    .metric-label {
        color: #64748b;
        font-size: 0.9rem;
        margin-bottom: 0.4rem;
    }

    .metric-value {
        color: #172033;
        font-size: 2rem;
        font-weight: 700;
    }

    .metric-description {
        color: #94a3b8;
        font-size: 0.8rem;
        margin-top: 0.25rem;
    }

    .result-score {
        background: #ffffff;
        border: 1px solid #dbe3ed;
        border-radius: 14px;
        padding: 1.5rem 1.8rem;
        margin: 1.5rem 0 2rem 0;
    }

    .result-score-label {
        color: #64748b;
        font-size: 0.9rem;
        margin-bottom: 0.3rem;
    }

    .result-score-value {
        color: #172033;
        font-size: 2.7rem;
        font-weight: 750;
        line-height: 1.1;
    }

    .result-score-description {
        color: #94a3b8;
        font-size: 0.85rem;
        margin-top: 0.4rem;
    }

    .timeline-container {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 14px;
        padding: 1.5rem;
        overflow-x: auto;
    }

    .timeline {
        min-width: 900px;
    }

    .timeline-header {
        display: grid;
        grid-template-columns: 90px 1fr;
        margin-bottom: 8px;
    }

    .timeline-axis {
        position: relative;
        height: 34px;
        border-bottom: 1px solid #cbd5e1;
    }

    .timeline-tick {
        position: absolute;
        bottom: 0;
        transform: translateX(-50%);
        color: #64748b;
        font-size: 0.72rem;
        white-space: nowrap;
    }

    .timeline-tick-line {
        position: absolute;
        bottom: -6px;
        width: 1px;
        height: 7px;
        background: #94a3b8;
    }

    .timeline-row {
        display: grid;
        grid-template-columns: 90px 1fr;
        min-height: 68px;
        border-bottom: 1px solid #edf1f5;
    }

    .timeline-row:last-child {
        border-bottom: none;
    }

    .timeline-workplace {
        display: flex;
        align-items: center;
        color: #334155;
        font-weight: 650;
        font-size: 0.85rem;
    }

    .timeline-track {
        position: relative;
        height: 68px;
        background:
            repeating-linear-gradient(
                to right,
                transparent 0,
                transparent calc(10% - 1px),
                #edf1f5 calc(10% - 1px),
                #edf1f5 10%
            );
    }

    .timeline-block {
        position: absolute;
        top: 15px;
        height: 38px;
        border-radius: 7px;
        background: #334155;
        border: 1px solid #26364d;
        display: flex;
        align-items: center;
        padding: 0 10px;
        box-sizing: border-box;
        overflow: hidden;
        white-space: nowrap;
        color: #ffffff;
        font-size: 0.72rem;
        font-weight: 600;
        box-shadow: 0 2px 5px rgba(15, 23, 42, 0.12);
    }

    .timeline-block:hover {
        z-index: 10;
        box-shadow: 0 5px 14px rgba(15, 23, 42, 0.2);
    }

    .timeline-block-label {
        overflow: hidden;
        text-overflow: ellipsis;
    }

    .timeline-legend {
        display: flex;
        gap: 1.5rem;
        margin-top: 1rem;
        color: #64748b;
        font-size: 0.8rem;
    }

    .timeline-legend-item {
        display: flex;
        align-items: center;
        gap: 7px;
    }

    .timeline-legend-dot {
        width: 10px;
        height: 10px;
        border-radius: 3px;
        background: #334155;
    }

    .sequence-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 1rem 1.25rem;
        margin-bottom: 0.6rem;
    }

    .sequence-number {
        color: #94a3b8;
        font-size: 0.8rem;
        margin-right: 0.7rem;
    }

    .sequence-text {
        color: #334155;
        font-weight: 600;
    }

    </style>
    """, unsafe_allow_html=True)


def page_header(title, subtitle=""):
    st.markdown(
        f'<div class="page-title">{title}</div>',
        unsafe_allow_html=True
    )

    if subtitle:
        st.markdown(
            f'<div class="page-subtitle">{subtitle}</div>',
            unsafe_allow_html=True
        )


def metric_card(label, value, description=""):
    st.markdown(
        f"""
        <div class="metric-box">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-description">{description}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown(
    """
    <style>

    .production-timeline {
        width: 100%;
        margin-top: 18px;
        margin-bottom: 30px;
    }

    .timeline-axis-row {
        display: flex;
        width: 100%;
        height: 55px;
    }

    .timeline-label-space {
        width: 72px;
        min-width: 72px;
    }

    .timeline-axis {
        position: relative;
        flex: 1;
        height: 100%;
        border-top: 1px solid #d8dee8;
    }

    .timeline-axis-tick {
        position: absolute;
        top: 0;
        height: 100%;
        border-left: 1px solid #e5e9f0;
        transform: translateX(-50%);
    }

    .timeline-axis-tick span {
        position: absolute;
        top: 8px;
        left: 50%;
        transform: translateX(-50%);
        font-size: 11px;
        color: #64748b;
        white-space: nowrap;
    }

    .timeline-row {
        display: flex;
        width: 100%;
        min-height: 48px;
        margin-bottom: 7px;
    }

    .timeline-workplace-name {
        width: 72px;
        min-width: 72px;
        display: flex;
        align-items: center;
        font-size: 13px;
        font-weight: 600;
        color: #334155;
    }

    .timeline-track {
        position: relative;
        flex: 1;
        min-height: 42px;
        border-radius: 7px;
        background:
            repeating-linear-gradient(
                to right,
                transparent 0%,
                transparent calc(10% - 1px),
                #e8edf3 calc(10% - 1px),
                #e8edf3 10%
            );
        border-top: 1px solid #eef1f5;
        border-bottom: 1px solid #eef1f5;
    }

    .timeline-operation {
        position: absolute;
        top: 5px;
        height: 32px;
        min-width: 24px;
        border-radius: 6px;
        background: #334155;
        border: 1px solid #263449;
        box-sizing: border-box;
        display: flex;
        align-items: center;
        padding: 0 9px;
        overflow: hidden;
        white-space: nowrap;
        cursor: default;
        transition:
            transform 0.12s ease,
            box-shadow 0.12s ease;
    }

    .timeline-operation:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 10px rgba(15, 23, 42, 0.18);
        z-index: 10;
    }

    .timeline-operation span {
        color: white;
        font-size: 11px;
        font-weight: 600;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
    }

    </style>
    """,
    unsafe_allow_html=True
)