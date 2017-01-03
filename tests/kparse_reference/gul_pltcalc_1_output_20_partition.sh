#!/bin/bash
mkfifo fifo/gul_P1

mkfifo fifo/gul_S1_summary_P1
mkfifo fifo/gul_S1_summarypltcalc_P1
mkfifo fifo/gul_S1_pltcalc_P1

mkfifo fifo/gul_P2

mkfifo fifo/gul_S1_summary_P2
mkfifo fifo/gul_S1_summarypltcalc_P2
mkfifo fifo/gul_S1_pltcalc_P2

mkfifo fifo/gul_P3

mkfifo fifo/gul_S1_summary_P3
mkfifo fifo/gul_S1_summarypltcalc_P3
mkfifo fifo/gul_S1_pltcalc_P3

mkfifo fifo/gul_P4

mkfifo fifo/gul_S1_summary_P4
mkfifo fifo/gul_S1_summarypltcalc_P4
mkfifo fifo/gul_S1_pltcalc_P4

mkfifo fifo/gul_P5

mkfifo fifo/gul_S1_summary_P5
mkfifo fifo/gul_S1_summarypltcalc_P5
mkfifo fifo/gul_S1_pltcalc_P5

mkfifo fifo/gul_P6

mkfifo fifo/gul_S1_summary_P6
mkfifo fifo/gul_S1_summarypltcalc_P6
mkfifo fifo/gul_S1_pltcalc_P6

mkfifo fifo/gul_P7

mkfifo fifo/gul_S1_summary_P7
mkfifo fifo/gul_S1_summarypltcalc_P7
mkfifo fifo/gul_S1_pltcalc_P7

mkfifo fifo/gul_P8

mkfifo fifo/gul_S1_summary_P8
mkfifo fifo/gul_S1_summarypltcalc_P8
mkfifo fifo/gul_S1_pltcalc_P8

mkfifo fifo/gul_P9

mkfifo fifo/gul_S1_summary_P9
mkfifo fifo/gul_S1_summarypltcalc_P9
mkfifo fifo/gul_S1_pltcalc_P9

mkfifo fifo/gul_P10

mkfifo fifo/gul_S1_summary_P10
mkfifo fifo/gul_S1_summarypltcalc_P10
mkfifo fifo/gul_S1_pltcalc_P10

mkfifo fifo/gul_P11

mkfifo fifo/gul_S1_summary_P11
mkfifo fifo/gul_S1_summarypltcalc_P11
mkfifo fifo/gul_S1_pltcalc_P11

mkfifo fifo/gul_P12

mkfifo fifo/gul_S1_summary_P12
mkfifo fifo/gul_S1_summarypltcalc_P12
mkfifo fifo/gul_S1_pltcalc_P12

mkfifo fifo/gul_P13

mkfifo fifo/gul_S1_summary_P13
mkfifo fifo/gul_S1_summarypltcalc_P13
mkfifo fifo/gul_S1_pltcalc_P13

mkfifo fifo/gul_P14

mkfifo fifo/gul_S1_summary_P14
mkfifo fifo/gul_S1_summarypltcalc_P14
mkfifo fifo/gul_S1_pltcalc_P14

mkfifo fifo/gul_P15

mkfifo fifo/gul_S1_summary_P15
mkfifo fifo/gul_S1_summarypltcalc_P15
mkfifo fifo/gul_S1_pltcalc_P15

mkfifo fifo/gul_P16

mkfifo fifo/gul_S1_summary_P16
mkfifo fifo/gul_S1_summarypltcalc_P16
mkfifo fifo/gul_S1_pltcalc_P16

mkfifo fifo/gul_P17

mkfifo fifo/gul_S1_summary_P17
mkfifo fifo/gul_S1_summarypltcalc_P17
mkfifo fifo/gul_S1_pltcalc_P17

mkfifo fifo/gul_P18

mkfifo fifo/gul_S1_summary_P18
mkfifo fifo/gul_S1_summarypltcalc_P18
mkfifo fifo/gul_S1_pltcalc_P18

mkfifo fifo/gul_P19

mkfifo fifo/gul_S1_summary_P19
mkfifo fifo/gul_S1_summarypltcalc_P19
mkfifo fifo/gul_S1_pltcalc_P19

mkfifo fifo/gul_P20

mkfifo fifo/gul_S1_summary_P20
mkfifo fifo/gul_S1_summarypltcalc_P20
mkfifo fifo/gul_S1_pltcalc_P20



# --- Do insured loss kats ---


# --- Do ground up loss kats ---

