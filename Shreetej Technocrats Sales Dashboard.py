import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(
    page_title="Dashboard - Shreetej Technocrats Sales",
    page_icon="₹",
    layout="wide"
)

# ── Data ──────────────────────────────────────────────────────────────────────
months = ['Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec','Jan','Feb','Mar']

fy2526 = [4198167, 6047196, 8729570, 6465936, 7009267,
          5780814, 3468420, 3537555, 6158338, 2950253, 4176552, 11396772]

fy2425 = [5058716, 5016185, 6408338, 4724145, 6863043,
          4557826, 4730895, 3669660, 5400574, 5342103, 4019996, 6196777]

insights = {
    'Apr': "April started lower (–17%). Slow opening to the financial year.",
    'May': "May bounced back strongly — 20% higher than last year! 🚀",
    'Jun': "Best first-half month! Revenue grew 36% over last year.",
    'Jul': "July dipped –27% vs last year, but still a solid number.",
    'Aug': "Very close to last year (+2%). Consistent performance.",
    'Sep': "Strong September! +27% growth — mid-year recovery in full swing.",
    'Oct': "October dipped –27%. Post-festive slowdown may be the cause.",
    'Nov': "Nearly identical to last year (–4%). Reliable baseline month.",
    'Dec': "December grew +14%. Great end-of-calendar-year push!",
    'Jan': "January was the toughest — down 45% vs last year. Watch this month.",
    'Feb': "February held steady at +4% growth. Consistent and dependable.",
    'Mar': "🌟 BEST MONTH! Revenue nearly doubled — +84% over last year!",
}

df = pd.DataFrame({
    'Month': months,
    'FY 25-26 (₹)': fy2526,
    'FY 24-25 (₹)': fy2425,
})
df['Change %'] = ((df['FY 25-26 (₹)'] - df['FY 24-25 (₹)']) / df['FY 24-25 (₹)'] * 100).round(1)
df['FY 25-26 (L)'] = (df['FY 25-26 (₹)'] / 1e5).round(2)
df['FY 24-25 (L)'] = (df['FY 24-25 (₹)'] / 1e5).round(2)

total_2526 = sum(fy2526)
total_2425 = sum(fy2425)
growth = ((total_2526 - total_2425) / total_2425 * 100)
best_month_idx = df['Change %'].idxmax()
worst_month_idx = df['Change %'].idxmin()

