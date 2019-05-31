NEURON {
  SUFFIX max
  USEION ca READ cai
  RANGE val, cval, vmin, cmin, cmean, vmean, Csum
}

ASSIGNED {
  v (millivolt)
  val (millivolt)
  vmin (millivolt)
  vmean (millivolt)
	cai (millimolar)
	cval (millimolar)
	cmin (millimolar)
	cmean (millimolar)
  Vsum (mV)
  Csum (mV)
  npts (1)
}

INITIAL {
  Vsum = 0
  Csum = 0
  npts = 0
  val = v
  cval = cai
  vmin = v
  cmin = cai
	
}

BREAKPOINT {
  if (v>val) {
    val = v
  }
  if( cai > cval ) {
	cval = cai
  }

  if (v<vmin) {
    vmin = v
  }
  if( cai > cval ) {
	cval = cai
  }

  Vsum = Vsum + v
  Csum = Csum + cai
  npts = npts + 1

  vmean = Vsum/npts
  cmean = Csum/npts
}
