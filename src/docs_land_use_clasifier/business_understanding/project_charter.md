# Project Charter - Entendimiento del Negocio

## Clasificación de imagenes satelitales por uso de suelo


## Objetivo del Proyecto

[Descripción breve del objetivo del proyecto y por qué es importante]

Desarrollar un modelo de clasificación de imágenes que identifique correctamente distintas categorías de imágenes aéreas utilizando técnicas de deep learning con la arquitectura de una red neuronal convolucional EfficientNetB0 con fine tuning.

## Alcance del Proyecto

El modelo abordará un conjunto específico de 21 categorías de imágenes aéreas, como "beach", "forest", "parkinglot", entre otras.

Procesos Incluidos:

Preprocesamiento de las imágenes
Implementación de un modelo de clasificación usando EfficientNetB0 como base.
Entrenamiento del modelo utilizando datos ya preprocesados y organizados.
Evaluación del modelo con métricas estándar como precisión, recall, F1-score y matriz de confusión.
Despliegue del modelo a producción

Entregables del Proyecto:

Modelo entrenado y desplegado  con los mejores hiperparámetros encontrados.
Resultados de evaluación del modelo (métricas y visualización de predicciones).
Código reproducible documentado.


### Incluye:


Formato de los datos:

Tipo de datos: Imágenes aéreas.
Resolución: Todas las imágenes serán preprocesadas y redimensionadas a un tamaño uniforme (por ejemplo, 224x224 píxeles, compatible con EfficientNetB0).
Canales: RGB (imágenes en color).
Formato de archivo: .Tiff

Clases:

El dataset contiene 21 clases distintas, representando diferentes tipos de áreas terrestres observadas desde el aire. Ejemplos de estas clases incluyen:
agricultural, airplane, beach, buildings, forest, parkinglot, entre otras.
Cada clase tiene un número equilibrado (100) para evitar problemas severos de desbalanceo.

Etiquetado:
Cada imagen está etiquetada con una única categoría, lo que permite un problema de clasificación multiclase.


#### Resultados esperados

Se espera poder evaluar ls resultados de una red neuranl convolucional en relación con el pasado resultado de Efficentnet con transfer learning con las siguientes métricas de desempeño:

* Precisión: Medir qué tan preciso es el modelo al predecir las clases correctas.
* Recall: Evaluar cuántas de las instancias verdaderas de cada clase fueron correctamente identificadas.
* F1-Score: Balance entre precisión y recall.
* Matriz de Confusión: Proporcionará una visualización detallada de las predicciones vs. las etiquetas verdaderas, permitiendo entender mejor las clases que están siendo confundidas.

* Despliegue del modelo empleando Railway y fastAPI se incluye como API Web

## Metodología

Team Data Science para el Proyecto de Clasificación de Imágenes Aéreas
En este proyecto de clasificación de imágenes aéreas, aplicaremos la metodología Team Data Science (TDS) para estructurar y guiar cada fase del desarrollo del modelo, asegurando que el trabajo en equipo sea fluido y que todas las decisiones estén alineadas con los objetivos del proyecto. 

A continuación se detallan las fases específicas que seguiremos, adaptadas al contexto de nuestro proyecto.

#### Fase 1: Definición del Problema

Objetivo del Proyecto: Desarrollar un modelo de clasificación capaz de identificar diferentes tipos de áreas terrestres a partir de imágenes aéreas. Este modelo se aplicará a un conjunto de imágenes aéreas etiquetadas con categorías como: agricultural, airplane, baseballdiamond, beach, forest, entre otras.

#### Métricas de Éxito:

Precisión: Medir qué tan preciso es el modelo al predecir las clases correctas.
Recall: Evaluar cuántas de las instancias verdaderas de cada clase fueron correctamente identificadas.
F1-Score: Balance entre precisión y recall, útil cuando se tiene un desbalance de clases.
Matriz de Confusión: Proporcionará una visualización detallada de las predicciones vs. las etiquetas verdaderas, permitiendo entender mejor las clases que están siendo confundidas.

#### Fase 2: Adquisición y Preprocesamiento de Datos
Conjunto de Datos: Se utilizará un conjunto de datos de imágenes aéreas preprocesadas que ya han sido etiquetadas por categorías. El conjunto de datos incluye imágenes de 224x224 píxeles (después del redimensionamiento), divididas en 21 clases.

