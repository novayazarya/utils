# Bash для DA/DS
## AACT
В `act.csv` находится часть записей из базы AACT, которая использовалась в предыдущей неделе. Попробуем поработать с ней только из `bash`.

```bash
head -n 1 aact.csv
```
```shell
nct_id,study_type,acronym,baseline_population,brief_title,official_title,overall_status
```

Посмотрим, какие вообще есть `study_type`

- Отрезаем заголовок
- Разбиваем по запятой
- Сортируем и считаем уникальные

```bash
cat aact.csv | tail -n +2 | cut -d"," -f3 | sort | uniq
```
```shell
Expanded Access
Interventional
N/A
Observational
Observational [Patient Registry]
```

- `cat` - просто читает файл
- `|` - передает выход предыдущей команды как вход на следующую
- `tail` - смотрим последние строки (если бы мы передали `-n 10` -- было бы последние 10 строк, а так мы смотрим до 2й строки)
- `cut` - вырезает элемент -- с помощью d выбираем разделитель, а с помощью `f` -- номер нужного нам столбца
- `sort` - сортировка
- `uniq` - выибираем уникальные

Уберем N\A значения - не хотим их видеть в выборке

```bash
cat aact.csv | wc -l
```
```shell
1001
```
`wc` - word count, с параметром `l` считаем строки

```bash
cat aact.csv | tail -n +2 | sed -e "/N\/A/"d | wc -l
```
```shell
996
```
`sed` - позволяет редактировать файл, не открывая его (e просто идет перед командами, а `d` удаляет регулярные выражения выбранные)

```bash
cat aact.csv | tail -n +2 | sed -e "/N\/A/"d | cut -d"," -f3 | sort | uniq
```
```shell
Expanded Access
Interventional
Observational
Observational [Patient Registry]
```
Сохраним этот результат в промежуточных файл

```bash
cat aact.csv | tail -n +2 | sed -e "/N\/A/"d > aact-fillna.csv
```

Предположим, что мы хотим составить набор данных для алгоритма машинного обучения, который бы предсказывал тип исследования по его описанию.

Для этого нам необходимо оставить только текст и значение `study_type`, перемешать все данные и разделить их на два набора данных - один `train` для обучения, другой `test` для проверки корректности работы в соотношении 70\30.

```bash
cat aact-fillna.csv | wc -l
```
```shell
996
```

```bash
export TRAIN_SIZE=$(( $(cat aact-fillna.csv | wc -l) * 70 / 100 ))
echo $TRAIN_SIZE
```
```shell
697
```

```bash
cat aact-fillna.csv | cut -d"," -f3,6,7 | shuf > shuffled-aact.csv
cat shuffled-aact.csv | head -n $TRAIN_SIZE > train-aact.csv
cat shuffled-aact.csv | tail -n +$(($TRAIN_SIZE+1)) > test-aact.csv
```

`shuf` - позволяет делать случайные перестановки

```bash
cat train-aact.csv | wc -l
```
```shell
697
```
```bash
cat test-aact.csv | wc -l
```
```shell
299
```
```bash
cat aact.csv | sort -t ',' -k2 | head -n 1
```
```shell
628,NCT00004323,Interventional,,,Phase II Study of Bone Marrow Transplantation Using Related Donors in Patients With Aplastic Anemia,,Completed
```

Команда `sort` также имеет возможность сортировать поток не по целой строке, а по определенной ее части. Ключ `-t` указывает разделитель строки , а ключ `-k` указывает номер секции (колонки) по которой необходимо сортировать.

## COVID

Поэкспериментируем теперь с базой covid

```bash
head covid.json
```
```shell
{
    "measures": [
        {
            "uid": 4,
            "country_iso2": "AF",
            "country_iso3": "AFG",
            "country_code": 4,
            "country": "Afghanistan",
            "combined_name": "Afghanistan",
            "population": 38928341,
```
```bash
cat covid.json | jq '.measures[0] | keys'
```
```shell
[
  "combined_name",
  "confirmed",
  "country",
  "country_code",
  "country_iso2",
  "country_iso3",
  "deaths",
  "loc",
  "population",
  "recovered",
  "uid"
]
```

`jq` - позволяет работать с json

