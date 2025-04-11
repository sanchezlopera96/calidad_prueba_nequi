# calidad_prueba_nequi
Simulador de pruebas de carga para aplicaciones financieras, inspirado en el caso de estudio de Nequi y herramientas como JMeter. Este simulador permite modelar distintos escenarios de carga sobre múltiples APIs financieras, visualizando tiempos de respuesta, tasas de error y métricas del sistema.

🚀 Características
Simulación de carga con diferentes escenarios: Normal, Alta y Extrema.

Cálculo de tiempos de respuesta y tasas de error por API.

Visualización tabular de resultados.

Recomendaciones basadas en métricas obtenidas.

Uso de colores en consola para una experiencia más visual (con colorama).

Exportación y visualización de resultados posibles con json, matplotlib, numpy y más.

📦 Requisitos
Este script utiliza las siguientes bibliotecas:

bash

pip install colorama tabulate matplotlib numpy

🧠 Estructura del simulador
Clases y métodos principales
Componente y	Descripción

FinancialLoadTestSimulator()	Clase principal que contiene APIs, escenarios y lógica de simulación.
print_header()	Muestra el encabezado con estilo.
print_apis()	Muestra la tabla de APIs disponibles para pruebas.
print_scenarios()	Presenta los escenarios predefinidos.
run_simulation()	Ejecuta una simulación con un escenario o configuración personalizada.
_calculate_results()	Calcula métricas como tiempo de respuesta, tasa de error, CPU y memoria.
_display_results()	Muestra los resultados de la simulación en consola.
