"""Reference-distance error forced by retaining the supplied interior fixes."""
import numpy as np

def distance_error_floor(observed,reference_length,horizon):
    p=np.asarray(observed,dtype=float)
    if p.ndim!=2 or p.shape[1]!=3 or len(p)<2 or not np.isfinite(p).all() or np.any(np.diff(p[:,0])<=0):
        raise ValueError('Finite time-ordered (time,x,y) fixes required')
    if not np.isfinite(reference_length) or reference_length<0 or not np.isfinite(horizon) or horizon<=0:
        raise ValueError('Nonnegative finite distance and positive horizon required')
    inside=p[(p[:,0]>=0)&(p[:,0]<=horizon)]
    chords=float(np.linalg.norm(np.diff(inside[:,1:],axis=0),axis=1).sum())
    return max(0.,chords-reference_length)
