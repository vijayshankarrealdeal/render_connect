from __future__ import annotations
from datetime import datetime
from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel
from sqlalchemy import UniqueConstraint

# ---------------------------
# Linking table for Many-to-Many relationship between Post and Tag
# ---------------------------
class PostTag(SQLModel, table=True):
    post_id: int = Field(foreign_key="posts.post_id", primary_key=True)
    tag_id: int = Field(foreign_key="tags.tag_id", primary_key=True)


# ---------------------------
# Users Table
# ---------------------------
class User(SQLModel, table=True):
    __tablename__ = "users"
    
    user_id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(sa_column_kwargs={"unique": True})
    email: str = Field(sa_column_kwargs={"unique": True})
    hashed_password: str
    bio: Optional[str] = None
    profile_picture_url: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now())
    updated_at: datetime = Field(default_factory=datetime.now())
    
    # Relationships
    posts: List[Post] = Relationship(back_populates="user")
    comments: List[Comment] = Relationship(back_populates="user")
    likes: List[Like] = Relationship(back_populates="user")
    sent_messages: List[Message] = Relationship(
        back_populates="sender", sa_relationship_kwargs={"foreign_keys": "[Message.sender_id]"}
    )
    received_messages: List[Message] = Relationship(
        back_populates="receiver", sa_relationship_kwargs={"foreign_keys": "[Message.receiver_id]"}
    )
    following: List[Follow] = Relationship(
        back_populates="follower", sa_relationship_kwargs={"foreign_keys": "[Follow.follower_id]"}
    )
    followers: List[Follow] = Relationship(
        back_populates="followed", sa_relationship_kwargs={"foreign_keys": "[Follow.followed_id]"}
    )


# ---------------------------
# Posts Table
# ---------------------------
class Post(SQLModel, table=True):
    __tablename__ = "posts"
    
    post_id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.user_id")
    content: str
    created_at: datetime = Field(default_factory=datetime.now())
    updated_at: datetime = Field(default_factory=datetime.now())
    
    # Relationships
    user: Optional[User] = Relationship(back_populates="posts")
    comments: List[Comment] = Relationship(back_populates="post")
    likes: List[Like] = Relationship(back_populates="post")
    media: List[Media] = Relationship(back_populates="post")
    tags: List[Tag] = Relationship(back_populates="posts", link_model=PostTag)


# ---------------------------
# Comments Table
# ---------------------------
class Comment(SQLModel, table=True):
    __tablename__ = "comments"
    
    comment_id: Optional[int] = Field(default=None, primary_key=True)
    post_id: int = Field(foreign_key="posts.post_id")
    user_id: int = Field(foreign_key="users.user_id")
    content: str
    created_at: datetime = Field(default_factory=datetime.now())
    
    # Relationships
    user: Optional[User] = Relationship(back_populates="comments")
    post: Optional[Post] = Relationship(back_populates="comments")


# ---------------------------
# Likes Table
# ---------------------------
class Like(SQLModel, table=True):
    __tablename__ = "likes"
    __table_args__ = (UniqueConstraint("post_id", "user_id", name="unique_like"),)
    
    like_id: Optional[int] = Field(default=None, primary_key=True)
    post_id: int = Field(foreign_key="posts.post_id")
    user_id: int = Field(foreign_key="users.user_id")
    created_at: datetime = Field(default_factory=datetime.now())
    
    # Relationships
    user: Optional[User] = Relationship(back_populates="likes")
    post: Optional[Post] = Relationship(back_populates="likes")


# ---------------------------
# Follows Table
# ---------------------------
class Follow(SQLModel, table=True):
    __tablename__ = "follows"
    
    follower_id: int = Field(foreign_key="users.user_id", primary_key=True)
    followed_id: int = Field(foreign_key="users.user_id", primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now())
    
    # Relationships
    follower: Optional[User] = Relationship(
        back_populates="following", sa_relationship_kwargs={"foreign_keys": "[Follow.follower_id]"}
    )
    followed: Optional[User] = Relationship(
        back_populates="followers", sa_relationship_kwargs={"foreign_keys": "[Follow.followed_id]"}
    )


# ---------------------------
# Messages Table
# ---------------------------
class Message(SQLModel, table=True):
    __tablename__ = "messages"
    
    message_id: Optional[int] = Field(default=None, primary_key=True)
    sender_id: int = Field(foreign_key="users.user_id")
    receiver_id: int = Field(foreign_key="users.user_id")
    content: str
    sent_at: datetime = Field(default_factory=datetime.now())
    read_at: Optional[datetime] = None
    
    # Relationships
    sender: Optional[User] = Relationship(
        back_populates="sent_messages", sa_relationship_kwargs={"foreign_keys": "[Message.sender_id]"}
    )
    receiver: Optional[User] = Relationship(
        back_populates="received_messages", sa_relationship_kwargs={"foreign_keys": "[Message.receiver_id]"}
    )


# ---------------------------
# Media Table
# ---------------------------
class Media(SQLModel, table=True):
    __tablename__ = "media"
    
    media_id: Optional[int] = Field(default=None, primary_key=True)
    post_id: int = Field(foreign_key="posts.post_id")
    media_url: str
    media_type: Optional[str] = None  # e.g., 'image', 'video'
    created_at: datetime = Field(default_factory=datetime.now())
    
    # Relationships
    post: Optional[Post] = Relationship(back_populates="media")


# ---------------------------
# Tags Table
# ---------------------------
class Tag(SQLModel, table=True):
    __tablename__ = "tags"
    
    tag_id: Optional[int] = Field(default=None, primary_key=True)
    tag_name: str = Field(sa_column_kwargs={"unique": True})
    
    # Relationships
    posts: List[Post] = Relationship(back_populates="tags", link_model=PostTag)