#### Tareas de Preprocesamiento:
* Normalización de imágenes: Convertir las imágenes a un rango de [0, 1] dividiendo por 255.0.
* Redimensionamiento: Asegurarse de que las imágenes tengan dimensiones uniformes (224x224) para ser compatibles con el modelo EfficientNetB0.

* Aumento de Datos (Data Augmentation): Para evitar sobreajuste y mejorar la generalización, se emplearán técnicas de aumento de datos como rotación, cambio de escala, traslación, entre otras, para aumentar la diversidad de las imágenes en el conjunto de entrenamiento.

#### Fase 3: Exploración y Análisis de Datos

#### Exploración Visual:

Visualizar algunas muestras de cada clase para comprender mejor el tipo de imágenes con las que estamos trabajando.

Análisis de la distribución de clases para detectar posibles desequilibrios. Si alguna clase tiene muchas menos muestras que las demás, se considerarán técnicas como pesos de clase o submuestreo.

#### Análisis Estadístico:
Evaluar la dispersión de las imágenes, detectar posibles problemas de calidad de datos (como imágenes mal etiquetadas o irrelevantes) y asegurarse de que las etiquetas sean coherentes.

Colaboración: El equipo de datos será responsable de esta fase, mientras que los científicos de datos y el equipo de ingeniería trabajarán conjuntamente para explorar y transformar los datos para su posterior uso en el modelo.


#### Fase 4: Modelado y Entrenamiento
Modelo Seleccionado: EfficientNetB0 será el modelo preentrenado que utilizaremos debido a su eficiencia y capacidad para realizar una clasificación precisa de imágenes con una arquitectura ligera.

Fine-tuning: Fine-tune de EfficientNetB0, utilizando las primeras capas congeladas (preentrenadas en el conjunto de datos ImageNet) y reentrenando las capas superiores del modelo con el conjunto de datos específico de nuestro proyecto.

##### Ajuste de Hiperparámetros:

Selección de un optimizador adecuado (Adam, RMSprop,).
Determinación de la tasa de aprendizaje.
Uso de técnicas como early stopping para evitar sobreajuste.
Entrenamiento:

El modelo se entrenará en el conjunto de entrenamiento utilizando las imágenes preprocesadas. Se utilizará validación cruzada para ajustar hiperparámetros y prevenir el sobreajuste.
El equipo de científicos de datos se encargará del entrenamiento, mientras que los ingenieros de ML ayudarán en la implementación de técnicas de optimización y en la monitorización de los resultados.

#### Fase 5: Evaluación

Evaluación del Modelo:
Después de entrenar el modelo, se evaluará en el conjunto de datos de prueba para verificar su capacidad de generalización. Las métricas principales para evaluar el rendimiento de acuerdo a las metricas.

Matriz de Confusión para visualizar cómo el modelo clasifica correctamente o confunde las clases.

Manejo de Desbalance de Clases:
Si algunas clases tienen un rendimiento significativamente peor, el equipo de datos podría investigar posibles técnicas de re-muestreo, ajuste de pesos o incluso la reetiquetación de las clases.

Colaboración: Todos los miembros del equipo revisarán los resultados, discutiendo las posibles áreas de mejora y colaborando en la selección de ajustes a realizar.

Despliegue del Modelo como modelo descargable.

## Cronograma

| Etapa | Duración Estimada | Fechas |
|------|---------|-------|
| Entendimiento del negocio y carga de datos (fase 1 y 2) | 1 semanas | 21  al 28 de Noviembre |
| Preprocesamiento, análisis exploratorio (fase 3)| 1 semanas | del 29 de Noviembre al 5 de diciembre |
| Modelado ,entrenamiento y fine tuning (fase 4)| 1 semanas | del 6 de al 12 de Diciembre |
| Evaluación , despliegue y  entrega final (fase 5) | 1 semanas | del 13 de Diciembre al 21 de Diciembre |

Hay que tener en cuenta que estas fechas son de ejemplo, estas deben ajustarse de acuerdo al proyecto.

## Equipo del Proyecto

- Líder del proyecto / Cientifico de Datos / Ing de Dato / Ingeniero ML
- / Cientifico de Datos / Ing de Dato / Ingeniero ML

