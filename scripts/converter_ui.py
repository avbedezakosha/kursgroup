import logging
import subprocess
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.Logger(__name__)


def convert_ui_files() -> None:
    input_dir: str = '..\\app\\gui\\ui'
    output_dir: str = '../app/gui/ui/generated'

    try:
        base_path = Path(__file__).parent.resolve()
        ui_path = base_path / input_dir
        py_path = base_path / output_dir

        ui_files = list(ui_path.glob('*.ui'))

        if not ui_files:
            logger.warning(f'Нет *.ui файлов в {ui_path}')

        py_path.mkdir(parents=True, exist_ok=True)

        for ui_file in ui_files:
            py_file = py_path / f'ui_{ui_file.stem}.py'
            command = [
                'pyuic5',
                '--from-imports',
                '--output', str(py_file),
                str(ui_file)
            ]

            result = subprocess.run(command, capture_output=True, text=True)

            if result.returncode == 0:
                logger.info(f'Успех: {ui_file.name} -> {py_file.name}')
            else:
                logger.error(f'Ошибка: {ui_file.name}: {result.stderr}')
    except Exception as err:
        logger.error(f"Критическая ошибка: {str(err)}", exc_info=True)


if __name__ == '__main__':
    convert_ui_files()
