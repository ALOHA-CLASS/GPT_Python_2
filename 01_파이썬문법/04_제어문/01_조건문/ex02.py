# 다중 조건문
# - 위의 나온 조건이 만족하지 않을 때, (if)
#   아래의 조건을 확인하고 (elif)
#   모두 만족하지 않으면 else 문을 실행한다.

score = input("성적 : ")  # "70"
score = int(score)        # 70

# 학점 출력
if score >= 90:
	print("A학점")
elif score >= 80:
	print("B학점")
elif score >= 70:
	print("C학점")
elif score >= 60:
	print("D학점")
else:
	print("F학점")

