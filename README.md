# Dotykowe pianino

![przód urządzenia](https://user-images.githubusercontent.com/55759533/154842083-fec29976-d40c-4050-a156-dd2744a9b58f.png)

![tył urządzenia](https://user-images.githubusercontent.com/55759533/154842186-a3fd6bd8-f2f5-47c6-9c44-6d79fd3a8947.jpg)


## Cel i zakres projektu.

Celem projektu było zbudowanie elektronicznego pianina z dwiema oktawami umożliwiającego grę i naukę nowych utworów. 

![Link do filmu prezentującego działanie urządzenia](https://drive.google.com/file/d/13YwG8BwCzGuzHZQqKEZ0cRvVdIGhbyhH/view)

## Sprzęt
Wykorzystana platforma sprzętowa, czujniki pomiarowe, elementy wykonawcze:
- Raspberry Pi Zero
- Adafruit MPR121 (czujnik dotyku)
- Diody LED
- Przyciski
- Wyświetlacz LED
- Buzzer
- Multipleksery
- Sklejka drewniana
- Taśma miedziana

## Schematy

Piosenki do nauki są przechowywane w bazie danych.

![schemat bazy danych](https://user-images.githubusercontent.com/55759533/154841812-6edbc9ba-a3a3-4822-bf3f-19a4c33178eb.png)
    
![schemat urządzenia](https://user-images.githubusercontent.com/55759533/154841841-352cdee4-c63e-4dee-8cbc-02e78dd2b0fa.png)


## Program

Kod został podzielony na część dotyczącą obsługi menu, część zawierającą różne opcje grania utworów, część z funkcjami obsługującą klawisze oraz przyciski, a także część obsługującą pojedyncze elementy układu. 

Zmiany wywołane 
przez przyciśnięcie przycisków (góra/dół/ok) są wykrywane przez wywołanie funkcji asynchronicznych. Za każdym razem, gdy któryś z nich jest przyciskany, wywołana zostaje funkcja `refresh_menu()`. W funkcji `refresh_main_menu()` można zmieniać opcje pomiędzy „Graj sam”, „Odtwórz utwór”, „Naucz się grać” oraz „Wyjście”. Natomiast w funkcji `refresh_songs_menu()` następuje pobranie utworów z bazy utworów oraz wyświetlanie dwóch kolejnych na wyświetlaczu, z których kliknięciem przycisku „OK”, można wybrać jedną.

Funkcje `free_play()` oraz  `learn_song()` wywołują z odpowiednimi argumentami inną funkcję sprawdzającą przyciśnięte klawisze oraz zapalającą diody. Opcja `play_song()` najpierw pobiera odpowiednią piosenkę z bazy danych, a następnie gra odpowiadające jej dźwięki.


W funkcji `check_keys()` działa pętla główna, gdzie odczytywane są A oraz B, które sprawdzają, które wejście (00/01/10/11) z „czwórek” iksów lub igreków multipleksera było aktywne poziomem wysokim. Z kolei moduł dotykowy Adafruit jest przyłączony do X oraz Y multiplekserów i w ten sposób jest odczytywany numer multipleksera oraz czy zostało wybrane X czy Y. W ten sposób odczytuje się informację o naciśniętym klawiszu.

W przypadku wybrania opcji freeplay, wystarczy zagrać odpowiadający kombinacji  dźwięk. Przykładowo, kombinacja „BY11” odczytana w powyższej funkcji, odpowiada dźwiękowi „D1”.

Gdy zostanie wybrana opcja learnsong, to następuje iteracja przez wszystkie dźwięki piosenki oraz zapalanie diody przed zagraniem dźwięku przez grającego. Dioda gaśnie po naciśnięciu klawisza odpowiadającemu zapalonej diodzie.

## Podsumowanie i wnioski

Najtrudniejszym i najbardziej czasochłonnym elementem całego projektu (ze względu na brak odpowiednich narzędzi i doświadczenia) było wykonanie drewnianej bazy. Brak statywu do wiertarki spowodował, że trudno było utrzymać równe położenie otworów, nie mówiąc o wycinaniu i fazowaniu otworów pod wyświetlacz i przyciski. 
Rozplanowanie elementów na gotowej desce zdecydowanie ułatwiło nam pracę i sprawiło, że tył pianina wygląda estetycznie, mimo dużej ilości połączeń. 
Od strony programowej najbardziej skomplikowana wydaje się być funkcja sprawdzająca naciśnięcie klawisza. Zastosowanie multiplekserów pozwoliło na zmniejszenie ilości połączeń i użycie ograniczonej ilości wejść płytki Adafruit. Umieszczenie w układzie dwóch takich modułów umożliwiłoby jednak sprawdzanie wszystkich wejść synchronicznie, co w tej chwili zastępujemy szybkim przełączaniem kontekstu. Nierozwiązana pozostaje jeszcze kwestia grania akordów. 
Wybór Raspberry Pi Zero był dobrym pomysłem, ponieważ ma ono wbudowany moduł bluetooth. Dzięki temu oprócz buzzera dodamy możliwość podłączenia głośnika bluetooth, by otrzymać lepszy dźwięk. Mając zwykłe Raspberry prawdopodobnie użyłybyśmy złącza mini jack, jednakże ten komputer pozwolił nam nieco zredukować koszty.

© Katarzyna Badio, Anna Panfil 2021
