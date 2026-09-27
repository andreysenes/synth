* VOZ-9 sim library — include once from each .cir
* Paths relative to voz-9/sim/ (run ngspice from that directory)

.include models/jfet.mod
.include models/diodes.mod
.include models/npn.mod
.include models/opamps.mod
.include models/rails.mod

.subckt wire IN OUT
Rw IN OUT 0.1
.ends wire

* --- Potentiometers (u in [0,1], CCW–W–CW) ---
* ngspice requires params: on .subckt for instance overrides

.subckt pot_lin CCW W CW params: Rtot=100k u=0.5
.param uu={min(max(u, 1e-6), 1-1e-6)}
Rlo CCW W {Rtot * uu}
Rhi W   CW {Rtot * (1 - uu)}
.ends pot_lin

.subckt pot_log CCW W CW params: Rtot=100k u=0.5
.param uu={min(max(u, 1e-6), 1-1e-6)}
.param ueff={(pow(10, uu) - 1) / 9}
Rlo CCW W {Rtot * ueff}
Rhi W   CW {Rtot * (1 - ueff)}
.ends pot_log

.subckt pot_antilog CCW W CW params: Rtot=100k u=0.5
.param uu={min(max(u, 1e-6), 1-1e-6)}
.param ueff={log(1 + 9 * uu) / log(10)}
Rlo CCW W {Rtot * ueff}
Rhi W   CW {Rtot * (1 - ueff)}
.ends pot_antilog

* --- Voltage-controlled switches (ctrl > 0.5 → closed) ---
.model SWCLOSE SW(Vt=0.5 Vh=0.1 Ron=0.05 Roff=100Meg)

.subckt sw_spst A B CTRL
S1 A B CTRL 0 SWCLOSE
.ends sw_spst

* SPDT: CTRL high → COM-A; low → COM-B
.subckt sw_spdt COM A B CTRL
S1 COM A CTRL 0 SWCLOSE
S2 COM B ninv 0 SWCLOSE
Binv ninv 0 V={1 - v(CTRL)}
.ends sw_spdt

* MODE: CTRL_P >0.5 → pitch; CTRL_T >0.5 → time; both low → open
.subckt sw_mode COM PITCH TIME CTRL_P CTRL_T
Sp COM PITCH CTRL_P 0 SWCLOSE
St COM TIME  CTRL_T 0 SWCLOSE
.ends sw_mode

* Jack normals: CTRL=0 (unplugged) tip↔sw; CTRL=1 open
.subckt jack_sw TIP SW GND CTRL
* closed when unplugged: use inverted ctrl
Binv ninv 0 V={1 - v(CTRL)}
Sn TIP SW ninv 0 SWCLOSE
Rg TIP GND 100Meg
.ends jack_sw
