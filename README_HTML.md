# Symulator Generatora Synchronicznego - Wersja HTML

## 🌐 Pełna Aplikacja Webowa

Interaktywny symulator dynamiczny generatora synchronicznego trójfazowego napisany w czystym HTML/JavaScript.

## ✨ Funkcje

### 📊 Kompletne Rozwiązanie Problemu
Generator synchroniczny trójfazowy:
- **Moc znamionowa**: 200 MVA, 16 kV (L-L)
- **Reaktancja synchroniczna**: Xs = 1.60 p.u.
- **Napięcie na zaciskach**: 15 kV
- **SEM wewnętrzna**: 24 kV
- **Kąt mocy**: δ = 25°

Automatyczne obliczenia:
- **(a)** Prąd linii: 0.476 p.u. = 3.435 kA
- **(b)** Moc: P = 74.29 MW, Q = 49.45 MVAR
- **(c)** Prąd 75%, ten sam wsp. mocy: E = 21.46 kV, δ = 20.76°
- **(d)** Wsp. mocy = 1.0: E = 17.56 kV, δ = 31.35°
- **(e)** Diagramy fazorowe dla wszystkich warunków

### 🎛️ Interaktywne Suwaki
Kontrola parametrów w czasie rzeczywistym:
- Reaktancja synchroniczna (Xs)
- Napięcie zaciskowe (V)
- SEM wewnętrzna (E)
- Kąt mocy (δ)
- Moc mechaniczna (Pm)
- Stała bezwładności (H)
- Współczynnik tłumienia (D)
- Czas symulacji

### 🔬 Symulacja Dynamiczna ODE
Dwa solvery:
- **RK45** (Runge-Kutta 4. rzędu) - wysoka dokładność
- **Euler** - szybki, edukacyjny

Równanie wahań: `d²δ/dt² = (Pm - Pe - D·ω)/(2H)`

### 📈 Wizualizacje w Czasie Rzeczywistym
Cztery dynamiczne wykresy:
1. **Charakterystyka Moc-Kąt** - krzywa Pe(δ) z punktami roboczymi
2. **Diagramy Fazorowe** - wszystkie trzy warunki pracy
3. **Delta vs Czas** - dynamika kąta mocy
4. **Omega vs Czas** - odchylenie prędkości podczas stanów przejściowych

### 🎬 Animacja
- Odtwarzanie w czasie rzeczywistym
- Markery pokazujące aktualny punkt w czasie
- Zapętlona animacja

### 📱 Responsywny Design
- Automatyczne dopasowanie do rozmiaru okna
- Wykresy skalowane dynamicznie
- Działa na desktop i mobile

## 🚀 Jak Używać

### Otwarcie Aplikacji
Wystarczy otworzyć plik w przeglądarce:

```bash
# W Linux/Mac
xdg-open synchronous_generator_simulator.html

# W Windows
start synchronous_generator_simulator.html

# Lub po prostu kliknij dwukrotnie plik
```

### Brak Instalacji!
- ✅ Nie wymaga instalacji Python
- ✅ Nie wymaga instalacji bibliotek
- ✅ Działa offline (po pierwszym załadowaniu)
- ✅ Kompatybilny ze wszystkimi nowoczesnymi przeglądarkami

### Obsługa

#### 1. Dostosowanie Parametrów
- Przesuń suwaki aby zmienić wartości
- Aplikacja automatycznie przelicza wyniki
- Wszystkie obliczenia aktualizują się dynamicznie

#### 2. Przeglądanie Wyników
- **Panel Wyników**: Szczegółowe obliczenia dla części (a-d)
- **Wykres Moc-Kąt**: Pokazuje krzywą Pe(δ) z punktami roboczymi
- **Diagram Fazorowy**: Pokazuje relacje napięć, prądów i SEM

#### 3. Uruchomienie Symulacji Dynamicznej
1. Dostosuj moc mechaniczną (Pm), bezwładność (H) i tłumienie (D)
2. Wybierz typ solvera (RK45 lub Euler)
3. Kliknij przycisk **"▶️ Symuluj"**
4. Zobacz wyniki w dziedzinie czasu na dolnych wykresach

#### 4. Animacja
1. Po uruchomieniu symulacji kliknij **"🎬 Animacja"**
2. Oglądaj odtwarzanie dynamiki generatora w czasie rzeczywistym
3. Kliknij **"⏸️ Stop"** aby zatrzymać
4. Animacja automatycznie się zapętla

#### 5. Reset
- Kliknij przycisk **"🔄 Reset"** aby przywrócić domyślne wartości

## 🔧 Szczegóły Techniczne

### Technologie
- **HTML5** - struktura
- **CSS3** - stylowanie z gradientami
- **JavaScript (ES6+)** - logika obliczeń
- **Plotly.js** - interaktywne wykresy
- **Canvas API** - diagramy fazorowe

### Wartości Bazowe
- **S_base** = 200 MVA
- **V_base (L-L)** = 16 kV
- **V_base (faza)** = 16/√3 kV = 9.238 kV
- **I_base** = 200 MVA / (√3 × 16 kV) = 7.217 kA
- **Z_base** = 16² / 200 = 1.28 Ω

### Obliczenia

#### Obliczanie Prądu
```
Ia = (E∠δ - V∠0°) / (jXs)
```

#### Obliczanie Mocy
```
S = V × Ia*
P = Re(S)
Q = Im(S)
```

#### Równanie Wahań
```
M × d²δ/dt² = Pm - Pe - D × dδ/dt
gdzie:
  M = 2H / ω_base
  Pe = (E × V / Xs) × sin(δ)
  ω_base = 2π × 60 rad/s (dla 60 Hz)
```

### Implementacja Solverów

