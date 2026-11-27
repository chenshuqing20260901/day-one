import random
random.seed(7)

n = 500
# A组：老结算页 10%付费
a_users = n
a_payers = sum(1 for _ in range(n) if random.random() < 0.10)
a_revenue = sum(random.randint(30,200) for _ in range(a_payers))

# B组：新结算页 13%付费
b_users = n
b_payers = sum(1 for _ in range(n) if random.random() < 0.13)
b_revenue = sum(random.randint(30,200) for _ in range(b_payers))

a_payrate = a_payers / a_users * 100
b_payrate = b_payers / b_users * 100
a_arpu = a_revenue / a_users
b_arpu = b_revenue / b_users

print(f"""
group | users | payers | revenue | pay_rate_% | ARPU
A     | {a_users:5d} | {a_payers:6d} | {a_revenue:7d} | {a_payrate:10.2f} | {a_arpu:.2f}
B     | {b_users:5d} | {b_payers:6d} | {b_revenue:7d} | {b_payrate:10.2f} | {b_arpu:.2f}
""")

lift = b_payrate - a_payrate
print(f"\nB vs A 转化率提升: {lift:+.2f} 个百分点")

# 卡方检验函数
def chi2_test(a_pay, a_no, b_pay, b_no):
    total = a_pay + a_no + b_pay + b_no
    row1 = a_pay + b_pay
    row2 = a_no + b_no
    col1 = a_pay + a_no
    col2 = b_pay + b_no
    e11 = row1 * col1 / total
    e12 = row1 * col2 / total
    e21 = row2 * col1 / total
    e22 = row2 * col2 / total
    chi2 = (a_pay-e11)**2/e11 + (b_pay-e12)**2/e12 + (a_no-e21)**2/e21 + (b_no-e22)**2/e22
    return chi2

a_not_pay = a_users - a_payers
b_not_pay = b_users - b_payers
chi_val = chi2_test(a_payers, a_not_pay, b_payers, b_not_pay)

print(f"\n卡方 χ² = {chi_val:.3f}，95%显著性阈值：3.84")

# 核心改动：由数据自动输出结论，不再写死文字
if chi_val > 3.84:
    print("✅ 结论：差异统计显著。有较高把握认为新版B真实提升转化率，不是随机波动。")
else:
    print("⚠️ 结论：差异不显著。当前样本下，无法排除这个差距只是随机运气，不建议直接全量上线。")

print("\n备注：95%置信标准只是业务常用参考，不是绝对标准；样本量越小，越容易被随机影响。")

