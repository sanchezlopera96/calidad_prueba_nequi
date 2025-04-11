import time
import random
import json
import matplotlib.pyplot as plt
import numpy as np
from tabulate import tabulate
from colorama import Fore, Style, init
import sys
sys.stdout.reconfigure(encoding='utf-8')

# Inicializar colorama para colores en consola
init(autoreset=True)

class FinancialLoadTestSimulator:
    """
    Simulador de pruebas de carga para aplicaciones financieras
    Basado en el caso de estudio de Nequi y JMeter
    """
    
    def __init__(self):
        # Definir las APIs disponibles
        self.apis = {
            "auth": {"name": "Autenticación (Auth API)", "path": "/api/v2/oauth/token", "method": "POST"},
            "balance": {"name": "Consulta de saldo (Deposit API)", "path": "/api/v2/deposits/accounts/{accountId}", "method": "GET"},
            "p2p": {"name": "Transferencias P2P (P2P API)", "path": "/api/v2/p2p", "method": "POST"},
            "qr": {"name": "Pagos QR (QR API)", "path": "/api/v1/qr/push", "method": "POST"},
            "withdrawal": {"name": "Retiros (Withdrawal API)", "path": "/api/v2/withdrawals", "method": "POST"}
        }
        
        # Definir escenarios predefinidos
        self.scenarios = {
            "normal": {
                "name": "Carga normal (1,000 usuarios)",
                "users": 1000,
                "distribution": {"auth": 0, "balance": 40, "p2p": 30, "qr": 20, "withdrawal": 10}
            },
            "high": {
                "name": "Carga alta (10,000 usuarios)",
                "users": 10000,
                "distribution": {"auth": 0, "balance": 25, "p2p": 45, "qr": 20, "withdrawal": 10}
            },
            "extreme": {
                "name": "Carga extrema (20,000 usuarios)",
                "users": 20000,
                "distribution": {"auth": 20, "balance": 20, "p2p": 40, "qr": 15, "withdrawal": 5}
            }
        }
        
        # Inicializar resultados
        self.results = None
    
    def print_header(self):
        """Muestra el encabezado del simulador"""
        print(Fore.CYAN + "\n" + "="*80)
        print(Fore.CYAN + " "*20 + "SIMULADOR DE PRUEBAS DE CARGA PARA APLICACIONES FINANCIERAS")
        print(Fore.CYAN + " "*30 + "Caso de estudio: Nequi")
        print(Fore.CYAN + "="*80 + "\n")
    
    def print_apis(self):
        """Muestra las APIs disponibles para pruebas"""
        print(Fore.YELLOW + "\nAPIs disponibles para pruebas:")
        headers = ["Clave", "Nombre", "Ruta", "Método"]
        table_data = []
        
        for key, api in self.apis.items():
            table_data.append([key, api["name"], api["path"], api["method"]])
        
        print(tabulate(table_data, headers=headers, tablefmt="pretty"))
    
    def print_scenarios(self):
        """Muestra los escenarios predefinidos"""
        print(Fore.YELLOW + "\nEscenarios predefinidos:")
        headers = ["Clave", "Nombre", "Usuarios", "Distribución de APIs"]
        table_data = []
        
        for key, scenario in self.scenarios.items():
            distribution_str = ", ".join([f"{self.apis[api]['name'].split(' ')[0]}: {pct}%" 
                                         for api, pct in scenario["distribution"].items() if pct > 0])
            table_data.append([key, scenario["name"], scenario["users"], distribution_str])
        
        print(tabulate(table_data, headers=headers, tablefmt="pretty"))
    
    def run_simulation(self, scenario_key=None, custom_users=None, custom_distribution=None):
        """
        Ejecuta la simulación de carga
        
        Args:
            scenario_key (str): Clave del escenario predefinido (normal, high, extreme)
            custom_users (int): Número personalizado de usuarios
            custom_distribution (dict): Distribución personalizada de APIs
        """
        print(Fore.GREEN + "\nIniciando simulación de carga...")
        
        # Determinar parámetros de simulación
        if scenario_key and scenario_key in self.scenarios:
            scenario = self.scenarios[scenario_key]
            users = scenario["users"]
            distribution = scenario["distribution"]
            print(f"Utilizando escenario: {scenario['name']}")
        else:
            users = custom_users if custom_users else 5000
            distribution = custom_distribution if custom_distribution else {
                "auth": 10, "balance": 30, "p2p": 40, "qr": 15, "withdrawal": 5
            }
            print(f"Utilizando configuración personalizada: {users} usuarios")
        
        # Mostrar detalles de la prueba
        print(f"Número de usuarios concurrentes: {users}")
        print("Distribución de peticiones:")
        for api, percentage in distribution.items():
            if percentage > 0:
                print(f"  - {self.apis[api]['name']}: {percentage}%")
        
        # Simulación de progreso
        print("\nEjecutando prueba de carga ", end="")
        for _ in range(10):
            print(".", end="", flush=True)
            time.sleep(0.2)
        print(" ¡completado!")
        
        # Calcular resultados
        self.results = self._calculate_results(users, distribution)
        
        # Mostrar resultados
        self._display_results()
        
        return self.results
    
    def _calculate_results(self, users, distribution):
        """
        Calcula los resultados de la simulación basándose en modelos predictivos
        
        Args:
            users (int): Número de usuarios concurrentes
            distribution (dict): Distribución de peticiones por API
        
        Returns:
            dict: Resultados de la simulación
        """
        # Calcular tiempo de respuesta y tasa de error para cada API
        response_time = {}
        error_rate = {}
        errors = []
        
        for api in self.apis:
            # Obtener porcentaje de la API en la distribución
            percentage = distribution.get(api, 0)
            api_users = int(users * percentage / 100)
            
            # Calcular tiempo de respuesta basado en usuarios
            # Fórmula basada en datos reales del caso Nequi
            base_time = 1.2 if api == "p2p" else 0.8 if api == "auth" else 1.0
            
            if users <= 1000:
                calc_time = base_time
            elif users <= 10000:
                calc_time = base_time * (1 + (users - 1000) / 3000)
            else:
                calc_time = base_time * (1 + 3 + (users - 10000) / 2000)
            
            # Añadir variación aleatoria
            calc_time = calc_time * (1 + random.uniform(-0.1, 0.1))
            response_time[api] = round(calc_time, 2)
            
            # Calcular tasa de error
            if users <= 1000:
                error_pct = 0.5
            elif users <= 10000:
                error_pct = 0.5 + (users - 1000) * 0.00075
            else:
                error_pct = 8 + (users - 10000) * 0.0027
            
            # Añadir variación aleatoria
            error_pct = error_pct * (1 + random.uniform(-0.1, 0.2))
            error_rate[api] = round(error_pct, 2)
            
            # Añadir tipos de errores específicos cuando la tasa es alta
            if error_pct > 5 and api_users > 0:
                errors.append({"api": api, "code": 429, "message": "Too Many Requests"})
            if error_pct > 15 and api_users > 0:
                errors.append({"api": api, "code": 504, "message": "Gateway Timeout"})
            if error_pct > 25 and api_users > 0:
                errors.append({"api": api, "code": 503, "message": "Service Unavailable"})
                errors.append({"api": api, "code": 500, "message": "Internal Server Error"})
        
        # Calcular métricas del sistema
        system_metrics = {"cpu": 0, "memory": 0}
        
        if users <= 1000:
            system_metrics["cpu"] = 45
            system_metrics["memory"] = 60
        elif users <= 10000:
            system_metrics["cpu"] = 45 + (users - 1000) * 0.004
            system_metrics["memory"] = 60 + (users - 1000) * 0.003
        else:
            system_metrics["cpu"] = 85 + (users - 10000) * 0.0015
            system_metrics["memory"] = 90 + (users - 10000) * 0.0005
        
        # Añadir variación aleatoria
        system_metrics["cpu"] = min(100, system_metrics["cpu"] * (1 + random.uniform(-0.05, 0.05)))
        system_metrics["memory"] = min(100, system_metrics["memory"] * (1 + random.uniform(-0.05, 0.05)))
        
        # Calcular estadísticas globales
        valid_response_times = [rt for api, rt in response_time.items() if distribution.get(api, 0) > 0]
        valid_error_rates = [er for api, er in error_rate.items() if distribution.get(api, 0) > 0]
        
        avg_response_time = sum(valid_response_times) / len(valid_response_times) if valid_response_times else 0
        avg_error_rate = sum(valid_error_rates) / len(valid_error_rates) if valid_error_rates else 0
        
        # Preparar resultados
        results = {
            "response_time": response_time,
            "error_rate": error_rate,
            "system_metrics": {
                "cpu": round(system_metrics["cpu"], 1),
                "memory": round(system_metrics["memory"], 1)
            },
            "errors": errors,
            "total_users": users,
            "avg_response_time": round(avg_response_time, 2),
            "avg_error_rate": round(avg_error_rate, 2),
            "distribution": distribution
        }
        
        return results
    
    def _display_results(self):
        """Muestra los resultados de la simulación en formato tabular y recomendaciones"""
        if not self.results:
            print(Fore.RED + "\nNo hay resultados disponibles. Ejecute una simulación primero.")
            return
        
        print(Fore.GREEN + "\n" + "="*80)
        print(Fore.GREEN + " "*30 + "RESULTADOS DE LA SIMULACIÓN")
        print(Fore.GREEN + "="*80)
        
        # Mostrar métricas generales
        print(Fore.CYAN + "\nMétricas generales:")
        general_data = [
            ["Usuarios concurrentes", f"{self.results['total_users']:,}"],
            ["Tiempo medio de respuesta", f"{self.results['avg_response_time']:.2f} segundos"],
            ["Tasa de error global", f"{self.results['avg_error_rate']:.2f}%"],
            ["Uso de CPU", f"{self.results['system_metrics']['cpu']:.1f}%"],
            ["Uso de memoria", f"{self.results['system_metrics']['memory']:.1f}%"],
        ]
        print(tabulate(general_data, tablefmt="pretty"))
        
        # Mostrar tiempos de respuesta por API
        print(Fore.CYAN + "\nTiempos de respuesta por API:")
        rt_data = []
        for api, rt in self.results["response_time"].items():
            if self.results["distribution"].get(api, 0) > 0:
                rt_data.append([self.apis[api]["name"], f"{rt:.2f} segundos"])
        print(tabulate(rt_data, headers=["API", "Tiempo de respuesta"], tablefmt="pretty"))
        
        # Mostrar tasa de error por API
        print(Fore.CYAN + "\nTasa de error por API:")
        er_data = []
        for api, er in self.results["error_rate"].items():
            if self.results["distribution"].get(api, 0) > 0:
                er_data.append([self.apis[api]["name"], f"{er:.2f}%"])
        print(tabulate(er_data, headers=["API", "Tasa de error"], tablefmt="pretty"))
        
        # Mostrar errores detectados
        if self.results["errors"]:
            print(Fore.RED + "\nErrores detectados:")
            error_data = []
            for error in self.results["errors"]:
                api = error["api"]
                error_data.append([
                    self.apis[api]["name"],
                    error["code"],
                    error["message"]
                ])
            print(tabulate(error_data, headers=["API", "Código", "Mensaje"], tablefmt="pretty"))
        
        # Mostrar diagnóstico
        print(Fore.CYAN + "\nDiagnóstico:")
        if self.results["avg_error_rate"] < 5:
            print(Fore.GREEN + "✓ El sistema funciona de manera óptima bajo esta carga.")
        elif self.results["avg_error_rate"] < 15:
            print(Fore.YELLOW + "⚠ El sistema muestra signos de degradación. Se recomienda optimizar las APIs con mayor tasa de error.")
        else:
            print(Fore.RED + "✗ ¡Sistema sobrecargado! Se requiere implementar throttling inteligente, priorización de transacciones " +
                  "y escalado horizontal inmediato.")
        
        # Mostrar recomendaciones
        self._show_recommendations()
    
    def _show_recommendations(self):
        """Muestra recomendaciones basadas en los resultados de la simulación"""
        if not self.results:
            return
        
        print(Fore.CYAN + "\nRecomendaciones para mejorar el rendimiento:")
        
        recommendations = []
        
        # Recomendaciones basadas en tasa de error
        if self.results["avg_error_rate"] > 8:
            recommendations.append("Optimizar API de Transferencias: Las transferencias P2P muestran tiempos " +
                                 "de respuesta elevados. Implemente caché para operaciones recurrentes y optimice " +
                                 "consultas a base de datos.")
        
        # Recomendaciones basadas en CPU
        if self.results["system_metrics"]["cpu"] > 75:
            recommendations.append("Escalar Horizontalmente: El uso de CPU supera el 75%. Implemente auto-scaling " +
                                 "para añadir más nodos durante picos de demanda.")
        
        # Recomendaciones basadas en errores específicos
        has_429 = any(e["code"] == 429 for e in self.results["errors"])
        has_500_503 = any(e["code"] in [500, 503] for e in self.results["errors"])
        
        if has_429:
            recommendations.append("Revisar Políticas de Rate Limiting: Los errores 429 (Too Many Requests) indican " +
                                 "que las políticas de limitación de tasa actuales son demasiado restrictivas para " +
                                 "el volumen de usuarios.")
        
        if has_500_503:
            recommendations.append("Implementar Degradación Controlada: Los errores 503 y 500 sugieren fallos completos. " +
                                 "Implemente circuit breakers y estrategias de degradación controlada para mantener " +
                                 "funcionalidades críticas operativas.")
        
        # Recomendación para caso óptimo
        if self.results["avg_error_rate"] < 5:
            recommendations.append("Monitoreo Continuo: El sistema muestra buen rendimiento. Se recomienda implementar " +
                                 "un sistema de monitoreo continuo para detectar cambios en los patrones de uso y " +
                                 "anticipar futuros picos.")
        
        # Mostrar recomendaciones
        for i, rec in enumerate(recommendations, 1):
            print(f"{i}. {rec}")
    
    def plot_results(self):
        """Genera gráficos con los resultados de la simulación"""
        if not self.results:
            print(Fore.RED + "\nNo hay resultados disponibles para graficar. Ejecute una simulación primero.")
            return
        
        # Configurar el estilo de los gráficos
        plt.style.use('ggplot')
        
        # Crear figura con 2 subplots (tiempos de respuesta y tasas de error)
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
        fig.suptitle(f'Resultados de Simulación: {self.results["total_users"]:,} usuarios', fontsize=16)
        
        # Preparar datos
        apis = [api for api, pct in self.results["distribution"].items() if pct > 0]
        api_names = [self.apis[api]["name"].split(" ")[0] for api in apis]
        response_times = [self.results["response_time"][api] for api in apis]
        error_rates = [self.results["error_rate"][api] for api in apis]
        
        # Gráfico de tiempos de respuesta
        bars1 = ax1.bar(api_names, response_times, color='steelblue')
        ax1.set_title('Tiempos de Respuesta por API')
        ax1.set_ylabel('Tiempo (segundos)')
        ax1.set_ylim(0, max(response_times) * 1.2)
        
        # Añadir etiquetas de valor
        for bar in bars1:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                    f'{height:.2f}s', ha='center', va='bottom')
        
        # Gráfico de tasas de error
        bars2 = ax2.bar(api_names, error_rates, color='indianred')
        ax2.set_title('Tasa de Error por API')
        ax2.set_ylabel('Error (%)')
        ax2.set_ylim(0, max(error_rates) * 1.2)
        
        # Añadir etiquetas de valor
        for bar in bars2:
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                    f'{height:.2f}%', ha='center', va='bottom')
        
        # Añadir marcas de nivel crítico en tasas de error
        ax2.axhline(y=5, linestyle='--', color='orange', alpha=0.7, label='Nivel de advertencia (5%)')
        ax2.axhline(y=15, linestyle='--', color='red', alpha=0.7, label='Nivel crítico (15%)')
        ax2.legend()
        
        # Añadir información adicional en un cuadro de texto
        textstr = '\n'.join((
            f'Usuarios concurrentes: {self.results["total_users"]:,}',
            f'Tasa de error global: {self.results["avg_error_rate"]:.2f}%',
            f'Tiempo medio de respuesta: {self.results["avg_response_time"]:.2f}s',
            f'CPU: {self.results["system_metrics"]["cpu"]:.1f}%',
            f'Memoria: {self.results["system_metrics"]["memory"]:.1f}%'))
        
        props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
        fig.text(0.15, 0.02, textstr, fontsize=12, bbox=props)
        
        # Ajustar layout y mostrar gráfico
        plt.tight_layout(rect=[0, 0.05, 1, 0.95])
        plt.show()
    
    def save_results(self, filename='load_test_results.json'):
        """Guarda los resultados de la simulación en un archivo JSON"""
        if not self.results:
            print(Fore.RED + "\nNo hay resultados disponibles para guardar. Ejecute una simulación primero.")
            return
        
        with open(filename, 'w') as f:
            json.dump(self.results, f, indent=4)
        
        print(Fore.GREEN + f"\nResultados guardados en {filename}")
    
    def interactive_menu(self):
        """Menú interactivo para la simulación de pruebas de carga"""
        self.print_header()
        
        while True:
            print(Fore.CYAN + "\nOpciones disponibles:")
            print("1. Ver APIs disponibles")
            print("2. Ver escenarios predefinidos")
            print("3. Ejecutar escenario predefinido")
            print("4. Ejecutar configuración personalizada")
            print("5. Graficar resultados")
            print("6. Guardar resultados")
            print("0. Salir")
            
            choice = input("\nSeleccione una opción (0-6): ")
            
            if choice == '1':
                self.print_apis()
            elif choice == '2':
                self.print_scenarios()
            elif choice == '3':
                self.print_scenarios()
                scenario_key = input("\nIngrese la clave del escenario (normal, high, extreme): ").lower()
                if scenario_key in self.scenarios:
                    self.run_simulation(scenario_key=scenario_key)
                else:
                    print(Fore.RED + "Escenario no válido. Use 'normal', 'high' o 'extreme'.")
            elif choice == '4':
                try:
                    users = int(input("\nIngrese número de usuarios concurrentes: "))
                    print("\nIngrese distribución de peticiones (porcentaje para cada API, debe sumar 100):")
                    
                    custom_distribution = {}
                    total_percentage = 0
                    
                    for api in self.apis:
                        while True:
                            try:
                                percentage = int(input(f"{self.apis[api]['name']}: "))
                                if percentage < 0:
                                    print(Fore.RED + "El porcentaje no puede ser negativo.")
                                    continue
                                    
                                if total_percentage + percentage > 100:
                                    print(Fore.RED + f"El total supera 100%. Quedan {100 - total_percentage}% disponibles.")
                                    continue
                                
                                custom_distribution[api] = percentage
                                total_percentage += percentage
                                break
                            except ValueError:
                                print(Fore.RED + "Ingrese un número entero válido.")
                    
                    if total_percentage != 100:
                        print(Fore.RED + f"La suma debe ser 100%. Total actual: {total_percentage}%")
                    else:
                        self.run_simulation(custom_users=users, custom_distribution=custom_distribution)
                        
                except ValueError:
                    print(Fore.RED + "Entrada no válida. Ingrese números enteros.")
            elif choice == '5':
                self.plot_results()
            elif choice == '6':
                filename = input("\nIngrese nombre de archivo (o presione Enter para usar el predeterminado): ")
                if not filename:
                    filename = 'load_test_results.json'
                self.save_results(filename)
            elif choice == '0':
                print(Fore.GREEN + "\n¡Gracias por usar el simulador de pruebas de carga!")
                break
            else:
                print(Fore.RED + "Opción no válida. Intente de nuevo.")


# Ejemplo de uso
if __name__ == "__main__":
    simulator = FinancialLoadTestSimulator()
    simulator.interactive_menu()
