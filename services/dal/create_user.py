from db.utils.with_session import with_session
from models.user import User

def create_user(**user_data):
    return with_session(__create_user, **user_data)

def __create_user(session, **user_data):
    new_user = User(
        **user_data
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

    return user_data
