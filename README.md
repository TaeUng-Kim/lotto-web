# 로또 번호 공방

1회부터 쌓인 로또 6/45 당첨번호의 누적 빈도와 최근 흐름을 보고, 고른 번호로 5게임을 만드는 모바일용 웹 페이지.

## 구성

| 파일 | 역할 |
|---|---|
| `index.html` | 페이지 전체 (HTML/CSS/JS 한 파일, 빌드 없음) |
| `draws.json` | 1회~최신 회차 당첨번호 `[회차, 날짜, n1..n6, 보너스]` |
| `update_data.py` | 당첨번호를 받아 `draws.json` 갱신 (표준 라이브러리만 사용) |
| `.github/workflows/update-draws.yml` | 매주 일요일 0시(KST) 자동 갱신, 9시 재시도 |

## 로컬에서 보기

```bash
python -m http.server 8765
```

브라우저에서 http://localhost:8765 를 연다. `index.html`을 파일로 바로 열면 `draws.json`을 읽지 못한다.

## 배포 (Cloudflare Pages)

- 빌드 명령: 없음
- 출력 디렉터리: `/`
- 자동 갱신 커밋이 push되면 Cloudflare가 다시 배포한다.

과거 빈도는 다음 회차 확률을 바꾸지 않는다. 재미로 쓰는 도구다.
