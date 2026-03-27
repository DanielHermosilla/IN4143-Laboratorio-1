from __future__ import annotations

from typing import Callable

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from scipy.stats import norm, t as student_t


DEPENDENT_VARIABLES = [
    "Probabilidad de resolver Sudoku",
    "Prob. Resolver Crucigrama de letras",
    "Capacidad de recordar nombres raros",
    "Habilidad para encontrar llaves perdidas",
    "Velocidad para resolver laberintos",
    "Precisión en recordar cumpleaños",
    "Eficiencia organizando calcetines",
    "Rapidez contando ovejas para dormir",
    "Destreza armando muebles de IKEA",
    "Intuición para adivinar contraseñas",
]

MAIN_AGE_GROUPS = {
    "Jóvenes (20-40)": "jovenes",
    "Adultos (40-60)": "adultos",
    "Veteranos (+60)": "veteranos",
}

BASE_COLORS = {
    DEPENDENT_VARIABLES[0]: "#66C2A5",
    DEPENDENT_VARIABLES[1]: "#FC8D62",
    DEPENDENT_VARIABLES[2]: "#8DA0CB",
    DEPENDENT_VARIABLES[3]: "#E78AC3",
    DEPENDENT_VARIABLES[4]: "#A6D854",
}

GROUP_ALPHA = {
    "Jóvenes (20-40)": 0.60,
    "Adultos (40-60)": 0.80,
    "Veteranos (+60)": 1.00,
    "Todos": 1.00,
}

REPLICATION_MODES = {
    "Análisis estándar": "standard",
    "Efectos heterogéneos por grupo etario": "age",
    "Múltiples variables dependientes": "multiple_variables",
}


