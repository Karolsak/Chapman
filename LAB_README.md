# Laboratorium Modelowania Silników Elektrycznych

Interaktywna aplikacja do symulacji i badania różnych typów silników elektrycznych z interfejsem graficznym opartym na tkinter.

## Opis

Aplikacja umożliwia modelowanie i analizę trzech głównych typów silników elektrycznych:

### 1. Silnik DC (prądu stałego)
- **Wzbudzenie bocznikowe (shunt)** - wzbudzenie równolegle z twornikiem
- **Wzbudzenie szeregowe (series)** - wzbudzenie szeregowo z twornikiem
- **Wzbudzenie obce (separate)** - niezależne wzbudzenie

**Charakterystyki:**
- Moment vs Prędkość
- Prąd twornika vs Moment
- Sprawność vs Moment
- Moc wyjściowa vs Prędkość

### 2. Silnik Indukcyjny (asynchroniczny)
Model oparty na schemacie zastępczym IEEE z uwzględnieniem:
- Rezystancji i reaktancji stojana
- Rezystancji i reaktancji wirnika
- Reaktancji magnesującej

**Charakterystyki:**
- Moment vs Prędkość
- Moment vs Poślizg
- Sprawność vs Prędkość
- Współczynnik mocy vs Moment

### 3. Silnik Synchroniczny
Model z uwzględnieniem:
- Reaktancji synchronicznej
- SEM wzbudzenia
- Kąta obciążenia

**Charakterystyki:**
- Moment vs Kąt obciążenia
- Prąd vs Kąt obciążenia
- Współczynnik mocy vs Moment
- Moc wyjściowa vs Kąt obciążenia

## Instalacja

### Wymagania
- Python 3.7 lub nowszy
- NumPy
- Matplotlib
- Tkinter (zazwyczaj wbudowany w Pythonie)

### Instalacja zależności

```bash
pip install -r requirements_lab.txt
```

lub bezpośrednio:

```bash
pip install numpy matplotlib
```

## Uruchomienie

```bash
python electric_motor_lab.py
```

lub:

```bash
python3 electric_motor_lab.py
```

## Użytkowanie

1. **Wybierz typ silnika** - kliknij odpowiednią zakładkę (Silnik DC, Silnik Indukcyjny, Silnik Synchroniczny)

2. **Ustaw parametry** - w lewym panelu wprowadź parametry silnika:
   - Napięcia zasilania
   - Rezystancje i reaktancje
   - Stałe silnika
   - Parametry konstrukcyjne

3. **Uruchom symulację** - kliknij przycisk "Uruchom Symulację"

4. **Analizuj wyniki** - sprawdź wykresy charakterystyk:
   - Powiększaj wykresy (ikona lupy)
   - Przesuwaj widok (ikona krzyżyka)
   - Zapisuj wykresy (ikona dyskietki)

5. **Eksperymentuj** - zmieniaj parametry i obserwuj wpływ na charakterystyki

## Parametry silników

### Silnik DC

| Parametr | Symbol | Jednostka | Zakres | Opis |
|----------|--------|-----------|--------|------|
| Napięcie | V | V | 0-500 | Napięcie zasilania |
| Rezystancja twornika | Ra | Ω | 0.01-10 | Rezystancja obwodu twornika |
| Rezystancja wzbudzenia | Rf | Ω | 1-500 | Rezystancja obwodu wzbudzenia |
| Stała SEM | Ke | V·s/rad | 0.1-5 | Stała siły elektromotorycznej |
| Stała momentu | Kt | N·m/A | 0.1-5 | Stała momentu elektromagnetycznego |

### Silnik Indukcyjny

| Parametr | Symbol | Jednostka | Zakres | Opis |
|----------|--------|-----------|--------|------|
| Liczba biegunów | P | - | 2-12 | Liczba biegunów (parzysta) |
| Napięcie | V | V | 100-1000 | Napięcie fazowe |
| Częstotliwość | f | Hz | 25-100 | Częstotliwość sieci |
| Rezystancja stojana | Rs | Ω | 0.01-10 | Rezystancja uzwojenia stojana |
| Rezystancja wirnika | Rr | Ω | 0.01-10 | Rezystancja uzwojenia wirnika |
| Reaktancja stojana | Xs | Ω | 0.1-10 | Reaktancja rozproszenia stojana |
| Reaktancja wirnika | Xr | Ω | 0.1-10 | Reaktancja rozproszenia wirnika |
| Reaktancja magn. | Xm | Ω | 10-200 | Reaktancja magnesująca |

### Silnik Synchroniczny

