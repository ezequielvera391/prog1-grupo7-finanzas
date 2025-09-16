# prog1-grupo7-finanzas
# Algoritmos y Estructura de Datos I

## Integrantes
- Darkelys Pineda  
- Ezequiel Vera  
- Valentino Dorrego  
- Valentina Milagros Castillo  

## Introducción
El propósito de este documento es definir el alcance del proyecto orientado al desarrollo de una aplicación de consola en Python para la gestión de gastos personales.  
La idea principal es desarrollar un programa en donde los usuarios puedan registrar, organizar y analizar sus ingresos y egresos, con el fin de mejorar la administración de sus finanzas.

## Alcance del Producto

### Beneficios
- Favorece el ahorro y la planificación económica personal.  
- Facilita la visualización de los principales rubros.  
- Brinda una herramienta práctica para cumplir metas económicas (ejemplo: ahorrar para un viaje, comprar un bien, entre otros).  
- Reduce la dependencia de cálculos manuales o anotaciones dispersas en papel.  

### Objetivos y Metas
- Registrar y organizar ingresos y egresos de forma sencilla y rápida.  
- Clasificar los gastos por categorías (alimentación, transporte, vivienda, ocio, etc.) para una mejor visualización.  
- Generar reportes automáticos que permitan analizar la situación financiera en distintos períodos (semanal, mensual, anual).  
- Calcular estadísticas clave como: balance entre ingresos y gastos, promedio de gasto mensual, porcentaje de ahorro y distribución de gastos por categoría.  
- El proyecto busca fomentar la organización financiera personal, aplicando conceptos de programación estructurada en un entorno práctico y útil para la vida cotidiana.  

## Requisitos Funcionales
- Acceso al sistema a través de consola.  
- Login de usuarios, con nombre y contraseña para acceder a sus registros de gastos personales.  
- Módulo para el ingreso, modificación y borrado de ingresos de dinero.  
- Módulo para el ingreso, modificación y borrado de gastos.  
- Módulo para el ingreso, modificación y borrado de objetivos de ahorro.  
- Mostrar de manera gráfica por consola (en gráfico de barras o similar) la distribución de porcentajes de gastos por categoría con selector de periodo de tiempo (día, semana, mes, año, histórico).  
- Mostrar de manera gráfica por consola el avance en el objetivo de ahorro y si se está o no dentro del objetivo.  

## Requisitos No Funcionales
No definidos aún. Probablemente se usará alguna librería para mejorar la experiencia de usuario, como **rich** y **lib**.  

---

### Primer MVP 40%
El **primer MVP** representa aproximadamente el **40% del alcance total**. Incluye la estructura básica del sistema y las funciones mínimas necesarias para comenzar a interactuar con la aplicación:  

- Definición de la estructura de datos para usuarios, ingresos y egresos.  
- Creación de un **usuario hardcodeado** para login inicial.  
- Implementación de la función de **login** (validación de usuario y contraseña).  
- Definición de listas para ingresos y egresos con sus propiedades (id, monto, categoría, fecha, usuario).  
- Implementación de funciones **ABM (Alta, Baja, Modificación)** para ingresos y egresos.  
- Definición de la función `main()` con interacción básica por consola.  

Este MVP permite validar la estructura inicial del programa y sirve como base para construir el resto de los módulos más avanzados (objetivos de ahorro, reportes gráficos y estadísticas).  

---

### Segundo MVP (80%)  
Ampliación de funcionalidades y robustez:  
- **Validaciones más sólidas** para inputs.  
- **Módulo ABM de objetivos de ahorro.**  
- **Persistencia de datos en archivos CSV o JSON** para reemplazar las listas en memoria.  
- **Métricas sobre los datos ingresados**, como:  
  - Gasto total por mes.  
  - Porcentaje de aumento o disminución de ahorro entre períodos.  
  - Promedio de gasto por categoría.  
- Ampliación del módulo de **autenticación**, incorporando registro básico de usuarios.  

--- 

### Versión Final (100%)  
Mejoras e integración completa:  
- Uso de librerías para mejorar visualizaciones en consola.  
- Reportes gráficos más claros y legibles.  
- Mejora en la experiencia de usuario (menús más intuitivos, mensajes más descriptivos).  
- Incluir más metricas
