/* Created by Language version: 6.2.0 */
/* VECTORIZED */
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include "scoplib_ansi.h"
#undef PI
#define nil 0
#include "md1redef.h"
#include "section.h"
#include "nrniv_mf.h"
#include "md2redef.h"
 
#if METHOD3
extern int _method3;
#endif

#if !NRNGPU
#undef exp
#define exp hoc_Exp
extern double hoc_Exp(double);
#endif
 
#define _threadargscomma_ _p, _ppvar, _thread, _nt,
#define _threadargs_ _p, _ppvar, _thread, _nt
 
#define _threadargsprotocomma_ double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt,
#define _threadargsproto_ double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt
 	/*SUPPRESS 761*/
	/*SUPPRESS 762*/
	/*SUPPRESS 763*/
	/*SUPPRESS 765*/
	 extern double *getarg();
 /* Thread safe. No static _p or _ppvar. */
 
#define t _nt->_t
#define dt _nt->_dt
#define vhalf _p[0]
#define tpeak _p[1]
#define vpeak _p[2]
#define vpeakm _p[3]
#define dvdt2 _p[4]
#define dvdt2peak _p[5]
#define dvdtpeak _p[6]
#define onset_ref _p[7]
#define onset _p[8]
#define vonset _p[9]
#define halfwidth _p[10]
#define dvdr _p[11]
#define vrest _p[12]
#define Rmismatch _p[13]
#define Zmismatch _p[14]
#define Rback _p[15]
#define Zback _p[16]
#define Rfwd _p[17]
#define Zfwd _p[18]
#define R _p[19]
#define Z _p[20]
#define aRmismatch _p[21]
#define aZmismatch _p[22]
#define aRback _p[23]
#define aZback _p[24]
#define aRfwd _p[25]
#define aZfwd _p[26]
#define aR _p[27]
#define aZ _p[28]
#define f _p[29]
#define Xo _p[30]
#define Xlen _p[31]
#define Xsec _p[32]
#define Xfrc _p[33]
#define sign _p[34]
#define dvdt _p[35]
#define v1 _p[36]
#define v2 _p[37]
#define v3 _p[38]
#define below _p[39]
#define below_old _p[40]
#define upstroke _p[41]
#define downstroke _p[42]
#define v _p[43]
#define _g _p[44]
 
#if MAC
#if !defined(v)
#define v _mlhv
#endif
#if !defined(h)
#define h _mlhh
#endif
#endif
 
