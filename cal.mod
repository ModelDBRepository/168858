TITLE Calcium high-threshold L type current for RD Traub, J Neurophysiol 89:909-921, 2003

COMMENT

	Implemented by Maciej Lazarewicz 2003 (mlazarew@seas.upenn.edu)

ENDCOMMENT

INDEPENDENT { t FROM 0 TO 1 WITH 1 (ms) }

UNITS { 
	(mV) = (millivolt) 
	(mA) = (milliamp) 
}
 
NEURON { 
	SUFFIX cal
	USEION ca WRITE ica
	RANGE  gbar, ica, vshift
}

PARAMETER { 
	gbar = 0.0 	(mho/cm2)
	v  		(mV)  
        vshift =0.0     (mV)
}
 
ASSIGNED { 
	ica 		(mA/cm2) 
	alpha beta	(/ms)
}
 
STATE {
	m
}

BREAKPOINT { 
	SOLVE states METHOD cnexp
	ica = gbar * m * m * ( v - 125 ) 
}
 
INITIAL { 
	rates(v) 
	m = alpha / ( alpha + beta )
	m = 0
}
 
DERIVATIVE states { 
	rates(v) 
	m' = alpha * ( 1 - m ) - beta * m 
}

UNITSOFF 

PROCEDURE rates(v) { LOCAL tmp

	alpha = 1.6 / ( 1 + exp( - 0.072 * ( v + vshift - 5 ) ) )
	tmp = v + vshift + 8.9
	if ( fabs( tmp ) < 1e-6 ) {
		beta  = 0.1 * exp( - tmp / 5 ) 
	}else{
		beta  = 0.02 * tmp / ( exp( tmp / 5 ) - 1 )
	}
}

UNITSON
