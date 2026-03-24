# COSC 3P32 – Assignment 3 Solutions

---

## Question 1 [4 marks]

**Relation:** `Assignments(cid, semester, aid, type, duedate, weight, maxmarks)`  
**Attribute codes:** C = cid, S = semester, A = aid, T = type, D = duedate, W = weight, M = maxmarks

### a)
The key (cid, semester, aid) determines all other attributes:

> **CSA → TDWM**

### b)
For a given course, semester, and due date there is exactly one assignment (i.e. the combination CSD determines A):

> **CSD → A**

### c)
For a given course and semester, the same weight always implies the same max marks:

> **CSW → M**

### d)
For a given course, assignments of the same type always have the same weight:

> **CT → W**

---

## Question 2 [20 marks]

**Schema:** R = VWXYZ  
**FDs:** F = { VW→XY, V→X, W→Z, YZ→Z, Z→V }

### a) Three independent reasons the table is not a legal instance

| V  | W  | X  | Y  | Z  |
|----|----|----|----|----|
| v1 | w1 | x1 | y1 | z1 |
| v2 | w1 | x2 | y2 | z1 |
| v2 | w2 | x1 | y2 | z2 |

1. **V→X is violated (rows 2 and 3).**  
   Both rows have V = v2, yet X = x2 in row 2 and X = x1 in row 3. A functional dependency requires a unique X value for each V value.

2. **Z→V is violated (rows 1 and 2).**  
   Both rows have Z = z1, yet V = v1 in row 1 and V = v2 in row 2. A unique V value is required for each Z value.

3. **W→V is violated (rows 1 and 2).**  
   W→Z and Z→V together imply W→V (a member of F⁺). Both rows have W = w1, yet V = v1 in row 1 and V = v2 in row 2, violating this derived dependency.

---

### b) FDs on each projection

**R₁ = VWX**

Project F onto {V, W, X}.  Compute closures of all subsets of VWX:

- V⁺ = {V, X} (via V→X) → **V→X**  
- W⁺ = {W, Z, V, X} (via W→Z, Z→V, V→X); intersected with VWX → W→VX, so **W→V** (and W→X is implied by W→V plus V→X, so not listed separately)  
- VW⁺ is already covered by the two FDs above.

Non-trivial FDs on R₁ (excluding trivial and those implied by others in the set):

> **V→X,  W→V**

**R₂ = WYZ**

Project F onto {W, Y, Z}:

- W⁺ = VWXYZ (via W→Z, Z→V, V→X, then VW→XY since both V and W are in the closure); intersected with WYZ → W→YZ, giving **W→Z** and **W→Y**  
- Z⁺ = {Z, V, X}; intersected with WYZ = {Z}. No non-trivial FD.  
- Y⁺ = {Y}. No non-trivial FD.  
- YZ⁺ = {Y, Z, V, X}; intersected with WYZ = {Y, Z}. Only trivial.

Non-trivial FDs on R₂:

> **W→Z,  W→Y**

(equivalently written as W→YZ)

---

### c) Is the decomposition lossless-join?

The shared attributes are R₁ ∩ R₂ = **{W}**.

For a lossless-join decomposition, we need R₁ ∩ R₂ to be a superkey of at least one of the two sub-relations.  
W⁺ under F contains VWXYZ (shown above), so in particular W→VWX = R₁.  
Therefore **{W} is a superkey of R₁**, and the decomposition is **lossless-join**. ✓

---

### d) Lossless-join BCNF decomposition

**Step 0 – Find the key of R.**

Compute W⁺:  
W →(W→Z)→ Z →(Z→V)→ V →(V→X)→ X, and now with both V and W: VW →(VW→XY)→ Y.  
So W⁺ = **VWXYZ = R**. W is the unique candidate key.

**Step 0 – Identify BCNF violations.**

A non-trivial FD X→Y violates BCNF when X is not a superkey.

- VW→XY: VW ⊇ {W} (key) → superkey ✓  
- **V→X:** V⁺ = VX ≠ R → **violation**  
- W→Z: W is the key → superkey ✓  
- YZ→Z: trivial ✓  
- **Z→V:** Z⁺ = VXZ ≠ R → **violation**

**Step 1 – Decompose using V→X.**

V⁺ = {V, X}

- **R_A = VX** (key: V)
- **R_B = VWYZ** (R minus (V⁺ − V) = VWXYZ − {X})

FDs on R_B = VWYZ (project F):  
W⁺ ∩ VWYZ = VWYZ → W is the key of VWYZ.  
Z⁺ ∩ VWYZ = {Z, V} = VZ → Z is **not** a superkey → **BCNF violation (Z→V)**.  
Other FDs holding on VWYZ: W→Z, Z→V, W→V, VW→Y, W→Y.

