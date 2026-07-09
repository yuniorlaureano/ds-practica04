# ds-practica04
Pract. 04-Proyecto Final [COLABORATIVO]: de Machine Learning sobre OULAD

## Estructura del proyecto

```
ds-practica04/
├── data/                       # CSVs fuente del dataset OULAD
│   ├── assess_detail.csv
│   ├── assess_plan.csv
│   ├── cursos.csv
│   ├── registrations.csv
│   ├── student_info.csv
│   ├── vle_click_stream.csv
│   └── vle_modules.csv
├── notebooks/
│   └── mian.ipynb              # Notebook de exploración y análisis
├── sql/
│   └── create_tables.sql       # DDL de las tablas destino en SQL Server
├── src/
│   ├── main.py                 # Punto de entrada: ejecuta el pipeline de carga
│   ├── db/
│   │   ├── operations.py       # CRUD y bulk copy contra SQL Server (mssql-python)
│   │   └── queries.py          # Queries SQL reutilizables (p. ej. CREATE_TABLES)
│   ├── pipelines/
│   │   ├── oulad_pypeline.py   # Orquesta la carga de cada CSV a su tabla
│   │   └── validators.py       # Reglas de validación de datos por dataset
│   └── util/
│       ├── config.py           # Carga la configuración desde variables de entorno (.env)
│       ├── csv_reader_helper.py# Lectura/streaming de CSVs por chunks
│       ├── custom_path.py      # Resolución de rutas hacia los archivos en /data
│       └── helper.py           # Utilidades varias
├── .env                        # Variables de entorno locales (NO se sube a git)
├── requirements.txt            # Dependencias fijadas del proyecto
└── README.md
```

## Requisitos previos

- Python 3.12 o superior
- Acceso a una instancia de SQL Server (local o remota)
- [ODBC Driver 18 for SQL Server](https://learn.microsoft.com/sql/connect/odbc/download-odbc-driver-for-sql-server) instalado en el equipo (requerido por `mssql-python`)

## Instalación

1. Crear y activar un entorno virtual en la raíz del proyecto:

   ```powershell
   python -m venv .venv
   .venv\Scripts\activate
   ```

2. Instalar las librerías necesarias:

   ```powershell
   pip install mssql-python python-dotenv numpy pandas matplotlib seaborn scipy scikit-learn
   ```

## Configuración de la conexión a la base de datos (.env)

La cadena de conexión se carga con `python-dotenv` desde un archivo `.env` ubicado en la raíz del proyecto (ver [src/util/config.py](src/util/config.py)). Este archivo **no se versiona** (está listado en `.gitignore`), por lo que cada persona debe crear el suyo localmente.

1. Crear un archivo `.env` en la raíz del proyecto.
2. Definir la variable `CON_STRING` con el formato que espera `mssql-python`:

   ```env
   CON_STRING="Server=<host>;Database=<nombre_bd>;Uid=<usuario>;Pwd=<password>;TrustServerCertificate=yes;"
   ```

   Ejemplo:

   ```env
   CON_STRING="Server=localhost;Database=OULAD_KONGO;Uid=sa;Pwd=TuPasswordAqui;TrustServerCertificate=yes;"
   ```

   | Parámetro              | Descripción                                             |
   |------------------------|----------------------------------------------------------|
   | `Server`               | Host o IP del servidor SQL Server                        |
   | `Database`             | Nombre de la base de datos destino                       |
   | `Uid` / `Pwd`          | Credenciales de acceso                                    |
   | `TrustServerCertificate` | `yes` para omitir la validación del certificado TLS (útil en entornos de desarrollo) |

`Config` (en `src/util/config.py`) llama a `load_dotenv()` y expone el valor mediante `config.CON_STRING`, el cual es usado por [src/db/operations.py](src/db/operations.py) para abrir la conexión con `mssql_python.connect(...)`.

## Ejecución

Desde la carpeta `src/`, ejecutar el pipeline de carga completo (crea las tablas e inserta los CSV de `data/`):

```powershell
cd src
python main.py
```

## Ejecución en Google Colab

Para correr en colab solo debe acceder al link que le estaremos proveyendo en el archivo `Instrucciones y enlaces.docx`, en el archivo zip adjunto a la tarea. Este archivo contiene los enlaces a los diferentes servicios que se están consumiendo
