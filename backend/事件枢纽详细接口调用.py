import requests
import time
import json
import hashlib
import os

# -------------------------- 基础配置（已优化关键参数） --------------------------
# 接口地址（保持不变）
API1_URL = "http://182.129.202.14:10023/pr-api/pai/event/data/receive/event/list"
API2_URL = "http://182.129.202.14:10023/pr-api/pai/event/data/receive/event/info"
API3_URL = "http://182.129.202.14:10023/pr-api/pai/event/data/receive/event/queryEventResult"
# 公共认证参数（确认与接口文档一致）
SYSTEM_CODE = "0325"
TOKEN = "b76e6ccb98af493895cda929b221ed88"
# 分页配置（修复“起始页>最大页数”问题，先从第1页测试）
PAGE_NUM_START = 1       # 起始页：从1开始，避免直接从250页导致无数据
MAX_TOTAL_PAGES = 1000     # 最大请求页数：保持10页，先验证少量数据
PAGE_SIZE = 100          # 每页条数：保持10条
REQUEST_INTERVAL = 1     # 请求间隔：避免高频请求被拦截
# 数据保存（确保路径可写，Windows路径双反斜杠）
SAVE_PATH = "F:\\sjsn"
DETAIL_SAVE_FILENAME = "event_detail_data.json"
FULL_SAVE_PATH = os.path.join(SAVE_PATH, DETAIL_SAVE_FILENAME)
# 关键：接口1返回的id字段名（若测试后发现是eventId等，直接修改这里）
ID_FIELD_NAME = "id"


# -------------------------- 工具函数（无修改，确保认证正确） --------------------------
def get_current_timestamp():
    """生成毫秒级时间戳（接口要求）"""
    return str(int(time.time() * 1000))

def generate_signature(timestamp, token):
    """SHA256签名规则：timestamp+token+timestamp（与原逻辑一致）"""
    sign_str = f"{timestamp}{token}{timestamp}"
    sha256 = hashlib.sha256()
    sha256.update(sign_str.encode("utf-8"))
    return sha256.hexdigest()

def get_headers():
    """生成通用请求头（接口1/2共用，减少重复代码）"""
    current_ts = get_current_timestamp()
    current_sign = generate_signature(current_ts, TOKEN)
    return {
        "system-code": SYSTEM_CODE,
        "system-signature": current_sign,
        "system-timestamp": current_ts
    }


