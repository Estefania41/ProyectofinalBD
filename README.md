# ProyectofinalBD
Proyecto final de bases de datos III
Football Analytics Dashboard ⚽📊
https://via.placeholder.com/800x400?text=Football+Analytics+Dashboard+Preview

Descripción 📝
Este dashboard interactivo permite visualizar y analizar estadísticas de partidos de fútbol, incluyendo:

📈 Comparación de rendimiento entre equipos

📊 Distribución de resultados (victorias locales/visitantes/empates)

🕸️ Grafos de relaciones entre equipos

📉 Tendencias temporales de rendimiento

Características principales ✨
Visualización interactiva con filtros por fecha, competición y equipos

KPIs clave: porcentaje de victorias, posesión promedio, goles por partido

Grafos dirigidos que muestran relaciones entre equipos

Datos en tiempo real conectados a Football Data API

Arquitectura escalable con Docker y MySQL
## Arquitectura del Proyecto

```mermaid
graph TD
    A[Dash Frontend] --> B[Python Backend]
    B --> C[MySQL Database]
    B --> D[Football Data API]
    C --> E[(Docker Container)]
    D --> E
```
