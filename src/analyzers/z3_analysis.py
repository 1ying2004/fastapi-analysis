from z3 import *

def demo_z3_solver():
    """Z3约束求解演示"""
    x = Int('x')
    y = Int('y')
    
    solver = Solver()
    solver.add(x > 0)
    solver.add(y > 0)
    solver.add(x + y == 10)
    solver.add(x > y)
    
    if solver.check() == sat:
        model = solver.model()
        print(f"解: x={model[x]}, y={model[y]}")
        return model
    else:
        print("无解")
        return None

def analyze_constraints(constraints):
    """分析约束条件"""
    x = Int('x')
    s = Solver()
    
    for c in constraints:
        s.add(c(x))
    
    if s.check() == sat:
        return s.model()
    return None

if __name__ == '__main__':
    result = demo_z3_solver()
    
    # 更复杂的示例
    constraints = [
        lambda x: x > 5,
        lambda x: x < 20,
        lambda x: x % 3 == 0
    ]
    model = analyze_constraints(constraints)
    if model:
        print(f"高级约束解: {model}")
