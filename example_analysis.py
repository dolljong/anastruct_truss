"""
트러스 구조 해석 예제

이 스크립트는 생성된 트러스 모델에 하중을 적용하고 구조 해석을 수행하는 예제입니다.
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from truss_model import create_truss_model

# 트러스 모델 생성
print("트러스 모델 생성 중...")
ss = create_truss_model()

# 하중 적용
print("\n하중 조건 설정 중...")
# 상현재의 모든 격점에 등분포 하중 적용 (예: 눈하중 또는 지붕 하중)
# 각 격점에 100kN 하향 하중
load_magnitude = -100  # kN (하향)

for node_id, node in ss.node_map.items():
    # 상현재 노드에만 하중 적용 (y = 12m)
    if abs(node.vertex.y - 12) < 0.01:
        ss.point_load(node_id=node_id, Fy=load_magnitude)
        print(f"  Node {node_id} ({node.vertex.x:.1f}, {node.vertex.y:.1f}): {load_magnitude} kN")

# 구조 해석 수행
print("\n구조 해석 수행 중...")
ss.solve()
print("구조 해석 완료!")

# 결과 출력
print("\n" + "="*60)
print("해석 결과")
print("="*60)

# 반력 계산
print("\n지점 반력:")
for node_id, node in ss.node_map.items():
    # 좌표로 지점 확인
    if abs(node.vertex.x) < 0.01 and abs(node.vertex.y) < 0.01:
        # 시작점 힌지
        Rx = node.Fx if hasattr(node, 'Fx') else 0
        Ry = node.Fy if hasattr(node, 'Fy') else 0
        print(f"  힌지 지점 (Node {node_id}, 0.0m, 0.0m): Rx = {Rx:.2f} kN, Ry = {Ry:.2f} kN")
    elif abs(node.vertex.x - 48) < 0.01 and abs(node.vertex.y) < 0.01:
        # 끝점 롤러
        Ry = node.Fy if hasattr(node, 'Fy') else 0
        print(f"  롤러 지점 (Node {node_id}, 48.0m, 0.0m): Ry = {Ry:.2f} kN")

# 최대 변위 찾기
max_displacement = 0
max_disp_node = None
for node_id, node in ss.node_map.items():
    ux = node.ux if hasattr(node, 'ux') and node.ux is not None else 0
    uy = node.uy if hasattr(node, 'uy') and node.uy is not None else 0
    displacement = (ux**2 + uy**2)**0.5
    if displacement > max_displacement:
        max_displacement = displacement
        max_disp_node = node_id

if max_disp_node:
    node = ss.node_map[max_disp_node]
    print(f"\n최대 변위:")
    print(f"  Node {max_disp_node} ({node.vertex.x:.1f}, {node.vertex.y:.1f})")
    print(f"  변위 크기: {max_displacement:.6f} m = {max_displacement*1000:.2f} mm")

# 최대 축력 찾기
max_axial = 0
max_axial_element = None
for element_id, element in ss.element_map.items():
    if hasattr(element, 'N') and element.N is not None:
        axial = abs(element.N)
        if axial > max_axial:
            max_axial = axial
            max_axial_element = element_id

if max_axial_element:
    element = ss.element_map[max_axial_element]
    print(f"\n최대 축력:")
    print(f"  Element {max_axial_element}")
    print(f"  축력: {element.N:.2f} kN")
    if element.N > 0:
        print(f"  (인장)")
    else:
        print(f"  (압축)")

print("="*60)

# 결과 시각화
print("\n결과 시각화 저장 중...")

try:
    # 변위도
    fig = ss.show_displacement(show=False, figsize=(16, 8), verbosity=1)
    if fig is not None:
        plt.savefig('truss_displacement.png', dpi=300, bbox_inches='tight')
        print("  - 변위도: truss_displacement.png")
    
    # 축력도
    fig = ss.show_axial_force(show=False, figsize=(16, 8), verbosity=1)
    if fig is not None:
        plt.savefig('truss_axial_force.png', dpi=300, bbox_inches='tight')
        print("  - 축력도: truss_axial_force.png")
    
    # 전단력도
    fig = ss.show_shear_force(show=False, figsize=(16, 8), verbosity=1)
    if fig is not None:
        plt.savefig('truss_shear_force.png', dpi=300, bbox_inches='tight')
        print("  - 전단력도: truss_shear_force.png")
    
    # 휨모멘트도
    fig = ss.show_bending_moment(show=False, figsize=(16, 8), verbosity=1)
    if fig is not None:
        plt.savefig('truss_bending_moment.png', dpi=300, bbox_inches='tight')
        print("  - 휨모멘트도: truss_bending_moment.png")
    
    # 반력도
    fig = ss.show_reaction_force(show=False, figsize=(16, 8), verbosity=1)
    if fig is not None:
        plt.savefig('truss_reaction_force.png', dpi=300, bbox_inches='tight')
        print("  - 반력도: truss_reaction_force.png")
    
    print("\n모든 결과 이미지가 저장되었습니다!")
    
except Exception as e:
    print(f"시각화 중 오류 발생: {e}")

plt.close('all')
