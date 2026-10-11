```powershell
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Creando estructura del proyecto ML" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

# 1. Crear carpetas
$directories = @(
    "data/raw",
    "data/processed",
    "data/external",
    "notebooks",
    "queries",
    "src",
    "models",
    "reports/figures"
)

foreach ($directory in $directories) {
    New-Item -ItemType Directory -Path $directory -Force | Out-Null
}

# 2. Crear notebooks
$notebooks = @(
    "notebooks/01_eda.ipynb",
    "notebooks/02_cleaning.ipynb",
    "notebooks/03_modeling.ipynb",
    "notebooks/04_evaluation.ipynb"
)

# 3. Crear archivos Python
$pythonFiles = @(
    "src/__init__.py",
    "src/data_processing.py",
    "src/evaluate.py",
    "src/features.py",
    "src/train.py",
    "src/utils.py"
)

# 4. Crear consultas SQL
$sqlFiles = @(
    "queries/query_build_master_dataset.sql",
    "queries/query_exploratory_clientes.sql",
    "queries/query_exploratory_historial_mensual.sql",
    "queries/query_exploratory_registres_number.sql",
    "queries/query_tables.sql"
)

# 5. Crear archivos de configuración
$configFiles = @(
    ".gitignore",
    "README.md",
    "requirements.txt",
    "pyproject.toml"
)

# 6. Crear archivos sin sobrescribir los existentes
$files = $notebooks + $pythonFiles + $sqlFiles + $configFiles

foreach ($file in $files) {
    if (-not (Test-Path $file)) {
        New-Item -ItemType File -Path $file | Out-Null
    }
}

Write-Host ""
Write-Host "Estructura creada correctamente." -ForegroundColor Green
Write-Host "Los archivos existentes se conservaron." -ForegroundColor Yellow
```