# ── Styles ────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  .main { background: #f8f9fb; }
  .block-container { padding-top: 1.5rem; padding-bottom: 2rem; }
  .metric-card {
    background: white;
    border-radius: 14px;
    padding: 1.2rem 1.5rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    text-align: center;
  }
  .metric-label { font-size: 13px; color: #888; margin-bottom: 4px; }
  .metric-value { font-size: 26px; font-weight: 600; }
  .section-title { font-size: 17px; font-weight: 600; color: #1a1a2e; margin: 0.5rem 0; }
  .insight-box {
    background: #e8f4fd;
    border-left: 4px solid #378ADD;
    border-radius: 8px;
    padding: 0.9rem 1.2rem;
    font-size: 14px;
    color: #1a3a5c;
    margin-top: 0.5rem;
  }
  .stSelectbox label { font-size: 13px !important; color: #555 !important; }
</style>
""", unsafe_allow_html=True)

# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown("## Dashboard - Shreetej Technocrats Sales")
st.markdown("**FY 2025–26 vs FY 2024–25** — click a chart bar or pick a month to explore insights")
st.markdown("---")

# ── KPI Cards ─────────────────────────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f"""<div class="metric-card">
        <div class="metric-label">Total FY 25–26</div>
        <div class="metric-value" style="color:#185FA5;">₹{total_2526/1e7:.2f} Cr</div>
    </div>""", unsafe_allow_html=True)

with c2:
    st.markdown(f"""<div class="metric-card">
        <div class="metric-label">Total FY 24–25</div>
        <div class="metric-value" style="color:#3B6D11;">₹{total_2425/1e7:.2f} Cr</div>
    </div>""", unsafe_allow_html=True)

with c3:
    arrow = "▲" if growth > 0 else "▼"
    col = "#3B6D11" if growth > 0 else "#A32D2D"
    st.markdown(f"""<div class="metric-card">
        <div class="metric-label">Year-on-Year Growth</div>
        <div class="metric-value" style="color:{col};">{arrow} {abs(growth):.1f}%</div>
    </div>""", unsafe_allow_html=True)

with c4:
    best = months[best_month_idx]
    st.markdown(f"""<div class="metric-card">
        <div class="metric-label">Best Month (Growth)</div>
        <div class="metric-value" style="color:#D85A30;">{best} +{df.loc[best_month_idx,'Change %']}%</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Chart ─────────────────────────────────────────────────────────────────────
col_left, col_right = st.columns([3, 1])

with col_right:
    chart_type = st.radio("Chart type", ["Bar", "Line"], horizontal=False)
    selected_month = st.selectbox("Highlight a month", ["None"] + months)

with col_left:
    highlight = selected_month if selected_month != "None" else None

    opacity_2526 = [1.0 if (highlight is None or m == highlight) else 0.35 for m in months]
    opacity_2425 = [1.0 if (highlight is None or m == highlight) else 0.35 for m in months]

    colors_2526 = [f'rgba(55,138,221,{o})' for o in opacity_2526]
    colors_2425 = [f'rgba(99,153,34,{o})' for o in opacity_2425]

    fig = go.Figure()

    if chart_type == "Bar":
        fig.add_trace(go.Bar(
            name='FY 25–26', x=months, y=df['FY 25-26 (L)'],
            marker_color=colors_2526,
            hovertemplate='<b>%{x}</b><br>FY 25–26: ₹%{y:.2f}L<extra></extra>'
        ))
        fig.add_trace(go.Bar(
            name='FY 24–25', x=months, y=df['FY 24-25 (L)'],
            marker_color=colors_2425,
            hovertemplate='<b>%{x}</b><br>FY 24–25: ₹%{y:.2f}L<extra></extra>'
        ))
        fig.update_layout(barmode='group')
    else:
        fig.add_trace(go.Scatter(
            name='FY 25–26', x=months, y=df['FY 25-26 (L)'],
            mode='lines+markers',
            line=dict(color='#378ADD', width=2.5),
            marker=dict(size=[12 if m == highlight else 6 for m in months], color=colors_2526),
            fill='tozeroy', fillcolor='rgba(55,138,221,0.08)',
            hovertemplate='<b>%{x}</b><br>FY 25–26: ₹%{y:.2f}L<extra></extra>'
        ))
        fig.add_trace(go.Scatter(
            name='FY 24–25', x=months, y=df['FY 24-25 (L)'],
            mode='lines+markers',
            line=dict(color='#639922', width=2.5),
            marker=dict(size=[12 if m == highlight else 6 for m in months], color=colors_2425),
            fill='tozeroy', fillcolor='rgba(99,153,34,0.08)',
            hovertemplate='<b>%{x}</b><br>FY 24–25: ₹%{y:.2f}L<extra></extra>'
        ))

    fig.update_layout(
        height=340,
        margin=dict(l=10, r=10, t=20, b=10),
        paper_bgcolor='white',
        plot_bgcolor='white',
        font=dict(family='sans-serif', size=13),
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
        yaxis=dict(
            title='Revenue (₹ Lakhs)', gridcolor='#f0f0f0',
            tickprefix='₹', ticksuffix='L', tickfont=dict(size=11)
        ),
        xaxis=dict(gridcolor='#f0f0f0', tickfont=dict(size=12)),
    )
    st.plotly_chart(fig, use_container_width=True)

# ── Insight Box ────────────────────────────────────────────────────────────────
if selected_month != "None":
    st.markdown(f"""<div class="insight-box">
        💡 <strong>{selected_month}:</strong> {insights[selected_month]}
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Change % Bar ───────────────────────────────────────────────────────────────
st.markdown('<p class="section-title">Month-on-month growth rate (%)</p>', unsafe_allow_html=True)

bar_colors = ['#3B6D11' if v >= 0 else '#A32D2D' for v in df['Change %']]
fig2 = go.Figure(go.Bar(
    x=months, y=df['Change %'],
    marker_color=bar_colors,
    text=[f"{v:+.1f}%" for v in df['Change %']],
    textposition='outside',
    hovertemplate='<b>%{x}</b><br>Change: %{y:.1f}%<extra></extra>'
))
fig2.add_hline(y=0, line_width=1, line_color='#ccc')
fig2.update_layout(
    height=240, margin=dict(l=10, r=10, t=30, b=10),
    paper_bgcolor='white', plot_bgcolor='white',
    yaxis=dict(title='Change %', gridcolor='#f0f0f0', ticksuffix='%'),
    xaxis=dict(gridcolor='#f0f0f0'),
    showlegend=False
)
st.plotly_chart(fig2, use_container_width=True)

# ── Data Table ─────────────────────────────────────────────────────────────────
st.markdown('<p class="section-title">Full month-by-month data</p>', unsafe_allow_html=True)

display_df = df[['Month','FY 25-26 (L)','FY 24-25 (L)','Change %']].copy()
display_df.columns = ['Month', 'FY 25–26 (₹L)', 'FY 24–25 (₹L)', 'Change %']

def highlight_change(val):
    if isinstance(val, float):
        color = '#d4edda' if val > 0 else '#f8d7da'
        return f'background-color: {color}'
    return ''

styled = display_df.style\
    .format({'FY 25–26 (₹L)': '₹{:.2f}L', 'FY 24–25 (₹L)': '₹{:.2f}L', 'Change %': '{:+.1f}%'})\
    .map(highlight_change, subset=['Change %'])\
    .set_properties(**{'text-align': 'center'})\
    .set_table_styles([
        {'selector': 'th', 'props': [('background-color', '#1a3a5c'), ('color', 'white'),
                                      ('font-size', '13px'), ('text-align', 'center')]},
        {'selector': 'td', 'props': [('font-size', '13px')]},
    ])

st.dataframe(styled, use_container_width=True, hide_index=True)

# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<center style='color:#aaa; font-size:12px;'>Revenue Dashboard · FY 2025–26 vs FY 2024–25 · Values in ₹ Lakhs</center>",
    unsafe_allow_html=True
)