import requests, json, re, os

session = requests.session()
# 配置用户名（一般是邮箱）
email = os.environ.get('EMAIL')
# 配置用户名对应的密码 和上面的email对应上
passwd = os.environ.get('PASSWD')
# server酱
SCKEY = os.environ.get('SCKEY')
# PUSHPLUS
Token = os.environ.get('TOKEN')
def push(content):
    if SCKEY != '1':
        url = "https://sctapi.ftqq.com/{}.send?title={}&desp={}".format(SCKEY, 'ikuuu签到', content)
        requests.post(url)
        print('推送完成')
    elif Token != '1':
        headers = {'Content-Type': 'application/json'}
        json = {"token": Token, 'title': 'ikuuu签到', 'content': content, "template": "json"}
        resp = requests.post(f'http://www.pushplus.plus/send', json=json, headers=headers).json()
        print('push+推送成功' if resp['code'] == 200 else 'push+推送失败')
    else:
        print('未使用消息推送推送！')

# 会不定时更新域名，记得Sync fork

login_url = 'https://ikuuu.pw/auth/login'
check_url = 'https://ikuuu.pw/user/checkin'
info_url = 'https://ikuuu.pw/user/profile'
user_url = 'https://ikuuu.pw/user'

header = {
        'origin': 'https://ikuuu.pw',
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
}
data = {
        'email': email,
        'passwd': passwd
}
try:
    content = ''
    print('进行登录...')
    response = json.loads(session.post(url=login_url,headers=header,data=data).text)
    print(response['msg'])
    # 获取账号名称
    # info_html = session.get(url=info_url,headers=header).text
#     info = "".join(re.findall('<span class="user-name text-bold-600">(.*?)</span>', info_html, re.S))
#     print(info)
    # 获取账号信息
    user_html = session.get(url=user_url,headers=header).text
    # 匹配会员时长
    membership_duration_match = re.search(r'<h4>会员时长</h4>\s*</div>\s*<div class="card-body">\s*([\u4e00-\u9fa5]+ \([\u4e00-\u9fa5]+\))', user_html)
    if membership_duration_match:
        membership_duration = membership_duration_match.group(1)
        content =  content + f"会员时长: {membership_duration}" + "\n\n"
    
    # 匹配永久 (免费版)
    permanent_free_match = re.search(r'<div class="card-body">\s*([\u4e00-\u9fa5]+ \([\u4e00-\u9fa5]+\))', user_html)
    if permanent_free_match:
        permanent_free = permanent_free_match.group(1)
        content =  content + f"永久 (免费版): {permanent_free}"+ "\n\n"
    
    # 匹配免费版: 永久
    free_version_match = re.search(r'免费版:\s*([\u4e00-\u9fa5]+)', user_html)
    if free_version_match:
        free_version = free_version_match.group(1)
        content =  content + f"免费版: {free_version}"+ "\n\n"
    
    
    # 匹配剩余流量的值和单位
    remaining_traffic_match = re.search(r'<span class="counter">([\d.]+)</span>\s*([A-Z]+)', user_html)
    if remaining_traffic_match:
        remaining_traffic_value = remaining_traffic_match.group(1)
        remaining_traffic_unit = remaining_traffic_match.group(2)
        content =  content + f"剩余流量: {remaining_traffic_value} {remaining_traffic_unit}"+ "\n\n"
    
    # 匹配今日已用的流量
    today_used_match = re.search(r'今日已用\s*:\s*([\dA-Z]+)', user_html)
    if today_used_match:
        today_used = today_used_match.group(1)
        content =  content + f"今日已用: {today_used}"+ "\n\n"
    
    # 匹配在线设备数和设备总数
    device_count_match = re.search(r'<span class="counter">(\d+)</span>\s*/\s*<span class="counterup">(\d+)</span>', user_html)
    if device_count_match:
        online_devices = device_count_match.group(1)
        total_devices = device_count_match.group(2)
        content =  content + f"在线设备数: {online_devices} / {total_devices}"+ "\n\n"
    
    # 匹配上次使用时间
    last_used_time_match = re.search(r'上次使用时间\s*:\s*([\d-]+\s*[\d:]+)', user_html)
    if last_used_time_match:
        last_used_time = last_used_time_match.group(1)
        content =  content + f"上次使用时间: {last_used_time}"+ "\n\n"
    
    
    # 匹配钱包余额
    wallet_balance_match = re.search(r'钱包余额.*?¥\s*<span class="counter">([\d.]+)</span>', user_html, re.S)
    if wallet_balance_match:
        wallet_balance = wallet_balance_match.group(1)
        content =  content + f"钱包余额: ¥{wallet_balance}"+ "\n\n"
    
    # 匹配累计获得返利金额
    rebate_amount_match = re.search(r'累计获得返利金额:\s*¥([\d.]+)', user_html)
    if rebate_amount_match:
        rebate_amount = rebate_amount_match.group(1)
        content =  content + f"累计获得返利金额: ¥{rebate_amount}"+ "\n\n"
    
    # 进行签到
    result = json.loads(session.post(url=check_url,headers=header).text)
    print(result['msg'])
    content = content + '签到结果：'+result['msg']+ "\n"
    # 进行推送
    push(content)
except:
    content = '签到失败'
    print(content)
    push(content)
