import time

def benchmark_python(num_iterations=10_000_000):
    print("======================================================")
    print(f"   BENCHMARK PYTHON PUR (N = {num_iterations} iterations)")
    print("======================================================")
    
    a = 1.4
    b = 0.3
    x = 0.1
    y = 0.1

    start_time = time.perf_counter()
    for _ in range(num_iterations):
        x_next = 1.0 - a * x * x + y
        y_next = b * x
        x = x_next
        y = y_next
    end_time = time.perf_counter()

    elapsed = end_time - start_time
    print(f"[Python - CPU Pur] Temps : {elapsed:.4f} secondes  (Etat final: x={x:.4f}, y={y:.4f})")
    print("======================================================\n")

if __name__ == "__main__":
    benchmark_python()
