---
name: gitcode-issue
description: |
  读取/创建 GitCode Issue。当用户提到 issue 时触发。
  触发词：查看issue、创建issue、issue详情、#编号
---

# GitCode Issue 技能

## 配置
Token 已保存在 `~/.gitcode_env`，每次使用前先加载：
```bash
source ~/.gitcode_env
```

## API 端点（v5，Bearer 认证）

| 功能 | 方法 | 端点 |
|------|------|--------|
| 列出 issues | GET | `/repos/{owner}/{repo}/issues?state=open` |
| 查看单个 issue | GET | `/repos/{owner}/{repo}/issues/{number}` |
| 查看评论 | GET | `/repos/{owner}/{repo}/issues/{number}/comments` |
| 创建 issue | POST | `/repos/{owner}/{repo}/issues` |

Base URL：`https://gitcode.com/api/v5`
认证头：`Authorization: Bearer $GITCODE_TOKEN`

## 常用命令

### 列出 open issues
```bash
curl -s -H "Authorization: Bearer $GITCODE_TOKEN" \
  "https://gitcode.com/api/v5/repos/Timmoc/tdchat_flutter/issues?state=open" \
  | jq '.[] | {number, title, state}'
```

### 查看单个 issue
```bash
curl -s -H "Authorization: Bearer $GITCODE_TOKEN" \
  "https://gitcode.com/api/v5/repos/Timmoc/tdchat_flutter/issues/1" \
  | jq '{number, title, state, body}'
```

### 创建 issue
```bash
curl -s -X POST \
  -H "Authorization: Bearer $GITCODE_TOKEN" \
  -H "Content-Type: application/json" \
  "https://gitcode.com/api/v5/repos/Timmoc/tdchat_flutter/issues" \
  -d '{"title":"标题","body":"描述内容"}'
```

## 注意事项
- 创建/修改操作需要仓库 Developer 以上权限
- Developer 权限**无法删除** issue（需要 Maintainer）
- 分页加 `?page=1&per_page=20`
