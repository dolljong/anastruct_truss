"# anastruct_truss

트러스 구조물 모델링 프로젝트

이 프로젝트는 `anastruct` 라이브러리를 사용하여 48m × 12m 트러스 구조물을 모델링하고 구조 해석을 수행하는 Python 코드를 제공합니다.

## 프로젝트 구성

- **truss_model.py**: 트러스 구조 모델 생성
- **visualize_truss.py**: 구조물 시각화
- **example_analysis.py**: 하중 적용 및 구조 해석 예제
- **README_TRUSS.md**: 상세 문서

## 빠른 시작

### 설치

```bash
pip install anastruct matplotlib
```

### 사용법

1. 트러스 모델 생성:
```bash
python truss_model.py
```

2. 구조물 시각화:
```bash
python visualize_truss.py
```

3. 구조 해석 예제 실행:
```bash
python example_analysis.py
```

이 명령은 트러스 구조에 하중을 적용하고 구조 해석을 수행하여 다음 결과를 생성합니다:
- 변위도 (truss_displacement.png)
- 축력도 (truss_axial_force.png)
- 전단력도 (truss_shear_force.png)
- 휨모멘트도 (truss_bending_moment.png)
- 반력도 (truss_reaction_force.png)

## 트러스 사양

- 전체 길이: 48m (8 bays × 6m)
- 높이: 12m
- 부재: 0.8×0.8m 두께 20mm 강재 각관
- 총 33개 부재 (상현재 8개, 하현재 8개, 수직재 9개, 사재 8개)
- 사재 배치: Pratt 트러스 형태 (중앙에서 시작하여 순차적으로 이전 격점 연결, 좌우 대칭)
- 지점: 좌측 힌지, 우측 롤러

자세한 내용은 [README_TRUSS.md](README_TRUSS.md)를 참조하세요." 