#### RK4 (uproszczona RK45)
- Metoda 4. rzędu
- Doskonała dokładność
- Automatyczna kontrola kroku czasowego
- Zalecany do dokładnych wyników

#### Metoda Eulera
- Metoda 1. rzędu
- Prosta i szybka
- Stały krok czasowy
- Dobra do celów edukacyjnych

## 📊 Przykładowe Wyniki

### Konfiguracja Domyślna
Z parametrami domyślnymi (E=24kV, V=15kV, δ=25°, Xs=1.60 p.u.):

**Część (a)**:
- |Ia| ≈ 0.476 p.u. ≈ 3.435 kA
- ∠Ia ≈ -33.65°

**Część (b)**:
- P ≈ 74.29 MW
- Q ≈ 49.45 MVAR
- Współczynnik mocy ≈ 0.832 opóźniony

**Część (c)**: (75% prądu, ten sam wsp. mocy)
- E ≈ 21.46 kV (L-L)
- δ ≈ 20.76°

**Część (d)**: (Wsp. mocy = 1.0)
- E ≈ 17.56 kV (L-L)
- δ ≈ 31.35°

## 🌟 Zalety Wersji HTML

### ✅ Łatwość Użycia
- Brak instalacji - po prostu otwórz w przeglądarce
- Działa na każdym systemie (Windows, Mac, Linux)
- Nie wymaga uprawnień administratora

### ✅ Przenośność
- Jeden plik - łatwy do udostępnienia
- Działa offline
- Można umieścić na stronie WWW
- Można uruchomić z pendrive'a

### ✅ Wydajność
- Natychmiastowe uruchomienie
- Szybkie obliczenia
- Płynne animacje
- Interaktywne wykresy z zoomem i przesuwaniem

### ✅ Nowoczesny Interfejs
- Piękny design z gradientami
- Responsywny layout
- Intuicyjna obsługa
- Profesjonalny wygląd

## 🎓 Wartość Edukacyjna

Symulator doskonale nadaje się do:
- Zrozumienia pracy generatora synchronicznego
- Wizualizacji relacji fazorowych
- Nauki o krzywych moc-kąt
- Studiowania stabilności przejściowej
- Porównywania metod rozwiązywania równań różniczkowych
- Eksploracji wpływu parametrów na zachowanie generatora

## 🔒 Bezpieczeństwo i Prywatność
- Wszystkie obliczenia wykonywane lokalnie w przeglądarce
- Brak wysyłania danych do zewnętrznych serwerów
- Nie wymaga połączenia internetowego (po załadowaniu Plotly.js)
- Nie śledzi użytkowników

## 📱 Kompatybilność

### Przeglądarki
- ✅ Chrome 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Edge 90+
- ✅ Opera 76+

### Systemy Operacyjne
- ✅ Windows 10/11
- ✅ macOS 10.15+
- ✅ Linux (wszystkie dystrybucje)
- ✅ Android 9+
- ✅ iOS 14+

## 🆚 Porównanie: HTML vs Python

| Funkcja | HTML | Python/Tkinter |
|---------|------|----------------|
| Instalacja | ❌ Nie wymagana | ✅ Wymagana |
| Biblioteki | ❌ Nie | ✅ numpy, scipy, matplotlib |
| Przenośność | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| Szybkość uruchomienia | ⚡ Natychmiastowa | ⏱️ Kilka sekund |
| Interfejs | 🎨 Nowoczesny | 📊 Standardowy |
| Obliczenia | ✅ Identyczne | ✅ Identyczne |
| Wykresy | ✅ Interaktywne | ✅ Statyczne/Interactive |
| Animacje | ✅ Płynne | ✅ Płynne |
| Edycja kodu | 📝 Łatwiejsza | 📝 Standard |

## 🎯 Wskazówki

### Optymalizacja Wydajności
- Dla długich symulacji użyj solvera Euler
- Zwiększ krok czasowy dla szybszych obliczeń
- Zmniejsz czas symulacji dla szybszego przetwarzania

### Najlepsze Praktyki
1. Zacznij od domyślnych parametrów
2. Zmień jeden parametr na raz aby zobaczyć efekt
3. Użyj RK45 dla dokładnych wyników
4. Użyj Euler do szybkiego podglądu

## 📖 Dokumentacja

### Struktura Kodu
```
synchronous_generator_simulator.html
├── HTML Structure (linie 1-300)
│   ├── Header
│   ├── Control Panel
│   └── Results & Plots Area
├── CSS Styling (linie 8-200)
│   ├── Responsive Grid
│   ├── Modern Design
│   └── Animations
└── JavaScript (linie 300-koniec)
    ├── Calculations
    ├── ODE Solvers
    ├── Plotting Functions
    └── Animation Control
```

## 🔄 Aktualizacje

### Wersja 1.0.0
- ✅ Pełna implementacja wszystkich obliczeń
- ✅ Dwa solvery ODE (RK45, Euler)
- ✅ Interaktywne wykresy Plotly
- ✅ Canvas diagramy fazorowe
- ✅ Animacja w czasie rzeczywistym
- ✅ Responsywny design
- ✅ Polska lokalizacja

## 📞 Wsparcie

Jeśli masz pytania lub sugestie:
1. Sprawdź kod źródłowy - jest dobrze skomentowany
2. Eksperymentuj z parametrami
3. Porównaj wyniki z wersją Python

## 🎉 Ciesz się!

Aplikacja jest gotowa do użycia. Otwórz plik HTML w przeglądarce i zacznij eksplorować fascynujący świat generatorów synchronicznych!

---

**Wersja**: 1.0.0
**Data**: 2025
**Typ**: Aplikacja webowa (HTML/JavaScript)
**Licencja**: Narzędzie edukacyjne - wolne użytkowanie