#if defined(__cplusplus)
extern "C" {
#endif
 static int hoc_nrnpointerindex =  -1;
 static Datum* _extcall_thread;
 static Prop* _extcall_prop;
 /* external NEURON variables */
 /* declaration of user functions */
 static void _hoc_check(void);
 static int _mechtype;
extern void _nrn_cacheloop_reg(int, int);
extern void hoc_register_prop_size(int, int, int);
extern void hoc_register_limits(int, HocParmLimits*);
extern void hoc_register_units(int, HocParmUnits*);
extern void nrn_promote(Prop*, int, int);
extern Memb_func* memb_func;
 extern void _nrn_setdata_reg(int, void(*)(Prop*));
 static void _setdata(Prop* _prop) {
 _extcall_prop = _prop;
 }
 static void _hoc_setdata() {
 Prop *_prop, *hoc_getdata_range(int);
 _prop = hoc_getdata_range(_mechtype);
   _setdata(_prop);
 hoc_retpushx(1.);
}
 /* connect user functions to hoc names */
 static VoidFunc hoc_intfunc[] = {
 "setdata_pk", _hoc_setdata,
 "check_pk", _hoc_check,
 0, 0
};
 /* declare global and static user variables */
 /* some parameters have upper and lower limits */
 static HocParmLimits _hoc_parm_limits[] = {
 0,0,0
};
 static HocParmUnits _hoc_parm_units[] = {
 "vhalf_pk", "mV",
 "tpeak_pk", "ms",
 "vpeak_pk", "mV",
 "vpeakm_pk", "mV",
 "dvdt2_pk", "mV/ms*ms",
 "dvdt2peak_pk", "mV/ms*ms",
 "dvdtpeak_pk", "mV/ms",
 "onset_ref_pk", "mV/ms",
 "onset_pk", "ms",
 "vonset_pk", "mV",
 "halfwidth_pk", "ms",
 "dvdr_pk", "mv/micron",
 "vrest_pk", "mV",
 "Rmismatch_pk", "1",
 "Zmismatch_pk", "1",
 "Rback_pk", "Mohm",
 "Zback_pk", "Mohm",
 "Rfwd_pk", "Mohm",
 "Zfwd_pk", "Mohm",
 "R_pk", "Mohm",
 "Z_pk", "Mohm",
 "aRmismatch_pk", "1",
 "aZmismatch_pk", "1",
 "aRback_pk", "Mohm",
 "aZback_pk", "Mohm",
 "aRfwd_pk", "Mohm",
 "aZfwd_pk", "Mohm",
 "aR_pk", "Mohm",
 "aZ_pk", "Mohm",
 "Xo_pk", "1",
 "Xlen_pk", "1",
 "Xsec_pk", "1",
 "Xfrc_pk", "1",
 "sign_pk", "1",
 0,0
};
 static double delta_t = 1;
 /* connect global user variables to hoc */
 static DoubScal hoc_scdoub[] = {
 0,0
};
 static DoubVec hoc_vdoub[] = {
 0,0,0
};
 static double _sav_indep;
 static void nrn_alloc(Prop*);
static void  nrn_init(_NrnThread*, _Memb_list*, int);
static void nrn_state(_NrnThread*, _Memb_list*, int);
 static void nrn_cur(_NrnThread*, _Memb_list*, int);
static void  nrn_jacob(_NrnThread*, _Memb_list*, int);
 
static int _ode_count(int);
 /* connect range variables in _p that hoc is supposed to know about */
 static const char *_mechanism[] = {
 "6.2.0",
"pk",
 "vhalf_pk",
 0,
 "tpeak_pk",
 "vpeak_pk",
 "vpeakm_pk",
 "dvdt2_pk",
 "dvdt2peak_pk",
 "dvdtpeak_pk",
 "onset_ref_pk",
 "onset_pk",
 "vonset_pk",
 "halfwidth_pk",
 "dvdr_pk",
 "vrest_pk",
 "Rmismatch_pk",
 "Zmismatch_pk",
 "Rback_pk",
 "Zback_pk",
 "Rfwd_pk",
 "Zfwd_pk",
 "R_pk",
 "Z_pk",
 "aRmismatch_pk",
 "aZmismatch_pk",
 "aRback_pk",
 "aZback_pk",
 "aRfwd_pk",
 "aZfwd_pk",
 "aR_pk",
 "aZ_pk",
 "f_pk",
 "Xo_pk",
 "Xlen_pk",
 "Xsec_pk",
 "Xfrc_pk",
 "sign_pk",
 0,
 0,
 0};
 
extern Prop* need_memb(Symbol*);

static void nrn_alloc(Prop* _prop) {
	Prop *prop_ion;
	double *_p; Datum *_ppvar;
 	_p = nrn_prop_data_alloc(_mechtype, 45, _prop);
 	/*initialize range parameters*/
 	vhalf = 0;
 	_prop->param = _p;
 	_prop->param_size = 45;
 
}
 static void _initlists();
 extern Symbol* hoc_lookup(const char*);
extern void _nrn_thread_reg(int, int, void(*f)(Datum*));
extern void _nrn_thread_table_reg(int, void(*)(double*, Datum*, Datum*, _NrnThread*, int));
extern void hoc_register_tolerance(int, HocStateTolerance*, Symbol***);
extern void _cvode_abstol( Symbol**, double*, int);

 void _peak_reg() {
	int _vectorized = 1;
  _initlists();
 	register_mech(_mechanism, nrn_alloc,nrn_cur, nrn_jacob, nrn_state, nrn_init, hoc_nrnpointerindex, 1);
 _mechtype = nrn_get_mechtype(_mechanism[1]);
     _nrn_setdata_reg(_mechtype, _setdata);
  hoc_register_dparam_size(_mechtype, 0);
 	hoc_register_cvode(_mechtype, _ode_count, 0, 0, 0);
 	hoc_register_var(hoc_scdoub, hoc_vdoub, hoc_intfunc);
 	ivoc_help("help ?1 pk /Users/cweaver/research/Neuron/Coskren/MorphologyPaperTwo/Scripts/NeuronMechanisms/x86_64/peak.mod\n");
 hoc_register_limits(_mechtype, _hoc_parm_limits);
 hoc_register_units(_mechtype, _hoc_parm_units);
 }
static int _reset;
static char *modelname = "peak.mod";

static int error;
static int _ninits = 0;
static int _match_recurse=1;
static void _modl_cleanup(){ _match_recurse=1;}
static int check(_threadargsproto_);
 
static int  check ( _threadargsproto_ ) {
   if ( v > vpeak  && vpeakm  == - 100.0 ) {
     tpeak = t ;
     vpeak = v ;
     }
   if ( v + 4.0 < vpeak ) {
     vpeakm = 1.0 ;
     }
   v1 = v2 ;
   v2 = v3 ;
   v3 = v ;
   dvdt = ( v3 - v2 ) / ( dt ) ;
   dvdt2 = ( v3 - 2.0 * v2 + v1 ) / ( dt * dt ) ;
   if ( dvdt > dvdtpeak ) {
     dvdtpeak = dvdt ;
     }
   if ( dvdt2 > dvdt2peak ) {
     dvdt2peak = dvdt2 ;
     }
   if ( dvdt > onset_ref  && onset  == 0.0  && t > 1.0 ) {
     onset = t - dt ;
     vonset = v2 ;
     }
   below = 0.0 ;
   if ( vhalf > v ) {
     below = 1.0 ;
     }
   if ( below  == 0.0  && below_old  == 1.0  && upstroke  == 0.0 ) {
     upstroke = t ;
     }
   if ( below  == 1.0  && below_old  == 0.0  && downstroke  == 0.0 ) {
     downstroke = t ;
     }
   halfwidth = downstroke - upstroke ;
   below_old = below ;
    return 0; }
 
static void _hoc_check(void) {
  double _r;
   double* _p; Datum* _ppvar; Datum* _thread; _NrnThread* _nt;
   if (_extcall_prop) {_p = _extcall_prop->param; _ppvar = _extcall_prop->dparam;}else{ _p = (double*)0; _ppvar = (Datum*)0; }
  _thread = _extcall_thread;
  _nt = nrn_threads;
 _r = 1.;
 check ( _p, _ppvar, _thread, _nt );
 hoc_retpushx(_r);
}
 
static int _ode_count(int _type){ hoc_execerror("pk", "cannot be used with CVODE"); return 0;}

static void initmodel(double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt) {
  int _i; double _save;{
 {
   tpeak = 0.0 ;
   vpeak = - 100.0 ;
   vpeakm = - 100.0 ;
   onset = 0.0 ;
   dvdtpeak = 0.0 ;
   dvdt2peak = 0.0 ;
   downstroke = 0.0 ;
   upstroke = 0.0 ;
   vrest = v ;
   check ( _threadargs_ ) ;
   }
 
}
}

static void nrn_init(_NrnThread* _nt, _Memb_list* _ml, int _type){
double* _p; Datum* _ppvar; Datum* _thread;
Node *_nd; double _v; int* _ni; int _iml, _cntml;
#if CACHEVEC
    _ni = _ml->_nodeindices;
#endif
_cntml = _ml->_nodecount;
_thread = _ml->_thread;
for (_iml = 0; _iml < _cntml; ++_iml) {
 _p = _ml->_data[_iml]; _ppvar = _ml->_pdata[_iml];
#if CACHEVEC
  if (use_cachevec) {
    _v = VEC_V(_ni[_iml]);
  }else
#endif
  {
    _nd = _ml->_nodelist[_iml];
    _v = NODEV(_nd);
  }
 v = _v;
 initmodel(_p, _ppvar, _thread, _nt);
}}

static double _nrn_current(double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt, double _v){double _current=0.;v=_v;{
} return _current;
}

static void nrn_cur(_NrnThread* _nt, _Memb_list* _ml, int _type) {
double* _p; Datum* _ppvar; Datum* _thread;
Node *_nd; int* _ni; double _rhs, _v; int _iml, _cntml;
#if CACHEVEC
    _ni = _ml->_nodeindices;
#endif
_cntml = _ml->_nodecount;
_thread = _ml->_thread;
for (_iml = 0; _iml < _cntml; ++_iml) {
 _p = _ml->_data[_iml]; _ppvar = _ml->_pdata[_iml];
#if CACHEVEC
  if (use_cachevec) {
    _v = VEC_V(_ni[_iml]);
  }else
#endif
  {
    _nd = _ml->_nodelist[_iml];
    _v = NODEV(_nd);
  }
 
}}

static void nrn_jacob(_NrnThread* _nt, _Memb_list* _ml, int _type) {
double* _p; Datum* _ppvar; Datum* _thread;
Node *_nd; int* _ni; int _iml, _cntml;
#if CACHEVEC
    _ni = _ml->_nodeindices;
#endif
_cntml = _ml->_nodecount;
_thread = _ml->_thread;
for (_iml = 0; _iml < _cntml; ++_iml) {
 _p = _ml->_data[_iml];
#if CACHEVEC
  if (use_cachevec) {
	VEC_D(_ni[_iml]) += _g;
  }else
#endif
  {
     _nd = _ml->_nodelist[_iml];
	NODED(_nd) += _g;
  }
 
}}

static void nrn_state(_NrnThread* _nt, _Memb_list* _ml, int _type) {
 double _break, _save;
double* _p; Datum* _ppvar; Datum* _thread;
Node *_nd; double _v; int* _ni; int _iml, _cntml;
#if CACHEVEC
    _ni = _ml->_nodeindices;
#endif
_cntml = _ml->_nodecount;
_thread = _ml->_thread;
for (_iml = 0; _iml < _cntml; ++_iml) {
 _p = _ml->_data[_iml]; _ppvar = _ml->_pdata[_iml];
 _nd = _ml->_nodelist[_iml];
#if CACHEVEC
  if (use_cachevec) {
    _v = VEC_V(_ni[_iml]);
  }else
#endif
  {
    _nd = _ml->_nodelist[_iml];
    _v = NODEV(_nd);
  }
 _break = t + .5*dt; _save = t;
 v=_v;
{
 { {
 for (; t < _break; t += dt) {
  { check(_p, _ppvar, _thread, _nt); }
  
}}
 t = _save;
 } {
   }
}}

}

static void terminal(){}

static void _initlists(){
 double _x; double* _p = &_x;
 int _i; static int _first = 1;
  if (!_first) return;
_first = 0;
}

#if defined(__cplusplus)
} /* extern "C" */
#endif
