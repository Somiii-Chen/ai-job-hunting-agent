#!/usr/bin/env python3
"""生成一封带附件、尚未发送的 .eml 邮件文件。

当 AI 没法直接控制 Mail.app 时用它（比如不是 Mac、AI 工具不能执行 AppleScript、
或者 Mail.app 里没加求职邮箱）。用户双击 .eml 打开后自己审核、发送：

  Apple Mail   双击打开后，菜单「邮件 → 再次发送」（Shift+Cmd+D），就变成可编辑的新邮件
  Outlook      双击直接以草稿打开（文件里带 X-Unsent: 1）
  Thunderbird  打开后选「编辑为新消息」

只用 Python 标准库，不需要安装任何东西。不会发送任何邮件。

用法:
  python3 make_eml.py --from "姓名 <you@example.com>" --to hr@company.com \\
      --subject "AI应用工程师 - 姓名" --body 正文.txt --attach 简历.pdf --out 01_公司_岗位.eml
"""
import argparse
import mimetypes
import os
import sys
from email import policy
from email.message import EmailMessage
from email.utils import formatdate, make_msgid


def main():
    p = argparse.ArgumentParser(description="生成未发送的 .eml 求职邮件")
    p.add_argument("--from", dest="sender", required=True, help='发件人，格式 "姓名 <邮箱>"')
    p.add_argument("--to", required=True, help="收件人邮箱")
    p.add_argument("--subject", required=True)
    p.add_argument("--body", required=True, help="正文文本文件（UTF-8）")
    p.add_argument("--attach", action="append", default=[], help="附件路径，可重复")
    p.add_argument("--out", required=True, help="输出的 .eml 路径")
    a = p.parse_args()

    for f in [a.body] + a.attach:
        if not os.path.isfile(f):
            sys.exit(f"文件不存在: {f}")

    msg = EmailMessage(policy=policy.SMTP)
    msg["From"] = a.sender
    msg["To"] = a.to
    msg["Subject"] = a.subject
    msg["Date"] = formatdate(localtime=True)
    msg["Message-ID"] = make_msgid()
    msg["X-Unsent"] = "1"  # Outlook 据此以草稿方式打开
    with open(a.body, encoding="utf-8") as fh:
        msg.set_content(fh.read())
    for f in a.attach:
        ctype, _ = mimetypes.guess_type(f)
        maintype, subtype = (ctype or "application/octet-stream").split("/", 1)
        with open(f, "rb") as fh:
            msg.add_attachment(fh.read(), maintype=maintype, subtype=subtype, filename=os.path.basename(f))

    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    with open(a.out, "wb") as fh:
        fh.write(msg.as_bytes())
    names = ", ".join(os.path.basename(f) for f in a.attach) or "无"
    print(f"已生成（未发送）: {a.out}\n  收件人: {a.to}\n  主题: {a.subject}\n  附件: {names}")


if __name__ == "__main__":
    main()
