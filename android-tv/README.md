# v2RayTun TV

TV-only сборка v2RayTun на основе официального APK с GitHub.

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
