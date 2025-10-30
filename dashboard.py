import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import io
import json
from src.ingest import read_csv, sort_records, filter_records
from src.transform import add_computed_fields, compute_improvement
from src.analyze import (compute_stats, grade_distribution, identify_at_risk,
                         section_comparison, top_performers, compute_percentile)

st.set_page_config(page_title="Academic Analytics",
                   page_icon="🎓", layout="wide")

st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
.hero {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 3rem;
    border-radius: 20px;
    color: white;
    text-align: center;
    margin-bottom: 2rem;
}
.hero h1 {font-size: 3rem; font-weight: 800; margin: 0;}
.hero p {font-size: 1.2rem; margin-top: 0.5rem;}
div[data-testid="stMetricValue"] {font-size: 2rem; font-weight: 700; color: #667eea;}
.stButton > button {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white; border: none; border-radius: 10px;
    padding: 0.6rem 2rem; font-weight: 600;
}
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_config():
    try:
        with open('config.json', 'r') as f:
            return json.load(f)
    except:
        return {
            'weights': {'quizzes': 0.2, 'midterm': 0.3, 'final': 0.4, 'attendance': 0.1},
            'thresholds': {'at_risk': 60},
            'grade_scale': {'A': 90, 'B': 80, 'C': 70, 'D': 60, 'F': 0}
        }


def process_data(source, weights, grade_scale):
    if isinstance(source, str):
        records, _ = read_csv(source)
    else:
        with open("temp_upload.csv", "wb") as f:
            f.write(source.getbuffer())
        records, _ = read_csv("temp_upload.csv")
    records = add_computed_fields(records, weights, grade_scale)
    for r in records:
        r['improvement'] = compute_improvement(r)
    return records


config = load_config()

st.markdown('<div class="hero"><h1>🎓 Academic Analytics</h1><p>Modern Student Performance Dashboard</p></div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    uploaded = st.file_uploader("📁 Upload CSV", type=['csv'])
    use_sample = st.checkbox("Use Sample Data", value=True)

if not uploaded and not use_sample:
    st.info("👆 Upload CSV or use sample data")
    st.stop()

source = "data/input.csv" if use_sample else uploaded
records = process_data(source, config['weights'], config['grade_scale'])
valid_grades = [r['final_grade'] for r in records if r['final_grade']]

if not valid_grades:
    st.error("No valid data")
    st.stop()

stats = compute_stats(valid_grades)
distribution = grade_distribution(records)

st.success(f"✅ Loaded {len(records)} students")

st.markdown("### 📊 Key Metrics")
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Students", len(records))
col2.metric("Average", f"{stats['mean']:.1f}")
col3.metric("Median", f"{stats['median']:.1f}")
col4.metric("Highest", f"{stats['max']:.1f}")
col5.metric("Lowest", f"{stats['min']:.1f}")

st.markdown("---")
st.markdown("### 📈 Visualizations")

col1, col2 = st.columns(2)

with col1:
    fig, ax = plt.subplots(figsize=(8, 5))
    grades = ['A', 'B', 'C', 'D', 'F']
    counts = [distribution.get(g, 0) for g in grades]
    colors = ['#10b981', '#3b82f6', '#f59e0b', '#f97316', '#ef4444']
    bars = ax.bar(grades, counts, color=colors, alpha=0.8,
                  edgecolor='white', linewidth=2)
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height, f'{int(height)}',
                ha='center', va='bottom', fontweight='bold')
    ax.set_title('Grade Distribution', fontsize=14, fontweight='bold')
    ax.set_ylabel('Students', fontsize=11)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(True, alpha=0.3)
    st.pyplot(fig)
    plt.close()

with col2:
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.hist(valid_grades, bins=20, color='#8b5cf6',
            alpha=0.8, edgecolor='white', linewidth=2)
    ax.set_title('Score Distribution', fontsize=14, fontweight='bold')
    ax.set_xlabel('Final Grade', fontsize=11)
    ax.set_ylabel('Frequency', fontsize=11)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(True, alpha=0.3)
    st.pyplot(fig)
    plt.close()

st.markdown("---")
st.markdown("### 🏫 Section Performance")

section_stats = section_comparison(records)
sections = list(section_stats.keys())
means = [section_stats[s]['mean'] for s in sections]

col1, col2 = st.columns([3, 1])

with col1:
    fig, ax = plt.subplots(figsize=(10, 4))
    bars = ax.bar(sections, means, color='#667eea',
                  alpha=0.8, edgecolor='white', linewidth=2)
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height, f'{height:.1f}',
                ha='center', va='bottom', fontweight='bold')
    ax.set_title('Average by Section', fontsize=14, fontweight='bold')
    ax.set_ylabel('Average Grade', fontsize=11)
    ax.set_ylim(0, 100)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(True, alpha=0.3)
    st.pyplot(fig)
    plt.close()

