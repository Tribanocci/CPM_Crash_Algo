import numpy as np
from scipy.optimize import milp, LinearConstraint,Bounds

def CPM_crash(N, Im_Cost, Tm, c, d, pr):
    d = np.array(d)
    # Periorismoi (Constraints)
    A = [[0]*(2*N+1)]
    b = []

    eq = 0
    for i in range(N):
        if len(pr[i]) == 0:
            if eq > 0:
                A.append([0]*(2*N+1))
            A[eq][i] = 1
            A[eq][N + 1 + i] = 1
            b.append(d[i])
            eq += 1
        else:
            for j in range(len(pr[i])):
                if eq > 0:
                    A.append([0]*(2*N+1))
                A[eq][i] = 1
                A[eq][pr[i][j]-1] = -1
                A[eq][N + 1 + i] = 1
                b.append(d[i])
                eq += 1

    for i in range(N):
        if eq > 0:
            A.append([0]*(2*N+1))
        A[eq][N] = 1
        A[eq][i] = -1
        b.append(0)
        eq += 1

    f = np.concatenate((np.zeros(N), [Im_Cost], np.array(c)), axis=0)
    A = np.array(A)
    intg = np.zeros_like(f)
    intg[(N+2)-1:] = np.ones_like(intg[(N+2)-1:])
    Ymax=d-Tm #megistos xronos sympiesis gia kathe ergasia
    b_l = np.array(b)
    b_u = np.ones_like(b_l)*np.inf
    l = np.zeros(2*N+1)
    u = np.concatenate((np.inf*np.ones(N+1), Ymax),axis=0)
    print(A)
    solv = milp(c=f, integrality=intg, bounds=Bounds(l, u), constraints=LinearConstraint(A, b_l, b_u))
    if solv.success:
        print("Optimization successful.")
        F = solv.x[:N+1]
        y = solv.x[N+1:]
        f_time = F[N]
        min_cost = np.dot(f, solv.x)
        compress_vector = y
        return [solv.success, f_time, min_cost, compress_vector]
    else:
        if solv.status == 2:
           return [solv.success, "Optimization failed: Problem is infeasible."]
        else:
            return [solv.success, "Optimization failed for another reason. Status:", solv.status]


#------Implementation Example------------------------

N=6
Im_Cost=100
Tm=np.array([4,7,8,4,3,2])
d=np.array([6,10,12,8,6,4])
c=np.array([90, 375/3.0, 300/4.0, 140/4.0 ,195/3.0 ,25])
pr=[    [],
        [1],
        [1],
        [1,2],
        [3],
        [4,5]
    ]

print(CPM_crash(N, Im_Cost, Tm, c, d, pr))

