from Blog.response import PostResponse
from fastapi import FastAPI, status, HTTPException
from Blog.request import PostCreateRequest, PostUpdateRequest

app = FastAPI(
    title='블로그 API'
    description="FastAPI 입문 실습 과제 - 블로그"
    version='1.0.0'
)

posts =[
    {'id': 1,  'title': 'Python', 'content': 'python 기초다지기'},
    {'id': 2,  'title': 'Html', 'content': '홈페이지 뼈대만들기'},
    {'id': 3,  'title': 'CSS', 'content': '홈페이지 꾸미기'}
]

# 전체 게시글 조회
@app.get(
    '/',
    response_model = list[PostResponse],
    status_code =status.HTTP_200_OK
)
def get_posts_handler():
    return posts

# 단일 게시글 조회
@app.get(
    '/{post_id}',
    response_model=PostResponse,
    status_code=status.HTTP_200_OK
)

def get_post_handler(post_id: int):
    for post in posts:
        if post['id'] == post_id:
            return post
    raise HTTPException(staus_code=status.HTTP_404_NOT_FOUND, detail='post not found')

# 게시글 생성 
@app.post(
    '/',
    response_model=PostResponse,
    status_code=status.HTTP_201_CREATED
)

def create_post_handler(body: PostCreateRequest):
    new_post = {
        'id': len(posts) + 1,
        'title': body.title, 
        'content': body.content,
    }
    posts.append(new_post)

# 게시글 수정
@app.patch(
    '/{post_id}',
    response_model=PostResponse,
    status_code=status.HTTP_200_OK           
)
def update_post_handler(post_id: int, body: PostUpdateRequest):
    for post in posts:
        if post['id'] == post_id:
            if body.title is not None:
                post['title'] = body.title
            if body.content is not None:
                post['content'] = body.concent
            return post
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='post not found')

# 게시글 삭제 
@app.delete(
    '/{post_id}',
    status_code= status.HTTP_204_NO_CONTENT
)

def delete_post_handler(post_id: int):
    for post in posts:
        if post['id']==post_id:
            posts.remove(post)
            return
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='post not found')