from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path
from typing import Any

CONFIG_FILE = Path(__file__).with_name("ssh_to_pi_config.json")
DEFAULT_CONFIG = {
    "host": "192.168.0.192", #樹梅派
    "user": "ziv",
    "port": 22,
    "extra_args": "",
}


def load_config() -> dict[str, Any]:
    if not CONFIG_FILE.exists():
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG.copy()

    with CONFIG_FILE.open("r", encoding="utf-8") as handle:
        config = json.load(handle)

    merged = DEFAULT_CONFIG.copy()
    merged.update(config)
    return merged


def save_config(config: dict[str, Any]) -> None:
    with CONFIG_FILE.open("w", encoding="utf-8") as handle:
        json.dump(config, handle, indent=2, ensure_ascii=False)


def build_ssh_command(config: dict[str, Any]) -> list[str]:
    cmd = ["ssh"]
    if config.get("port"):
        cmd.extend(["-p", str(config["port"])])
    if config.get("extra_args"):
        cmd.extend(config["extra_args"].split())
    cmd.append(f"{config['user']}@{config['host']}")
    return cmd


def main() -> int:
    parser = argparse.ArgumentParser(
        description="SSH 連線到樹莓派，並可儲存或更新目標 IP/帳號設定。",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--host", help="樹莓派 IP 或主機名稱")
    parser.add_argument("--user", help="SSH 登入帳號")
    parser.add_argument("--port", type=int, help="SSH 連接埠")
    parser.add_argument(
        "--extra-args",
        help="傳遞給 ssh 的其他參數，例如 -i key.pem",
    )
    parser.add_argument(
        "--set",
        action="store_true",
        help="儲存並更新配置後結束，不立即連線。",
    )
    parser.add_argument(
        "--show",
        action="store_true",
        help="顯示目前的 SSH 配置並結束。",
    )
    args = parser.parse_args()

    config = load_config()
    updated = False

    if args.host:
        config["host"] = args.host
        updated = True
    if args.user:
        config["user"] = args.user
        updated = True
    if args.port is not None:
        config["port"] = args.port
        updated = True
    if args.extra_args is not None:
        config["extra_args"] = args.extra_args
        updated = True

    if args.show:
        print("目前 SSH 設定:")
        print(f"  host: {config['host']}")
        print(f"  user: {config['user']}")
        print(f"  port: {config['port']}")
        print(f"  extra_args: {config['extra_args']}")
        return 0

    if args.set:
        if updated:
            save_config(config)
            print("已更新並儲存 SSH 設定。")
        else:
            print("未提供任何更新的參數，請加上 --host, --user, --port 或 --extra-args。")
            return 1
        return 0

    if updated:
        save_config(config)
        print("已更新 SSH 設定，接著開始連線。")

    print("==========================================")
    print("準備連線到樹莓派終端機")
    print(f"目標 IP: {config['host']}")
    print(f"帳號: {config['user']}")
    print("提示: 稍後若詢問密碼，請輸入對應帳號密碼")
    print("==========================================")
    print()

    cmd = build_ssh_command(config)
    return subprocess.run(cmd).returncode


if __name__ == "__main__":
    raise SystemExit(main())
