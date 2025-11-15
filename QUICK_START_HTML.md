# 🚀 Szybki Start - Wersja HTML

## Jak uruchomić symulator w 3 krokach:

### Krok 1️⃣: Znajdź plik
```
synchronous_generator_simulator.html
```

### Krok 2️⃣: Kliknij dwukrotnie
- **Windows**: Dwukrotne kliknięcie otworzy w domyślnej przeglądarce
- **Mac**: Dwukrotne kliknięcie lub przeciągnij na ikonę Chrome/Safari
- **Linux**: Dwukrotne kliknięcie lub:
  ```bash
  xdg-open synchronous_generator_simulator.html
  ```

### Krok 3️⃣: Gotowe! 🎉

## 🎮 Podstawowa obsługa:

### Pierwsze użycie:
1. **Kliknij "🔢 Oblicz Wszystko"** - zobaczysz wszystkie wyniki
2. **Przesuń suwaki** - wyniki aktualizują się automatycznie
3. **Kliknij "▶️ Symuluj"** - uruchom symulację dynamiczną
4. **Kliknij "🎬 Animacja"** - zobacz animację w czasie rzeczywistym

### Parametry do zabawy:
- **Kąt mocy δ** - zmień i zobacz jak wpływa na moc
- **SEM E** - zwiększ/zmniejsz napięcie wzbudzenia
- **Moc mechaniczna Pm** - dla symulacji dynamicznej

## 📊 Co zobaczysz:

### Panel wyników
Szczegółowe obliczenia dla wszystkich części zadania (a-d)

### Wykresy
1. **Moc-Kąt**: Krzywa Pe(δ) z punktami roboczymi
2. **Fazory**: Diagram wektorowy V, E, Ia
3. **Delta(t)**: Zmiana kąta mocy w czasie
4. **Omega(t)**: Odchylenie prędkości

## 💡 Wskazówki:

### ✅ Sprawdź domyślne wyniki:
- Prąd: **3.435 kA**
- Moc: **74.29 MW**
- Współczynnik mocy: **0.832**

### ✅ Eksperymentuj:
- Zmniejsz Xs → większa moc
- Zwiększ E → większa moc
- Zmień δ → różne punkty pracy

### ✅ Symulacja:
- **RK45** - dokładniejszy, wolniejszy
- **Euler** - szybszy, mniej dokładny

## 🔧 Rozwiązywanie problemów:

### Wykres nie wyświetla się?
- Sprawdź połączenie internetowe (Plotly.js ładuje się z CDN)
- Odśwież stronę (F5)

### Animacja nie działa?
- Najpierw kliknij "▶️ Symuluj"
- Potem "🎬 Animacja"

### Chcę wrócić do domyślnych wartości?
- Kliknij "🔄 Reset"

## 📱 Na telefonie/tablecie:

Aplikacja działa również na urządzeniach mobilnych!
- Wykresy są dotykowe (zoom, przesuwanie)
- Suwaki reagują na dotyk
- Layout dostosowuje się do ekranu

## 🌐 Udostępnianie:

### Chcesz pokazać komuś?
1. **Wyślij plik HTML** - jedna wiadomość email
2. **Umieść na Dropbox/Google Drive** - udostępnij link
3. **Wrzuć na GitHub Pages** - darmowy hosting

### Bez instalacji!
Odbiorcy nie muszą nic instalować - tylko otworzyć w przeglądarce!

## 🎓 Dla nauczycieli:

### Idealne do:
- Wykładów (demonstracje na żywo)
- Laboratoriów (studenci pracują lokalnie)
- Zadań domowych (łatwo udostępnić)
- Egzaminów (symulacje różnych przypadków)

### Zalety:
- Brak konfiguracji laboratorium
- Działa na każdym komputerze
- Studenci mogą pracować w domu
- Interaktywna nauka

## 🚀 Zaawansowane użycie:

### Modyfikacja kodu:
1. Otwórz plik w edytorze tekstu (Notepad++, VSCode)
2. Znajdź sekcję `<script>`
3. Zmień parametry/kolory/zachowanie
4. Zapisz i odśwież przeglądarkę

### Przykłady modyfikacji:
```javascript
// Zmień domyślną wartość Xs:
const Xs = 1.60; → const Xs = 2.0;

// Zmień kolor wykresu:
line: { color: 'blue' } → line: { color: 'red' }

// Zmień maksymalny czas symulacji:
max="20" → max="30"
```

## ⚡ Porównanie z wersją Python:

| Funkcja | HTML | Python |
|---------|------|--------|
| Wyniki obliczeń | ✅ Identyczne | ✅ Identyczne |
| Dokładność | ✅ Taka sama | ✅ Taka sama |
| Instalacja | ❌ Nie | ✅ Wymagana |
| Szybkość | ⚡ Natychmiastowa | ⏱️ 2-3 sekundy |
| Interfejs | 🎨 Nowoczesny | 📊 Tkinter |

## 🎯 Typowe scenariusze:

### Scenariusz 1: Analiza punktu pracy
1. Ustaw parametry generatora
2. Kliknij "Oblicz Wszystko"
3. Przeczytaj wyniki w panelu
4. Zobacz pozycję na wykresie Moc-Kąt

### Scenariusz 2: Wpływ wzbudzenia
1. Zanotuj początkową moc
2. Zwiększ E suwakiem
3. Obserwuj jak rośnie moc
4. Zobacz zmianę na diagramie fazorowym

### Scenariusz 3: Stabilność dynamiczna
1. Ustaw Pm bliżej mocy generowanej
2. Kliknij "Symuluj"
3. Zobacz oscylacje kąta δ
4. Zwiększ tłumienie D i symuluj ponownie

### Scenariusz 4: Porównanie solverów
1. Wybierz RK45, kliknij "Symuluj"
2. Zanotuj wynik
3. Wybierz Euler, kliknij "Symuluj"
4. Porównaj różnice

## 📖 Dalsze informacje:

- **README_HTML.md** - Pełna dokumentacja
- **Kod źródłowy** - Dobrze skomentowany w pliku HTML

## ✨ Miłej zabawy!

Aplikacja jest gotowa do użycia. Nie potrzebujesz nic instalować - po prostu otwórz i eksploruj!

---

**Potrzebujesz pomocy?**
- Sprawdź README_HTML.md
- Zobacz komentarze w kodzie
- Eksperymentuj z parametrami

**To wszystko! Powodzenia! 🎓⚡**
