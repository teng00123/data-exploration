"""
角色 ID 常量定义
================
所有角色鉴权逻辑统一引用此模块，禁止在业务代码中直接使用裸数字。

角色层级（从高到低）：
  SUPER_ADMIN  超级管理员    — 平台最高权限
  PROV_ADMIN   省级管理员    — 省级数据管理
  CITY_ADMIN   市级管理员    — 市级数据管理
  DIST_ADMIN   区县管理员    — 区县数据管理
  NORMAL_USER  普通用户      — 仅可访问授权资源

常量组（用于 role_id in <group> 判断）：
  ADMIN_ROLES        超级 + 省级 + 市级，拥有完整数据操作权限
  ALL_MGMT_ROLES     超级 + 省级 + 市级 + 区县，拥有管理视图权限
"""

# ── 单角色 ID ────────────────────────────────────────────────
SUPER_ADMIN: int = 1
PROV_ADMIN:  int = 1855189077904728066
CITY_ADMIN:  int = 1855189303667335169
DIST_ADMIN:  int = 1855188956748062721
NORMAL_USER: int = 1855188843279556609

# ── 角色组（frozenset 性能优于 tuple，支持 in 运算）──────────
# 超级 + 省级 + 市级：完整增删改查权限
ADMIN_ROLES: frozenset = frozenset({SUPER_ADMIN, PROV_ADMIN, CITY_ADMIN})

# 超级 + 省级 + 市级 + 区县：管理视图（含区县只读）
ALL_MGMT_ROLES: frozenset = frozenset({SUPER_ADMIN, PROV_ADMIN, CITY_ADMIN, DIST_ADMIN})

# 仅普通用户：只能访问被授权的资源
READONLY_ROLES: frozenset = frozenset({NORMAL_USER})
