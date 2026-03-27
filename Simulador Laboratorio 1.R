library(shiny)
library(shinydashboard)
library(DT)
library(plotly)
library(ggplot2)
library(dplyr)
library(scales)
library(stringr)

conditionalPanel(
  condition = "!output.has_sample",
  fluidRow(
    box(
      title = "🚀 Comienza el Experimento", status = "info", solidHeader = TRUE, width = 12,
      div(
        style = "text-align: center; padding: 50px;",
        h4("¡Comienza el experimento!", style = "color: #999;"),
        p("Haz click en 'Conseguir Muestra' para probar TralaleroTralaLex")
      )
    )
  )
)

dependent_variables <- list(
  "Probabilidad de resolver Sudoku",
  "Prob. Resolver Crucigrama de letras",
  "Capacidad de recordar nombres raros",
  "Habilidad para encontrar llaves perdidas",
  "Velocidad para resolver laberintos",
  "Precisión en recordar cumpleaños",
  "Eficiencia organizando calcetines",
  "Rapidez contando ovejas para dormir",
  "Destreza armando muebles de IKEA",
  "Intuición para adivinar contraseñas"
)

age_groups <- list(
  "Todos" = "todos",
  "Jóvenes (20-40)" = "jovenes",
  "Adultos (40-60)" = "adultos",
  "Veteranos (+60)" = "veteranos"
)

