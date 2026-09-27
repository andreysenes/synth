* VOZ-9 — J1–J9 pin map (must match pcb.md)
*
* Node names used everywhere: j1_1 … j1_20, j2_1 … j2_12,
* j3_1 … j3_20, j4_1 … j4_20, j5_1 … j5_16, j6_1 … j6_6,
* j7_1 … j7_12, j8_1 … j8_6, j9_1 … j9_12
*
* J1 OSC 2x10 (19 used)
*  1–2  OSC A A · B          (reostat 500kA — ends of pitch pot)
*  3–4  OSC B A · B
*  5–7  AMOUNT CCW · W · CW
*  8–10 SHAPE CCW · W · CW
* 11–13 CUTOFF CCW · W · CW
* 14–15 chave A COM · ON
* 16–17 chave B COM · ON
* 18–19 DRONE COM · ON
* 20    NC
*
* J2 LFO 2x6
*  1–3  RATE CCW · W · CW
*  4–6  DEPTH CCW · W · CW
*  7–9  TREM ON–OFF–ON: COM · A(220n tremolo) · B(47u flutter); centro = off
* 10–12 MODE COM · PITCH · TIME
*
* J3 DELAY 2x10 (painel visual: TIME · WET · F-BACK · H1 H2 H3 · STACK | VOLUME)
*  1–3  TIME CCW · W · CW
*  4–5  H1 COM · ON
*  6–7  H2 COM · ON
*  8–9  H3 COM · ON
* 10–12 F-BACK CCW · W · CW
* 13–15 WET CCW · W · CW
* 16–17 STACK COM · ON
* 18–20 VOLUME CCW · W · CW
*
* J4 PATCH A — each jack TIP · SW · GND
*  1–3 A, 4–6 B, 7–9 IN, 10–12 FILT, 13–15 FCV, 16–18 VCV
*
* J5 PATCH B
*  1–3 LFO, 4–6 ECV, 7–9 CLK, 10–12 SEND, 13–15 RCV
*
* J6 CTRL
*  1–2 LED A · K, 3–4 P4 TIP · GND, 5–6 1V8 · GATE (ânodo de D2)
*
* J7 IN combo + PRE + OSC IN 2x6: 1 X2, 2 X3, 3 X1, 4 TIP, 5 GND, 6–8 PRE, 9–11 OSC IN CCW · W · CW, 12 NC
* J8 OUT combo: 1 X2, 2 X3, 3 X1, 4 TIP, 5 GND, 6 NC
*
* J9 EQ voz 424 2x6
*  1–3  LOW CCW · W · CW     (shelf 100 Hz ±10 dB)
*  4–6  MID F CCW · W · CW   (250 Hz–5 kHz)
*  7–9  MID G CCW · W · CW   (±12 dB)
* 10–12 HIGH CCW · W · CW    (shelf 10 kHz ±10 dB)
*
* This file is documentation only — no circuit.
