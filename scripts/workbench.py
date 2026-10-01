#!/usr/bin/env python3
"""求职投递工作台（Excel）。

一个 .xlsx 文件，三个工作表：
  工作台    首页统计（总数、按状态、按投递方式），打开文件时自动计算
  投递记录  每个岗位一行：公司、城市、招聘类型、用哪份简历、投递状态（下拉）、匹配亮点、差距……
  选项      下拉菜单的取值

用 Excel、Numbers、WPS 都能打开。依赖 openpyxl（没有的话：pip3 install --user openpyxl）。

用法:
  python3 workbench.py init   <工作台.xlsx>
  python3 workbench.py add    <工作台.xlsx> '<JSON>'        # 字段名用下方 COLUMNS 里的中文列名
  python3 workbench.py update <工作台.xlsx> <公司> <岗位> '<JSON>'
  python3 workbench.py list   <工作台.xlsx> [投递状态]

例子:
  python3 workbench.py add 求职投递工作台.xlsx '{"公司":"某公司","岗位":"AI应用工程师","城市":"上海",
      "招聘类型":"社招","投递方式":"官网","优先级":"高","投递状态":"待投递","用哪份简历":"简历_技术版.pdf",
      "岗位链接":"https://...","匹配亮点":"...","差距":"..."}'
  python3 workbench.py update 求职投递工作台.xlsx 某公司 AI应用工程师 '{"投递状态":"已申请","投递时间":"2026-10-08"}'
"""
import json
import sys
from datetime import date, datetime

try:
    from openpyxl import Workbook, load_workbook
    from openpyxl.formatting.rule import FormulaRule
    from openpyxl.styles import Alignment, Font, PatternFill
    from openpyxl.worksheet.datavalidation import DataValidation
except ImportError:
    sys.exit("缺少 openpyxl。请先运行: pip3 install --user openpyxl")

RECORD_SHEET = "投递记录"
HOME_SHEET = "工作台"
OPTION_SHEET = "选项"
MAX_ROWS = 500

# (列名, 列宽)
COLUMNS = [
    ("序号", 6),
    ("公司", 16),
    ("部门/团队", 16),
    ("岗位", 28),
    ("城市", 10),
    ("招聘类型", 10),
    ("投递方式", 9),
    ("优先级", 7),
    ("投递状态", 12),
    ("用哪份简历", 26),
    ("招聘邮箱", 22),
    ("岗位链接", 30),
    ("匹配亮点", 40),
    ("差距", 32),
    ("发现日期", 11),
    ("投递时间", 16),
    ("截止时间", 11),
    ("下一步/待办", 30),
    ("备注", 30),
]
COL = {name: i + 1 for i, (name, _) in enumerate(COLUMNS)}

STATUSES = ["待投递", "草稿已建", "已申请", "简历筛选", "笔试/测评", "一面", "二面/终面",
            "Offer", "已拒绝/未通过", "已撤销", "不投"]
CLOSED = ["Offer", "已拒绝/未通过", "已撤销", "不投"]
OPTIONS = {
    "投递状态": STATUSES,
    "投递方式": ["邮件", "官网", "平台", "内推"],
    "招聘类型": ["社招", "校招", "应届", "实习", "管培"],
    "优先级": ["高", "中", "低"],
}

HEADER_FILL = PatternFill("solid", fgColor="1F4E79")
HEADER_FONT = Font(bold=True, color="FFFFFF")


def col_letter(n):
    s = ""
    while n:
        n, r = divmod(n - 1, 26)
        s = chr(65 + r) + s
    return s


def init(path):
    wb = Workbook()
    home = wb.active
    home.title = HOME_SHEET
    rec = wb.create_sheet(RECORD_SHEET)
    opt = wb.create_sheet(OPTION_SHEET)

    # 选项表
    for c, (name, values) in enumerate(OPTIONS.items(), start=1):
        opt.cell(1, c, name).font = Font(bold=True)
        for r, v in enumerate(values, start=2):
            opt.cell(r + 0, c, v)
        opt.column_dimensions[col_letter(c)].width = 14

    # 投递记录表头
    for name, width in COLUMNS:
        cell = rec.cell(1, COL[name], name)
        cell.fill, cell.font = HEADER_FILL, HEADER_FONT
        cell.alignment = Alignment(vertical="center")
        rec.column_dimensions[col_letter(COL[name])].width = width
    rec.freeze_panes = "E2"
    rec.auto_filter.ref = f"A1:{col_letter(len(COLUMNS))}{MAX_ROWS}"

    # 下拉菜单
    for c, name in enumerate(OPTIONS, start=1):
        n = len(OPTIONS[name])
        dv = DataValidation(type="list", formula1=f"={OPTION_SHEET}!${col_letter(c)}$2:${col_letter(c)}${n + 1}",
                            allow_blank=True)
        rec.add_data_validation(dv)
        L = col_letter(COL[name])
        dv.add(f"{L}2:{L}{MAX_ROWS}")

    # 状态颜色：已申请及之后的进行中为蓝，面试为绿，结束为灰
    s = col_letter(COL["投递状态"])
    rng = f"A2:{col_letter(len(COLUMNS))}{MAX_ROWS}"
    for cond, color in [
        (f'OR(${s}2="一面",${s}2="二面/终面",${s}2="Offer")', "E2EFDA"),
        (f'OR(${s}2="已拒绝/未通过",${s}2="已撤销",${s}2="不投")', "EDEDED"),
        (f'${s}2="草稿已建"', "FFF2CC"),
    ]:
        rec.conditional_formatting.add(rng, FormulaRule(formula=[cond], fill=PatternFill("solid", fgColor=color)))

    # 首页统计
    R = f"{RECORD_SHEET}!"
    D = col_letter(COL["岗位"])
    S = col_letter(COL["投递状态"])
    M = col_letter(COL["投递方式"])
    home["B2"] = "求职投递工作台"
    home["B2"].font = Font(bold=True, size=16)
    home["B3"] = "每投一个岗位，在「投递记录」加一行；投递状态用下拉选择；本页统计自动计算。"
    home["B5"], home["C5"] = "总岗位数", f"=COUNTA({R}{D}2:{D}{MAX_ROWS})"
    closed = "-".join(f'COUNTIF({R}{S}2:{S}{MAX_ROWS},"{x}")' for x in CLOSED)
    home["B6"], home["C6"] = "进行中", f"=C5-{closed}"
    home["B8"] = "按状态"
    home["B8"].font = Font(bold=True)
    for i, st in enumerate(STATUSES):
        home.cell(9 + i, 2, st)
        home.cell(9 + i, 3, f'=COUNTIF({R}{S}2:{S}{MAX_ROWS},"{st}")')
    row = 9 + len(STATUSES) + 1
    home.cell(row, 2, "按投递方式").font = Font(bold=True)
    for i, m in enumerate(OPTIONS["投递方式"]):
        home.cell(row + 1 + i, 2, m)
        home.cell(row + 1 + i, 3, f'=COUNTIF({R}{M}2:{M}{MAX_ROWS},"{m}")')
    home.column_dimensions["B"].width = 16
    home.column_dimensions["C"].width = 10
    for r in (5, 6):
        home.cell(r, 2).font = Font(bold=True)

    wb.save(path)
    print(f"已创建工作台: {path}")


