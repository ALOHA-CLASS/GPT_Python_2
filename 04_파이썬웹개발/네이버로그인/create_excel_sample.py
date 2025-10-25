import pandas as pd

# 샘플 데이터 생성
data = {
    '번호': [1, 2, 3],
    '아이디': ['h850415', 'h850415', 'h850415'],
    '비밀번호': ['123123', '123123', '123123'],
    '게시글 URL': [
        'https://cafe.naver.com/alohaclass/4',
        'https://cafe.naver.com/alohaclass/4',
        'https://cafe.naver.com/alohaclass/4'
    ],
    '댓글내용': [
        '안녕하세요 댓글 내용입니다1',
        '안녕하세요 댓글 내용입니다2',
        '안녕하세요 댓글 내용입니다3'
    ]
}

df = pd.DataFrame(data)
df.to_excel('naver_accounts.xlsx', index=False, engine='openpyxl')

print("엑셀 파일 'naver_accounts.xlsx'가 생성되었습니다.")
print("\n파일 내용:")
print(df.to_string(index=False))