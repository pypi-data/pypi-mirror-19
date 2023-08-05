# -*- coding: utf-8 -*-
REPORT_BANNER = """
╒══════════════════════════════════════════════════════════════════════════════╕
│                                                                              │
│                               /$$$$$$            /$$                         │
│                              /$$__  $$          | $$                         │
│           /$$$$$$$  /$$$$$$ | $$  \__//$$$$$$  /$$$$$$   /$$   /$$           │
│          /$$_____/ |____  $$| $$$$   /$$__  $$|_  $$_/  | $$  | $$           │
│         |  $$$$$$   /$$$$$$$| $$_/  | $$$$$$$$  | $$    | $$  | $$           │
│          \____  $$ /$$__  $$| $$    | $$_____/  | $$ /$$| $$  | $$           │
│          /$$$$$$$/|  $$$$$$$| $$    |  $$$$$$$  |  $$$$/|  $$$$$$$           │
│         |_______/  \_______/|__/     \_______/   \___/   \____  $$           │
│                                                          /$$  | $$           │
│                                                         |  $$$$$$/           │
│                                                          \______/            │
│                                                                              │
╞══════════════════════════════════════════════════════════════════════════════╡
""".strip()

TABLE_HEADING = """
╞══════════════════════════╤═══════════════╤═══════════════════╤═══════════════╡
│ package                  │ installed     │ affected          │ source        │
╞══════════════════════════╧═══════════════╧═══════════════════╧═══════════════╡
""".strip()

TABLE_FOOTER = """
╘══════════════════════════╧═══════════════╧═══════════════════╧═══════════════╛
""".strip()

TABLE_BREAK = """
╞══════════════════════════╡═══════════════╡═══════════════════╡═══════════════╡
""".strip()

REPORT_HEADING = """
│ REPORT                                                                       │
""".strip()

REPORT_SECTION = """
╞══════════════════════════════════════════════════════════════════════════════╡
""".strip()

REPORT_FOOTER = """
╘══════════════════════════════════════════════════════════════════════════════╛
""".strip()


def report(vulns, full=False):
    if vulns:
        table = []
        for vuln in vulns:
            table.append("│ {:24} │ {:13} │ {:17} │ {:13} │".format(
                vuln["name"][:24],
                vuln["version"][:13],
                ",".join(vuln["specs"])[:17],
                vuln["type"]
            ))
            if full:
                table.append(REPORT_SECTION)
                descr = vuln.description
                for chunk in [descr[i:i + 76] for i in range(0, len(descr), 76)]:
                    for line in chunk.splitlines():
                        table.append("│ {:76} │".format(line))
                table.append(REPORT_SECTION)
        table = "\n".join(table)
        return "\n".join([REPORT_BANNER, REPORT_HEADING, TABLE_HEADING, table, TABLE_FOOTER])
    else:
        report = "│ {:76} │".format("No known security vulnerabilities found.")
        return "\n".join([REPORT_BANNER, REPORT_HEADING, REPORT_SECTION, report, REPORT_FOOTER])
