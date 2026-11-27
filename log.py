#!/usr/bin/env python3
"""log.py —— 100天转型日志小工具（纯标准库，Termux 直接跑）

用法：
    python log.py "今天干了啥"              # 追加一行到 README 日志
    python log.py "干了啥" --tag 交付        # 带个标签，好看
    python log.py --checkin                  # 吐出打卡模板，填完复制走
    python log.py --git "commit message"     # add+commit+push 一条龙
    python log.py --show                     # 看最近 5 条日志
"""
import subprocess, sys, datetime, re, os

README = "README.md"
TODAY  = datetime.date.today().isoformat()          # 2026-11-27
DAY_NO = (datetime.date.today() - datetime.date(2026, 11, 22)).days + 1

def append_log(text, tag=""):
    """在 README 的 '## 日志' 段落末尾追加一行。没有该段落就追加到文件尾。"""
    line = f"- Day {DAY_NO}（{TODAY}）" + (f"【{tag}】" if tag else "") + f" {text}\n"

    if not os.path.exists(README):
        open(README, "w", encoding="utf-8").write("# 我的编程转型 100 天\n\n## 日志\n")

    src = open(README, encoding="utf-8").read()
    if "## 日志" in src:
        # 在 "## 日志" 之后、下一个 "## " 之前插入（没有下一个就插到末尾）
        head, tail = src.split("## 日志", 1)
        nxt = tail.find("\n## ")
        if nxt == -1:
            src = head + "## 日志" + tail.rstrip("\n") + "\n" + line
        else:
            src = head + "## 日志" + tail[:nxt] + line + tail[nxt:]
    else:
        src = src.rstrip("\n") + "\n\n## 日志\n" + line

    open(README, "w", encoding="utf-8").write(src)
    print(f"✅ 已写入 Day {DAY_NO}：{text}")

def show_log(n=5):
    src = open(README, encoding="utf-8").read() if os.path.exists(README) else ""
    lines = [l for l in src.splitlines() if l.startswith("- Day ")]
    print(f"\n—— 最近 {n} 条 ——")
    for l in lines[-n:]:
        print(l)
    print(f"共 {len(lines)} 条\n")

def checkin_template():
    """吐出打卡模板。已推送的 commit 自动填进最后一栏，省得你手敲。"""
    try:
        last = subprocess.check_output(
            ["git", "log", "--oneline", "-1"], text=True).strip()
    except Exception:
        last = "（还没 commit）"
    print(f"""
【Day {DAY_NO} 打卡 · {TODAY}】
今天干了：__________________________
产物链接：__________________________（GitHub / EdgeOne / 截图）
卡住的地方：________________________（贴报错原文，没有写"无"）
明天第一件事：______________________
commit：{last}
""".strip())

def git_snap(msg):
    """add → commit → push。任何一步炸了都把原文打出来，不吞异常。"""
    for cmd in (["git", "add", "-A"],
                ["git", "commit", "-m", f"day{DAY_NO}: {msg}"],
                ["git", "push"]):
        print("$", " ".join(cmd))
        r = subprocess.run(cmd, capture_output=True, text=True)
        print(r.stdout.rstrip() or r.stderr.rstrip())
        if r.returncode != 0 and "nothing to commit" not in r.stdout + r.stderr:
            print("⛔ 中断，把上面红色/报错原文贴给教练"); break

# ---------- 入口 ----------
if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        print(__doc__); sys.exit(0)
    if args[0] == "--show":
        show_log(int(args[1]) if len(args) > 1 else 5)
    elif args[0] == "--checkin":
        checkin_template()
    elif args[0] == "--git":
        git_snap(" ".join(args[1:]) or "update")
    else:
        tag = ""
        if "--tag" in args:
            i = args.index("--tag"); tag = args[i+1]; del args[i:i+2]
        text = " ".join(args).strip()
        if not text:
            print("⚠️  说点啥再按回车，例：python log.py 跑通csv读取 --tag 交付"); sys.exit(1)
        append_log(text, tag)

