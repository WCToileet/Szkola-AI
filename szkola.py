# szkola.py
# Mini-quiz Pythona - naturalny styl, interaktywny
# Autor: WCToileet

import random
import os
import time
from datetime import datetime

WYNIKI_PLIK = "wyniki.txt"
BEST_PLIK = "best_score.txt"

# ===== Funkcje podstawowe =====
def powitanie():
    print("🎓 Witaj w mojej mini szkole Python!")
    imie = input("Jak masz na imię? ").strip()
    if not imie:
        imie = "Uczestnik"
    print(f"Cześć {imie}! Zobaczmy, jak dobrze znasz Pythona.\n")
    return imie

def pobierz_pytania():
    return [
        {"p": "Jakiego typu jest liczba 5?", "a": "int"},
        {"p": "Jakiego typu jest tekst 'Hello'?", "a": "str"},
        {"p": "Jakiego typu jest liczba 3.14?", "a": "float"},
        {"p": "Jakiego słowa używamy, żeby zdefiniować funkcję?", "a": "def"},
        {"p": "Jakiego słowa używamy, żeby zwrócić wartość z funkcji?", "a": "return"},
        {"p": "Jaki operator sprawdza równość?", "a": "=="},
        {"p": "Co robi 'print' w Pythonie?", "a": "wypisuje"},
        {"p": "Jakiego słowa używamy do warunku?", "a": "if"},
        {"p": "Jakiego słowa używamy do pętli iterującej przez listę?", "a": "for"},
        {"p": "Jakiego słowa używamy do pętli warunkowej?", "a": "while"},
        {"p": "Jakiego znaku używamy do komentarza?", "a": "#"},
        {"p": "Jak przerwać pętlę przed końcem?", "a": "break"},
        {"p": "Jak pominąć jedną iterację w pętli?", "a": "continue"},
        {"p": "Co robi 'len()'?", "a": "liczy"},
        {"p": "Jak importujemy bibliotekę?", "a": "import"},
        {"p": "Jak złapać wyjątek (słowo kluczowe)?", "a": "try"},
        {"p": "Jak obsłużyć wyjątek po 'try'?", "a": "except"},
        {"p": "Jak stworzyć listę?", "a": "list"},
        {"p": "Jak stworzyć słownik?", "a": "dict"},
        {"p": "Jaki operator łączy stringi?", "a": "+"}
    ]

def wybierz_trudnosc():
    print("Wybierz poziom trudności:")
    print("1 - łatwy (3 pytania, częstsze podpowiedzi)")
    print("2 - normalny (5 pytań)")
    print("3 - trudny (7 pytań, rzadkie podpowiedzi)")
    wybor = input("Podaj 1, 2 lub 3 (domyślnie 2): ").strip()
    if wybor == "1":
        return {"ile": 3, "hint_chance": 0.8}
    elif wybor == "3":
        return {"ile": 7, "hint_chance": 0.3}
    else:
        return {"ile": 5, "hint_chance": 0.5}

# ===== Obsługa wyników =====
def zapisz_wynik(imie, punkty, ile, czas_s):
    czas = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    linia = f"{czas} | {imie} | {punkty}/{ile} | czas: {czas_s:.1f}s\n"
    with open(WYNIKI_PLIK, "a", encoding="utf-8") as f:
        f.write(linia)

def wczytaj_best():
    if not os.path.exists(BEST_PLIK):
        return {"best": 0, "streak": 0}
    try:
        with open(BEST_PLIK, "r", encoding="utf-8") as f:
            line = f.readline().strip()
            best, streak = line.split(",")
            return {"best": int(best), "streak": int(streak)}
    except Exception:
        return {"best": 0, "streak": 0}

def zapisz_best(best, streak):
    with open(BEST_PLIK, "w", encoding="utf-8") as f:
        f.write(f"{best},{streak}")

# ===== Funkcje quizu =====
def losowa_kaczka():
    if random.random() < 0.15:
        return " 🦆"
    return ""

