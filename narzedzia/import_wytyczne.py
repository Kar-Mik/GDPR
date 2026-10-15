#!/usr/bin/env python3
"""Zapisuje noty sygnalizacyjne soft law do zrodla/wytyczne/ (zasady: zrodla/wytyczne/ZRODLA.md).

Każda nota: status i wersja, daty, link do strony i PDF, SHA-256 pobranego PDF, 5–9 tez własnymi
słowami z numerem punktu (EROD/WP260) albo strony PDF (WP248 – bez numeracji punktów).
Numery punktów i brzmienie tez sprawdzone z tekstem PDF w przeglądarce 2026-10-15.

Użycie: python3 narzedzia/import_wytyczne.py
"""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "zrodla", "wytyczne")
DATA_POBRANIA = "2026-10-15"

DOKUMENTY = [
    {
        "plik": "edpb/2020-07-wytyczne-07-2020-administrator-podmiot-przetwarzajacy.md",
        "id": "edpb-wytyczne-07-2020",
        "nr": "07/2020",
        "tytul": "Wytyczne 07/2020 dotyczące pojęć administratora i podmiotu przetwarzającego zawartych w RODO",
        "organ": "EROD",
        "data": "2021-07-07",
        "status": "obowiazuje",
        "wersja": "2.0 – przyjęta po konsultacjach 7.07.2021 (wersja 1.0 do konsultacji: 2.09.2020)",
        "artykuly": "[4(7), 4(8), 4(10), 26, 28, 28(10)]",
        "strona": "https://www.edpb.europa.eu/documents/guideline/guidelines-072020-on-the-concepts-of-controller-and-processor-in-the-gdpr_pl",
        "pdf": "https://www.edpb.europa.eu/system/files/documents/2023-10/edpb_guidelines_202007_controllerprocessor_final_pl.pdf",
        "sha": "8cea33c15dd788b3d6b5803332dd7ebe90417776fc699e14fd36ba36fb8b27bb",
        "jezyk": "pl",
        "zastepuje": "opinię WP29 1/2010 (WP169)",
        "tezy": [
            ("pkt 12", "Role administratora i podmiotu przetwarzającego są pojęciami funkcjonalnymi – decyduje rzeczywista rola strony w danym przetwarzaniu, a nie nazwanie jej tak w umowie; podział ról nie podlega uzgodnieniom stron."),
            ("pkt 17–19", "Administratorem jest co do zasady organizacja, a nie osoba fizyczna w jej strukturze (członek zarządu, pracownik); przetwarzanie przez pracowników w ramach działalności organizacji odbywa się pod jej kontrolą."),
            ("pkt 40–41", "Administrator musi określić cele i „istotne sposoby” przetwarzania (jakie dane, jak długo, kto ma dostęp, czyje dane); „sposoby inne niż istotne” (np. wybór sprzętu, oprogramowania, szczegóły zabezpieczeń) może pozostawić podmiotowi przetwarzającemu."),
            ("pkt 45, 56", "Administrator ani współadministrator nie musi mieć faktycznego dostępu do przetwarzanych danych."),
            ("pkt 54–55", "Współadministrowanie: wspólny decydujący wpływ na cele i sposoby – w formie wspólnej decyzji albo decyzji zbieżnych, które się uzupełniają i są niezbędne, by przetwarzanie w ogóle zaszło."),
            ("pkt 57, 68, 71", "Współadministrowanie dotyczy tylko tych operacji, dla których strony wspólnie określają cele i sposoby; korzystanie ze wspólnej infrastruktury lub bazy nie przesądza o współadministrowaniu, gdy każda strona sama określa swoje cele."),
            ("pkt 76–77, 81", "Podmiot przetwarzający: (a) odrębny podmiot (spółka z grupy może nim być, dział tej samej spółki – nie), (b) przetwarza w imieniu administratora i nie dla własnych celów; po przekroczeniu instrukcji i określeniu własnych celów staje się administratorem (art. 28 ust. 10 RODO)."),
            ("pkt 112", "Umowa powierzenia nie powinna jedynie powtarzać art. 28 RODO – ma konkretnie opisać, jak wymagania będą spełnione (np. środki bezpieczeństwa, procedury)."),
            ("pkt 180", "„Zasadnicza treść uzgodnień” współadministratorów (art. 26 ust. 2) powinna obejmować co najmniej informacje z art. 13 i 14 z przypisaniem odpowiedzialności za każdy element oraz punkt kontaktowy, jeśli wyznaczono."),
        ],
    },
    {
        "plik": "edpb/2020-05-wytyczne-05-2020-zgoda.md",
        "id": "edpb-wytyczne-05-2020",
        "nr": "05/2020",
        "tytul": "Wytyczne 05/2020 dotyczące zgody na mocy rozporządzenia 2016/679",
        "organ": "EROD",
        "data": "2020-05-04",
        "status": "obowiazuje",
        "wersja": "1.1 (13.05.2020 – poprawki formatowania); 1.0 przyjęta 4.05.2020",
        "artykuly": "[4(11), 6(1)(a), 7, 7(3), 7(4), 8, 9(2)(a)]",
        "strona": "https://www.edpb.europa.eu/documents/guideline/guidelines-052020-on-consent-under-regulation-2016679_pl",
        "pdf": "https://www.edpb.europa.eu/system/files/documents/files/file1/edpb_guidelines_202005_consent_pl.pdf",
        "sha": "d00676b08167622871c753806bb092d3eb9914b17bab306ed91810b97634ea9e",
        "jezyk": "pl",
        "zastepuje": "wytyczne WP29 w sprawie zgody (WP259 rev.01)",
        "tezy": [
            ("pkt 16, 21–24", "Brak równowagi sił wyklucza zwykle dobrowolność zgody wobec organów publicznych i pracodawców; nie jest to zakaz bezwzględny, ale administrator musi wykazać, że odmowa nie niesie negatywnych skutków."),
            ("pkt 14, 26–27", "Uzależnianie usługi lub umowy od zgody na przetwarzanie wykraczające poza niezbędne minimum (art. 7 ust. 4) przemawia przeciw dobrowolności."),
            ("pkt 39", "„Cookie wall” – uzależnienie dostępu do usługi od zgody na cookies – nie spełnia warunku dobrowolnej zgody."),
            ("pkt 77, 81", "Zgoda wymaga wyraźnego działania potwierdzającego; wcześniej zaznaczone pola, opt-out i zbiorcza akceptacja regulaminu nie są zgodą."),
            ("pkt 86", "Przewijanie strony, przeglądanie lub podobna aktywność w żadnych okolicznościach nie są wyraźnym działaniem potwierdzającym."),
            ("pkt 90", "Zgodę uzyskuje się przed rozpoczęciem przetwarzania."),
            ("pkt 113–114, 116", "Wycofanie zgody musi być tak samo łatwe jak jej udzielenie (np. jedno kliknięcie ↔ jedno kliknięcie); brak łatwego wycofania czyni cały mechanizm zgody niezgodnym z RODO."),
            ("pkt 123", "Nie można „przeskoczyć” ze zgody na inną podstawę (np. uzasadniony interes) z mocą wsteczną, gdy ważność zgody budzi wątpliwości."),
            ("pkt 125, 131, 135", "Dziecko a usługi społeczeństwa informacyjnego (art. 8): domyślny próg 16 lat, państwo może go obniżyć do 13; weryfikacja wieku proporcjonalna do ryzyka, bez nadmiernego przetwarzania. (W u.o.d.o. brak przepisu obniżającego próg – zob. indeksy/klauzule-otwarte.md, art. 8.)"),
        ],
    },
    {
        "plik": "edpb/2020-01-wytyczne-3-2019-urzadzenia-wideo.md",
        "id": "edpb-wytyczne-3-2019",
        "nr": "3/2019",
        "tytul": "Wytyczne 3/2019 w sprawie przetwarzania danych osobowych przez urządzenia wideo",
        "organ": "EROD",
        "data": "2020-01-29",
        "status": "obowiazuje",
        "wersja": "2.1 (26.02.2021 – poprawa istotnego błędu); 2.0 przyjęta po konsultacjach 29.01.2020; 1.0 do konsultacji 10.07.2019",
        "artykuly": "[2(2)(c), 5(1)(c), 5(1)(e), 6(1)(f), 9, 12, 13, 35]",
        "strona": "https://www.edpb.europa.eu/documents/guideline/guidelines-32019-on-processing-of-personal-data-through-video-devices_pl",
        "pdf": "https://www.edpb.europa.eu/system/files/documents/files/file1/edpb_guidelines_201903_video_devices_pl_0.pdf",
        "sha": "b398469016ca1d669a0652c751aadc9de274c34d86d4c45a4ab2924daa2824ab",
        "jezyk": "pl",
        "zastepuje": "",
        "tezy": [
            ("pkt 12–13", "Wyjątek domowy (art. 2 ust. 2 lit. c) interpretuje się wąsko – kamera obejmująca choćby częściowo przestrzeń publiczną nie jest czynnością czysto osobistą (TSUE C-212/13 Ryneš); kamera tylko na własnej posesji może być objęta wyjątkiem – zależnie od okoliczności."),
            ("pkt 20", "Uzasadniony interes musi być realny i bieżący, nie fikcyjny ani spekulatywny – przed uruchomieniem monitoringu powinna istnieć rzeczywista sytuacja zagrożenia (np. wcześniejsze szkody, incydenty)."),
            ("pkt 24–25", "Niezbędność: najpierw rozważ środki łagodniejsze – ogrodzenie, oświetlenie, zamki, ochronę, folie antygraffiti; monitoring tylko jeśli nie są równie skuteczne."),
            ("pkt 27", "Monitoring co do zasady kończy się na granicy nieruchomości; jego rozszerzenie na bezpośrednie otoczenie tylko wyjątkowo, z zamaskowaniem obszarów nieistotnych."),
            ("pkt 36–37, 40", "Ważenie interesów: rozsądne oczekiwania osób – nie oczekuje się monitoringu w toaletach, saunach, gabinetach lekarskich, prywatnym ogrodzie czy mieszkaniu; tabliczka informacyjna nie zmienia obiektywnych oczekiwań."),
            ("pkt 44", "Zgoda jako podstawa systematycznego monitoringu – tylko wyjątkowo: monitoring obejmuje nieznaną liczbę osób, więc trudno wykazać uprzednią zgodę każdej z nich i zaprzestanie przetwarzania po jej wycofaniu."),
            ("pkt 73–74, 86", "Rozpoznawanie twarzy i inne dane biometryczne – art. 9 RODO; nie wolno uzależniać dostępu do usługi od zgody na przetwarzanie biometryczne."),
            ("pkt 111, 113–114", "Informacja warstwowa: pierwsza warstwa (znak ostrzegawczy) przed wejściem w strefę monitoringu, na wysokości wzroku – cel, administrator, prawa, odesłanie do pełnej informacji (druga warstwa)."),
            ("pkt 121", "Okres przechowywania: szkody zwykle widać w 1–2 dni, więc nagrania co do zasady usuwa się – najlepiej automatycznie – po kilku dniach; im dłużej (zwłaszcza ponad 72 godziny), tym silniejsze uzasadnienie potrzebne."),
        ],
    },
    {
        "plik": "edpb/2023-03-wytyczne-9-2022-zglaszanie-naruszen.md",
        "id": "edpb-wytyczne-9-2022",
        "nr": "9/2022",
        "tytul": "Wytyczne 9/2022 dotyczące zgłaszania naruszenia ochrony danych osobowych na podstawie RODO",
        "organ": "EROD",
        "data": "2023-03-28",
        "status": "obowiazuje",
        "wersja": "2.0 – przyjęta po konsultacjach 28.03.2023 (1.0 z 10.10.2022 – aktualizacja WP250 rev.01 do konsultacji ukierunkowanych)",
        "artykuly": "[4(12), 33, 33(1), 33(2), 33(4), 33(5), 34, 34(3)]",
        "strona": "https://www.edpb.europa.eu/documents/guideline/guidelines-92022-on-personal-data-breach-notification-under-gdpr_pl",
        "pdf": "https://www.edpb.europa.eu/system/files/documents/2024-10/edpb_guidelines_202209_personal_data_breach_notification_v2.0_pl_0.pdf",
        "sha": "f385ed3d05947f2f8b129bfd224368d4336171540afdcd2713f5780c3aa86d25",
        "jezyk": "pl",
        "zastepuje": "wytyczne WP29 w sprawie zgłaszania naruszeń (WP250 rev.01)",
        "tezy": [
            ("pkt 17–18", "Naruszenie może dotyczyć poufności, integralności lub dostępności danych (także kilku naraz); utrata dostępności – także czasowa – też jest naruszeniem."),
            ("pkt 22, 121", "Każde naruszenie, także niezgłaszane, dokumentuje się wewnętrznie (art. 33 ust. 5)."),
            ("pkt 31, 34", "Administrator „stwierdza” naruszenie, gdy ma dostateczną pewność, że incydent doprowadził do narażenia danych; krótkie postępowanie wyjaśniające nie biegnie jeszcze w terminie 72 godzin, ale trzeba je rozpocząć niezwłocznie."),
            ("pkt 44–46", "Podmiot przetwarzający zgłasza naruszenie administratorowi bez zbędnej zwłoki – EROD zaleca szybkie zgłoszenie i uzupełnianie informacji etapami; szczegóły powinna określać umowa powierzenia."),
            ("pkt 56–57, 62", "Informacje można przekazywać etapami (art. 33 ust. 4); zgłoszenie po 72 godzinach wymaga wyjaśnienia przyczyn opóźnienia."),
            ("pkt 72–73", "Administrator spoza UE podlegający RODO na mocy art. 3 ust. 2 nie korzysta z mechanizmu kompleksowej współpracy – sam przedstawiciel go nie uruchamia – i zgłasza naruszenie każdemu organowi państwa, w którym mieszkają osoby dotknięte naruszeniem (zmiana wersji 2.0)."),
            ("pkt 75, 82", "Zgłoszenie do organu jest obowiązkowe, chyba że naruszenie mało prawdopodobnie skutkuje ryzykiem dla praw i wolności."),
            ("pkt 88, 97, 99", "Przy wysokim ryzyku – zawiadomienie osób, co do zasady bezpośrednio; wyjątki z art. 34 ust. 3 (np. szyfrowanie, środki eliminujące ryzyko, niewspółmierny wysiłek → komunikat publiczny); organ może zażądać zawiadomienia (art. 34 ust. 4)."),
        ],
    },
    {
        "plik": "edpb/2024-10-wytyczne-1-2024-uzasadniony-interes-projekt.md",
        "id": "edpb-wytyczne-1-2024",
        "nr": "1/2024",
        "tytul": "Guidelines 1/2024 on processing of personal data based on Article 6(1)(f) GDPR (prawnie uzasadniony interes)",
        "organ": "EROD",
        "data": "2024-10-08",
        "status": "projekt",
        "wersja": "1.0 – wersja do konsultacji publicznych (konsultacje 9.10–20.11.2024); wersji ostatecznej na stronie EROD brak (stan 2026-10-15)",
        "artykuly": "[6(1)(f), 21, 13(1)(d)]",
        "strona": "https://www.edpb.europa.eu/public-consultations/guidelines-12024-on-processing-of-personal-data-based-on-article-61f-gdpr_pl",
        "pdf": "https://www.edpb.europa.eu/system/files/2024-10/edpb_guidelines_202401_legitimateinterest_en.pdf",
        "sha": "59692ea43ce9d2463b9947b5f5ee5daf676ee4b27952b3aaed40724e818abd47",
        "jezyk": "en",
        "zastepuje": "",
        "tezy": [
            ("pkt 12–13", "Trzy kumulatywne przesłanki: uzasadniony interes, niezbędność przetwarzania, wynik ważenia interesów; samo wskazanie interesu nie wystarcza."),
            ("pkt 17", "Interes jest „uzasadniony”, gdy jest zgodny z prawem, jasno i precyzyjnie określony oraz realny i obecny (nie spekulatywny)."),
            ("pkt 29", "Niezbędność: czy celu nie da się rozsądnie osiągnąć równie skutecznie środkami mniej ingerującymi w prawa osób."),
            ("pkt 52–53", "Rozsądne oczekiwania osób mają kluczowe znaczenie w ważeniu; samo poinformowanie o przetwarzaniu nie czyni go „oczekiwanym”."),
            ("pkt 71, 73", "Przy art. 6 ust. 1 lit. f osobie przysługuje sprzeciw (art. 21); „ważne prawnie uzasadnione podstawy” do kontynuacji przetwarzania musi wykazać administrator."),
            ("–", "Wersja konsultacyjna: tezy tylko sygnalizacyjnie; przed użyciem sprawdzić, czy EROD przyjęła wersję ostateczną."),
        ],
    },
    {
        "plik": "wp29/2017-10-wp248-ocena-skutkow-dpia.md",
        "id": "wp29-wp248-rev01",
        "nr": "WP248 rev.01",
        "tytul": "Wytyczne dotyczące oceny skutków dla ochrony danych oraz pomagające ustalić, czy przetwarzanie „może powodować wysokie ryzyko” do celów rozporządzenia 2016/679",
        "organ": "Grupa Robocza Art. 29 (przyjęte przez EROD 25.05.2018)",
        "data": "2017-10-04",
        "status": "obowiazuje",
        "wersja": "rev.01 – przyjęte 4.04.2017, ostatnio zmienione 4.10.2017; zatwierdzone przez EROD (lista „Endorsed WP29 Guidelines”)",
        "artykuly": "[25, 35, 35(1), 35(3), 35(7), 35(11), 36]",
        "strona": "https://ec.europa.eu/newsroom/article29/items/611236",
        "pdf": "https://ec.europa.eu/newsroom/just/document.cfm?doc_id=48464 (ZIP z wersjami językowymi – plik „wp248 rev.01_pl.pdf”)",
        "sha": "7ae81abff9d56a9b7eb6aab06c8f0f4bf786652a5260c3a81b7907f36f8f1913",
        "jezyk": "pl",
        "zastepuje": "",
        "tezy": [
            ("s. 8 PDF", "Jedna DPIA może obejmować zbiór podobnych operacji o podobnym wysokim ryzyku (art. 35 ust. 1, motyw 92)."),
            ("s. 10–13 PDF", "Dziewięć kryteriów wysokiego ryzyka: ocena/scoring i profilowanie; zautomatyzowane decyzje o skutkach prawnych; systematyczne monitorowanie; dane szczególne i bardzo osobiste; duża skala; łączenie zbiorów danych; osoby szczególnie wrażliwe (pracownicy, dzieci); innowacyjne technologie; przetwarzanie uniemożliwiające korzystanie z prawa lub usługi."),
            ("s. 13 PDF", "Reguła praktyczna: spełnienie dwóch kryteriów zwykle oznacza obowiązek DPIA; im więcej kryteriów, tym bardziej prawdopodobne wysokie ryzyko."),
            ("s. 14 PDF", "Jeśli administrator mimo spełnienia kryteriów uzna, że DPIA nie jest potrzebna – dokumentuje uzasadnienie i stanowisko IOD."),
            ("s. 15 PDF", "Kiedy DPIA nie jest wymagana – m.in. brak wysokiego ryzyka, wykorzystanie DPIA dla podobnych operacji, podstawa z art. 6 ust. 1 lit. c lub e z oceną dokonaną przy stanowieniu prawa."),
            ("s. 16–17 PDF", "DPIA przeprowadza się przed rozpoczęciem przetwarzania, możliwie wcześnie (privacy by design); to proces ciągły, a nie jednorazowy – przegląd przy zmianie ryzyka lub kontekstu."),
            ("s. 17 PDF", "Odpowiada administrator – z udziałem IOD i podmiotu przetwarzającego."),
            ("rozdz. III.E", "Konsultacja z organem nadzorczym (art. 36) – gdy ryzyko szczątkowe pozostaje wysokie."),
            ("–", "Polska lista operacji wymagających DPIA (art. 35 ust. 4): zrodla/pl/akty-wykonawcze-uodo/mp-2019-666-wykaz-dpia.md."),
        ],
    },
    {
        "plik": "wp29/2018-04-wp260-przejrzystosc.md",
        "id": "wp29-wp260-rev01",
        "nr": "WP260 rev.01",
        "tytul": "Wytyczne w sprawie przejrzystości na podstawie rozporządzenia 2016/679",
        "organ": "Grupa Robocza Art. 29 (przyjęte przez EROD 25.05.2018)",
        "data": "2018-04-11",
        "status": "obowiazuje",
        "wersja": "rev.01 – przyjęte 29.11.2017, ostatnio zmienione 11.04.2018; zatwierdzone przez EROD (lista „Endorsed WP29 Guidelines”)",
        "artykuly": "[5(1)(a), 12, 13, 14, 14(5)]",
        "strona": "https://ec.europa.eu/newsroom/article29/items/622227",
        "pdf": "https://ec.europa.eu/newsroom/article29/redirection/document/54194 (ZIP z wersjami językowymi – plik „wp260rev01_pl.pdf”)",
        "sha": "967946d2880462578a3a7c9170602e6d17342fad5ee74fd928670dfb160e45a3",
        "jezyk": "pl",
        "zastepuje": "",
        "tezy": [
            ("pkt 8", "„Zwięzła, przejrzysta, zrozumiała i łatwo dostępna forma” – informacja ma być skuteczna i zwięzła, wyraźnie oddzielona od innych treści (np. regulaminu)."),
            ("pkt 11", "Łatwa dostępność: osoba nie powinna szukać informacji – ma od razu wiedzieć, gdzie ją znaleźć."),
            ("pkt 13", "Unikać sformułowań typu „może”, „niektóre”, „często”, „możliwe”; jeśli są użyte, administrator musi wykazać, dlaczego nie mógł być precyzyjny."),
            ("pkt 17–18", "Domyślna forma – pisemna, w tym elektroniczna; dopuszczalne inne środki (np. ikony – art. 12 ust. 7)."),
            ("pkt 27", "Czas: art. 13 – „podczas pozyskiwania danych”; art. 14 – w rozsądnym terminie, najpóźniej w ciągu miesiąca (lub przy pierwszej komunikacji / ujawnieniu)."),
            ("pkt 29–30", "Przejrzystość obowiązuje przez cały czas przetwarzania – istotne zmiany informacji trzeba komunikować aktywnie."),
            ("pkt 35–36, 38", "Podejście warstwowe (online i offline): pierwsza warstwa – najważniejsze informacje (cele, tożsamość administratora, prawa, przetwarzanie o największym wpływie), pełna informacja w kolejnej warstwie."),
            ("pkt 64, 66", "Wyjątki z art. 14 ust. 5: „niewspółmiernie duży wysiłek” wymaga udokumentowanego testu równowagi; wyjątek z lit. c – gdy pozyskanie lub ujawnienie jest wyraźnie uregulowane prawem."),
        ],
    },
]


