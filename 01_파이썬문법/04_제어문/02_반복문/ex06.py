# 가위바위보 게임
# choice() : 리스트 요소 중 하나를 랜덤으로 선택
# 컴퓨터      : 가위 바위 보를 랜덤으로 선택
# 나          : 가위 바위 보를 입력
# 내가 질때 까지 게임을 계속 진행
# 가위바위보 게임 프로그램 만들어보기
import random
choices = ['가위', '바위', '보']
user = ''
win = True  # 내가 이겼는지 여부

while win:
    computer = random.choice(choices)
    user = input('가위바위보 입력: ')
    print("컴퓨터 : {}".format(computer))
    print("나     : {}".format(user))

    # 이겼을 때
    win1 = (user == '가위' and computer == '보')
    win2 = (user == '바위' and computer == '가위')
    win3 = (user == '보' and computer == '바위')

    if user == computer:
        print("비겼습니다!")
    elif win1 or win2 or win3:
        print("이겼습니다!")
    else:
        win = False
        print("졌습니다!")
