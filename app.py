"""
Academic Analytics Lite - Streamlit Web Application
Interactive data analysis and visualization tool
"""
import streamlit as st
import matplotlib.pyplot as plt
import io
import json
from src.ingest import read_csv, sort_records, filter_records, delete_record
from src.transform import add_computed_fields, compute_improvement
from src.analyze import (compute_stats, grade_distribution, identify_at_risk,
                         section_comparison, top_performers, find_outliers,
                         compute_percentile)
from src.reports import export_to_csv, export_at_risk_list


# Page configuration
st.set_page_config(
    page_title="Academic Analytics Lite",
    page_icon="📊",
    layout="wide"
)

# Load configuration


@st.cache_data
def load_config():
    """Load configuration from JSON file."""
    try:
        with open('config.json', 'r') as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Error loading config: {e}")
        return None


def process_uploaded_file(uploaded_file, weights, grade_scale):
    """Process uploaded CSV file."""
    # Save uploaded file temporarily
    with open("temp_upload.csv", "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Read and process
    records, errors = read_csv("temp_upload.csv")

    if errors:
        with st.expander("⚠️ Data Validation Warnings", expanded=False):
            for error in errors:
                st.warning(error)

    # Add computed fields
    records = add_computed_fields(records, weights, grade_scale)

    # Add improvement metric
    for record in records:
        record['improvement'] = compute_improvement(record)

    return records


def plot_grade_distribution(distribution):
    """Create bar chart for grade distribution."""
    fig, ax = plt.subplots(figsize=(8, 5))

    grades = ['A', 'B', 'C', 'D', 'F']
    counts = [distribution.get(g, 0) for g in grades]
    colors = ['#2ecc71', '#3498db', '#f39c12', '#e67e22', '#e74c3c']

    bars = ax.bar(grades, counts, color=colors, alpha=0.7, edgecolor='black')

    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}',
                ha='center', va='bottom', fontweight='bold')

    ax.set_xlabel('Letter Grade', fontsize=12, fontweight='bold')
    ax.set_ylabel('Number of Students', fontsize=12, fontweight='bold')
    ax.set_title('Grade Distribution', fontsize=14, fontweight='bold')
    ax.grid(axis='y', alpha=0.3)

    return fig


def plot_section_comparison(section_stats):
    """Create bar chart comparing sections."""
    fig, ax = plt.subplots(figsize=(10, 5))

    sections = list(section_stats.keys())
    means = [section_stats[s]['mean'] for s in sections]

    bars = ax.bar(sections, means, color='#3498db',
                  alpha=0.7, edgecolor='black')

    # Add value labels
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}',
                ha='center', va='bottom', fontweight='bold')

    ax.set_xlabel('Section', fontsize=12, fontweight='bold')
    ax.set_ylabel('Mean Grade', fontsize=12, fontweight='bold')
    ax.set_title('Section Performance Comparison',
                 fontsize=14, fontweight='bold')
    ax.set_ylim(0, 100)
    ax.grid(axis='y', alpha=0.3)

    return fig


def plot_score_histogram(valid_grades):
    """Create histogram of final grades."""
    fig, ax = plt.subplots(figsize=(10, 5))

    ax.hist(valid_grades, bins=20, color='#9b59b6',
            alpha=0.7, edgecolor='black')

    ax.set_xlabel('Final Grade', fontsize=12, fontweight='bold')
    ax.set_ylabel('Frequency', fontsize=12, fontweight='bold')
    ax.set_title('Final Grade Distribution', fontsize=14, fontweight='bold')
    ax.grid(axis='y', alpha=0.3)

    return fig


def plot_box_plot(valid_grades):
    """Create box plot of grades."""
    fig, ax = plt.subplots(figsize=(8, 6))

    bp = ax.boxplot([valid_grades], vert=True, patch_artist=True,
                    tick_labels=['Final Grades'])

    # Customize colors
    for patch in bp['boxes']:
        patch.set_facecolor('#3498db')
        patch.set_alpha(0.7)

    ax.set_ylabel('Grade', fontsize=12, fontweight='bold')
    ax.set_title('Grade Distribution Box Plot', fontsize=14, fontweight='bold')
    ax.grid(axis='y', alpha=0.3)

    return fig


