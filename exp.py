def is_on_curve(x: int, y: int, a: int, b: int, p: int) -> bool:
    """Check if point (x, y) lies on y^2 = x^3 + ax + b (mod p)."""
    return (y ** 2) % p == (x ** 3 + a * x + b) % p


def find_all_points(a: int, b: int, p: int) -> list[tuple[int, int]]:
    """Find all valid (x, y) points on the elliptic curve over F_p."""
    points = []
    for x in range(p):
        for y in range(p):
            if is_on_curve(x, y, a, b, p):
                points.append((x, y))
    return points


def main():
    # Parameters for y^2 = x^3 - x + 1 (mod 97)
    a, b, p = -1, 1, 97

    print("Calculating points...", flush=True)
    curve_points = find_all_points(a, b, p)
    print(f"Total valid points found on curve: {len(curve_points)}", flush=True)

    test_points = [(97, 96), (1, 1), (5, 10), (10, 20)]
    print("\n--- Point Verification ---", flush=True)
    for pt in test_points:
        status = (
            "ON the curve"
            if is_on_curve(pt[0], pt[1], a, b, p)
            else "NOT on the curve"
        )
        print(f"Point {pt}: {status}", flush=True)


if __name__ == "__main__":
    main()