def inject_styles() -> None:
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600&family=Space+Grotesk:wght@500;700&display=swap');

        .stApp,
        [data-testid="stAppViewContainer"] {
            background: #0b1118;
            color: #e2e8f0;
        }

        [data-testid="stHeader"] {
            background: rgba(11, 17, 24, 0.92);
        }

        [data-testid="stSidebar"] {
            background: #0f1722;
            border-right: 1px solid rgba(148, 163, 184, 0.10);
        }

        html, body, [class*="css"]  {
            font-family: "IBM Plex Sans", sans-serif;
        }

        h1, h2, h3,
        label,
        [data-testid="stMarkdownContainer"] p,
        [data-testid="stMarkdownContainer"] li,
        [data-testid="stCaptionContainer"] {
            color: #e2e8f0;
        }

        h1, h2, h3 {
            font-family: "Space Grotesk", sans-serif;
            letter-spacing: -0.02em;
        }

        div[data-baseweb="tab-list"] {
            background: rgba(15, 23, 42, 0.72);
            border: 1px solid rgba(148, 163, 184, 0.16);
            border-radius: 16px;
            padding: 0.3rem;
        }

        button[data-baseweb="tab"] {
            color: #cbd5e1;
            border-radius: 12px;
            font-size: 0.80rem;
            font-weight: 500;
            padding: 0.35rem 0.75rem;
        }

        button[data-baseweb="tab"][aria-selected="true"] {
            background: rgba(37, 99, 235, 0.22);
            color: #f8fafc;
        }

        div[data-testid="stMetric"] {
            background: rgba(15, 23, 42, 0.78);
            border: 1px solid rgba(148, 163, 184, 0.16);
            border-radius: 18px;
            padding: 0.9rem 1rem;
        }

        div[data-testid="stMetric"] * {
            color: #e2e8f0;
        }

        .main-intro {
            background: rgba(15, 23, 42, 0.42);
            border: 1px solid rgba(148, 163, 184, 0.12);
            border-radius: 20px;
            padding: 1.15rem 1.25rem;
            margin: 0.35rem 0 1.1rem;
        }

        .main-kicker {
            color: #60a5fa;
            font-size: 0.72rem;
            font-weight: 600;
            letter-spacing: 0.16em;
            text-transform: uppercase;
            margin-bottom: 0.45rem;
        }

        .main-intro h2 {
            margin: 0;
            color: #f8fafc;
            font-size: 1.9rem;
            line-height: 1.05;
        }

        .main-intro p {
            margin: 0.55rem 0 0;
            max-width: 56rem;
            color: #94a3b8;
            font-size: 0.98rem;
            line-height: 1.55;
        }

        .section-heading {
            margin: 1.5rem 0 0.55rem;
        }

        .section-heading h3 {
            margin: 0;
            color: #f8fafc;
            font-size: 1.7rem;
            line-height: 1.08;
        }

        .section-kicker {
            color: #94a3b8;
            font-size: 0.72rem;
            font-weight: 600;
            letter-spacing: 0.14em;
            text-transform: uppercase;
            margin-bottom: 0.35rem;
        }

        .legend-wrap {
            display: flex;
            flex-wrap: wrap;
            gap: 0.55rem 1rem;
            padding: 0.9rem 1rem;
            border: 1px solid rgba(148, 163, 184, 0.16);
            border-radius: 16px;
            background: rgba(15, 23, 42, 0.78);
            backdrop-filter: blur(8px);
            margin-bottom: 0.8rem;
        }

        .legend-title {
            width: 100%;
            font-weight: 600;
            color: #f8fafc;
            margin-bottom: 0.15rem;
        }

        .legend-item {
            display: inline-flex;
            align-items: center;
            gap: 0.45rem;
            font-size: 0.9rem;
            color: #e2e8f0;
            white-space: nowrap;
        }

        .legend-swatch {
            width: 12px;
            height: 12px;
            border-radius: 3px;
            display: inline-block;
            border: 1px solid rgba(248, 250, 252, 0.18);
        }

        .hint-text {
            color: #94a3b8;
            font-size: 0.95rem;
        }

        /* ── Hypothesis statement box ── */
        .hypothesis-box {
            background: rgba(15, 23, 42, 0.60);
            border: 1px solid rgba(148, 163, 184, 0.18);
            border-radius: 16px;
            padding: 1rem 1.25rem;
            margin: 0.5rem 0 1.2rem;
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
        }
        .hyp-row {
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }
        .hyp-label {
            background: rgba(239, 68, 68, 0.15);
            color: #fca5a5;
            border: 1px solid rgba(239, 68, 68, 0.25);
            border-radius: 6px;
            padding: 0.1rem 0.55rem;
            font-size: 0.85rem;
            font-weight: 700;
            font-family: "Space Grotesk", sans-serif;
            min-width: 2.4rem;
            text-align: center;
            flex-shrink: 0;
        }
        .hyp-label-alt {
            background: rgba(59, 130, 246, 0.15);
            color: #93c5fd;
            border-color: rgba(59, 130, 246, 0.25);
        }
        .hyp-text { color: #cbd5e1; font-size: 0.95rem; }
        .hyp-text strong { color: #f8fafc; }
        .hyp-formula {
            font-family: "IBM Plex Mono", "Courier New", monospace;
            color: #94a3b8;
            font-size: 0.88rem;
            padding: 0.35rem 0.7rem;
            background: rgba(0, 0, 0, 0.20);
            border-radius: 8px;
            margin-top: 0.2rem;
            display: inline-block;
            align-self: flex-start;
        }

        /* ── Control section label ── */
        .control-section-label {
            color: #60a5fa;
            font-size: 0.72rem;
            font-weight: 600;
            letter-spacing: 0.14em;
            text-transform: uppercase;
            margin-bottom: 0.5rem;
        }

        /* ── Multiple-tests warning ── */
        .tests-warning {
            background: rgba(245, 158, 11, 0.10);
            border: 1px solid rgba(245, 158, 11, 0.25);
            border-radius: 10px;
            color: #fcd34d;
            font-size: 0.87rem;
            padding: 0.5rem 0.75rem;
            margin-top: 0.5rem;
        }
        .tests-warning strong { color: #fde68a; }

        /* ── Verdict panels ── */
        .verdict-reject, .verdict-fail {
            display: flex;
            align-items: center;
            gap: 1.1rem;
            border-radius: 16px;
            padding: 1rem 1.25rem;
            margin: 1.1rem 0 0.6rem;
        }
        .verdict-reject {
            background: rgba(16, 185, 129, 0.10);
            border: 1px solid rgba(16, 185, 129, 0.28);
        }
        .verdict-fail {
            background: rgba(239, 68, 68, 0.09);
            border: 1px solid rgba(239, 68, 68, 0.22);
        }
        .verdict-icon { font-size: 1.55rem; width: 2rem; text-align: center; flex-shrink: 0; }
        .verdict-reject .verdict-icon { color: #34d399; }
        .verdict-fail    .verdict-icon { color: #f87171; }
        .verdict-body { flex: 1; min-width: 0; }
        .verdict-title {
            font-family: "Space Grotesk", sans-serif;
            font-size: 1.08rem;
            font-weight: 700;
            color: #f8fafc;
            line-height: 1.2;
        }
        .verdict-detail { font-size: 0.86rem; color: #94a3b8; margin-top: 0.2rem; }
        .verdict-stats { display: flex; gap: 1.4rem; flex-shrink: 0; }
        .verdict-stat  { display: flex; flex-direction: column; align-items: center; gap: 0.05rem; }
        .vs-label {
            font-size: 0.68rem; color: #64748b; font-weight: 600;
            letter-spacing: 0.07em; text-transform: uppercase;
        }
        .vs-value {
            font-family: "Space Grotesk", sans-serif;
            font-size: 1.0rem; font-weight: 700; color: #e2e8f0;
        }

        /* ── Empty state ── */
        .empty-state {
            text-align: center; padding: 2.8rem 1rem; color: #475569;
            border: 1px dashed rgba(148, 163, 184, 0.14);
            border-radius: 16px; margin-top: 1rem;
        }
        .empty-icon { font-size: 2.2rem; display: block; margin-bottom: 0.6rem; }
        .empty-state p { font-size: 0.96rem; margin: 0; color: #64748b; }
        .empty-state strong { color: #94a3b8; }

        </style>
        """,
        unsafe_allow_html=True,
    )


def initialize_state() -> None:
    if "current_sample" not in st.session_state:
        st.session_state.current_sample = None
    if "current_results" not in st.session_state:
        st.session_state.current_results = pd.DataFrame()
    if "current_results_config" not in st.session_state:
        st.session_state.current_results_config = None
    if "replication_results" not in st.session_state:
        st.session_state.replication_results = None
    if "replication_config" not in st.session_state:
        st.session_state.replication_config = None


def rgba(hex_color: str, alpha: float = 1.0) -> str:
    clean = hex_color.lstrip("#")
    red = int(clean[0:2], 16)
    green = int(clean[2:4], 16)
    blue = int(clean[4:6], 16)
    return f"rgba({red}, {green}, {blue}, {alpha:.2f})"


def generate_sample(n: int = 100, true_effect: float = 0.0) -> pd.DataFrame:
    rng = np.random.default_rng()
    treatment = np.resize(np.array([0, 1]), n)
    ages = np.rint(rng.uniform(20, 80, size=n)).astype(int)
    age_group = np.where(
        ages <= 40,
        "jovenes",
        np.where(ages <= 60, "adultos", "veteranos"),
    )
    outcome_base = rng.normal(0, 1, size=n) + treatment * true_effect

    data = {
        "treatment": treatment,
        "age": ages,
        "age_group": age_group,
        "id": np.arange(1, n + 1),
    }

    for index in range(1, len(DEPENDENT_VARIABLES) + 1):
        data[f"var_{index}"] = outcome_base + rng.normal(0, 0.3, size=n)

    return pd.DataFrame(data)


def filter_by_age_group(data: pd.DataFrame, group_code: str) -> pd.DataFrame:
    if group_code == "todos":
        return data.copy()
    return data.loc[data["age_group"] == group_code].copy()


def calculate_statistics(
    data: pd.DataFrame,
    var_index: int = 1,
    group_name: str = "Todos",
) -> dict[str, float | str | bool] | None:
    variable_name = f"var_{var_index}"
    treatment_data = data.loc[data["treatment"] == 1, variable_name].dropna()
    control_data = data.loc[data["treatment"] == 0, variable_name].dropna()

    if len(treatment_data) < 2 or len(control_data) < 2:
        return None

    mean_treatment = float(treatment_data.mean())
    mean_control = float(control_data.mean())
    beta = mean_treatment - mean_control
    var_treatment = float(treatment_data.var(ddof=1))
    var_control = float(control_data.var(ddof=1))
    n_treatment = int(treatment_data.shape[0])
    n_control = int(control_data.shape[0])

    pooled_var = (
        ((n_treatment - 1) * var_treatment) + ((n_control - 1) * var_control)
    ) / (n_treatment + n_control - 2)
    se_beta = float(np.sqrt(pooled_var * ((1 / n_treatment) + (1 / n_control))))

    if not np.isfinite(se_beta) or se_beta == 0:
        return None

    t_statistic = beta / se_beta
    degrees_of_freedom = n_treatment + n_control - 2
    p_value = float(2 * student_t.sf(abs(t_statistic), degrees_of_freedom))
    t_critical = float(student_t.ppf(0.975, degrees_of_freedom))
    ci_lower = beta - (t_critical * se_beta)
    ci_upper = beta + (t_critical * se_beta)

    return {
        "variable": DEPENDENT_VARIABLES[var_index - 1],
        "variable_index": var_index,
        "group": group_name,
        "beta": beta,
        "se_beta": se_beta,
        "t_statistic": t_statistic,
        "p_value": p_value,
        "ci_lower": ci_lower,
        "ci_upper": ci_upper,
        "n_total": int(data.shape[0]),
        "n_treatment": n_treatment,
        "n_control": n_control,
        "significant": p_value < 0.05,
    }


def run_analysis(
    sample_data: pd.DataFrame,
    analyze_by_age: bool,
    multiple_variables: bool,
    n_dependent_vars: int,
) -> pd.DataFrame:
    groups_to_analyze = MAIN_AGE_GROUPS if analyze_by_age else {"Todos": "todos"}
    variables_to_analyze = range(1, n_dependent_vars + 1) if multiple_variables else [1]

    rows: list[dict[str, float | str | int]] = []
    for variable_index in variables_to_analyze:
        for group_name, group_code in groups_to_analyze.items():
            group_data = filter_by_age_group(sample_data, group_code)
            if group_data.shape[0] < 4:
                continue

            statistics = calculate_statistics(group_data, variable_index, group_name)
            if statistics is None:
                continue

            rows.append(
                {
                    "Variable_Dependiente": statistics["variable"],
                    "Grupo_Etario": statistics["group"],
                    "Beta": round(float(statistics["beta"]), 4),
                    "Error_Std": round(float(statistics["se_beta"]), 4),
                    "T_Statistic": round(float(statistics["t_statistic"]), 3),
                    "P_Value": round(float(statistics["p_value"]), 4),
                    "IC_Inferior": round(float(statistics["ci_lower"]), 4),
                    "IC_Superior": round(float(statistics["ci_upper"]), 4),
                    "N_Total": int(statistics["n_total"]),
                }
            )

    return pd.DataFrame(rows)


def run_replication_study(
    n_replications: int,
    sample_size: int,
    true_effect: float,
    mode: str,
    n_dependent_vars: int,
    progress_callback: Callable[[int, int], None] | None = None,
) -> pd.DataFrame:
    variables_to_test = (
        range(1, n_dependent_vars + 1) if mode == "multiple_variables" else [1]
    )
    rows: list[dict[str, int | bool]] = []

    for replication_index in range(1, n_replications + 1):
        sample_data = generate_sample(n=sample_size, true_effect=true_effect)

        stats_all = calculate_statistics(sample_data, 1, "Todos")
        rejected_todos = bool(stats_all and stats_all["p_value"] < 0.05)

        rejected_any_var = False
        if mode == "multiple_variables" and n_dependent_vars > 1:
            rejected_any_var = any(
                bool(stats and stats["p_value"] < 0.05)
                for stats in (
                    calculate_statistics(sample_data, variable_index, "Todos")
                    for variable_index in variables_to_test
                )
            )

        rejected_any_subgroup = False
        if mode == "age":
            subgroup_rejections = []
            for group_name, group_code in MAIN_AGE_GROUPS.items():
                subgroup_data = filter_by_age_group(sample_data, group_code)
                if subgroup_data.shape[0] < 4:
                    continue
                stats = calculate_statistics(subgroup_data, 1, group_name)
                subgroup_rejections.append(bool(stats and stats["p_value"] < 0.05))
            rejected_any_subgroup = any(subgroup_rejections)

        rows.append(
            {
                "replication": replication_index,
                "rejected_todos": rejected_todos,
                "rejected_any_var": rejected_any_var,
                "rejected_any_subgroup": rejected_any_subgroup,
            }
        )

        if progress_callback is not None:
            progress_callback(replication_index, n_replications)

    return pd.DataFrame(rows)


def current_context_text(config: dict[str, object]) -> str:
    analyze_by_age = bool(config.get("analyze_by_age", False))
    multiple_variables = bool(config.get("multiple_variables", False))
    true_effect = float(config.get("true_effect", 0.0))

    if multiple_variables and analyze_by_age:
        analysis_label = "Múltiples variables y múltiples grupos"
    elif multiple_variables:
        analysis_label = "Múltiples variables"
    elif analyze_by_age:
        analysis_label = "Múltiples grupos etarios"
    else:
        analysis_label = "Análisis simple"

    return f"{analysis_label} | Efecto real de TralaleroTralaLex: {true_effect:.1f}"


def build_analysis_summary(results: pd.DataFrame) -> str:
    if results.empty:
        return ""

    n_variables = results["Variable_Dependiente"].nunique()
    n_groups = results["Grupo_Etario"].nunique()
    n_significant = int((results["P_Value"] < 0.05).sum())
    return (
        f"Simulación actual: {n_variables} variables x {n_groups} grupos = "
        f"{len(results)} análisis totales. {n_significant} con p < 0.05."
    )


def plot_color(variable_name: str, group_name: str, analyze_by_age: bool) -> str:
    base_color = BASE_COLORS.get(variable_name, "#0f766e")
    alpha = GROUP_ALPHA.get(group_name, 1.0) if analyze_by_age else 1.0
    return rgba(base_color, alpha)


def build_legend_html(results: pd.DataFrame, analyze_by_age: bool) -> str:
    if results.empty:
        return ""

    unique_rows = (
        results[["Variable_Dependiente", "Grupo_Etario"]]
        .drop_duplicates()
        .reset_index(drop=True)
    )

    items = []
    for _, row in unique_rows.iterrows():
        label = f"{row['Variable_Dependiente']} - {row['Grupo_Etario']}"
        color = plot_color(
            row["Variable_Dependiente"],
            row["Grupo_Etario"],
            analyze_by_age,
        )
        items.append(
            f'<span class="legend-item"><span class="legend-swatch" '
            f'style="background:{color};"></span>{label}</span>'
        )

    return (
        '<div class="legend-wrap">'
        '<div class="legend-title">Leyenda de t-statistics</div>'
        + "".join(items)
        + "</div>"
    )


def build_theoretical_plot(results: pd.DataFrame, analyze_by_age: bool) -> go.Figure:
    x_values = np.arange(-4.5, 4.6, 0.1)
    y_values = norm.pdf(x_values, loc=0, scale=1)
    critical_value = 1.96

    figure = go.Figure()
    figure.add_trace(
        go.Scatter(
            x=x_values,
            y=y_values,
            mode="lines",
            line={"color": "#f8fafc", "width": 3},
            name="Distribución teórica",
            hovertemplate="t=%{x:.2f}<br>Densidad=%{y:.3f}<extra></extra>",
        )
    )

    figure.add_vline(
        x=-critical_value, line_color="#dc2626", line_dash="dash", line_width=2
    )
    figure.add_vline(
        x=critical_value, line_color="#dc2626", line_dash="dash", line_width=2
    )
    figure.add_vline(x=0, line_color="#64748b", line_dash="dot", line_width=1)

    if not results.empty:
        for _, row in results.iterrows():
            figure.add_vline(
                x=float(row["T_Statistic"]),
                line_color=plot_color(
                    row["Variable_Dependiente"],
                    row["Grupo_Etario"],
                    analyze_by_age,
                ),
                line_width=2.5,
            )

    figure.add_annotation(
        x=critical_value + 0.35,
        y=float(y_values.max() * 0.90),
        text="Crítico si |t| > 1.96",
        showarrow=False,
        font={"color": "#dc2626", "size": 12},
    )

    figure.update_layout(
        title="Distribución teórica del t-statistic",
        xaxis_title="T-Statistic",
        yaxis_title="Densidad de probabilidad",
        margin={"l": 20, "r": 20, "t": 60, "b": 20},
        height=430,
        showlegend=False,
        font={"color": "#e2e8f0"},
        paper_bgcolor="#0b1118",
        plot_bgcolor="#0b1118",
    )
    figure.update_xaxes(showgrid=False, color="#e2e8f0")
    figure.update_yaxes(
        showgrid=True,
        gridcolor="rgba(148, 163, 184, 0.16)",
        zeroline=False,
        color="#e2e8f0",
    )
    return figure


def build_replication_caption(
    mode: str, n_dependent_vars: int, true_effect: float
) -> str:
    prefix = "La línea azul muestra la tasa acumulada de estudios con p < 0.05 usando toda la muestra. "

    if mode == "multiple_variables":
        suffix = (
            f"La línea verde muestra la proporción de estudios donde al menos una de las "
            f"{n_dependent_vars} variables fue significativa."
        )
    elif mode == "age":
        suffix = (
            "La línea naranja muestra la proporción de estudios donde al menos uno de los "
            "subgrupos etarios fue significativo."
        )
    else:
        suffix = "Este escenario corresponde al análisis estándar."

    if true_effect == 0:
        return (
            prefix
            + suffix
            + " La referencia roja punteada marca el 5% esperado bajo la hipótesis nula."
        )

    return prefix + suffix


def build_replication_plot(
    replication_results: pd.DataFrame,
    mode: str,
    n_dependent_vars: int,
    true_effect: float,
) -> go.Figure:
    data = replication_results.copy()
    steps = np.arange(1, len(data) + 1)
    data["cumulative_todos"] = data["rejected_todos"].astype(int).cumsum() / steps
    data["cumulative_any_var"] = data["rejected_any_var"].astype(int).cumsum() / steps
    data["cumulative_any_subgroup"] = (
        data["rejected_any_subgroup"].astype(int).cumsum() / steps
    )

    figure = go.Figure()
    figure.add_trace(
        go.Scatter(
            x=data["replication"],
            y=data["cumulative_todos"],
            mode="lines",
            line={"color": "#60a5fa", "width": 3},
            name="Todos los datos",
            hovertemplate="Estudio %{x}<br>Tasa %{y:.1%}<extra></extra>",
        )
    )

    if mode == "multiple_variables":
        figure.add_trace(
            go.Scatter(
                x=data["replication"],
                y=data["cumulative_any_var"],
                mode="lines",
                line={"color": "#34d399", "width": 3, "dash": "dash"},
                name="Al menos una variable",
                hovertemplate="Estudio %{x}<br>Tasa %{y:.1%}<extra></extra>",
            )
        )

    if mode == "age":
        figure.add_trace(
            go.Scatter(
                x=data["replication"],
                y=data["cumulative_any_subgroup"],
                mode="lines",
                line={"color": "#fbbf24", "width": 3, "dash": "dash"},
                name="Al menos un subgrupo",
                hovertemplate="Estudio %{x}<br>Tasa %{y:.1%}<extra></extra>",
            )
        )

    if true_effect == 0:
        figure.add_hline(y=0.05, line_color="#fb7185", line_dash="dot", line_width=2)

    max_y = data["cumulative_todos"].max()
    if mode == "multiple_variables":
        max_y = max(max_y, data["cumulative_any_var"].max())
    if mode == "age":
        max_y = max(max_y, data["cumulative_any_subgroup"].max())
    if true_effect == 0:
        max_y = max(max_y, 0.05)

    figure.update_layout(
        title="Evolución de la tasa de p-valores < 0.05",
        xaxis_title="Número de estudios acumulados",
        yaxis_title="Proporción acumulada",
        yaxis={"tickformat": ".0%", "range": [0, min(1.0, float(max_y) * 1.1 + 0.02)]},
        legend={
            "orientation": "h",
            "yanchor": "bottom",
            "y": 1.02,
            "xanchor": "left",
            "x": 0,
        },
        margin={"l": 20, "r": 20, "t": 60, "b": 20},
        height=560,
        font={"color": "#e2e8f0"},
        paper_bgcolor="#0b1118",
        plot_bgcolor="#0b1118",
    )
    figure.update_xaxes(showgrid=False, color="#e2e8f0")
    figure.update_yaxes(
        showgrid=True,
        gridcolor="rgba(148, 163, 184, 0.16)",
        zeroline=False,
        color="#e2e8f0",
    )

    return figure


def style_results_dataframe(results: pd.DataFrame) -> pd.io.formats.style.Styler:
    formatting = {
        "Beta": "{:.4f}",
        "Error_Std": "{:.4f}",
        "T_Statistic": "{:.3f}",
        "P_Value": "{:.4f}",
        "IC_Inferior": "{:.4f}",
        "IC_Superior": "{:.4f}",
    }

    def highlight_significance(values: pd.Series) -> list[str]:
        return [
            "background-color: rgba(16,185,129,0.18); color: #6ee7b7; font-weight: 700;"
            if value < 0.05
            else "color: #94a3b8;"
            for value in values
        ]

    return (
        results.style.format(formatting)
        .apply(highlight_significance, subset=["P_Value"])
        .hide(axis="index")
    )


def render_main_tab() -> None:
    # ── Hero ──────────────────────────────────────────────────────────────────
    st.markdown(
        """
        <div class="main-intro">
          <div class="main-kicker">Laboratorio 1 · IN4143</div>
          <h2>TralaleroTralaLex 💊</h2>
          <p>
            Simula el experimento tratamiento vs. placebo y observa cómo cambian el p-valor
            y el t-statistic al modificar el tamaño muestral, los grupos etarios y la cantidad
            de variables dependientes.
          </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Modelo e hipótesis ────────────────────────────────────────────────────
    st.markdown(
        """
        <div class="hypothesis-box">
          <div class="hyp-row">
            <span class="hyp-label">H₀</span>
            <span class="hyp-text">β = 0 &nbsp;—&nbsp; TralaleroTralaLex <strong>no tiene efecto</strong> sobre el desempeño cognitivo</span>
          </div>
          <div class="hyp-row">
            <span class="hyp-label hyp-label-alt">H₁</span>
            <span class="hyp-text">β ≠ 0 &nbsp;—&nbsp; TralaleroTralaLex <strong>sí tiene algún efecto</strong> (positivo o negativo)</span>
          </div>
          <div class="hyp-formula">Y<sub>i</sub> = α + β × Tratados<sub>i</sub> + ε<sub>i</sub> &nbsp;·&nbsp; Rechazamos H₀ si |t| > 1.96 &nbsp;(α = 5%)</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Controles ─────────────────────────────────────────────────────────────
    left_col, right_col = st.columns([1, 1], gap="large")

    with left_col:
        st.markdown(
            '<div class="control-section-label">Parámetros del experimento</div>',
            unsafe_allow_html=True,
        )
        true_effect = st.slider(
            "Efecto verdadero de la droga (β real)",
            min_value=0.0,
            max_value=1.0,
            value=0.0,
            step=0.1,
            key="main_true_effect",
            help="0 = H₀ verdadera (sin efecto real). Valores mayores simulan una droga que sí funciona.",
        )
        st.caption(
            "↳ Sin efecto — H₀ es verdadera"
            if true_effect == 0
            else f"↳ Efecto real de {true_effect:.1f} pts — H₀ es **falsa**"
        )

        sample_size = st.slider(
            "Tamaño de muestra (n)",
            min_value=20,
            max_value=500,
            value=100,
            step=10,
            key="main_sample_size",
            help="Mayor n → mayor potencia estadística → más fácil detectar efectos reales pequeños.",
        )
        st.caption(
            f"↳ {sample_size} participantes "
            f"({sample_size // 2} tratamiento + {sample_size // 2} control)"
        )

    with right_col:
        st.markdown(
            '<div class="control-section-label">Opciones de análisis</div>',
            unsafe_allow_html=True,
        )
        analyze_by_age = st.checkbox(
            "Dividir por grupos de edad",
            value=False,
            key="main_analyze_by_age",
            help="Genera 3 tests por variable (jóvenes, adultos, veteranos). Multiplica los falsos positivos potenciales.",
        )
        if analyze_by_age:
            st.caption("↳ Jóvenes (20-40) · Adultos (40-60) · Veteranos (+60)")

        n_dependent_vars = st.slider(
            "Variables dependientes simultáneas",
            min_value=1,
            max_value=5,
            value=1,
            step=1,
            key="main_n_dependent_vars",
            help="Más variables = más tests = mayor probabilidad de al menos un falso positivo accidental.",
        )
        multiple_variables = n_dependent_vars > 1
        if multiple_variables:
            st.caption(
                "↳ " + " · ".join(DEPENDENT_VARIABLES[:n_dependent_vars])
            )

        n_groups = 3 if analyze_by_age else 1
        n_total_tests = n_dependent_vars * n_groups
        if n_total_tests > 1:
            st.markdown(
                f'<div class="tests-warning">⚠️ Se ejecutarán <strong>{n_total_tests} tests</strong> simultáneos '
                f"({n_dependent_vars} var. × {n_groups} grupo{'s' if n_groups > 1 else ''})"
                f" — riesgo de comparaciones múltiples</div>",
                unsafe_allow_html=True,
            )

    # ── Botones de acción ──────────────────────────────────────────────────────
    btn_col, reset_col = st.columns([3, 1])
    get_sample = btn_col.button(
        "Conseguir muestra →",
        use_container_width=True,
        type="primary",
        key="main_get_sample",
    )
    reset = reset_col.button(
        "Limpiar",
        use_container_width=True,
        key="main_reset",
    )

    if get_sample:
        sample_data = generate_sample(n=sample_size, true_effect=true_effect)
        st.session_state.current_sample = sample_data
        st.session_state.current_results = run_analysis(
            sample_data=sample_data,
            analyze_by_age=analyze_by_age,
            multiple_variables=multiple_variables,
            n_dependent_vars=n_dependent_vars,
        )
        st.session_state.current_results_config = {
            "true_effect": true_effect,
            "sample_size": sample_size,
            "analyze_by_age": analyze_by_age,
            "multiple_variables": multiple_variables,
            "n_dependent_vars": n_dependent_vars,
        }

    if reset:
        st.session_state.current_sample = None
        st.session_state.current_results = pd.DataFrame()
        st.session_state.current_results_config = None
        st.session_state.replication_results = None
        st.session_state.replication_config = None

    current_results = st.session_state.current_results
    current_config = st.session_state.current_results_config or {
        "true_effect": true_effect,
        "sample_size": sample_size,
        "analyze_by_age": analyze_by_age,
        "multiple_variables": multiple_variables,
        "n_dependent_vars": n_dependent_vars,
    }

    # ── Estado vacío ───────────────────────────────────────────────────────────
    if current_results.empty:
        st.markdown(
            """
            <div class="empty-state">
              <span class="empty-icon">🧪</span>
              <p>Configura el experimento arriba y haz clic en <strong>Conseguir muestra</strong> para comenzar.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    # ── Veredicto del test principal ───────────────────────────────────────────
    main_row = current_results.iloc[0]
    p_main = float(main_row["P_Value"])
    beta_main = float(main_row["Beta"])
    t_main = float(main_row["T_Statistic"])

    if p_main < 0.05:
        v_class = "verdict-reject"
        v_icon = "✓"
        v_title = "Rechazamos H₀ con α = 5%"
        v_detail = f"p = {p_main:.4f} &lt; 0.05 — resultado estadísticamente significativo"
    else:
        v_class = "verdict-fail"
        v_icon = "✗"
        v_title = "No rechazamos H₀ con α = 5%"
        v_detail = f"p = {p_main:.4f} ≥ 0.05 — sin evidencia suficiente contra H₀"

    st.markdown(
        f"""
        <div class="{v_class}">
          <div class="verdict-icon">{v_icon}</div>
          <div class="verdict-body">
            <div class="verdict-title">{v_title}</div>
            <div class="verdict-detail">{v_detail}</div>
          </div>
          <div class="verdict-stats">
            <div class="verdict-stat"><span class="vs-label">β̂</span><span class="vs-value">{beta_main:+.4f}</span></div>
            <div class="verdict-stat"><span class="vs-label">t</span><span class="vs-value">{t_main:.3f}</span></div>
            <div class="verdict-stat"><span class="vs-label">p</span><span class="vs-value">{p_main:.4f}</span></div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Métricas resumen ───────────────────────────────────────────────────────
    significant_count = int((current_results["P_Value"] < 0.05).sum())
    total_tests = len(current_results)
    proportion = significant_count / total_tests

    m1, m2, m3 = st.columns(3)
    m1.metric(
        "Tests realizados",
        total_tests,
        help="Variables × grupos analizados en esta muestra",
    )
    m2.metric(
        "p < 0.05",
        significant_count,
        help="Tests con resultado estadísticamente significativo",
    )
    m3.metric(
        "Tasa significativa",
        f"{proportion:.0%}",
        delta=(
            f"{proportion - 0.05:+.0%} vs α esperado"
            if float(current_config.get("true_effect", 0.0)) == 0.0
            else None
        ),
        help="Con H₀ verdadera esperamos ≈ 5% de significativos por azar puro",
    )

    # ── Gráfico + Tabla lado a lado ────────────────────────────────────────────
    chart_col, table_col = st.columns([1.1, 1], gap="large")

    with chart_col:
        st.markdown(
            """
            <div class="section-heading">
              <div class="section-kicker">Visualización</div>
              <h3>Distribución t bajo H₀</h3>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.caption(current_context_text(current_config))
        st.html(
            build_legend_html(
                current_results,
                bool(current_config.get("analyze_by_age", False)),
            )
        )
        st.plotly_chart(
            build_theoretical_plot(
                current_results,
                bool(current_config.get("analyze_by_age", False)),
            ),
            use_container_width=True,
        )

    with table_col:
        st.markdown(
            """
            <div class="section-heading">
              <div class="section-kicker">Tabla de resultados</div>
              <h3>Resumen estadístico</h3>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.caption(build_analysis_summary(current_results))
        st.dataframe(
            style_results_dataframe(current_results),
            use_container_width=True,
        )


def render_replication_tab() -> None:
    controls_column, chart_column = st.columns([1, 1.8], gap="large")

    with controls_column:
        st.subheader("Estudio de replicación")
        n_replications = int(
            st.number_input(
                "Número de estudios",
                min_value=50,
                max_value=2000,
                value=500,
                step=50,
                key="replication_n_replications",
            )
        )
        replication_sample_size = int(
            st.number_input(
                "Participantes por estudio",
                min_value=20,
                max_value=500,
                value=100,
                step=10,
                key="replication_sample_size",
            )
        )
        replication_true_effect = float(
            st.number_input(
                "Efecto real de la droga",
                min_value=0.0,
                max_value=1.0,
                value=0.0,
                step=0.1,
                format="%.1f",
                key="replication_true_effect",
            )
        )
        mode_label = st.radio(
            "Opciones avanzadas",
            options=list(REPLICATION_MODES.keys()),
            help="En la replicación se activa a lo sumo una opción avanzada a la vez.",
            key="replication_mode",
        )
        mode = REPLICATION_MODES[mode_label]

        replication_n_dependent_vars = 1
        if mode == "multiple_variables":
            replication_n_dependent_vars = st.slider(
                "Número de variables",
                min_value=2,
                max_value=5,
                value=3,
                step=1,
                key="replication_n_dependent_vars",
            )

        if st.button(
            "Ejecutar meta-estudio",
            use_container_width=True,
            type="primary",
            key="run_replication",
        ):
            progress_bar = st.progress(0.0, text="Preparando meta-estudio...")

            def update_progress(step: int, total: int) -> None:
                progress_bar.progress(step / total, text=f"Estudio {step} de {total}")

            st.session_state.replication_results = run_replication_study(
                n_replications=n_replications,
                sample_size=replication_sample_size,
                true_effect=replication_true_effect,
                mode=mode,
                n_dependent_vars=replication_n_dependent_vars,
                progress_callback=update_progress,
            )
            st.session_state.replication_config = {
                "n_replications": n_replications,
                "sample_size": replication_sample_size,
                "true_effect": replication_true_effect,
                "mode": mode,
                "n_dependent_vars": replication_n_dependent_vars,
            }
            progress_bar.empty()

    with chart_column:
        replication_results = st.session_state.replication_results
        replication_config = st.session_state.replication_config

        if (
            replication_results is None
            or replication_results.empty
            or replication_config is None
        ):
            st.info(
                "Ejecuta el meta-estudio para ver cómo evoluciona la tasa acumulada de rechazos."
            )
            return

        final_columns = st.columns(3)
        final_columns[0].metric(
            "Estudios corridos",
            int(replication_results["replication"].max()),
        )
        final_columns[1].metric(
            "Tasa final: todos los datos",
            f"{replication_results['rejected_todos'].mean():.1%}",
        )

        mode = str(replication_config["mode"])
        if mode == "multiple_variables":
            final_metric = replication_results["rejected_any_var"].mean()
            final_label = "Tasa final: al menos una variable"
        elif mode == "age":
            final_metric = replication_results["rejected_any_subgroup"].mean()
            final_label = "Tasa final: al menos un subgrupo"
        else:
            final_metric = replication_results["rejected_todos"].mean()
            final_label = "Tasa final: análisis estándar"

        final_columns[2].metric(final_label, f"{final_metric:.1%}")
        st.plotly_chart(
            build_replication_plot(
                replication_results=replication_results,
                mode=mode,
                n_dependent_vars=int(replication_config["n_dependent_vars"]),
                true_effect=float(replication_config["true_effect"]),
            ),
            use_container_width=True,
        )
        st.caption(
            build_replication_caption(
                mode=mode,
                n_dependent_vars=int(replication_config["n_dependent_vars"]),
                true_effect=float(replication_config["true_effect"]),
            )
        )


def main() -> None:
    st.set_page_config(
        page_title="TralaleroTralaLex",
        layout="wide",
    )
    inject_styles()
    initialize_state()

    st.title("Simulador de Inferencia Causal")
    st.markdown(
        '<p class="hint-text">Laboratorio 1.</p>',
        unsafe_allow_html=True,
    )

    experiment_tab, replication_tab = st.tabs(
        ["Experimento principal", "Replicación"],
    )

    with experiment_tab:
        render_main_tab()

    with replication_tab:
        render_replication_tab()


if __name__ == "__main__":
    main()
