import re
import os

def validate_markdown_links(filepath):
    """
    Valida links em um arquivo Markdown, verificando se os arquivos locais existem.
    """
    broken_links = []
    base_dir = os.path.dirname(filepath)

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Regex para encontrar links Markdown: [texto](url)
    # E também imagens Markdown: ![alt text](url)
    link_pattern = re.compile(r'\[.*?\]\((.*?)\)')
    links = link_pattern.findall(content)

    for link in links:
        # Ignora links externos (http, https)
        if link.startswith('http://') or link.startswith('https://'):
            continue

        # Remove âncoras (#section) de links internos
        if '#' in link:
            link = link.split('#')[0]

        # Constrói o caminho absoluto para o arquivo local
        full_path = os.path.join(base_dir, link)
        full_path = os.path.normpath(full_path)

        if not os.path.exists(full_path):
            broken_links.append(link)
            
    return broken_links

if __name__ == '__main__':
    # Exemplo de uso (assumindo que este script está em src/)
    # E o README.md está no diretório pai
    readme_path = os.path.join(os.path.dirname(__file__), '..', 'README.md')
    broken = validate_markdown_links(readme_path)
    if broken:
        print(f"Links quebrados encontrados em {readme_path}:")
        for link in broken:
            print(f"- {link}")
    else:
        print(f"Nenhum link quebrado encontrado em {readme_path}.")

