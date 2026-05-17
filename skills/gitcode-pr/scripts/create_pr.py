#!/usr/bin/env python3
"""
使用 GitCode API v5 创建 Pull Request

使用方法:
    python3 create_pr.py --title "PR标题" --head "feature/xxx" --base "main"

注意:
    head 参数：同仓库直接用分支名，如 "feature/xxx"
    跨仓库(fork)才用 "username:branch" 格式
"""

import requests
import sys
import os
import argparse


def load_env_file(env_path="~/.gitcode_env"):
    """从文件加载环境变量"""
    env_path = os.path.expanduser(env_path)
    if not os.path.exists(env_path):
        return {}

    env_vars = {}
    with open(env_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                if '=' in line:
                    key, value = line.split('=', 1)
                    env_vars[key.strip()] = value.strip().strip('"').strip("'")
    return env_vars


def load_pr_template(template_path=None):
    """加载 PR 模板"""
    if template_path is None:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        template_path = os.path.join(script_dir, '..', 'assets', 'pr_template.md')

    if os.path.exists(template_path):
        with open(template_path, 'r', encoding='utf-8') as f:
            return f.read()
    return None


def create_pull_request(
    owner,
    repo,
    title,
    head,
    base,
    token,
    body=None,
    issue=None,
    description=None,
):
    """
    创建 Pull Request

    Args:
        owner: 仓库所有者
        repo: 仓库名称
        title: PR 标题
        head: 源分支名（同仓库直接写分支名，如 "feature/xxx"）
        base: 目标分支
        token: GitCode 访问令牌
        body: PR 描述完整内容
        issue: 关联的 issue 编号 (如: "7")
        description: PR 描述摘要 (用于填充模板)

    Returns:
        PR 信息字典，失败返回 None
    """

    base_url = "https://gitcode.com/api/v5"

    # 处理 body
    if body is None:
        if issue and description:
            template = load_pr_template()
            if template:
                body = template.replace('{{issue}}', issue).replace('{{description}}', description)
        else:
            body = ""

    pr_data = {
        "title": title,
        "head": head,
        "base": base,
        "body": body
    }

    print("正在创建 Pull Request...")
    print("目标仓库: {}/{}".format(owner, repo))
    print("源分支: {}".format(head))
    print("目标分支: {}".format(base))
    print("-" * 50)

    headers = {
        'Authorization': 'Bearer {}'.format(token),
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    try:
        url = "{}/repos/{}/{}/pulls".format(base_url, owner, repo)
        response = requests.post(url, headers=headers, json=pr_data, timeout=30)

        if response.status_code in [200, 201]:
            result = response.json()
            print("✅ Pull Request 创建成功！")
            print("PR 编号: #{}".format(result.get('number', result.get('iid', '未知'))))
            print("PR 链接: {}".format(result.get('web_url', result.get('html_url', '获取失败'))))
            print("状态: {}".format(result.get('state', '未知')))
            return result
        else:
            print("❌ 创建失败，状态码: {}".format(response.status_code))
            print("响应内容: {}".format(response.text[:300]))
            return None

    except requests.exceptions.RequestException as e:
        print("❌ 请求异常: {}".format(e))
        return None


def main():
    """主函数"""
    env_vars = load_env_file()
    token = env_vars.get('GITCODE_TOKEN', '')

    parser = argparse.ArgumentParser(description='使用 GitCode API v5 创建 Pull Request')
    parser.add_argument('--owner', default='Timmoc', help='仓库所有者 (默认: Timmoc)')
    parser.add_argument('--repo', default='tdchat_flutter', help='仓库名称 (默认: tdchat_flutter)')
    parser.add_argument('--title', required=True, help='PR 标题')
    parser.add_argument('--head', required=True, help='源分支名 (同仓库直接写分支名，如 feature/xxx)')
    parser.add_argument('--base', default='main', help='目标分支 (默认: main)')
    parser.add_argument('--body', help='PR 描述完整内容')
    parser.add_argument('--issue', help='关联的 issue 编号 (如: 7)')
    parser.add_argument('--description', help='PR 描述摘要')
    parser.add_argument('--token', default=token, help='GitCode 访问令牌')

    args = parser.parse_args()

    if not args.token:
        print("❌ 错误: 未找到 GitCode Token")
        print("请设置环境变量 GITCODE_TOKEN 或提供 --token 参数")
        sys.exit(1)

    result = create_pull_request(
        owner=args.owner,
        repo=args.repo,
        title=args.title,
        head=args.head,
        base=args.base,
        body=args.body,
        issue=args.issue,
        description=args.description or "",
        token=args.token
    )

    if result:
        print("\n" + "=" * 50)
        print("下一步建议：")
        print("1. 检查 PR 状态和评论")
        print("2. 准备好回复审查者可能提出的问题")
        sys.exit(0)
    else:
        print("\n请检查错误信息并根据提示进行调整")
        sys.exit(1)


if __name__ == "__main__":
    main()
