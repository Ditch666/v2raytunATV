# Анализ v2RayTun APK (GitHub release)

Источник: `v2RayTun_universal.apk` v5.23.73 (`com.v2raytun.android`)

## Архитектура

- **Стек:** Kotlin, View Binding, ViewPager2, Material Components
- **Ядро:** `libgojni.so` (Go/xray), `libhysteria2.so`, `libhev-socks5-tunnel.so`
- **UI:** Activities + Fragments, не Compose

## Логика «Телефон / ТВ»

Определение TV в `w.A.F(Context)` (декомпилированный `Utils.kt`):

```kotlin
fun isTv(context: Context): Boolean {
    val leanback = context.packageManager.hasSystemFeature("android.software.leanback")
    val uiMode = (context.getSystemService(UI_MODE_SERVICE) as UiModeManager).currentModeType
    return leanback || uiMode == Configuration.UI_MODE_TYPE_TELEVISION
}

fun isPhone(context: Context): Boolean = !isTv(context)
```

`MainActivity.onCreate()`:

- `isPhone` → `BottomNavigationView` + `layout/activity_main.xml`
- `isTv` → `NavigationRailView` + `layout-television/activity_main.xml`

## TV-ресурсы (уже в APK)

21 layout в `res/layout-television/`, включая:

- `activity_main.xml` — боковая навигация
- `fragment_connection.xml` — D-pad фокус, `nextFocusLeft="@id/navigationRail"`
- экраны редактирования серверов, пресетов, маршрутизации

## TV-only патчи (этот репозиторий)

| Патч | Эффект |
|------|--------|
| `leanback required=true` | APK не ставится на телефон |
| Убран `LAUNCHER` | Только иконка в TV-лаунчере |
| `F(Context)` → always `true` | Всегда TV-ветка кода |
| `layout-television/*` → `layout/` | TV-layout на всех экранах |
| `rounded_border_button.xml` | Подсветка фокуса на кнопках |
| `navbar_item_color.xml` | Подсветка фокуса в навигации |

## Ограничения сборки из APK

- Исходный Kotlin обфусцирован (`w.A`, `r.a`, …)
- Обновления — повторная декомпиляция + патчи
- Для production лучше получить исходники у авторов