def main():
    """Main Streamlit application."""

    st.title("📊 Academic Analytics Lite")
    st.markdown("**Interactive Student Performance Analysis Tool**")
    st.markdown("---")

    # Load configuration
    config = load_config()
    if not config:
        st.error("Failed to load configuration. Please check config.json")
        return

    weights = config['weights']
    thresholds = config['thresholds']
    grade_scale = config['grade_scale']

    # Sidebar for configuration
    with st.sidebar:
        st.header("⚙️ Configuration")

        st.subheader("Grade Weights")
        quiz_weight = st.slider("Quizzes", 0.0, 1.0, weights['quizzes'], 0.05)
        midterm_weight = st.slider(
            "Midterm", 0.0, 1.0, weights['midterm'], 0.05)
        final_weight = st.slider("Final", 0.0, 1.0, weights['final'], 0.05)
        attendance_weight = st.slider(
            "Attendance", 0.0, 1.0, weights['attendance'], 0.05)

        # Update weights
        weights = {
            'quizzes': quiz_weight,
            'midterm': midterm_weight,
            'final': final_weight,
            'attendance': attendance_weight
        }

        total_weight = sum(weights.values())
        if abs(total_weight - 1.0) > 0.01:
            st.warning(f"⚠️ Weights sum to {total_weight:.2f}, not 1.0")

        st.subheader("Thresholds")
        at_risk_threshold = st.number_input("At-Risk Threshold", 0, 100,
                                            int(thresholds['at_risk']))

    # File upload
    st.header("1️⃣ Upload CSV File")
    uploaded_file = st.file_uploader("Choose a CSV file", type=['csv'])

    # Use sample data option
    use_sample = st.checkbox("Use sample data (data/input.csv)")

    if uploaded_file or use_sample:

        # Process data
        if use_sample:
            records, errors = read_csv("data/input.csv")
            if errors:
                with st.expander("⚠️ Data Validation Warnings", expanded=False):
                    for error in errors:
                        st.warning(error)
            records = add_computed_fields(records, weights, grade_scale)
            for record in records:
                record['improvement'] = compute_improvement(record)
        else:
            records = process_uploaded_file(
                uploaded_file, weights, grade_scale)

        st.success(f"✅ Loaded {len(records)} student records")

        # Store in session state
        st.session_state['records'] = records

        # Tabs for different sections
        tab1, tab2, tab3, tab4 = st.tabs([
            "📋 Data View",
            "📊 Analytics",
            "🔧 Operations",
            "📥 Reports"
        ])

        # TAB 1: Data View
        with tab1:
            st.header("Student Records")

            # Display options
            col1, col2 = st.columns(2)
            with col1:
                sort_by = st.selectbox("Sort by",
                                       ['student_id', 'last_name', 'final_grade', 'section'])
            with col2:
                sort_order = st.radio("Order", ['Ascending', 'Descending'],
                                      horizontal=True)

            # Sort records
            sorted_records = sort_records(records, sort_by,
                                          reverse=(sort_order == 'Descending'))

            # Display table
            display_data = []
            for r in sorted_records:
                display_data.append({
                    'ID': r['student_id'],
                    'Name': f"{r['first_name']} {r['last_name']}",
                    'Section': r['section'],
                    'Quiz Avg': f"{r['quiz_average']:.1f}" if r['quiz_average'] else 'N/A',
                    'Midterm': r['midterm'] if r['midterm'] else 'N/A',
                    'Final Exam': r['final'] if r['final'] else 'N/A',
                    'Final Grade': f"{r['final_grade']:.2f}" if r['final_grade'] else 'N/A',
                    'Letter': r['letter_grade'],
                    'Attendance': f"{r['attendance_percent']:.0f}%" if r['attendance_percent'] else 'N/A'
                })

            st.dataframe(display_data, width='stretch', height=400)

        # TAB 2: Analytics
        with tab2:
            st.header("Statistical Analysis")

            # Extract valid grades
            valid_grades = [r['final_grade'] for r in records
                            if r['final_grade'] is not None]

            if not valid_grades:
                st.warning("No valid grades to analyze")
                return

            # Statistics
            stats = compute_stats(valid_grades)
            distribution = grade_distribution(records)

            # Display stats
            col1, col2, col3, col4, col5 = st.columns(5)
            col1.metric("Mean", f"{stats['mean']:.2f}")
            col2.metric("Median", f"{stats['median']:.2f}")
            col3.metric("Std Dev", f"{stats['std']:.2f}")
            col4.metric("Min", f"{stats['min']:.2f}")
            col5.metric("Max", f"{stats['max']:.2f}")

            st.markdown("---")

            # Visualizations
            col1, col2 = st.columns(2)

            with col1:
                st.subheader("Grade Distribution")
                fig1 = plot_grade_distribution(distribution)
                st.pyplot(fig1)
                plt.close()

            with col2:
                st.subheader("Score Histogram")
                fig2 = plot_score_histogram(valid_grades)
                st.pyplot(fig2)
                plt.close()

            col3, col4 = st.columns(2)

            with col3:
                st.subheader("Section Comparison")
                section_stats = section_comparison(records)
                fig3 = plot_section_comparison(section_stats)
                st.pyplot(fig3)
                plt.close()

            with col4:
                st.subheader("Box Plot")
                fig4 = plot_box_plot(valid_grades)
                st.pyplot(fig4)
                plt.close()

            # Percentiles
            st.markdown("---")
            st.subheader("Percentile Analysis")
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("25th Percentile",
                        f"{compute_percentile(valid_grades, 25):.2f}")
            col2.metric("50th Percentile",
                        f"{compute_percentile(valid_grades, 50):.2f}")
            col3.metric("75th Percentile",
                        f"{compute_percentile(valid_grades, 75):.2f}")
            col4.metric("90th Percentile",
                        f"{compute_percentile(valid_grades, 90):.2f}")

            # Outliers
            outliers = find_outliers(valid_grades)
            if outliers:
                st.warning(
                    f"🔍 Found {len(outliers)} outlier grades: {[round(o, 2) for o in outliers]}")

            # At-risk students
            at_risk = identify_at_risk(records, at_risk_threshold)
            if at_risk:
                st.markdown("---")
                st.subheader(
                    f"⚠️ At-Risk Students (Grade < {at_risk_threshold})")
                at_risk_data = []
                for r in at_risk:
                    at_risk_data.append({
                        'ID': r['student_id'],
                        'Name': f"{r['first_name']} {r['last_name']}",
                        'Section': r['section'],
                        'Final Grade': f"{r['final_grade']:.2f}",
                        'Letter': r['letter_grade'],
                        'Attendance': f"{r['attendance_percent']:.0f}%" if r['attendance_percent'] else 'N/A'
                    })
                st.dataframe(at_risk_data, width='stretch')

            # Top performers
            st.markdown("---")
            st.subheader("🏆 Top 10 Performers")
            top_10 = top_performers(records, 10)
            top_data = []
            for r in top_10:
                top_data.append({
                    'Rank': top_10.index(r) + 1,
                    'ID': r['student_id'],
                    'Name': f"{r['first_name']} {r['last_name']}",
                    'Section': r['section'],
                    'Final Grade': f"{r['final_grade']:.2f}",
                    'Letter': r['letter_grade']
                })
            st.dataframe(top_data, width='stretch')

        # TAB 3: Operations
        with tab3:
            st.header("Array Operations")

            col1, col2 = st.columns(2)

            with col1:
                st.subheader("🔍 Filter Records")
                filter_section = st.selectbox("Filter by Section",
                                              ['All'] + sorted(list(set(r['section'] for r in records))))

                if filter_section != 'All':
                    filtered = filter_records(records,
                                              lambda r: r['section'] == filter_section)
                    st.info(
                        f"Found {len(filtered)} students in section {filter_section}")

                    display_filtered = []
                    for r in filtered:
                        display_filtered.append({
                            'ID': r['student_id'],
                            'Name': f"{r['first_name']} {r['last_name']}",
                            'Final Grade': f"{r['final_grade']:.2f}" if r['final_grade'] else 'N/A',
                            'Letter': r['letter_grade']
                        })
                    st.dataframe(display_filtered, width='stretch')

            with col2:
                st.subheader("🗑️ Delete Record")
                student_ids = [r['student_id'] for r in records]
                delete_id = st.selectbox(
                    "Select Student ID to Delete", student_ids)

                if st.button("Delete Student", type="primary"):
                    updated_records = delete_record(records, delete_id)
                    st.session_state['records'] = updated_records
                    st.success(f"Deleted student {delete_id}")
                    st.rerun()

            st.markdown("---")
            st.subheader("📊 Project Fields")

            available_fields = ['student_id', 'first_name', 'last_name', 'section',
                                'final_grade', 'letter_grade', 'attendance_percent']
            selected_fields = st.multiselect("Select fields to display",
                                             available_fields, default=['student_id', 'first_name', 'last_name', 'final_grade'])

            if selected_fields:
                projected_data = []
                for r in records:
                    row = {}
                    for field in selected_fields:
                        value = r.get(field)
                        if field == 'final_grade' and value is not None:
                            row[field] = f"{value:.2f}"
                        elif field == 'attendance_percent' and value is not None:
                            row[field] = f"{value:.0f}%"
                        else:
                            row[field] = value if value is not None else 'N/A'
                    projected_data.append(row)

                st.dataframe(projected_data, width='stretch', height=300)

        # TAB 4: Reports
        with tab4:
            st.header("Export Reports")

            col1, col2 = st.columns(2)

            with col1:
                st.subheader("📄 Export All Records")
                if st.button("Download All Records CSV"):
                    # Create CSV in memory
                    output = io.StringIO()
                    import csv

                    fields = ['student_id', 'last_name', 'first_name', 'section',
                              'quiz_average', 'midterm', 'final', 'final_grade',
                              'letter_grade', 'attendance_percent']

                    writer = csv.DictWriter(
                        output, fieldnames=fields, extrasaction='ignore')
                    writer.writeheader()
                    writer.writerows(records)

                    st.download_button(
                        label="📥 Download CSV",
                        data=output.getvalue(),
                        file_name="all_students.csv",
                        mime="text/csv"
                    )

            with col2:
                st.subheader("⚠️ Export At-Risk Students")
                at_risk = identify_at_risk(records, at_risk_threshold)

                if at_risk:
                    if st.button("Download At-Risk List CSV"):
                        output = io.StringIO()
                        import csv

                        fields = ['student_id', 'last_name', 'first_name', 'section',
                                  'final_grade', 'letter_grade', 'attendance_percent']

                        writer = csv.DictWriter(
                            output, fieldnames=fields, extrasaction='ignore')
                        writer.writeheader()
                        writer.writerows(at_risk)

                        st.download_button(
                            label="📥 Download CSV",
                            data=output.getvalue(),
                            file_name="at_risk_students.csv",
                            mime="text/csv"
                        )
                else:
                    st.info("No at-risk students found")

            st.markdown("---")
            st.subheader("📊 Export by Section")

            sections = sorted(list(set(r['section'] for r in records)))

            for section in sections:
                section_records = filter_records(records,
                                                 lambda r: r['section'] == section)

                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(
                        f"**Section {section}**: {len(section_records)} students")
                with col2:
                    output = io.StringIO()
                    import csv

                    fields = ['student_id', 'last_name', 'first_name',
                              'final_grade', 'letter_grade']

                    writer = csv.DictWriter(
                        output, fieldnames=fields, extrasaction='ignore')
                    writer.writeheader()
                    writer.writerows(section_records)

                    st.download_button(
                        label=f"📥 Section {section}",
                        data=output.getvalue(),
                        file_name=f"section_{section}.csv",
                        mime="text/csv",
                        key=f"section_{section}"
                    )


if __name__ == "__main__":
    main()
