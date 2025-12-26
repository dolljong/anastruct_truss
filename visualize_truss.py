"""
트러스 구조물 시각화 스크립트

이 스크립트는 truss_model.py에서 생성된 트러스 구조를 시각화하여 이미지 파일로 저장합니다.
"""

import matplotlib
matplotlib.use('Agg')  # GUI 없는 환경에서 사용
import matplotlib.pyplot as plt
from truss_model import create_truss_model

# 트러스 모델 생성
ss = create_truss_model()

# 구조물 시각화 및 저장
try:
    fig = ss.show_structure(show=False, figsize=(16, 8))
    if fig is not None:
        plt.savefig('truss_structure.png', dpi=300, bbox_inches='tight')
        print("\n구조물 이미지가 'truss_structure.png'로 저장되었습니다.")
    else:
        print("\n시각화 생성 실패")
except Exception as e:
    print(f"\n시각화 중 오류 발생: {e}")
    
    # 수동으로 구조물 그리기
    print("\n수동 시각화 시도 중...")
    fig, ax = plt.subplots(figsize=(16, 8))
    
    # 모든 부재 그리기
    for element_id, element in ss.element_map.items():
        x_coords = [element.vertex_1.x, element.vertex_2.x]
        y_coords = [element.vertex_1.y, element.vertex_2.y]
        ax.plot(x_coords, y_coords, 'b-', linewidth=2)
    
    # 노드 표시
    for node_id, node in ss.node_map.items():
        ax.plot(node.vertex.x, node.vertex.y, 'ro', markersize=6)
    
    # 지점 표시
    # 힌지 지점 (0, 0)
    ax.plot(0, 0, 'g^', markersize=15, label='Hinged Support')
    # 롤러 지점 (48, 0)
    ax.plot(48, 0, 'gs', markersize=15, label='Roller Support')
    
    ax.set_xlabel('X (m)', fontsize=12)
    ax.set_ylabel('Y (m)', fontsize=12)
    ax.set_title('트러스 구조물 (48m × 12m)', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.set_aspect('equal')
    ax.legend()
    
    plt.tight_layout()
    plt.savefig('truss_structure.png', dpi=300, bbox_inches='tight')
    print("구조물 이미지가 'truss_structure.png'로 저장되었습니다.")

plt.close()
