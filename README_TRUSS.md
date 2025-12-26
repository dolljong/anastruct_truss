# 트러스 구조물 모델링

이 프로젝트는 `anastruct` 라이브러리를 사용하여 트러스 구조물을 모델링하는 Python 코드를 제공합니다.

## 구조물 사양

### 기하학적 특성
- **전체 길이**: 48m
- **격점 간격**: 6m
- **Bay 개수**: 8개
- **트러스 높이**: 12m

### 부재 구성
1. **하현재 (Bottom Chord)**: 8개 부재
2. **상현재 (Top Chord)**: 8개 부재
3. **수직재 (Vertical Members)**: 9개 부재 (모든 격점에서 상현재와 하현재 연결)
4. **사재 (Diagonal Members)**: 8개 부재
   - 중앙 하현재 격점에서 바로 전 상현재 격점으로 시작
   - 이전 하현재 격점에서 이전 상현재 격점으로 반복 연결
   - 중앙을 기준으로 좌우 대칭 배치

**총 부재 수**: 33개

### 단면 특성
- **단면 형태**: 각관 (Hollow Steel Section)
- **외부 치수**: 0.8m × 0.8m
- **두께**: 20mm (0.02m)
- **재료**: 강재 (Steel)
- **탄성계수**: 210 GPa (210 × 10⁶ kN/m²)

### 계산된 단면 특성
- **단면적 (A)**: 0.0624 m²
- **2차 모멘트 (I)**: 6.33 × 10⁻³ m⁴
- **축강성 (EA)**: 1.31 × 10⁷ kN
- **휨강성 (EI)**: 1.33 × 10⁶ kNm²

### 지점 조건
- **좌측 지점 (0, 0)**: 힌지 지점 (Hinged Support) - 수평, 수직 이동 구속
- **우측 지점 (48, 0)**: 롤러 지점 (Roller Support) - 수직 이동만 구속

## 파일 구성

- `truss_model.py`: 트러스 모델 생성 메인 스크립트
- `visualize_truss.py`: 트러스 구조 시각화 및 이미지 저장 스크립트
- `truss_structure.png`: 생성된 트러스 구조 시각화 이미지

## 설치 방법

필요한 패키지를 설치합니다:

```bash
pip install anastruct matplotlib
```

## 사용 방법

### 1. 트러스 모델 생성

```bash
python truss_model.py
```

이 명령은 트러스 모델을 생성하고 구조물의 상세 정보를 출력합니다.

### 2. 트러스 구조 시각화

```bash
python visualize_truss.py
```

이 명령은 트러스 구조를 시각화하여 `truss_structure.png` 파일로 저장합니다.

### 3. 구조 해석 예제

```bash
python example_analysis.py
```

이 명령은 트러스 구조에 상현재 각 격점에 100kN 하향 하중을 적용하고 구조 해석을 수행합니다.
해석 결과는 다음 파일로 저장됩니다:
- `truss_displacement.png`: 변위도
- `truss_axial_force.png`: 축력도
- `truss_shear_force.png`: 전단력도 (NEW)
- `truss_bending_moment.png`: 휨모멘트도
- `truss_reaction_force.png`: 반력도

### 4. Python 코드에서 사용

```python
from truss_model import create_truss_model

# 트러스 모델 생성
ss = create_truss_model()

# 생성된 SystemElements 객체로 추가 작업 수행 가능
# 예: 하중 추가, 해석 수행 등
```

## 트러스 모델 세부 정보

### 노드 구성
- **하현재 노드**: 9개 (x좌표: 0, 6, 12, 18, 24, 30, 36, 42, 48m, y좌표: 0m)
- **상현재 노드**: 9개 (x좌표: 0, 6, 12, 18, 24, 30, 36, 42, 48m, y좌표: 12m)

### 사재 연결 패턴
사재는 Pratt 트러스 형태로 배치됩니다:

**좌측 사재**:
- 하현재 (24m, 0) → 상현재 (18m, 12m)
- 하현재 (18m, 0) → 상현재 (12m, 12m)
- 하현재 (12m, 0) → 상현재 (6m, 12m)
- 하현재 (6m, 0) → 상현재 (0m, 12m)

**우측 사재** (좌측과 대칭):
- 하현재 (24m, 0) → 상현재 (30m, 12m)
- 하현재 (30m, 0) → 상현재 (36m, 12m)
- 하현재 (36m, 0) → 상현재 (42m, 12m)
- 하현재 (42m, 0) → 상현재 (48m, 12m)

이 패턴은 중앙 격점에서 시작하여 이전 격점으로 순차적으로 연결되며,
모든 사재가 동일한 각도를 유지하면서 좌우 대칭을 이룹니다.

## 추가 분석

생성된 `SystemElements` 객체를 사용하여 다음과 같은 추가 분석을 수행할 수 있습니다:

```python
from truss_model import create_truss_model

ss = create_truss_model()

# 하중 추가 (예: 상현재 중앙에 집중 하중)
ss.point_load(node_id=14, Fy=-100)  # 100kN 하향 하중

# 구조 해석 수행
ss.solve()

# 결과 확인
ss.show_displacement()  # 변위 표시
ss.show_axial_force()  # 축력 표시
ss.show_shear_force()  # 전단력 표시
ss.show_bending_moment()  # 휨모멘트 표시
ss.show_reaction_force()  # 반력 표시
```

## 라이선스

이 프로젝트는 교육 및 연구 목적으로 제작되었습니다.

## 참고

- anastruct 문서: https://anastruct.readthedocs.io/
