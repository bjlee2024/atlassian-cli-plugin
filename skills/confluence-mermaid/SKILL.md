# Confluence Mermaid Diagram Best Practices

Confluence 페이지에 Mermaid 다이어그램을 삽입할 때 `vfcVisualizeMermaid` 매크로를 사용하는 베스트프랙티스 가이드.

## Triggers
- `mermaid`
- `다이어그램`
- `diagram`
- `confluence mermaid`
- `confluence diagram`

## Instructions

### vfcVisualizeMermaid 매크로 템플릿

Confluence storage format에서 Mermaid 다이어그램을 삽입하려면 다음 매크로를 사용하세요:

```xml
<ac:structured-macro ac:name="vfcVisualizeMermaid" ac:schema-version="1" data-layout="default">
  <ac:parameter ac:name="display-options">{:hh false, :e "content", :rf "mermaid", :scl nil, :vk nil}</ac:parameter>
  <ac:plain-text-body><![CDATA[
flowchart LR
    A["시작"] --> B["처리"]
    B --> C["완료"]
  ]]></ac:plain-text-body>
</ac:structured-macro>
```

### 지원 다이어그램 타입

| 타입 | 선언 | 용도 |
|------|------|------|
| Flowchart | `flowchart LR` / `flowchart TD` | 프로세스 흐름, 의사결정 |
| Sequence | `sequenceDiagram` | API 호출, 시스템 간 통신 |
| State | `stateDiagram-v2` | 상태 전이, 라이프사이클 |
| Gantt | `gantt` | 일정, 타임라인 |
| Class | `classDiagram` | 클래스 구조, 관계 |
| ER | `erDiagram` | 데이터 모델, 엔티티 관계 |
| Mindmap | `mindmap` | 브레인스토밍, 개념 정리 |

### Mermaid 코드 작성 규칙

1. **노드 텍스트에 `"` 사용 필수** (특수문자, 한글 포함 시):
   ```
   A["한글 텍스트"]
   B["특수문자: (괄호)"]
   ```

2. **줄바꿈은 `<br/>` 사용**:
   ```
   A["첫째 줄<br/>둘째 줄"]
   ```

3. **Subgraph 활용** (그룹핑):
   ```
   subgraph "서비스 A"
       A1["모듈 1"]
       A2["모듈 2"]
   end
   ```

4. **한글 텍스트 안전 사용**:
   - 반드시 `"` 따옴표로 감싸기
   - 노드 ID는 영문/숫자 사용 (예: `A1`, `svcA`)
   - 라벨에만 한글 사용: `svcA["서비스 A"]`

5. **Edge 라벨**:
   ```
   A -->|"요청"| B
   B -->|"응답"| A
   ```

### 전체 예시: 마이크로서비스 아키텍처

```xml
<ac:structured-macro ac:name="vfcVisualizeMermaid" ac:schema-version="1" data-layout="default">
  <ac:parameter ac:name="display-options">{:hh false, :e "content", :rf "mermaid", :scl nil, :vk nil}</ac:parameter>
  <ac:plain-text-body><![CDATA[
flowchart LR
    subgraph "클라이언트"
        WEB["웹 앱"]
        MOB["모바일 앱"]
    end

    subgraph "API Gateway"
        GW["API Gateway"]
    end

    subgraph "서비스"
        AUTH["인증 서비스"]
        USER["사용자 서비스"]
        ORDER["주문 서비스"]
    end

    subgraph "데이터"
        DB1[("PostgreSQL")]
        DB2[("Redis")]
    end

    WEB -->|"REST"| GW
    MOB -->|"REST"| GW
    GW -->|"인증"| AUTH
    GW -->|"사용자"| USER
    GW -->|"주문"| ORDER
    AUTH --> DB2
    USER --> DB1
    ORDER --> DB1
  ]]></ac:plain-text-body>
</ac:structured-macro>
```

### 검증 워크플로우

Mermaid 다이어그램을 Confluence 페이지에 적용할 때 다음 단계를 따르세요:

1. **Mermaid 문법 검증**: 코드 작성 후 문법 오류가 없는지 확인
   - 모든 노드 ID가 유효한지 (영문/숫자)
   - 따옴표가 올바르게 닫혀 있는지
   - 화살표 구문이 정확한지 (`-->`, `-->|"label"|`)

2. **매크로 래핑**: 검증된 Mermaid 코드를 `vfcVisualizeMermaid` 매크로로 래핑

3. **페이지 업데이트**: `atlassian-cli confluence page update` 명령으로 페이지 업데이트

4. **렌더링 확인**: 업데이트 후 페이지를 조회하여 매크로가 정상 로드되는지 확인
   ```bash
   atlassian-cli confluence page get <PAGE_ID> --format json
   ```
   - storage body에 `ac:structured-macro` 태그가 올바르게 포함되어 있는지 확인

### 주의사항

- `CDATA` 블록 안에서 `]]>` 문자열을 사용하지 마세요 (CDATA 종료로 인식됨)
- 매크로의 `display-options` 파라미터는 기본값을 유지하세요
- 복잡한 다이어그램은 여러 개의 작은 다이어그램으로 분리하는 것을 권장
- Confluence Cloud와 Data Center에서 `vfcVisualizeMermaid` 플러그인이 설치되어 있어야 렌더링됨