def _rows(ws):
    for r in range(2, ws.max_row + 1):
        if ws.cell(r, COL["岗位"]).value:
            yield r


def _norm(s):
    return "".join(str(s or "").split()).lower()


def _write(ws, r, data):
    unknown = [k for k in data if k not in COL]
    if unknown:
        sys.exit(f"未知列名: {unknown}。可用列名: {[n for n, _ in COLUMNS]}")
    for k, v in data.items():
        if k == "序号":
            continue
        if k in OPTIONS and v not in (None, "") and v not in OPTIONS[k]:
            sys.exit(f"「{k}」只能填: {OPTIONS[k]}，收到: {v}")
        cell = ws.cell(r, COL[k], v)
        if k == "岗位链接" and v:
            cell.hyperlink = v
            cell.font = Font(color="0563C1", underline="single")
        if k in ("匹配亮点", "差距", "下一步/待办", "备注"):
            cell.alignment = Alignment(wrap_text=True, vertical="top")


def add(path, data):
    wb = load_workbook(path)
    ws = wb[RECORD_SHEET]
    for r in _rows(ws):
        if _norm(ws.cell(r, COL["公司"]).value) == _norm(data.get("公司")) and \
                _norm(ws.cell(r, COL["岗位"]).value) == _norm(data.get("岗位")):
            sys.exit(f"重复：第 {r} 行已有「{data.get('公司')} / {data.get('岗位')}」，未添加。要修改请用 update。")
    if not data.get("岗位") or not data.get("公司"):
        sys.exit("「公司」和「岗位」必填")
    r = max(list(_rows(ws)) or [1]) + 1
    data.setdefault("发现日期", date.today().isoformat())
    data.setdefault("投递状态", "待投递")
    ws.cell(r, COL["序号"], r - 1)
    _write(ws, r, data)
    wb.save(path)
    print(f"已添加第 {r} 行: {data['公司']} / {data['岗位']} / {data['投递状态']}")


def update(path, company, position, data):
    wb = load_workbook(path)
    ws = wb[RECORD_SHEET]
    hits = [r for r in _rows(ws)
            if _norm(company) in _norm(ws.cell(r, COL["公司"]).value)
            and _norm(position) in _norm(ws.cell(r, COL["岗位"]).value)]
    if len(hits) != 1:
        sys.exit(f"找到 {len(hits)} 行匹配「{company} / {position}」，需要正好 1 行。请把公司或岗位名写得更具体。")
    if data.get("投递状态") == "已申请" and "投递时间" not in data:
        data["投递时间"] = datetime.now().strftime("%Y-%m-%d %H:%M")
    _write(ws, hits[0], data)
    wb.save(path)
    print(f"已更新第 {hits[0]} 行: {data}")


def list_rows(path, status=None):
    ws = load_workbook(path)[RECORD_SHEET]
    n = 0
    for r in _rows(ws):
        st = ws.cell(r, COL["投递状态"]).value
        if status and st != status:
            continue
        n += 1
        g = lambda k: ws.cell(r, COL[k]).value or ""
        print(f"{g('序号')}. [{st}] {g('公司')} / {g('岗位')} / {g('城市')} / {g('招聘类型')} / "
              f"{g('投递方式')} / 简历: {g('用哪份简历')} / {g('岗位链接')}")
    print(f"共 {n} 行")


def main(argv):
    if len(argv) < 3:
        sys.exit(__doc__)
    cmd, path = argv[1], argv[2]
    if cmd == "init":
        init(path)
    elif cmd == "add" and len(argv) == 4:
        add(path, json.loads(argv[3]))
    elif cmd == "update" and len(argv) == 6:
        update(path, argv[3], argv[4], json.loads(argv[5]))
    elif cmd == "list":
        list_rows(path, argv[3] if len(argv) > 3 else None)
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main(sys.argv)
