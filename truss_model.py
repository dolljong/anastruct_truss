"""
트러스 구조물 모델링 스크립트

조건:
1. 전체 길이: 48m, 격점 간격: 6m, 총 8개 bay
2. 트러스 높이: 12m
3. 모든 격점에서 상현재와 하현재를 연결하는 수직재 존재
4. 사재는 중앙 하현재 격점에서 바로 전 상현재 격점으로 시작하여,
   이전 하현재 격점에서 이전 상현재 격점으로 반복 연결 (우측 대칭)
5. 지점 조건: 하현재 시작점 힌지, 끝점 롤러
6. 부재: 0.8x0.8m 두께 20mm 강재 각관
"""

from anastruct import SystemElements

def create_truss_model():
    """트러스 모델을 생성하고 반환합니다."""
    
    # 트러스 시스템 생성
    ss = SystemElements()
    
    # 파라미터 설정
    total_length = 48  # 전체 길이 (m)
    bay_spacing = 6    # 격점 간격 (m)
    num_bays = 8       # bay 개수
    height = 12        # 트러스 높이 (m)
    
    # 상현재와 하현재의 노드 좌표 생성
    # 하현재 (bottom chord): y = 0
    # 상현재 (top chord): y = height
    bottom_nodes = [(i * bay_spacing, 0) for i in range(num_bays + 1)]
    top_nodes = [(i * bay_spacing, height) for i in range(num_bays + 1)]
    
    # 1. 하현재 부재 생성 (bottom chord)
    for i in range(num_bays):
        ss.add_element(location=[bottom_nodes[i], bottom_nodes[i + 1]])
    
    # 2. 상현재 부재 생성 (top chord)
    for i in range(num_bays):
        ss.add_element(location=[top_nodes[i], top_nodes[i + 1]])
    
    # 3. 수직재 생성 (vertical members)
    # 모든 격점에서 상현재와 하현재를 연결
    for i in range(num_bays + 1):
        ss.add_element(location=[bottom_nodes[i], top_nodes[i]])
    
    # 4. 사재 생성 (diagonal members)
    # 중앙 하현재 격점에서 바로 전 상현재 격점으로 시작하여
    # 이전 하현재 격점에서 이전 상현재 격점으로 반복 연결
    # 중앙 격점은 인덱스 4 (0부터 8까지 중 4번째)
    center_index = num_bays // 2  # 4
    
    # 좌측 사재: 중앙에서 좌측으로 이전 격점 간 연결
    # center_index(4) → top(3), bottom(3) → top(2), bottom(2) → top(1), bottom(1) → top(0)
    for i in range(center_index):
        bottom_idx = center_index - i
        top_idx = center_index - i - 1
        ss.add_element(location=[bottom_nodes[bottom_idx], top_nodes[top_idx]])
    
    # 우측 사재: 중앙을 기준으로 대칭
    # center_index(4) → top(5), bottom(5) → top(6), bottom(6) → top(7), bottom(7) → top(8)
    for i in range(center_index):
        bottom_idx = center_index + i
        top_idx = center_index + i + 1
        ss.add_element(location=[bottom_nodes[bottom_idx], top_nodes[top_idx]])
    
    # 5. 지점 조건 설정
    # 노드 ID 찾기: 하현재 시작점(0,0)과 끝점(48,0)
    node_id_start = None
    node_id_end = None
    
    for node_id, node in ss.node_map.items():
        if abs(node.vertex.x) < 0.01 and abs(node.vertex.y) < 0.01:
            # 시작점 (0, 0)
            node_id_start = node_id
        elif abs(node.vertex.x - total_length) < 0.01 and abs(node.vertex.y) < 0.01:
            # 끝점 (48, 0)
            node_id_end = node_id
    
    if node_id_start is not None:
        # 하현재 시작점: 힌지 지점
        ss.add_support_hinged(node_id=node_id_start)
    
    if node_id_end is not None:
        # 하현재 끝점: 롤러 지점 (수평 방향만 구속 해제)
        ss.add_support_roll(node_id=node_id_end, direction=2)
    
    # 6. 부재 속성 설정
    # 0.8x0.8m 두께 20mm 강재 각관
    # EA (축강성) 및 EI (휨강성) 계산
    # 강재 탄성계수: E = 210 GPa = 210 × 10^9 Pa = 210 × 10^6 kN/m²
    
    E = 210e6  # kN/m²
    
    # 각관 단면 특성 계산
    b = 0.8  # 외부 폭 (m)
    t = 0.02  # 두께 (m)
    b_inner = b - 2 * t  # 내부 폭 (m)
    
    # 단면적 (A)
    A_outer = b * b
    A_inner = b_inner * b_inner
    A = A_outer - A_inner  # m²
    
    # 2차 모멘트 (I)
    I_outer = (b ** 4) / 12
    I_inner = (b_inner ** 4) / 12
    I = I_outer - I_inner  # m⁴
    
    # EA와 EI 설정
    EA = E * A  # kN
    EI = E * I  # kNm²
    
    # 모든 부재에 속성 적용
    for element_id in range(1, ss.id_last_element + 1):
        ss.element_map[element_id].EA = EA
        ss.element_map[element_id].EI = EI
    
    # 모델 정보 출력
    print("=" * 60)
    print("트러스 모델이 생성되었습니다.")
    print("=" * 60)
    print(f"총 길이: {total_length}m")
    print(f"높이: {height}m")
    print(f"Bay 수: {num_bays}개")
    print(f"격점 간격: {bay_spacing}m")
    print(f"총 부재 수: {ss.id_last_element}")
    print(f"\n부재 단면 특성:")
    print(f"  - 단면 형태: 각관 (Hollow Steel Section)")
    print(f"  - 외부 치수: {b}m × {b}m")
    print(f"  - 두께: {t}m ({t*1000}mm)")
    print(f"  - 단면적(A): {A:.6f} m²")
    print(f"  - 2차 모멘트(I): {I:.6e} m⁴")
    print(f"  - 탄성계수(E): {E:.2e} kN/m²")
    print(f"  - 축강성(EA): {EA:.2e} kN")
    print(f"  - 휨강성(EI): {EI:.2e} kNm²")
    print(f"\n지점 조건:")
    print(f"  - 시작점 (0, 0): 힌지 지점 (node_id={node_id_start})")
    print(f"  - 끝점 ({total_length}, 0): 롤러 지점 (node_id={node_id_end})")
    print("=" * 60)
    
    return ss

if __name__ == "__main__":
    # 트러스 모델 생성
    ss = create_truss_model()
    
    # 구조물 시각화 (matplotlib가 사용 가능한 환경에서만 작동)
    try:
        ss.show_structure()
    except Exception as e:
        print(f"\n참고: 구조물 시각화 중 오류 발생 (GUI 환경이 필요할 수 있음)")
        print(f"오류 내용: {e}")
        print("\n모델은 정상적으로 생성되었으며, 'ss' 객체를 통해 접근할 수 있습니다.")
