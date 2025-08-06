from db.utils.with_session import with_session
from models.user import User

def create_user():
    return with_session(__create_user)

def __create_user(session):
    new_user = User(
        full_name="Spongebob Squarepants",
        is_guest = True
        # addresses=[Address(email_address="spongebob@sqlalchemy.org")],
    )
    # sandy = User(
    #     name="sandy",
    #     fullname="Sandy Cheeks",
    #     addresses=[
    #         Address(email_address="sandy@sqlalchemy.org"),
    #         Address(email_address="sandy@squirrelpower.org"),
    #     ],
    # )
    # patrick = User(name="patrick", fullname="Patrick Star")
    session.add_all([new_user])
    session.commit()
