# Changelog

Формат: [Keep a Changelog](https://keepachangelog.com/ru/1.1.0/), версии по [SemVer](https://semver.org/lang/ru/).

## [Unreleased]

### Added
- Каркас пакета: реестр `@algo`, `show` / `search` / `list_algos` / `help`, CLI `rustinpy list|show|search|export`.
- `rustinpy.io`, `rustinpy.interactive`, `rustinpy.mathx`, `rustinpy.ds` (140 алгоритмов).
- `rustinpy.graph` (64) и `rustinpy.tree` (20): обходы, кратчайшие пути, DAG, DSU/MST, SCC/2-SAT, мосты, Эйлер, функциональные графы, потоки, паросочетания, LCA, HLD, центроиды, изоморфизм.
- `rustinpy.dp` (30), `rustinpy.strings` (29), `rustinpy.roman` (7), `rustinpy.bits` (22): рюкзаки, LIS/LCS, DP по маскам и профилю, digit DP, CHT/Li Chao, D&C/Knuth; Z/KMP, хеши, Ахо-Корасик, суффиксный массив и автомат, Манакер, BWT; римские числа; xor-базис, SOS DP, FWHT.
- `rustinpy.geometry` (26), `rustinpy.game` (9), `rustinpy.introductory` (28), `rustinpy.sorting` (37): точная геометрия на целых, оболочка, ближайшая пара, сканирование; Ним и Шпраг-Гранди; вводные задачи и конструктивы (Прюфер, де Брёйн); бинпоиск по ответу, расписания, Иосиф, скользящая медиана.
- `rustinpy.counting` (28): задачи CSES на подсчёт и конструктивы: слоны, перестановки, Raab Game, распределения функциональных графов и турниров, Maximum Building I/II, Cyclic Array, Coding Company, Two Stacks Sorting, Coin Grid (Кёниг), Grid Puzzle I/II.
- `rustinpy.misc` (10): короткие задачи ICPC-UZ; задачи 2025 года реализованы по официальному разбору жюри (NOT VERIFIED).
- `scripts/gen_catalog.py` → `docs/CATALOG.md`, `scripts/export_trd.py`, README на русском и английском, `docs/PUBLISHING.md`.
- Бенчмарки `pytest -m slow`; CI на Python 3.9–3.13 и Windows; публикация через Trusted Publishing.
