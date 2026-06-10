# v2RayTun TV

TV-only сборка v2RayTun на основе официального APK с GitHub.

## Где скачать готовый APK

**Готовый файл не лежит в репозитории** (он весит ~96 МБ и собирается автоматически).

### Вариант 1 — GitHub Releases (самый простой)

После публикации релиза файл будет здесь:

**https://github.com/Ditch666/v2raytunATV/releases**

Ищите файл: `v2RayTun-tv.apk`

### Вариант 2 — GitHub Actions (артефакт сборки)

1. Откройте **https://github.com/Ditch666/v2raytunATV/actions**
2. Выберите workflow **Build Android TV APK**
3. Откройте последний успешный запуск (зелёная галочка)
4. Внизу страницы — раздел **Artifacts**
5. Скачайте **v2RayTun-tv-apk** (внутри будет `v2RayTun-tv.apk`)

Если сборок ещё нет — нажмите **Run workflow** справа, чтобы запустить вручную.

### Вариант 3 — Собрать у себя на компьютере

```bash
git clone https://github.com/Ditch666/v2raytunATV.git
cd v2raytunATV
chmod +x android-tv/scripts/build-tv-apk.sh
./android-tv/scripts/build-tv-apk.sh
```

Файл появится локально: `build/android-tv/output/v2RayTun-tv.apk`

---

## Отличия от universal APK

- Устанавливается **только на Android TV** (`leanback` required)
- Нет иконки в лаунчере телефона — только `LEANBACK_LAUNCHER`
- Всегда используется TV-интерфейс (боковая навигация, D-pad)
- Усилена подсветка фокуса на кнопках и элементах навигации

## Сборка

```bash
# Из корня репозитория
chmod +x android-tv/scripts/build-tv-apk.sh
./android-tv/scripts/build-tv-apk.sh
```

Готовый APK: `build/android-tv/output/v2RayTun-tv.apk`

### Требования

- Java 17+
- Python 3
- `curl`, `keytool`
- `tools/apktool.jar` (скачивается при первой настройке окружения)

## Установка на TV

```bash
adb connect <tv-ip>:5555
adb install -r build/android-tv/output/v2RayTun-tv.apk
```

## Управление пультом

| Клавиша | Действие |
|---------|----------|
| ↑ ↓ ← → | Перемещение фокуса |
| OK / Enter | Выбор элемента |
| Back | Назад |

Фокус подсвечивается рамкой accent-цвета на кнопках и пунктах навигации.

## Структура

```
android-tv/
├── ANALYSIS.md          # Результаты анализа APK
├── patches/             # Ресурсы и smali-патчи
├── scripts/
│   ├── apply-tv-patches.py
│   └── build-tv-apk.sh
└── README.md
```

Подробный анализ декомпиляции: [ANALYSIS.md](ANALYSIS.md)
