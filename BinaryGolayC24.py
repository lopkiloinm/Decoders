import numpy as np

# Define the matrix B from the textbook
B = np.array([
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0],
    [1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1],
    [1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0],
    [1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1],
    [1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1],
    [1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 1],
    [1, 0, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0],
    [1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0],
    [1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0],
    [1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1]
], dtype=int)

# Add identity matrix to form G
I = np.eye(12, dtype=int)
G = np.hstack((I, B))

def compute_syndrome(r):
    return np.dot(r, G.T) % 2

def weight(vec):
    return np.sum(vec)

def print_vector(v, name="vector"):
    v_str = ''.join(map(str, v.astype(int)))
    print(f"${name} = ({v_str})$")

def correct_errors(r):
    s = compute_syndrome(r)
    print("\\textbf{Step 1: Compute Syndrome}")
    print_vector(s, "s")

    # Condition (2)
    if weight(s) <= 3:
        e = np.concatenate((s, np.zeros(12, dtype=int)))
        print("\\textbf{Condition (2) met: }", end="")
        print_vector(e, "e")
        return (r - e) % 2

    # Condition (3)
    for i, l_i in enumerate(B.T, start=1):
        if weight((s + l_i) % 2) <= 2:
            y_i = np.zeros(12, dtype=int)
            y_i[i-1] = 1
            e = np.concatenate(((s + l_i) % 2, y_i))
            print(f"\\textbf{{Condition (3) met for $l_{{{i}}}$:}}")
            print_vector(e, "e")
            return (r - e) % 2

    print("\\textbf{Step 4: Compute } $B^T S$")
    B_T_s = np.dot(B.T, s) % 2
    print_vector(B_T_s, "B^T S")

    # Condition (5)
    if weight(B_T_s) <= 3:
        e = np.concatenate((np.zeros(12, dtype=int), B_T_s))
        print("\\textbf{Condition (5) met: }", end="")
        print_vector(e, "e")
        return (r - e) % 2

    # Condition (6)
    for i, r_i in enumerate(B, start=0):
        if weight((B.T @ s + r_i) % 2) <= 2:
            x_i = np.zeros(12, dtype=int)
            x_i[i] = 1
            e = np.concatenate((x_i, (B.T @ s + r_i) % 2))
            print(f"\\textbf{{Condition (6) met for $r_{{{i+1}}}$:}}")
            print_vector(e, "e")
            return (r - e) % 2

    # Condition (7)
    print("\\textbf{At least 4 errors detected. Request retransmission.}")
    return None

# Define an example received vector r
r = np.array(list(map(int, list("111100000000001110100111"))))
print("\\textbf{Received Vector}")
print_vector(r, "r")

# Attempt to correct errors in r
corrected_r = correct_errors(r)
if corrected_r is not None:
    print("\\textbf{Corrected Vector}")
    print_vector(corrected_r, "Corrected r")
else:
    # Handle failure to correct 
    print("\\textbf{Failure to correct r.}")
