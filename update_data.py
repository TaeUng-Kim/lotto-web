"""로또 6/45 당첨번호를 받아 draws.json 으로 저장한다.

매주 일요일 0시(KST) 예약 작업에서 실행한 뒤 Artifact 를 다시 게시한다.
출력 형식: {"updated": "...", "draws": [[회차, "YYYY-MM-DD", n1..n6, 보너스], ...],
           "latest": {"no": 최신 회차, "prizes": [[당첨자 수, 1인당 당첨금] | null, ...1~5등]}}
"""
import json
import sys
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

SOURCE = "https://smok95.github.io/lotto/results/all.json"
OUT = Path(__file__).with_name("draws.json")
KST = timezone(timedelta(hours=9))
FIRST_DRAW = datetime(2002, 12, 7, tzinfo=KST)


def expected_latest(now):
    """토요일 20:35 추첨 기준, 지금까지 끝났어야 하는 최신 회차."""
    last_sat = now - timedelta(days=(now.weekday() - 5) % 7)
    last_sat = last_sat.replace(hour=20, minute=35, second=0, microsecond=0)
    if last_sat > now:
        last_sat -= timedelta(days=7)
    return (last_sat.date() - FIRST_DRAW.date()).days // 7 + 1


def main():
    req = urllib.request.Request(SOURCE, headers={"User-Agent": "lotto-web-updater"})
    with urllib.request.urlopen(req, timeout=60) as r:
        raw = json.load(r)

    draws = []
    for x in sorted(raw, key=lambda x: x["draw_no"]):
        nums = sorted(x["numbers"])
        if len(nums) != 6 or not all(1 <= n <= 45 for n in nums + [x["bonus_no"]]):
            sys.exit(f"잘못된 데이터: {x['draw_no']}회")
        draws.append([x["draw_no"], x["date"][:10], *nums, x["bonus_no"]])

    if [d[0] for d in draws] != list(range(1, len(draws) + 1)):
        sys.exit("회차 번호가 연속되지 않습니다")

    # 최신 회차의 등수별 [당첨자 수, 1인당 당첨금]. 당첨자가 없는 등수는 null.
    last = max(raw, key=lambda x: x["draw_no"])
    prizes = [[d["winners"], d["prize"]] if d.get("winners") else None for d in last.get("divisions", [])[:5]]

    now = datetime.now(KST)
    OUT.write_text(json.dumps({"updated": now.isoformat(timespec="minutes"), "draws": draws,
                               "latest": {"no": last["draw_no"], "prizes": prizes}},
                              separators=(",", ":")), encoding="utf-8")

    latest, want = draws[-1][0], expected_latest(now)
    print(f"저장: {OUT} ({latest}회, {draws[-1][1]}: {draws[-1][2:8]} + {draws[-1][8]})")
    if latest < want:
        print(f"경고: 기대 최신 회차는 {want}회인데 데이터는 {latest}회까지입니다 (원본 갱신 지연)")
        sys.exit(2)


if __name__ == "__main__":
    main()
