"""Script principal que orquestra a coleta e visualização de dados climáticos"""

import subprocess
import sys
import os
from pathlib import Path
from dotenv import load_dotenv
from config import APP_NAME, DATA_DIR, CSV_FILE
from logger_config import get_logger

load_dotenv()
logger = get_logger('main')

DASHBOARD_FILE = Path('dashboard.py')
FETCH_FILE = Path('fetch_weather.py')

def check_files():
    """Verifica se os arquivos necessários existem"""
    Path(DATA_DIR).mkdir(exist_ok=True)
    
    missing_files = []
    if not DASHBOARD_FILE.exists():
        missing_files.append('dashboard.py')
    if not FETCH_FILE.exists():
        missing_files.append('fetch_weather.py')
    
    if missing_files:
        logger.error(f"Arquivos não encontrados: {', '.join(missing_files)}")
        sys.exit(1)
    
    logger.info("✅ Todos os arquivos necessários foram encontrados")

def fetch_weather():
    """Executa o script de coleta de dados da API"""
    logger.info("📡 Atualizando dados climáticos da API...")
    
    try:
        result = subprocess.run(
            [sys.executable, str(FETCH_FILE)],
            check=False,
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            logger.info("✅ Dados climáticos atualizados com sucesso!")
            return True
        else:
            logger.warning("⚠️ Falha ao atualizar dados da API. Continuando com dados existentes...")
            if result.stderr:
                logger.debug(f"Erro: {result.stderr}")
            return False
            
    except Exception as e:
        logger.error(f"❌ Erro ao executar fetch_weather.py: {str(e)}")
        return False

def validate_data():
    """Valida se os dados necessários existem antes de iniciar o dashboard"""
    if not Path(CSV_FILE).exists():
        logger.warning(f"⚠️ Arquivo de dados {CSV_FILE} não encontrado")
        logger.info("Tentando buscar dados da API...")
        if not fetch_weather():
            logger.error("❌ Não foi possível obter dados. Encerrando.")
            sys.exit(1)

def start_dashboard():
    """Inicia o dashboard do Streamlit"""
    logger.info(f"🚀 Iniciando {APP_NAME} Dashboard...")
    
    try:
        subprocess.run(
            ['streamlit', 'run', str(DASHBOARD_FILE)],
            check=False
        )
    except FileNotFoundError:
        logger.error("❌ Streamlit não está instalado. Execute: pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        logger.error(f"❌ Erro ao iniciar dashboard: {str(e)}")
        sys.exit(1)

def main():
    """Função principal"""
    logger.info(f"{'='*60}")
    logger.info(f"Iniciando {APP_NAME}")
    logger.info(f"{'='*60}")
    
    try:
        check_files()
        validate_data()
        fetch_weather()
        start_dashboard()
    except KeyboardInterrupt:
        logger.info("\n⚠️ Aplicação interrompida pelo usuário")
        sys.exit(0)
    except Exception as e:
        logger.error(f"❌ Erro inesperado: {str(e)}", exc_info=True)
        sys.exit(1)

if __name__ == '__main__':
    main()