kat fifo/gul_S1_pltcalc_P1 fifo/gul_S1_pltcalc_P2 fifo/gul_S1_pltcalc_P3 fifo/gul_S1_pltcalc_P4 fifo/gul_S1_pltcalc_P5 fifo/gul_S1_pltcalc_P6 fifo/gul_S1_pltcalc_P7 fifo/gul_S1_pltcalc_P8 fifo/gul_S1_pltcalc_P9 fifo/gul_S1_pltcalc_P10 fifo/gul_S1_pltcalc_P11 fifo/gul_S1_pltcalc_P12 fifo/gul_S1_pltcalc_P13 fifo/gul_S1_pltcalc_P14 fifo/gul_S1_pltcalc_P15 fifo/gul_S1_pltcalc_P16 fifo/gul_S1_pltcalc_P17 fifo/gul_S1_pltcalc_P18 fifo/gul_S1_pltcalc_P19 fifo/gul_S1_pltcalc_P20 > output/gul_S1_pltcalc.csv & pid1=$!

sleep 2

# --- Do insured loss computes ---


# --- Do ground up loss  computes ---

pltcalc < fifo/gul_S1_summarypltcalc_P1 > fifo/gul_S1_pltcalc_P1 &

tee < fifo/gul_S1_summary_P1 fifo/gul_S1_summarypltcalc_P1  > /dev/null & pid2=$!
summarycalc -g -1 fifo/gul_S1_summary_P1  < fifo/gul_P1 &
pltcalc < fifo/gul_S1_summarypltcalc_P2 > fifo/gul_S1_pltcalc_P2 &

tee < fifo/gul_S1_summary_P2 fifo/gul_S1_summarypltcalc_P2  > /dev/null & pid3=$!
summarycalc -g -1 fifo/gul_S1_summary_P2  < fifo/gul_P2 &
pltcalc < fifo/gul_S1_summarypltcalc_P3 > fifo/gul_S1_pltcalc_P3 &

tee < fifo/gul_S1_summary_P3 fifo/gul_S1_summarypltcalc_P3  > /dev/null & pid4=$!
summarycalc -g -1 fifo/gul_S1_summary_P3  < fifo/gul_P3 &
pltcalc < fifo/gul_S1_summarypltcalc_P4 > fifo/gul_S1_pltcalc_P4 &

tee < fifo/gul_S1_summary_P4 fifo/gul_S1_summarypltcalc_P4  > /dev/null & pid5=$!
summarycalc -g -1 fifo/gul_S1_summary_P4  < fifo/gul_P4 &
pltcalc < fifo/gul_S1_summarypltcalc_P5 > fifo/gul_S1_pltcalc_P5 &

tee < fifo/gul_S1_summary_P5 fifo/gul_S1_summarypltcalc_P5  > /dev/null & pid6=$!
summarycalc -g -1 fifo/gul_S1_summary_P5  < fifo/gul_P5 &
pltcalc < fifo/gul_S1_summarypltcalc_P6 > fifo/gul_S1_pltcalc_P6 &

tee < fifo/gul_S1_summary_P6 fifo/gul_S1_summarypltcalc_P6  > /dev/null & pid7=$!
summarycalc -g -1 fifo/gul_S1_summary_P6  < fifo/gul_P6 &
pltcalc < fifo/gul_S1_summarypltcalc_P7 > fifo/gul_S1_pltcalc_P7 &

tee < fifo/gul_S1_summary_P7 fifo/gul_S1_summarypltcalc_P7  > /dev/null & pid8=$!
summarycalc -g -1 fifo/gul_S1_summary_P7  < fifo/gul_P7 &
pltcalc < fifo/gul_S1_summarypltcalc_P8 > fifo/gul_S1_pltcalc_P8 &

tee < fifo/gul_S1_summary_P8 fifo/gul_S1_summarypltcalc_P8  > /dev/null & pid9=$!
summarycalc -g -1 fifo/gul_S1_summary_P8  < fifo/gul_P8 &
pltcalc < fifo/gul_S1_summarypltcalc_P9 > fifo/gul_S1_pltcalc_P9 &

tee < fifo/gul_S1_summary_P9 fifo/gul_S1_summarypltcalc_P9  > /dev/null & pid10=$!
summarycalc -g -1 fifo/gul_S1_summary_P9  < fifo/gul_P9 &
pltcalc < fifo/gul_S1_summarypltcalc_P10 > fifo/gul_S1_pltcalc_P10 &

tee < fifo/gul_S1_summary_P10 fifo/gul_S1_summarypltcalc_P10  > /dev/null & pid11=$!
summarycalc -g -1 fifo/gul_S1_summary_P10  < fifo/gul_P10 &
pltcalc < fifo/gul_S1_summarypltcalc_P11 > fifo/gul_S1_pltcalc_P11 &