def main():
    for d in DOKUMENTY:
        sciezka = os.path.join(OUT, d["plik"])
        os.makedirs(os.path.dirname(sciezka), exist_ok=True)
        weryf = (f"numery punktów i treść tez porównane z tekstem PDF ({DATA_POBRANIA}); tezy – opis własny"
                 if d["status"] != "projekt" else
                 f"wersja konsultacyjna; numery punktów porównane z PDF EN ({DATA_POBRANIA}); tezy – opis własny")
        L = [
            "---",
            f"id: {d['id']}",
            "typ: wytyczne",
            f'tytul: "{d["tytul"]}"',
            f'sygnatura: {d["nr"]}',
            f'organ: {d["organ"]}',
            f"data: {d['data']}",
            f"status: {d['status']}",
            "podstawa: RODO",
            f"artykuly_rodo: {d['artykuly']}",
            f"zrodlo: {d['strona']}",
            f"jezyk_tekstu: {d['jezyk']}",
            f"sha256_pdf: {d['sha']}",
            f'weryfikacja: "{weryf}"',
            "---",
            "",
            f"# {d['organ'].split(' (')[0]} – {d['nr']}: {d['tytul']}",
            "",
            "| | |",
            "|---|---|",
            f"| Wersja | {d['wersja']} |",
            f"| Status | {'**projekt (konsultacje)** – sygnalizacyjnie' if d['status']=='projekt' else 'wersja ostateczna, obowiązuje (niewiążąca wykładnia)'} |",
        ]
        if d["zastepuje"]:
            L.append(f"| Zastępuje | {d['zastepuje']} |")
        L += [
            f"| Strona dokumentu | {d['strona']} |",
            f"| PDF ({d['jezyk'].upper()}) | {d['pdf']} |",
            "",
            "## Kluczowe tezy (sygnalizacyjnie)",
            "",
            "*Opis własny, z numerem " + ("strony PDF w wersji PL (dokument nie ma numeracji punktów)" if d["nr"].startswith("WP248") else "punktu źródła") + ". Do opinii – czytać pełny tekst.*",
            "",
        ]
        for ref, teza in d["tezy"]:
            L.append(f"- **{ref}** – {teza}" if ref != "–" else f"- {teza}")
        L.append("")
        with open(sciezka, "w", encoding="utf-8") as f:
            f.write("\n".join(L))
    print("Zapisano not:", len(DOKUMENTY))


if __name__ == "__main__":
    main()