Roles en el Equipo:
Científicos de Datos: Responsable del desarrollo y ajuste del modelo, implementación de métricas, y análisis de los resultados.
Ingenieros de Datos: Encargados de la preparación de los datos, preprocesamiento, aumento de datos, y asegurarse de que los datos estén disponibles para el entrenamiento.
Ingenieros de ML: Trabajan en la implementación de modelos, optimización y ajustes de hiperparámetros, y validación de los modelos.
Ingenieros de Infraestructura: Encargados del despliegue y monitoreo del modelo en producción.
Expertos del Dominio: Aportan conocimiento específico sobre las áreas terrestres para guiar la interpretación de las clases y ayudar a validar el modelo.

Este enfoque estructurado y colaborativo asegura que el modelo de clasificación de imágenes aéreas sea de alta calidad, eficiente y esté alineado con los objetivos del proyecto, proporcionando una solución robusta que se puede mejorar de manera continua.

## Presupuesto

### Duración del Proyecto: 4 semanas

| **Concepto**               | **Descripción**                                                                | **Costo Estimado (COP)** |
|----------------------------|--------------------------------------------------------------------------------|--------------------------|
| **Científico de Datos**     | Desarrollo y ajuste de modelos, análisis de resultados, implementación de métricas de evaluación | 80,000 por hora |
| **Ingeniero de Datos**      | Preprocesamiento, aumento de datos, preparación y gestión de conjuntos de datos | 70,000 por hora |
| **Ingeniero de ML**         | Implementación de modelos, ajuste de hiperparámetros, optimización de rendimiento y despliegue | 90,000 por hora |
| **Total Horas por Semana**  | 3 personas, 15 horas por semana (45 horas semanales en total)                 | 45 x 80,000 = 3,600,000 |
| **Duración Total (4 semanas)** | Costo total de mano de obra del equipo completo durante 4 semanas           | 3,600,000 x 4 = 14,400,000 |

## Costos de Infraestructura

| **Concepto**               | **Descripción**                                                                | **Costo Estimado (COP)** |
|----------------------------|--------------------------------------------------------------------------------|--------------------------|
| **Google Colab Pro**       | Suscripción a Google Colab Pro para mejorar el rendimiento y uso de GPU/TPU (1 mes) | 30,000 por mes  |
| **Total de Google Colab Pro** | 1 suscripción para todo el equipo (3 personas)                                   | 30,000 x 1 = 30,000      |
| **Computadoras/Equipos**    | Uso de computadoras de los miembros del equipo, incluidos costos de mantenimiento y electricidad | 200,000 por persona por mes (3 personas) |
| **Total de Computadoras**   | Costos mensuales para las computadoras del equipo                             | 200,000 x 3 = 600,000    |

### **Resumen del Presupuesto por 4 Semanas**

| **Concepto**               | **Descripción**                                                                | **Costo Total (COP)**    |
|----------------------------|--------------------------------------------------------------------------------|--------------------------|
| **Mano de Obra (4 semanas)** | Costo total por el trabajo de 3 personas durante 4 semanas                    | 14,400,000               |
| **Google Colab Pro**        | Costo de la suscripción a Google Colab Pro para 1 mes                          | 30,000                   |
| **Computadoras**            | Costo de uso de computadoras de 3 personas por 1 mes                           | 600,000                  |
| **Total Proyecto (4 semanas)** | Suma de todos los costos: trabajo, infraestructura y recursos adicionales     | **15,030,000**           |


## Stakeholders

-  Delivery manager
-  Project manager

### Relación con los stakeholders:

- Delivery manager:

    * Seguimiento de entregas. El delivery manager se asegurará Asegurarse de que el trabajo del equipo de ciencia de datos (incluyendo la preparación de datos, modelado y evaluación) avance según lo planeado.

    * Comunicación con stakeholders: Proporcionar retroalimentación continua a las partes interesadas, informando sobre el progreso y asegurándose de que los entregables cumplan con los plazos establecidos.

    * Gestión de recursos y riesgos: Asegurar que los recursos estén disponibles y gestionar posibles riesgos que puedan retrasar la entrega de los resultados o los modelos.

- Project Manager:
    * Dar lineamientos generales de objetivos y alcance:
    * Dar lineamiento de aplicación  de metodologías ágiles o específicas de ciencia de datos (Team Data Science Process) para garantizar que el proyecto se ejecute de manera eficiente.
    * Identificación áreas de mejora en la ejecución del proyecto y asegurándose de que el equipo de datos esté aprendiendo y mejorando con cada iteración

## Aprobaciones

- Diego Alejandro Ferro Martínez del líder del proyecto


- [Firma del aprobador]


- 28 de Noviembre de 2024