# -------------------------- 步骤1：调用接口1获取id（重点优化调试与逻辑） --------------------------
def fetch_all_event_ids():
    all_ids = []
    page_num = PAGE_NUM_START  # 从配置的起始页开始
    print("="*50)
    print("=== 开始调用接口1：获取事件ID列表 ===")
    print(f"配置：起始页{page_num} | 最大页{MAX_TOTAL_PAGES} | 每页{PAGE_SIZE}条 | ID字段名{ID_FIELD_NAME}")
    print("="*50)

    while page_num <= MAX_TOTAL_PAGES:
        try:
            headers = get_headers()
            # 接口1请求参数：保留eventStatus=4，新增调试打印
            params = {
                "system-code": SYSTEM_CODE,
                "system-signature": headers["system-signature"],
                "system-timestamp": headers["system-timestamp"],
                "eventStatus": "4",  # 若后续发现此状态无数据，可注释此行
                "pageSize": PAGE_SIZE,
                "pageNum": page_num
            }

            # 1. 发送请求并打印关键调试信息
            print(f"\n【接口1】请求第{page_num}页 | 参数：{json.dumps(params, ensure_ascii=False)[:200]}")
            response = requests.get(API1_URL, params=params, headers=headers, timeout=15)
            response.raise_for_status()  # 触发HTTP错误（如404、500）
            result = response.json()
            print(f"【接口1】第{page_num}页响应 | 状态码：{response.status_code} | 返回code：{result.get('code')}")

            # 2. 处理正常响应（code=200）
            if result.get("code") == 200:
                data = result.get("data", {})
                current_page_records = data.get("rows", [])
                total_records = data.get("total", 0)
                total_pages_api = (total_records + PAGE_SIZE - 1) // PAGE_SIZE  # 接口返回的总页数

                # 打印接口返回的核心数据（便于排查无数据原因）
                print(f"【接口1】第{page_num}页数据 | 总行数：{len(current_page_records)} | 接口总数据：{total_records}条 | 接口总页数：{total_pages_api}页")
                if len(current_page_records) > 0:
                    print(f"【接口1】第1条数据示例：{json.dumps(current_page_records[0], ensure_ascii=False)[:300]}")

                # 3. 提取ID（兼容不同字段名，通过配置修改）
                current_page_ids = []
                for record in current_page_records:
                    event_id = record.get(ID_FIELD_NAME)
                    if event_id:
                        current_page_ids.append(event_id)
                        # 打印提取到的ID（确认是否正确）
                        print(f"【接口1】提取ID：{event_id}")

                all_ids.extend(current_page_ids)
                print(f"【接口1】第{page_num}页完成 | 本页ID数：{len(current_page_ids)} | 累计ID数：{len(all_ids)}")

                # 4. 判断是否需要继续请求（取“接口总页数”和“配置最大页”的最小值）
                stop_page = min(total_pages_api, MAX_TOTAL_PAGES)
                if page_num >= stop_page:
                    print(f"\n【接口1】请求终止：已达接口总页数{total_pages_api}页（或配置最大页{MAX_TOTAL_PAGES}页）")
                    break

                # 5. 分页递增与频率控制
                page_num += 1
                time.sleep(REQUEST_INTERVAL)

            # 3. 处理接口返回错误（code≠200）
            else:
                error_msg = result.get("msg", "未知错误")
                print(f"【接口1】第{page_num}页错误 | 返回信息：{error_msg}")
                # 错误时重试1次，仍失败则跳过当前页
                time.sleep(2)
                retry_response = requests.get(API1_URL, params=params, headers=headers, timeout=15)
                retry_result = retry_response.json()
                if retry_result.get("code") == 200:
                    print(f"【接口1】第{page_num}页重试成功")
                    continue
                else:
                    print(f"【接口1】第{page_num}页重试失败，跳过当前页")
                    page_num += 1
                    time.sleep(REQUEST_INTERVAL)

        # 4. 处理网络异常（如超时、连接失败）
        except requests.exceptions.RequestException as e:
            print(f"【接口1】第{page_num}页请求异常 | 错误：{str(e)}")
            print(f"【接口1】5秒后重试第{page_num}页...")
            time.sleep(5)
        # 5. 处理其他未知异常
        except Exception as e:
            print(f"【接口1】第{page_num}页处理异常 | 错误：{str(e)}")
            page_num += 1
            time.sleep(REQUEST_INTERVAL)

    # 最终结果汇总
    print("="*50)
    print(f"=== 接口1请求完成 | 累计获取有效ID数：{len(all_ids)} ===")
    print("="*50)
    return all_ids


# -------------------------- 步骤2：调用接口2获取详情（保留原逻辑，优化提示） --------------------------
def fetch_event_details_by_ids(event_ids):
    # 先判断是否有有效ID
    if not event_ids:
        print("\n" + "="*50)
        print("=== 调用接口2失败：无有效ID可请求 ===")
        print("="*50)
        return []

    all_detail_data = []
    total_ids = len(event_ids)
    print("\n" + "="*50)
    print(f"=== 开始调用接口2：获取{total_ids}个事件详情 ===")
    print("="*50)

    # 确保保存目录存在
    if not os.path.exists(SAVE_PATH):
        os.makedirs(SAVE_PATH)
        print(f"【接口2】创建保存目录：{SAVE_PATH}")

    # 逐个请求详情（便于定位单个ID问题）
    for idx, event_id in enumerate(event_ids, 1):
        try:
            headers = get_headers()
            # 接口2参数：核心是ID（与接口1的ID字段名一致）
            params = {
                "system-code": SYSTEM_CODE,
                "system-signature": headers["system-signature"],
                "system-timestamp": headers["system-timestamp"],
                ID_FIELD_NAME: event_id  # 用配置的ID字段名，确保与接口1一致
            }

            # 发送接口2请求
            print(f"\n【接口2】请求第{idx}/{total_ids}个 | ID：{event_id}")
            response = requests.get(API2_URL, params=params, headers=headers, timeout=15)
            response.raise_for_status()
            result = response.json()

            # 处理正常响应
            if result.get("code") == 200:
                detail_data = result.get("data", {})
                all_detail_data.append(detail_data)
                print(f"【接口2】第{idx}/{total_ids}个成功 | ID：{event_id} | 详情数据长度：{len(json.dumps(detail_data))}字符")

                # 实时保存（覆盖写入，避免中断丢失数据）
                with open(FULL_SAVE_PATH, "w", encoding="utf-8") as f:
                    json.dump(all_detail_data, f, ensure_ascii=False, indent=2)
                print(f"【接口2】已保存至：{FULL_SAVE_PATH} | 累计保存：{len(all_detail_data)}条")

            # 处理接口错误
            else:
                error_msg = result.get("msg", "未知错误")
                print(f"【接口2】第{idx}/{total_ids}个失败 | ID：{event_id} | 错误：{error_msg}")

            # 控制请求频率
            time.sleep(REQUEST_INTERVAL)

        # 处理网络异常
        except requests.exceptions.RequestException as e:
            print(f"【接口2】第{idx}/{total_ids}个异常 | ID：{event_id} | 错误：{str(e)}")
            time.sleep(2)
        # 处理其他异常
        except Exception as e:
            print(f"【接口2】第{idx}/{total_ids}个处理异常 | ID：{event_id} | 错误：{str(e)}")

    # 最终结果汇总
    print("\n" + "="*50)
    print(f"=== 接口2请求完成 | 成功获取：{len(all_detail_data)}条详情 | 保存路径：{FULL_SAVE_PATH} ===")
    print("="*50)
    return all_detail_data