| Parametr | Symbol | Jednostka | Zakres | Opis |
|----------|--------|-----------|--------|------|
| Liczba biegunów | P | - | 2-12 | Liczba biegunów (parzysta) |
| Napięcie | V | V | 100-1000 | Napięcie fazowe |
| Częstotliwość | f | Hz | 25-100 | Częstotliwość sieci |
| Reaktancja synch. | Xs | Ω | 0.1-10 | Reaktancja synchroniczna |
| Rezystancja twornika | Ra | Ω | 0.01-5 | Rezystancja uzwojenia twornika |
| SEM wzbudzenia | Ef | V | 100-1000 | Siła elektromotoryczna wzbudzenia |

## Przykłady zastosowań

### 1. Analiza wpływu wzbudzenia na charakterystyki silnika DC
```
- Ustaw typ wzbudzenia: bocznikowe
- Uruchom symulację i zaobserwuj charakterystyki
- Zmień na wzbudzenie szeregowe
- Porównaj różnice w charakterystykach moment-prędkość
```

### 2. Badanie punktu maksymalnego momentu silnika indukcyjnego
```
- Ustaw parametry silnika indukcyjnego
- Uruchom symulację
- Na wykresie Moment-Poślizg znajdź punkt maksymalny
- Sprawdź odpowiadającą prędkość i poślizg
```

### 3. Optymalizacja współczynnika mocy silnika synchronicznego
```
- Ustaw parametry silnika
- Uruchom symulację
- Obserwuj wykres Współczynnik mocy vs Moment
- Dostosuj SEM wzbudzenia (Ef) dla uzyskania cos(φ) = 1
```

## Podstawy teoretyczne

### Równania silnika DC

**Napięcie:**
```
V = Ea + Ia·Ra
Ea = Ke·φ·ω
```

**Moment:**
```
T = Kt·φ·Ia
```

### Równania silnika indukcyjnego

**Moment elektromagnetyczny:**
```
T = (3·V²·Rr/s) / (ωs·[(Rs + Rr/s)² + (Xs + Xr)²])
```

**Poślizg:**
```
s = (ns - n) / ns
```

### Równania silnika synchronicznego

**Moment:**
```
T = (3·V·Ef·sin(δ)) / (ωs·Xs)
```

**Prędkość synchroniczna:**
```
ns = 120·f / P [RPM]
ωs = 2·π·f / (P/2) [rad/s]
```

## Dodatkowe funkcje

- **Zoom** - powiększanie obszarów wykresów
- **Pan** - przesuwanie widoku wykresu
- **Save** - zapisywanie wykresów do plików
- **Reset** - powrót do domyślnego widoku
- **Grid** - automatyczna siatka na wykresach

## Struktura kodu

```
electric_motor_lab.py
├── DCMotor - Klasa modelu silnika DC
├── InductionMotor - Klasa modelu silnika indukcyjnego
├── SynchronousMotor - Klasa modelu silnika synchronicznego
└── MotorLabGUI - Główna klasa interfejsu graficznego
    ├── create_dc_motor_tab() - Zakładka silnika DC
    ├── create_induction_motor_tab() - Zakładka silnika indukcyjnego
    ├── create_sync_motor_tab() - Zakładka silnika synchronicznego
    └── create_comparison_tab() - Zakładka informacyjna
```

## Rozwiązywanie problemów

### Problem: Brak modułu tkinter
```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# Fedora
sudo dnf install python3-tkinter

# macOS (zwykle wbudowany)
brew install python-tk
```

### Problem: Błędy matplotlib
```bash
pip install --upgrade matplotlib
```

### Problem: Aplikacja nie uruchamia się
- Sprawdź wersję Pythona: `python --version` (wymagane ≥3.7)
- Sprawdź instalację zależności: `pip list | grep -E "numpy|matplotlib"`
- Uruchom w trybie verbose: `python -v electric_motor_lab.py`

## Licencja

Ten kod jest częścią projektu edukacyjnego TSE3080 Electrical Machines.

## Autor

Laboratorium stworzone dla kursu TSE3080 - Electrical Machines

## Odnośniki

- [Chapman - Electric Machinery Fundamentals](http://www.mhhe.com/chapman)
- [NumPy Documentation](https://numpy.org/doc/)
- [Matplotlib Documentation](https://matplotlib.org/stable/contents.html)
- [Tkinter Documentation](https://docs.python.org/3/library/tkinter.html)

## Changelog

### v1.0.0 (2025-11-06)
- Pierwsza wersja aplikacji laboratoryjnej
- Implementacja modeli DC, indukcyjnego i synchronicznego
- Interfejs graficzny z 4 zakładkami
- Wizualizacja charakterystyk w czasie rzeczywistym
- Regulacja parametrów silników