ui <- dashboardPage(
  dashboardHeader(title = "🧠 TralaleroTralaLex: ¿Milagro Cognitivo o Azar? 🧠"),
  
  dashboardSidebar(
    sidebarMenu(
      menuItem("🔬 Experimento Principal", tabName = "main", icon = icon("flask")),
      menuItem("📊 Replicación", tabName = "replication", icon = icon("repeat"))
    )
  ),
  
  dashboardBody(
    tags$head(
      tags$style(HTML("
        .content-wrapper, .right-side {
          background-color: #f4f4f4;
        }
        .box {
          border-radius: 8px;
        }
        .btn-custom {
          margin: 5px;
          border-radius: 5px;
        }
        .significant {
          background-color: #ffebee !important;
          color: #c62828;
          font-weight: bold;
        }
        .not-significant {
          background-color: #e8f5e8 !important;
          color: #2e7d32;
        }
        .big-number {
          font-size: 48px;
          font-weight: bold;
          text-align: center;
        }
        .metric-box {
          background: linear-gradient(45deg, #ff6b6b, #4ecdc4);
          color: white;
          border-radius: 10px;
          padding: 20px;
          margin: 10px 0;
        }
        .warning-box {
          background: #ff9800;
          color: white;
          border-radius: 8px;
          padding: 15px;
          margin: 10px 0;
        }
      "))
    ),
    
    tabItems(
      tabItem(tabName = "main",
              fluidRow(
                box(
                  title = "🧪 Contexto del Experimento", status = "info", solidHeader = TRUE,
                  width = 12, collapsible = TRUE,
                  
                  div(
                    style = "background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 10px;",
                    h3("💊 TralaleroTralaLex: La Píldora Cognitiva del Futuro", style = "text-align: center;"),
                    p("¡Bienvenido al laboratorio! Estás investigando la efectividad de ",
                      strong("TralaleroTralaLex"), ", una nueva droga que promete mejorar dramáticamente las capacidades cognitivas."),
                    p("🎯 ", strong("Tu misión:"), " Determinar si esta droga realmente funciona o si los efectos 'significativos' son solo producto del azar."),
                    p("⚗️ ", strong("El experimento:"), " Participantes reciben la droga (tratamiento) o placebo (control), y medimos su desempeño en varias tareas cognitivas.")
                  )
                )
              ),
              
              fluidRow(
                box(
                  title = "🎛️ Configuración del Experimento", status = "primary", solidHeader = TRUE,
                  width = 12, collapsible = TRUE,
                  
                  fluidRow(
                    column(3,
                           h5("💊 Efecto Verdadero de TralaleroTralaLex"),
                           sliderInput("true_effect", "",
                                       min = 0, max = 1, value = 0, step = 0.1),
                           textOutput("true_effect_text")
                    ),
                    column(3,
                           h5("👥 Tamaño de Muestra Inicial"),
                           sliderInput("sample_size", "",
                                       min = 20, max = 500, value = 100, step = 10),
                           textOutput("sample_size_text")
                    ),
                    column(3,
                           h5("🎯 Análisis por Grupos Etarios"),
                           checkboxInput("analyze_by_age", "Dividir por grupos de edad", value = FALSE),
                           conditionalPanel(
                             condition = "input.analyze_by_age",
                             div(style = "font-size: 12px; color: #666; margin-top: 5px;",
                                 "Se analizarán: Jóvenes (20-40), Adultos (40-60), Veteranos (+60)")
                           )
                    ),
                    column(3,
                           h5("🧪 Múltiples Variables Dependientes"),
                           checkboxInput("multiple_variables", "Probar múltiples variables", value = FALSE),
                           conditionalPanel(
                             condition = "input.multiple_variables",
                             sliderInput("n_dependent_vars", "Número de variables:",
                                         min = 2, max = 5, value = 3, step = 1),
                             div(style = "font-size: 12px; color: #666;",
                                 textOutput("current_variables"))
                           )
                    )
                  )
                )
              ),
              
              fluidRow(
                box(
                  title = "🚀 Acciones del Experimento", status = "success", solidHeader = TRUE,
                  width = 12,
                  
                  fluidRow(
                    column(6,
                           actionButton("get_sample", "🔬 Conseguir Muestra",
                                        class = "btn btn-primary btn-custom btn-block")
                    ),
                    column(6,
                           actionButton("reset_all", "🧹 Limpiar Memoria",
                                        class = "btn btn-danger btn-custom btn-block")
                    )
                  )
                )
              ),
              
              conditionalPanel(
                condition = "output.has_results",
                fluidRow(
                  column(4,
                         div(
                           class = "metric-box",
                           div(class = "big-number", textOutput("total_tests")),
                           div(style = "text-align: center; font-size: 16px;", "Pruebas Realizadas")
                         )
                  ),
                  column(4,
                         div(
                           class = "metric-box",
                           div(class = "big-number", textOutput("p_values_under_05")),
                           div(style = "text-align: center; font-size: 16px;", "P-valores < 0.05")
                         )
                  ),
                  column(4,
                         div(
                           class = "metric-box",
                           div(class = "big-number", textOutput("proportion_under_05")),
                           div(style = "text-align: center; font-size: 16px;", "Proporción < 0.05")
                         )
                  )
                )
              ),
              
              fluidRow(
                box(
                  title = "📊 Distribución Teórica del T-Statistic",
                  status = "primary", solidHeader = TRUE, width = 12,
                  
                  div(
                    style = "margin-bottom: 10px;",
                    h5("📐 Fórmula: t-statistic = β / error estándar de β"),
                    h5(textOutput("current_context"))
                  ),
                  uiOutput("t_stat_legend"),
                  plotlyOutput("theoretical_plot", height = "400px")
                )
              ),
              
              conditionalPanel(
                condition = "output.has_results",
                fluidRow(
                  box(
                    title = "📜 Resultados de la Simulación Actual",
                    status = "warning", solidHeader = TRUE, width = 12,
                    
                    div(
                      style = "margin-bottom: 15px;",
                      h5("🎯 ", textOutput("analysis_summary", inline = TRUE))
                    ),
                    
                    DT::dataTableOutput("current_results_table")
                  )
                )
              )
      ),
      
      tabItem(tabName = "replication",
              fluidRow(
                box(
                  title = "🔄 Estudio de Replicación de TralaleroTralaLex", status = "primary",
                  solidHeader = TRUE, width = 12,
                  
                  fluidRow(
                    column(4,
                           h5("⚙️ Configuración del Estudio:"),
                           numericInput("n_replications", "🔄 Número de Estudios:",
                                        value = 500, min = 50, max = 2000, step = 50),
                           numericInput("replication_sample_size", "👥 Participantes por Estudio:",
                                        value = 100, min = 20, max = 500, step = 10),
                           numericInput("replication_true_effect", "💊 Efecto Real de la Droga:",
                                        value = 0, min = 0, max = 1, step = 0.1),
                           
                           h5("🔍 Opciones Avanzadas (selecciona máximo una):"),
                           checkboxInput("replication_analyze_by_age", "Efectos heterogéneos por grupo etario", value = FALSE),
                           checkboxInput("replication_multiple_variables", "Múltiples variables dependientes", value = FALSE),
                           conditionalPanel(
                             condition = "input.replication_multiple_variables",
                             sliderInput("replication_n_dependent_vars", "Número de variables:",
                                         min = 2, max = 5, value = 3, step = 1)
                           ),
                           
                           actionButton("run_replication", "🚀 Ejecutar Meta-Estudio",
                                        class = "btn btn-primary btn-block")
                    ),
                    
                    column(8,
                           conditionalPanel(
                             condition = "output.has_replication_results",
                             plotlyOutput("rejection_rate_evolution", height = "600px")
                           )
                    )
                  )
                )
              )
      )
    )
  )
)

server <- function(input, output, session) {
  
  values <- reactiveValues(
    current_sample = NULL,
    current_results = data.frame(),
    replication_results = NULL
  )
  
  generate_sample <- function(n = 100, true_effect = 0, add_to_existing = FALSE, existing_data = NULL) {
    if (add_to_existing && !is.null(existing_data)) {
      new_n <- round(n * 0.5)
    } else {
      new_n <- n
    }
    
    treatment <- rep(c(0, 1), length.out = new_n)
    ages <- round(runif(new_n, 20, 80))
    age_group <- ifelse(ages <= 40, "jovenes",
                        ifelse(ages <= 60, "adultos", "veteranos"))
    
    outcome_base <- rnorm(new_n, mean = 0, sd = 1) + treatment * true_effect
    
    new_data <- data.frame(
      treatment = treatment,
      age = ages,
      age_group = age_group,
      id = 1:new_n
    )
    
    for (i in 1:length(dependent_variables)) {
      var_name <- paste0("var_", i)
      new_data[[var_name]] <- outcome_base + rnorm(new_n, 0, 0.3)
    }
    
    if (add_to_existing && !is.null(existing_data)) {
      new_data$id <- new_data$id + max(existing_data$id)
      return(rbind(existing_data, new_data))
    } else {
      return(new_data)
    }
  }
  
  filter_by_age_group <- function(data, group) {
    if (is.null(group) || group == "todos") return(data)
    return(data[data$age_group == group, ])
  }
  
  calculate_statistics <- function(data, var_index = 1, group_name = "Todos") {
    var_name <- paste0("var_", var_index)
    treatment_data <- data[data$treatment == 1, ]
    control_data <- data[data$treatment == 0, ]
    
    if (nrow(treatment_data) < 2 || nrow(control_data) < 2) return(NULL)
    
    mean_treatment <- mean(treatment_data[[var_name]], na.rm = TRUE)
    mean_control <- mean(control_data[[var_name]], na.rm = TRUE)
    beta <- mean_treatment - mean_control
    var_treatment <- var(treatment_data[[var_name]], na.rm = TRUE)
    var_control <- var(control_data[[var_name]], na.rm = TRUE)
    n_treatment <- nrow(treatment_data)
    n_control <- nrow(control_data)
    pooled_var <- ((n_treatment - 1) * var_treatment + (n_control - 1) * var_control) / (n_treatment + n_control - 2)
    se_beta <- sqrt(pooled_var * (1/n_treatment + 1/n_control))
    
    if (is.na(se_beta) || se_beta == 0) return(NULL)
    
    t_statistic <- beta / se_beta
    df <- n_treatment + n_control - 2
    p_value <- 2 * pt(abs(t_statistic), df, lower.tail = FALSE)
    alpha <- 0.05
    t_critical <- qt(1 - alpha/2, df)
    ci_lower <- beta - t_critical * se_beta
    ci_upper <- beta + t_critical * se_beta
    
    return(list(
      variable = dependent_variables[[var_index]],
      variable_index = var_index,
      group = group_name,
      beta = beta, se_beta = se_beta, t_statistic = t_statistic,
      p_value = p_value, ci_lower = ci_lower, ci_upper = ci_upper,
      n_total = nrow(data), n_treatment = n_treatment, n_control = n_control,
      significant = p_value < 0.05
    ))
  }
  
  run_analysis <- function(sample_data, replace_current = TRUE) {
    if (replace_current) {
      values$current_results <- data.frame()
    }
    
    groups_to_analyze <- if (input$analyze_by_age) {
      list("Jóvenes (20-40)" = "jovenes", "Adultos (40-60)" = "adultos", "Veteranos (+60)" = "veteranos")
    } else {
      list("Todos" = "todos")
    }
    vars_to_analyze <- if (input$multiple_variables) 1:input$n_dependent_vars else 1
    
    for (var_idx in vars_to_analyze) {
      for (group_name in names(groups_to_analyze)) {
        group_value <- groups_to_analyze[[group_name]]
        group_data <- filter_by_age_group(sample_data, group_value)
        if (nrow(group_data) < 4) next
        stats <- calculate_statistics(group_data, var_idx, group_name)
        if (is.null(stats)) next
        new_row <- data.frame(
          Variable_Dependiente = stats$variable,
          Grupo_Etario = stats$group,
          Beta = round(stats$beta, 4), 
          Error_Std = round(stats$se_beta, 4),
          T_Statistic = round(stats$t_statistic, 3), 
          P_Value = round(stats$p_value, 4),
          IC_Inferior = round(stats$ci_lower, 4),
          IC_Superior = round(stats$ci_upper, 4),
          N_Total = stats$n_total, 
          stringsAsFactors = FALSE
        )
        values$current_results <- rbind(values$current_results, new_row)
      }
    }
  }
  
  observeEvent(input$get_sample, {
    new_data <- generate_sample(n = input$sample_size, true_effect = input$true_effect)
    values$current_sample <- new_data
    run_analysis(new_data, replace_current = TRUE)
  })
  
  observeEvent(input$replication_analyze_by_age, {
    if (input$replication_analyze_by_age) {
      updateCheckboxInput(session, "replication_multiple_variables", value = FALSE)
    }
  })
  
  observeEvent(input$replication_multiple_variables, {
    if (input$replication_multiple_variables) {
      updateCheckboxInput(session, "replication_analyze_by_age", value = FALSE)
    }
  })
  
  observeEvent(input$reset_all, {
    values$current_sample <- NULL
    values$current_results <- data.frame()
    values$replication_results <- NULL
  })
  
  observeEvent(input$run_replication, {
    withProgress(message = 'Replicando estudios de TralaleroTralaLex...', value = 0, {
      n_reps <- input$n_replications
      replication_data <- data.frame()
      
      vars_to_test <- if (input$replication_multiple_variables) 1:input$replication_n_dependent_vars else 1
      
      for (i in 1:n_reps) {
        incProgress(1/n_reps, detail = paste("Estudio", i, "de", n_reps))
        sample_data <- generate_sample(n = input$replication_sample_size, true_effect = input$replication_true_effect)
        
        stats_todos <- calculate_statistics(sample_data, 1, "Todos")
        rejected_todos <- ifelse(!is.null(stats_todos), stats_todos$p_value < 0.05, FALSE)
        
        rejected_any_var <- FALSE
        if (input$replication_multiple_variables && length(vars_to_test) > 1) {
          var_results <- sapply(vars_to_test, function(var_idx) {
            stats <- calculate_statistics(sample_data, var_idx, "Todos")
            ifelse(!is.null(stats), stats$p_value < 0.05, FALSE)
          })
          rejected_any_var <- any(var_results, na.rm = TRUE)
        }
        
        rejected_any_subgroup <- FALSE
        if (input$replication_analyze_by_age) {
          subgroup_results <- sapply(c("jovenes", "adultos", "veteranos"), function(group_code) {
            group_data <- filter_by_age_group(sample_data, group_code)
            if (nrow(group_data) < 4) return(FALSE)
            stats <- calculate_statistics(group_data, 1, group_code)
            ifelse(!is.null(stats), stats$p_value < 0.05, FALSE)
          })
          rejected_any_subgroup <- any(subgroup_results, na.rm = TRUE)
        }
        
        rep_result <- data.frame(
          replication = i,
          rejected_todos = rejected_todos,
          rejected_any_var = rejected_any_var,
          rejected_any_subgroup = rejected_any_subgroup
        )
        replication_data <- rbind(replication_data, rep_result)
      }
      values$replication_results <- replication_data
    })
  })
  
  output$true_effect_text <- renderText({
    if (input$true_effect == 0) "🚫 Sin efecto (placebo)" else paste("💊 Mejora de", input$true_effect, "puntos")
  })
  output$sample_size_text <- renderText({ paste("👥", input$sample_size, "participantes") })
  output$current_variables <- renderText({
    if (!input$multiple_variables) {
      "Una sola variable: Probabilidad de resolver Sudoku"
    } else {
      vars_to_show <- dependent_variables[1:input$n_dependent_vars]
      paste(unlist(vars_to_show), collapse = ", ")
    }
  })
  output$current_context <- renderText({
    analyses_text <- if (input$multiple_variables && input$analyze_by_age) {
      "Múltiples variables × múltiples grupos"
    } else if (input$multiple_variables) {
      "Múltiples variables"
    } else if (input$analyze_by_age) {
      "Múltiples grupos etarios"
    } else {
      "Análisis simple"
    }
    paste("🎯", analyses_text, "- Efecto real de TralaleroTralaLex:", input$true_effect)
  })
  
  output$total_tests <- renderText({ nrow(values$current_results) })
  output$p_values_under_05 <- renderText({ sum(values$current_results$P_Value < 0.05, na.rm = TRUE) })
  output$proportion_under_05 <- renderText({
    if (nrow(values$current_results) == 0) return("0%")
    prop <- sum(values$current_results$P_Value < 0.05, na.rm = TRUE) / nrow(values$current_results) * 100
    paste0(round(prop, 1), "%")
  })
  
  output$has_sample <- reactive({ !is.null(values$current_sample) })
  outputOptions(output, "has_sample", suspendWhenHidden = FALSE)
  output$has_results <- reactive({ nrow(values$current_results) > 0 })
  outputOptions(output, "has_results", suspendWhenHidden = FALSE)
  output$has_replication_results <- reactive({ !is.null(values$replication_results) })
  outputOptions(output, "has_replication_results", suspendWhenHidden = FALSE)
  
  output$t_stat_legend <- renderUI({
    req(nrow(values$current_results) > 0)
    
    variable_colors <- setNames(
      c("#66C2A5", "#FC8D62", "#8DA0CB", "#E78AC3", "#A6D854"),
      unlist(dependent_variables[1:5])
    )
    
    plot_data <- values$current_results %>%
      mutate(
        Combined_Label = paste(Variable_Dependiente, Grupo_Etario, sep = " - "),
        Plot_Color = {
          base_color <- variable_colors[Variable_Dependiente]
          if (input$analyze_by_age) {
            case_when(
              Grupo_Etario == "Jóvenes (20-40)" ~ alpha(base_color, 0.6),
              Grupo_Etario == "Adultos (40-60)" ~ alpha(base_color, 0.8),
              Grupo_Etario == "Veteranos (+60)" ~ alpha(base_color, 1.0),
              TRUE ~ base_color
            )
          } else {
            base_color
          }
        }
      )
    
    legend_items <- apply(plot_data, 1, function(row) {
      sprintf(
        '<span style="margin-right: 15px; font-size: 12px; white-space: nowrap;">
           <span style="display: inline-block; width: 12px; height: 12px; border-radius: 2px; background-color: %s; vertical-align: middle; margin-right: 5px;"></span>
           %s
         </span>',
        row["Plot_Color"],
        row["Combined_Label"]
      )
    })
    
    div(
      style = "padding: 10px; border: 1px solid #ddd; border-radius: 5px; margin-bottom: 10px; background-color: #f9f9f9; display: flex; flex-wrap: wrap;",
      h5("Leyenda de T-Statistics:", style="margin-top: 0; width: 100%;"),
      HTML(paste(legend_items, collapse = ""))
    )
  })
  
  output$theoretical_plot <- renderPlotly({
    x_seq <- seq(-4.5, 4.5, by = 0.1)
    y_theoretical <- dnorm(x_seq, mean = 0, sd = 1)
    theoretical_data <- data.frame(x = x_seq, y = y_theoretical)
    critical_value <- 1.96
    
    p <- ggplot(theoretical_data, aes(x = x, y = y)) +
      geom_line(color = "#2196F3", size = 1.5) +
      geom_vline(xintercept = c(-critical_value, critical_value), color = "#f44336", linetype = "dashed", size = 1) +
      geom_vline(xintercept = 0, color = "#666", linetype = "dotted", alpha = 0.7) +
      labs(title = "Distribución Teórica del T-Statistic", x = "T-Statistic", y = "Densidad de Probabilidad") +
      theme_minimal() + theme(plot.title = element_text(hjust = 0.5, size = 14))
    
    if (!is.null(values$current_sample) && nrow(values$current_results) > 0) {
      
      variable_colors <- setNames(
        c("#66C2A5", "#FC8D62", "#8DA0CB", "#E78AC3", "#A6D854"),
        unlist(dependent_variables[1:5])
      )
      
      plot_data <- values$current_results %>%
        mutate(
          Plot_Color = {
            base_color <- variable_colors[Variable_Dependiente]
            if (input$analyze_by_age) {
              case_when(
                Grupo_Etario == "Jóvenes (20-40)" ~ alpha(base_color, 0.6),
                Grupo_Etario == "Adultos (40-60)" ~ alpha(base_color, 0.8),
                Grupo_Etario == "Veteranos (+60)" ~ alpha(base_color, 1.0),
                TRUE ~ base_color
              )
            } else {
              base_color
            }
          }
        )
      
      p <- p + 
        geom_vline(data = plot_data, aes(xintercept = T_Statistic, color = Plot_Color), size = 1.5) +
        scale_color_identity(guide = "none")
    }
    
    p <- p +
      annotate("text", x = critical_value + 0.3, y = max(theoretical_data$y) * 0.9,
               label = paste("Crítico\nsi |t| >", critical_value),
               color = "#f44336", size = 3, fontface = "bold")
    
    ggplotly(p) %>% config(displayModeBar = FALSE)
  })
  
  output$current_analysis_info <- renderTable({
    req(values$current_sample)
    analysis_type <- if (input$multiple_variables && input$analyze_by_age) {
      paste(input$n_dependent_vars, "vars × 3 grupos")
    } else if (input$multiple_variables) {
      paste(input$n_dependent_vars, "variables")
    } else if (input$analyze_by_age) {
      "3 grupos etarios"
    } else {
      "Análisis simple"
    }
    data.frame(
      Aspecto = c("🎯 Tipo de Análisis", "👥 Participantes", "🧪 Pruebas", "💊 Efecto Real"),
      Detalle = c(analysis_type, nrow(values$current_sample), nrow(values$current_results),
                  ifelse(input$true_effect == 0, "Ninguno (placebo)", input$true_effect)),
      stringsAsFactors = FALSE
    )
  }, bordered = TRUE, striped = TRUE)
  
  output$main_results <- renderTable({
    req(values$current_sample, nrow(values$current_results) > 0)
    latest <- values$current_results[nrow(values$current_results), ]
    data.frame(
      Estadística = c("💊 Beta (Efecto)", "📏 Error Estándar", "📊 T-Statistic", "🎯 P-valor"),
      Valor = c(latest$Beta, latest$Error_Std, latest$T_Statistic, latest$P_Value),
      stringsAsFactors = FALSE
    )
  }, bordered = TRUE, striped = TRUE)
  
  output$confidence_intervals <- renderTable({
    req(values$current_sample, nrow(values$current_results) > 0)
    latest <- values$current_results[nrow(values$current_results), ]
    data.frame(
      Métrica = "🎯 IC 95%",
      Valor = paste0("[", latest$IC_Inferior, ", ", latest$IC_Superior, "]"),
      stringsAsFactors = FALSE
    )
  }, bordered = TRUE, striped = TRUE)
  
  output$detailed_results_plot <- renderPlotly({
    req(nrow(values$current_results) > 1)
    
    variable_colors <- setNames(
      c("#66C2A5", "#FC8D62", "#8DA0CB", "#E78AC3", "#A6D854"),
      unlist(dependent_variables[1:5])
    )
    
    plot_data <- values$current_results %>%
      mutate(
        Experiment_ID = 1:n(),
        P_Value_Numeric = as.numeric(P_Value),
        Combined_Label = paste(Variable_Dependiente, Grupo_Etario, sep = " - "),
        Plot_Color = {
          base_color <- variable_colors[Variable_Dependiente]
          if (input$analyze_by_age) {
            case_when(
              Grupo_Etario == "Jóvenes (20-40)" ~ alpha(base_color, 0.6),
              Grupo_Etario == "Adultos (40-60)" ~ alpha(base_color, 0.8),
              Grupo_Etario == "Veteranos (+60)" ~ alpha(base_color, 1.0),
              TRUE ~ base_color
            )
          } else {
            base_color
          }
        }
      )
    
    color_values <- setNames(plot_data$Plot_Color, plot_data$Combined_Label)
    
    p <- ggplot(plot_data, aes(x = Experiment_ID, y = P_Value_Numeric)) +
      geom_point(aes(color = Combined_Label,
                     size = abs(T_Statistic),
                     text = paste("Análisis:", Combined_Label, "<br>P-valor:", round(P_Value_Numeric, 4))),
                 alpha = 0.9) +
      geom_hline(yintercept = 0.05, color = "#f44336", linetype = "dashed", size = 1.2) +
      scale_color_manual(name = "Variable y Grupo", values = color_values) +
      scale_y_continuous(trans = "log10",
                         breaks = c(0.001, 0.01, 0.05, 0.1, 0.5, 1),
                         labels = c("0.001", "0.01", "0.05", "0.1", "0.5", "1.0")) +
      labs(title = "🔍 Todos los Análisis de TralaleroTralaLex",
           subtitle = "Cada punto = una prueba estadística (Variable × Grupo Etario)",
           x = "📊 Número de Análisis", y = "📈 P-valor (escala log)", size = "|T-Statistic|") +
      theme_minimal() +
      theme(plot.title = element_text(hjust = 0.5, size = 16),
            plot.subtitle = element_text(hjust = 0.5, size = 12),
            legend.position = "bottom", legend.box = "vertical")
    
    p <- p + annotate("text", x = max(plot_data$Experiment_ID, na.rm = TRUE) * 0.7, y = 0.08,
                      label = "Línea p = 0.05",
                      color = "#f44336", fontface = "bold")
    
    ggplotly(p, tooltip = "text") %>% config(displayModeBar = FALSE)
  })
  
  output$analysis_summary <- renderText({
    if (nrow(values$current_results) == 0) return("")
    n_vars <- length(unique(values$current_results$Variable_Dependiente))
    n_groups <- length(unique(values$current_results$Grupo_Etario))
    n_under_05 <- sum(values$current_results$P_Value < 0.05, na.rm = TRUE)
    paste("Simulación actual:", n_vars, "variables ×", n_groups, "grupos =",
          nrow(values$current_results), "análisis totales.", n_under_05, "con p < 0.05.")
  })
  
  output$current_results_table <- DT::renderDataTable({
    req(nrow(values$current_results) > 0)
    display_data <- values$current_results
    DT::datatable(
      display_data,
      options = list(pageLength = -1,
                     scrollX = TRUE, 
                     scrollY = "400px",
                     order = list(list(0, 'desc')),
                     columnDefs = list(
                       list(targets = which(colnames(display_data) == "P_Value") - 1,
                            render = JS("function(data, type, row, meta) { 
                                        if (type === 'display' && data < 0.05) { 
                                          return '<span style=\"background-color: #ffeb3b; font-weight: bold;\">' + data + '</span>'; 
                                        } 
                                        return data; 
                                      }"))
                     )
      ),
      rownames = FALSE
    ) %>%
      DT::formatRound(columns = c("Beta", "Error_Std", "T_Statistic", "P_Value", "IC_Inferior", "IC_Superior"), digits = 4)
  })
  
  output$rejection_rate_evolution <- renderPlotly({
    req(values$replication_results)
    
    data <- values$replication_results %>%
      mutate(
        cumulative_todos = cumsum(rejected_todos) / row_number(),
        cumulative_any_var = if(input$replication_multiple_variables) cumsum(rejected_any_var) / row_number() else NA,
        cumulative_any_subgroup = if(input$replication_analyze_by_age) cumsum(rejected_any_subgroup) / row_number() else NA
      )
    
    caption_text <- "La línea roja horizontal indica el valor de 5% del eje y. "
    
    if (input$replication_multiple_variables && input$replication_analyze_by_age) {
      caption_text <- paste0(caption_text, 
                             "Línea azul: análisis con todos los datos. ",
                             "Línea verde discontinua: proporción de estudios donde al menos una variable es significativa. ",
                             "Línea naranja discontinua: proporción de estudios donde al menos un subgrupo etario es significativo.")
    } else if (input$replication_multiple_variables) {
      caption_text <- paste0(caption_text,
                             "Línea azul: análisis con todos los datos usando una variable. ",
                             "Línea verde discontinua: proporción de estudios donde al menos una de las ", 
                             input$replication_n_dependent_vars, " variables es significativa.")
    } else if (input$replication_analyze_by_age) {
      caption_text <- paste0(caption_text,
                             "Línea azul: análisis con todos los datos. ",
                             "Línea naranja discontinua: proporción de estudios donde al menos uno de los 3 subgrupos etarios es significativo.")
    } else {
      caption_text <- paste0(caption_text, "Línea azul: análisis estándar con todos los datos.")
    }
    
    p <- ggplot(data, aes(x = replication)) +
      geom_line(aes(y = cumulative_todos, color = "Todos los datos"), size = 1.2) +
      labs(title = "Evolución de la Tasa de p-valor < 0.05",
           x = "Número de Estudios Acumulados", 
           y = "Proporción de p-valores < 0.05",
           color = "Análisis",
           caption = str_wrap(caption_text, width = 100)) +
      theme_minimal() +
      theme(plot.title = element_text(hjust = 0.5, size = 14),
            plot.caption = element_text(hjust = 0.5, color = "#666", size = 10))
    
    if (input$replication_multiple_variables) {
      p <- p + geom_line(aes(y = cumulative_any_var, color = "Al menos una variable"), size = 1.2, linetype = "dashed")
    }
    
    if (input$replication_analyze_by_age) {
      p <- p + geom_line(aes(y = cumulative_any_subgroup, color = "Al menos un subgrupo"), size = 1.2, linetype = "dashed")
    }
    
    expected_rate <- if(input$replication_true_effect == 0) 0.05 else NA
    
    y_max <- max(c(data$cumulative_todos, 
                   if(input$replication_multiple_variables) data$cumulative_any_var else NULL,
                   if(input$replication_analyze_by_age) data$cumulative_any_subgroup else NULL,
                   0.05), na.rm = TRUE)
    y_min <- min(c(data$cumulative_todos, 
                   if(input$replication_multiple_variables) data$cumulative_any_var else NULL,
                   if(input$replication_analyze_by_age) data$cumulative_any_subgroup else NULL,
                   0.05), na.rm = TRUE)
    
    y_breaks <- sort(unique(c(seq(0, ceiling(y_max * 10) / 10, by = 0.05), 0.05)))
    y_breaks <- y_breaks[y_breaks >= y_min & y_breaks <= y_max * 1.1]
    
    p <- p + 
      scale_y_continuous(breaks = y_breaks, labels = scales::percent_format(accuracy = 1)) +
      coord_cartesian(ylim = c(max(0, y_min - 0.01), y_max * 1.05))
    
    if (!is.na(expected_rate)) {
      p <- p + geom_hline(yintercept = expected_rate, color = "#f44336", linetype = "dotted", size = 1)
    }
    
    p <- p + scale_color_manual(values = c(
      "Todos los datos" = "#2196F3",
      "Al menos una variable" = "#4CAF50",
      "Al menos un subgrupo" = "#FF9800"
    ))
    
    ggplotly(p) %>% config(displayModeBar = FALSE)
  })
  
  output$n_studies <- renderText({ ifelse(is.null(values$replication_results), "0", nrow(values$replication_results)) })
}

shinyApp(ui = ui, server = server)