tee < fifo/gul_S1_summary_P11 fifo/gul_S1_summarypltcalc_P11  > /dev/null & pid12=$!
summarycalc -g -1 fifo/gul_S1_summary_P11  < fifo/gul_P11 &
pltcalc < fifo/gul_S1_summarypltcalc_P12 > fifo/gul_S1_pltcalc_P12 &

tee < fifo/gul_S1_summary_P12 fifo/gul_S1_summarypltcalc_P12  > /dev/null & pid13=$!
summarycalc -g -1 fifo/gul_S1_summary_P12  < fifo/gul_P12 &
pltcalc < fifo/gul_S1_summarypltcalc_P13 > fifo/gul_S1_pltcalc_P13 &

tee < fifo/gul_S1_summary_P13 fifo/gul_S1_summarypltcalc_P13  > /dev/null & pid14=$!
summarycalc -g -1 fifo/gul_S1_summary_P13  < fifo/gul_P13 &
pltcalc < fifo/gul_S1_summarypltcalc_P14 > fifo/gul_S1_pltcalc_P14 &

tee < fifo/gul_S1_summary_P14 fifo/gul_S1_summarypltcalc_P14  > /dev/null & pid15=$!
summarycalc -g -1 fifo/gul_S1_summary_P14  < fifo/gul_P14 &
pltcalc < fifo/gul_S1_summarypltcalc_P15 > fifo/gul_S1_pltcalc_P15 &

tee < fifo/gul_S1_summary_P15 fifo/gul_S1_summarypltcalc_P15  > /dev/null & pid16=$!
summarycalc -g -1 fifo/gul_S1_summary_P15  < fifo/gul_P15 &
pltcalc < fifo/gul_S1_summarypltcalc_P16 > fifo/gul_S1_pltcalc_P16 &

tee < fifo/gul_S1_summary_P16 fifo/gul_S1_summarypltcalc_P16  > /dev/null & pid17=$!
summarycalc -g -1 fifo/gul_S1_summary_P16  < fifo/gul_P16 &
pltcalc < fifo/gul_S1_summarypltcalc_P17 > fifo/gul_S1_pltcalc_P17 &

tee < fifo/gul_S1_summary_P17 fifo/gul_S1_summarypltcalc_P17  > /dev/null & pid18=$!
summarycalc -g -1 fifo/gul_S1_summary_P17  < fifo/gul_P17 &
pltcalc < fifo/gul_S1_summarypltcalc_P18 > fifo/gul_S1_pltcalc_P18 &

tee < fifo/gul_S1_summary_P18 fifo/gul_S1_summarypltcalc_P18  > /dev/null & pid19=$!
summarycalc -g -1 fifo/gul_S1_summary_P18  < fifo/gul_P18 &
pltcalc < fifo/gul_S1_summarypltcalc_P19 > fifo/gul_S1_pltcalc_P19 &

tee < fifo/gul_S1_summary_P19 fifo/gul_S1_summarypltcalc_P19  > /dev/null & pid20=$!
summarycalc -g -1 fifo/gul_S1_summary_P19  < fifo/gul_P19 &
pltcalc < fifo/gul_S1_summarypltcalc_P20 > fifo/gul_S1_pltcalc_P20 &

tee < fifo/gul_S1_summary_P20 fifo/gul_S1_summarypltcalc_P20  > /dev/null & pid21=$!
summarycalc -g -1 fifo/gul_S1_summary_P20  < fifo/gul_P20 &

eve 1 20 | getmodel | gulcalc -S100 -L100 -r -c - > fifo/gul_P1  &
eve 2 20 | getmodel | gulcalc -S100 -L100 -r -c - > fifo/gul_P2  &
eve 3 20 | getmodel | gulcalc -S100 -L100 -r -c - > fifo/gul_P3  &
eve 4 20 | getmodel | gulcalc -S100 -L100 -r -c - > fifo/gul_P4  &
eve 5 20 | getmodel | gulcalc -S100 -L100 -r -c - > fifo/gul_P5  &
eve 6 20 | getmodel | gulcalc -S100 -L100 -r -c - > fifo/gul_P6  &
eve 7 20 | getmodel | gulcalc -S100 -L100 -r -c - > fifo/gul_P7  &
eve 8 20 | getmodel | gulcalc -S100 -L100 -r -c - > fifo/gul_P8  &
eve 9 20 | getmodel | gulcalc -S100 -L100 -r -c - > fifo/gul_P9  &
eve 10 20 | getmodel | gulcalc -S100 -L100 -r -c - > fifo/gul_P10  &
eve 11 20 | getmodel | gulcalc -S100 -L100 -r -c - > fifo/gul_P11  &
eve 12 20 | getmodel | gulcalc -S100 -L100 -r -c - > fifo/gul_P12  &
eve 13 20 | getmodel | gulcalc -S100 -L100 -r -c - > fifo/gul_P13  &
eve 14 20 | getmodel | gulcalc -S100 -L100 -r -c - > fifo/gul_P14  &
eve 15 20 | getmodel | gulcalc -S100 -L100 -r -c - > fifo/gul_P15  &
eve 16 20 | getmodel | gulcalc -S100 -L100 -r -c - > fifo/gul_P16  &
eve 17 20 | getmodel | gulcalc -S100 -L100 -r -c - > fifo/gul_P17  &
eve 18 20 | getmodel | gulcalc -S100 -L100 -r -c - > fifo/gul_P18  &
eve 19 20 | getmodel | gulcalc -S100 -L100 -r -c - > fifo/gul_P19  &
eve 20 20 | getmodel | gulcalc -S100 -L100 -r -c - > fifo/gul_P20  &

