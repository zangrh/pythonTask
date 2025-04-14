# 银行家算法

def is_safe_state(processes, available, maximum, allocation):
    """检查系统是否处于安全状态

    Args:
        processes (_type_): 进程数量
        available (_type_): 可用资源向量
        maximum (_type_): 最大需求矩阵
        allocation (_type_): 分配矩阵
        return: 如果系统处于安全状态，返回 True 和安全序列；否则返回 False 和 None
    """
    
    # 初始化
    n_processes = len(processes)
    n_resourses = len(available)
    
    # 计算需求矩阵（need = maximum - allocation）
    need  = [[maximum[i][j] - allocation[i][j] for j in range(n_resourses)] for i in range(n_processes)]
    
    finish = [False] * n_processes  # 完成标志数组
    safe_sequence = []  # 安全序列
    work = available[:]  # 工作向量，初始化为可用资源
    
    # 寻找安全序列
    while len(safe_sequence) < n_processes:
        found = False
        for i in range(n_processes):
            if not finish[i] and all(need[i][j] <= work[j] for j in range(n_resourses)):
                work = [work[j] + allocation[i][j] for j in range(n_resourses)]  # 释放资源
                finish[i] = True
                safe_sequence.append(i)
                found = True
                
            if not found:
                return False, None
            
        return True, safe_sequence
    
def request_resources(process_id, request, processes, available, maximum, allocation):
    """处理资源请求

    Args:
        process_id (_type_):请求资源的进程id
        request (_type_): 请求的资源向量
        processes (_type_): 进程列表
        available (_type_): 可用资源向量
        maximum (_type_): 最大需求矩阵
        allocation (_type_): 分配矩阵
        return: 如果请求可以被满足且系统仍处于安全状态，返回 True；否则返回 False
    """
    n_resources = len(available)
    
    # 检查请求是否超过最大需求
    if any(request[j] > maximum[process_id][j] for j in range(n_resources)):
        print("错误：请求的资源超过最大需求！")
        return False
    
    # 检查请求是否超过当前可用资源
    if any(request[j] > available[j] for j in range(n_resources)):
        print("错误：请求的资源超过可用资源！")
        return False
    
    # 尝试分配资源
    available = [available[j] - request[j] for j in range(n_resources)]
    allocation[process_id] = [allocation[process_id][j] + request[j] for j in range(n_resources)]
    
    # 检查系统是否处于安全状态
    is_safe, _ = is_safe_state(processes, available, maximum, allocation)
    
    if is_safe:
        print("请求已批准，系统处于安全状态。")
        return True
    else:
        available = [available[j] + request[j] for j in range(n_resources)]
        allocation[process_id] = [allocation[process_id][j] - request[j] for j in range(n_resources)]
        print("请求被拒绝，系统将进入不安全状态！")
        return False


# 示例
if __name__ == "__main__":
    # 进程数量和资源类型数量
    processes = [0, 1, 2]
    available = [9, 12, 7]  # 可用资源向量
    maximum = [
        [3, 5, 3],  # P0 的最大需求
        [3, 2, 2],  # P1 的最大需求
        [5, 0, 2]   # P2 的最大需求
    ]
    allocation = [
        [0, 1, 0],  # P0 当前分配
        [0, 0, 0],  # P1 当前分配
        [1, 0, 2]   # P2 当前分配
    ]

    # 检查初始状态是否安全
    is_safe, safe_sequence = is_safe_state(processes, available, maximum, allocation)
    if is_safe:
        print(f"系统处于安全状态，安全序列为: {safe_sequence}")
    else:
        print("系统处于不安全状态！")

    # 处理资源请求
    process_id = 1
    request = [1, 0, 3]
    request_resources(process_id, request, processes, available, maximum, allocation)