# --------------------------调用接口3 获取部门信息 --------------------------------
def fetch_dept_info(event_ids):
    # 先判断是否有有效ID
    if not event_ids:
        print("\n" + "="*50)
        print("=== 调用接口3失败：无有效ID可请求 ===")
        print("="*50)
        return []

    all_detail_data = []
    total_ids = len(event_ids)
    print("\n" + "="*50)
    print(f"=== 开始调用接口3：获取{total_ids}个事件详情 ===")
    print("="*50)

    for idx, event_id in enumerate(event_ids, 1):
        try:
            headers = get_headers()
            # 接口2参数：核心是ID（与接口1的ID字段名一致）
            params = {
                "sourceSystemCode": SYSTEM_CODE,
                "eventNum": event_id,  # 用配置的ID字段名，确保与接口1一致
                "id": event_id  # 用配置的ID字段名，确保与接口1一致
            }

            # 发送接口2请求
            print(f"\n【接口3】请求第{idx}/{total_ids}个 | ID：{event_id}")
            response = requests.get(API2_URL, params=params, headers=headers, timeout=15)
            response.raise_for_status()
            result = response.json()
            print(result)
            # 处理正常响应
            if result.get("code") == 200:
                detail_data = result.get("data", {})
                all_detail_data.append(detail_data)
                print(f"【接口3】第{idx}/{total_ids}个成功 | ID：{event_id} | 详情数据长度：{len(json.dumps(detail_data))}字符")

                # # 实时保存（覆盖写入，避免中断丢失数据）
                # with open(FULL_SAVE_PATH, "w", encoding="utf-8") as f:
                #     json.dump(all_detail_data, f, ensure_ascii=False, indent=2)
                # print(f"【接口3】已保存至：{FULL_SAVE_PATH} | 累计保存：{len(all_detail_data)}条")

            # 处理接口错误
            else:
                error_msg = result.get("msg", "未知错误")
                print(f"【接口3】第{idx}/{total_ids}个失败 | ID：{event_id} | 错误：{error_msg}")

            # 控制请求频率
            time.sleep(REQUEST_INTERVAL)

        # 处理网络异常
        except requests.exceptions.RequestException as e:
            print(f"【接口3】第{idx}/{total_ids}个异常 | ID：{event_id} | 错误：{str(e)}")
            time.sleep(2)
        # 处理其他异常
        except Exception as e:
            print(f"【接口3】第{idx}/{total_ids}个处理异常 | ID：{event_id} | 错误：{str(e)}")

    # 最终结果汇总
    print("\n" + "="*50)
    print(f"=== 接口3请求完成 | 成功获取：{len(all_detail_data)}条详情 | 保存路径：{FULL_SAVE_PATH} ===")
    print("="*50)
    return all_detail_data

# -------------------------- 主流程：按顺序执行（无修改） --------------------------
if __name__ == "__main__":
    event_ids = ["1200323615709"]
    # # 步骤1：获取所有ID
    # event_ids = fetch_all_event_ids()
    # # 步骤2：根据ID获取详情并保存
    # fetch_all_event_ids()
    # fetch_event_details_by_ids(event_ids)
    # 步骤3： 根据ID获取部门信息
    fetch_dept_info(event_ids)