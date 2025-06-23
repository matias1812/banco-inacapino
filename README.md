# 🏦 Sistema Bancario INACAPINO

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Rich](https://img.shields.io/badge/Rich-13.0+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Status](https://img.shields.io/badge/Status-Completed-success.svg)

*Sistema bancario completo desarrollado en Python con interfaz de consola rica y colorida*

</div>

---

## 📋 Descripción del Proyecto

El **Sistema Bancario INACAPINO** es una aplicación de consola desarrollada en Python que simula las operaciones básicas de un banco. Incluye gestión de clientes, productos financieros, transferencias, créditos y un sistema completo de avances con tarjeta de crédito.

### ✨ Características Principales

- 🔐 **Validación segura** de RUN chileno con dígito verificador
- 💰 **Gestión completa** de cuentas y saldos
- 🏦 **Dos tipos de crédito**: Línea de crédito y tarjeta de crédito
- 📊 **Interfaz rica** con colores y tablas usando Rich
- 🔄 **Operaciones bancarias** completas (transferencias, depósitos, retiros)
- 📈 **Sistema de avances** con cuotas e intereses
- 📱 **Gestión de contactos** para transferencias seguras

---

## 🏗️ Arquitectura del Sistema

\`\`\`
📦 banco-inacapino/
├── 📄 main.py              # Punto de entrada y menú principal
├── 📄 data.py              # Almacenamiento de datos (listas globales)
├── 📄 utils.py             # Utilidades y validaciones
├── 👥 clientes.py          # Gestión de clientes
├── 📞 contactos.py         # Gestión de contactos
├── 💸 transferencias.py    # Sistema de transferencias
├── 💰 movimientos.py       # Depósitos, retiros y pagos
├── 💳 creditos.py          # Línea de crédito
├── 🎫 avances.py           # Avances con tarjeta
├── 💵 pagos_avances.py     # Pago de cuotas
├── 📊 consultas.py         # Consultas y reportes
└── 📖 README.md            # Este archivo
\`\`\`

### 🔄 Flujo de Datos

```mermaid
graph TD
    A[main.py] --> B[Menú Principal]
    B --> C[Gestión Clientes]
    B --> D[Operaciones Bancarias]
    B --> E[Productos de Crédito]
    B --> F[Consultas]
    
    C --> G[clientes.py]
    C --> H[contactos.py]
    
    D --> I[transferencias.py]
    D --> J[movimientos.py]
    
    E --> K[creditos.py]
    E --> L[avances.py]
    E --> M[pagos_avances.py]
    
    F --> N[consultas.py]
    
    G --> O[data.py]
    H --> O
    I --> O
    J --> O
    K --> O
    L --> O
    M --> O
    N --> O
