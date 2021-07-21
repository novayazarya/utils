В `act.csv` находится часть записей из базы AACT, которая использовалась в предыдущей неделе. Попробуем поработать с ней только из `bash`.

```console
head -n 1 aact.csv
,nct_id,study_type,acronym,baseline_population,brief_title,official_title,overall_status
```

Посмотрим, какие вообще есть `study_type`

- Отрезаем заголовок
- Разбиваем по запятой
- Сортируем и считаем уникальные

```console
cat aact.csv | tail -n +2 | cut -d"," -f3 | sort | uniq
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

```console
cat aact.csv | wc -l
1001
```
`wc` - word count, с параметром `l` считаем строки

```console
cat aact.csv | tail -n +2 | sed -e "/N\/A/"d | wc -l
996
```
`sed` - позволяет редактировать файл, не открывая его (e просто идет перед командами, а `d` удаляет регулярные выражения выбранные)

```console
cat aact.csv | tail -n +2 | sed -e "/N\/A/"d | cut -d"," -f3 | sort | uniq
Expanded Access
Interventional
Observational
Observational [Patient Registry]
```
Сохраним этот результат в промежуточных файл

```console
cat aact.csv | tail -n +2 | sed -e "/N\/A/"d > aact-fillna.csv
```

Предположим, что мы хотим составить набор данных для алгоритма машинного обучения, который бы предсказывал тип исследования по его описанию.

Для этого нам необходимо оставить только текст и значение `study_type`, перемешать все данные и разделить их на два набора данных - один `train` для обучения, другой `test` для проверки корректности работы в соотношении 70\30.

```console
cat aact-fillna.csv | wc -l
996
```

```console
export TRAIN_SIZE=$(( $(cat aact-fillna.csv | wc -l) * 70 / 100 ))
```
```console
echo $TRAIN_SIZE
697
```

```console
cat aact-fillna.csv | cut -d"," -f3,6,7 | shuf > shuffled-aact.csv
cat shuffled-aact.csv | head -n $TRAIN_SIZE > train-aact.csv
cat shuffled-aact.csv | tail -n +$(($TRAIN_SIZE+1)) > test-aact.csv
```

`shuf` - позволяет делать случайные перестановки




