import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib.animation import PillowWriter
m = 1
hbar = 1
std = 0.5
mean = -60
N = 1000
x = np.linspace(-70,70,N+2)
dx = x[1]-x[0]
k0 = 5
lamda  = hbar**2/(2*m*(dx**2))
v = 0*x
v0=1.7*(k0**2)/2*m
for i in range(len(v)):
    if x[i]<=-10 and x[i]>=-11.7:
        v[i]=12.5
psi_0 = (np.exp( -(x[1:-1]-mean)**2/4*(std**2))/np.sqrt(std*np.sqrt(2*np.pi)))*np.exp(1j*k0*(x[1:-1]-mean))
A = np.cumsum((np.abs(psi_0**2))*dx)/4
H = lamda*(2*np.diag(np.ones(N)) - np.diag(np.ones(N-1),-1) - np.diag(np.ones(N-1),1) + (v[1:-1]/lamda)*np.diag(np.ones(N)))
E, psi = np.linalg.eigh(H)
B = np.sum(np.abs((psi[:,0])**2)*dx)
psi = psi/np.sqrt(B)
c = 0*psi_0
for i in range(len(c)):
    c[i] = np.sum(psi_0*np.conj(psi[:,i])*dx)
c = c/np.sqrt(np.sum(np.abs(c)**2)) 
def Psi(t):
    return psi@(c*np.exp(-E*1j*t/hbar))/np.sqrt(7.150000000000343)
np.sum(np.abs(c[298:1000])**2)
avgE = np.sum(E*np.abs(c)**2)
print(f"average energy(E): {avgE}")
t=15
R = np.sum(np.abs(Psi(t)[0:428])**2)
T = np.sum(np.abs(Psi(t)[429:999])**2)
print(f"Reflection (R): {R}")
print(f"Transmission (T): {T}")
print(f"R + T: {R + T}")
fig, ax = plt.subplots(1,1,figsize = (7,4))
ln2, = plt.plot([],[],color="darkblue",label='Real')
ln3, = plt.plot([],[],color="limegreen",label='Imaginary')
ln1, = plt.plot([],[],color="red",label='$\psi^* \psi$')
ax.set_title('Quantum Tunneling')
ax.set_xlim(-55,40)
ax.set_ylim(-0.21,0.21)
ax.plot(x[1:-1],0.19/12.5*v[1:-1],color="black")
plt.legend(handles=[ln1,ln2,ln3]);
ax.legend(loc='upper right')
def animate(i):
    ln1.set_data(x[1:-1],np.abs(Psi(1/25*i))**2)
    ln2.set_data(x[1:-1],np.real(Psi(1/25*i)))
    ln3.set_data(x[1:-1],np.imag(Psi(1/25*i)))
ani = animation.FuncAnimation(fig,animate,frames=625,interval=50)   
ani.save('Quantum tunneling.gif',writer='pillow',fps=30,dpi=100)