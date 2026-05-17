---
name: gitcode-pr
description: |
  创建/查看 GitCode PR。触发词：创建PR、提PR、查看PR、PR评论
---

# GitCode PR 技能

## 配置
```bash
source ~/.gitcode_env
```

## API 端点（v5，Bearer 认证）

| 功能 | 方法 | 端点 |
|------|------|--------|
| 创建 PR | POST | `/repos/{owner}/{repo}/pulls` |
| 查看 PR | GET | `/repos/{owner}/{repo}/pulls/{number}` |
| PR 列表 | GET | `/repos/{owner}/{repo}/pulls?state=open` |
| PR 评论 | GET | `/repos/{owner}/{repo}/pulls/{number}/comments` |
| 创建评论 | POST | `/repos/{owner}/{repo}/pulls/{number}/comments` |
| PR 文件变更 | GET | `/repos/{owner}/{repo}/pulls/{number}/files` |

Base URL：`https://gitcode.com/api/v5`
认证头：`Authorization: Bearer $GITCODE_TOKEN`

## 完整流程：创建分支 → 提交 → Push → 创建 PR

```bash
# 1. 确保在主分支并更新
git checkout main && git pull origin main

# 2. 创建功能分支
git checkout -b feature/xxx

# 3. 修改代码并提交
git add .
git commit -m "feat: 描述(#issue_id)"

# 4. Push 到远程
git push origin feature/xxx

# 5. 创建 PR（head 直接用分支名，不要加 username: 前缀）
source ~/.gitcode_env
curl -s -X POST \
  -H "Authorization: Bearer $GITCODE_TOKEN" \
  -H "Content-Type: application/json" \
  "https://gitcode.com/api/v5/repos/Timmoc/tdchat_flutter/pulls" \
  -d '{
    "title": "feat: 添加新功能(#1)",
    "head": "feature/xxx",
    "base": "main",
    "body": "## 描述\n\nCloses #1"
  }' | jq '{number, title, web_url, state}'
```

## PR 标题规范（Conventional Commits）

```
<type>: <描述>(#issue_id)
```

| type | 说明 |
|------|------|
| feat | 新功能 |
| fix | Bug 修复 |
| docs | 文档 |
| refactor | 重构 |
| perf | 性能优化 |

## 常用命令

### 查看 PR 详情
```bash
curl -s -H "Authorization: Bearer $GITCODE_TOKEN" \
  "https://gitcode.com/api/v5/repos/Timmoc/tdchat_flutter/pulls/9" \
  | jq '{number, title, state, web_url}'
```

### 添加 PR 评论
```bash
# 普通评论
curl -s -X POST \
  -H "Authorization: Bearer $GITCODE_TOKEN" \
  -H "Content-Type: application/json" \
  "https://gitcode.com/api/v5/repos/Timmoc/tdchat_flutter/pulls/9/comments" \
  -d '{"body":"评论内容"}'

# 行内评论（指定文件和行号）
curl -s -X POST \
  -H "Authorization: Bearer $GITCODE_TOKEN" \
  -H "Content-Type: application/json" \
  "https://gitcode.com/api/v5/repos/Timmoc/tdchat_flutter/pulls/9/comments" \
  -d '{"body":"建议优化","path":"lib/main.dart","line":42,"side":"RIGHT"}'
```

## 注意事项

- **head 参数**：同仓库 PR 直接用分支名（如 `"feature/xxx"`），只有跨仓库（fork）才用 `"username:branch"` 格式
- **PR URL**：GitCode 的 MR 页面路径是 `/merge_requests/{number}`，不是 `/pull/`
- **权限**：Developer 可以创建/评论 PR，但无法删除 PR 或 Issue
- **v4 API**：`/api/v4/` 在 `gitcode.com` 下被 WAF 拦截，统一用 `/api/v5/`
