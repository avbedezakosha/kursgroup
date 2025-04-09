from pathlib import Path
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom


def generate_qrc(resources_dir: str, output_file: str, prefixes: dict):
    root = Element('RCC', version='1.0')

    # Исправление 1: Создаем отдельный qresource для каждого префикса
    for prefix, folder in prefixes.items():
        qresource = SubElement(root, 'qresource', {'prefix': prefix.strip('/')})
        folder_path = Path(resources_dir) / folder

        if not folder_path.exists():
            continue

        # Исправление 2: Рекурсивный поиск файлов с правильным относительным путем
        for file_path in sorted(folder_path.rglob('*')):
            if file_path.is_file() and not file_path.name.startswith('.'):
                # Исправление 3: Правильное формирование относительного пути
                rel_path = file_path.relative_to(resources_dir)

                # Исправление 4: Нормализация путей для разных ОС
                normalized_path = rel_path.as_posix()

                # Исправление 5: Правильный alias без дублирования префикса
                SubElement(
                    qresource,
                    'file',
                    {'alias': normalized_path.replace(folder, '').lstrip('/')}
                ).text = normalized_path

    # Форматирование XML
    xml_str = minidom.parseString(tostring(root)).toprettyxml(indent='  ')
    xml_str = '\n'.join([line for line in xml_str.split('\n') if line.strip()][1:])

    # Создание родительских директорий
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open('w', encoding='utf-8') as f:
        f.write(f'<!DOCTYPE RCC>\n{xml_str}')


if __name__ == "__main__":
    CONFIG = {
        'resources_dir': Path(__file__).parent.parent,
        'output_file': Path(__file__).parent.parent / 'src' / 'generated' / 'resources.qrc',
        'prefixes': {
            'images': 'assets/images',  # Исправление 6: Убрал слеши в ключах
            'icons': 'assets/icons',
            'fonts': 'assets/fonts',
            'styles': 'styles'
        }
    }

    generate_qrc(**CONFIG)
    print(f"Resource file generated at: {CONFIG['output_file']}")