**Step 2 – Decompose R_B = VWYZ using Z→V.**

Z⁺ (in VWYZ) = {Z, V}

- **R_C = VZ** (key: Z)
- **R_D = WYZ** (VWYZ minus (Z⁺ − Z) = VWYZ − {V})

FDs on R_D = WYZ:  
W⁺ ∩ WYZ = WYZ → W is the key; both W→Z (from F) and W→Y hold. All FDs have W (a superkey) on the left → **BCNF** ✓.

**Final decomposition:**

| Relation | Key | FDs |
|----------|-----|-----|
| **VX** | V | V→X |
| **VZ** | Z | Z→V |
| **WYZ** | W | W→Z, W→Y |

**Lossless-join verification:**  
- VX ∩ VWYZ = {V}; V→X holds → V is a key of VX ✓  
- VZ ∩ WYZ = {Z}; Z→V holds → Z is a key of VZ ✓  
Each decomposition step is lossless-join, so the overall decomposition is lossless-join. ✓

---

### e) Is the BCNF decomposition dependency-preserving?

First find the **minimal cover** of F:

1. Decompose RHS: { VW→X, VW→Y, V→X, W→Z, YZ→Z, Z→V }
2. Remove trivial FD YZ→Z.
3. Minimize LHS of VW→X: compute W⁺ without VW→X = {W,Z,V,X} (via W→Z, Z→V, V→X); X ∈ W⁺, so V is redundant → replace with **W→X**.
4. Minimize LHS of VW→Y: compute W⁺ without VW→Y = {W,Z,V,X}; Y ∉ W⁺, so V is not redundant. VW→Y stays.
5. Remove redundant FDs: W→X is redundant (derivable via W→Z, Z→V, V→X). Remove W→X.

**Minimal cover:** { **VW→Y, V→X, W→Z, Z→V** }

Now check each FD against decomposition {VX, VZ, WYZ}:

| FD | Preserved in | Without join? |
|----|-------------|---------------|
| V→X | VX | ✓ |
| W→Z | WYZ | ✓ |
| Z→V | VZ | ✓ |
| VW→Y | WYZ contains W→Y; augmentation gives VW→Y | ✓ |

All FDs in the minimal cover are preserved without joining any pair of relations. The decomposition **is dependency-preserving**. ✓

---

## Question 3 [11 marks]

**Schema:** R = ABCDEGH  
**FDs:** F = { B→AGH, CD→B, C→EG, E→AD, G→E }

---

### a) Minimal cover

**Step 1 – Decompose all RHS into singletons:**

{ B→A, B→G, B→H, CD→B, C→E, C→G, E→A, E→D, G→E }

**Step 2 – Minimize LHS (only CD→B has multiple attributes):**

- Remove C? Compute D⁺ = {D}. B ∉ D⁺ → C is not redundant.  
- Remove D? Compute C⁺ (without CD→B) = {C, E(C→E), G(C→G), A(E→A), D(E→D)} = {C,E,G,A,D}. B ∉ C⁺ → D is not redundant.  
CD→B stays as-is.

**Step 3 – Remove redundant FDs:**

- **B→A:** Remove it. B⁺ = {B, G(B→G), H(B→H), E(G→E), A(E→A), D(E→D)} = {A,B,D,E,G,H}. A ∈ B⁺ → **redundant, remove**.

  Current set: { B→G, B→H, CD→B, C→E, C→G, E→A, E→D, G→E }

- **B→G:** Remove it. B⁺ = {B,H}. G ∉ B⁺ → not redundant. Keep.

- **B→H:** Remove it. B⁺ = {B,G,E,A,D}. H ∉ B⁺ → not redundant. Keep.

- **CD→B:** Remove it. (CD)⁺ = {C,D,E,G,A}. B ∉ → not redundant. Keep.

- **C→E:** Remove it. C⁺ = {C, G(C→G), E(G→E), A(E→A), D(E→D)} = {C,G,E,A,D}. E ∈ C⁺ (via G→E) → **redundant, remove**.

  Current set: { B→G, B→H, CD→B, C→G, E→A, E→D, G→E }

- **C→G:** Remove it. C⁺ = {C}. G ∉ C⁺ → not redundant. Keep.

- **E→A:** Remove it. E⁺ = {E,D}. A ∉ → not redundant. Keep.

- **E→D:** Remove it. E⁺ = {E,A}. D ∉ → not redundant. Keep.

- **G→E:** Remove it. G⁺ = {G}. E ∉ → not redundant. Keep.

**Minimal cover:**

> **{ B→G, B→H, CD→B, C→G, E→A, E→D, G→E }**

