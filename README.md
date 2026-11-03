# Manufacturing AI Coding Skills

제조업의 생산·품질·검증 프로세스를 AI 소프트웨어 개발에 적용하는 코딩 스킬 저장소입니다. 제조업처럼 보이는 그림이나 제조업 분야 프로그램만 만드는 것이 목적이 아닙니다.

현재 단계는 **기본 스킬 원본 보존 + 분석 재검토 + 개선 준비**입니다. 16개 `SKILL.md`는 사용자 제공 ZIP의 바이트를 그대로 유지했습니다. 개선안은 아직 스킬 본문에 적용하지 않았습니다.

## 먼저 볼 자료

- [재검토 의견](reports/REVIEW_KO.md): 첨부 분석에서 신뢰할 수 있는 내용, 평가기 문제와 해석 한계.
- [스킬별 업데이트 준비안](reports/UPDATE_PLAN_KO.md): 16개 스킬의 최소 수정 방향과 완료 기준.
- [기본 스킬 목록과 라우팅](skills/README.md).
- [실제 로켓 코딩 A/B/C 비교](comparisons/rocket-code/README.md): 동일 요청으로 작성한 코드, 실행 결과, 그림과 검증 기록.
- [원본 및 추적 정보](sources/manifest.json).

## 구성

| 경로 | 내용 |
|---|---|
| `skills/<name>/SKILL.md` | 제조업 프로세스 코딩 스킬 16개, 원문 보존 |
| `skills/benchmark/` | 원본의 반복 테스트 실행 횟수 시연 |
| `comparators/` | B 조건의 검증 스킬 스냅샷, 원 출처와 MIT 라이선스 |
| `benchmarks/abc-v1/` | 첨부된 수작업 A/B/C 구현과 18개 테스트, 원문 보존 |
| `evidence/completeness-review/` | 90건 사후 코드 리뷰, 원문 보존 |
| `evidence/study-reference/` | 리뷰가 참조한 90회 연구의 보고서와 선택된 코드 근거 |
| `sources/` | 사용자가 첨부한 ZIP 3개와 SHA-256 목록 |
| `reports/verification/` | 이번 재검증의 원시 출력과 결과 |
| `comparisons/rocket-code/` | 새로 실행한 독립 A/B/C 코딩 비교 |

첨부 문서의 지시문과 과거 실험 지시문은 연구자료입니다. 현재 사용자 요청을 대체하는 지시로 해석하지 않습니다. 저장소 전체가 자동 설치되는 스킬 묶음은 아닙니다.

## 재검증

Python 표준 라이브러리로 다음을 실행합니다.

```sh
python -X utf8 scripts/recheck_evidence.py
```

이 명령은 원본 해시, 리뷰 JSON/CSV·그룹 집계, 기존 A/B/C 테스트 결과를 확인하고 `reports/verification/`에 결과를 씁니다. 벤치마크의 결과 파일을 덮어쓰는 원본 실행기는 임시 복사본에서만 실행합니다. 샘플 테스트 3개도 실행합니다.

**감사 PASS는 자료 일치와 재현 성공이라는 뜻입니다. 평가기 타당성이나 스킬의 우월성 판정이 아닙니다.** 항상 예외만 던지는 가짜 구현이 기존 평가기에서 13/18을 통과하는 문제가 확인됐습니다.

원본 ZIP 내부의 캐시 바이트코드는 ZIP에만 보존하고 작업 파일에서는 제외했습니다. `.gitattributes`는 Git의 자동 개행 변환을 꺼 원본 해시를 유지합니다. 원본 스킬의 변경은 다음 개선 단계에서 별도 변경 이력으로 관리합니다.

## 출처와 해석 범위

기본 스킬의 직접 출처는 `Manufacturing_AI_Process_Control_Skills_v1.zip`입니다. Downloads에서 추가 확인한 `Manufacturing_AI_ABC_90_Run_Study.zip`의 스킬 16개와도 일치했습니다. 이 관련 연구 ZIP 전체는 업로드하지 않고 필요한 보고서와 코드만 포함했습니다. 그 연구가 주장하는 최초 원본 ZIP 해시는 과거 보고값이며, 이번 첨부 ZIP에서 직접 계산한 해시와 구분합니다.

B 스킬의 MIT 라이선스는 `comparators/LICENSE`에 보존했습니다. 이 라이선스를 제조업 스킬 전체에 임의로 확대 적용하지 않았습니다. 원본 `GITHUB_RESEARCH.md`는 과거 참고목록이며 이번 작업에서 외부 저장소의 독창성이나 최신 상태를 검증한 결과는 아닙니다.