wait $pid1 $pid2 $pid3 $pid4 $pid5 $pid6 $pid7 $pid8 $pid9 $pid10 $pid11 $pid12 $pid13 $pid14 $pid15 $pid16 $pid17 $pid18 $pid19 $pid20 $pid21 


rm fifo/gul_P1

rm fifo/gul_S1_summary_P1
rm fifo/gul_S1_summarypltcalc_P1
rm fifo/gul_S1_pltcalc_P1

rm fifo/gul_P2

rm fifo/gul_S1_summary_P2
rm fifo/gul_S1_summarypltcalc_P2
rm fifo/gul_S1_pltcalc_P2

rm fifo/gul_P3

rm fifo/gul_S1_summary_P3
rm fifo/gul_S1_summarypltcalc_P3
rm fifo/gul_S1_pltcalc_P3

rm fifo/gul_P4

rm fifo/gul_S1_summary_P4
rm fifo/gul_S1_summarypltcalc_P4
rm fifo/gul_S1_pltcalc_P4

rm fifo/gul_P5

rm fifo/gul_S1_summary_P5
rm fifo/gul_S1_summarypltcalc_P5
rm fifo/gul_S1_pltcalc_P5

rm fifo/gul_P6

rm fifo/gul_S1_summary_P6
rm fifo/gul_S1_summarypltcalc_P6
rm fifo/gul_S1_pltcalc_P6

rm fifo/gul_P7

rm fifo/gul_S1_summary_P7
rm fifo/gul_S1_summarypltcalc_P7
rm fifo/gul_S1_pltcalc_P7

rm fifo/gul_P8

rm fifo/gul_S1_summary_P8
rm fifo/gul_S1_summarypltcalc_P8
rm fifo/gul_S1_pltcalc_P8

rm fifo/gul_P9

rm fifo/gul_S1_summary_P9
rm fifo/gul_S1_summarypltcalc_P9
rm fifo/gul_S1_pltcalc_P9

rm fifo/gul_P10

rm fifo/gul_S1_summary_P10
rm fifo/gul_S1_summarypltcalc_P10
rm fifo/gul_S1_pltcalc_P10

rm fifo/gul_P11

rm fifo/gul_S1_summary_P11
rm fifo/gul_S1_summarypltcalc_P11
rm fifo/gul_S1_pltcalc_P11

rm fifo/gul_P12

rm fifo/gul_S1_summary_P12
rm fifo/gul_S1_summarypltcalc_P12
rm fifo/gul_S1_pltcalc_P12

rm fifo/gul_P13

rm fifo/gul_S1_summary_P13
rm fifo/gul_S1_summarypltcalc_P13
rm fifo/gul_S1_pltcalc_P13

rm fifo/gul_P14

rm fifo/gul_S1_summary_P14
rm fifo/gul_S1_summarypltcalc_P14
rm fifo/gul_S1_pltcalc_P14

rm fifo/gul_P15

rm fifo/gul_S1_summary_P15
rm fifo/gul_S1_summarypltcalc_P15
rm fifo/gul_S1_pltcalc_P15

rm fifo/gul_P16

rm fifo/gul_S1_summary_P16
rm fifo/gul_S1_summarypltcalc_P16
rm fifo/gul_S1_pltcalc_P16

rm fifo/gul_P17

rm fifo/gul_S1_summary_P17
rm fifo/gul_S1_summarypltcalc_P17
rm fifo/gul_S1_pltcalc_P17

rm fifo/gul_P18

rm fifo/gul_S1_summary_P18
rm fifo/gul_S1_summarypltcalc_P18
rm fifo/gul_S1_pltcalc_P18

rm fifo/gul_P19

rm fifo/gul_S1_summary_P19
rm fifo/gul_S1_summarypltcalc_P19
rm fifo/gul_S1_pltcalc_P19

rm fifo/gul_P20

rm fifo/gul_S1_summary_P20
rm fifo/gul_S1_summarypltcalc_P20
rm fifo/gul_S1_pltcalc_P20

