* VOZ-9 — default panel state (overwritten by painel.html / export)
* Fractions u in [0,1]; switches 0/1; MODE -1/0/1

.param pitch_a=0.3
.param pitch_b=0.5
.param amount=0.5
.param shape=0.3
.param cutoff=0.5
.param rate=0.4
.param depth=0.3
.param pre=0.55
.param osc_in=0.7
.param eq_low=0.5
.param eq_mid_f=0.45
.param eq_mid_g=0.5
.param eq_high=0.5
.param time_u=0.4
.param fback=0.25
.param wet=0.4
.param volume=0.7

.param sw_osc_a=1
.param sw_osc_b=1
.param sw_drone=1
.param sw_trem=0
.param sw_trem_t=0
.param sw_trem_f=0
.param sw_mode=0
.param sw_h1=1
.param sw_h2=1
.param sw_h3=1
.param sw_stack=0
.param sw_gate=0

* Derived MODE controls (pitch / time) — avoid inline comparisons on V sources
.param sw_mode_p=0
.param sw_mode_t=0

.param jack_a=0
.param jack_b=0
.param jack_in=0
.param jack_filt=0
.param jack_fcv=0
.param jack_vcv=0
.param jack_lfo=0
.param jack_ecv=0
.param jack_clk=0
.param jack_send=0
.param jack_rcv=0