(equivalently written with grouped RHS: { B→GH, CD→B, C→G, E→AD, G→E })

---

### b) Candidate keys

Identify attributes that **never** appear on the right-hand side of any FD in the minimal cover:

RHS attributes = { G, H, B, G, A, D, E } = {A, B, D, E, G, H}.  
Attribute **C** does not appear in any RHS → C must be in every candidate key.

Compute C⁺:  
C →(C→G)→ G →(G→E)→ E →(E→A)→ A, →(E→D)→ D. Now C and D are in the closure →(CD→B)→ B →(B→H)→ H.  
C⁺ = **{A, B, C, D, E, G, H} = R**. ✓

C alone is a superkey; no proper subset of {C} (i.e., ∅) is a superkey.

> **Unique candidate key: { C }**

---

### c) 3NF Synthesis

**Step 1 – Create a relation for each FD in the minimal cover (grouping same LHS):**

| Relation | Generating FD(s) | Proposed Key |
|----------|-----------------|--------------|
| **BGH** | B→GH | B |
| **BCD** | CD→B | CD |
| **CG** | C→G | C |
| **ADE** | E→AD | E |
| **GE** | G→E | G |

**Step 2 – Ensure a candidate key of R is present.**

The candidate key of R is {C}. Relation **BCD** contains C → no new relation needed. ✓

**Step 3 – Remove redundant relations (subsets of others).**

No relation is a subset of another. None removed.

**Final 3NF decomposition: { BGH, BCD, CG, ADE, GE }**

**FDs on each relation:**

*BGH* (key: B):  
- **B→GH**  
  *(G⁺ ∩ BGH = {G}; H⁺ ∩ BGH = {H} — no other non-trivial FDs)*

*BCD* (key: C):  
C⁺ includes D (via C→G→E→D) and then B (via CD→B), so C is the sole candidate key.  
- **CD→B**  
- **C→BD** (C→D via the chain C→G→E→D; C→B via C→D + CD→B)  
- **B→D** (via B→G→E→D, projected onto BCD)  
  *(CD→B is implied by C→B; we show the independent set)*

*CG* (key: C):  
- **C→G**

*ADE* (key: E):  
- **E→AD**

*GE* (key: G):  
- **G→E**

**Lossless-join:** The decomposition contains relation BCD which includes C, the sole candidate key of R. By the 3NF synthesis theorem this guarantees a lossless join. ✓

**Dependency-preserving:** Every FD in the minimal cover appears directly in one of the resulting relations (B→GH in BGH, CD→B in BCD, C→G in CG, E→AD in ADE, G→E in GE). ✓

---

## Question 4 [15 marks]

```sql
Restaurant(rname, address, phone, stars)
Chef(cname, specialdish, rating)
CooksFor(cname, rname, salary)
Offers(rname, dishname, price)
```

---

### a) CHECK – every chef has a rating between 0 and 10

Add to the `Chef` table:

```sql
CHECK (rating >= 0 AND rating <= 10)
```

---

### b) CHECK – no chef salary at 'BigMac' exceeds 100

Add to the `CooksFor` table:

```sql
CHECK (rname <> 'BigMac' OR salary <= 100)
```

---

### c) Assertion – every restaurant has at least one chef

```sql
CREATE ASSERTION every_restaurant_has_chef
CHECK (
    NOT EXISTS (
        SELECT *
        FROM   Restaurant R
        WHERE  NOT EXISTS (
                   SELECT *
                   FROM   CooksFor CF
                   WHERE  CF.rname = R.rname
               )
    )
);
```

---

### d) Assertion – every offered dish has at least one chef whose special dish it is

```sql
CREATE ASSERTION every_dish_has_special_chef
CHECK (
    NOT EXISTS (
        SELECT *
        FROM   Offers O
        WHERE  NOT EXISTS (
                   SELECT *
                   FROM   Chef C
                   WHERE  C.specialdish = O.dishname
               )
    )
);
```

---

### e) Trigger – 10% raise on stars increase (SQL:1999 standard)

```sql
CREATE TRIGGER stars_raise
AFTER UPDATE OF stars ON Restaurant
REFERENCING OLD ROW AS old_row
            NEW ROW AS new_row
FOR EACH ROW
WHEN (new_row.stars > old_row.stars)
BEGIN ATOMIC
    UPDATE CooksFor
    SET    salary = salary * 1.10
    WHERE  rname = new_row.rname;
END;
```

*The `WHEN` clause fires only when the star rating **increases**. The `FOR EACH ROW` granularity ensures the correct `rname` is available for each updated restaurant. The 10% raise is applied to all chefs currently cooking for that restaurant.*
