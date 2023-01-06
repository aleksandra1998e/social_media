from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session


from app.db.models import Post, User, Like
from app.db.schema import PostCreate, PostUpdate, PostOut


router = APIRouter()


def get_db(request):
    return request.state.db


def get_current_user(request: Request, db: Session = Depends(get_db)):
    """Get current user from request"""
    user_id = request.headers.get("User-ID")
    if not user_id:
        raise HTTPException(status_code=401, detail="Not authenticated")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/posts", response_model=list[PostOut])
def read_posts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    posts = db.query(Post).offset(skip).limit(limit).all()
    return posts


@router.post("/posts", response_model=PostOut)
def create_post(post: PostCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    # Create new post
    new_post = Post(**post.dict(), user_id=user.id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.put("/posts/{id}", response_model=PostOut)
def update_post(id: int, post: PostUpdate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    # Get post by id
    stored_post = db.query(Post).filter(Post.id == id).first()
    if not stored_post:
        raise HTTPException(status_code=404, detail="Post not found")

    # Check if user is the owner of the post
    if stored_post.user_id != user.id:
        raise HTTPException(status_code=403, detail="Forbidden")

    # Update post
    stored_post.title = post.title
    stored_post.content = post.content
    db.commit()
    return stored_post


@router.delete("/posts/{id}")
def delete_post(id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    # Get post by id
    stored_post = db.query(Post).filter(Post.id == id).first()
    if not stored_post:
        raise HTTPException(status_code=404, detail="Post not found")

    # Check if user is the owner of the post
    if stored_post.user_id != user.id:
        raise HTTPException(status_code=403, detail="Forbidden")

    # Delete post
    db.delete(stored_post)
    db.commit()
    return {"message": "Post deleted"}


@router.post("/posts/{id}/like")
def like_post(id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    # Get post by id
    stored_post = db.query(Post).filter(Post.id == id).first()
    if not stored_post:
        raise HTTPException(status_code=404, detail="Post not found")

    # Check if user is not the owner of the post
    if stored_post.user_id == user.id:
        raise HTTPException(status_code=400, detail="Can't like own post")

    # Check if user has already liked the post
    like = db.query(Like).filter(Like.user_id == user.id, Like.post_id == stored_post.id).first()
    if like:
        raise HTTPException(status_code=400, detail="Post already liked")

    # Like post
    new_like = Like(user_id=user.id, post_id=stored_post.id)
    db.add(new_like)
    db.commit()
    return {"message": "Post liked"}


@router.delete("/posts/{id}/like")
def unlike_post(id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    # Get post by id
    stored_post = db.query(Post).filter(Post.id == id).first()
    if not stored_post:
        raise HTTPException(status_code=404, detail="Post not found")

    # Check if user has not already liked the post
    like = db.query(Like).filter(Like.user_id == user.id, Like.post_id == stored_post.id).first()
    if not like:
        raise HTTPException(status_code=400, detail="Post not liked")

    # Unlike post
    db.delete(like)
    db.commit()
    return {"message": "Post unliked"}
