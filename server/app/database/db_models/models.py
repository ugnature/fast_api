from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class InstagramUserDBTabelModel(Base):
    __tablename__ = "insta_users"
    user_id = Column(Integer, nullable=False, primary_key=True)
    user_email = Column(String, nullable=False, unique=True)
    user_password = Column(String, nullable=False)
    user_created_at = Column(TIMESTAMP(timezone=True),
                             nullable=False, server_default=text('now()'))
    user_updated_at = Column(TIMESTAMP(timezone=True),
                             nullable=False, server_default=text('CURRENT_TIMESTAMP'))


class InstagramDBTableModel(Base):
    __tablename__ = "insta_posts"

    id = Column(Integer, primary_key=True, nullable=False)
    user_key_id = Column(Integer,  ForeignKey(
        "insta_users.user_id", ondelete="CASCADE"), nullable=False)
    post_title = Column(String, nullable=False)
    post_content = Column(String, nullable=False)
    post_published = Column(Boolean, server_default='TRUE', nullable=False)
    post_created_at = Column(TIMESTAMP(timezone=True),
                             nullable=False, server_default=text('now()'))
    # here we added a new feature
    # we created a relatioship with userTable so who ever access the post can also also see the username and userdetail
    # but to see this in result we have to go in to response scheema and add this owner map
    owner = relationship("InstagramUserDBTabelModel")


class voteDBTable(Base):
    __tablename__ = "votes"

    vote_post_id = Column(Integer, ForeignKey(
        "insta_posts.id", ondelete="CASCADE"), primary_key=True)
    vote_user_id = Column(Integer, ForeignKey(
        "insta_users.user_id",  ondelete="CASCADE"), primary_key=True)