def losowy_komentarz():
    komentarze = ["Świetna robota!", "Jeszcze lepiej następnym razem!", "Super!", "Brawo!", "Keep it up!"]
    return random.choice(komentarze)

def quiz(imie, ile, hint_chance):
    pytania = pobierz_pytania()
    losowe = random.sample(pytania, k=ile)
    punkty = 0
    bledne = []
    podpowiedzi = [
        "Spróbuj pomyśleć o typach danych.",
        "Zwróć uwagę na składnię.",
        "Przypomnij sobie słowa kluczowe.",
        "Myśl o tym, co robi funkcja lub operator."
    ]
    czasy = []

    for i, q in enumerate(losowe, start=1):
        print(f"Pytanie {i}: {q['p']}")
        start = time.time()
        odp = input("Twoja odpowiedź: ").strip().lower()
        koniec = time.time()
        czas_odp = koniec - start
        czasy.append(czas_odp)

        poprawna = q['a'].lower()
        odp_norm = odp.replace(" ", "")
        poprawna_norm = poprawna.replace(" ", "")

        if odp_norm == poprawna_norm:
            print(f"✅ Dobra odpowiedź!{losowa_kaczka()} {losowy_komentarz()}\n")
            punkty += 1
        else:
            print(f"❌ Nie tym razem. Poprawna odpowiedź: {q['a']}")
            if random.random() < hint_chance:
                print(f"💡 Podpowiedź: {random.choice(podpowiedzi)}")
            print()
            bledne.append(q)

        # Bonusowe pytanie
        if random.random() < 0.1:
            print("🎁 Bonusowe pytanie!")
            print("Co robi funkcja input() w Pythonie?")
            odp_bonus = input("Odpowiedź: ").strip().lower()
            if odp_bonus in ["pobiera dane od użytkownika", "pobiera dane"]:
                print("✅ Super! Dodatkowy punkt! 🎉\n")
                punkty += 1
            else:
                print("❌ Nie tym razem.\n")

    sredni_czas = sum(czasy) / len(czasy)
    return punkty, ile, bledne, sredni_czas

def poziom_gracza(punkty, ile):
    ratio = punkty / ile
    if ratio == 1:
        return "Mistrz Pythona"
    elif ratio >= 0.6:
        return "Średniozaawansowany"
    else:
        return "Początkujący"

def podsumowanie(imie, punkty, ile, bledne, sredni_czas, best_info):
    print(f"\n{imie}, ukończyłeś quiz — wynik: {punkty}/{ile} punktów")
    print(f"Średni czas odpowiedzi: {sredni_czas:.1f} s")
    print(f"Twój poziom: {poziom_gracza(punkty, ile)}")

    if bledne:
        print("\n💡 Powtórka — zwróć uwagę na:")
        for q in bledne:
            print(f"- {q['p']} → {q['a']}")

    best = best_info["best"]
    streak = best_info["streak"]

    if punkty > best:
        best = punkty
        streak = 1
        print("\n🔥 Nowy rekord! Gratulacje! Rekord został zapisany.")
    elif punkty == best and best != 0:
        streak += 1
        print(f"\n⭐ Równo z rekordem! Streak: {streak}")
    else:
        streak = 0

    print(f"\nNajlepszy wynik: {best} punktów. Obecny streak: {streak}")

    zapisz_best(best, streak)
    zapisz_wynik(imie, punkty, ile, sredni_czas)

# ===== Main =====
def main():
    imie = powitanie()
    ustaw = wybierz_trudnosc()
    ile = ustaw["ile"]
    hint_chance = ustaw["hint_chance"]

    best_info = wczytaj_best()
    punkty, ile, bledne, sredni_czas = quiz(imie, ile, hint_chance)
    podsumowanie(imie, punkty, ile, bledne, sredni_czas, best_info)

if __name__ == "__main__":
    main()