```bash
cat covid.json | jq '.measures[].confirmed' | head
```
```shell
0
0
0
0
0
0
0
0
0
0
```
```bash
cat covid.json | jq '.measures[].confirmed' | awk '{sum += $1} END {print sum}'
```
```shell
2339039
```
`awk` - позволяет выполнять над файлом построчные операции

Может точно также подсчитать среднее

```bash
cat covid.json | jq '.measures[].confirmed' | awk '{sum += $1; count += 1} END { print sum / count }'
```
```shell
2339.04
```
С медианой придется идти немного другим путем

```bash
export MEDIAN_INDEX=$(( $(cat covid.json | jq '.measures[].confirmed' | wc -l) / 2 ))
echo $MEDIAN_INDEX
```
```shell
500
```
```bash
cat covid.json | jq '.measures[].confirmed' | sort -n | sed -n -e "$MEDIAN_INDEX"p
```
```shell
61
```

## Word count

Давайте попробуем подсчитать количество раз, которое встречается каждое слово в документе. В качестве самого документа со словами будем использовать заголовки из aact

Получаем только тексты

```bash
cat aact.csv | tail -n +2 | cut -d"," -f6,7 | head
```
Заменяем все пробелы на перенос строк
```bash
cat aact.csv | tail -n +2 | cut -d"," -f6,7 | sed -e "s/\s\+/\\n/g"  | head
```
```shell
A
New
Psychotherapy
Intervention
for
Older
Cancer
Patients,Cancer
and
Aging
```
```bash
cat aact.csv | tail -n +2 | cut -d"," -f6,7 | sed -e "s/\s\+/\\n/g" | sort | uniq -c
```
```shell
      1 AspivixTM"
      1 ASPS,"A
      1 ASS
      1 Assay
      1 Assay,"A
      1 Assertive
     21 Assess
     11 Assessing
     26 Assessment
      2 Assist
      2 Assistance
      3 Assisted
      2 Assisting
      1 Assiut
```
Выходные данные были обрезаны

Теперь хотим узнать топ 20 самых популярных слов в тексте

```bash
cat aact.csv | tail -n +2 | cut -d"," -f6,7 | sed -e "s/\s\+/\\n/g" | sort | uniq -c > word-count.txt
```
`-k1` - первое поле, `n` - сравниваем как числа, `r` - в обратном порядке

```bash
cat word-count.txt | sort -t ' ' -k1nr | head -n 20
```
```shell
   1457 of
    978 in
    710 and
    543 the
    534 With
    349 for
    334 Study
    324 Patients
    278 to
    249 on
    207 a
    178 A
    153 Treatment
    132 COVID-19
    130 Trial
    103 Randomized
     97 After
     90 During
     89 Clinical
     84 Phase
```

В файле measures.json содержатся наблюдения о новых заболевших коронавирусом. Каждая запись соответствует одному дню наблюдения. Для каждой записи в поле `country` указана страна, где производились измерения. В поле `data` указаны сами измерения в формате csv. В каждой строке этой таблицы csv лежат два числа - заболевшие женщины и заболевшие мужчины. Каждая строка относится к своему региону в стране, где производились измерения.

Необходимо выяснить, в какой стране было наибольшее количество дней измерений. Для этой страны необходимо подсчитать суммарное количество заболевших во все дни наблюдений. Это число (итоговое количество заболевших) - ответ на задачу

Подсказка: для того, чтобы восстановить привычный вид csv таблицы, воспользуйтесь `sed`, чтобы подправить переносы строк и кавычки. Можно использовать любые средства, описанные в стандартной документации инструментов, которые мы разбирали.

---
Посмотрим на список стран в каждом дне измерений и посчитаем уникальное вхождение каждой страны

```bash
cat measures.json | jq '.measures[].country' | sort | uniq -c
```
```shell
     74 "Canada"
     95 "Russia"
     81 "USA"
```
Значит Россия на 1 месте по количеству измерений

Заменим ковычки, запятые и символ переноса строки на '\n' и посчитаем сумму всех чисел
```bash
 cat measures.json | jq '.measures[] | select(.country == "Russia") | .data' | sed -e 's/\\n/\n/g; s/,/\n/g; s/\"/\n/g' | jq -s 'add'
```
```shell
174497
```
