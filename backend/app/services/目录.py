from app.db import 连接
from app.modules import 偏差隔离升 as 域


def 总览() -> dict:
    conn = 连接()
    try:
        域.确保结构(conn)

        def c(sql: str) -> int:
            return conn.execute(sql).fetchone()[0]

        return {
            "开关版本": c("SELECT COUNT(*) FROM 开关版本"),
            "分桶规": c("SELECT COUNT(*) FROM 分桶规 WHERE 状态='生效'"),
            "下发票": c("SELECT COUNT(*) FROM 下发票"),
            "已下发": c("SELECT COUNT(*) FROM 下发票 WHERE 状态='已下发'"),
            "部分放量": c("SELECT COUNT(*) FROM 下发票 WHERE 状态='部分放量'"),
            "已放量": c("SELECT COUNT(*) FROM 下发票 WHERE 状态='已放量'"),
            "回读证": c("SELECT COUNT(*) FROM 回读证"),
            "确认回读": c("SELECT COUNT(*) FROM 回读证 WHERE 结果='确认'"),
            "偏差回读": c("SELECT COUNT(*) FROM 回读证 WHERE 结果='偏差'"),
            "隔离边缘": c("SELECT COUNT(*) FROM 隔离边缘 WHERE 状态='隔离中'"),
            "命运条": c("SELECT COUNT(*) FROM 命运账"),
            "最近贯验通过": bool(
                (conn.execute(
                    "SELECT 是否通过 FROM 轨贯验 ORDER BY 编号 DESC LIMIT 1"
                ).fetchone() or [0])[0]
            ),
        }
    finally:
        conn.close()
