"""k-means on 150 points, standard library only. This is the "source" the explainer walks through."""
import math
import random

random.seed(7)
TRUE_CENTRES = [(2.0, 2.0), (7.0, 3.0), (4.5, 7.5)]
points = [(random.gauss(cx, 1.0), random.gauss(cy, 1.0)) for cx, cy in TRUE_CENTRES for _ in range(50)]
K = 3


def nearest(p, centres):
    return min(range(len(centres)), key=lambda k: math.dist(p, centres[k]))


def mean(ps):
    return (sum(x for x, _ in ps) / len(ps), sum(y for _, y in ps) / len(ps))


centres = random.sample(points, K)          # start: K random points
history = []
while True:
    labels = [nearest(p, centres) for p in points]
    new = [mean([p for p, l in zip(points, labels) if l == k]) for k in range(K)]
    moved = max(math.dist(a, b) for a, b in zip(centres, new))
    history.append({"centres": centres, "labels": labels, "moved": moved})
    centres = new
    if moved < 1e-6:
        break

inertia = sum(math.dist(p, centres[l]) ** 2 for p, l in zip(points, labels))
print(f"converged after {len(history)} rounds, inertia {inertia:.1f}")
