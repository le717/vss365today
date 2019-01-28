from sqlalchemy.orm import sessionmaker

from src.models import Emails, Tweets, Givers
from src.core.helpers import create_db_connection, load_env_vals


__all__ = [
    "add_tweet_to_db",
    "get_all_emails",
    "get_all_givers",
    "get_latest_tweet",
    "get_tweet_by_date",
    "get_tweets_by_giver"
]


def __connect_to_db_sqlalchemy():
    # Connect to the database
    config = load_env_vals()
    _, db = create_db_connection(config)

    # Make a database session
    Session = sessionmaker(bind=db)
    return Session()


def get_all_emails() -> list:
    # Get all the emails
    session = __connect_to_db_sqlalchemy()
    all_emails = session.query(Emails).all()
    session.close()
    return all_emails


def get_uid_by_handle(handle: str, in_flask: bool = True):
    # Use the appropriate database api depending on
    # if we are inside a Flask context or not
    if in_flask:
        return Givers.query.filter_by(handle=handle).first()
    else:
        session = __connect_to_db_sqlalchemy()
        uid = session.query(Givers.uid).filter_by(handle=handle).first()
        session.close()
        return uid


def get_latest_tweet(in_flask: bool = True):
    # Use the appropriate database api depending on
    # if we are inside a Flask context or not
    if in_flask:
        return Tweets.query.order_by(Tweets.date.desc()).first_or_404()
    else:
        session = __connect_to_db_sqlalchemy()
        tweet = session.query(Tweets).order_by(Tweets.date.desc()).first()
        session.close()
        return tweet


def get_all_givers():
    return Givers.query.distinct().all()


def get_tweets_by_month(month: str):
    pass
    # return Tweets.query.filter(Tweets.date.month == 1).all()


def get_tweets_by_giver(handle: str):
    uid = get_uid_by_handle(handle)
    return Tweets.query.filter_by(uid=uid.uid).all()


def get_tweet_by_date(date: str):
    return Tweets.query.filter(Tweets.date == date).first_or_404()


def add_giver_to_db(giver_dict: dict):
    """Add a giver to the database."""
    giver = Givers(
        uid=giver_dict["uid"],
        handle=giver_dict["handle"]
    )
    session = __connect_to_db_sqlalchemy()
    session.add(giver)
    session.commit()
    session.close()


def add_tweet_to_db(tweet_dict: dict):
    """Add a tweet to the database."""
    tweet = Tweets(
        tweet_id=tweet_dict["tweet_id"],
        date=tweet_dict["date"],
        uid=tweet_dict["uid"],
        content=tweet_dict["content"],
        word=tweet_dict["word"]
    )
    session = __connect_to_db_sqlalchemy()
    session.add(tweet)
    session.commit()
    session.close()
