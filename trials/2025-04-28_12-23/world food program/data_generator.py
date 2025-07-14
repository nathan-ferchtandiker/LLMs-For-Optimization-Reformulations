import random

def generate_data_dat(filename='data.dat', seed=42):
    random.seed(seed)

    # Sizes
    num_suppliers = 20
    num_transshipment = 25
    num_beneficiaries = 15
    num_nodes = num_suppliers + num_transshipment + num_beneficiaries
    num_commodities = 10
    num_nutrients = 7

    # Create nodes
    nodes = [f"n{i}" for i in range(1, num_nodes+1)]

    # Create subsets
    suppliers = nodes[0:num_suppliers]  # First node as supplier
    beneficiaries = nodes[num_suppliers:num_suppliers+num_beneficiaries]  # Last nodes as beneficiaries
    transshipment = nodes[num_suppliers+num_beneficiaries:]

    # Create arcs (randomly connecting nodes)
    arcs = []
    for i in suppliers:
        for j in transshipment:
            if i != j and random.random() < 0.15:
                arcs.append((i, j))
                
    for i in transshipment:
        for j in beneficiaries:
            if i != j and random.random() < 0.15:
                arcs.append((i, j))
        
    # Commodities and nutrients
    commodities = [f"c{k}" for k in range(1, num_commodities+1)]
    nutrients = [f"nut{l}" for l in range(1, num_nutrients+1)]

    # Paths: all possible paths from suppliers to beneficiaries through transshipment nodes
    paths = []
    for s in suppliers:
        for b in beneficiaries:
            for t in transshipment:
                paths.append(f"{s}_{t}_{b}")

    # Write to file
    with open(filename, 'w') as f:
        # Sets
        f.write(f"set P := {' '.join(paths)};\n")
        f.write(f"set K := {' '.join(commodities)};\n")
        f.write(f"set L := {' '.join(nutrients)};\n")
        f.write(f"set N := {' '.join(nodes)};\n")
        f.write(f"set A := " + ' '.join(f"({i} {j})" for (i,j) in arcs) + ";\n")
        f.write(f"set N_S := {' '.join(suppliers)};\n")
        f.write(f"set N_T := {' '.join(transshipment)};\n")
        f.write(f"set N_B := {' '.join(beneficiaries)};\n\n")

        # Parameters
        # Cost per path/commodity
        f.write("param cpk:\n")
        f.write("         " + '   '.join(commodities) + " :=\n")
        for p in paths:
            f.write(f"    {p}   " + '   '.join(f"{random.uniform(1,5):.2f}" for _ in commodities) + "\n")
        f.write(";\n\n")

        # Cost per arc/commodity
        f.write("param c:\n")
        f.write("          " + '   '.join(commodities) + " :=\n")
        for (i,j) in arcs:
            f.write(f"({i},{j}) " + '   '.join(f"{random.uniform(1,5):.2f}" for _ in commodities) + "\n")
        f.write(";\n\n")

        # Nutrient value
        f.write("param nutval:\n")
        f.write("          " + '   '.join(nutrients) + " :=\n")
        for k in commodities:
            f.write(f"    {k}   " + '   '.join(f"{random.uniform(1,10):.2f}" for _ in nutrients) + "\n")
        f.write(";\n\n")

        # Nutrient requirement
        f.write("param nutreq :=\n")
        for l in nutrients:
            f.write(f"    {l}   {random.uniform(50, 500):.1f}\n")
        f.write(";\n\n")

        # Demand at beneficiary camps
        f.write("param dem :=\n")
        for b in beneficiaries:
            f.write(f"    {b}   {random.randint(50, 500)}\n")
        f.write(";\n\n")

        # Path to beneficiary camp mapping
        f.write("param e:\n")
        f.write("        " + '   '.join(paths) + " :=\n")
        for b in beneficiaries:
            f.write(f"    {b}   " + '   '.join(str(random.choice([0,1])) for _ in paths) + "\n")
        f.write(";\n\n")

        f.write("end;\n")

generate_data_dat('data.dat', seed=42)