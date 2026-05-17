# GitCode Skills

AI Agent 专用 GitCode 集成技能，支持 Issue 和 PR 操作。

## 技能列表

### gitcode-issue

读取和创建 GitCode Issue。

| 功能 | 方法 | 端点 |
|------|------|------|
| 列出 issues | GET | `/repos/{owner}/{repo}/issues` |
| 查看单个 issue | GET | `/repos/{owner}/{repo}/issues/{number}` |
| 查看评论 | GET | `/repos/{owner}/{repo}/issues/{number}/comments` |
| 创建 issue | POST | `/repos/{owner}/{repo}/issues` |

### gitcode-pr

创建和管理 GitCode Pull Request。

| 功能 | 方法 | 端点 |
|------|------|------|
| 创建 PR | POST | `/repos/{owner}/{repo}/pulls` |
| 查看 PR | GET | `/repos/{owner}/{repo}/pulls/{number}` |
| PR 评论 | GET | `/repos/{owner}/{repo}/pulls/{number}/comments` |
| 创建评论 | POST | `/repos/{owner}/{repo}/pulls/{number}/comments` |

## API 规范

- Base URL：`https://gitcode.com/api/v5`
- 认证方式：`Authorization: Bearer $GITCODE_TOKEN`
- 环境变量配置：`~/.gitcode_env`

## 注意事项

- 同仓库 PR 的 `head` 参数直接用分支名，如 `"feature/xxx"`
- 跨仓库（fork）PR 用 `"username:branch"` 格式
- Developer 权限可以创建 Issue/PR/评论，无法删除或关闭他人的
- 不要使用 `/api/v4/`（被 WAF 拦截），统一用 `/api/v5/`
