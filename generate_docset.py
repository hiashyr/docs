#!/usr/bin/env python3
import os
import shutil
import sqlite3
from pathlib import Path

def build_and_create_docset():
    """Собирает Sphinx документацию и создает docset"""
    
    print("🚀 Сборка документации...")
    
    # Собираем HTML
    result = os.system("make html")
    if result != 0:
        print("❌ Ошибка при сборке документации!")
        return
    
    # Создаем docset структуру
    docset_dir = Path("My Django Project.docset")
    if docset_dir.exists():
        shutil.rmtree(docset_dir)
        print("🗑️ Удален старый docset")
    
    (docset_dir / "Contents/Resources/Documents").mkdir(parents=True)
    print("📁 Создана структура папок")
    
    # Копируем HTML
    html_dir = Path("build/html")
    if not html_dir.exists():
        print("❌ Папка build/html не найдена!")
        return
    
    copied_files = 0
    for item in html_dir.rglob("*"):
        if item.is_file():
            relative = item.relative_to(html_dir)
            dest = docset_dir / "Contents/Resources/Documents" / relative
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(item, dest)
            copied_files += 1
    
    print(f"📄 Скопировано файлов: {copied_files}")
    
    # Создаем индекс поиска
    create_search_index(docset_dir)
    
    # Info.plist
    create_info_plist(docset_dir)
    
    print(f"✅ Docset создан: {docset_dir}")
    
    # Копируем в Zeal
    copy_to_zeal(docset_dir)

    # Копируем иконку если она существует
    icon_src = Path("icon.png")
    if icon_src.exists():
        shutil.copy2(icon_src, docset_dir / "icon.png")
        print("🎨 Иконка добавлена в docset")
    else:
        print("⚠️ Иконка не найдена. Создайте файл icon.png в папке docs/")

def create_search_index(docset_dir):
    """Создает поисковый индекс"""
    conn = sqlite3.connect(docset_dir / "Contents/Resources/docSet.dsidx")
    cur = conn.cursor()
    
    cur.execute('''
        CREATE TABLE searchIndex(
            id INTEGER PRIMARY KEY,
            name TEXT,
            type TEXT,
            path TEXT
        )
    ''')
    cur.execute('CREATE UNIQUE INDEX anchor ON searchIndex (name, type, path)')
    
    # Добавляем элементы в индекс
    index_entries = [
        # Основные разделы
        ('Главная', 'Guide', 'index.html'),
        ('Настройка окружения', 'Guide', 'setup.html'),
        
        # Команды Django
        ('runserver', 'Command', 'setup.html#id5'),
        ('makemigrations', 'Command', 'setup.html#id6'),
        ('migrate', 'Command', 'setup.html#id6'),
        ('startapp', 'Command', 'setup.html#id6'),
        ('createsuperuser', 'Command', 'setup.html#id6'),
        
        # Ключевые концепции
        ('Виртуальное окружение', 'Concept', 'setup.html#id2'),
        ('requirements.txt', 'Concept', 'setup.html#id7'),
        ('Django проект', 'Concept', 'setup.html#id3'),
        
        # Предстоящие разделы (можно добавить позже)
        ('Структура проекта', 'Guide', 'project-structure.html'),
        ('Модели', 'Guide', 'models.html'),
        ('Представления', 'Guide', 'views.html'),
        ('Шаблоны', 'Guide', 'templates.html'),
        ('URLs', 'Guide', 'urls.html'),
        ('Формы', 'Guide', 'forms.html'),
        ('Админка', 'Guide', 'admin.html'),
    ]
    
    cur.executemany(
        'INSERT OR IGNORE INTO searchIndex(name, type, path) VALUES (?, ?, ?)',
        index_entries
    )
    
    conn.commit()
    conn.close()
    print(f"🔍 Добавлено записей в индекс: {len(index_entries)}")
    
def create_info_plist(docset_dir):
    """Создает Info.plist для docset"""
    info_plist = '''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleIdentifier</key>
    <string>django-russian-docs</string>
    <key>CFBundleName</key>
    <string>Документация Django на русском</string>
    <key>DocSetPlatformFamily</key>
    <string>mydjangoproject</string>
    <key>dashIndexFilePath</key>
    <string>index.html</string>
    <key>isJavaScriptEnabled</key>
    <true/>
    <key>isDashDocset</key>
    <true/>
</dict>
</plist>'''
    
    with open(docset_dir / "Contents/Info.plist", "w") as f:
        f.write(info_plist)
    print("⚙️ Создан Info.plist")

def copy_to_zeal(docset_dir):
    """Копирует docset в Zeal"""
    zeal_path = Path.home() / 'Library/Application Support/Zeal/Zeal/docsets'
    zeal_path.mkdir(parents=True, exist_ok=True)
    
    dest_path = zeal_path / docset_dir.name
    
    # Удаляем старую версию если существует
    if dest_path.exists():
        shutil.rmtree(dest_path)
        print("🗑️ Удалена старая версия из Zeal")
    
    # Копируем в Zeal
    shutil.copytree(docset_dir, dest_path)
    print(f"✅ Docset скопирован в Zeal: {dest_path}")

if __name__ == "__main__":
    build_and_create_docset()