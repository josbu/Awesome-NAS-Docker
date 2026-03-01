#!/usr/bin/env python3
"""
Split README.md into separate category files
"""
import re
from pathlib import Path

# Read original README
readme_path = Path("/home/node/.openclaw/workspace-agent05/Awesome-NAS-Docker/README.md")
with open(readme_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Define section mappings
sections = {
    "1.1 数据处理支持": {
        "file": "docs/ai-data-processing.md",
        "title": "1.1 数据处理支持"
    },
    "1.2 AI应用工具": {
        "file": "docs/ai-tools.md",
        "title": "1.2 AI 应用工具"
    },
    "1.3 部署与优化": {
        "file": "docs/ai-deployment.md",
        "title": "1.3 部署与优化"
    },
    "1.4 辅助开发工具": {
        "file": "docs/ai-devtools.md",
        "title": "1.4 辅助开发工具"
    },
    "2.1 开发环境": {
        "file": "docs/dev-environment.md",
        "title": "2.1 开发环境"
    },
    "2.2 自动化体系": {
        "file": "docs/dev-automation.md",
        "title": "2.2 自动化体系"
    },
    "2.3 镜像管理": {
        "file": "docs/dev-images.md",
        "title": "2.3 镜像管理"
    },
    "2.4 部署工具链": {
        "file": "docs/dev-toolchain.md",
        "title": "2.4 部署工具链"
    },
    "3.1 智能处理": {
        "file": "docs/data-processing.md",
        "title": "3.1 智能处理"
    },
    "3.2 分析与可视化": {
        "file": "docs/data-analytics.md",
        "title": "3.2 分析与可视化"
    },
    "3.3 协作与共享": {
        "file": "docs/data-collaboration.md",
        "title": "3.3 协作与共享"
    },
    "4.1 视频处理": {
        "file": "docs/media-video.md",
        "title": "4.1 视频处理"
    },
    "4.2 音频管理": {
        "file": "docs/media-audio.md",
        "title": "4.2 音频管理"
    },
    "4.3 传输协议": {
        "file": "docs/media-streaming.md",
        "title": "4.3 传输协议"
    },
    "4.4 图像处理": {
        "file": "docs/media-image.md",
        "title": "4.4 图像处理"
    },
    "4.5 流媒体服务": {
        "file": "docs/media-services.md",
        "title": "4.5 流媒体服务"
    },
    "5.1 自动化运维": {
        "file": "docs/ops-automation.md",
        "title": "5.1 自动化运维"
    },
    "5.2 资源监控": {
        "file": "docs/ops-monitoring.md",
        "title": "5.2 资源监控"
    },
    "5.3 网络治理": {
        "file": "docs/ops-network.md",
        "title": "5.3 网络治理"
    },
    "5.4 安全防护": {
        "file": "docs/ops-security.md",
        "title": "5.4 安全防护"
    },
    "5.5 日志体系": {
        "file": "docs/ops-logging.md",
        "title": "5.5 日志体系"
    },
    "6.1 通讯协同": {
        "file": "docs/collab-communication.md",
        "title": "6.1 通讯协同"
    },
    "6.2 客户管理": {
        "file": "docs/collab-crm.md",
        "title": "6.2 客户管理"
    },
    "6.3 文档协作": {
        "file": "docs/collab-docs.md",
        "title": "6.3 文档协作"
    },
    "6.4 项目管理": {
        "file": "docs/collab-project.md",
        "title": "6.4 项目管理"
    },
    "7.1 渗透测试": {
        "file": "docs/security-pentest.md",
        "title": "7.1 渗透测试"
    },
    "7.1 加密体系": {
        "file": "docs/security-encryption.md",
        "title": "7.2 加密体系"
    },
    "7.3 身份认证": {
        "file": "docs/security-auth.md",
        "title": "7.3 身份认证"
    },
    "7.4 数据保护": {
        "file": "docs/security-privacy.md",
        "title": "7.4 数据保护"
    },
    "8.1 家庭娱乐": {
        "file": "docs/home-entertainment.md",
        "title": "8.1 家庭娱乐"
    },
    "8.2 健康管理": {
        "file": "docs/home-health.md",
        "title": "8.2 健康管理"
    },
    "8.3 智能家居": {
        "file": "docs/home-smarthome.md",
        "title": "8.3 智能家居"
    },
    "8.4 生活服务": {
        "file": "docs/home-lifestyle.md",
        "title": "8.4 生活服务"
    },
    "9.1 文件处理": {
        "file": "docs/productivity-files.md",
        "title": "9.1 文件处理"
    },
    "9.2 信息聚合": {
        "file": "docs/productivity-aggregation.md",
        "title": "9.2 信息聚合"
    },
    "9.3 办公辅助": {
        "file": "docs/productivity-office.md",
        "title": "9.3 办公辅助"
    },
    "9.4 个人助手": {
        "file": "docs/productivity-assistant.md",
        "title": "9.4 个人助手"
    },
    "9.5 时间管理": {
        "file": "docs/productivity-time.md",
        "title": "9.5 时间管理"
    },
    "10.1 存储方案": {
        "file": "docs/infrastructure-storage.md",
        "title": "10.1 存储方案"
    },
    "10.2 网络服务": {
        "file": "docs/infrastructure-network.md",
        "title": "10.2 网络服务"
    },
    "10.3 消息体系": {
        "file": "docs/infrastructure-messaging.md",
        "title": "10.3 消息体系"
    },
}

# Find all section headers
lines = content.split('\n')
section_starts = {}

for i, line in enumerate(lines):
    for section_name in sections.keys():
        # Match both ### and #### headers
        if f"#### {section_name}" in line or f"### {section_name}" in line:
            section_starts[section_name] = i
            break

# Extract content for each section
for section_name, section_info in sections.items():
    if section_name not in section_starts:
        continue

    start_line = section_starts[section_name]

    # Find the next section
    end_line = len(lines)
    for other_section, other_line in section_starts.items():
        if other_line > start_line and other_line < end_line:
            end_line = other_line

    # Extract content
    section_content = lines[start_line:end_line]
    section_text = '\n'.join(section_content).strip()

    # Add header
    output = f"# {section_info['title']}\n\n"
    output += "[← 返回主页](../README.md)\n\n"
    output += "---\n\n"
    output += section_text

    # Write to file
    output_path = Path("/home/node/.openclaw/workspace-agent05/Awesome-NAS-Docker") / section_info['file']
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(output)

    print(f"Created: {section_info['file']}")

print("\n✅ All sections split successfully!")
