# 安全说明

## ⚠️ 重要：已泄露密钥必须立即轮换

历史 Git 提交中 `backend/config.yaml` 包含明文密钥。即使该文件已从版本控制中移除，
**历史 commit 中的密钥已经泄露，必须立即作废并轮换。**

### 需要立即轮换的凭证

| 凭证 | 位置 | 操作 |
|------|------|------|
| 数据库密码 `123456` | `config.yaml → database.password` | 修改数据库用户密码 |
| Redis 密码 `xshl2023` | `config.yaml → redis.password` | 修改 Redis `requirepass` |
| OpenAI API Key `sk-6m5vyo0T9iZ3...` | `config.yaml → openai.api_key` | 在 OpenAI 控制台撤销并重新生成 |
| SECRET_KEY `Pd0MIJCX_4SOc...` | `config.yaml → SECRET_KEY` | 重新生成，所有现有 JWT 将失效 |
| Fernet Key `GHiC1UXbXbu3t...` | `backend/utils.py` | 重新生成，现有加密数据需重新加密 |
| JWT Secret `Xi_HpEd93wgZ5G...` | `app.py` | 已移除硬编码，使用环境变量 |
| 短信 AppKey `qfR0wpiQLMecI...` | `config.yaml → sms_config` | 联系短信服务商重置 |

### 从 Git 历史中彻底清除

> ⚠️ 以下操作会重写 Git 历史，需要所有协作者重新 clone 仓库。

#### 方法 1：BFG Repo Cleaner（推荐，更快）

```bash
# 下载 BFG
wget https://repo1.maven.org/maven2/com/madgag/bfg/1.14.0/bfg-1.14.0.jar

# 删除 config.yaml 的所有历史
java -jar bfg-1.14.0.jar --delete-files config.yaml --no-blob-protection your-repo.git

# 清理
cd your-repo
git reflog expire --expire=now --all
git gc --prune=now --aggressive
git push --force --all
```

#### 方法 2：git filter-branch

```bash
git filter-branch --force --index-filter \
  'git rm --cached --ignore-unmatch backend/config.yaml' \
  --prune-empty --tag-name-filter cat -- --all

git push --force --all
git push --force --tags
```

### 本地配置方式

```bash
# 1. 复制配置模板
cp backend/config.yaml.example backend/config.yaml
cp .env.example .env

# 2. 填入真实配置值（config.yaml 和 .env 均已加入 .gitignore）
vim backend/config.yaml
vim .env

# 3. 生成新的安全密钥
python -c "import secrets; print(secrets.token_urlsafe(32))"           # SECRET_KEY / JWT_SECRET_KEY
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"  # FERNET_KEY
```

### 环境变量优先级

所有敏感配置均支持**环境变量覆盖**，优先级：**环境变量 > config.yaml**。

生产环境建议完全通过环境变量注入，config.yaml 只保留非敏感的结构配置。
