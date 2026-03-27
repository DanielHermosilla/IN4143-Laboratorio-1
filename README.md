# Simulador Laboratorio 1

Este repositorio ahora incluye dos versiones del simulador:

- `app.R`: versión original en Shiny.
- `app.py`: versión en Streamlit lista para correr y desplegar.

## Ejecutar localmente

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Despliegue

La app de Streamlit se puede hostear directamente en plataformas como Streamlit Community Cloud, Render o Railway.

- Archivo de entrada: `app.py`
- Dependencias: `requirements.txt`
- Comando de arranque genérico:

```bash
streamlit run app.py --server.address 0.0.0.0 --server.port $PORT
```

## Qué mantiene la versión Streamlit

- Simulación del experimento con tratamiento y control.
- Prueba t de dos muestras con beta, error estándar, t, p-valor e intervalo de confianza.
- Análisis por grupos etarios.
- Análisis con múltiples variables dependientes.
- Meta-estudio de replicación con evolución acumulada de rechazos.
