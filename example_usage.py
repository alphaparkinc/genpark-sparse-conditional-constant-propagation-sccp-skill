from client import SCCPOptimizer

def main():
    print("=== Testing Sparse Conditional Constant Propagation ===")
    ir = [
        ('a', 'CONST', 5, None),
        ('b', 'CONST', 15, None),
        ('c', '+', 'a', 'b'),
        ('d', '*', 'c', 2),
    ]
    sccp = SCCPOptimizer(ir)
    constants = sccp.run()
    print("SCCP Found Constants:", constants)
    assert constants['c'] == 20
    assert constants['d'] == 40

    print("SCCP Optimizer verified successfully!")

if __name__ == '__main__':
    main()