with col2:
    st.markdown("**Percentiles**")
    st.metric("25th", f"{compute_percentile(valid_grades, 25):.1f}")
    st.metric("50th", f"{compute_percentile(valid_grades, 50):.1f}")
    st.metric("75th", f"{compute_percentile(valid_grades, 75):.1f}")
    st.metric("90th", f"{compute_percentile(valid_grades, 90):.1f}")

st.markdown("---")
st.markdown("### 👥 Student Rankings")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**🏆 Top 10 Performers**")
    top_10 = top_performers(records, 10)
    top_df = pd.DataFrame([{
        'Rank': i+1,
        'Name': f"{r['first_name']} {r['last_name']}",
        'Section': r['section'],
        'Grade': f"{r['final_grade']:.1f}",
        'Letter': r['letter_grade']
    } for i, r in enumerate(top_10)])
    st.dataframe(top_df, hide_index=True, use_container_width=True, height=400)

with col2:
    st.markdown("**⚠️ At-Risk Students**")
    at_risk = identify_at_risk(records, config['thresholds']['at_risk'])
    if at_risk:
        risk_df = pd.DataFrame([{
            'Name': f"{r['first_name']} {r['last_name']}",
            'Section': r['section'],
            'Grade': f"{r['final_grade']:.1f}",
            'Letter': r['letter_grade']
        } for r in at_risk])
        st.dataframe(risk_df, hide_index=True,
                     use_container_width=True, height=400)
    else:
        st.success("✅ No at-risk students")

st.markdown("---")
st.markdown("### 📋 All Students")

sorted_records = sort_records(records, 'final_grade', reverse=True)
df = pd.DataFrame([{
    'ID': r['student_id'],
    'Name': f"{r['first_name']} {r['last_name']}",
    'Section': r['section'],
    'Quiz': f"{r['quiz_average']:.1f}" if r['quiz_average'] else 'N/A',
    'Midterm': f"{r['midterm']:.0f}" if r['midterm'] else 'N/A',
    'Final': f"{r['final']:.0f}" if r['final'] else 'N/A',
    'Grade': f"{r['final_grade']:.1f}" if r['final_grade'] else 'N/A',
    'Letter': r['letter_grade']
} for r in sorted_records])

st.dataframe(df, hide_index=True, use_container_width=True, height=450)

st.markdown("---")
st.markdown("### 📥 Export Reports")

col1, col2, col3, col4 = st.columns(4)

with col1:
    output = io.StringIO()
    df.to_csv(output, index=False)
    st.download_button("📄 All Students", output.getvalue(),
                       "all_students.csv", use_container_width=True)

with col2:
    if at_risk:
        output = io.StringIO()
        risk_df.to_csv(output, index=False)
        st.download_button("⚠️ At-Risk", output.getvalue(),
                           "at_risk.csv", use_container_width=True)

with col3:
    output = io.StringIO()
    top_df.to_csv(output, index=False)
    st.download_button("🏆 Top 10", output.getvalue(),
                       "top_10.csv", use_container_width=True)

with col4:
    section_a = filter_records(records, lambda r: r['section'] == 'A')
    if section_a:
        output = io.StringIO()
        pd.DataFrame([{
            'ID': r['student_id'],
            'Name': f"{r['first_name']} {r['last_name']}",
            'Grade': f"{r['final_grade']:.1f}" if r['final_grade'] else 'N/A'
        } for r in section_a]).to_csv(output, index=False)
        st.download_button("📊 Section A", output.getvalue(),
                           "section_a.csv", use_container_width=True)
